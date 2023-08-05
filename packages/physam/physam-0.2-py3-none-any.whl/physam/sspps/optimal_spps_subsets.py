
import os
import sys

import numpy as np
import cvxpy as cp
from cvxpy.atoms.affine.binary_operators import multiply


from .variables import Vars, fas_to_dic

# import glob
# fasta_glob  = '/Users/ulises/Desktop/ABL/software/sketch_subsets/data/*-out.fas'
# fasta_files = glob.glob(fasta_glob)
# group_file  = '/Users/ulises/Desktop/ABL/software/sketch_subsets/data/spps_groups.txt'

class Opt(Vars):

    def __init__(self, 
                 fasta_files=None, 
                 group_file=None, 
                 epis_ipis=False,
                 spps_min = 15,
                 spps_max = 45,
                 suffix = '_subset'):

        super().__init__(fasta_files, group_file, epis_ipis)
        
        self.spps_min = spps_min
        self.spps_max = spps_max
        self.suffix   = suffix
        
    def discharge(self, L, features):
        # getting constraints coefficients
        spps = []
        len_nogap = []
        gc  = []
        obj = []
        # discharge
        for k,v in features.items():
            # k,v
            spps.append(k)
            obj.append( v['pis']  )
            len_nogap.append(  v['len_nogap'] )
            gc.append( v['gc']*100/L )

        spps_array = np.array( spps )

        discharge =(
            spps_array,
            obj,
            len_nogap,
            gc
        )
        return discharge

    def is_small(self, N, base_fasta):
        
        pass

    def select(self, file):

        base_fasta = os.path.basename(file)
        aln = fas_to_dic(file)

        L, features = self.stats(aln)
        N = len(features.keys())

        (spps_array,
         obj,
         len_nogap,
         gc) = self.discharge(L, features)


        x   = cp.Variable( N, integer = True )
        pis = cp.Constant( np.array(obj) )

        ob_fun = cp.sum( multiply(pis, x) )

        # constraints vars
        c_l = cp.sum( multiply( len_nogap, x )  )
        c_gc = cp.sum( multiply( gc, x ) )


        sys.stdout.write('Finding subsets for %s\r' % base_fasta)
        sys.stdout.flush()

        n_spps = self.spps_max

        while True:

            if n_spps < self.spps_min:
                break
            
            constraints = [
                cp.sum(x) == n_spps,
                c_l  >= 0.8*n_spps*L,
                c_gc >= 45*n_spps,
                c_gc <= 55*n_spps,
                x >= 0,
                x <= 1
            ]

            subsel = cp.Problem( cp.Maximize( ob_fun ), constraints )
            subsel.solve(solver = cp.GLPK_MI, warm_start = True)

            if subsel.status == 'optimal':
                break

            n_spps -= 1

        if subsel.status != 'optimal':
            sys.stdout.write('Finding subsets for %s. Not found: problem %s\n' % (base_fasta, subsel.status))
            sys.stdout.flush()
            return None


        n_iter = self.spps_max - n_spps
        sys.stdout.write('Finding subsets for %s, found after %s iterations\n' % (base_fasta, n_iter))
        sys.stdout.flush()


        index = subsel.solution.primal_vars[ x.id ]

        self.write_selection( spps_array, index, aln, file )

    def write_selection(self, spps_array, index, aln, file ):

        opt_sel = spps_array[index == 1.]

        with open(file + self.suffix, 'w') as f:
            for spps in opt_sel:
                f.write(
                    "%s\n%s\n" % ( spps, aln[spps] )
                )

    def selection(self):
        for file in self.fasta_files:
            self.select(file)
self = Opt()
# var_c = Vars(
#         fasta_files = fasta_files,
#         group_file  = group_file,
#         epis_ipis   = False
#     )

# aln = fas_to_dic(var_c.fasta_files[0])
# L, features = var_c.stat_iterator( var_c.fasta_files[0] )
# N = len(features.keys())

# # getting constraints coefficients
# spps = []
# len_nogap = []
# gc  = []
# obj = []
# # discharge
# for k,v in features.items():
#     # k,v
#     spps.append(k)
#     obj.append( v['pis']  )
#     len_nogap.append(  v['len_nogap'] )
#     gc.append( v['gc']*100/L )

# spps_array = np.array( spps )


# # min_spps = 15
# x   = cp.Variable( N, integer = True )
# pis = cp.Constant( np.array(obj) )

# ob_fun = cp.sum( multiply(pis, x) )

# # constraints vars
# c_l = cp.sum( multiply( len_nogap, x )  )
# c_gc = cp.sum( multiply( gc, x ) )

# n_spps = 45
# while True:

#     if n_spps < 15:
#         break
    
#     constraints = [
#         cp.sum(x) == n_spps,
#         c_l  >= 0.8*n_spps*L,
#         c_gc >= 45*n_spps,
#         c_gc <= 55*n_spps,
#         x >= 0,
#         x <= 1
#     ]

#     subsel = cp.Problem( cp.Maximize( ob_fun ), constraints )
#     subsel.solve(solver = cp.GLPK_MI, warm_start = True)

#     print(subsel.status)

#     if subsel.status == 'optimal':
#         break

#     n_spps -= 1

# # subsel.value
# index = subsel.solution.primal_vars[ x.id ]
# opt_sel = spps_array[index == 1.]



# # values = [(a,b) for a,b in zip(spps_array, obj)]
# # dtype = [('spps', '<U57'), ('pis', int)]
# # a = np.array(values, dtype=dtype)
# # manual_selection = np.sort(a, order = 'pis')[::-1][:45]
# # manual_spps = set([ a for a,_ in manual_selection])
# # manual_spps == set(opt_sel)




