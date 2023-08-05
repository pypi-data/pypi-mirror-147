

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


def group_def(group_file):
    out = {}
    with open(group_file, 'r') as f:
        for i in f.readlines():
            g,spps = i.strip().split(',')
            out[ ">" +  spps] = g
            
    return out

def check_per(value, var):
    assert 0 <= value <= 100, f"{var} ({value}) out of percentage range"
