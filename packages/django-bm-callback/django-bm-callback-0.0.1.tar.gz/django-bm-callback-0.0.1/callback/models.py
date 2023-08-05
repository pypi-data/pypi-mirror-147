from django.db import models


class Callback(models.Model):

    name = models.CharField("Name", max_length=255)

    phone = models.CharField('Phone', max_length=255)

    descriptions = models.TextField('Descriptions', max_length=1000)

    executed = models.BooleanField('Executed', default=False)

    outstanding = models.BooleanField('Outstanding', default=False)

    # yorchoices = (('executed', "EXECUTED"),
    #     ('outstanding', "OUTSTANDING"))
    #
    # choice = models.CharField(max_length=250, choices=yorchoices)


