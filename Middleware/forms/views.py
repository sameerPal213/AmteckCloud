# forms/views.py
import io
import math
import requests
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect, FileResponse
from django.views import generic
from django.urls import reverse
from django.templatetags.static import static
from box.models import ProjectFolders
from django.db.models import Count, Q
from box.utils import create_folder_in_folder, get_file_embed, searchFolder, upload_file_to_box
from coins.models import Project
from .forms import (
    QAQC100_1_Model_Form as QAQC100_1, SafetyTaskAnalysisForm, STAPostTaskForm, 
    AMQ100_1_Model_Form as AMQ100_1,
    AMQ100_2_Model_Form as AMQ100_2,
    AMQ100_3_Model_Form as AMQ100_3,
    AMQ130_1_Model_Form as AMQ130_1,
    AMQ140_1_Model_Form as AMQ140_1,
    AMQ200_1_Model_Form as AMQ200_1,
    AMQ160_1_Model_Form as AMQ160_1,
    AMQ160_2_Model_Form as AMQ160_2,
    AMQ150_2_Model_Form as AMQ150_2,
    AMQ150_1_Model_Form as AMQ150_1,
    get_STAEmployeeAcknowledgementFormSet, get_STAHazardMitigationFormSet, 
    get_STARequiredEmployeeCertificationFormSet, get_STARequiredPermitFormSet, 
    get_STARequiredProcedureFormSet, get_STARequiredSpecialCertificationFormSet, 
    get_STAToolInspectionFormSet)
from .models import (Qaqc1001Response, STAEmployeeAcknowledgement, STAEmployeeCertification, 
                    STAPermit, STAProcedure, STARequiredEmployeeCertification, STARequiredPermit, 
                    STARequiredProcedure, STARequiredSpecialCertification, STASpecialCertification, 
                    SafetyTaskAnalysisHazardAssessment, SafetyTaskAnalysisResponse, SafetyTaskAnalysisTool, 
                    SafetyTaskAnalysisToolInspection)
from .serializers import SafetyTaskAnalysisResponseSerializer
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from jsignature.utils import draw_signature

# VIEWS
# views are the entry point for all code that displays something to the end
# user. There are multiple different paths that can be followed from here but
# the main idea is that some pre or post processing is done to the request and
# then a HTML template is called with the needed data.


# FORM VIEWS ###################################################################
# if the endpoint contains a form, the html form with the needed visual items is
# specified as well as a form from forms.py that contains any other form info as
# well as the model that the form data is stored in.

# entry form for the 100.1 QAQC form
# @login_required
def qaqc100_1(request):
    # process the data if a post request
    if request.method == "POST":
        form = QAQC100_1(request.POST)
        if form.is_valid():
            # save the response if valid
            form.save()
            # after submitting send the user to the list of responses for the
            # form
            # return HttpResponseRedirect("/forms/qaqc/100_1/")
            form = QAQC100_1()
            return render(request, "QAQC/100_1.html", {"form": form})
        else:
            print(form.errors)
    else:
        form = QAQC100_1()
    return render(request, "QAQC/100_1.html", {"form": form})


@login_required
def post_task_assignment(request, response_id):
    if request.method == "POST":
        response_form = STAPostTaskForm(request.POST)
        if response_form.is_valid():
            response_form.save()
            return HttpResponseRedirect(reverse('forms:staresponse-list'))
        else:
            print(response_form.errors)
    else:
        sta_data = get_object_or_404(SafetyTaskAnalysisResponse, id=response_id)
        response_form = STAPostTaskForm(initial={'response': sta_data})  # Auto populate the form with sta_data

        return render(request, "JSA/staposttask.html", {
            "response_form": response_form,
            "sta_data": sta_data
        })


