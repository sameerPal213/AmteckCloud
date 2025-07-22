from boxsdk import JWTAuth, Client
from am_nexus.celery import app
from coins.models import Project, ProjectsDirectory
import json

# Utility function to create projects directory superstructure in DB
@app.task(bind=True)
def _util_createDirStruct(self):
    with open('./box/directory_structure.json') as f:
        inJSON = json.load(f)
        for doc in inJSON:
            inDir = ProjectsDirectory(**doc)
            inDir.save()

# Function to create as-user client
@app.task(bind=True)
def boxAuth(self, jwtPath, usrID):
    auth = JWTAuth.from_settings_file(jwtPath)
    client = Client(auth)
    usr = client.user(user_id=usrID)
    return client.as_user(usr)

# Function that copies template folder to appropriate dept, status, and stage; gives copied folder proper name
@app.task(bind=True)
def addProject(self, projID):
    #Template folder ID
    TEMPLATE_ID = '111793970945'
    #Query DB for project
    proj = Project.objects.get(pij_num=projID)
    destID = ProjectsDirectory.objects.get(dept=proj.mkg_code, status=proj.pty_type, stage=proj.pst_type).boxID
    #Format copy request
    projName = proj.pij_name+"-"+proj.pij_dispno
    projName = projName.strip()
    projName = projName.translate({ord(i): None for i in '<>:"?*.'})
    projName = projName.translate({ord(i): ord('_') for i in '/\\|'})
    #Create as-user client
    boxClient = boxAuth('./box/config.json', '755000110')
    #Create Folder objects
    srcFolder = boxClient.folder(TEMPLATE_ID)
    destFolder = boxClient.folder(destID)
    #Copy template to proper location and get box ID from response
    projBoxID = srcFolder.copy(parent_folder=destFolder, name=projName).id
    #Save Box ID to DB
    proj.boxID = projBoxID
    proj.save()

# Function that moves folder from current location to proper department, status, and stage
@app.task(bind=True)
def updateProject(self, projID):
    #Query DB for project
    proj = Project.objects.get(pij_num=projID)
    destID = ProjectsDirectory.objects.get(dept=proj.mkg_code, status=proj.pty_type, stage=proj.pst_type).boxID
    # Create as-user client
    boxClient = boxAuth('./box/config.json', '755000110')
    # Create Folder objects
    srcFolder = boxClient.folder(proj.boxID)
    destFolder = boxClient.folder(destID)
    #Move folder to proper location
    srcFolder.move(destFolder)


