#!/usr/bin/env python3

import os
import sys
import random
import argparse


def fas_to_dic(file):
    
    file_content = open(file, 'r').readlines()
    seqs_list   = []
    
    for i in file_content:
        line = i.strip()
        if line: # just if file starts empty
            seqs_list.append(line) 
    
    keys = [] 
    values = []    
    i = 0
    while(">" in seqs_list[i]):
        keys.append(seqs_list[i])
        i += 1 
        JustOneValue = []

        while((">" in seqs_list[i]) == False):
            JustOneValue.append(seqs_list[i]) 
            i += 1

            if(i == len(seqs_list)):
                i -= 1
                break

        values.append("".join(JustOneValue).upper().replace(" ", ""))
        
    return dict(zip(keys, values))

def vsum(A,B,n):
    C = []
    for i in range(n):
        C.append( A[i] + B[i] )
    return C

def even_res(Re,nsets):

    if Re == nsets:
        return [1]*nsets

    else:
        Ree = Re%nsets

        A = [ Re//nsets ]*nsets 
        B = [1]*Ree + [0]*(nsets - Ree)

        return vsum( A, B, nsets )

def checked_sizes(raw_dist, max_size):

    updated_sizes = []

    for i in raw_dist:

        if i > max_size:
            updated_sizes.append(max_size)

        else:
            updated_sizes.append(i)

    return updated_sizes

def subset_sizes_mpp(S, mod):
    """
    set size when S is more than twice S
    """

    nsets = S//mod # floor division
    Re    = S%mod  # modulus

    int_load = [mod]*nsets
    res_load = even_res(Re, nsets)

    return vsum( int_load, res_load, nsets )
    # return checked_sizes(raw_dist, max_size)

def glob_set_dims(S, mod, base_fasta):
    """
    hard coded magic numbers:

    30 as mod
    15 as min element size
    45 as max element size
    """
    if S < 15:
        # not_taken_aln.append( base_fasta )
        sys.stderr.write('%s number of species: %s, not taken\n' % (base_fasta, S))
        sys.stderr.flush()
        return None

    elif 15 <= S <= 45:
        return [ S ]
    
    elif 46 <= S <= 59:
        return [ mod,  S%mod ]

    else:
        return subset_sizes_mpp(S, mod)    

def _write_selection( aln, taken, out_name ):

    with open(out_name, 'w') as f:
        for spps in taken:
            f.write( 
                "%s\n%s\n"  % ( spps, aln[spps] ) 
            )
            
def make_sets(set_dims, all_spps, fasta_file, aln):
    """
    generate subsets
    """

    for n,sd in enumerate(set_dims):

        out_name = "%s_subset_%s.fas" % (fasta_file, n + 1)
        taken    = random.sample( all_spps, sd )

        _write_selection( aln, taken, out_name )
        all_spps.difference_update( taken )

def getOpts():

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="""

            Random subsets based on species alignment

    Hard coded numbers:
        - 15 as min element size
        - 45 as max element size
        - 30 main group size

    * Usage:
        $ %(prog)s [alignments]

Designed by U. Rosas & E. Ribeiro
    """)
    parser.add_argument('filenames',
                        nargs="+",
                        help='exons names')

    parser.add_argument('-s', '--seed',
                        metavar = "",
                        type    = int,
                        default = 12345,
                        help    = '[Optional] set seed [Default: 12345]')
    args = parser.parse_args()
    return args

def main():

    mod = 30

    args = getOpts()

    alns = args.filenames
    random.seed(args.seed)

    not_taken_aln = []

    for fasta_file in alns:

        base_fasta = os.path.basename(fasta_file)

        aln      = fas_to_dic(fasta_file)
        all_spps = set(aln.keys())

        S = len(all_spps)

        sys.stdout.write('writting subsets for %s\n' % base_fasta)
        sys.stdout.flush()

        set_dims = glob_set_dims(S, mod, base_fasta)

        if not set_dims:
            not_taken_aln.append(base_fasta)
            continue

        make_sets( set_dims, all_spps, fasta_file, aln )

    if not_taken_aln:
        with open('low_number_of_spps.txt', 'w') as f:
            for i in not_taken_aln:
                f.write("%s\n" % i)

if __name__ == "__main__":
    main()
