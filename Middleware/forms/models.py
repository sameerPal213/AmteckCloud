# forms/models.py
from tkinter import W
from django.db import models
from coins.models import Job
from jsignature.fields import JSignatureField
from django.utils.translation import gettext as _


# Create your models here.

class Qaqc1001Response(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        null=False,
        limit_choices_to={'job_active': 'a'})
    area = models.CharField(max_length=100, null=True, default='')
    sheet_no = models.IntegerField()
    drawing = models.CharField(max_length=100)
    conduit_run_from = models.CharField(max_length=20)
    conduit_run_to = models.CharField(max_length=20)

    # Checklist
    conforms_to_NEC = models.BooleanField(default=False)
    conforms_to_NEC_corrections_needed = models.BooleanField(default=False)
    conforms_to_NEC_corrections_completed = models.BooleanField(default=False)

    installed_per_drawing = models.BooleanField(default=False)
    installed_per_drawing_corrections_needed = models.BooleanField(default=False)
    installed_per_drawing_corrections_completed = models.BooleanField(default=False)

    supports_anchored = models.BooleanField(default=False)
    supports_anchored_corrections_needed = models.BooleanField(default=False)
    supports_anchored_corrections_completed = models.BooleanField(default=False)

    conduit_leveled = models.BooleanField(default=False)
    conduit_leveled_corrections_needed = models.BooleanField(default=False)
    conduit_leveled_corrections_completed = models.BooleanField(default=False)

    material_classification = models.BooleanField(default=False)
    material_classification_corrections_needed = models.BooleanField(default=False)
    material_classification_corrections_completed = models.BooleanField(default=False)

    pull_points = models.BooleanField(default=False)
    pull_points_corrections_needed = models.BooleanField(default=False)
    pull_points_corrections_completed = models.BooleanField(default=False)

    expansion_joints = models.BooleanField(default=False)
    expansion_joints_corrections_needed = models.BooleanField(default=False)
    expansion_joints_corrections_completed = models.BooleanField(default=False)

    low_point_drains = models.BooleanField(default=False)
    low_point_drains_corrections_needed = models.BooleanField(default=False)
    low_point_drains_corrections_completed = models.BooleanField(default=False)

    unions = models.BooleanField(default=False)
    unions_corrections_needed = models.BooleanField(default=False)
    unions_corrections_completed = models.BooleanField(default=False)

    seals = models.BooleanField(default=False)
    seals_corrections_needed = models.BooleanField(default=False)
    seals_corrections_completed = models.BooleanField(default=False)

    couplings_tight = models.BooleanField(default=False)
    couplings_tight_corrections_needed = models.BooleanField(default=False)
    couplings_tight_corrections_completed = models.BooleanField(default=False)

    excessive_threads = models.BooleanField(default=False)
    excessive_threads_corrections_needed = models.BooleanField(default=False)
    excessive_threads_corrections_completed = models.BooleanField(default=False)

    bushings = models.BooleanField(default=False)
    bushings_corrections_needed = models.BooleanField(default=False)
    bushings_corrections_completed = models.BooleanField(default=False)

    bonding_jumpers = models.BooleanField(default=False)
    bonding_jumpers_corrections_needed = models.BooleanField(default=False)
    bonding_jumpers_corrections_completed = models.BooleanField(default=False)

    field_changes_on_drawing = models.BooleanField(default=False)
    field_changes_on_drawing_corrections_needed = models.BooleanField(default=False)
    field_changes_on_drawing_corrections_completed = models.BooleanField(default=False)

    test_signature = JSignatureField(null=True)

    class Meta:
        managed = True
        db_table = "Bronze].[qaqc_100_1"


