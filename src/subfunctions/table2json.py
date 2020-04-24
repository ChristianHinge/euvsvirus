import argparse
from Bio.File import as_handle
from utilities import argument_parsing as argue, pandas_util as pd

def get_parser():
    parser = argparse.ArgumentParser(description='Convert table to JSON.')
    argue.inoutfile(parser)
    argue.delimiter(parser)
    argue.header(parser)
    return parser

def parse_args(args):
    return argue.parse_inoutfile(argue.parse_delimiter(args))

def main(args):
    args = parse_args(args)
    table = pd.read_pandas(args.infile, args.delimiter, args.header)
    with as_handle(args.outfile, 'w') as fh:
        colstrs = ['"{}": {}'.format(col, list(table[col])) for col in table]
        fh.write("{" + ',\n'.join(colstrs) + "}\n")
