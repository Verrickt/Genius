# from func import *
import json
import glob
import raw_graphs
from raw_graphs import *
import pickle
results = []
import tqdm

def generate_dataset(prefix,baseDir):
    res = []
    files = glob.glob(baseDir+r'\*.cfg')
    for path in tqdm.tqdm(files):
        with open(path, 'r') as input:
            g = pickle.load(input)
            for i in range(len(g.raw_graph_list)):
                handle_graph(g, g.raw_graph_list[i],res)
    print len(res)
    with open(r'C:\Users\Von\Desktop\Extracted'+"\\"+prefix+'.json','w') as output:
        output.write(str.join('\n',res))


def handle_graph(gparent,g0,ans):
    res = {}
    g = g0.g
    res["n_num"]=len(g)
    succs = []
    features = []
    instructions = []
    blockNames = []
    res["fname"]=g0.funcname
    for i in range(len(g)):
        succs.append(list(g.successors(i)))
        features.append(get_features(g.node[i]['v']))
        instructions.append(g.node[i]['rawInsts'])
        blockNames.append(g.node[i]['blockName'])
    res["rawInsts"]=instructions
    res["succs"]=succs
    res["features"]=features
    res["src"]=gparent.binary_name
    res['blockNames']=blockNames
    ans.append(json.dumps(res))


def get_features(v):
    string_const = len(v[1])
    num_const = len(v[0])
    num_transfer = v[7]
    num_call = v[4]
    num_inst = v[5]
    num_arith_inst = v[3]
    off_spring = v[2]
    return [string_const,num_const,num_transfer,num_call,num_inst,num_arith_inst,off_spring]


version = ['1.0.1f','1.0.1u']
arch = ['i386','arm','mips']
optim = ['O0','O1','O2','O3']
for v in version:
    for a in arch:
        for o in optim:
            prefix = v+'-'+a+'-'+o
            generate_dataset(prefix,r'C:\Users\Von\Desktop\Extracted'+'\\'+prefix+'\\')

