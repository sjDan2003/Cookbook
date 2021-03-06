import unittest
from unittest.mock import patch
from Services import GoogleDriveClass


class GoogleDriveTestClass(unittest.TestCase):

    # The constructor of GoogleDriveClass gets the credentials of the user.
    # Since we don't want to do this in test, we'll mock this out.
    @patch('Services.GoogleDriveClass.__init__', unittest.mock.Mock(return_value=None))
    def setUp(self):

        self.googleDrive = GoogleDriveClass()
        self.dummyFileName = '/data/savedRecipes.json'

    # TODO: Now that I have a better understanding of unittest's Mocking system, need
    # come up with a test plan for unittesting Google Drive methods.
    def test_ListFiles(self):

        pass
