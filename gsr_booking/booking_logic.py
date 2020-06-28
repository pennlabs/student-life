import datetime
import math
import random

import requests
from gsr_booking.models import GSRBookingCredentials
from django.contrib.auth import get_user_model
MIN_SLOT_HRS = 0.5  # the minimum booking allowed per person
User = get_user_model()

def book_rooms_for_group(group, rooms, requester_pennkey):
    """ makes a request to labs api server to book rooms for group """
    members = group.get_pennkey_active_members()
    room_json_array = []
    complete_success = True
    partial_success = False
    error = None
    fatal_error = False  # if false, don't book the remaining rooms, but still return them

    if len(members) < 1:
        result_json = construct_result_json_obj(
            [],
            False,
            False,
            "No members in the group have enabled their pennkey to be used for group bookings",
        )
        return result_json

    # randomize order, and put requester first in the order
    for (i, member) in enumerate(members):  # puts the requester as the first person
        if member["username"] == requester_pennkey:
            temp = members[0]
            members[0] = member
            members[i] = temp
            break

    # call book_room_for_group on each room
    # TODO: pass on failed_members from one request to the other to avoid wasting calls
    for room in rooms:
        is_wharton = room["is_wharton"]
        roomid = room["room"]
        lid = room["lid"]
        start = datetime.datetime.fromisoformat(room["start"])
        end = datetime.datetime.fromisoformat(room["end"])

        if not fatal_error:
            (booking_slots, next_start, next_end, error, room_fatal_error) = book_room_for_group(
                members, is_wharton, roomid, lid, start, end
            )
        else:
            room_fatal_error = None
            booking_slots = []
            next_start = start
            next_end = end

        (room_json, room_complete_success, room_partial_success) = construct_room_json_obj(
            booking_slots, lid, roomid, end, next_start, next_end
        )
        room_json_array.append(room_json)
        complete_success = complete_success and room_complete_success and (error is None)
        partial_success = partial_success or room_partial_success
        fatal_error = fatal_error or room_fatal_error

    result_json = construct_result_json_obj(
        room_json_array, partial_success, complete_success, error
    )
    return result_json


def book_room_for_group(members, is_wharton, room, lid, start, end):
    """returns (booking_slots, next_start, next_end, error, isFatalError)"""
    MAX_SLOT_HRS = 1.5  # the longest booking allowed per person
    if not is_wharton:
        MAX_SLOT_HRS = 2.0

    next_start = start
    next_end = min(end, next_start + datetime.timedelta(hours=MAX_SLOT_HRS))

    # loop through each member, and attempt to book on their behalf
    booking_slots = []  # booking_slots is an array of (i.e. 30 minute) booking_slots
    failed_members = []  # store the members w/ failed bookings in here
    error = None
    for member in members:
        session_id = get_session_id_for_user(member['user'])
        
        if (is_wharton and session_id == None) or (not is_wharton and member["user__email"] == ""):
            continue # this member cannot be used for booking b/c missing info
        if next_end - next_start < datetime.timedelta(hours=MIN_SLOT_HRS):
            break

        # make 'blind-booking' request to labs-api-server first
        try:
            success = book_room_for_user(
                    room, lid, next_start.isoformat(), next_end.isoformat(), member["user__email"], session_id
                )
            if success:
                new_booking_slots = split_booking(
                    next_start, next_end, member["username"], True
                )
                booking_slots.extend(new_booking_slots)

                next_start = next_end
                next_end = min(end, next_start + datetime.timedelta(hours=MAX_SLOT_HRS))
            else:
                failed_members.append(member)
        except BookingError as e:
            error = e
            if is_fatal_error(e):
                return (booking_slots, next_start, next_end, error, True)
            else:
                failed_members.append(member)

    # if unbooked slots still remain, loop through each member again
    # but get reservation credits first to see how much we can book
    for member in failed_members:
        session_id = get_session_id_for_user(member['user'])

        if next_end - next_start < datetime.timedelta(hours=MIN_SLOT_HRS):
            break  # booked everything already
        if (is_wharton and session_id == None) or (not is_wharton and member["user__email"] == ""):
            continue # this member cannot be used for booking b/c missing info

        # calculate number of credits already used via getReservations
        (success, used_credit_hours) = get_used_booking_credit_for_user(
            lid, member["user__email"], session_id
        )
        remaining_credit_hours = MAX_SLOT_HRS - used_credit_hours
        rounded_remaining_credit_hours = math.floor(2 * remaining_credit_hours) / 2
        if success and remaining_credit_hours >= MIN_SLOT_HRS:
            next_end = min(
                end, next_start + datetime.timedelta(hours=rounded_remaining_credit_hours),
            )
            try:
                success = book_room_for_user(
                    room,
                    lid,
                    next_start.isoformat(),
                    next_end.isoformat(),
                    member["user__email"],
                    session_id
                )
                if success:
                    new_booking_slots = split_booking(
                        next_start, next_end, member["username"], True
                    )
                    booking_slots.extend(new_booking_slots)

                    next_start = next_end
                    next_end = min(end, next_start + datetime.timedelta(hours=MAX_SLOT_HRS))
            except BookingError as e:
                error = e
                if is_fatal_error(e):
                    return (booking_slots, next_start, next_end, error, True)
    if next_start >= end:
        # even if there was a daily limit error, delete it if all rooms were booked
        error = None
    return (booking_slots, next_start, next_end, error, False)


def is_fatal_error(error):
    """
    fatal errors should halt the booking algorithm right away, and return the current bookings
    non-fatal errors include running out of reservation credits; everything else is considered a fatal error
    """
    if error is not None:
        error = str(error).lower()
        if "daily limit" in error or "reservation limit" in error:
            return False
        return True
    return False


