'''
Created on Jul 15, 2016

@author: btbuxton
'''

import unittest
import sys

def main():
    suites = unittest.defaultTestLoader.discover('tests')
    test_suite = unittest.TestSuite(suites)
    unittest.TextTestRunner().run(test_suite)
    
if __name__ == '__main__':
    print(sys.path)
    main()