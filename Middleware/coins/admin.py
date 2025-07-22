# coins/admin.py
from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from .models import (
        Project, Job, Section, CostCode, Activity, WBS, CostTransaction, 
        PurchaseOrder, PurchaseOrderItem, PurchaseOrderLine, ContractManagerJob,
        SOVResource, SOVChangeManagement, SOVItem, ProjectsDirectory, Employee)

# Register your models here.

@admin.register(ProjectsDirectory)
class ProjectsDirectoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'dept', 'status', 'stage', 'boxID')
    search_fields = ['dept', 'status', 'stage', 'boxID']

# EMPLOYEE
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('coins_id', 'first_name', 'last_name', 'status', 'job_title')
    search_fields = ['coins_id', 'first_name', 'last_name', 'job_title',]
    list_filter = ('job_title', 'status')
    
# PROJECT
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('pij_dispno', 'pij_name', 'boxID')
    search_fields = ['pij_num', 'pij_dispno', 'pij_name']
    list_filter = ('pty_type', 'pst_type', 'boxID')

# JOB
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_name', 'job_num', 'project')
    search_fields = ['job_num', 'job_name']
    list_filter = ('job_active', 'jcl_loc', 'job_fore', 'job_cust', 'job_complete')

# SECTION
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('job_num', 'jcs_section', 'jcs_shdesc', 'jcs_active',)
    search_fields = ['job_num', 'jcs_section', 'jcs_desc']
admin.site.register(CostCode)
admin.site.register(Activity)
admin.site.register(WBS)
admin.site.register(CostTransaction)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)
admin.site.register(PurchaseOrderLine)

# CONTRACT MANAGER JOB
@admin.register(ContractManagerJob)
class ContractManagerJobAdmin(admin.ModelAdmin):
    list_display = ('job_num', 'svj_lastrev', 'count_changes_link', )
    search_fields = ['job_num', ]

    def count_changes_link(self, obj):
        count = SOVChangeManagement.objects.filter(job_num=obj.job_num).count()
        url = (
            reverse("admin:coins_sovchangemanagement_changelist")
            + "?"
            + urlencode({"q": f"{obj.job_num}"})
        )
        if count == 0:
            return "-"
        else: 
            return format_html('<a href="{}">{} Changes</a>', url, count)
    count_changes_link.short_description = "Changes"

# SOV CHANGE
@admin.register(SOVChangeManagement)
class SOVChangeManagementAdmin(admin.ModelAdmin):
    list_display = ('job_num', 'svl_type', 'svv_type', 'svv_number',
    'count_items_link',)
    search_fields = ['job_num', 'svl_type', 'svv_type', 'svv_desc', ]

    def count_items_link(self, obj):
        count = SOVItem.objects.filter(
                job_num = obj.job_num,
                svv_number = obj.svv_number, 
                svl_type = obj.svl_type).count()
        url = (
                reverse("admin:coins_sovitem_changelist")
                + "?"
                + urlencode({"q": f"{obj.job_num}"}))
        if count == 0:
            return "-"
        else:
            return format_html('<a href="{}">{} Items</a>', url, count)
    count_items_link.short_description = "Items"

# SOV ITEM
@admin.register(SOVItem)
class SOVItemAdmin(admin.ModelAdmin):
    list_display = ('job_num', 'svl_type', 'svi_id', 'svv_number', )
    search_fields = ['job_num', 'svl_type', 'svi_id', ]

# SOV RESOURCE
@admin.register(SOVResource)
class SOVResourceAdmin(admin.ModelAdmin):
    list_display = ('job_num', 'jwb_code', 'jsc_cc', 'svr_qty', 'tun_unit', 
            'svr_vintrate', 'svr_vintvalue', 'svi_id', )
    search_fields = ['job_num', 'jcc_cc', 'svi_id', ]