# entry form for the JSA Form
# @login_required
def jsa_entry(request):
    # process the data if a POST request
    STAToolInspectionFormSet                = get_STAToolInspectionFormSet()
    STAHazardMitigationFormSet              = get_STAHazardMitigationFormSet()
    STAEmployeeAcknowledgementFormSet       = get_STAEmployeeAcknowledgementFormSet()
    STARequiredPermitFormSet                = get_STARequiredPermitFormSet()
    STARequiredProcedureFormSet             = get_STARequiredProcedureFormSet()
    STARequiredEmployeeCertificationFormSet = get_STARequiredEmployeeCertificationFormSet()
    STARequiredSpecialCertificationFormSet  = get_STARequiredSpecialCertificationFormSet()
    if request.method == "POST":
        response_form                           = SafetyTaskAnalysisForm(request.POST)
        tool_inspections_formset                = STAToolInspectionFormSet(request.POST)
        hazard_mitigation_formset               = STAHazardMitigationFormSet(request.POST)
        employee_acknowledgement_formset        = STAEmployeeAcknowledgementFormSet(request.POST)
        required_permit_formset                 = STARequiredPermitFormSet(request.POST)
        required_procedure_formset              = STARequiredProcedureFormSet(request.POST)
        required_employee_cert_formset          = STARequiredEmployeeCertificationFormSet(request.POST)
        required_special_cert_formset           = STARequiredSpecialCertificationFormSet(request.POST)
        
        # if all forms are valid save the response and related forms
        if (response_form.is_valid() 
            and tool_inspections_formset.is_valid() 
            and hazard_mitigation_formset.is_valid() 
            and employee_acknowledgement_formset.is_valid()
            and required_permit_formset.is_valid()
            and required_procedure_formset.is_valid()
            and required_employee_cert_formset.is_valid()
            and required_special_cert_formset.is_valid()):
            # set the assessor
            response_form.instance.assessor = request.user
            # save the response
            response = response_form.save()
            tool_inspections = tool_inspections_formset.save(commit=False)
            hazard_mitigations = hazard_mitigation_formset.save(commit=False)
            employee_acknowledgements = employee_acknowledgement_formset.save(commit=False)
            permits = required_permit_formset.save(commit=False)
            procedures = required_procedure_formset.save(commit=False)
            employee_certs = required_employee_cert_formset.save(commit=False)
            special_certs = required_special_cert_formset.save(commit=False)
            
            for tool_inspection in tool_inspections:
                tool_inspection.response = response
                tool_inspection.save()
            for hazard_mitigation in hazard_mitigations:
                hazard_mitigation.response = response
                hazard_mitigation.save()
            for employee_acknowledgement in employee_acknowledgements:
                employee_acknowledgement.response = response
                employee_acknowledgement.save()
            for permit in permits:
                permit.response = response
                permit.save()
            for procedure in procedures:
                procedure.response = response
                procedure.save()
            for employee_cert in employee_certs:
                employee_cert.response = response
                employee_cert.save()
            for special_cert in special_certs:
                special_cert.response = response
                special_cert.save()

            # Create the file
            pdf_buffer = create_jsa_pdf(request, response.id)
            
            # Check if the sta field exists for the job
            job = response.job
            try:
                project_folder, created = ProjectFolders.objects.get_or_create(project=job.project)
                # if the folder id exists just save the pdf to that folder
                if (project_folder.sta != ''):
                    file = upload_file_to_box(pdf_buffer, project_folder.sta, f"{response.job.job_name} - {response.date.strftime('%Y-%m-%d %H%M%S')}.pdf")
                    response.boxID = file.id
                    response.save()
                # if no there are a number of steps to follow
                else:
                    # First: is the project folder ID saved?
                    if job.project.boxID:
                        # Search for the STA folder in the safety folder
                        folders = searchFolder(job.project.boxID, "STAs")
                        if len(folders) > 0:
                            # if a result was returned, make sure it is the STA
                            # folder, save the folder ID, and then upload the file
                            project_folder.sta = folders[0].id
                            project_folder.save()
                            file = upload_file_to_box(pdf_buffer, project_folder.sta, f"{response.job.job_name} - {response.date.strftime('%Y-%m-%d %H%M%S')}.pdf")
                            response.boxID = file.id
                            response.save()
                        else:
                            # Create the folder, save the ID, and upload the file
                            folders = searchFolder(job.project.boxID, "06-Safety")
                            sta_folder = create_folder_in_folder(folders[0].id, "STAs")
                            project_folder.sta = sta_folder.id
                            project_folder.save()
                            file = upload_file_to_box(pdf_buffer, project_folder.sta, f"{response.job.job_name} - {response.date.strftime('%Y-%m-%d %H%M%S')}.pdf")
                            response.boxID = file.id
                            response.save()
                    else:
                        # if no boxId exists, search for the project folder and save the id
                        print("Project does not have a boxId.")
                    print("STA field does not exist for the project.")
            except ProjectFolders.DoesNotExist:
                print("Project folder does not exist for the project.")
            return HttpResponseRedirect("/forms/jsa/")
        else:
            if (response_form.errors): print(response_form.errors)
            if (tool_inspections_formset.errors): print(f'Errors in tool inspection forms: {tool_inspections_formset.errors} {tool_inspections_formset.non_form_errors()}')
            if (hazard_mitigation_formset.errors): print(f'Errors in hazard mitigation forms: {hazard_mitigation_formset.errors} {hazard_mitigation_formset.is_bound}')
            if (employee_acknowledgement_formset.errors): print(f'Errors in employee acknowledgements: {employee_acknowledgement_formset.errors}')
            if (required_permit_formset.errors): print(f'Errors in required permits: {required_permit_formset.errors}')
            if (required_procedure_formset.errors): print(f'Errors in required procedures: {required_procedure_formset.errors}')
            if (required_employee_cert_formset.errors): print(f'Errors in employee certifications: {required_employee_cert_formset.errors}')
            if (required_special_cert_formset.errors): print(f'Errors in special certifications: {required_special_cert_formset.errors}')
    # if not a POST request, create the forms
    else:
        response_form = SafetyTaskAnalysisForm()

        tools = SafetyTaskAnalysisTool.objects.all()
        initial = [{'tool': tool.id} for tool in tools]
        tool_inspections_formset = STAToolInspectionFormSet(initial=initial)

        hazard_mitigation_formset = STAHazardMitigationFormSet()
        employee_acknowledgement_formset = STAEmployeeAcknowledgementFormSet()

        permits = STAPermit.objects.all()
        initial = [{'permit': permit.id} for permit in permits]
        required_permit_formset = STARequiredPermitFormSet(
            initial=initial)

        procedures = STAProcedure.objects.all()
        initial = [{'procedure': procedure.id} for procedure in procedures]
        required_procedure_formset = STARequiredProcedureFormSet(
            initial=initial)

        employee_certs = STAEmployeeCertification.objects.all()
        initial = [{'certification': cert.id} for cert in employee_certs]
        required_employee_cert_formset = STARequiredEmployeeCertificationFormSet(
            initial=initial)

        special_certs = STASpecialCertification.objects.all()
        initial = [{'certification': cert.id} for cert in special_certs]
        required_special_cert_formset = STARequiredSpecialCertificationFormSet(
            initial=initial)

    return render(request, "JSA/SafetyTaskAnalysis.html", {
        "response_form": response_form,
        "tool_inspections_formset": tool_inspections_formset,
        "hazard_mitigation_formset": hazard_mitigation_formset,
        "employee_acknowledgement_formset": employee_acknowledgement_formset,
        "required_permit_formset": required_permit_formset,
        "required_procedure_formset": required_procedure_formset,
        "required_employee_cert_formset": required_employee_cert_formset,
        "required_special_cert_formset": required_special_cert_formset
    })


