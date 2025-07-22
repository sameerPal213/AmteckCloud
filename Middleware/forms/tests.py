from django.test import TestCase
from .models import SafetyTaskAnalysisResponse

# Create your tests here.
class SafetyTaskAnalysisResponseTest(TestCase):
    def test_create_response(self):
        """Test if a response can be created properly"""
        response = SafetyTaskAnalysisResponse.objects.create()
