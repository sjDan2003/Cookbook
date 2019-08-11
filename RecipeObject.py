from RecipeScrapers import RecipeScraper


class RecipeObjectClass():
    """This class manages all of the recipe data for each
    recipe
    """

    def __init__(self, recipe_object=None):

        if recipe_object is None:
            self.data = {}
            self.status_code = 0
        else:
            self.data = recipe_object.data
            self.status_code = recipe_object.status_code

    def get_recipe_data_from_url(self, url):

        """Creates a new scraper object and extracts the recipe
        data from the user provided URL

        Args:
            url: The web address for the recipe to scrape

        Returns:
            None
        """

        self.data, self.status_code = RecipeScraper().scrape_recipe_data(url)

    def is_data_valid(self):

        """Checks to make sure that the HTML data is valid

        Returns:
            True if at least one recipe field is valid
            False if there are not valid recipe fields
        """

        return self.data != {}

    def set_recipe_from_dict(self, recipe_dict):
        """This function is used to copy pre-parsed recipe data stored in a dictionary
        format to this object.

        Args:
            recipe_dict: A dictionary containing pre-parsed recipe data

        Returns:
            None
        """
        self.data = recipe_dict

    def get_recipe_name(self):
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

    def get_ingredients(self):
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

    def get_instructions(self):
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

    def get_html_response_code_dict(self):
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

    def get_recipe_errors(self):
        """This function looks at all of the parts of the recipe and looks for issues.
        If there are any issues the user should be notified.

        Args:
            None

        Returns:
            A string with all of the errors that were found.
            If there are no errors, a blank string is returned
        """

        error_string = ''

        # If there was an HTTP error with getting the recipe
        # look up the code and output the error to the user.
        if self.status_code >= 400:

            responses_dict = self.get_html_response_code_dict()
            short_message_index = 0
            long_message_index = 1
            if self.status_code in responses_dict:
                error_message_tuple = responses_dict[self.status_code]
                error_string = '{}\n{}'.format(error_message_tuple[short_message_index],
                                               error_message_tuple[long_message_index])
            else:
                error_string = 'Unknown Error Getting Recipe Information'

        else:

            # If the user was able to connect to the recipe, but for some
            # reason the scrapper wasn't able to get a part of it
            # inform the host which parts of the recipe it couldn't find.
            if self.get_recipe_name() == '':
                error_string += 'Problem finding Recipe Name\n'
            if self.get_ingredients() == '':
                error_string += 'Problem finding Recipe Ingredients\n'
            if self.get_instructions() == '':
                error_string += 'Problem finding Recipe Instructions\n'

        return error_string

    def get_data(self):
        """Returns the dictionary data of the recipie to the calling function

        Args:
            None

        Returns:
            The dictionary data.
        """

        return self.data
