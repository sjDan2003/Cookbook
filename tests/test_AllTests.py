import unittest
import os

loader = unittest.TestLoader()
testDir = os.path.dirname(__file__)
suite = loader.discover(testDir)

runner = unittest.TextTestRunner()
runner.run(suite)