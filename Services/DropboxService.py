from dropbox import Dropbox
from dropbox.exceptions import ApiError
import json


class DropboxServiceClass:

    def __init__(self):

        self.dropbox = None

        accessToken = self.GetAccessToken()

        if len(accessToken) != 0:
            self.dropbox = Dropbox(accessToken)

    def GetAccessToken(self):
        """Reads the developer's access token from the Dropbox Json file
        This access token should only be used for development purposes

        Returns:
            THe developer's access token
        """

        accessToken = ''
        developerAccessTokenFilename = 'data/DropboxData.json'

        try:

            with open(developerAccessTokenFilename) as dropboxData:

                dropboxDataDict = json.load(dropboxData)
                accessToken = dropboxDataDict['Access Token']

        except FileNotFoundError as error:

            accessToken = 'Error'

        return accessToken

    def GetUserAccountInfo(self):

        return self.dropbox.users_get_current_account()

    def _files_upload_wrapper(in_file_pointer, dropbox_file_path):

        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        return_message = None
        print("Uploading " + localFilePath + " to Dropbox as " + dropboxFilePath + "...")
        try:
            self.dropbox.files_upload(readFile.read(),
                                        dropboxFilePath,
                                        mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                return_message = 'Cannot back up; insufficient space.'
            elif err.user_message_text:
                return_message = '{}'.format(err.user_message_text)
            else:
                return_message = '{}'.format(err)

        return return_message

    def SaveToDropbox(self, localFilePath, dropboxFilePath='/my-file-backup.txt'):

        return_message = None

        try:
            with open(localFilePath, 'rb') as readFile:
                return_message = _files_upload_wrapper(readFile,
                                                       dropbox_file_path)

        except FileNotFoundError as error:
            return_message = 'Local file not found'


# dropBoxObj = DropboxServiceClass()
# print(dropBoxObj.GetUserAccountInfo())
