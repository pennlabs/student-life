from django.db import models

class Poll(models.Model):
    question = models.CharField(max_length=255)
    org_author = models.CharField(max_length=255) #TODO: turn this into a 1-1 relationship with org user acct
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
       super().save(*args, **kwargs)

    def __str__(self):
        return "{}: {}".format(self.pk, self.question)