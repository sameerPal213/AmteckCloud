from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from coins.models import Job
from forms.models import (Qaqc1001Response as qaqc1001, 
                          STAEmployeeAcknowledgement, STAEmployeeCertification, STAProcedure, 
                          STARequiredEmployeeCertification, STARequiredPermit, 
                          STARequiredProcedure, Qaqc1002Response as qaqc1002, STASpecialCertification,
                          SafetyTaskAnalysisResponse, SafetyTaskAnalysisTool, 
                          SafetyTaskAnalysisToolInspection, STAPostTask, 
                          SafetyTaskAnalysisHazardAssessment, 
                          STARequiredSpecialCertification, STAPermit)
from forms.fields import CheckboxTextField
from forms.widgets import GroupedSelect


class STAPostTaskForm(ModelForm):
    class Meta:
        model = STAPostTask
        fields = "__all__"
        widgets = {
            "injury_or_incident_comment": forms.Textarea(attrs={'rows':4}),
            "improvements": forms.Textarea(attrs={'rows':4}),
            "safety_violations": forms.Textarea(attrs={'rows':4})
        }


class QAQC100_1_Model_Form(ModelForm):
    class Meta:
        model = qaqc1001
        fields = "__all__"
        labels = {
            "conforms_to_NEC" : _( 
                'Ensure installation conforms to the appropriate NEC ' 
                'Article(s)'),
            "installed_per_drawing" : _( 
                'Verify conduit is installed as per drawings and details.'),
            "supports_anchored" : _(
                'Verify supports are anchored securely.'),
            "conduit_leveled" : _(
                'Verify conduit is level and parallel or perpindicular to '
                'structural members'),
            "material_classification" : _(
                'Verify material/type is adequate for area classification'),
            "pull_points" : _(
                'Verify pull points are installed as required'),
            "expansion_joints" : _(
                'Verify expansion joints are installed as required'),
            "low_point_drains" : _(
                'Verify low point drains are installed as required'),
            "unions" : _(
                'Verify unions are installed for equipment removal (if '
                'required)'),
            "seals" : _(
                'Verify seals are of the right type and installed for '
                'classified areas'),
            "couplings_tight" : _(
                'Verify all couplings, fittings, and connectors are tight'),
            "excessive_threads" : _(
                'Verify there is no excessive thread exposure (2 threads max)'),
            "bushings" : _(
                'Verify that bushings aare installed and of the correct type'),
            "bonding_jumpers" : _(
                'Verify bonding jumpers are installed as required'),
            "field_changes_on_drawing" : _(
                'Document field changes on as-built drawings')
            }

class QAQC100_2_Model_Form(ModelForm):
    class Meta:
        model = qaqc1002
        fields = "__all__"
        labels = {
            "conduit_material_thickness" : _(
                "Verify conduit is of the material and wall thickness specified"),
            "coordinates_stubups" : _(
                "Verify coordinates for stub-ups"),
            "conduit_radius_manufacturer_specification" : _(
                "Verify conduits radiuses are within cable manufacturers "
                "specifications"),
            "conduit_spacing_sufficient" : _(
                "Verify conduit spacing is sufficient as per NEC Article 310 and "
                "Annex B"),
            "spacing_sufficient_signal_separation" : _(
                "Verify spacing is sufficient for signal separation as per IEEE "
                "or project requirements"),
            "conduit_material_interval_support" : _(
                "Verify conduit support materials (chairs, rebar, etc.) are placed "
                "on intervals to support the conduit as per the NEC and the "
                "rigors of concrete pouring or back filling"),
            "trench_sloped_away" : _(
                "Verify trench is sloped away from building / equipment to "
                "allow for drainage"),
            "sufficient_distance_conduit" : _(
                "Verify sufficient distance between conduit and finished grade "
                "to conform with NEC Table 300.5 & Table 300.50 as required"),
            "conduit_clean_debris" : _(
                "Verify conduit is clean and free of debris"),
            "stubups_capped" : _(
                "Verify stub-ups are capped for back fill or concrete pouring"),
            "document_field_drawings" : _(
                "Document field changes on as-built drawings"),
            "ground_penetration_sealed" : _(
                "Verify thru slab/ground penetrations have been properly "
                "sealed")
        }


