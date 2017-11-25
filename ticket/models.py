from django.db import models
from shop.models import Item


class Status(models.Model):
    ACCEPTED = 1
    REJECTE = 2
    PENDING = 3
    FAILED = 4

    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'

    def __str__(self):
        return self.name


class Ticket(models.Model):

    items = models.ManyToManyField(Item)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.ForeignKey(Status)

    def __str__(self):
        return self.pk
