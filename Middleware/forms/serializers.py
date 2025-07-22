from rest_framework import serializers
from .models import SafetyTaskAnalysisResponse


class SafetyTaskAnalysisResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyTaskAnalysisResponse
        fields = ['id', 'date', 'location_of_work']
