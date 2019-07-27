import bs4 as bs
import urllib.request
from RecipeScrapers import *


class RecipeObjectClass():

    def __init__(self, recipeObj=None):

        if recipeObj is None:
            self.data = {}
            self.validData = False
            self.statusCode = 0
        else:
            self.data = recipeObj.data
            self.validData = recipeObj.validData
            self.statusCode = recipeObj.statusCode

    def GetScrapper(self, url):
        """Gets the class pointer to the specific scrapper based on the URL
        of the food website.

        Different food sites use different methods to format the recipe data
        This function identifies the best scrapper to scrape the recipe data
        and returns it to the calling fucntion

        Args:
            url: The full URL of the food website

        Returns:
            Class pointer for the specific scraper to parse the website
        """

        if 'allrecipes' in url:
            return AllRecipesScraper
        elif 'epicurious' in url:
            return EpicuriousScrapper
        elif 'cookinglight' in url or 'myrecipes' in url:
            return CookingLightScraper
        elif 'thekitchn' in url:
            return TheKitchnScrapper
        elif 'bettycrocker' in url:
            return BettyCrockerScraper
        elif 'eatingwell' in url:
            return EatingWellScraper
        elif 'cooks' in url:
            return CooksScraper
        else:
            return JsonScraper

    def GetHtmlData(self, url):
        """Retrieves the HTML data from a url
        Other functions or libraries will be used to parse this data.

        Args:
            url: The website to open and read the HTML data

        Returns:
            If there is an issue opening the website this function will return
            a blank string
            Otherwise the entire website's HTML data will be returned.
        """

        # Adding a custom header will prevent a 403 Forbidden response from a website
        # Rather than using the default header and retrying on a 403, just send
        # the custom header initially.
        requestHeaders = {}
        requestHeaders['User-Agent'] = 'Chrome Browser'
        source = ''

        # Create a request so headers can be added
        req = urllib.request.Request(url, headers=requestHeaders)
        try:
            with urllib.request.urlopen(req) as response:
                source = response.read()
                self.statusCode = response.getcode()
        except urllib.error.HTTPError as httpError:

            # Save the error code for this object.
            # The GUI will later poll this code and output
            # relevant information to the user.
            self.statusCode = httpError.code

        except urllib.error.URLError as urlError:
            # TODO: Investigate what URLErrors could happen
            # and properly handle each one.
            # For now just print the cause so the app doesn't crash
            # on the user.
            print(urlError.reason)

        return source

    def GetRecipeFromUrl(self, url):
        """Determines how to scrape the recipe data using the URL, and passes
        the URL's HTML data to the correct scrapper to extract the recipe data.
        If there is a valid recipe data in the URL the validData flag is set to True
        and use the data from the recipe scrapper
        Otherwise the validData flag is set to false and the data dict is set to empty.

        Args:
            url: The website where the recipe is located.

        Returns:
            None.
        """

        rawHtmlData = self.GetHtmlData(url)

        # If there was an issue getting the HTML data, treat this as invalid data
        # and return.
        if rawHtmlData != '':
            soup = bs.BeautifulSoup(rawHtmlData, 'lxml')
            scrapper = self.GetScrapper(url)
            recipeData = scrapper().ExtractRecipeData(soup)
            if recipeData is not None:
                self.data = recipeData
                self.validData = True
            else:
                self.data = {}
                self.validData = False
                print('Could not find recipe data for {}'.format(url))
                if type(rawHtmlData) is bytes:
                    # TODO: Need to find a way to properly decode these sites.
                    # Beautiful Soup will correctly not find the type, but print
                    # the reason why
                    print('Source is byte string')
        else:
            self.data = {}
            self.validData = False
            print('Raw html data invalid')

    def SetRecipeFromDict(self, recipeDict):
        """This function is used to copy pre-parsed recipe data stored in a dictionary
        format to this object.

        Args:
            recipeDict: A dictionary containing pre-parsed recipe data

        Returns:
            None
        """
        self.data = recipeDict
        self.validData = True

    def GetRecipeName(self):
        """Returns the recipe name to the calling function

        Args:
            None

        Returns:
            If a name wasn't stored, this function will returns a blank string
            Otherwise the name of the recipe is returned.
        """

        if 'name' in self.data:
            return self.data['name']
        else:
            return ''

    def GetIngredients(self):
        """Returns the recipe ingredients to the calling function

        Args:
            None

        Returns:
            If the ingredients weren't stored, this function will returns a blank string
            Otherwise the ingredients of the recipe are returned.
        """

        if 'recipeIngredient' in self.data:
            return self.data['recipeIngredient']
        else:
            return ''

    def GetInstructions(self):
        """Returns the recipe instructions to the calling function

        Args:
            None

        Returns:
            If the instructions weren't stored, this function will returns a blank string
            Otherwise the instructions of the recipe are returned.
        """

        if 'recipeInstructions' in self.data:
            return self.data['recipeInstructions']
        else:
            return ''

    def GetHtmlResponseCodeDict(self):
        """This function returns a table with an index of all Html Response
        codes, and their corresponding message.
        This is based on the table from http.serverBaseHTTPRequestHandler.responses
        only that the messages have been modified to be more user friendly

        Args:
            None

        Returns:
            A dictionary containing error codes and their corresponding
            messages
        """

        return {100: ('Continue', 'Request received, please continue'),
                101: ('Switching Protocols',
                      'Switching to new protocol; obey Upgrade header'),

                200: ('OK', 'Request fulfilled, document follows'),
                201: ('Created', 'Document created, URL follows'),
                202: ('Accepted',
                      'Request accepted, processing continues off-line'),
                203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
                204: ('No Content', 'Request fulfilled, nothing follows'),
                205: ('Reset Content', 'Clear input form for further input.'),
                206: ('Partial Content', 'Partial content follows.'),

                300: ('Multiple Choices',
                      'Object has several resources -- see URI list'),
                301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
                302: ('Found', 'Object moved temporarily -- see URI list'),
                303: ('See Other', 'Object moved -- see Method and URL list'),
                304: ('Not Modified',
                      'Document has not changed since given time'),
                305: ('Use Proxy',
                      'You must use proxy specified in Location to access this '
                      'resource.'),
                307: ('Temporary Redirect',
                      'Object moved temporarily -- see URI list'),
                400: ('Bad Request',
                      'Bad request syntax or unsupported method'),
                401: ('Unauthorized',
                      'Sorry, but you do not have permission to view this recipe'),
                402: ('Payment Required',
                      'Payment is required to view this recipe.'),
                403: ('Forbidden',
                      'Sorry, but it is forbidden to access this recipe'),
                404: ('Not Found', 'Please check the recipe web address and try again.'),
                405: ('Method Not Allowed',
                      'Specified method is invalid for this server.'),
                406: ('Not Acceptable', 'URI not available in preferred format.'),
                407: ('Proxy Authentication Required', 'You must authenticate with '
                      'this proxy before proceeding.'),
                408: ('Request Timeout',
                      'Sorry but the website timed out while trying to connect\n \
                       Please try again later.'),
                409: ('Conflict', 'Request conflict.'),
                410: ('Gone',
                      'Sorry but it seems like the recipe has been removed..'),
                411: ('Length Required', 'Client must specify Content-Length.'),
                412: ('Precondition Failed', 'Precondition in headers is false.'),
                413: ('Request Entity Too Large', 'Entity is too large.'),
                414: ('Request-URI Too Long', 'URI is too long.'),
                415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
                416: ('Requested Range Not Satisfiable',
                      'Cannot satisfy request range.'),
                417: ('Expectation Failed',
                      'Expect condition could not be satisfied.'),
                500: ('Internal Server Error', 'Server got itself in trouble'),
                501: ('Not Implemented',
                      'Server does not support this operation'),
                502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
                503: ('Service Unavailable',
                      'The server cannot process the request due to a high load'),
                504: ('Gateway Timeout',
                      'The gateway server did not receive a timely response'),
                505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
                }

    def GetRecipeErrors(self):
        """This function looks at all of the parts of the recipe and looks for issues.
        If there are any issues the user should be notified.

        Args:
            None

        Returns:
            A string with all of the errors that were found.
            If there are no errors, a blank string is returned
        """

        errorStr = ''

        # If there was an HTTP error with getting the recipe
        # look up the code and output the error to the user.
        if self.statusCode >= 400:

            responsesDict = self.GetHtmlResponseCodeDict()
            shortMessageIndex = 0
            longMessageIndex = 1
            if self.statusCode in responsesDict:
                errorMessageTuple = responsesDict[self.statusCode]
                errorStr = '{}\n{}'.format(errorMessageTuple[shortMessageIndex],
                                           errorMessageTuple[longMessageIndex])
            else:
                errorStr = 'Unknown Error Getting Recipe Information'

        else:

            # If the user was able to connect to the recipe, but for some
            # reason the scrapper wasn't able to get a part of it
            # inform the host which parts of the recipe it couldn't find.
            if self.GetRecipeName() == '':
                errorStr += 'Problem finding Recipe Name\n'
            if self.GetIngredients() == '':
                errorStr += 'Problem finding Recipe Ingredients\n'
            if self.GetInstructions() == '':
                errorStr += 'Problem finding Recipe Instructions\n'

        return errorStr

    def GetData(self):
        """Returns the dictionary data of the recipie to the calling function

        Args:
            None

        Returns:
            The dictionary data.
        """

        return self.data
