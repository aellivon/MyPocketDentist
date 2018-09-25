from rest_framework import serializers
from Evidence.models import Evidence


class QuestionSerializer(serializers.ModelSerializer):
    """
        This class is a serializer for the evidence model that will only return
            the id and the question.
    """
    class Meta:
        model = Evidence
        fields = ('id','question','image')


