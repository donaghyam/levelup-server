from django.db import models


class Events(models.Model):

    game = models.ForeignKey("Games", on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)