class Qaqc1002Response(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        null=False)
    area = models.CharField(max_length=100, null=True, default='')
    sheet_no = models.IntegerField()
    drawing = models.CharField(max_length=100)
    conduit_run_from = models.CharField(max_length=20)
    conduit_run_to = models.CharField(max_length=20)

    # Checklist
    conduit_material_thickness = models.BooleanField(default=False)
    conduit_material_thickness_corrections_needed = models.BooleanField(default=False)
    conduit_material_thickness_corrections_completed = models.BooleanField(default=False)

    coordinates_stubups = models.BooleanField(default=False)
    coordinates_stubups_corrections_needed = models.BooleanField(default=False)
    coordinates_stubups_corrections_completed = models.BooleanField(default=False)

    conduit_radius_manufacturer_specification = models.BooleanField(default=False)
    conduit_radius_manufacturer_specification_corrections_needed = models.BooleanField(default=False)
    conduit_radius_manufacturer_specification_corrections_completed = models.BooleanField(default=False)

    conduit_spacing_sufficient = models.BooleanField(default=False)
    conduit_spacing_sufficient_corrections_needed = models.BooleanField(default=False)
    conduit_spacing_sufficient_corrections_completed = models.BooleanField(default=False)

    spacing_sufficient_signal_separation = models.BooleanField(default=False)
    spacing_sufficient_signal_separation_corrections_needed = models.BooleanField(default=False)
    spacing_sufficient_signal_separation_corrections_completed = models.BooleanField(default=False)

    conduit_material_interval_support = models.BooleanField(default=False)
    conduit_material_interval_support_corrections_needed = models.BooleanField(default=False)
    conduit_material_interval_support_corrections_completed = models.BooleanField(default=False)

    trench_sloped_away = models.BooleanField(default=False)
    trench_sloped_away_corrections_needed = models.BooleanField(default=False)
    trench_sloped_away_corrections_completed = models.BooleanField(default=False)

    sufficient_distance_conduit = models.BooleanField(default=False)
    sufficient_distance_conduit_corrections_needed = models.BooleanField(default=False)
    sufficient_distance_conduit_corrections_completed = models.BooleanField(default=False)

    conduit_clean_debris = models.BooleanField(default=False)
    conduit_clean_debris_corrections_needed = models.BooleanField(default=False)
    conduit_clean_debris_corrections_completed = models.BooleanField(default=False)

    stubups_capped = models.BooleanField(default=False)
    stubups_capped_corrections_needed = models.BooleanField(default=False)
    stubups_capped_corrections_completed = models.BooleanField(default=False)

    document_field_drawings = models.BooleanField(default=False)
    document_field_drawings_corrections_needed = models.BooleanField(default=False)
    document_field_drawings_corrections_completed = models.BooleanField(default=False)

    ground_penetration_sealed = models.BooleanField(default=False)
    ground_penetration_sealed_corrections_needed = models.BooleanField(default=False)
    ground_penetration_sealed_corrections_completed = models.BooleanField(default=False)

    remarks = models.TextField()

    class Meta:
        managed = True
        db_table = "Bronze].[forms_qaqc_100_2"


class STAPPECategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    
    class Meta:
        managed = True
        db_table = "Bronze].[forms_safetytaskanalysis_ppecategory"
        ordering = ['name']
        verbose_name = _("STA PPE Category")
        
    def __str__(self):
        return self.name


