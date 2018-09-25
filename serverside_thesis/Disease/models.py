from __future__ import unicode_literals

from django.db import models


class Disease(models.Model):
    """
        This model is where the disease will be stored
    """

    name = models.CharField(max_length=255)
    details = models.CharField(max_length=500,blank=True)
    advise = models.CharField(max_length=500,blank=True)
    cause = models.CharField(max_length=500,blank=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Disease"
        verbose_name_plural = "Diseases"