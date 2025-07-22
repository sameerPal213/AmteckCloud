from django.core.management.base import BaseCommand
from django.db.models import Count
from coins.models import Job


class Command(BaseCommand):
    help = 'Delete duplicate records based on job_num'

    def handle(self, *args, **options):
        duplicate_ids = Job.objects.values('job_num').annotate(count=Count('id')).filter(count__gt=1)
        duplicate_record_ids = [item['id'] for item in Job.objects.filter(job_num__in=duplicate_ids.values('job_num')).values('id')]
        Job.objects.filter(id__in=duplicate_record_ids).delete()        
        
        self.stdout.write(self.style.SUCCESS('Duplicate records deleted successfully'))
