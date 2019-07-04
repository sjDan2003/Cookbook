import unittest
from unittest.mock import patch, mock_open
from Services import DropboxServiceClass


class DropboxTestClass(unittest.TestCase):

    # The constructor of DropboxServiceClass gets the credentials of the user.
    # Since we don't want to do this in test, we'll mock this out.
    @patch('Services.DropboxServiceClass.__init__', unittest.mock.Mock(return_value=None))
    def setUp(self):

        self.dropBoxObj = DropboxServiceClass()

    def test_GetAccesToken(self):

        with patch('builtins.open', new_callable=mock_open()) as mockedOpen:
            with patch('Services.DropboxService.json.load') as mock_json:

                self.dropBoxObj.GetAccessToken()
                mockedOpen.assert_called_with('data/DropboxData.json')

    def test_GetAccessToken_FileNotFound(self):

        with patch('builtins.open', create=True) as mockedOpen:
            mockedOpen.side_effect = FileNotFoundError()
            self.dropBoxObj.GetAccessToken()
