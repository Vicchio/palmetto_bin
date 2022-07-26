#!/usr/bin/env python
# 
# Stephen Patrick Vicchio 
# 2019-10-28
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  

import sys
import os
import argparse

DIR_ = os.getcwd()
FAIL = '\033[91m'
ENDC = '\033[0m'


# Parsing the command line arguments
parser = argparse.ArgumentParser(description="""\n
        This is an examples scipt using argparse to read command line inputs into a
        python script. 
        \n""")
parser.add_argument('-i', action='store', dest='INPUT', 
                    default=None, help='any sort of input that you\'d like within the script.')
parser.add_argument('-s', action='store', dest='STATUS', 
                    default=None, help='another input variabe that you\'d like within the script.')
parser.add_argument('-o', action='store', dest='OUTPUT',
                    default=None, help='any sort of output you\'d like from the script.')
parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
args = parser.parse_args()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# M A I N   P R O G R A M  

print(args.INPUT)
print(args.STATUS)
print(args.OUTPUT)




