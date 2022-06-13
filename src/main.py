#!/usr/bin/env python

'''
CMS395: A Lexical Analyzer for the PL/0 Language
Fall 2021
Daniel Liew, Benjamin Mann, Cameron Dolly
'''

from lexical_analyzer import analyze_file
from pl0_parser.parser import Parser
import constants

if __name__ == '__main__':
    tokens = analyze_file(constants.FILENAME)
    Parser(tokens).parse()
