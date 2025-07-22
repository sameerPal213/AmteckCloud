from django import forms
from forms.widgets import GroupedSelect
from .models import Skill, User, Assessment, SkillScore

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['user', 'job', 'assessor', 'is_self_assessment', 'comments']


class ScoreForm(forms.ModelForm):
    class Meta:
        model = SkillScore
        fields = ['skill', 'score', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 1, 'cols': 60}),  # Limiting to 4 rows and 40 columns
            'skill': GroupedSelect(
                model=Skill, 
                display_field='name', 
                group_field='category__name', 
                all_option=True,
                queryset=Skill.objects.all().order_by('category__name', 'order') # Ordering by category and then name
            ),
            'score': forms.Select(choices=SkillScore.SCORE_CHOICES),
        }

    def clean(self):
        cleaned_data = super().clean()
        score = cleaned_data.get('score')
        comments = cleaned_data.get('comments')

        if score == 1 and not comments:
            self.add_error('comments', 'Comments are required for Needs Development scores')

        return cleaned_data


def get_ScoreFormSet():
    return forms.inlineformset_factory(Assessment, SkillScore, form=ScoreForm, extra=1)
