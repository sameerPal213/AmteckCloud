# vim: ai ts=4 sts=4 et sw=4

# coins/models.py
from django.db import models
from geopy.geocoders import Nominatim

class ProjectsDirectory(models.Model):
    id      = models.AutoField(primary_key=True)
    dept    = models.CharField(max_length=3)
    status  = models.CharField(max_length=3)
    stage   = models.CharField(max_length=3)
    boxID   = models.CharField(max_length=255)

    class Meta:
        managed     = True
        db_table    = "coins_projectdirectory"


class Job(models.Model):
    project               = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='job', primary_key=True)
    job_accruals          = models.BooleanField(default=False)
    job_altcur            = models.BooleanField(default=False)
    job_altenq            = models.BooleanField(default=False)
    job_billovride        = models.BooleanField(default=False)
    job_billtoparent      = models.BooleanField(default=False)
    job_buildcal          = models.BooleanField(default=False)
    job_ccmrr             = models.BooleanField(default=False)
    job_complete          = models.BooleanField(default=False)
    job_conden            = models.BooleanField(default=False)
    job_costmove          = models.BooleanField(default=False)
    job_cpint_calc        = models.BooleanField(default=False)
    job_cvrinactive       = models.BooleanField(default=False)
    job_delete            = models.BooleanField(default=False)
    job_desc_1            = models.TextField(null=True)
    job_detcost           = models.BooleanField(default=False)
    job_feecat            = models.BooleanField(default=False)
    job_feetype           = models.BooleanField(default=False)
    job_fmblkstd          = models.BooleanField(default=False)
    job_fmbudfroze        = models.BooleanField(default=False)
    job_fmcustom          = models.BooleanField(default=False)
    job_fmusest           = models.BooleanField(default=False)
    job_fnomorejobs       = models.BooleanField(default=False)
    job_fsched3p          = models.BooleanField(default=False)
    job_fusecomploc       = models.BooleanField(default=False)
    job_fwinsims          = models.BooleanField(default=False)
    job_gencvrcal         = models.BooleanField(default=False)
    job_grns              = models.BooleanField(default=False)
    job_instype           = models.BooleanField(default=False)
    job_lw_sub            = models.BooleanField(default=False)
    job_multcust          = models.BooleanField(default=False)
    job_nonstd            = models.BooleanField(default=False)
    job_open              = models.BooleanField(default=False)
    job_paccruals         = models.BooleanField(default=False)
    job_pacomp            = models.BooleanField(default=False)
    job_paexist           = models.BooleanField(default=False)
    job_paynotrc          = models.BooleanField(default=False)
    job_pgrns             = models.BooleanField(default=False)
    job_phase             = models.BooleanField(default=False)
    job_plpcksm           = models.BooleanField(default=False)
    job_POGandl           = models.BooleanField(default=False)
    job_popcksm           = models.BooleanField(default=False)
    job_pwalloc           = models.BooleanField(default=False)
    job_salesnotrc        = models.BooleanField(default=False)
    job_scpcksm           = models.BooleanField(default=False)
    job_sctatendl         = models.BooleanField(default=False)
    job_shipaddr_1        = models.CharField(max_length=100, null=False)
    job_shipaddr_2        = models.CharField(max_length=100, null=False)
    job_shipaddr_3        = models.CharField(max_length=100, null=False)
    job_shipaddr_4        = models.CharField(max_length=4, null=False)
    job_sin_add           = models.BooleanField(default=False)
    job_sin_def           = models.BooleanField(default=False)
    job_usejobdt          = models.BooleanField(default=False)
    job_usewbs            = models.BooleanField(default=False)
    job_whenpaid          = models.BooleanField(default=False)
    job_xmlerrtrap        = models.BooleanField(default=False)
    cmh_model             = models.CharField(max_length=36,null=False, default='')
    csb_type              = models.CharField(max_length=54,null=False, default='')
    ctt_code              = models.CharField(max_length=16,null=False, default='')
    cur_code              = models.CharField(max_length=18,null=False, default='')
    fcm_code              = models.CharField(max_length=24,null=False, default='')
    jcl_loc               = models.CharField(max_length=54,null=False, default='')
    job_accmeth           = models.CharField(max_length=6,null=False, default='')
    job_accmethp          = models.CharField(max_length=6,null=False, default='')
    job_active            = models.CharField(max_length=6,null=False, default='')
    job_chclass           = models.CharField(max_length=150,null=False, default='')
    job_cmtype            = models.CharField(max_length=30,null=False, default='')
    job_cust              = models.CharField(max_length=342,null=False, default='')
    job_exmpttax          = models.CharField(max_length=36,null=False, default='')
    job_fore              = models.CharField(max_length=66,null=False, default='')
    job_name              = models.CharField(max_length=588,null=False, default='')
    job_num               = models.CharField(max_length=60,null=False, default='')
    job_param             = models.CharField(max_length=1524,null=False, default='')
    job_pcode             = models.CharField(max_length=60,null=False, default='')
    job_revby             = models.CharField(max_length=72,null=False, default='')
    job_revtax            = models.CharField(max_length=36,null=False, default='')
    job_revver            = models.CharField(max_length=60,null=False, default='')
    job_sctatend          = models.CharField(max_length=6,null=False, default='')
    job_security          = models.CharField(max_length=66,null=False, default='')
    job_slacct            = models.CharField(max_length=84,null=False, default='')
    job_sumlevel          = models.CharField(max_length=9,null=False, default='')
    job_tel               = models.CharField(max_length=84,null=False, default='')
    jty_type              = models.CharField(max_length=18,null=False, default='')
    rcm_num               = models.CharField(max_length=48,null=False, default='')
    job_antdate           = models.DateField(null=True)
    job_compdate          = models.DateField(null=True)
    job_condate           = models.DateField(null=True)
    job_eotcomp           = models.DateField(null=True)
    job_opendate          = models.DateField(null=True)
    job_origcomp          = models.DateField(null=True)
    pij_edate             = models.DateField(null=True)
    pij_sdate             = models.DateField(null=True)
    job_eotwks            = models.DecimalField(max_digits=38, decimal_places=0, null=True)
    job_feeval            = models.DecimalField(max_digits=38, decimal_places=2, null=True)
    job_maxorder          = models.DecimalField(max_digits=18, decimal_places=2, null=True)
    job_origwks           = models.DecimalField(max_digits=30, decimal_places=0, null=True)
    job_retention         = models.DecimalField(max_digits=17, decimal_places=2, null=True)
    job_retfpaperc        = models.DecimalField(max_digits=24, decimal_places=2, null=True)
    job_retlim            = models.DecimalField(max_digits=24, decimal_places=2, null=True)
    job_retlimperc        = models.DecimalField(max_digits=30, decimal_places=2, null=True)
    job_retmosperc        = models.DecimalField(max_digits=24, decimal_places=2, null=True)
    job_retmsdperc        = models.DecimalField(max_digits=24, decimal_places=2, null=True)
    job_retperc           = models.DecimalField(max_digits=17, decimal_places=2, null=True)
    job_retscmoffperc     = models.DecimalField(max_digits=24, decimal_places=2, null=True)
    job_retscmosperc      = models.DecimalField(max_digits=24, decimal_places=2, null=True)
    job_retscperc         = models.DecimalField(max_digits=24, decimal_places=2, null=True)
    job_activity          = models.IntegerField(null=True)
    job_casid             = models.IntegerField(null=True)
    job_chseries          = models.IntegerField(null=True)
    job_duration          = models.IntegerField(null=True)
    job_fmStdttime        = models.IntegerField(null=True)
    job_fmtravmph         = models.IntegerField(null=True)
    job_gracedays         = models.IntegerField(null=True)
    job_leadip            = models.IntegerField(null=True)
    job_leadiy            = models.IntegerField(null=True)
    job_leadop            = models.IntegerField(null=True)
    job_leadoy            = models.IntegerField(null=True)
    job_length            = models.IntegerField(null=True)
    job_liability         = models.IntegerField(null=True)
    job_retperiod         = models.IntegerField(null=True)
    job_section           = models.IntegerField(null=True)
    job_stact             = models.IntegerField(null=True)
    job_startwk           = models.IntegerField(null=True)
    job_stkindex          = models.IntegerField(null=True)
    job_stkmeth           = models.IntegerField(null=True)
    job_stsect            = models.IntegerField(null=True)
    job_svs_recduedays    = models.IntegerField(null=True)
    job_svs_submitduedays = models.IntegerField(null=True)
    job_svv_recduedays    = models.IntegerField(null=True)
    job_svv_submitduedays = models.IntegerField(null=True)
    kco                   = models.IntegerField(null=True)
    latitude              = models.DecimalField(max_digits=10, decimal_places=5, null=True)
    longitude             = models.DecimalField(max_digits=11, decimal_places=5, null=True)


    class Meta:
        managed     = True
        db_table    = "coins_job"
        ordering    = ["job_num"]

    def __str__(self):
        return f"{self.job_num} - {self.job_name}"


