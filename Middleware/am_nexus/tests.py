import os
import django

# # --- Setup Django environment ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Middleware.am_nexus.settings')  # Replace with your project name
django.setup()

from forms.models import Qaqc1001Response  # Import your Project model
from coins.models import Project, Job  # Import the Project model from coins app

# job = Job.objects.get(project_id=1)
# project = Project.objects.get(id=5)
# job = Job.objects.get(project=project)

def insert_project():
    # Insert data into Project table
    project = Qaqc1001Response.objects.create(
        fc_code='FC001',
        kco=1,
        mkf_status='Active',
        mkg_code='MKG001',
        mkm_code='MKM001',
        mkm_reserverel=100,
        msg_code='MSG001',
        pfc_type='TypeA',
        pij_abstract='1',
        pij_annual='0',
        pij_archived='0',
        pij_biddue_time='12:00',
        pij_client1=101,
        pij_client2=102,
        pij_coinsid='COINS001',
        pij_contractno='CN001',
        pij_country='CountryA',
        pij_currency='USD',
        pij_dispno='DISP001',
        pij_formofexec='Exec1',
        pij_invcvo='1',
        pij_isparent='0',
        pij_lastrev=123.45678,
        pij_leadno='Lead1',
        pij_manual='1',
        pij_marginperc=10.5,
        pij_marketSector='Sector1',
        pij_multibids='1',
        pij_name='Project One',
        pij_num='NUM001',
        pij_origweeks=10,
        pij_our_value=1000,
        pij_out_comment='Comment1',
        pij_outcome='Outcome1',
        pij_parent='Parent1',
        pij_plrevmore='1',
        pij_revby='RevBy1',
        pij_revver='Ver1',
        pij_screvmore='0',
        pij_shippcode='Ship1',
        pij_tend_value=500,
        pij_tenderno='Tender1',
        pij_value=1500,
        pij_winprob='WinProb1',
        pij_worklist='Worklist1',
        por_type='TypeP',
        ppc_seq=1,
        ppc_seq2=2,
        ppo_seq='PS1',
        ppo_seq2='PS2',
        ppo_seq3='PS3',
        ppo_seq4='PS4',
        pst_type='PST1',
        pty_type='PTY1',
        boxID='Box1'
    )
    print(f"Inserted Project with ID {project.id} and Name {project.pij_name}")

if __name__ == "__main__":
    insert_project()


# # project = Project.objects.get(id=5)

# # Insert sample data
# record = Qaqc1001Response.objects.create(
#     project=job,
#     area="North Wing",
#     sheet_no=101,
#     drawing="DRW-2025-001",
#     conduit_run_from="Panel A",
#     conduit_run_to="Panel B",
    
#     conforms_to_NEC=True,
#     conforms_to_NEC_corrections_needed=False,
#     conforms_to_NEC_corrections_completed=False,

#     installed_per_drawing=True,
#     installed_per_drawing_corrections_needed=False,
#     installed_per_drawing_corrections_completed=False,

#     supports_anchored=True,
#     supports_anchored_corrections_needed=False,
#     supports_anchored_corrections_completed=False,

#     conduit_leveled=True,
#     conduit_leveled_corrections_needed=False,
#     conduit_leveled_corrections_completed=False,

#     material_classification=True,
#     material_classification_corrections_needed=False,
#     material_classification_corrections_completed=False,

#     pull_points=True,
#     pull_points_corrections_needed=False,
#     pull_points_corrections_completed=False,

#     expansion_joints=False,
#     expansion_joints_corrections_needed=False,
#     expansion_joints_corrections_completed=False,

#     low_point_drains=False,
#     low_point_drains_corrections_needed=False,
#     low_point_drains_corrections_completed=False,

#     unions=True,
#     unions_corrections_needed=False,
#     unions_corrections_completed=False,

#     seals=True,
#     seals_corrections_needed=False,
#     seals_corrections_completed=False,

