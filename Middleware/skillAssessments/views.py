from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Avg, F, ExpressionWrapper, FloatField, Max
from django.db.models.functions import TruncMonth
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from coins.models import Job
from .models import Assessment, Category, Skill, User
from .forms import SkillForm, UserForm, AssessmentForm, get_ScoreFormSet
from .filters import SkillFilter
from .serializers import SkillSerializer
from collections import defaultdict
from rest_framework import generics
import json

# Create your views here.
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'user_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # All users
        context['users_info'] = User.objects.annotate(
            # count of skills assesses not on self assessments
            skills_assessed=Count('assessments', filter=Q(assessments__is_self_assessment=False)),
            # average scores excluding 0 where not a self assessment
            average_score=Avg('assessments__scores__score', filter=Q(assessments__scores__score__gt=0, assessments__is_self_assessment=False)),
            self_assessments=Count('assessments', filter=Q(assessments__is_self_assessment=True)),
            most_recent_assessment=Max('assessments__recorded_at')
        ).filter(Q(skills_assessed__gt=0) | Q(self_assessments__gt=0)) # only show users with scores

        # Get the count of users with scores and users without scores
        users_with_scores = User.objects.annotate(num_scores=Count('assessments')).filter(num_scores__gt=0).count()
        users_without_scores = User.objects.annotate(num_scores=Count('assessments')).filter(num_scores=0).count()

        # Prepare the data for chart.js
        context['chart_data'] = {
            'labels': ['Users with Scores', 'Users without Scores'],
            'datasets': [{
                'data': [users_with_scores, users_without_scores],
                'backgroundColor': ['#ff9999', '#66b3ff']
            }]
        }
        
        # Aggregate assessments by month
        assessments_per_month = Assessment.objects.annotate(month=TruncMonth('recorded_at')).values('month').annotate(count=Count('id')).order_by('month')

        # Prepare data for the chart
        labels = [result['month'].strftime("%Y-%m") for result in assessments_per_month]
        data = [result['count'] for result in assessments_per_month]

        # Add to context
        context['assessment_activity_data'] = {
            'labels': labels,
            'data': data,
        }
        return context


class SkillDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'skill_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pull all skills
        context['skills'] = Skill.objects.annotate(
            average_score=Avg('skill_scores__score'),
            num_assessments=Count('skill_scores')
        )
        # Pull all categories
        context['categories'] = Category.objects.all()
        
        context['category_charts'] = []

        for category in context['categories']:
            # Pull all skills in the category
            skills = context['skills'].filter(category=category)
            if not skills:
                continue

            skill_data = []

            # Prepare data for the chart
            for skill in skills:
                skill_data.append({
                    'name': skill.name,
                    'average_score': skill.average_score,
                    'num_assessments': skill.num_assessments or 0
                })

            # Prepare the data for chart.js
            chart_data = {
                'category': category.name,
                'datasets': [{
                    'data': [skill['num_assessments'] for skill in skill_data],
                    'label': 'Number of Assessments',
                }, {
                    'data': [skill['average_score'] for skill in skill_data],
                    'label': 'Average Score',
                }],
                'labels': [skill['name'] for skill in skill_data]
            }

            context['category_charts'].append(chart_data)

        return context


class JobDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'job_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pull all jobs and annotate
        context['jobs'] = Job.objects.values("job_name", "job_num").annotate(
            num_users=Count('employees_onsite', distinct=True),
            num_users_with_grades=Count(
                'employees_onsite', 
                filter=Q(employees_onsite__assessments__scores__isnull=False), 
                distinct=True),
            num_skills=Count('employees_onsite__assessments__scores__skill', distinct=True),
            num_assessors=Count('employees_onsite__assessments_given__assessor', distinct=True)
        ).annotate(
            users_with_grades_percentage=ExpressionWrapper(
                F('num_users_with_grades') * 100 / F('num_users'), 
                output_field=FloatField())
        ).filter(num_users__gt=0)
        return context


class JobDetailView(LoginRequiredMixin, TemplateView):
    template_name='job_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_number = self.kwargs['job_number']
        
        # Pull the job and other relevant data
        job = get_object_or_404(Job, job_num=job_number)
        total_onsite_employees = job.employees_onsite.count()
        assessments_completed = job.assessments.count()

        # 
        skills_scored_percentage = Skill.objects.annotate(
            scored_count=Count(
                'skill_scores__assessment__user', 
                filter=Q(skill_scores__assessment__user__job=job), 
                distinct=True
            ),
            percentage_scored=ExpressionWrapper(
                F('scored_count') * 100 / total_onsite_employees, 
                output_field=FloatField()
            )
        ).filter(skill_scores__assessment__user__job=job).distinct()
        
        # Get highest and lowest scored skills
        highest_scores = Skill.objects.filter(
            skill_scores__assessment__user__job=job
        ).annotate(
            average_score=Avg('skill_scores__score')
        ).order_by('-average_score')[:5]
        lowest_scores = Skill.objects.filter(
            skill_scores__assessment__user__job=job
        ).annotate(
            average_score=Avg('skill_scores__score')
        ).order_by('average_score')[:5]

        context['job'] = job
        context['assessments_completed'] = assessments_completed
        context['highest_scores'] = highest_scores
        context['lowest_scores'] = lowest_scores
        context['skills_scored_percentage'] = skills_scored_percentage
        return context