# INDEX VIEWS ##################################################################
class QAQC100_1IndexView(LoginRequiredMixin, generic.ListView):
    model = Qaqc1001Response
    template_name = "QAQC/100_1_index.html"


class STAResponseList(LoginRequiredMixin, generic.ListView):
    model = SafetyTaskAnalysisResponse
    template_name = 'JSA/staresponse_list.html'
    context_object_name = 'responses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calculate frozen_count and complete_post_task_count
        complete = Count('id', filter=Q(staposttask__isnull=False))
        incomplete = Count('id', filter=Q(staposttask__isnull=True))
        
        # Calculate project response counts
        project_counts = SafetyTaskAnalysisResponse.objects.values('job__job_num', 'job__job_name').annotate(
            complete=complete,
            incomplete=incomplete
            ).order_by('job__job_num')
        
        # Add the counts to the context
        context['projects'] = project_counts
        
        return context


@login_required
def qaqc_forms_index(request):
    return render(request, "QAQC/index.html")


@login_required
def forms_home_page(request):
    return render(request, "FormsHomePage.html")


# SERIALIZER VIEWS #############################################################
class SafetyTaskAnalysisResponseList(APIView):
    def get(self, request):
        responses = SafetyTaskAnalysisResponse.objects.all()
        serializer = SafetyTaskAnalysisResponseSerializer(responses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# PDF VIEWS ####################################################################
# convert JSA response to PDF
def create_jsa_pdf(request, response_id):
    try:
        form_response = SafetyTaskAnalysisResponse.objects.get(id=response_id)
    except SafetyTaskAnalysisResponse.DoesNotExist:
        raise Http404("Response does not exist")

    # create a file-like buffer to receive pdf data.
    buffer = io.BytesIO()
    
    # create the pdf object, using the buffer as its "file"
    p = CustomCanvas(buffer, pagesize=(letter[1], letter[0]))
    width, height = letter[1], letter[0]
    
    # Insert company logo at the top of the document
    logo_path = static('Amteck_Vert_no_tag_Black.png')
    logo_url = request.build_absolute_uri(logo_path)
    if ':' not in request.get_host():
        logo_url = logo_url.replace(request.get_host(), f"{request.get_host()}:8001")
    im = ImageReader(io.BytesIO(requests.get(logo_url).content))
    p.drawImage(im, x=0.692*inch, y=7.1*inch, width=1*inch, height=0.8437*inch, mask='auto')

    # File Title
    p.draw_rect_with_string(1.8*inch, 7.1*inch, 3*inch, .5*inch, 'Safety Task Analysis (STA)', border=False, bold=True)

    # Date box
    x = 5.627*inch
    w = 4.915*inch
    y = 7.5218*inch
    h = .42185*inch
    p.draw_rect_with_string(x, y, w, h, "AM & PM Review", bold=True)
    p.draw_rect_with_string(x+w/2, y+h/2, w/2, h/2, form_response.assessor.full_name, label="By", border=False)
    p.draw_rect_with_string(x, y, w/2, h/2, form_response.date.strftime("%Y-%m-%d"), label="Date", border=False)
    p.draw_rect_with_string(x+w/2, y, w/2, h/2, form_response.date.strftime("%I:%M %p"), label="Time", border=False)

    
    # Draw things on the PDF. Here's where the pdf generation happens.
    p.setFont('Helvetica', 11)

    # Place layout boxes on the document #######################################
    # Page 1 Top Box
    x = 0.692*inch
    y = 5.567*inch
    w = 9.850*inch
    h = 1.433*inch
    line_height = 0.205*inch
    box_gap = 0.05*inch
    text_padding = 0.05*inch
    p.rect(x, y, w, h)
    # sub boxes
    p.draw_rect_with_string(x, y + (6/7)*h, w/2, h/7, form_response.job.job_name, label='Project Name')
    p.draw_rect_with_string(x + w/2, y + (6/7)*h, w/2, h/7, form_response.location_of_work, label='Location of Work')
    p.draw_rect_with_string(x, y + (5/7)*h, w/3, h/7, form_response.job.job_num, label='Project Number')
    p.drawString(x+w/3+text_padding, y+(5/7)*h+text_padding, f'Supervisor Review & Initial    Mid-Morning    Mid-Afternoon')
    p.draw_rect_with_string(x, y + (3/7)*h, w/3, (2/7)*h, "Date")
    p.rect(x + w/3, y + (5/7)*h, (2/3)*w, h/7, 1)
    p.draw_rect_with_string(x, y,               w/3, (3/7)*h, "Lead Superintendent", True, bold=True)
    p.draw_rect_with_string(x, y+line_height,   w/3, (1/7)*h, form_response.lead_superintendent_name, label='Name', border=False)
    p.draw_rect_with_string(x, y,               w/3, (1/7)*h, form_response.lead_superintendent_phone, label='Phone', border=False)
    p.draw_rect_with_string(x+w/3,  y,              w/3, (3/7)*h, "Area Superintendent/Foreman", True, bold=True)
    p.draw_rect_with_string(x+w/3,  y+line_height,  w/3, (1/7)*h, form_response.foreman_name, label='Name', border=False)
    p.draw_rect_with_string(x+w/3,  y,              w/3, (1/7)*h, form_response.foreman_phone, label='Phone', border=False)
    p.draw_rect_with_string(x+2*w/3,    y,              w/3, (3/7)*h, "Site Safety Coordinator/Manager", True, bold=True)
    p.draw_rect_with_string(x+(2/3)*w,  y+line_height,  w/3, (1/7)*h, form_response.manager_name, label='Name', border=False)
    p.draw_rect_with_string(x+(2/3)*w,  y,              w/3, (1/7)*h, form_response.manager_phone, label='Phone', border=False)

    # Page 1 2nd Box
    h = line_height * 2
    y = y - h - box_gap
    p.draw_rect_with_string(x, y + h/2, w, h/2, "CUT 4 LEVEL GLOVES, HARD HAT, & HIGH VISIBILITY ATTIRE IS REQUIRED 100% OR THE TIME WHILE ON SITE", True, bold=True)
    p.draw_rect_with_string(x, y, w, h/2, "THIS IS FOR YOUR SAFETY!!!!!", True, bold=True)

    # Page 1 3rd Box
    h = 7 * line_height
    y = y - h - box_gap
    p.draw_rect_with_string(x, y + (6/7)*h, w, h/7, "Describe (in detail) Work to be Performed", True, bold=True)
    p.draw_rect_with_string(x, y, w, (6/7)*h, form_response.performed_work)

    # Page 1 4th Box
    h = 6 * line_height
    y = y - h - box_gap
    p.draw_rect_with_string(x, y + (5/6)*h, w, h/6, "Tools & Equipment Needed for Task", True, bold=True)
    p.draw_rect_with_string(x, y, w, (5/6)*h, form_response.needed_equipment)

    # Page 1 Bottom Section
    h = line_height * 8
    y = y - h - box_gap
    p.draw_rect_with_string(x, y, w, h, "Lift Equipment for Task", True, bold=True)
    p.drawCentredString(x + w/2, y+(6/8)*h+text_padding, "Ladders are to be the last resort to using an Aerial Lift")
    p.draw_rect_with_string(x, y+(5/8)*h, w/4, h/8, form_response.ladder_work_elevation, label='Estimated Work Elevation')
    p.draw_rect_with_string(x + w/4, y+(5/8)*h, w/2, h/8, "If using Aerial Lift go to Lift Equipment Section Below", True, bold=True)
    p.draw_rect_with_string(x + (3/4)*w, y+(5/8)*h, w/4, h/8, "If using a ladder fill out below", True, bold=True)
    p.draw_rect_with_string(x, y+(3/8)*h, w, (2/8)*h, form_response.ladder_reason_for_use, label='Explain why you have to use a ladder')
    p.draw_rect_with_string(x, y+(2/8)*h, w/2, (1/8)*h, form_response.ladder_type, label='Ladder Type')
    p.draw_rect_with_string(x+w/2, y+(2/8)*h, w/2, (1/8)*h, form_response.ladder_height, label='Ladder Height')
    p.draw_rect_with_string(x, y, w/2, (2/8)*h, form_response.ladder_approve_printed_name, label='Reviewed and Approved by')
    p.draw_rect_with_string(x+w/2, y, w/2, (2/8)*h, "Signature:", bold=True)
    if form_response.ladder_approve_signature != None:
        signature_image = Image.open(draw_signature(
            form_response.ladder_approve_signature, as_file=True))
        bg = Image.new("RGB", signature_image.size, (255, 255, 255))
        bg.paste(signature_image, signature_image)
        p.drawInlineImage(bg, x+w/2+1*inch, y+text_padding, width=w/6, height=(1/4)*h-2*text_padding)
    # Finish Page 1
    p.showPage()

    # set up page 2
    p.setFont('Helvetica', 11)
    
    # Page 2 Top Section
    x = 0.692*inch
    h = 6 * line_height
    y = height - h - 0.5*inch
    w = 9.850*inch
    line_height = 0.205*inch
    box_gap = 0.05*inch
    text_padding = 0.05*inch
    p.draw_rect_with_string(x, y, w, h, "Lift Equipment for Task", centered=True, bold=True)
    p.draw_rect_with_string(x, y+(4/6)*h, w, h/6, form_response.get_lift_display(), label='Lift Type and Size')
    p.draw_rect_with_string(x, y+(3/6)*h, w, h/6, "Ground Assessment: This must be completed prior to operation of lift.", bold=True)
    p.draw_rect_with_string(x, y+(2/6)*h, w/2, h/6, form_response.safe_travel, label='Has a safe path of travel & working are been reviewed?')
    p.draw_rect_with_string(x+w/2, y+(2/6)*h, w/2, h/6, form_response.soils, label='Are soft or unstable soils present?')
    p.draw_rect_with_string(x, y+(1/6)*h, w/2, h/6, form_response.spotter_required, label='Is a Spotter required when moving lift?')
    p.draw_rect_with_string(x+w/2, y+(1/6)*h, w/4, h/6, form_response.spotter_name, label='Name of Spotter')
    p.draw_rect_with_string(x+(3/4)*w, y+(1/6)*h, w/4, h/6, form_response.spotter_qualified, label='Spotter is Qualified')
    p.draw_rect_with_string(x, y, w/2, h/6, form_response.inspection_performed, label='Equipment Inspection has been performed and documented?')
    p.draw_rect_with_string(x+w/2, y, w/2, h/6, form_response.inspection_form_accessible, label='Equipment Inspection form is readily accessible?')

    # Page 2 2nd Section
    lines = 9
    permits = STARequiredPermit.objects.filter(response=form_response)
    h = lines * line_height
    y = y - h - 0.2 * inch
    p.draw_rect_with_string(x, y + (8/lines)*h, w/4, h/lines, "Permits Required", True, bold=True)
    p.draw_rect_with_string(x + w/4, y + (8/lines)*h, w/4, h/lines, "Comments", True, bold=True)
    # Iterate over permits
    for i, permit in enumerate(permits[:8], start=1):
        permit_name = permit.permit.name
        required = "X" if permit.required else ""
        comments = permit.comments

        box_y_pos = y + (lines - 1 - i)/lines * h

        p.draw_rect_with_string(x,              box_y_pos, w/4,     h/lines, permit_name)
        p.draw_rect_with_string(x + (3/16)*w,   box_y_pos, w/16,    h/lines, required)
        p.draw_rect_with_string(x + w/4,        box_y_pos, w/4,     h/lines, comments)

    procedures = STARequiredProcedure.objects.filter(response=form_response)
    p.draw_rect_with_string(x + (2/4)*w, y + (8/lines)*h, w/4, h/lines, "Procedures Required", True, bold=True)
    p.draw_rect_with_string(x + (3/4)*w, y + (8/lines)*h, w/4, h/lines, "Comments", True, bold=True)
    # Iterate over procedures
    for i, procedure in enumerate(procedures[:8], start=1):
        name = procedure.procedure.name
        required = procedure.required
        comments = procedure.comments

        box_y_pos = y + (lines - 1 -i)/lines * h

        p.draw_rect_with_string(x + (2/4)*w,    box_y_pos, w/4, h/lines, name)
        p.draw_rect_with_string(x + (11/16)*w,  box_y_pos, w/32, h/lines, required)
        p.draw_rect_with_string(x + (3/4)*w,    box_y_pos, w/4, h/9, comments)

    # Pull certificates related to this response
    lines = 6
    certificates = STARequiredEmployeeCertification.objects.filter(response=form_response)
    h = 6 * line_height
    y = y - h - 0.2*inch
    # print headers
    p.draw_rect_with_string(x, y + (5/6)*h, (2/3)*w, h/6, "Required Employee Certifications", True, bold=True)
    # Iterate over certificates
    for i, certificate in enumerate(certificates, start=1):
        box_x_offset = 0
        if i > lines-1:
            box_x_offset = (2/6)*w
            box_y_pos = y + (lines - 1 - i + lines - 1)/lines * h
        else: 
            box_x_offset = 0
            box_y_pos = y + (lines - 1 - i)/lines * h
        certificate_name = certificate.certification.name
        required = "X" if certificate.required else ""
        comments = certificate.comments
        # print the values
        p.draw_rect_with_string(x + box_x_offset,           box_y_pos, (1/6)*w, h/6, certificate_name)
        p.draw_rect_with_string(x + box_x_offset + (1/6)*w, box_y_pos, (1/6)*w, h/6, required, True)

    # pull special certificates related to this response
    spec_certs = STARequiredSpecialCertification.objects.filter(response=form_response)
    lines = 6
    # print headers
    p.draw_rect_with_string(x + (2/3)*w, y + (5/6)*h, w/3, h/6, "Special Certifications", True, bold=True)
    # iterate over certs
    for i, cert in enumerate(spec_certs, start=1):
        # set the line height
        box_y_pos = y + (lines-1-i)/lines * h
        # pull values
        cert_name = cert.certification.name
        required = cert.required
        comments = cert.comments
        # print the values
        p.draw_rect_with_string(x + (4/6)*w, box_y_pos, w/6, h/6, cert_name)
        p.draw_rect_with_string(x + (5/6)*w, box_y_pos, w/6, h/6, required, True)


    # Fetch the related tool inspections
    tool_inspections = SafetyTaskAnalysisToolInspection.objects.filter(response=form_response)

    # Page 2 Bottom Section
    h = 13 * line_height
    y = y - h - 0.2*inch
    p.rect(x, y, w, h)
    p.draw_rect_with_string(x, y + (12/13)*h, (3/14)*w, h/13, "Tools Required", True, bold=True)
    p.draw_rect_with_string(x + (3/14)*w, y + (12/13)*h, (1/14)*w, h/13, "Using", True, bold=True)
    p.draw_rect_with_string(x + (4/14)*w, y + (12/13)*h, (1/14)*w, h/13, "Inspected", True, bold=True)
    p.draw_rect_with_string(x + (5/14)*w, y + (12/13)*h, (3/14)*w, h/13, "Trained", True, bold=True)

    # Iterate over tool inspections
    for i, tool_inspection in enumerate(tool_inspections[:12], start=1):
        tool_name = tool_inspection.tool.name
        using = "X" if tool_inspection.inspection else ""
        inspected = "X" if tool_inspection.inspection else ""
        trained = "X" if tool_inspection.training_received else ""

        box_y_pos = y + (12/13 - i/13) * h

        p.draw_rect_with_string(x, box_y_pos, (3/14)*w, h/13, tool_name)
        p.draw_rect_with_string(x + (3/14)*w, box_y_pos, (1/14)*w, h/13, using, True)
        p.draw_rect_with_string(x + (4/14)*w, box_y_pos, (1/14)*w, h/13, inspected, True)
        p.draw_rect_with_string(x + (5/14)*w, box_y_pos, (3/14)*w, h/13, trained, True)

    # If there are more than 12 tool inspections, print the remaining in a new section
    if len(tool_inspections) > 12:
        p.draw_rect_with_string(x + (8/14)*w, y + (12/13)*h, (3/14)*w, h/13, "Additional Tools", True, bold=True)
        p.draw_rect_with_string(x + (11/14)*w, y + (12/13)*h, (1/14)*w, h/13, "Using", True, bold=True)
        p.draw_rect_with_string(x + (12/14)*w, y + (12/13)*h, (1/14)*w, h/13, "Inspected", True, bold=True)
        p.draw_rect_with_string(x + (13/14)*w, y + (12/13)*h, (1/14)*w, h/13, "Trained", True, bold=True)

        for i, tool_inspection in enumerate(tool_inspections[12:], start=1):
            tool_name = tool_inspection.tool.name
            using = "X" if tool_inspection.inspection else ""
            inspected = "X" if tool_inspection.inspection else ""
            trained = "X" if tool_inspection.training_received else ""

            box_y_pos = y + (12/13 - i/13) * h

            p.draw_rect_with_string(x + (8/14)*w, box_y_pos, (3/14)*w, h/13, tool_name)
            p.draw_rect_with_string(x + (11/14)*w, box_y_pos, (1/14)*w, h/13, using, True)
            p.draw_rect_with_string(x + (12/14)*w, box_y_pos, (1/14)*w, h/13, inspected, True)
            p.draw_rect_with_string(x + (13/14)*w, box_y_pos, (1/14)*w, h/13, trained, True)

    # finish page 2
    p.showPage()

    # Page 3 ###################################################################

    # Fetch the related hazard assessments
    hazard_assessments = SafetyTaskAnalysisHazardAssessment.objects.filter(response=form_response)
    # Page 3 Top Section
    lines = len(hazard_assessments) + 1
    h = lines * line_height
    y = height - h - 0.5*inch
    p.rect(x, y, w, h)
    p.draw_rect_with_string(x, y + ((lines-1)/lines)*h, (3/14)*w, h/lines, "Hazard", True, bold=True)
    p.draw_rect_with_string(x + (3/14)*w, y + ((lines-1)/lines)*h, (11/14)*w, h/lines, "Comments", True, bold=True)
    # Iterate over hazard assessments
    for i, hazard_assessment in enumerate(hazard_assessments, start=1):
        hazard_name = hazard_assessment.hazard.name
        comments = hazard_assessment.comment

        box_y_pos = y + ((lines - 1 - i)/lines) * h

        p.draw_rect_with_string(x, box_y_pos, (3/14)*w, h/lines, hazard_name)
        p.draw_rect_with_string(x + (3/14)*w, box_y_pos, (11/14)*w, h/lines, comments)

    # Fetch required ppe
    required_ppe = form_response.ppe.all()
    # adjust position
    columns = 4
    lines = math.ceil(len(required_ppe) / columns) + 1                          # add 1 for header row
    h = lines * line_height
    y = y - h - 0.25*inch                                                       # position under last box by one row
    p.rect(x, y, w, h)
    # print header
    p.draw_rect_with_string(x, y + ((lines-1)/lines)*h, w, h/lines, "PPE Required", True, bold=True)
    # loop over all items
    for i, ppe in enumerate(required_ppe, start=1):
        col = (i - 1) % columns
        row = (i - 1) // columns
        box_x_pos = x + col * (w / columns)
        box_y_pos = y + ((lines - 2 - row) / lines) * h
        p.draw_rect_with_string(box_x_pos, box_y_pos, w / columns, h / lines, ppe.name, border=False)

    # Fetch employee acknowledgements
    employee_acknowledgements = STAEmployeeAcknowledgement.objects.filter(response=form_response)
    # set up dimensions
    lines = len(employee_acknowledgements) + 1
    line_height = line_height * 2  # double the line height to fit signatures better
    h = lines * line_height
    y = y - h - 0.25*inch  # position under last box by one row
    # print header
    p.draw_rect_with_string(x, y + ((lines-1)/lines) * h, w, h/lines, "Employee Acknowledgement", True, bold=True)
    # loop over acknowledgements
    for i, acknowledgement in enumerate(employee_acknowledgements, start=1):
        box_y_pos = y + ((lines - 1 - i)/lines) * h
        p.draw_rect_with_string(x, box_y_pos, w/4, h/lines, str(acknowledgement.employee), border=False)

        signature_image = Image.open(draw_signature(
            acknowledgement.shift_start_signature, as_file=True))
        bg = Image.new("RGB", signature_image.size, (255, 255, 255))
        bg.paste(signature_image, signature_image)
        aspect_ratio = signature_image.width / signature_image.height
        p.drawInlineImage(bg, x + w/4, box_y_pos, width=h/lines * aspect_ratio, height=h/lines)

        signature_image = Image.open(draw_signature(
            acknowledgement.shift_end_signature, as_file=True))
        bg = Image.new("RGB", signature_image.size, (255, 255, 255))
        bg.paste(signature_image, signature_image)
        aspect_ratio = signature_image.width / signature_image.height
        p.drawInlineImage(bg, x + w/2, box_y_pos, width=h/lines * aspect_ratio, height=h/lines)

        p.draw_rect_with_string(x + 3*w/4, box_y_pos, w/4, h/lines, acknowledgement.comments, border=False)
    # draw boxes and headers, doing them at the end so they have a higher z than the signatures
    p.rect(x, y, w, h)
    p.draw_rect_with_string(x, y + ((lines-1)/lines) * h, w/4, h/lines/2, "Employee Name", True, bold=True)
    p.draw_rect_with_string(x + (1/4)*w, y + ((lines-1)/lines) * h, w/4, h/lines/2, "Shift Start", True, bold=True)
    p.draw_rect_with_string(x + (2/4)*w, y + ((lines-1)/lines) * h, w/4, h/lines/2, "Shift End", True, bold=True)
    p.draw_rect_with_string(x + (3/4)*w, y + ((lines-1)/lines) * h, w/4, h/lines/2, "Comments", True, bold=True)

    # close the pdf cleanly
    p.showPage()

    # close the pdf cleanly
    p.save()

    buffer.seek(0)
    return buffer


# this renders the responses onto a pdf and downloads it
def create_qaqc_100_1_pdf(request, response_id):
    try:
        form_response = Qaqc1001Response.objects.get(id=response_id)
    except Qaqc1001Response.DoesNotExist:
        raise Http404("Response does not exist")

    # Pull in form to use lables
    form = QAQC100_1()
    labels_dict = {}
    for field_name, field in form.fields.items():
        if field.label:
            labels_dict[field_name] = str(field.label)

    # create a file-like buffer to receive pdf data.
    buffer = io.BytesIO()

    # create the pdf object, using the buffer as its "file"
    p = canvas.Canvas(buffer, letter)
    width, height = letter

    # Draw things on the PDF. Here's where the pdf generation happens.
    p.setFont('Helvetica', 11)

    # set fill to blue for header box
    p.setFillColorCMYK(.57, .27, 0, .17)
    p.rect(0.50*inch, 10.25*inch, 7.5*inch, .25*inch, stroke=0, fill=1)
    # set fill white for header box text
    p.setFillColorRGB(1,1,1)
    p.drawCentredString(width/2, 10.3304*inch, 'ABOVE GROUND CONDUIT INSPECTION SHEET')

    # set fill black for main text
    p.setFillColorRGB(0,0,0)

    # Project Box and Text
    p.rect(.5*inch, 9.7*inch, 3.75*inch, .4457*inch, stroke=1, fill=0)
    p.drawString( .575*inch, 9.94*inch, f'PROJECT: {form_response.project.job_name}')
    # Area Box and Text
    p.rect(4.25*inch, 9.7*inch, 1.875*inch, .4457*inch, stroke=1, fill=0)
    p.drawString(4.325*inch, 9.94*inch, f'AREA: {form_response.area}')
    # Sheet No Box and Text
    p.rect(6.125*inch, 9.7*inch, 1.875*inch, .4457*inch, stroke=1, fill=0)
    p.drawString(6.2*inch, 9.94*inch, f'SHEET NO: {form_response.sheet_no}')
    # Drawing Box and Text
    p.rect(.5*inch, 9*inch, 3.75*inch, .7*inch, stroke=1, fill=0)
    p.drawString(.575*inch, 9.495*inch, f'DRAWING: {form_response.drawing}')
    # Conduit Run Box and Text
    p.rect(4.25*inch, 9*inch, 3.75*inch, .7*inch, stroke=1, fill=0)
    p.drawString(4.325*inch, 9.495*inch, f'CONDUIT RUN:')
    p.drawString(4.325*inch, 9.29*inch, f'FROM: {form_response.conduit_run_from}')
    p.drawString(4.325*inch, 9.085*inch, f'TO: {form_response.conduit_run_to}')

    # Headers of Checklist Table
    p.setFillColorCMYK(0.10, 0.04, 0.0, 0.04)
    p.rect(0.5*inch, 8.46*inch, 0.5*inch, 0.54*inch, stroke=1, fill=1)
    p.rect(1*inch, 8.46*inch, 5*inch, 0.54*inch, stroke=1, fill=1)
    p.rect(6*inch, 8.46*inch, 1*inch, 0.54*inch, stroke=1, fill=1)
    p.rect(7*inch, 8.46*inch, 1*inch, 0.54*inch, stroke=1, fill=1)
    p.setFillColorRGB(0,0,0)
    p.drawString(   0.575*inch, 8.59*inch, 'Item')
    p.drawString(   1.075*inch, 8.59*inch, 'Description')
    p.drawString(   6.075*inch, 8.795*inch, 'Corrections')
    p.drawString(   6.075*inch, 8.59*inch, 'Needed')
    p.drawString(   7.075*inch, 8.795*inch, 'Corrections')
    p.drawString(   7.075*inch, 8.59*inch, 'Completed')

    # Iterate through the checkboxes
    for i, field in enumerate(
            ["conforms_to_NEC", "installed_per_drawing", "supports_anchored", 
                "conduit_leveled", "material_classification", "pull_points", 
                "expansion_joints", "low_point_drains", "unions", "seals",
                "couplings_tight", "excessive_threads", "bushings",
                "bonding_jumpers", "field_changes_on_drawing"],start=1):
        question_name = labels_dict[field]
        # Draw the label
        box_y_pos = 8.46*inch - i*.32*inch
        text_y_pos = box_y_pos + .1*inch

        p.rect( .5*inch,    box_y_pos, .5*inch, .32*inch, stroke=1, fill=0)
        p.drawString( .6*inch,      text_y_pos, f'{i}.')

        p.rect( 1*inch,     box_y_pos, 5*inch,  .32*inch, stroke=1, fill=0)
        p.drawString(1.075*inch,    text_y_pos , question_name)

        # Draw correction checkboxes for each group
        checkbox_names = [f"{field}_corrections_needed",
                f"{field}_corrections_completed"]
        for j, checkbox_name in enumerate(checkbox_names, start=1):
            checkbox_value = getattr(form_response, checkbox_name)

            box_x_pos = 5*inch + j*1*inch
            check_box_x_pos = box_x_pos + .4*inch
            check_box_y_pos = box_y_pos + .06*inch

            p.rect(box_x_pos, box_y_pos, 1*inch, .32*inch, stroke=1, fill=0)
            p.rect(check_box_x_pos, check_box_y_pos, .2*inch, .2*inch, fill=0)

            if checkbox_value:
                p.drawString(check_box_x_pos+ .05*inch, check_box_y_pos+.05*inch, 'X')



    # add the signature
    #signature_image = Image.open(draw_signature(
    #    form_response.test_signature, as_file=True))
    #bg = Image.new("RGB", signature_image.size, (255, 255, 255))
    #bg.paste(signature_image, signature_image)
    #p.drawInlineImage(bg, 100, 600, width=200, height=100)

    # close the pdf cleanly
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="hello.pdf")


