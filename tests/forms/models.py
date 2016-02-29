from django.db import models


class Poet(models.Model):
    name = models.CharField(max_length=100)


class Poem(models.Model):
    poet = models.ForeignKey(Poet, models.CASCADE)
    name = models.CharField(max_length=100)