class Project(models.Model):
    id                  = models.AutoField(primary_key=True)
    fc_code             = models.CharField(max_length=8, null=True, default='', blank=True)
    kco                 = models.IntegerField(null=True, blank=True)
    last_change         = models.DateField(null=True, blank=True)
    mkf_status          = models.CharField(max_length=16, null=True, default='', blank=True)
    mkg_code            = models.CharField(max_length=18, null=False, default='')
    mkm_code            = models.CharField(max_length=18, null=True, default='', blank=True)
    mkm_reserverel      = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    msg_code            = models.CharField(max_length=18, null=True, default='', blank=True)
    pfc_type            = models.CharField(max_length=36, null=True, default='', blank=True)
    pij_abstract        = models.BooleanField(null=True)
    pij_annual          = models.BooleanField(null=True)
    pij_archived        = models.BooleanField(null=True)
    pij_biddue          = models.DateField(null=True, blank=True)
    pij_biddue_time     = models.CharField(max_length=30, null=True, default='', blank=True)
    pij_cashcompl       = models.DateField(null=True, blank=True)
    pij_client1         = models.IntegerField(null=True, blank=True)
    pij_client2         = models.IntegerField(null=True, blank=True)
    pij_close           = models.DateField(null=True, blank=True)
    pij_coinsid         = models.CharField(max_length=222, null=True, default='', blank=True)
    pij_contractno      = models.CharField(max_length=60, null=True, default='', blank=True)
    pij_country         = models.CharField(max_length=40, null=True, default='', blank=True)
    pij_currency        = models.CharField(max_length=18, null=True, default='', blank=True)
    pij_dispno          = models.CharField(max_length=60, null=False, default='')
    pij_edate           = models.DateField(null=True, blank=True)
    pij_estclose        = models.DateField(null=True, blank=True)
    pij_formofexec      = models.CharField(max_length=6, null=True, default='', blank=True)
    pij_invcvo          = models.BooleanField(null=True, blank=True)
    pij_isparent        = models.BooleanField(null=True, blank=True)
    pij_lastrev         = models.DecimalField(max_digits=13, decimal_places=5, null=True, blank=True)
    pij_leadno          = models.CharField(max_length=60, null=True, default='', blank=True)
    pij_manual          = models.BooleanField(null=True)
    pij_marginperc      = models.DecimalField(max_digits=38, decimal_places=2, null=True, blank=True)
    pij_marketSector    = models.CharField(max_length=36, null=True, default='', blank=True)
    pij_multibids       = models.BooleanField(null=True)
    pij_name            = models.CharField(max_length=2592, null=False, default='')
    pij_num             = models.CharField(max_length=42, null=False, default='')
    pij_origweeks       = models.IntegerField(null=True)
    pij_our_value       = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    pij_out_comment     = models.CharField(max_length=1218, null=True, default='', blank=True)
    pij_outcome         = models.CharField(max_length=72, null=True, default='', blank=True)
    pij_parent          = models.CharField(max_length=42, null=True, default='', blank=True)
    pij_plrevmore       = models.BooleanField(null=True)
    pij_recdate         = models.DateField(null=True, blank=True)
    pij_revby           = models.CharField(max_length=78, null=True, default='', blank=True)
    pij_revver          = models.CharField(max_length=60, null=True, default='', blank=True)
    pij_screvmore       = models.BooleanField(null=True)
    pij_sdate           = models.DateField(null=True, blank=True)
    pij_shippcode       = models.CharField(max_length=60, null=True, default='', blank=True)
    pij_tend_value      = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
    pij_tenderno        = models.CharField(max_length=60, null=True, default='', blank=True)
    pij_value           = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
    pij_winprob         = models.CharField(max_length=18, null=True, default='', blank=True)
    pij_worklist        = models.CharField(max_length=40, null=True, default='', blank=True)
    por_type            = models.CharField(max_length=36, null=True, default='', blank=True)
    ppc_seq             = models.IntegerField(null=True, blank=True)
    ppc_seq2            = models.IntegerField(null=True, blank=True)
    ppo_seq             = models.CharField(max_length=24, null=True, default='', blank=True)
    ppo_seq2            = models.CharField(max_length=24, null=True, default='', blank=True)
    ppo_seq3            = models.CharField(max_length=24, null=True, default='', blank=True)
    ppo_seq4            = models.CharField(max_length=24, null=True, default='', blank=True)
    pst_type            = models.CharField(max_length=16, null=True, default='', blank=True)
    pty_type            = models.CharField(max_length=16, null=True, default='', blank=True)
    boxID               = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed     = True
        db_table    = "coins_project"
        ordering    = ["pij_dispno"]

    def __str__(self):
        return f"{self.pij_dispno} - {self.pij_name}"


