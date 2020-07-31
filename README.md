# My Cookbook

My Cookbook is an app that alllows users to create recipes, organize them, and store them all in one place.
Their recipies can either live on their computer, or in the cloud where they can be access from any device.
This app is written in Python and uses Django web framework.


## Other Names

* RecipeGrabber
* FoodieFavories
* RecipeHub

## Getting Started

This code relies on several Python libraries that can be easily installed using virtualenv

```shell
pip3 install -r requirements.txt
```

## Testing

Unit tests have been written in the test folder. These tests have been written using Test Driven Development (TDD) methodolody to speed up the development and ensure that changes to the app can be quickly tested.

To run these tests, execute the following command:
```shell
$ python3 -m unittest discover
```
To suppress print statements, append the ```-b ``` parameter to the unittest command

## Tested Websites

The following food websites have been used to test this app:

* www.foodnetwork.com
* www.allrecipes.com
* www.food.com
* www.epicurious.com
* www.cookinglight.com
* www.simplyrecipes.com
* www.chowhound.com
* www.thekitchn.com
* www.myfoodandfamily.com
* www.myrecipes.com
* www.bettycrocker.com
* www.eatingwell.com