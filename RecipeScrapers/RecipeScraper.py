import urllib.request
import bs4 as bs
from .AllRecipeScraper import AllRecipesScraper
from .EpicuriousScraper import EpicuriousScraper
from .CookingLightScraper import CookingLightScraper
from .TheKitchnScraper import TheKitchnScraper
from .BettyCrokerScraper import BettyCrockerScraper
from .EatingWellScraper import EatingWellScraper
from .CooksScraper import CooksScraper
from .JsonScraper import JsonScraper


class RecipeScraper:
    """This class determines the best scraper to get the recipe data
    then connects to the internet to get the recipe information.
    """

    def get_scrapper(self, url):
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

        return_scraper = None

        if 'allrecipes' in url:
            return_scraper = AllRecipesScraper
        elif 'epicurious' in url:
            return_scraper = EpicuriousScraper
        elif 'cookinglight' in url or 'myrecipes' in url:
            return_scraper = CookingLightScraper
        elif 'thekitchn' in url:
            return_scraper = TheKitchnScraper
        elif 'bettycrocker' in url:
            return_scraper = BettyCrockerScraper
        elif 'eatingwell' in url:
            return_scraper = AllRecipesScraper
        elif 'cooks' in url:
            return_scraper = CooksScraper
        else:
            return_scraper = JsonScraper

        return return_scraper

    def scrape_recipe_data(self, url):

        """Determines how to scrape the recipe data using the URL, and passes
        the URL's HTML data to the correct scrapper to extract the recipe data.

        Args:
            url: The website where the recipe is located.

        Returns:
            None.
        """

        raw_html_data, status_code = self.get_html_data(url)

        with open('../test_Annova.html', 'w') as f:
            f.write(raw_html_data.decode("utf-8") )

        # If there was an issue getting the HTML data, treat this as invalid data
        # and return.
        if raw_html_data != '':
            soup = bs.BeautifulSoup(raw_html_data, 'lxml')
            scrapper = self.get_scrapper(url)
            extracted_data = scrapper().extract_recipe_data(soup)
            if extracted_data is not None:
                recipe_data = extracted_data
            else:
                recipe_data = {}
                print('Could not find recipe data for {}'.format(url))
                if isinstance(raw_html_data, bytes):
                    # TODO: Need to find a way to properly decode these sites.
                    # Beautiful Soup will correctly not find the type, but print
                    # the reason why
                    print('Source is byte string')
        else:
            recipe_data = {}
            print('Raw html data invalid')

        return recipe_data, status_code

    def get_html_data(self, url):
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
        request_headers = {}
        request_headers['User-Agent'] = 'Mozilla/5.0'
        source = ''
        status_code = 0

        # Create a request so headers can be added
        req = urllib.request.Request(url, headers=request_headers)
        try:
            with urllib.request.urlopen(req) as response:
                source = response.read()
                status_code = response.getcode()
        except urllib.error.HTTPError as http_error:

            # Save the error code for this object.
            # The GUI will later poll this code and output
            # relevant information to the user.
            status_code = http_error.code

        except urllib.error.URLError as url_error:
            # TODO: Investigate what URLErrors could happen
            # and properly handle each one.
            # For now just print the cause so the app doesn't crash
            # on the user.
            print(url_error.reason)

        return source, status_code
