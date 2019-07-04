import unittest
from unittest.mock import patch, Mock
from WebsiteScraper import RecipeObjectClass
from urllib.error import HTTPError


class RecipeObjectTestClass(unittest.TestCase):

    @patch('WebsiteScraper.urllib.request.Request')
    @patch('WebsiteScraper.urllib.request.urlopen')
    def test_GetHtmlData_Status_200(self, mock_urlopen, mock_request):

        testString = 'This is a test string'
        testUrl = 'www.mockurl.com'

        # Simply stub out the request so it doesn't try and make a request with the URL
        mock_request = Mock()

        mock_urlopen.return_value.__enter__.return_value.read.side_effect = [testString]
        recipeObject = RecipeObjectClass()
        source = recipeObject.GetHtmlData(testUrl)
        self.assertEqual(testString, source, 'Expected mocked GetHtmlData to return mocked data')

    @patch('WebsiteScraper.urllib.request.Request')
    @patch('WebsiteScraper.urllib.request.urlopen')
    def test_GetHtmlData_Status_400(self, mock_urlopen, mock_request):

        testString = ''
        testUrl = 'www.mockurl.com'
        testCode = 400

        # Simply stub out the request so it doesn't try and make a request with the URL
        mock_request = Mock()

        mock_urlopen.return_value.__enter__.return_value.read.side_effect = HTTPError(testUrl, testCode,None, None, None)
        recipeObject = RecipeObjectClass()
        source = recipeObject.GetHtmlData(testUrl)
        self.assertEqual(testString, source, 'GetHtmlData should return blank string for errors')

    def test_GetRecipeErrors_ErrorCode_404(self):

        testRecipe = RecipeObjectClass()
        testRecipe.statusCode = 404
        message = testRecipe.GetRecipeErrors()
        expectedShortMessage = 'Not Found'
        expectedLongMessage = 'Please check the recipe web address and try again.'
        expectedMessage = '{}\n{}'.format(expectedShortMessage, expectedLongMessage)
        self.assertEqual(expectedMessage, message)