class SafetyTaskAnalysisForm(ModelForm):
    class Meta:
        model = SafetyTaskAnalysisResponse
        widgets = {
                "performed_work": forms.Textarea(attrs={'rows': 4, 'cols': 98}),
                "needed_equipment": forms.Textarea(attrs={'rows': 4, 'cols': 98}),
                "ladder_reason_for_use": forms.Textarea(attrs={'rows': 4, 'cols': 55}),
                "lockout_comments": forms.Textarea(attrs={'rows': 3, 'cols': 65}),
                "hot_work_comments": forms.Textarea(attrs={'rows': 3, 'cols': 65}),
                "trench_comments": forms.Textarea(attrs={'rows': 3, 'cols': 65}),
                "confined_comments": forms.Textarea(attrs={'rows': 3, 'cols': 65}),
                "line_break_comments": forms.Textarea(attrs={'rows': 3, 'cols': 65}),
                "energized_work_comments": forms.Textarea(attrs={'rows': 3, 'cols': 65}),
                "scaffolds_comments": forms.Textarea(attrs={'rows': 3, 'cols': 65}),
                "crane_lift_comments": forms.Textarea(attrs={'rows': 3, 'cols': 65}),
                "caution_sign_comments": forms.Textarea(attrs={'rows': 3, 'cols': 65}),
                "danger_sign_comments": forms.Textarea(attrs={'rows': 3, 'cols': 65}),
                "hole_watch_comments": forms.Textarea(attrs={'rows': 3, 'cols': 65}),
                "o2_monitoring_comments": forms.Textarea(attrs={'rows': 3, 'cols': 65}),
                "door_monitor_comments": forms.Textarea(attrs={'rows': 3, 'cols': 65}),
                }
        fields = "__all__"
        label = {}


class STAToolInspectionForm(ModelForm):
    class Meta:
        model = SafetyTaskAnalysisToolInspection
        fields = ['tool', 'inspection', 'training_received']

def get_STAToolInspectionFormSet():
    count = SafetyTaskAnalysisTool.objects.all().count()
    return forms.inlineformset_factory(
        SafetyTaskAnalysisResponse, 
        SafetyTaskAnalysisToolInspection, 
        form=STAToolInspectionForm, 
        extra=count)


class STAHazardMitigationForm(ModelForm):
    class Meta:
        model = SafetyTaskAnalysisHazardAssessment
        fields = ['hazard', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'cols': 65})
        }

def get_STAHazardMitigationFormSet():
    return forms.inlineformset_factory(
        SafetyTaskAnalysisResponse, 
        SafetyTaskAnalysisHazardAssessment, 
        form=STAHazardMitigationForm, 
        extra=1)


class STAEmployeeAcknowledgementForm(ModelForm):
    class Meta:
        model = STAEmployeeAcknowledgement
        fields = ['employee','shift_start_signature', 'shift_end_signature',
                  'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 2, 'cols': 30})
        }

def get_STAEmployeeAcknowledgementFormSet():
    return forms.inlineformset_factory(
        SafetyTaskAnalysisResponse, 
        STAEmployeeAcknowledgement, 
        form=STAEmployeeAcknowledgementForm, 
        extra=1)


class STARequiredPermitForm(ModelForm):
    class Meta:
        model = STARequiredPermit
        fields = ['permit', 'required', 'comments']
        widgets = {
                "comments": forms.Textarea(attrs={'rows': 2, 'cols': 100}),
                }

def get_STARequiredPermitFormSet():
    count = STAPermit.objects.all().count()
    return forms.inlineformset_factory(
        SafetyTaskAnalysisResponse, 
        STARequiredPermit, 
        form=STARequiredPermitForm,
        extra=count)


class STARequiredProcedureForm(ModelForm):
    class Meta:
        model = STARequiredProcedure
        fields = ['procedure', 'required', 'comments']
        widgets = {
                "comments": forms.Textarea(attrs={'rows': 2, 'cols': 100}),
                }

def get_STARequiredProcedureFormSet():
    count = STAProcedure.objects.all().count()
    return forms.inlineformset_factory(
        SafetyTaskAnalysisResponse, 
        STARequiredProcedure, 
        form=STARequiredProcedureForm , 
        extra=count)


class STARequiredEmployeeCertificationForm(ModelForm):
    class Meta:
        model = STARequiredEmployeeCertification
        fields = ['certification', 'required', 'comments']
        widgets = {
                "comments": forms.Textarea(attrs={'rows': 2, 'cols': 100}),
                }

def get_STARequiredEmployeeCertificationFormSet():
    count = STAEmployeeCertification.objects.all().count()
    return forms.inlineformset_factory(
        SafetyTaskAnalysisResponse, 
        STARequiredEmployeeCertification, 
        form=STARequiredEmployeeCertificationForm , 
        extra=count)


class STARequiredSpecialCertificationForm(ModelForm):
    class Meta:
        model = STARequiredSpecialCertification
        fields = ['certification', 'required', 'comments']
        widgets = {
                "comments": forms.Textarea(attrs={'rows': 2, 'cols': 100}),
                }

def get_STARequiredSpecialCertificationFormSet():
    count = STASpecialCertification.objects.all().count()
    return forms.inlineformset_factory(
        SafetyTaskAnalysisResponse, 
        STARequiredSpecialCertification, 
        form=STARequiredSpecialCertificationForm , 
        extra=count)