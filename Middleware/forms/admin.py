from django.contrib import admin
from .models import (SafetyTaskAnalysisResponse, SafetyTaskAnalysisTool, 
                     SafetyTaskAnalysisHazard, STAPPE, STAPPECategory, STAPermit,
                     STAProcedure, STAEmployeeCertification, STASpecialCertification,
                     STAPostTask)

@admin.register(SafetyTaskAnalysisResponse)
class SafetyTaskAnalysisResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'assessor', 'job', 'location_of_work', 'date', 'lead_superintendent_name', 'lead_superintendent_phone', 'foreman_name', 'foreman_phone', 'manager_name', 'manager_phone']
    list_filter = ['job']
    search_fields = ['job__name', 'location_of_work', 'lead_superintendent_name', 'foreman_name', 'manager_name']
    readonly_fields = ['id', 'date']
    fieldsets = [
        ('Response Information', {'fields': ['assessor', 'boxID']}),
        ('Project Information', {'fields': ['job', 'location_of_work', 'date']}),
        ('Manager Information', {'fields': ['lead_superintendent_name', 'lead_superintendent_phone', 'foreman_name', 'foreman_phone', 'manager_name', 'manager_phone']}),
        ('Details', {'fields': ['performed_work', 'needed_equipment']}),
        ('Elevated Work Assessment', {'fields': ['ladder_work_elevation', 'ladder_reason_for_use', 'ladder_type', 'ladder_height', 'ladder_approve_printed_name', 'ladder_approve_signature']}),
        ('Lift Equipment', {'fields': ['lift', 'safe_travel', 'soils', 'spotter_required', 'spotter_name', 'spotter_qualified', 'inspection_performed', 'inspection_form_accessible']}),
        ('Permits', {'fields': ['lockout', 'lockout_comments', 'hot_work', 'hot_work_comments', 'trench', 'trench_comments', 'confined', 'confined_comments', 'line_break', 'line_break_comments', 'energized_work', 'energized_work_comments', 'scaffolds', 'scaffolds_comments', 'crane_lift', 'crane_lift_comments']}),
        ('Procedures Required', {'fields': ['caution_sign', 'caution_sign_comments', 'danger_sign', 'danger_sign_comments', 'fire_watch', 'fire_watch_comments', 'hole_watch', 'hole_watch_comments', 'o2_monitoring', 'o2_monitoring_comments', 'door_monitor', 'door_monitor_comments']}),
        ('Required Certificates', {'fields': ['forklift', 'utv', 'scissor', 'boom', 'powder_actuated', 'lockout_tagout', 'signal_person', 'other', 'competent_person', 'confined_space', 'excavations', 'scaffold', 'qualified_person']}),
        ('Other', {'fields': ['ppe']})
    ]


admin.site.register(SafetyTaskAnalysisTool)
admin.site.register(SafetyTaskAnalysisHazard)
admin.site.register(STAPPE)
admin.site.register(STAPPECategory)
admin.site.register(STAPermit)
admin.site.register(STAProcedure)
admin.site.register(STAEmployeeCertification)
admin.site.register(STASpecialCertification)
admin.site.register(STAPostTask)