class Section(models.Model):
    id              = models.AutoField(primary_key=True)
    job_num         = models.CharField(max_length=60,null=False, default='')
    jcs_section     = models.CharField(max_length=48,null=False, default='')
    jcs_desc        = models.TextField()
    jcs_shdesc      = models.TextField()
    last_change     = models.DateField(null=True)
    jcs_revby       = models.CharField(max_length=78,null=False, default='')
    jcs_complete    = models.BooleanField(null=True)
    jcs_active      = models.CharField(max_length=6,null=False, default='')
    jcs_compdate    = models.DateField(null=True)
    jcs_taxable     = models.BooleanField(null=True)
    jcs_taxable     = models.BooleanField(null=True)
    jcs_taxable = models.BooleanField(null=True)
    jcs_taxable = models.BooleanField(null=True)
    jcs_taxable = models.BooleanField(null=True)
    jcs_taxable = models.BooleanField(null=True)
    jcs_exmpttax = models.CharField(max_length=36,null=False, default='')
    jcs_seorder = models.BooleanField(null=True)
    jcs_manager = models.CharField(max_length=66,null=False, default='')

    class Meta:
        managed     = True
        db_table    = "coins_section"
        ordering    = ["job_num","jcs_section"]

    def __str__(self):
        return f"{self.job_num} - {self.jcs_section}"


class CostCode(models.Model):
    id              = models.AutoField(primary_key=True)
    job_num         = models.CharField(max_length=60,null=False, default='')
    jcc_cc          = models.CharField(max_length=60,null=False, default='')
    jcc_desc        = models.TextField(null=True)
    jcc_units       = models.CharField(max_length=12,null=False, default='')
    jcc_quanpost    = models.BooleanField(null=True)
    jcc_glacct_1        = models.TextField(null=True)
    jcc_glacct_2        = models.TextField(null=True)
    jcc_glacct_3        = models.TextField(null=True)
    jcc_glacct_4        = models.TextField(null=True)
    jcc_glacct_5        = models.TextField(null=True)
    jcc_glacct_5        = models.TextField(null=True)
    jcc_costbas     = models.CharField(max_length=12,null=False, default='')
    jcc_item        = models.TextField(null=True)
    jcc_open        = models.BooleanField(null=True)
    jcc_shdesc      = models.TextField(null=True)
    jcc_revacct     = models.CharField(max_length=60,null=False, default='')
    jcc_defcat      = models.CharField(max_length=6,null=False, default='')
    jcc_anal_1      = models.CharField(max_length=78,null=False, default='')
    jcc_anal_2      = models.CharField(max_length=78,null=False, default='')
    jcs_section     = models.CharField(max_length=48,null=False, default='')
    jca_activity    = models.CharField(max_length=18,null=False, default='')
    jsc_cc          = models.CharField(max_length=36,null=False, default='')
    jcc_percomp     = models.DecimalField(null=True,max_digits=17, decimal_places=0)
    jcc_revby       = models.CharField(max_length=60,null=False, default='')

    class Meta:
        managed     = True
        db_table    = "coins_costcode"
        ordering    = ["job_num","jcc_cc"]

    def __str__(self):
        return f"{self.job_num} - {self.jcc_cc}"


