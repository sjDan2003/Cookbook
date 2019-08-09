import unittest
from unittest.mock import patch, mock_open
from Services import DropboxServiceClass
from dropbox.exceptions import ApiError


class DropboxTestClass(unittest.TestCase):

    # The constructor of DropboxServiceClass gets the credentials of the user.
    # Since we don't want to do this in test, we'll mock this out.
    def setUp(self):

        with patch('Services.DropboxServiceClass.get_access_token') as mockedToken:
            with patch('Services.DropboxService.Dropbox', spec=True) as mockedDropbox:
                mockedToken.return_value = 'Test Token'
                self.dropBoxObj = DropboxServiceClass()
                self.testFilename = '/data/testfile.txt'

    def test_GetAccesToken(self):

        with patch('builtins.open', new_callable=mock_open()) as mockedOpen:
            with patch('DropboxService.json.load') as mock_json:

                self.dropBoxObj.get_access_token()
                mockedOpen.assert_called_with('data/DropboxData.json')

    def test_GetAccessToken_FileNotFound(self):

        with patch('builtins.open', create=True) as mockedOpen:
            mockedOpen.side_effect = FileNotFoundError()
            expected_token = 'Error'
            actual_token = self.dropBoxObj.get_access_token()
            self.assertEqual(expected_token, actual_token, 'Expecting Error')

    # TODO: Determine how to return a mocked Dropbox object without actually
    # authorizing an account.
    @unittest.SkipTest
    def test_save_to_dropbox(self):

        with patch('builtins.open', create=mock_open()) as mockedOpen:
            with patch('Services.DropboxService.Dropbox.files_upload') as mockedFilesUpload:
                self.dropBoxObj.save_to_dropbox(self.testFilename)
