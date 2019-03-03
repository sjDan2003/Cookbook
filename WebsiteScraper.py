import bs4 as bs
import urllib.request
import json


url = 'https://www.runnersworld.com/recipes/irish-pork-stew-with-irish-stout-and-caraway-seeds'

source = urllib.request.urlopen(url).read()
soup = bs.BeautifulSoup(source, 'lxml')
print(soup.title)
print(soup.title.string)
print(soup.title.parent.name)
print(soup.p)

data = json.loads(soup.find('script', type='application/ld+json').text)
print(data['headline'])
