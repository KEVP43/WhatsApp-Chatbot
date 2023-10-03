import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from insurancebot import views

# Define the scopes and credentials file
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
CREDS_FILE = 'client_secret.json'
FOLDER_ID = '1iwqzHiqHvzDUYzaMQBrOQXWQ0SX2DflR'


def authenticate_and_get_service():
    # Load credentials from file
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials, let the user log in
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)

    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    # Build the Drive API service
    service = build('drive', 'v3', credentials=creds)
    return service

def list_files_in_folder(service, folder_id):
    results = service.files().list(
        pageSize=10,
        fields="nextPageToken, files(id, name)",
        q=f"'{folder_id}' in parents").execute()
    items = results.get('files', [])

    if not items:
        print(f'No files found in folder with ID {folder_id}.')
    else:
        print(f'Files in folder with ID {folder_id}:')
        for item in items:
            print(f"{item['name']} ({item['id']})")

def download_file_by_name(service, folder_id, file_name, destination_folder):
    global response
    response = "You are successfully entered to Gdrive Folders."
    results = service.files().list(
        pageSize=10,
        fields="nextPageToken, files(id, name)",
        q=f"'{folder_id}' in parents and name = '{file_name}'").execute()
    items = results.get('files', [])

    if not items:
        print(f'File "{file_name}" not found in folder with ID {folder_id}.')
    else:
        file_id = items[0]['id']
        file_path = os.path.join(destination_folder, file_name)

        request = service.files().get_media(fileId=file_id)
        fh = open(file_path, 'wb')
        downloader = request.execute()

        with open(file_path, 'wb') as f:
            f.write(downloader)

        print(f'Downloaded: {file_name}')

if __name__ == '__main__':
    service = authenticate_and_get_service()
    
    # Replace 'destination_folder' with the path where you want to save the downloaded files.
    destination_folder = 'D:\Django\insurance\documents'
    
    response = list_files_in_folder(service, FOLDER_ID)
    # Prompt the user for the filename they want to download
    file_to_download = views.insurancebot.message
    
    download_file_by_name(service, FOLDER_ID, file_to_download, destination_folder)
