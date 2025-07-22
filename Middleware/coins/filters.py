import django_filters
from .models import Job


class JobFilter(django_filters.FilterSet):
    job_name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Job
        fields = ['job_num', 'job_name', 'latitude', 'longitude', 'job_desc_1']