class Activity(models.Model):
    id              = models.AutoField(primary_key=True)
    job_num         = models.CharField(max_length=60,null=False, default='')
    jph_phase       = models.CharField(max_length=4,null=False, default='')
    jca_activity    = models.CharField(max_length=18,null=False, default='')
    last_change     = models.DateField(null=True)
    jja_desc        = models.TextField(null=True)
    jja_shdesc      = models.TextField(null=True)
    jja_chclass     = models.CharField(max_length=60,null=False, default='')
    jja_class       = models.CharField(max_length=16,null=False, default='')
    jca_revby       = models.CharField(max_length=60,null=False, default='')
    jca_revver      = models.CharField(max_length=60,null=False, default='')
    jca_retired     = models.BooleanField(null=True)
    jca_param       = models.CharField(max_length=16,null=False, default='')

    class Meta:
        managed     = True
        db_table    = "coins_activity"
        ordering    = ["job_num","jca_activity"]
        verbose_name_plural = "Activities"

    def __str__(self):
        return f"{self.job_num} - {self.jca_activity}"


class WBS(models.Model):
    id              = models.AutoField(primary_key=True)
    job_num         = models.CharField(max_length=60,null=False, default='')
    jph_phase       = models.CharField(max_length=4,null=False, default='')
    jwb_code        = models.CharField(max_length=48,null=False, default='')
    jwb_desc        = models.TextField(null=True)
    jca_activity    = models.CharField(max_length=18,null=False, default='')
    jcs_section     = models.CharField(max_length=48,null=False, default='')
    jwb_percomp         = models.DecimalField(null=True,max_digits=17, decimal_places=2)
    jwb_costs       = models.DecimalField(null=True,max_digits=17, decimal_places=2)
    jwb_level       = models.IntegerField(null=True)
    last_change     = models.DateField(null=True)
    jwb_todate      = models.DateField(null=True)
    jwb_fromdate    = models.DateField(null=True)
    jwb_revby       = models.CharField(max_length=60,null=False, default='')
    jwb_revver      = models.CharField(max_length=60,null=False, default='')
    jwb_paingain_1  = models.BooleanField(null=True)
    jwb_paingain_2  = models.BooleanField(null=True)
    jwb_paingain_3  = models.BooleanField(null=True)
    jwb_paingain_4  = models.BooleanField(null=True)
    jwb_paingain_5  = models.BooleanField(null=True)
    jwb_defcss      = models.CharField(max_length=16,null=False, default='')
    jwb_fcctype     = models.IntegerField(null=True)
    jwb_qty         = models.DecimalField(null=True,max_digits=20, decimal_places=8)
    csb_type        = models.CharField(max_length=16,null=False, default='')
    jwb_fccbase     = models.CharField(max_length=24,null=False, default='')
    jwb_units       = models.CharField(max_length=18,null=False, default='')
    stl_code        = models.CharField(max_length=16,null=False, default='')

    class Meta:
        managed     = True
        db_table    = "coins_wbs"
        ordering    = ["job_num","jwb_code"]

    def __str__(self):
        return f"{self.job_num} - {self.jwb_code}"


class CostTransaction(models.Model):
    id              = models.AutoField(primary_key=True)
    job_num = models.CharField(max_length=60,null=False, default='')
    jcc_cc = models.CharField(max_length=60,null=False, default='')
    kco = models.IntegerField(null=True)
    jct_cat = models.CharField(max_length=6,null=False, default='')
    jct_fdate = models.DateField(null=True)
    jct_tdate = models.DateField(null=True)
    coj_source = models.CharField(max_length=12,null=False, default='')
    coj_type = models.CharField(max_length=24,null=False, default='')
    jct_amount = models.DecimalField(null=True,max_digits=20, decimal_places=2)
    jct_rhrs = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    jct_iref = models.CharField(max_length=60,null=False, default='')
    jct_qty = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    jct_effdate = models.DateField(null=True)
    cob_num = models.IntegerField(null=True)
    gla_acct = models.CharField(max_length=60,null=False, default='')
    jct_xref = models.CharField(max_length=60,null=False, default='')
    cbt_type = models.CharField(max_length=36,null=False, default='')
    jct_srcnum = models.IntegerField(null=True)
    jct_wedate = models.DateField(null=True)
    jct_cur_amt_1 = models.DecimalField(null=True,max_digits=20, decimal_places=2)
    jct_cur_amt_2 = models.DecimalField(null=True,max_digits=20, decimal_places=2)
    jct_cur_amt_6 = models.DecimalField(null=True,max_digits=20, decimal_places=2)
    jct_lastrev = models.DecimalField(null=True,max_digits=20, decimal_places=5)
    jct_revby = models.CharField(max_length=60,null=False, default='')
    jct_revver = models.CharField(max_length=60,null=False, default='')
    jct_xml = models.TextField(null=True)
    jct_uoq = models.CharField(max_length=18,null=False, default='')
    jct_coinsid = models.TextField(null=True)
    jct_salestax = models.DecimalField(null=True,max_digits=32, decimal_places=2)
    jct_cur_salestax_1 = models.DecimalField(null=True,max_digits=20, decimal_places=2)
    jct_cur_salestax_2 = models.DecimalField(null=True,max_digits=20, decimal_places=2)
    jct_cur_salestax_6 = models.DecimalField(null=True,max_digits=20, decimal_places=2)
    jct_cur_tax_1 = models.DecimalField(null=True,max_digits=20, decimal_places=2)
    jct_cur_tax_2 = models.DecimalField(null=True,max_digits=20, decimal_places=2)
    jct_cur_tax_6 = models.DecimalField(null=True,max_digits=20, decimal_places=2)
    jct_tax = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    jct_cur_chg1amt_1 = models.DecimalField(null=True,max_digits=20, decimal_places=2)
    jct_cur_chg1amt_2 = models.DecimalField(null=True,max_digits=20, decimal_places=2)
    jct_cur_chg1amt_6 = models.DecimalField(null=True,max_digits=20, decimal_places=2)
    imt_ref = models.IntegerField(null=True)
    jct_srckco = models.IntegerField(null=True)

    class Meta:
        managed     = True
        db_table    = "coins_costtransaction"
        ordering    = ["job_num","jcc_cc"]
        verbose_name = "Cost Transaction"

    def __str__(self):
        return f"{self.job_num} - {self.jcc_cc}"


