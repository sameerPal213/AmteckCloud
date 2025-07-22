from .tasks import boxAuth

# Function to search for a folder on Box
def searchFolder(folderID, searchTerm):
    # Create as-user client
    boxClient = boxAuth('./box/config.json', '755000110')
    # Search for the folder
    items = boxClient.search().query(query=searchTerm, ancestor_folder_ids=[folderID], type='folder')
    # Return the search results
    return [item for item in items]


def upload_file_to_box(file_content_stream, folder_id, file_name):
    # Create as-user client
    boxClient = boxAuth('./box/config.json', '755000110')
    # Set the file attributes
    new_file = boxClient.folder(folder_id).upload_stream(file_content_stream, file_name)
    return new_file


def create_folder_in_folder(folder_id, folder_name):
    # Create as-user client
    boxClient = boxAuth('./box/config.json', '755000110')
    # Create the folder
    new_folder = boxClient.folder(folder_id).create_subfolder(folder_name)
    return new_folder


def get_file_embed(file_id):
    # Create as-user client
    boxClient = boxAuth('./box/config.json', '755000110')
    embed_url = boxClient.file(file_id).get_embed_url()
    return embed_url
