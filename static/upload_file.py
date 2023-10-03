import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Define the scopes and credentials file
SCOPES = ['https://www.googleapis.com/auth/drive.file']  # Modify as needed
CREDS_FILE = 'client_secret.json'
UPLOAD_FOLDER = 'https://drive.google.com/drive/folders/1tDrwBQyWFP-WekWUTgu0GusbXDUnbKiX?usp=sharing'  # Folder containing files to upload

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

def upload_files(service, folder_id):
    for root, _, files in os.walk(UPLOAD_FOLDER):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file_path)[-1].lower()
            
            # Check if the file extension is allowed
            if file_extension in ['.jpg', '.jpeg', '.pdf']:
                file_metadata = {
                    'name': file,
                    'parents': [folder_id]
                }
                media = MediaFileUpload(file_path, resumable=True)
                
                try:
                    uploaded_file = service.files().create(
                        body=file_metadata,
                        media_body=media,
                        fields='id'
                    ).execute()
                    
                    print(f'Successfully uploaded: {file}')
                except Exception as e:
                    print(f'Error uploading {file}: {e}')

if __name__ == '__main__':
    service = authenticate_and_get_service()
    
    # Replace 'folder_id' with the ID of the destination folder in Google Drive.
    folder_id = '1tDrwBQyWFP-WekWUTgu0GusbXDUnbKiX'
    
    upload_files(service, folder_id)
