from django.shortcuts import render
from rest_framework.views import APIView  # returns API Data
from rest_framework.response import Response # returns response

# Models

from Disease.models import Disease

from Evidence.models import(
        Evidence
    )

# Serializers

from Disease.serializers import (
        MultipleDiseaseSerializer,
        DiseaseProfileSerializer,
        EvidenceProfileSerializer
   )


from rest_framework.views import APIView  # returns API Data


class GetListOfAllDisease(APIView):


    def get(self,request):
        """
            This function will display all the disease.

            Args: None.

            Returns: serializer.data (json) - A json response of
                        the all the disease.
        """
        disease = Disease.objects.filter(archived=False)

        serializer = MultipleDiseaseSerializer(
            disease,many=True)
        
        return Response(serializer.data)

        
class ShowDiseaseProfile(APIView):


    def get(self,request,profile_id):

        """
            This function will display the specified disease profile.

            Args: profile_id (int) - Represents id of the profile that the class 
                    will be getting.

            Returns: data (json) - A json response of the details of the profile.
        """

        disease_profile = Disease.objects.filter(id=profile_id)
            
        profile_serializer = DiseaseProfileSerializer(
            disease_profile,many=True)

        evidence_profile = Evidence.objects.filter(
                evidences__rule__archived=False,
                evidences__rule__disease__id=profile_id)

        evidence_serializer = EvidenceProfileSerializer(
             evidence_profile,many=True)
        
        data = { 'disease': profile_serializer.data,
            'evidence': evidence_serializer.data }

        return Response(data)


class SearchDiseaseProfile(APIView):


    def get(self,request,search):
        """
            This fucntion will display all the searched diseases.

            Args: search (string) - Represents the searched value of the user.

            Returns: serializer.data (json) - A json response of the question or 
                        the list of result base on the disease
        """
        list_of_all_disease = (Disease.objects.filter(
                archived=False,name__icontains=search)).distinct()
            

        serializer = MultipleDiseaseSerializer(
            list_of_all_disease,many=True)
        return Response(serializer.data)