class PurchaseOrder(models.Model):
    id              = models.AutoField(primary_key=True)
    kco = models.IntegerField(null=True)
    poh_ordno = models.CharField(max_length=60,null=False, default='')
    poh_chgno = models.CharField(max_length=18,null=False, default='')
    pot_type = models.CharField(max_length=6,null=False, default='')
    poh_accno = models.CharField(max_length=48,null=False, default='')
    poh_odate = models.DateField(null=True)
    poh_ddate = models.DateField(null=True)
    poh_analysis = models.CharField(max_length=60,null=False, default='')
    job_num = models.CharField(max_length=60,null=False, default='')
    poh_attention = models.TextField(null=True)
    poh_name = models.TextField(null=True)
    poh_add_1 = models.TextField(null=True)
    poh_add_2 = models.TextField(null=True)
    poh_add_3 = models.TextField(null=True)
    poh_add_4 = models.TextField(null=True)
    poh_pcode = models.CharField(max_length=60,null=False, default='')
    poh_reqdby = models.CharField(max_length=60,null=False, default='')
    pob_code = models.CharField(max_length=60,null=False, default='')
    poh_shipaddr_1 = models.TextField(null=True)
    poh_shipaddr_2 = models.TextField(null=True)
    poh_shipaddr_3 = models.TextField(null=True)
    poh_shipaddr_4 = models.TextField(null=True)
    poh_printed = models.BooleanField(null=True)
    poh_amount = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    poh_prndate = models.DateField(null=True)
    poh_reprndate = models.DateField(null=True)
    poh_reprints = models.IntegerField(null=True)
    tip_type = models.CharField(max_length=48,null=False, default='')
    poh_desc = models.TextField(null=True)
    cim_intref = models.IntegerField(null=True)
    cio_intref = models.IntegerField(null=True)
    poh_offname = models.TextField(null=True)
    poh_tradingas = models.TextField(null=True)
    poh_specins_1 = models.TextField(null=True)
    poh_committed = models.BooleanField(null=True)
    poh_cancelled = models.BooleanField(null=True)
    poh_reqno = models.TextField(null=True)
    poh_agreement = models.BooleanField(null=True)
    pja_code = models.TextField(null=True)
    cim_legalname_1 = models.TextField(null=True)
    tsv_code = models.CharField(max_length=32,null=False, default='')
    cof_form = models.CharField(max_length=60,null=False, default='')
    poh_sctype = models.CharField(max_length=18,null=False, default='')
    poh_famount = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    poh_internal = models.TextField(null=True)
    poh_mpo = models.CharField(max_length=6,null=False, default='')
    cof_form2 = models.CharField(max_length=60,null=False, default='')
    poh_terms_1 = models.CharField(max_length=60,null=False, default='')
    poh_terms_2 = models.CharField(max_length=60,null=False, default='')
    poh_grnreq = models.CharField(max_length=6,null=False, default='')
    poh_items = models.IntegerField(null=True)
    poh_votype = models.CharField(max_length=6,null=False, default='')
    poh_lastchgno = models.CharField(max_length=18,null=False, default='')
    poh_lastvotype = models.CharField(max_length=6,null=False, default='')
    poh_shippcode = models.CharField(max_length=60,null=False, default='')
    ppg_no = models.IntegerField(null=True)
    poh_origddate = models.DateField(null=True)
    poh_lastrev = models.DateTimeField(null=True)
    poh_revby = models.CharField(max_length=60,null=False, default='')
    poh_revver = models.CharField(max_length=60,null=False, default='')
    peh_enqno = models.CharField(max_length=60,null=False, default='')
    poh_commitby = models.CharField(max_length=60,null=False, default='')
    poh_commiton = models.DateField(null=True)
    poh_xml = models.TextField(null=True)
    poh_appstat = models.CharField(max_length=18,null=False, default='')
    jwb_code = models.CharField(max_length=48,null=False, default='')
    poh_coinsid = models.TextField(null=True)
    poh_grnreqp = models.CharField(max_length=6,null=False, default='')
    vat_code = models.CharField(max_length=48,null=False, default='')
    poh_tax = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    poh_perfbond = models.CharField(max_length=6,null=False, default='')
    poh_warranties = models.CharField(max_length=6,null=False, default='')
    poh_lw_sub = models.BooleanField(null=True)
    poh_param = models.TextField(null=True)
    poh_paytype = models.CharField(max_length=6,null=False, default='')
    poh_whenpaid = models.BooleanField(null=True)
    cdf_type = models.CharField(max_length=18,null=False, default='')
    poh_dRet = models.DecimalField(null=True,max_digits=24, decimal_places=2)
    poh_groupstat = models.CharField(max_length=24,null=False, default='')
    poh_lumpsumpo = models.BooleanField(null=True)
    poh_multianal = models.CharField(max_length=6,null=False, default='')
    poh_ftax = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    ttt_code = models.CharField(max_length=48,null=False, default='')
    poh_commitdt = models.DateTimeField(null=True)
    poh_grn_mix = models.CharField(max_length=16,null=False, default='')
    oh_walloc_mix = models.CharField(max_length=16,null=False, default='')
    poh_chgref = models.CharField(max_length=18,null=False, default='')
    poh_chgformat = models.CharField(max_length=18,null=False, default='')

    class Meta:
        managed     = True
        db_table    = "coins_purchaseorder"
        ordering    = ["job_num","poh_ordno", "poh_chgno"]
        verbose_name = "Purchase Order"

    def __str__(self):
        return f"{self.poh_ordno} {self.poh_chgno}"


