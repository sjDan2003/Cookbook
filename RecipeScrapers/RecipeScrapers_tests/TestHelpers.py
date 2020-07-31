import bs4 as bs
import os

def read_recipe_data(scraper_name, test_file_name):
    """
        Helper function to read the actual recipe from a test HTML file
        This function will open the file, creat a soup object from it
        and call the recipe scraper to extract the data.
    """

    with open(os.path.join(os.path.dirname(__file__),'testHtml/{}'.format(test_file_name)),'r') as inHtml:
        soup = bs.BeautifulSoup(inHtml.read(), 'lxml')
        return scraper_name().extract_recipe_data(soup)

def read_empty_recipe_data(scraper_name):
    """
        Helper function to parse an empty HTML string
        This will be used to test the case where recipe data
        is not found.
    """

    soup = bs.BeautifulSoup("<html></html>", 'lxml')
    return scraper_name().extract_recipe_data(soup)