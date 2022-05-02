from django.db import models


class Games(models.Model):

    game_type = models.ForeignKey("Game_Type", on_delete=models.CASCADE)
    title = models.TextField()
    maker = models.TextField()
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    number_of_players = models.IntegerField()
    skill_level = models.TextField()