class PurchaseOrderLine(models.Model):
    id              = models.AutoField(primary_key=True)
    kco = models.IntegerField(null=True)
    poh_ordno = models.CharField(max_length=60,null=False, default='')
    poh_chgno = models.CharField(max_length=18,null=False, default='')
    jwb_code = models.CharField(max_length=48,null=False, default='')
    pol_seq = models.IntegerField(null=True)
    pol_price = models.DecimalField(null=True,max_digits=38, decimal_places=5)
    pol_qty = models.DecimalField(null=True,max_digits=38, decimal_places=8)
    poi_item = models.CharField(max_length=24,null=False, default='')
    pol_desc_1 = models.TextField(null=True)
    pol_desc_2 = models.TextField(null=True)
    pol_desc_3 = models.TextField(null=True)
    pol_desc_4 = models.TextField(null=True)
    pol_type = models.CharField(max_length=6,null=False, default='')
    pol_pcat = models.CharField(max_length=6,null=False, default='')
    gla_acct = models.TextField(null=True)
    jcc_cc = models.CharField(max_length=60,null=False, default='')
    job_num = models.CharField(max_length=60,null=False, default='')
    pol_analysis = models.TextField(null=True)
    pol_cat = models.CharField(max_length=6,null=False, default='')
    pol_amount = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    pol_per = models.CharField(max_length=12,null=False, default='')
    pol_uoq = models.CharField(max_length=12,null=False, default='')
    tsv_code = models.CharField(max_length=60,null=False, default='')
    tip_type = models.CharField(max_length=48,null=False, default='')
    pol_ddate = models.DateField(null=True)
    pol_code = models.CharField(max_length=60,null=False, default='')
    pol_factor = models.DecimalField(null=True,max_digits=38, decimal_places=5)
    pol_qtyclass = models.CharField(max_length=6,null=False, default='')
    pol_tendqty = models.DecimalField(null=True,max_digits=38, decimal_places=8)
    pol_orderrate = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    pol_orderval = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    pol_votype = models.CharField(max_length=6,null=False, default='')
    pol_effdate = models.DateField(null=True)
    rqh_reqno = models.CharField(max_length=60,null=False, default='')
    rql_seq = models.IntegerField(null=True)
    rqb_seq = models.IntegerField(null=True)
    pol_famount = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    rqi_item = models.CharField(max_length=18,null=False, default='')
    pol_xml = models.TextField(null=True)
    pol_coinsid = models.TextField(null=True)
    vat_code = models.CharField(max_length=48,null=False, default='')
    pol_tax = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    pol_param = models.TextField(null=True)
    pol_chgovd_1 = models.BooleanField(null=True)
    pol_chgovd_2 = models.BooleanField(null=True)
    pol_chgovd_3 = models.BooleanField(null=True)
    pol_chgtax_1 = models.BooleanField(null=True)

    class Meta:
        managed     = True
        db_table    = "coins_purchaseorderline"
        ordering    = ["job_num","poh_ordno"]
        verbose_name = "Purchase Order Line"

    def __str__(self):
        return f"{self.poh_ordno}"


class PurchaseOrderItem(models.Model):
    id              = models.AutoField(primary_key=True)
    kco = models.IntegerField(null=True)
    tip_type = models.CharField(max_length=48,null=False, default='')
    poh_ordno = models.CharField(max_length=60,null=False, default='')
    poi_item = models.CharField(max_length=24,null=False, default='')
    poi_ddate = models.DateField(null=True)
    poi_qtybal = models.DecimalField(null=True,max_digits=38, decimal_places=8)
    poi_qtydel = models.DecimalField(null=True,max_digits=38, decimal_places=8)
    poi_qtyinv = models.DecimalField(null=True,max_digits=38, decimal_places=8)
    poi_amtinv = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    poi_complete = models.BooleanField(null=True)
    poi_amount = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    poi_analysis = models.TextField(null=True)
    poi_canbal = models.DecimalField(null=True,max_digits=38, decimal_places=8)
    poi_fcuser = models.CharField(max_length=60,null=False, default='')
    poi_fcdate = models.DateField(null=True)
    poi_qty = models.DecimalField(null=True,max_digits=38, decimal_places=8,)
    tsv_code = models.CharField(max_length=60,null=False, default='')
    rqh_reqno = models.CharField(max_length=60,null=False, default='')
    rql_seq = models.IntegerField(null=True)
    rqb_seq = models.IntegerField(null=True)
    poi_lastrev = models.TextField(null=True)
    poi_revby = models.CharField(max_length=60,null=False, default='')
    poi_coinsid = models.TextField(null=True)
    vat_code = models.CharField(max_length=48,null=False, default='')
    poi_tax = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    poi_param = models.TextField(null=True)
    poi_fchargeinv_1 = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    poi_ftax = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    poi_amtinv_base = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    poi_chargeinv_1 = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    poi_ftaxinv = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    poi_taxinv = models.DecimalField(null=True,max_digits=38, decimal_places=2)

    class Meta:
        managed     = True
        db_table    = "coins_purchaseorderitem"
        ordering    = ["poh_ordno"]
        verbose_name = "Purchase Order Item"

    def __str__(self):
        return f"{self.poh_ordno}"


