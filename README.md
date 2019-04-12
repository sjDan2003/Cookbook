# My Cookbook

My Cookbook is an app that alllows users to create recipes, organize them, and store them all in one place.
Their recipies can either live on their computer, or in the cloud where they can be access from any device.
This app is written in Python and uses the Kivy GUI Library.


## Other Names

* RecipeGrabber
* FoodieFavories
* RecipeHub

## Getting Started

This code relies on the following Python Libraries.

* Kivy

  Kivy has at least one dependency.
  First you shoud install Cython:
  ```shell
  $ pip3 install Cython
  ```

  Depending on your system, you may also need pygame:
  ```shell
  $ pip3 install pygame
  ```

  Finally, you can install Kivy:
  ```shell
  $ pip3 install kivy
  ```

* Beautiful Soup

   Visit the following website for instructions to install Beautiful Soup:
   https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup


* Google Python API

   In order to save recipes to a user's Google Drive folder, the following packages need to be installed:
   ```shell
   pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```

## Testing

Unit tests have been written in the test folder. These tests have been written using Test Driven Development (TDD) methodolody to speed up the development and ensure that changes to the app can be quickly tested.

To run these tests, execute the following command:
```shell
$ python3 tests/test_AllTests.py
```

## Tested Websites

The following food websites have been used to test this app:

* www.foodnetwork.com
* www.allrecipes.com
* www.food.com
* www.yummly.com
* www.epicurious.com
* www.cookinglight.com
* www.simplyrecipes.com
* www.chowhound.com
* www.thekitchn.com
* www.simplyrecipes.com
* www.myfoodandfamily.com
* www.myrecipes.com
* www.bettycrocker.com
* www.eatingwell.com
* www.cooks.com