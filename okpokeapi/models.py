from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=50)

class Move(models.Model):
    name = models.CharField(max_length=50)
    power = models.IntegerField()

class Pokemon(models.Model):
    name = models.CharField(max_length=50)
    order = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    types = models.ManyToManyField(Type, related_name='pokemons')
    moves = models.ManyToManyField(Move, related_name='pokemons')
