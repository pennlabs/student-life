from django.db import models

class LaundryHall(models.Model):
    LOCATION_QUAD = "QUAD"
    LOCATION_KCEH = "KCEH"
    LOCATION_NCH = "NCH"
    LOCATION_HILL = "HILL"
    LOCATION_SANSOM = "SAMSON"
    LOCATION_STOUFFER = "STOUFFER"
    LOCATION_HARNWELL = "HARNWELL"
    LOCATION_GREGORY = "GREGORY"
    LOCATION_HARRISON = "HARRISON"
    LOCATION_DUBOIS = "DUBOIS"
    LOCATION_RODIN = "RODIN"
    LOCATION_CHOICES = [
        (LOCATION_QUAD, "Quad"),
        (LOCATION_KCEH, "KCECH"),
        (LOCATION_NCH, "New College House"),
        (LOCATION_HILL, "Hill"),
        (LOCATION_SANSOM, "Sansom"),
        (LOCATION_STOUFFER, "Stouffer"),
        (LOCATION_HARNWELL, "Harnwell"),
        (LOCATION_GREGORY, "Gregory"),
        (LOCATION_HARRISON, "Harrison"),
        (LOCATION_DUBOIS, "DuBois"),
        (LOCATION_RODIN, "Rodin"),
    ]

    name = models.TextField()
    hall = models.CharField(max_length=17, choices = LOCATION_CHOICES)
    total_washers = models.IntegerField(default=0, null=False)
    total_dryers = models.IntegerField(default=0, null=False)


class LaundrySnapshot(models.Model):
    hall = models.ForeignKey(LaundryHall, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    washers_available = models.IntegerField()
    dryers_available = models.IntegerField() 
    