class STAPPE(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    category = models.ForeignKey(STAPPECategory, on_delete=models.CASCADE)
    
    class Meta:
        managed = True
        db_table = "Bronze].[forms_safetytaskanalysis_ppe"
        ordering = ['name']
        verbose_name = _("STA PPE")

    def __str__(self):
        return self.name


# TODO might look into moving the subcategories of this into their own models
# that have a one-to-many reference to allow for picking
class SafetyTaskAnalysisResponse(models.Model):
    id = models.AutoField(primary_key=True)

    # Project Information
    job          = models.ForeignKey(Job, on_delete=models.CASCADE, null=False, blank=False, limit_choices_to={'job_active': 'active'})
    location_of_work = models.CharField(max_length=100, null=False, blank=False, default='')  # might need to be changed to a FK
    date             = models.DateTimeField(auto_now=True)
    assessor         = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, null=True, blank=True)

    # Manager Information
    lead_superintendent_name = models.ForeignKey(
        'coins.Employee', 
        on_delete=models.CASCADE, 
        related_name='superintendent',
        limit_choices_to={'job_title__contains': 'Superintendent'})
    lead_superintendent_phone = models.CharField( default='', null=True, blank=True, max_length=100)
    foreman_name = models.ForeignKey(
        'coins.Employee', 
        on_delete=models.CASCADE, 
        related_name='foreman',
        limit_choices_to={'job_title__contains': 'Superintendent'} | {'job_title__contains': 'Foreman'}
        )
    foreman_phone = models.CharField(default='', null=True, blank=True, max_length=100)
    manager_name = models.ForeignKey(
        'coins.Employee', 
        on_delete=models.CASCADE, 
        related_name='manager',
        limit_choices_to={'job_title__contains': 'Safety'})
    manager_phone = models.CharField(default='', null=True, blank=True, max_length=100)

    # Details
    performed_work   = models.TextField(null=False, blank=False)
    needed_equipment = models.TextField(null=False, blank=False)

    # Elevated Work Assessment
    ladder_work_elevation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ladder_reason_for_use = models.TextField(null=True, blank=True)
    LADDER_TYPES = [
        ("aframe", "A-Frame"),
        ("platform", "Platform"),
        ]
    ladder_type = models.CharField(max_length=8, choices=LADDER_TYPES, null=True, blank=True)
    LADDER_HEIGHTS = [
        ('6', '6\''),
        ('8', '8\''),
        ('10', '10\''),
        ]
    ladder_height = models.CharField(max_length=2, choices=LADDER_HEIGHTS, null=True, blank=True)
    ladder_approve_printed_name = models.CharField(max_length=50, null=True, blank=True)
    ladder_approve_signature = JSignatureField(null=True, blank=True)
    
    # Lift Equipment
    LIFT_CHOICES = [
    ("Scissor", (
        ("sc19", "19' Scissor"),
        ("sc26", "26' Scissor"),
        ("sc32", "32' Scissor"),
        ("sc", "Other"),
        )
    ),
    ("Booms", (
        ("art45", "45' Art Boom"),
        ("art", "Other"),
        )
    ),
    ('unknown', 'Unknown'),
    ]
    lift                       = models.CharField(max_length=7, choices=LIFT_CHOICES, null=True, blank=True)
    safe_travel                = models.BooleanField()
    soils                      = models.BooleanField()
    spotter_required           = models.BooleanField()
    spotter_name               = models.CharField(max_length=50, null=True, blank=True)
    spotter_qualified          = models.BooleanField()
    inspection_performed       = models.BooleanField()
    inspection_form_accessible = models.BooleanField()
    
    # Permits
    lockout                 = models.BooleanField(default=False)
    lockout_comments        = models.TextField(default='', blank=True)
    hot_work                = models.BooleanField(default=False)
    hot_work_comments       = models.TextField(default='', blank=True)
    trench                  = models.BooleanField(default=False)
    trench_comments         = models.TextField(default='', blank=True)
    confined                = models.BooleanField(default=False)
    confined_comments       = models.TextField(default='', blank=True)
    line_break              = models.BooleanField(default=False)
    line_break_comments     = models.TextField(default='', blank=True)
    energized_work          = models.BooleanField(default=False)
    energized_work_comments = models.TextField(default='', blank=True)
    scaffolds               = models.BooleanField(default=False)
    scaffolds_comments      = models.TextField(default='', blank=True)
    crane_lift              = models.BooleanField(default=False)
    crane_lift_comments     = models.TextField(default='', blank=True)

    # Procedures Required
    caution_sign           = models.BooleanField(default=False)
    caution_sign_comments  = models.TextField(default='', blank=True)
    danger_sign            = models.BooleanField(default=False)
    danger_sign_comments   = models.TextField(default='', blank=True)
    fire_watch             = models.BooleanField(default=False)
    fire_watch_comments    = models.TextField(default='', blank=True)
    hole_watch             = models.BooleanField(default=False)
    hole_watch_comments    = models.TextField(default='', blank=True)
    o2_monitoring          = models.BooleanField(default=False)
    o2_monitoring_comments = models.TextField(default='', blank=True)
    door_monitor           = models.BooleanField()
    door_monitor_comments  = models.TextField(blank=True, null=True)

    # Required Certificates
    forklift         = models.BooleanField(default=False)
    utv              = models.BooleanField(default=False)
    scissor          = models.BooleanField(default=False)
    boom             = models.BooleanField(default=False)
    powder_actuated  = models.BooleanField(default=False)
    lockout_tagout   = models.BooleanField(default=False)
    signal_person    = models.BooleanField(default=False)
    other            = models.CharField(default='', max_length=50, blank=True)
    competent_person = models.BooleanField(default=False)
    confined_space   = models.BooleanField(default=False)
    excavations      = models.BooleanField(default=False)
    scaffold         = models.BooleanField(default=False)
    qualified_person = models.BooleanField(default=False)

    # PPE Requirements 
    ppe = models.ManyToManyField(STAPPE, blank=True, null=True)

    # Box ID
    boxID = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "Bronze].[forms_safetytaskanalysisresponse"
        verbose_name=_("STA Response")
        verbose_name_plural=_("STA Responses")


