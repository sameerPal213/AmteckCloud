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
                          STARequiredSpecialCertification, STAPermit,
                          Amq1001Response as amq1001, Amq1002Response as amq1002,
                          Amq1003Response as Amq1003, Amq1301Response as Amq1301,
                          Amq1401Response as Amq1401)
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

class AMQ100_1_Model_Form(ModelForm):
    class Meta:
        model = amq1001
        fields = "__all__"
        labels = {
            "conforms_to_NEC" : _( 
                'Ensure installation conforms to the appropriate NEC ' 
                'Article(s)'),
            "installed_per_iwp_drawing" : _( 
                'Verify conduit is installed as per IWP drawings and details'),
            "supports_anchored" : _(
                'Verify supports are anchored securely'),
            "conduit_leveled" : _(
                'Verify conduit is level and parallel or perpindicular to '
                'structural members'),
            "material_classification" : _(
                'Verify material/type is correct for area classification'),
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
            "mandrel_conduit_per_project" : _(
                'Mandrel conduit as required per project specs.'),
            "field_changes_on_drawing" : _(
                'Document field changes on as-built drawings')
            }

class AMQ100_2_Model_Form(ModelForm):
    class Meta:
        model = amq1002
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
                "or project specifications"),
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
            "ground_penetration_sealed" : _(
                "Verify thru slab/ground penetrations have been properly "
                "sealed"),
            "mandrel_conduit_per_project" : _(
                'Mandrel conduit as required per project specifications'),    
            "document_field_drawings" : _(
                "Document field changes on as-built drawings")
        }

class AMQ100_3_Model_Form(ModelForm):
    class Meta:
        model  = Amq1003
        fields = "__all__"
        labels = {
            "conduit_material_specification": _(
                "Confirm stub-up conduit material is correct per specifications, GRC / PVC."),
            "window_size_stubup":             _(
                "Verify window size of stub-up locations"),
            "coordinates_stubups":            _(
                "Verify coordinates for stub-ups"),
            "stubup_spacing_endbells":        _(
                "Verify stub-up spacing is adequate for End Bells, Terminal Adapters, Lock Rings"),
            "stubups_plumb_level":            _(
                "Verify that all stub-ups are plumb/level before and after backfilling operations"),
            "equipment_location_correct":     _(
                "Verify equipment location is correct per plans"),
            "grounding_tails_stubbed":        _(
                "Verify grounding tails are stubbed up in the right sections"),
            "stubup_size_count_match":        _(
                "Verify stub-up size and count match the plans"),
            "stubup_seal_at_SOG":             _(
                "Verify stub-ups at equipment have the SOG seal broken (see UG Conduit Detail)"),
            "stubups_blown_clean":            _(
                "Verify all stub-ups have been blown clean or a duct cleaner pulled through"),
            "pull_string_installed":          _(
                "Verify pull string or mule tape is installed"),
            "stubups_labeled":                _(
                "Verify that all stub-ups are properly labeled"),
            "slab_penetrations_sealed":       _(
                "Verify thru slab/ground penetrations have been properly sealed"),
            "stubup_ends_sealed":             _(
                "Verify stub-up ends are properly sealed to prevent debris from falling in"),
            "installation_photos_video":      _(
                "Confirm installation with corresponding pictures and/or video"),
            "supporting_documentation_attached": _(
                "Attach all supporting documentation used to install stub-ups"),
        }

class AMQ130_1_Model_Form(ModelForm):
    class Meta:
        model = Amq1301
        fields = "__all__"
        labels = {
            "raceways_inspected": _(
                "Verify raceways have been inspected, cleaned out and accepted prior" \
                " to cable installation"),
            "underground_conduits_swabbed": _(
                "Verify all associated underground conduits have been swabbed / mandrel prior to cable installation, "\
                "if applicable"),
            "pull_rope_size": _(
                "Verify adequate pull rope size for distance and weight"),
            "cables_brought_up_safe_temp": _(
                "Verify cables are brought up to a safe pulling temperature"),
            "pulling_tension_monitor": _(
                "Verify maximum pulling tension. Monitor if applicable"),
            "pulling_lubricants": _(
                "Verify pulling lubricants are appropriate"),
            "cable_bending_radii": _(
                "Verify cable-bending radiuses are within manufacturers recommendations"),
            "cable_marked_identified": _(
                "Verify cable is properly marked and identified"),
            "reference_specification_sheets": _(
                "Reference applicable specification sheets prior to installation"),
            "cable_connectors_installation": _(
                "Verify proper installation of cable connectors if applicable"),
            "cable_ends_sealed": _(
                "Verify cable ends are properly sealed as required"),
            "insulation_stripped": _(
                "Verify insulation is stripped to the proper length, and ALL conductor " \
                "stranding is within the terminal lug"),
            "conductors_tagged": _(
                "Verify conductors are properly tagged as per drawings and specifications"),
            "termination_points_per_drawings": _(
                "Verify termination points are as per drawings"),
            "cables_routed_secured": _(
                "Verify cables and conductors are properly routed and securely supported"),
            "termination_kits": _(
                "Verify proper installation of termination kits if applicable"),
            "installation_conforms_NEC": _(
                "Verify installation conforms to ALL applicable NEC articles"),
        }
class AMQ140_1_Model_Form(ModelForm):
    class Meta:
        model  = Amq1401
        fields = "__all__"
        labels = {
            "nec_article_392": _(
                "Conforms to NEC Article 392"),
            "installed_per_drawings": _(
                "Installed per drawings and details"),
            "supports_anchored_securely": _(
                "Cable Tray and supports anchored securely"),
            "fitting_radiuses_correct": _(
                "Fitting radiuses sized correctly and are as seamless as possible"),
            "cuts_edges_smooth_recoated": _(
                "Cuts and edges are smooth and recoated"),
            "dividers_installed_securely": _(
                "Dividers are installed securely"),
            "expansion_joints_bond_jumpers": _(
                "Expansion joints and bonding jumpers at proper intervals"),
            "tray_grounded_confirm_size": _(
                "Cable Tray grounded as required - Confirm ground size"),
            "cables_tied_down_intervals": _(
                "Cables are tied down at required intervals"),
            "correct_voltage_designation": _(
                "Correct voltage / signal type per designation"),
            "warning_labels_installed": _(
                "Warning labels installed as required"),
            "id_labels_installed": _(
                "Identification labels installed as required"),
            "penetrations_fire_caulked": _(
                "Verify penetrations are properly fire caulked / sealed as required"),
            "covers_installed_secured": _(
                "Covers are installed and anchored securely"),
            "field_changes_documented": _(
                "Field changes documented on as-built drawings"),
            "photographs_taken": _(
                "Photographs have been taken of the installation"),
        }
