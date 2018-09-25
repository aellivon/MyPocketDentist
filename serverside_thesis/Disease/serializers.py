from rest_framework import serializers
from Disease.models import Disease
from Evidence.models import Evidence


class MultipleDiseaseSerializer(serializers.ModelSerializer):
    """
        This class is a serializer for the disease model that will only return
            id, name, and advise
    """
    class Meta:
        model = Disease 
        fields = ('id','name','advise','details')


class EvidenceProfileSerializer(serializers.ModelSerializer):
   
    """
         This class is a serializer for the disease model that will only return
            name, and evidence_type
    """

    class Meta:
        model = Evidence 
        fields = ('name','image')


class DiseaseProfileSerializer(serializers.ModelSerializer):
    """
        This class is a serializer for the disease model that will only return
            name, and advise, cause, and details
    """

    class Meta:
        model = Disease 
        fields = ('name','advise','cause','details')