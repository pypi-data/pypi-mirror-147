#!/usr/bin/env python

import argparse


from physam.sspps.utils import check_per
from physam.sspps.optimal_spps_subsets import Opt

def getOpts():

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="""

            Optimal species subsampling

    Usage:

    %(prog)s [exons]
""")

    parser.add_argument('exons',
                        nargs  = "*",
                        help='Filenames')
    parser.add_argument('-s', '--spps_range',
                        metavar = "",
                        nargs   = 2,
                        type    = int,
                        default = [15, 45],
                        help    = 'Min & max number of species [Default = 15 45]')
    parser.add_argument('-l', '--min_occu',
                        metavar = "",
                        type    = float,
                        default = 80,
                        help    = 'Min occupancy percentage [Default = 80]')
    parser.add_argument('-g', '--gc_range',
                        metavar = "",
                        nargs   = 2,
                        type    = int,
                        default = [45, 55],
                        help    = 'Min & max overall gc average [Default = 45 55]')
    parser.add_argument('-o', '--suffix',
                        metavar = "",
                        type    = str,
                        default = "_subset",
                        help    = 'Suffix [Default = _subset]')                    
    args = parser.parse_args()
    return args

def main():
    args = getOpts()

    # check constraints values
    spps_min,spps_max = args.spps_range
    assert spps_max > spps_min, f"min species ({spps_min}) greater than max species ({spps_max})"

    gc_min,gc_max = args.gc_range
    assert gc_max > gc_min, f"min overall gc ({gc_min}) greater than max overall gc ({gc_max})"
    check_per(gc_min, "gc_min")
    check_per(gc_max, "gc_max")

    min_occu = args.min_occu/100
    check_per(min_occu*100, "min_occu")
    # check constraints values

    Opt(
        fasta_files = args.exons,
        group_file=None,
        epis_ipis= False,
        suffix = args.suffix,
        # constraints
        spps_min = spps_min,
        spps_max = spps_max,
        occu_min = min_occu,
        gc_per_min = gc_min,
        gc_per_max = gc_max
    ).selection()

if __name__ == "__main__":
    main()
