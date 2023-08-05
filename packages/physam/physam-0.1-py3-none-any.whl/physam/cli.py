#!/usr/bin/env python

import argparse
from .sspps.optimal_spps_subsets import Opt

def getOpts():

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="""
            Optimal subsetting
    Usage:

    %(prog)s [exons]

""",
                                     epilog="")
    parser.add_argument('exons',
                        nargs  = "*",
                        help='Filenames')

    parser.add_argument('-l', '--min',
                        metavar = "",
                        type    = int,
                        default = 15,
                        help    = '[Optional] Minimum number of species [Default = 15]')
    parser.add_argument('-u', '--max',
                        metavar = "",
                        type    = int,
                        default = 45,
                        help    = '[Optional] Maximum number of species [Default = 45]')
    parser.add_argument('-s', '--suffix',
                        metavar = "",
                        type    = str,
                        default = "_subset",
                        help    = '[Optional] suffix [Default = _rooted_groups.tsv]')                    
    args = parser.parse_args()
    return args

def main():
    args = getOpts()
    Opt(
        fasta_files = args.exons,
        group_file=None,
        epis_ipis= False,
        spps_min=args.min,
        spps_max=args.max,
        suffix= args.suffix
    ).selection()


if __name__ == "__main__":
    main()
