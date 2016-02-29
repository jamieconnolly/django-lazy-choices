from django.db import models


class Poet(models.Model):
    name = models.CharField(max_length=100)


class Poem(models.Model):
    poet = models.ForeignKey(Poet, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