class STAPostTask(models.Model):
    response                    = models.ForeignKey(SafetyTaskAnalysisResponse, on_delete=models.CASCADE)
    injury_or_incident          = models.BooleanField(default=False)
    injury_or_incident_comment  = models.TextField(blank=True, null=True)
    injury_or_incident_reported = models.BooleanField(default=False)
    improvements                = models.TextField(blank=True, null=True)
    safety_violations           = models.TextField(blank=True, null=True)
    hazard_observations_made    = models.BooleanField(default=False)
    hazard_observations_count   = models.IntegerField(blank=True, null=True)
    supervisor_signature        = JSignatureField(blank=False, null=False)

    class Meta:
        managed = True
        db_table = "Bronze].[forms_safetytaskanalysis_posttask"
        verbose_name = _("STA Post Task")
        verbose_name_plural = _("STA Post Tasks")

    def __str__(self):
        return f'STA: {self.response.job.job_num} {self.response.id} - Post Task Assignment'


class STAPermit(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)

    class Meta:
        managed = True
        ordering = ['name']
        db_table = "Bronze].[forms_safetytaskanalysis_permits"
        verbose_name = _("STA Permit")
        verbose_name_plural = _("STA Permits")

    def __str__(self):
        return self.name


class STAProcedure(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)

    class Meta:
        managed = True
        ordering = ['name']
        db_table = "Bronze].[forms_safetytaskanalysis_procedures"
        verbose_name = _("STA Procedure")
        verbose_name_plural = _("STA Procedures")

    def __str__(self):
        return self.name


class STAEmployeeCertification(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)

    class Meta:
        managed = True
        ordering = ['name']
        db_table = "Bronze].[forms_safetytaskanalysis_employeecertifications"
        verbose_name = _("STA Employee Certification")
        verbose_name_plural = _("STA Employee Certifications")

    def __str__(self):
        return self.name


class STASpecialCertification(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)

    class Meta:
        managed = True
        ordering = ['name']
        db_table = "Bronze].[forms_safetytaskanalysis_specialcertifications"
        verbose_name = _("STA Special Certification")
        verbose_name_plural = _("STA Special Certifications")

    def __str__(self):
        return self.name


class SafetyTaskAnalysisTool(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)

    class Meta:
        managed = True
        ordering = ['name']
        db_table = "Bronze].[forms_safetytaskanalysis_tools"
        verbose_name = _("STA Tool")
        verbose_name_plural = _("STA Tools")

    def __str__(self):
        return self.name


class SafetyTaskAnalysisToolInspection(models.Model):
    response = models.ForeignKey(SafetyTaskAnalysisResponse, on_delete=models.CASCADE)
    tool = models.ForeignKey(SafetyTaskAnalysisTool, on_delete=models.CASCADE)
    inspection = models.BooleanField(default=False)
    training_received = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = "Bronze].[forms_safetytaskanalysis_toolinspection"
        verbose_name = _("STA Tool Inspection")
        verbose_name_plural = _("STA Tool Inspections")


