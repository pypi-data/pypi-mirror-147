
import copy
import collections
from .utils import fas_to_dic, group_def

class Vars:

    def __init__(self, 
                fasta_files = None,
                group_file = None,
                epis_ipis = False
                ):

        self.fasta_files = fasta_files
        self.gap_chars  = ['N', '-', '!', '?']
        self.gc = ['G', 'C', 'S']
        self.epis_ipis  = epis_ipis
        # self.group_file = group_file
        
        self.group_def = group_def(group_file) if group_file else None


    def _init_spps_table(self, aln):
        return { k:0 for k in aln.keys() }
        
    def stats(self, aln):

        df_template = self._init_spps_table(aln)
        
        species_pis  = copy.deepcopy(df_template)
        nogap_length = copy.deepcopy(df_template)
        gc_count     = copy.deepcopy(df_template)
        # gc_p1_count  = copy.deepcopy(df_template)
        # gc_p2_count  = copy.deepcopy(df_template)
        # gc_p3_count  = copy.deepcopy(df_template)
        
        seq_len = len(next(iter(aln.values())))

        # GAAA
        GDEF = self.group_def if self.epis_ipis else None

        # pos_iter = 0
        for pos in range(seq_len):
            # pos = 1874
            # print(pos)
            column = {}
            for k,v in aln.items():

                tmp_base = v[pos]

                if tmp_base in self.gap_chars:
                    continue

                column[k] = tmp_base

                # other metrics
                nogap_length[k] += 1

                # overall gc content
                gc_count[k] += 1 if tmp_base in self.gc else 0
                
                # gc by position
                # if pos_iter == 0:
                #     gc_p1_count[k] += 1 if tmp_base in self.gc else 0
                #     pos_iter += 1

                # elif pos_iter == 1:
                #     gc_p2_count[k] += 1 if tmp_base in self.gc else 0
                #     pos_iter += 1

                # elif pos_iter == 2:
                #     gc_p3_count[k] += 1 if tmp_base in self.gc else 0
                #     pos_iter = 0

            data_sum = collections.Counter( column.values() )
            uniq_char = len(data_sum)

            if not uniq_char:
                continue

            if uniq_char > 1:
                
                tmp_pi = [base for base,count in data_sum.items() if count > 1]

                if len(tmp_pi) > 1:

                    self.update_species_pis(column, tmp_pi,
                                            species_pis, GDEF)
        
        merged = self.merge_dfs(
                    species_pis , 
                    nogap_length, 
                    gc_count     
                )
                
        return (seq_len, merged) 

    def merge_dfs(self, pis, length, gc):
        out = {}
        for k,v in pis.items():
            out[k] = {
                'pis': v, 
                'len_nogap': length[k],
                'gc': gc[k] 
            }
        return out 

    def update_species_pis(self, column, tmp_pi, species_pis, GDEF):

        if not self.epis_ipis:
            return self.update_overall(column, 
                                       tmp_pi, 
                                       species_pis)

        else:

            return self.update_group_based(column, 
                                           tmp_pi, 
                                           species_pis,
                                           GDEF)

    def update_overall(self, column, tmp_pi, species_pis):

        for k,v in column.items():
            if v in tmp_pi:
                species_pis[k] += 1

    # group based 
    def update_group_based(self, column, tmp_pi, species_pis, GDEF):

        pis_column = { k:v for k,v in column.items() if v in tmp_pi  }
        
        for base in tmp_pi:

            column_set = {}
            for k,v in pis_column.items():
                if v == base:
                    column_set[k] = GDEF[k]
                    
            group_freq     = collections.Counter( column_set.values() )
            is_mixed_group = len(group_freq) > 1

            for s,g in column_set.items():

                # ipis
                if group_freq[g] > 1:
                    species_pis[s] += 1

                # epis 
                if is_mixed_group:
                    species_pis[s] += 1

                del pis_column[s]

    def stat_iterator(self, fas):
        # fas = self.fasta_files[0]
        aln = fas_to_dic(fas)

        return self.stats(aln)


    def get(self):
        out = []
        for fas in self.fasta_files:
            out.append(self.stat_iterator(fas))

        return out

# import glob
# fasta_glob = '/Users/ulises/Desktop/ABL/software/sketch_subsets/data/*-out.fas'
# fasta_files = ['/Users/ulises/Desktop/ABL/software/sketch_subsets/data/ND5.phy-out.fas']

# fasta_files = glob.glob(fasta_glob)
# print(fasta_files)
# group_file = '/Users/ulises/Desktop/ABL/software/sketch_subsets/data/spps_groups.txt'

# self = Vars(
#     fasta_files = fasta_files,
#     group_file  = group_file,
#     epis_ipis   = True
# )
