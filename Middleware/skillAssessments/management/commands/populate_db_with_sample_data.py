import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from skillAssessments.models import Category, Skill, User, Assessment, SkillScore
from coins.models import Job

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of assessments to create')

    def handle(self, *args, **kwargs):
        # Pull in arguments
        count = kwargs['count']
        def random_date_within_last_year():
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            return start_date + (end_date - start_date) * random.random()

        # Get Users
        user_objs = User.objects.all()

        # Get Jobs
        job_objs = Job.objects.all()

        # Get Skills
        skill_objs = Skill.objects.all()

        # Create Assessments and SkillScores
        for _ in range(count):  # Create 10 assessments
            user = random.choice(user_objs)
            assessor = random.choice([u for u in user_objs if u != user])
            job = random.choice(job_objs)
            recorded_at = random_date_within_last_year()
            assessment = Assessment.objects.create(user=user, assessor=assessor, job=job, recorded_at=recorded_at)

            for _ in range(random.randint(1, 10)):
                SkillScore.objects.create(
                    assessment=assessment,
                    skill=random.choice(skill_objs),
                    score=random.randint(1, 4),
                    comments='Sample comment'
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample data'))

