import pickle
import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload, MediaIoBaseDownload


class GoogleDriveClass():

    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    # MIME stands for Multipurpose Internet Mail Extensions, and is also sometimes referred
    # to as Media Type. It's a standard that indicates the nature of a file.
    mimeTypes = {'HTML': 'text/html', 'zip': 'application/zip', 'plainText': 'text/plain',
                'richText': 'application/rtf', 'openOfficeDoc': 'application/vnd.oasis.opendocument.text',
                'pdf':	'application/pdf', 'msWord' : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'epub': 'application/epub+zip', 'msExcel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'openOfficeSheet': 'application/x-vnd.oasis.opendocument.spreadsheet', 'pdf': 'application/pdf', 'csv': 'text/csv',
                'tsv': 'text/tab-separated-values', 'htmlZip': 'application/zip', 'jpeg': 'image/jpeg', 'png': 'image/png',
                'svg': 'image/svg+xml', 'msPowerPoint': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'openOfficePresentation': 'application/vnd.oasis.opendocument.presentation',
                'json': 'application/vnd.google-apps.script+json'}


    def __init__(self):

        creds = self.GetCredentials()
        self.drive_service = build('drive', 'v3', credentials=creds)


    def DeleteFile(self, fileId):
        """Deletes a file using its Google Drive file ID

        Args:
            fileId: The Google Drive ID of the file to be deleted

        Returns:
            None
        """

        self.drive_service.files().delete(fileId = fileId).execute()


    def DoesFileExist(self, filename):
        """Checks if the file already exists in the user's Google
        Drive folder

        Args:
            filename: The name of the file to check

        Returns
            True if filename exists
            False if the filename does not exist
        """

        fileId = self.GetFileIdFromFilename(filename)

        if fileId == None:

            return False

        else:

            return True


    def DownloadFile(self, file_id):
        """Downloads a plain text file from the user's Google Drive account.
        This function assumes that the file_id is valid and exists

        Args:
            file_id: The Google Drive file ID to download

        Returns:
            The string data of the file
        """

        request = self.drive_service.files().get_media(fileId=file_id)
        byteStringBuffer = io.BytesIO()
        downloader = MediaIoBaseDownload(byteStringBuffer, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        stringData = byteStringBuffer.getvalue().decode("utf-8")
        return stringData

    def GetCredentials(self):
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
        tokenFilename = 'data/token.pickle'
        credentialsFilename = 'data/credentials.json'
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(tokenFilename):
            with open(tokenFilename, 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentialsFilename, self.SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open(tokenFilename, 'wb') as token:
                pickle.dump(creds, token)

        return creds


    def GetFileList(self):
        """Calls the Google API to get the list of files in the user's
        Google Drive folder that obey's the SCOPES permissions

        Returns:
            A list of the files in the user's drive folder
        """

        results = self.drive_service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        return results.get('files', [])


    def GetFileIdFromFilename(self, filename):
        """Gets the file ID that is connected with the filename

        Args:
            filename: The name with extension to get the file ID of

        Returns:
            If the filename exists, the corresponding file ID is returned
            Else this function returns None
        """


        fileList = self.GetFileList()
        for fileItem in fileList:
            if fileItem['name'] == filename:
                return fileItem['id']
        return None


    def GetFileName(self, filePath):
        """Gets the file name of the file being uploaded
        or downloaded

        Args:
            filePath: The full file path to get the file name for

        Returns:
            If the file path contains a valid filename, then
            the file name is returned.
            Else, if the file path is a folder or blank, then
            None is returned.
        """

        fileName = os.path.split(filePath)[1]

        if fileName is not '':
            return fileName
        else:
            return None


    def GetFileType(self, filePath):
        """Gets the file type from the file being uploaded
        or downloaded to the user's Google Drive Account

        Args:
            filePath: The file to get the file type for

        Returns:
            If the file has a file type, that file type is returned
            Else, this function returns None
        """

        fileType = os.path.splitext(filePath)[1]

        if fileType is not '':
            return fileType
        else:
            return None


    def GetMimeTypeFromFileName(self, filePath):
        """Determines the MIME type to use based on the file type

        Args:
            filePath: Path to the file being uploaded or downloaded

        Returns:
            If the file type is supported, will return the MIME type
            this API uses for the file type.
            If the file type is not supported, will return None
        """

        file_type = self.GetFileType(filePath)

        if file_type in ['.json', '.txt']:

            return self.mimeTypes['plainText']

        else:
            print("Unknown file type")
            return None


    def PrintFileList(self):
        """Gets a list of files from the user's Google Drive account
        and prints them to the console
        """

        items = self.GetFileList()
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))


    def UpdateFile(self, fileId, filePath):
        """Updates an existing file in Google Drive
        This function assumes the calling function has verified that the file already
        exists and the file ID points to a valid file.

        Args:
            fileId: The Google Drive file ID for the file to be updated
            filePath: The local file path of the file to update

        Returns:
            None
        """

        file_metadata = {'name': self.GetFileName(filePath)}
        mimeType = self.GetMimeTypeFromFileName(filePath)

        media = MediaFileUpload(filePath,
                                mimetype=mimeType)
        file = self.drive_service.files().update(fileId = fileId,
                                            body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()


    def UploadFile(self, filePath):

        """Uploads a file to the user's Google Drive account

        Args:
            filePath: The file path on the user's local storage where the file is stored

        Returns:
            None
        """

        file_metadata = {'name': self.GetFileName(filePath)}
        mimeType = self.GetMimeTypeFromFileName(filePath)

        media = MediaFileUpload(filePath,
                                mimetype=mimeType)
        file = self.drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """

    cloudService = GoogleDriveClass()

    localBaseDir = os.path.split(os.path.abspath(__file__))[0]
    localRecipeJson = os.path.join(localBaseDir, 'data/savedRecipes.json')

    print(localRecipeJson)

    #cloudService.DeleteFile('1CS51JEXW9jlLGZq3JUzOmAMMnXVJlRak')
    cloudService.DownloadFile('1dJqBAErXGC_rwqIGBvUj5pRfjUcK6V-P')
    return
    filename = cloudService.GetFileName(localRecipeJson)
    print(filename)

    if cloudService.DoesFileExist(filename):

        print('Updating file')
        fileId = cloudService.GetFileIdFromFilename(filename)
        cloudService.UpdateFile(fileId, localRecipeJson)

    else:

        print('Uploading new file')
        cloudService.UploadFile(localRecipeJson)


    cloudService.PrintFileList()

    #cloudService.DeleteFile(fileId)

    #cloudService.PrintFileList()

if __name__ == '__main__':
    main()