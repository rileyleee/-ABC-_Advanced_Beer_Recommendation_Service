from django.db import models

class Beer(models.Model):
    id = models.AutoField(primary_key=True)
    big_kind = models.CharField(max_length=100)
    kind = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    brewery = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    abv = models.CharField(max_length=100)
    average = models.CharField(max_length=100)
    ratings = models.CharField(max_length=100)
    reviews = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    body = models.FloatField()
    sweet = models.FloatField()
    fruity = models.FloatField()
    hoppy = models.FloatField()
    malty = models.FloatField()
