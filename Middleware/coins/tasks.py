from am_nexus.celery import app
from coins.models import Project, ProjectsDirectory
from box.tasks import addProject, updateProject
import logging
import json

@app.task(bind=True)
def delayPrint(self, inStr):
    print(inStr)

logger = logging.getLogger(__name__)

# Configure logging to output to the console
logging.basicConfig(level=logging.DEBUG)

# This function creates or updates the Project model and calls the corresponding Box function
@app.task(bind=True)
def projectHandler(self, projReq):
    # Save the action and body of the project request
    projReqAction = projReq["COINSInterface"]["Header"]["_attributes"]["action"]
    projReqBody = projReq["COINSInterface"]["Body"]["pi_projectRow"]
    
    logger.info(f"Received project request with action: {projReqAction}")
    
    # Creates the project model and calls the Box project creation function
    if projReqAction == "CREATE":
        # Create Project model
        inRec, created = Project.objects.get_or_create(
            pij_num         = projReqBody["pij_num"],
            pij_archived    = False if projReqBody["pij_archived"] == 'no' else True,
            pij_name        = projReqBody["pij_name"],
            pij_dispno      = projReqBody["pij_dispno"],
            mkg_code        = projReqBody["mkg_code"],
            pty_type        = projReqBody["pty_type"],
            pst_type        = projReqBody["pst_type"],
        )
        # Save Project model
        inRec.save()

        # Hand off to Box projectCreate task
        logger.debug(json.dumps(inRec.pij_num, indent=4))
        addProject.apply_async(args=[inRec.pij_num])

    elif projReqAction == "UPDATE":
        # Query and update DB record
        upRec, created = Project.objects.get_or_create(pij_num=projReqBody["pij_num"])
        upRec.pty_type = projReqBody["pty_type"]
        upRec.pst_type = projReqBody["pst_type"]

        # Save project model
        upRec.save()

        # Hand off to Box projectUpdate task
        logger.debug(json.dumps(upRec.pij_num, indent=4))
        updateProject.apply_async(args=[upRec.pij_num])

    logger.info("Project handling completed.")
