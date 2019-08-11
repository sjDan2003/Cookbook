import pickle
import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from .LocalFileService import LocalFileServiceClass


class GoogleDriveClass(LocalFileServiceClass):

    """This class manages uploading, downloading, updating and managing
    files on a user's Google Drive account that are used by the program.

    On the first run, the user's default web browser will open to grant the
    application permission to read and write data that this program creates.
    This class will not modify data other data that was not created by this
    program.

    Attributes:
        SCOPES: A list with a single element indicating the permissions this
                class requires.
        mime_types: Dictionary to match filetypes with its MIME type
        drive_service: The Google Drive object that will access the user's
                       account.
    """

    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    # MIME stands for Multipurpose Internet Mail Extensions, and is also
    # sometimes referred to as Media Type.
    # It's a standard that indicates the nature of a file.
    mime_types = {'HTML': 'text/html', 'zip': 'application/zip', 'plainText': 'text/plain',
                  'richText': 'application/rtf', 'epub': 'application/epub+zip',
                  'openOfficeDoc': 'application/vnd.oasis.opendocument.text',
                  'pdf': 'application/pdf', 'csv': 'text/csv', 'png': 'image/png',
                  'msWord': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                  'msExcel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                  'openOfficeSheet': 'application/x-vnd.oasis.opendocument.spreadsheet',
                  'tsv': 'text/tab-separated-values', 'htmlZip': 'application/zip',
                  'svg': 'image/svg+xml', 'jpeg': 'image/jpeg',
                  'msPowerPoint': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                  'openOfficePresentation': 'application/vnd.oasis.opendocument.presentation',
                  'json': 'application/vnd.google-apps.script+json'}

    def __init__(self):

        creds = self.get_credentials()
        self.drive_service = build('drive', 'v3', credentials=creds)

    def delete_file(self, file_id):
        """Deletes a file using its Google Drive file ID

        Args:
            fileId: The Google Drive ID of the file to be deleted

        Returns:
            None
        """

        self.drive_service.files().delete(fileId=file_id).execute()

    def does_file_exist(self, filename):
        """Checks if the file already exists in the user's Google
        Drive folder

        Args:
            filename: The name of the file to check

        Returns
            True if filename exists
            False if the filename does not exist
        """

        file_id = self.get_file_id_from_filename(filename)

        if file_id is None:

            return False

        else:

            return True

    def download_file(self, file_id):
        """Downloads a plain text file from the user's Google Drive account.
        This function assumes that the file_id is valid and exists

        Args:
            file_id: The Google Drive file ID to download

        Returns:
            The string data of the file
        """

        request = self.drive_service.files().get_media(fileId=file_id)
        byte_string_buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(byte_string_buffer, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        string_data = byte_string_buffer.getvalue().decode("utf-8")
        return string_data

    def get_credentials(self):
        """Obtains the user's credentials or generates new ones
        in order to get permission to upload or download files.

        This function will open up a web browser so the user can
        grant this program permission to access their Google Drive
        data. In this case, this program will store the credentials
        locally so the user doesn't have to repeat this process again.

        Returns:
            The credentials to allow this API to upload or download files.
        """

        creds = None
        folder_path = os.path.dirname(__file__)
        token_path = 'data/token.pickle'
        credentials_path = 'data/credentials.json'
        token_filename = os.path.join(folder_path, token_path)
        credentials_filename = os.path.join(folder_path, credentials_path)

        # The file token.pickle stores the user's access and refresh tokens
        # and is created automatically when the authorization flow completes
        # for the first time.
        if os.path.exists(token_filename):
            with open(token_filename, 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_filename, self.SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open(token_filename, 'wb') as token:
                pickle.dump(creds, token)

        return creds

    def get_file_list(self):
        """Calls the Google API to get the list of files in the user's
        Google Drive folder that obey's the SCOPES permissions

        Returns:
            A list of the files in the user's drive folder
        """

        results = self.drive_service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        return results.get('files', [])

    def get_file_id_from_filename(self, filename):
        """Gets the file ID that is connected with the filename

        Args:
            filename: The name with extension to get the file ID of

        Returns:
            If the filename exists, the corresponding file ID is returned
            Else this function returns None
        """

        file_list = self.get_file_list()
        for file_item in file_list:
            if file_item['name'] == filename:
                return file_item['id']
        return None

    def get_mime_types_from_filename(self, file_path):
        """Determines the MIME type to use based on the file type

        Args:
        file_path: Path to the file being uploaded or downloaded

        Returns:
            If the file type is supported, will return the MIME type
            this API uses for the file type.
            If the file type is not supported, will return None
        """

        file_type = self.get_file_type(file_path)
        mime_type = None

        if file_type in ['.json', '.txt']:
            mime_type = self.mime_types['plainText']
        else:
            print("Unknown file type")

        return mime_type

    def print_file_list(self):
        """Gets a list of files from the user's Google Drive account
        and prints them to the console
        """

        items = self.get_file_list()
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))

    def update_file(self, file_id, file_path):
        """Updates an existing file in Google Drive
        This function assumes the calling function has verified that the file
        already exists and the file ID points to a valid file.

        Args:
            file_id: The Google Drive file ID for the file to be updated
            file_path: The local file path of the file to update

        Returns:
            None
        """

        file_metadata = {'name': self.get_filename(file_path)}
        mime_types = self.get_mime_types_from_filename(file_path)

        media = MediaFileUpload(file_path,
                                mime_types=mime_types)
        file = self.drive_service.files().update(fileId=file_id,
                                                 body=file_metadata,
                                                 media_body=media,
                                                 fields='id').execute()

    def upload_file(self, file_path):
        """Uploads a file to the user's Google Drive account

        Args:
            file_path: The file path on the user's local storage where
                       the file is stored

        Returns:
            None
        """

        file_metadata = {'name': self.get_filename(file_path)}
        mime_types = self.get_mime_types_from_filename(file_path)

        media = MediaFileUpload(file_path,
                                mime_types=mime_types)
        file = self.drive_service.files().create(body=file_metadata,
                                                 media_body=media,
                                                 fields='id').execute()
