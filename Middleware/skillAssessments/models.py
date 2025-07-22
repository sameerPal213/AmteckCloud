from django.db import models
from django.db.models.fields import AutoField
from django.utils import timezone
from django.utils.translation import gettext as _
from coins.models import Job, Employee


# Create your models here.mo
class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, default='')

    class Meta:
        managed = True
        db_table = "Bronze].[skills_category"
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=50, default='', null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    max_score = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    order = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = "Bronze].[skills_skill"
        verbose_name = _("skill")
        verbose_name_plural = _("skills")

    def __str__(self):
        return self.name
    


class User(Employee):
    job = models.ForeignKey("coins.Job",
                            verbose_name=_("Current Job"),
                            on_delete=models.SET_NULL, 
                            blank=True,
                            null=True,
                            related_name='employees_onsite')
    is_assessor = models.BooleanField(default=False)

    class Meta:
        managed=True
        db_table = "Bronze].[skills_user"
        verbose_name = _("user")
        verbose_name_plural = _("users")
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"pk": self.pk})



class Assessment(models.Model):
    id = models.AutoField(primary_key=True)
    recorded_at = models.DateTimeField(_("recorded_at"), default=timezone.now)
    user = models.ForeignKey("skillAssessments.User", 
                             related_name='assessments', 
                             verbose_name=_("Employee"), 
                             on_delete=models.CASCADE)
    assessor = models.ForeignKey("skillAssessments.User", 
                                 related_name='assessments_given', 
                                 verbose_name=_("Assessor"), 
                                 on_delete=models.CASCADE,
                                 limit_choices_to={'is_assessor': True},
                                 blank=True,
                                 null=True)
    job = models.ForeignKey("coins.Job", 
                            verbose_name=_("Project"), 
                            on_delete=models.CASCADE,
                            related_name='assessments',
                            blank=True,
                            null=True)
    skill_scores = models.ManyToManyField("skillAssessments.Skill",
                                          through='SkillScore')
    is_self_assessment = models.BooleanField()
    comments = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "Bronze].[skills_assessment"
        verbose_name = _("Assessment")
        verbose_name_plural = _("Assessments")

    def __str__(self):
        return f"{self.user} {self.assessor} {self.recorded_at}"

    def get_absolute_url(self):
        return reverse("Assessment_detail", kwargs={"pk": self.pk})
    


class SkillScore(models.Model):
    NOT_OBSERVED = 0
    NEEDS_DEVELOPMENT = 1
    INTERMEDIATE_KNOWLEDGE = 2
    SOLID_KNOWLEDGE = 3
    ADVANCED_KNOWLEDGE = 4

    SCORE_CHOICES = [
        (NOT_OBSERVED, f"{NOT_OBSERVED} - Not Observed"),
        (NEEDS_DEVELOPMENT, f"{NEEDS_DEVELOPMENT} - Needs Development"),
        (INTERMEDIATE_KNOWLEDGE, f"{INTERMEDIATE_KNOWLEDGE} - Intermediate Knowledge"),
        (SOLID_KNOWLEDGE, f"{SOLID_KNOWLEDGE} - Solid Knowledge"),
        (ADVANCED_KNOWLEDGE, f"{ADVANCED_KNOWLEDGE} - Advanced Knowledge"),
    ]
    id = models.AutoField(primary_key=True)
    assessment = models.ForeignKey("skillAssessments.Assessment", 
                                   verbose_name="Assessment", 
                                   on_delete=models.CASCADE,
                                   related_name='scores')
    skill = models.ForeignKey("skillAssessments.Skill", 
                              verbose_name=_("Skill"), 
                              on_delete=models.CASCADE,
                              related_name='skill_scores')
    score = models.IntegerField(choices=SCORE_CHOICES)
    comments = models.TextField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = "Bronze].[skills_skill_score"
        verbose_name = _("Skill Score")
        verbose_name_plural = _("Skill Scores")