def construct_result_json_obj(room_json_array, partial_success, complete_success, error):
    result_json = {
        "complete_success": complete_success,
        "partial_success": partial_success,
        "rooms": room_json_array,
    }
    # handle potential error
    if error is not None:
        if "not a valid".lower() in str(error).lower():
            result_json["error"] = "Attempted to book for an invalid time slot"
        elif "daily limit".lower() in str(error).lower():
            result_json["error"] = "Group does not have sufficient booking credits"
        else:
            result_json["error"] = str(error)
    elif not complete_success:
        result_json["error"] = "Group does not have sufficient booking credits"
    elif complete_success:
        result_json["partial_success"] = True  # in case, 0 bookings were made
    return result_json


def construct_room_json_obj(succesful_booking_slots, lid, room, end, next_start, next_end):
    """
    Takes in a set of booking_slots and constructs a room JSON object from them. E.g.
    room_json = {
        "lid": "2587",
        "room": "16993",
        "bookings": [
            {
                "start": "2020-03-06T18:00:00-05:00",
                "end": "2020-03-06T18:30:00-05:00",
                "pennkey": rehaan,
                "booked": true
            }
        ]
    }
    Returns (room_json, complete_success, partial_success)
    """
    booking_slots = succesful_booking_slots
    complete_success = next_end - next_start < datetime.timedelta(hours=MIN_SLOT_HRS)
    partial_success = len(booking_slots) > 0

    # add failed bookings to bookings
    failed_booking_slots = split_booking(next_start, end, None, False)
    booking_slots.extend(failed_booking_slots)

    room_json = {"lid": lid, "room": room, "bookings": booking_slots}

    return (room_json, complete_success, partial_success)


def get_used_booking_credit_for_user(lid, email, session_id):
    """ returns a user's used booking credit (in hours) for a specific building (lid) """
    reservations_url = "https://api.pennlabs.org/studyspaces/reservations"
    if lid == 1:
        reservations_url = reservations_url + "?sessionid=" + session_id
    else:
        reservations_url = reservations_url + "?email=" + email
    try:
        r = requests.get(reservations_url)
        if r.status_code == 200:
            resp_data = r.json()
            reservations = resp_data["reservations"]
            used_credit_hours = 0
            for reservation in reservations:
                from_date = datetime.datetime.fromisoformat(reservation["fromDate"])
                to_date = datetime.datetime.fromisoformat(reservation["toDate"])
                reservation_hours = (to_date - from_date).total_seconds() / 3600
                if reservation["lid"] == lid and reservation_hours >= MIN_SLOT_HRS:
                    used_credit_hours += reservation_hours
            return (True, used_credit_hours)
    except requests.exceptions.RequestException as e:
        print(e)
    return (False, 0)


def split_booking(start, end, pennkey, booked):
    """
    splits a booking into smaller bookings (of min_slot_hrs) for displaying to user
    """
    bookings = []
    temp_start = start
    temp_end = temp_start + datetime.timedelta(hours=MIN_SLOT_HRS)
    while end - temp_start >= datetime.timedelta(hours=MIN_SLOT_HRS):
        booking_obj = {
            "start": temp_start.isoformat(),
            "end": temp_end.isoformat(),
            "booked": booked,
        }
        if pennkey is not None:
            booking_obj["pennkey"] = pennkey
        bookings.append(booking_obj)
        temp_start = temp_end
        temp_end += datetime.timedelta(hours=MIN_SLOT_HRS)
    return bookings

def book_huntsman_room_for_user(room, lid, start, end, session_id):
    """
    Tries to make a booking for an individual user,
    and returns success or not (and the error) in a tuple
    """

    BOOKING_URL = "https://api.pennlabs.org/studyspaces/book"
    form_data = {
        "room": room,
        "lid": lid,
        "start": start,
        "end": end,
        "sessionid": session_id
    }

    try:
        r = requests.post(BOOKING_URL, data=form_data)
        if r.status_code == 200:
            resp_data = r.json()
            if "error" in resp_data and resp_data["error"] is not None:
                raise BookingError(resp_data["error"])
            return resp_data["results"]
    except requests.exceptions.RequestException as e:
        print("error: " + str(e))
    return False

def book_room_for_user(room, lid, start, end, email, session_id):
    """
    Tries to make a booking for an individual user,
    and returns success or not (and the error) in a tuple
    """
    BOOKING_URL = "https://api.pennlabs.org/studyspaces/book"
    form_data = {
        "room": room,
        "lid": lid,
        "start": start,
        "end": end
    }
    if lid == 1:
        form_data['sessionid'] = session_id
    else:
        new_form_data = {
            "firstname": "Group GSR User",
            "lastname": "Group GSR User",
            "groupname": "Group GSR",
            "size": "2-3",
            "phone": "2158986533",
            "email": email
        }
        form_data = {**form_data, **new_form_data} #add new form data
    try:
        r = requests.post(BOOKING_URL, data=form_data)
        if r.status_code == 200:
            resp_data = r.json()
            if "error" in resp_data and resp_data["error"] is not None:
                raise BookingError(resp_data["error"])
            return resp_data["results"]

    except requests.exceptions.RequestException as e:
        print("error: " + str(e))
    return False

def get_session_id_for_user(user_pk):
    """ Returns a user's session id (for huntsman bookings) if it exists, or None otherwise """
    try:
        cred = GSRBookingCredentials.objects.get(user=user_pk)
        return cred.session_id
    except GSRBookingCredentials.DoesNotExist:
        return None

class BookingError(Exception):
    def __init__(self, error_str):
        self.error_str = error_str

    def __str__(self):
        return self.error_str