class ContractManagerJob(models.Model):
    id              = models.AutoField(primary_key=True)
    kco = models.IntegerField(null=True)
    job_num = models.CharField(max_length=60,null=False, default='')
    svj_lastrev = models.DecimalField(null=True,max_digits=38, decimal_places=8)
    svj_revby = models.CharField(max_length=60,null=False, default='')
    svj_revver = models.CharField(max_length=60,null=False, default='')
    svj_coinsid = models.TextField(null=True)
    svj_res = models.BooleanField(null=True)
    svj_start = models.DateField(null=True)
    svj_pdate = models.DateField(null=True)
    svj_sdate = models.DateField(null=True)
    svj_edate = models.DateField(null=True)
    svj_fadate = models.DateField(null=True)
    svj_jobtemplate = models.CharField(max_length=60,null=False, default='')

    class Meta:
        managed     = True
        db_table    = "coins_contractmanagerjob"
        ordering    = ["job_num"]
        verbose_name = "Contract Manager Job"

    def __str__(self):
        return f"{self.job_num}"


class SOVItem(models.Model):
    id              = models.AutoField(primary_key=True)
    kco = models.IntegerField(null=True)
    job_num = models.CharField(max_length=60,null=False, default='')
    svl_type = models.CharField(max_length=24,null=False, default='')
    svi_id = models.IntegerField(null=True)
    svi_seq = models.DecimalField(null=True,max_digits=38, decimal_places=5)
    svi_item = models.CharField(max_length=60,null=False, default='')
    svi_desc = models.TextField(null=True)
    svi_vqty = models.DecimalField(null=True,max_digits=38, decimal_places=8)
    svi_intvalue = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svi_vintvalue = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svi_extvalue = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svi_vextvalue = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svi_shdesc = models.TextField(null=True)
    svi_lastrev = models.DateTimeField(null=True)
    svi_revby = models.CharField(max_length=60,null=False, default='')
    svi_revver = models.CharField(max_length=60,null=False, default='')
    svi_xml = models.TextField(null=True)
    svi_coinsid = models.TextField(null=True)
    svi_clientref = models.TextField(null=True)
    svi_intrate = models.DecimalField(null=True,max_digits=17, decimal_places=2)
    svi_vintrate = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svi_extrate = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svi_vextrate = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svi_level1_seq = models.IntegerField(null=True)
    svi_level1_code = models.CharField(max_length=60,null=False, default='')
    svi_level1_id = models.IntegerField(null=True)
    css_series = models.CharField(max_length=60,null=False, default='')
    svv_type = models.CharField(max_length=30,null=False, default='')
    svv_number = models.CharField(max_length=60,null=False, default='')
    svi_splintrt_1 = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svi_splintrt_2 = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svi_splintrt_3 = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svi_splintrt_4 = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svi_splintrt_5 = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svi_splintrt_6 = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svi_splvintrt_1 = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svi_splvintrt_2 = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svi_splvintrt_3 = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svi_splvintrt_4 = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svi_splvintrt_5 = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svi_splvintrt_6 = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svi_splextrt_1 = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svi_splvextrt_1 = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svi_splintval_1 = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svi_splintval_2 = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svi_splintval_3 = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svi_splintval_4 = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svi_splintval_5 = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svi_splintval_6 = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svi_splvintval_1 = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svi_splvintval_2 = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svi_splvintval_3 = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svi_splvintval_4 = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svi_splvintval_5 = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svi_splvintval_6 = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svi_splextval_1 = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svi_splvextval_1 = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    vat_code = models.CharField(max_length=36,null=False, default='')
    svi_level_codes_1 = models.CharField(max_length=60,null=False, default='')
    svi_level_seqs_1 = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svi_level_ids_1 = models.IntegerField(null=True)
    svi_csaref = models.CharField(max_length=42,null=False, default='')
    svi_ctakeup = models.DecimalField(null=True,max_digits=38, decimal_places=3)
    svi_rtakeup = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svi_billtype = models.CharField(max_length=48,null=False, default='')
    svi_matosret = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svi_status = models.CharField(max_length=36,null=False, default='')
    svi_revanal = models.TextField(null=True)

    class Meta:
        managed     = True
        db_table    = "coins_sovitem"
        ordering    = ["job_num"]
        verbose_name = "SOV Item"

    def __str__(self):
        return f"{self.job_num}"


