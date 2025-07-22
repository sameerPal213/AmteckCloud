from django.db import models
from coins.models import Employee

class Estimate(models.Model):
    id = models.CharField(max_length=50, null=False, blank=False, default='', primary_key=True)
    name = models.CharField(max_length=200, null=False, blank=False, default='')
    number = models.CharField(max_length=50, null=False, blank=False, default='')
    status_choices = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    status = models.CharField(max_length=50, choices=status_choices, null=False, blank=False, default='')
    createdBy = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    createdDate = models.DateTimeField(blank=True, null=True)
    dueDate = models.DateField(blank=True, null=True)
    startDate = models.DateField(blank=True, null=True)
    endDate = models.DateField(blank=True, null=True)
    contract = models.CharField(max_length=200, blank=True, null=True)
    isDeleted = models.BooleanField(default=False)
    
    # pulled from estimate details
    laborColumn = models.CharField(max_length=50, null=True, blank=True, default='')
    laborFactorMethod = models.CharField(max_length=50, null=True, blank=True, default='')
    imperialMetric = models.CharField(max_length=50, null=True, blank=True, default='', choices=[('imperial','Imperial'), ('metric','Metric')])
    industry = models.CharField(max_length=50, null=True, blank=True, default='')
    applyMarkupOnOverhead = models.BooleanField(default=False)
    applyOverheadAndMarkupOnTax = models.BooleanField(default=False)
    vendorPricingPrecedence = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
    duration = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    timeInterval = models.CharField(max_length=50, null=True, blank=True, default='')

    class Meta:
        managed = True
        db_table = "Bronze].[accubid_estimate"
        verbose_name = "estimate"
        verbose_name_plural = "estimates"


class BidSummary(models.Model):
    id = models.CharField(max_length=50, null=False, blank=False, default='', primary_key=True)
    name = models.CharField(max_length=200, null=False, blank=False, default='')
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, null=False, related_name="bidSummaries")

    class Meta:
        managed = True
        db_table = "Bronze].[accubid_bid_summary"
        verbose_name = "bid summary"
        verbose_name_plural = "bid summaries"


class Project(models.Model):
    id = models.CharField(max_length=50, null=False, blank=False, default='', primary_key=True)
    name = models.CharField(max_length=200, null=False, blank=False, default='')
    number = models.CharField(max_length=50, null=False, blank=False, default='')
    type = models.CharField(max_length=200, null=False, blank=False, default='')
    startDate = models.DateField(blank=True, null=True)
    endDate = models.DateField(blank=True, null=True)
    createdDate = models.DateTimeField(blank=True, null=True)
    createdBy = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    managingBranchName = models.CharField(max_length=200, null=True, blank=True, default='')
    projectPath = models.CharField(max_length=200, null=True, blank=True, default='')
    trimbleProjectId = models.CharField(max_length=50, null=True, blank=True, default='')

    # pulled from project details
    siteName = models.CharField(max_length=200, null=True, blank=True, default='')
    sitePhone = models.CharField(max_length=20, null=True, blank=True, default='')
    siteFax = models.CharField(max_length=20, null=True, blank=True, default='')
    siteStreet1 = models.CharField(max_length=200, null=True, blank=True, default='')
    siteStreet2 = models.CharField(max_length=200, null=True, blank=True, default='')
    siteCity = models.CharField(max_length=200, null=True, blank=True, default='')
    siteState = models.CharField(max_length=50, null=True, blank=True, default='')
    siteZip = models.CharField(max_length=50, null=True, blank=True, default='')
    siteCountry = models.CharField(max_length=50, null=True, blank=True, default='')

    class Meta:
        managed = True
        db_table = "Bronze].[accubid_project"
        verbose_name = "project"
        verbose_name_plural = "projects"


class Database(models.Model):
    token = models.CharField(max_length=200, null=False, blank=False, default='')
    name = models.CharField(max_length=200, null=False, blank=False, default='')
    company = models.CharField(max_length=200, null=False, blank=False, default='')

    class Meta:
        managed = True
        db_table = "Bronze].[accubid_database"
        verbose_name = "database"
        verbose_name_plural = "databases"
