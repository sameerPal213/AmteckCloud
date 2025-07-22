from django.urls import path
from .views import ( UserDetailView, UserDashboardView, SkillDetailView, 
                    assessment_create_view, HomePageView, AddSkillView, 
                    AddUserView, SkillList, SkillDashboardView, 
                    JobDashboardView, JobDetailView)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('api/skills/', SkillList.as_view(), name='skill-list'),
    path('user-view/', UserDashboardView.as_view(), name='user-dashboard'), 
    path('user-view/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('skill-view/', SkillDashboardView.as_view(), name='skill-dashboard'),
    path('skill-scores/<int:pk>', SkillDetailView.as_view(), name='skill-detail'),
    path('job-view/', JobDashboardView.as_view(), name='job-dashboard'),
    path('job-view/<int:job_number>/', JobDetailView.as_view(), name='job-detail'),
    path('new-score/', assessment_create_view, name='new-score'),
    path('add-skill/', AddSkillView.as_view(), name='add-skill'),
    path('add-user/', AddUserView.as_view(), name='add-user'),
]
