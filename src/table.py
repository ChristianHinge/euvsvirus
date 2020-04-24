#!/usr/bin/env python3
import argparse
from utilities import argument_parsing as argue

from subfunctions import table2json

def get_parser():
    parser = argparse.ArgumentParser(description="Collection of small scripts for table files.")
    subparsers = argue.subparser_group(parser)
    subparsers.add_parser("json", parents=[table2json.get_parser()], add_help=False).set_defaults(function=table2json.main)
    
    return parser

if __name__ == '__main__':
    parsed_args = get_parser().parse_args()
    parsed_args.function(parsed_args)

