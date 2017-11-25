from django.db import models


class Item(models.Model):

    name = models.CharField(blank=False, max_length=150)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cover = models.URLField()


    def __str__(self):
        return self.name