# Custom Canvas Class ##########################################################
# Add a new method to the Canvas class for drawing a rectangle with a string inside
class CustomCanvas(canvas.Canvas):
    def draw_rect_with_string(self, x, y, w, h, text, centered=False, label=None, border=True, bold=False):
        if border:
            self.rect(x, y, w, h, 1)

        if bold:
            self.setFont('Helvetica-Bold', 11)
        else:
            self.setFont('Helvetica', 11)

        # convert booleans
        if type(text) == bool:
            text = "X" if text else ""
            
        if centered:
            self.drawCentredString(x + w/2, y+h-0.15*inch, text)
        else:
            if label:
                padding = self.draw_rect_with_string(x, y, w, h, label + ": ", border=False, bold=True)
                self.setFont('Helvetica', 11)
                self.drawString(x + padding + 0.05*inch, y+h-0.15*inch, str(text))
            else:
                self.drawString(x + 0.05*inch, y+h-0.15*inch, text)

        return stringWidth(str(text), 'Helvetica-Bold', 11)


@login_required
def view_jsa_pdf(request, jsa_box_id):
    try:
        embed_url = get_file_embed(jsa_box_id)
        return render(request, "JSA/file_embed.html", {"embed_url": embed_url})
    except Exception as e:
        print(f"Error: {e}")
        raise Http404("File not found")

