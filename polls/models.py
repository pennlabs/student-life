from django.db import models

class Poll(models.Model):
    question_text = models.CharField(max_length=255)
    org_author = models.CharField(max_length=255) #TODO: turn this into a 1-1 relationship with org user acct
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
       super().save(*args, **kwargs)

    def __str__(self):
        return "{}: {}".format(self.pk, self.question_text)

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
       super().save(*args, **kwargs)

    def __str__(self):
        return "{}: {} ({} votes)".format(self.pk, self.option_text, self.votes)