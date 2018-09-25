from __future__ import unicode_literals

from django.db import models
from Disease.models import Disease


class Evidence(models.Model):

    """
        This model is where the evidence will be stored
    """

    name = models.CharField(max_length=255)

    linked_disease = models.ForeignKey(
                        Disease,related_name="linked_disease",
                        blank=True,null=True,
                        help_text="If an evidence is also a disease,\
                        please link it here.")

    question = models.CharField(max_length=500, blank=True,null=True,
                        help_text="When an evidence is not linked to a \
                        disease, this field is required.")

    image = models.ImageField(upload_to='media/', \
                        default='media/None/no-img.jpg',blank=True)
    
    archived = models.BooleanField(default=False)
   
    def __str__(self):
        return "{} - {}".format(self.id,self.name)

    class Meta:
        verbose_name = "Evidence"
        verbose_name_plural = "Evidences"