# @login_required
def amq100_1(request):
    # process the data if a post request
    if request.method == "POST":
        form = AMQ100_1(request.POST)
        if form.is_valid():
            # save the response if valid
            form.save()
  
            form = AMQ100_1()
            # return render(request, "AMQ/100_1.html", {"form": form})
            return redirect('forms:confirmation-page')
        else:
            print(form.errors)
    else:
        form = AMQ100_1()
    return render(request, "AMQ/100_1.html", {"form": form})

# @login_required
def amq100_2(request):
    # process the data if a post request
    if request.method == "POST":
        form = AMQ100_2(request.POST)
        if form.is_valid():
            # save the response if valid
            form.save()
         
            form = AMQ100_2()
            # return render(request, "AMQ/100_2.html", {"form": form})
            return redirect('forms:confirmation-page')
        else:
            print(form.errors)
    else:
        form = AMQ100_2()
    return render(request, "AMQ/100_2.html", {"form": form})

# @login_required
def amq100_3(request):
    # process the data if a post request
    if request.method == "POST":
        form = AMQ100_3(request.POST)
        if form.is_valid():
            # save the response if valid
            form.save()
           
            form = AMQ100_3()
            # return render(request, "AMQ/100_3.html", {"form": form})
            return redirect('forms:confirmation-page')
        else:
            print(form.errors)
    else:
        form = AMQ100_3()
    return render(request, "AMQ/100_3.html", {"form": form})