#     couplings_tight=True,
#     couplings_tight_corrections_needed=False,
#     couplings_tight_corrections_completed=False,

#     excessive_threads=False,
#     excessive_threads_corrections_needed=False,
#     excessive_threads_corrections_completed=False,

#     bushings=True,
#     bushings_corrections_needed=False,
#     bushings_corrections_completed=False,

#     bonding_jumpers=True,
#     bonding_jumpers_corrections_needed=False,
#     bonding_jumpers_corrections_completed=False,

#     field_changes_on_drawing=False,
#     field_changes_on_drawing_corrections_needed=False,
#     field_changes_on_drawing_corrections_completed=False,

#     test_signature=None  # You can set this if you have a signature value
# )

# print(f"Inserted record with ID {record.id}")



# from coins.models import Job, Project  # Adjust app name as needed
# from datetime import date

# # Get the Project with ID 5
# project = Project.objects.get(id=5)

# job = Job.objects.create(
#     project=project,
#     job_shipaddr_1="123 Main Street",
#     job_shipaddr_2="Suite 101",
#     job_shipaddr_3="Industrial Area",
#     job_shipaddr_4="P1",
#     cmh_model="Model-A",
#     csb_type="Construction",
#     ctt_code="CTT001",
#     cur_code="USD",
#     fcm_code="FCM123",
#     jcl_loc="North Yard",
#     job_accmeth="STD",
#     job_accmethp="STD",
#     job_active="a",
#     job_chclass="Standard Class",
#     job_cmtype="Type-1",
#     job_cust="Customer ABC",
#     job_exmpttax="NONE",
#     job_fore="Manager John",
#     job_name="Warehouse Construction Phase 1",
#     job_num="JOB-1001",
#     job_param="Default Params",
#     job_pcode="PC001",
#     job_revby="Auditor A",
#     job_revtax="REV-TAX-001",
#     job_revver="REV1",
#     job_sctatend="N",
#     job_security="Level-2",
#     job_slacct="ACCT-567",
#     job_sumlevel="L1",
#     job_tel="123-456-7890",
#     jty_type="TY-A",
#     rcm_num="RCM-99",
    
#     # Dates
#     job_antdate=date(2025, 7, 21),
#     job_compdate=None,
#     job_condate=None,
#     job_eotcomp=None,
#     job_opendate=date(2025, 7, 1),
#     job_origcomp=None,
#     pij_edate=None,
#     pij_sdate=None,
    
#     # Numeric fields
#     job_eotwks=0,
#     job_feeval=100000.00,
#     job_maxorder=500000.00,
#     job_origwks=52,
#     job_retention=5.00,
#     job_retfpaperc=0.00,
#     job_retlim=10000.00,
#     job_retlimperc=10.00,
#     job_retmosperc=5.00,
#     job_retmsdperc=5.00,
#     job_retperc=5.00,
#     job_retscmoffperc=0.00,
#     job_retscmosperc=0.00,
#     job_retscperc=0.00,
#     job_activity=1,
#     job_casid=1,
#     job_chseries=1,
#     job_duration=120,
#     job_fmStdttime=8,
#     job_fmtravmph=60,
#     job_gracedays=10,
#     job_leadip=0,
#     job_leadiy=0,
#     job_leadop=0,
#     job_leadoy=0,
#     job_length=300,
#     job_liability=100000,
#     job_retperiod=12,
#     job_section=2,
#     job_stact=1,
#     job_startwk=1,
#     job_stkindex=1,
#     job_stkmeth=1,
#     job_stsect=1,
#     job_svs_recduedays=30,
#     job_svs_submitduedays=30,
#     job_svv_recduedays=30,
#     job_svv_submitduedays=30,
#     kco=1,
#     latitude=12.97160,
#     longitude=77.59460
# )

# print(f"Job {job.job_num} created for Project ID {project.id}")
