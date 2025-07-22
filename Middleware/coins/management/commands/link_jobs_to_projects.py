from django.core.management.base import BaseCommand
from django.db import transaction
from coins.models import Job, Project

class Command(BaseCommand):
    help = 'Link Jobs to Projects based on job_num and pij_dispno'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            jobs = Job.objects.all()
            for job in jobs:
                try:
                    project = Project.objects.get(pij_dispno=job.job_num)
                    project.job_set.add(job)
                    self.stdout.write(self.style.SUCCESS(f'Successfully linked Job {job.job_num} to Project {project.pij_dispno}'))
                except Project.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'No Project found for Job {job.job_num}'))