# @login_required
def amq130_1(request):
    # process the data if a post request
    if request.method == "POST":
        form = AMQ130_1(request.POST)
        if form.is_valid():
            # save the response if valid
            form.save()
           
            form = AMQ130_1()
            # return render(request, "AMQ/130_1.html", {"form": form})
            return redirect('forms:confirmation-page')
        else:
            print(form.errors)
    else:
        form = AMQ130_1()
    return render(request, "AMQ/130_1.html", {"form": form})

# @login_required
def amq140_1(request):
    # process the data if a post request
    if request.method == "POST":
        form = AMQ140_1(request.POST)
        if form.is_valid():
            # save the response if valid
            form.save()
           
            form = AMQ140_1()
            # return render(request, "AMQ/140_1.html", {"form": form})
            return redirect('forms:confirmation-page')
        else:
            print(form.errors)
    else:
        form = AMQ140_1()
    return render(request, "AMQ/140_1.html", {"form": form})

# @login_required
def amq200_1(request):
    # process the data if a post request
    if request.method == "POST":
        form = AMQ200_1(request.POST)
        if form.is_valid():
            # save the response if valid
            form.save()
            
            form = AMQ200_1()
            # return render(request, "AMQ/200_1.html", {"form": form})
            return redirect('forms:confirmation-page')
        else:
            print(form.errors)
    else:
        form = AMQ200_1()
    return render(request, "AMQ/200_1.html", {"form": form})

