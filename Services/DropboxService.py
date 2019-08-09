import json
from dropbox import Dropbox
from dropbox.exceptions import ApiError
from dropbox.files import WriteMode


class DropboxServiceClass:

    """This class manages the authorization and managment of a user's
    dropbox account.

    Args:
        dropbox: A dropbox object with the ability to access a user's
                 Dropbox account
    """

    def __init__(self):

        self.dropbox = None

        access_token = self.get_access_token()

        if access_token != '' or access_token != 'Error':
            self.dropbox = Dropbox(access_token)

    def get_access_token(self):
        """Reads the developer's access token from the Dropbox Json file
        This access token should only be used for development purposes

        Returns:
            THe developer's access token
        """

        access_token = ''
        developer_access_token_filename = 'data/DropboxData.json'

        try:

            with open(developer_access_token_filename) as dropbox_data:

                dropbox_data_dict = json.load(dropbox_data)
                access_token = dropbox_data_dict['Access Token']

        except FileNotFoundError as error:

            access_token = 'Error'

        return access_token

    def get_user_account_info(self):

        """Returns a user's account information in a dictionary format
        """

        return self.dropbox.users_get_current_account()

    def _files_upload_wrapper(self, in_file_pointer, dropbox_file_path):

        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        return_message = None
        print("Uploading " + in_file_pointer + " to Dropbox as " + dropbox_file_path + "...")
        try:
            self.dropbox.files_upload(in_file_pointer.read(),
                                      dropbox_file_path,
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

    def save_to_dropbox(self, localFilePath, dropbox_file_path='/my-file-backup.txt'):

        return_message = None

        try:
            with open(localFilePath, 'rb') as read_file:
                return_message = self._files_upload_wrapper(read_file,
                                                            dropbox_file_path)

        except FileNotFoundError as error:
            return_message = 'Local file not found'

        return return_message


# dropBoxObj = DropboxServiceClass()
# print(dropBoxObj.get_user_account_info())
