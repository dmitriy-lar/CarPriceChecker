from django.db import models


class Film(models.Model):
    title = models.CharField(max_length=256, null=False, blank=False)
    last_rating = models.CharField(max_length=6, null=True, blank=True)
    last_time_checked = models.DateTimeField()

    def __str__(self):
        return self.title