# @login_required
def amq160_1(request):
    # process the data if a post request
    if request.method == "POST":
        form = AMQ160_1(request.POST)
        if form.is_valid():
            # save the response if valid
            form.save()
            
            form = AMQ160_1()
            # return render(request, "AMQ/160_1.html", {"form": form})
            return redirect('forms:confirmation-page')
        else:
            print(form.errors)
    else:
        form = AMQ160_1()
    return render(request, "AMQ/160_1.html", {"form": form})

# @login_required
def amq160_2(request):
    # process the data if a post request
    if request.method == "POST":
        form = AMQ160_2(request.POST)
        if form.is_valid():
            # save the response if valid
            form.save()
            
            form = AMQ160_2()
            # return render(request, "AMQ/160_2.html", {"form": form})
            return redirect('forms:confirmation-page')
        else:
            print(form.errors)
    else:
        form = AMQ160_2()
    return render(request, "AMQ/160_2.html", {"form": form})

# @login_required
def amq150_2(request):
    # process the data if a post request
    if request.method == "POST":
        form = AMQ150_2(request.POST)
        if form.is_valid():
            # save the response if valid
            form.save()
            
            form = AMQ150_2()
            # return render(request, "AMQ/150_2.html", {"form": form})
            return redirect('forms:confirmation-page')
        else:
            print(form.errors)
    else:
        form = AMQ150_2()
    return render(request, "AMQ/150_2.html", {"form": form})

# @login_required
def amq150_1(request):
    # process the data if a post request
    if request.method == "POST":
        form = AMQ150_1(request.POST)
        if form.is_valid():
            # save the response if valid
            form.save()
            
            form = AMQ150_1()
            # return render(request, "AMQ/150_1.html", {"form": form})
            return redirect('forms:confirmation-page')
        else:
            print(form.errors)
    else:
        form = AMQ150_1()
    return render(request, "AMQ/150_1.html", {"form": form})

def confirmation_page(request):
    return render(request, "ConfirmationPage/confirmation_page.html")