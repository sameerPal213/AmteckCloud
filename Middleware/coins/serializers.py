from rest_framework import serializers
from .models import Job, Section, Activity

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['job_num', 'job_name', 'latitude', 'longitude', 'job_desc_1',
            'id',
        ]


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['jcs_section', 'job_num', 'jcs_desc']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['jca_activity', 'jja_desc', 'job_num']
