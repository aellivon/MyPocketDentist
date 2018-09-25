from __future__ import unicode_literals
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from Disease.models import Disease
from Evidence.models import Evidence

class Rule(models.Model):
    """
        This model is where the rule will be stored
    """

    disease = models.ForeignKey(Disease,related_name="diseases")

    certainty_factor = models.FloatField( \
        help_text="This ranges from -100 to 100.  \
                    <br/> Positive values means that the evidence confirms or \
                    supports the disease.  \
                    <br/> Negative values means that the evidence does  \
                    not support the disease.", \
        default=0,validators=[MinValueValidator(-100), MaxValueValidator(100)])

    Condition_Order = models.CharField(\
        help_text="This field will be the basis of the condition's \
                    hierarchy/order, If two or more evidence exists in a rule." + \
                    "<br/>  This statement only accepts the corresponding \
                    'evidence number', parenthesis , an 'or' (disjunction), \
                    and an 'and' (conjuction)." +  \
                    "<br/> e.g. 24 and 34" \
                    "<br/> **Ignore this if you have only one evidence in a rule."
            ,max_length=500,default=None,blank=True)
    

    archived = models.BooleanField(default=False)

    def __str__(self):
           return "{}-{}".format(self.id,self.disease)

    class Meta:
        verbose_name = "Rule"
        verbose_name_plural = "Rules"



class RulesEvidence(models.Model):
    """
        This model is where the rule's disease will be stored
    """

    rule = models.ForeignKey(Rule,related_name="rules")
    evidence = models.ForeignKey(Evidence,related_name="evidences")

    class Meta:
        verbose_name = "Rules Evidence"
        verbose_name_plural = "Rules Evidences"

    def __str__(self):
           return "{}".format(self.id)

