# This __init__ file makes the test folder a Python module
# Now all unit tests can be executed my running
# python3 -m unittest discover
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