class SOVChangeManagement(models.Model):
    id              = models.AutoField(primary_key=True)
    kco = models.IntegerField(null=True)
    job_num = models.CharField(max_length=60,null=False, default='')
    svl_type = models.CharField(max_length=24,null=False, default='')
    svv_type = models.CharField(max_length=30,null=False, default='')
    svv_number = models.CharField(max_length=60,null=False, default='')
    svv_desc = models.TextField(null=True)
    svv_detail = models.TextField(null=True)
    svv_lastrev = models.DateTimeField(null=True)
    svv_revby = models.CharField(max_length=60,null=False, default='')
    svv_revver = models.CharField(max_length=60,null=False, default='')
    svv_coinsid = models.TextField(null=True)
    svv_tdate = models.DateField(null=True)
    svv_ldate = models.DateField(null=True)
    svv_aino = models.CharField(max_length=60,null=False, default='')
    svv_aiconum = models.CharField(max_length=60,null=False, default='')
    svv_clref = models.CharField(max_length=60,null=False, default='')
    svv_status = models.CharField(max_length=36,null=False, default='')
    css_series = models.CharField(max_length=60,null=False, default='')
    svv_ctakeup = models.DecimalField(null=True,max_digits=38, decimal_places=3)
    svv_rtakeup = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svv_userid = models.CharField(max_length=60,null=False, default='')
    svv_estvalue_1 = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svv_estcost_L = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svv_estcost_M = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svv_estcost_E = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svv_estcost_S = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svv_estcost_O = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svv_estcost_T = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svv_appvalue_1 = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svv_appcost_L = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svv_appcost_M = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svv_appcost_E = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svv_appcost_S = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svv_appcost_O = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svv_appcost_T = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svv_tappcost = models.DecimalField(
            null=True,
            max_digits=38, 
            decimal_places=2,
            verbose_name='Approved Cost')
    svv_testcost = models.DecimalField(
            null=True,
            max_digits=38, 
            decimal_places=2,
            verbose_name='Proposed Cost')
    svv_tappvalue = models.DecimalField(
            null=True,
            max_digits=38, 
            decimal_places=2,
            verbose_name='Approved Value')
    svv_testvalue = models.DecimalField(
            null=True,
            max_digits=38, 
            decimal_places=2,
            verbose_name='Proposed Value')
    svv_intref = models.IntegerField(null=True)
    vat_code = models.CharField(max_length=36,null=False, default='')
    svv_pricing = models.CharField(max_length=16,null=False, default='')
    ppo_seq = models.CharField(max_length=24,null=False, default='')
    svv_effdate = models.DateField(null=True)
    svi_billtype = models.CharField(max_length=48,null=False, default='')
    svi_revanal = models.CharField(max_length=60,null=False, default='')
    svv_date_received = models.DateField(null=True)

    class Meta:
        managed     = True
        db_table    = "coins_sovchangemanagement"
        ordering    = ["job_num"]
        verbose_name = "SOV Change Management"

    def __str__(self):
        return f"{self.job_num}"


class SOVResource(models.Model):
    id              = models.AutoField(primary_key=True)
    kco = models.IntegerField(null=True)
    job_num = models.CharField(max_length=60,null=False, default='')
    svl_type = models.CharField(max_length=24,null=False, default='')
    svi_id = models.IntegerField(null=True)
    svr_id = models.IntegerField(null=True)
    svr_seq = models.IntegerField(null=True)
    svr_desc = models.TextField(null=True)
    tsv_type = models.CharField(max_length=48,null=False, default='')
    tsv_code = models.CharField(max_length=32,null=False, default='')
    jwb_code = models.CharField(max_length=36,null=False, default='')
    svr_qty = models.DecimalField(null=True,max_digits=38, decimal_places=8)
    tun_unit = models.CharField(max_length=12,null=False, default='')
    svr_intvalue = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svr_extvalue = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svr_lastrev = models.DateTimeField(null=True)
    svr_revby = models.CharField(max_length=60,null=False, default='')
    svr_revver = models.CharField(max_length=60,null=False, default='')
    svr_coinsid = models.TextField(null=True)
    svr_cat = models.CharField(max_length=6,null=False, default='')
    jcc_cc = models.CharField(max_length=60,null=False, default='')
    svr_intrate = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svr_extrate = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    css_series = models.CharField(max_length=60,null=False, default='')
    svr_vintrate = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svr_vextrate = models.DecimalField(null=True,max_digits=38, decimal_places=4)
    svr_vintvalue = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svr_vextvalue = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svr_analysis = models.CharField(max_length=60,null=False, default='')
    jsc_cc = models.CharField(max_length=36,null=False, default='')
    svr_ctakuppercent = models.DecimalField(null=True,max_digits=38, decimal_places=3)
    svr_rtakeuppercent = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svr_plant = models.BooleanField(null=True)
    svr_perunit_1 = models.CharField(max_length=48,null=False, default='')
    svr_perunit_2 = models.CharField(max_length=48,null=False, default='')
    svr_budqty = models.DecimalField(null=True,max_digits=38, decimal_places=2)
    svr_revonly = models.BooleanField(null=True)

    class Meta:
        managed     = True
        db_table    = "coins_sovresource"
        ordering    = ["job_num"]
        verbose_name = "SOV Resource"

    def __str__(self):
        return f"{self.job_num}"


class Employee(models.Model):
    id          = models.AutoField(primary_key=True)
    coins_id    = models.CharField(max_length=10, null=False, default='')
    first_name  = models.CharField(max_length=50, null=False, default='')
    middle_name = models.CharField(max_length=50, null=False, default='', blank=True)
    last_name   = models.CharField(max_length=50, null=False, default='')
    suffix      = models.CharField(max_length=50, null=False, default='', blank=True)
    payroll_type    = models.CharField(max_length=20, null=False, default='')
    class_name       = models.CharField(max_length=50, null=False, default='')
    status      = models.CharField(max_length=10, null=False, default='')
    original_hire_date  = models.DateField(null=True, blank=True)
    last_rehire_date    = models.DateField(null=True, blank=True)
    manually_entered    = models.DateField(null=True, blank=True)
    benefit_group       = models.CharField(max_length=50, null=False
            , default='')
    date_of_birth       = models.DateField(null=True, blank=True)
    flsa_status         = models.CharField(max_length=50, null=False, default='', blank=True)
    termination_date    = models.DateField(null=True, blank=True)
    job_title           = models.CharField(max_length=50, null=False, default='')    

    class Meta:
        managed= True
        db_table= "coins_employee"
        ordering= ["last_name","first_name"]
        verbose_name = "Employee"
        
    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