class UserDetailView(LoginRequiredMixin, TemplateView):
    template_name='user_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        
        # Pull the user and other relevant data
        user = get_object_or_404(User, pk=user_id)
        context['user'] = user

        # Fetch score history for each skill excluding self assessments
        skill_scores = (Assessment.objects
                        .filter(user=user, is_self_assessment=False)
                        .values('scores__skill__name', 'scores__score', 'recorded_at')
                        .order_by('scores__skill__name', '-recorded_at'))
        
        # Fetch self assessment score history for each skill
        self_assessment_scores = (Assessment.objects
                                  .filter(user=user, is_self_assessment=True)
                                  .values('scores__skill__name', 'scores__score', 'recorded_at')
                                  .order_by('scores__skill__name', '-recorded_at'))
        
        # Organize data for chart.js
        skill_history = defaultdict(lambda: {'assessments': [], 'self_assessments': []})
        for entry in skill_scores:
            skill_name = entry['scores__skill__name']
            skill_history[skill_name]['assessments'].append({
                'score': entry['scores__score'],
                'date': entry['recorded_at'].strftime('%Y-%m-%d')
            })
        
        for entry in self_assessment_scores:
            skill_name = entry['scores__skill__name']
            skill_history[skill_name]['self_assessments'].append({
                'score': entry['scores__score'],
                'date': entry['recorded_at'].strftime('%Y-%m-%d')
            })
        
        context['skill_history'] = json.dumps(skill_history, cls=DjangoJSONEncoder)

        # Calculate the number of skills with scores over time excluding self assessments
        skills_over_time = (Assessment.objects
                            .filter(user=user, is_self_assessment=False)
                            .annotate(month=TruncMonth('recorded_at'))
                            .values('month')
                            .annotate(num_skills=Count('scores__skill', distinct=True))
                            .order_by('month'))
        skills_over_time_data = {
            'labels': [result['month'].strftime("%Y-%m") for result in skills_over_time],
            'data': [result['num_skills'] for result in skills_over_time]
        }
        context['skills_over_time'] = json.dumps(skills_over_time_data, cls=DjangoJSONEncoder)

        # Calculate the number of skills the user has been scored for excluding self assessments
        user_skills_count = Assessment.objects.filter(user=user, is_self_assessment=False).values('scores__skill').distinct().count()
        # Calculate the total number of skills available
        total_skills_count = Skill.objects.count()
        # Prepare the data
        skills_pie_data = {
            'labels': ['Skills Scored', 'Skills Not Scored'],
            'data': [user_skills_count, total_skills_count - user_skills_count]
        }
        context['skills_pie_data'] = json.dumps(skills_pie_data, cls=DjangoJSONEncoder)

        return context


class SkillDetailView(LoginRequiredMixin, DetailView):
    model = Skill
    template_name = "skill_scores.html"
    context_object_name = 'skill'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["assessments"] = self.object.assessment_set.all().order_by('-recorded_at')
        return context


class AddSkillView(LoginRequiredMixin, CreateView):
    model = Skill
    form_class = SkillForm
    template_name = 'add_skill.html'
    success_url = reverse_lazy('home')


class AddUserView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'add_user.html'
    success_url = reverse_lazy('home')


@login_required
def assessment_create_view(request):
    ScoreFormSet = get_ScoreFormSet()
    if request.method == 'POST':
        assessment_form = AssessmentForm(request.POST)
        score_formset = ScoreFormSet(request.POST)
        
        if assessment_form.is_valid() and score_formset.is_valid():
            assessment = assessment_form.save()
            scores = score_formset.save(commit=False)
            for score in scores:
                score.assessment = assessment
                score.save()
            return redirect('home') # replace with the success page
        else:
            print(assessment_form.errors)
            print(score_formset.errors)
    else:
        assessment_form = AssessmentForm()
        ScoreFormSet = get_ScoreFormSet()
        score_formset = ScoreFormSet()

    return render(request, 'assessment_form.html', {
        'assessment_form': assessment_form,
        'score_formset': score_formset,
    })

# SERIALIZER VIEWS #############################################################
class SkillList(LoginRequiredMixin, generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SkillFilter