class STARequiredPermit(models.Model):
    response = models.ForeignKey(SafetyTaskAnalysisResponse, on_delete=models.CASCADE)
    permit = models.ForeignKey(STAPermit, on_delete=models.CASCADE)
    required = models.BooleanField(default=False)
    comments = models.TextField(blank=True, default='')

    class Meta:
        managed = True
        db_table = "Bronze].[forms_safetytaskanalysis_requiredpermit"
        verbose_name = _("STA Required Permit")
        verbose_name_plural = _("STA Required Permits")


class STARequiredProcedure(models.Model):
    response = models.ForeignKey(SafetyTaskAnalysisResponse, on_delete=models.CASCADE)
    procedure = models.ForeignKey(STAProcedure, on_delete=models.CASCADE)
    required = models.BooleanField(default=False)
    comments = models.TextField(blank=True, default='')

    class Meta:
        managed = True
        db_table = "Bronze].[forms_safetytaskanalysis_requiredprocedure"
        verbose_name = _("STA Required Procedure")
        verbose_name_plural = _("STA Required Procedures")


class STARequiredEmployeeCertification(models.Model):
    response = models.ForeignKey(SafetyTaskAnalysisResponse, on_delete=models.CASCADE)
    certification = models.ForeignKey(STAEmployeeCertification, on_delete=models.CASCADE)
    required = models.BooleanField(default=False)
    comments = models.TextField(blank=True, default='')

    class Meta:
        managed = True
        db_table = "Bronze].[forms_safetytaskanalysis_employeecertificate"
        verbose_name = _("STA Required Employee Certification")
        verbose_name_plural = _("STA Required Employee Certifications")


class STARequiredSpecialCertification(models.Model):
    response = models.ForeignKey(SafetyTaskAnalysisResponse, on_delete=models.CASCADE)
    certification = models.ForeignKey(STASpecialCertification, on_delete=models.CASCADE)
    required = models.BooleanField(default=False)
    comments = models.TextField(blank=True, default='')

    class Meta:
        managed = True
        db_table = "Bronze].[forms_safetytaskanalysis_specialcertification"
        verbose_name = _("STA Required Special Certification")
        verbose_name_plural = _("STA Required Special Certifications")


class SafetyTaskAnalysisHazard(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    
    class Meta:
        managed = True
        db_table = "Bronze].[forms_safetytaskanalysis_hazard"
        ordering = ['name']
        verbose_name = _("STA Hazard")
        verbose_name_plural = _("STA Hazards")

    def __str__(self):
        return self.name


class SafetyTaskAnalysisHazardAssessment(models.Model):
    response = models.ForeignKey(SafetyTaskAnalysisResponse, on_delete=models.CASCADE)
    hazard = models.ForeignKey(SafetyTaskAnalysisHazard, on_delete=models.CASCADE)
    comment = models.TextField(blank=False, null=True)

    class Meta:
        managed = True
        db_table = "Bronze].[forms_safetytaskanalysis_hazardassessment"
        verbose_name = _("STA Hazard Assessment")
        verbose_name_plural = _("STA Hazard Assessments")


class STAEmployeeAcknowledgement(models.Model):
    response = models.ForeignKey(SafetyTaskAnalysisResponse, on_delete=models.CASCADE)
    employee = models.ForeignKey('coins.Employee', on_delete=models.CASCADE)
    shift_start_signature = JSignatureField(null=True)
    shift_end_signature = JSignatureField(null=True)
    comments = models.TextField(blank=True, default='')
    
    class Meta:
        managed = True
        db_table = "Bronze].[forms_safetytaskanalysis_employeeacknowledgement"
        verbose_name = _("STA Employee Acknowledgement")
        verbose_name_plural = _("STA Employee Acknowledgements")
