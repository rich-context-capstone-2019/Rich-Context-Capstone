import json 
import itertools
import pandas as pd
import networkx as nx
from networkx.readwrite import json_graph
import community
import re
import nltk
from nltk.tokenize import word_tokenize

def writeNX(filename, g):
    network_json = json_graph.node_link_data(g)
    json.dump(network_json, open(filename, 'w'), indent=2)
def readNX(filename):
    with open(filename) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)

### 1. Load train_test data
tt_pub = pd.read_json('data/train_test/publications.json')
tt_data = pd.read_json('data/train_test/data_sets.json')
tt_cit = pd.read_json('data/train_test/data_set_citations.json')
tt_cit['source'] = 'train_test'

### 2. Load Rich Context Competition Data

p1_pub = pd.read_json('data/phase1_holdout_publications.json')
p2_pub = pd.read_json('data/phase2_holdout_publications.json')

p1_cit = pd.read_json('data/competition-output/phase1-final/rcc-03/raw_results/data_set_citations.json')
p1_cit['source'] = 'phase1'
p2_cit = pd.read_json('data/competition-output/phase2-final/rcc-05/raw_results/holdout/output/data_set_citations.json')
p2_cit['source'] = 'phase2'
p2_cit_wc =  pd.read_json('data/competition-output/phase2-final/rcc-05/raw_results/wc_holdout/output/data_set_citations.json')
p2_cit_wc['source'] = 'phase2_wc'

### 3. Combine data from step 1 & 2
all_pubs = pd.concat([tt_pub, p1_pub, p2_pub]).reset_index(drop=True)
all_data = tt_data

all_cit = pd.concat([tt_cit[['publication_id', 'data_set_id', 'score', 'source']], 
                     p1_cit[['publication_id', 'data_set_id', 'score', 'source']], 
                     p2_cit[['publication_id', 'data_set_id', 'score', 'source']],
                     p2_cit_wc[['publication_id', 'data_set_id', 'score', 'source']]]).reset_index(drop=True)
all_cit['pub_name'] = ['pub_'+str(i) for i in all_cit.publication_id] 
all_cit['data_name'] = ['data_'+str(i) for i in all_cit.data_set_id] 


### 5. Generate [dataset, publication] Graph
pub_nodes = ['pub_'+str(i) for i in all_pubs.publication_id]
data_nodes = ['data_'+str(i) for i in all_data.data_set_id]
pub_edges = [(x,y) for x,y in zip(all_cit.pub_name, all_cit.data_name)]
    
### 6. Extract & Integrate Subject Terms
all_sub = [i.split(',') for i in all_data.subjects]
all_sub = set(list(itertools.chain(*all_sub)))
sub_edges = [('data_'+str(x),sub) for x,y in zip(all_data.data_set_id, all_data.subjects) for sub in y.split(',')]

def addST(g, c=False):
    if c:
        g.add_nodes_from(all_sub)
        g.add_edges_from(new_sub_edges)
    else:
        g.add_nodes_from(all_sub)
        g.add_edges_from(edges)

### 7. Load & Integrate Author
all_auth = pd.read_csv('data/p1p2_PubAuthor_pairs.csv')[['publication_id', 'AuthorId']]
all_auth = pd.concat([all_auth, pd.read_csv('data/PubAuthor_pairs.csv')[['publication_id', 'AuthorId']]]).reset_index(drop=True)
auth_nodes = ['auth_'+str(i) for i in list(set(all_auth.AuthorId))]
auth_edges = [('pub_'+str(x),'auth_'+str(y)) for x,y in zip(all_auth.publication_id, all_auth.AuthorId)]

def addAuth(g):
    g.add_nodes_from(auth_nodes)
    g.add_edges_from(auth_edges)

### 8. Load & Integrate Publication Text Similarity Edges
all_sim = pd.read_csv('data/doc_sim.csv')[['Doc1', 'Doc2', 'Similarity']]
top_sim = all_sim[all_sim.Similarity >= 0.95]
sim_edges = [(x,y) for x,y in zip(top_sim.Doc1, top_sim.Doc2)]

def addPubSim(g):
    g.add_edges_from(sim_edges)
    
    ### 4. Contract Similar Dataset Titles
roman = re.compile("""
    ^                   # beginning of string
    M{0,4}              # thousands - 0 to 4 M's
    (CM|CD|D?C{0,3})    # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),
                        #            or 500-800 (D, followed by 0 to 3 C's)
    (XC|XL|L?X{0,3})    # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),
                        #        or 50-80 (L, followed by 0 to 3 X's)
    (IX|IV|V?I{0,3})    # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
                        #        or 5-8 (V, followed by 0 to 3 I's)
    $                   # end of string
    """ ,re.VERBOSE)
def remove_roman(sent):
    sent = word_tokenize(sent)
    sent = [i for i in sent if not roman.search(i)]
    return " ".join(sent)
def simplify_title(s):
    s = remove_roman(s)
    s = s.lower()
    s = re.sub("[^a-zA-Z]+", "", s)
    return s

df_datasets = all_data.copy()
df_datasets['data_name'] = ['data_'+str(i) for i in df_datasets.data_set_id]
df_datasets['title_unique'] = [simplify_title(i) for i in df_datasets.title]

titles = [simplify_title(i) for i in all_data.title]

df_titles = pd.DataFrame(set(titles)).reset_index()
df_titles.columns = ['title_id','title_unique']
df_titles.title_id = ['title_'+str(i) for i in df_titles.index]

df_datasets = pd.merge(df_datasets, df_titles, on='title_unique', how='left')

contract = df_datasets.groupby('title_id')['data_name'].apply(list).reset_index()
contract['focal'] = [i[0] for i in contract.data_name]
contract['count'] = [len(i) for i in contract.data_name]

df_datasets = pd.merge(df_datasets, contract[['title_id', 'focal']], on='title_id', how='left')

focals = dict(zip(df_datasets.data_name,df_datasets.focal))

new_edges = [(x,focals[y]) for x,y in pub_edges]
new_data_nodes = list(set([focals[i] for i in data_nodes]))
new_sub_edges = [(focals[x], y) for x,y in sub_edges]

def startG(c=False):
    g = nx.Graph()
    if c:
        g.add_nodes_from(pub_nodes+new_data_nodes)
        g.add_edges_from(new_edges)
    else:
        g.add_nodes_from(pub_nodes+data_nodes)
        g.add_edges_from(pub_edges) 
    return g
### 9. Load & Integrate Field of Study Entity
all_fos = pd.read_csv('data/allFoS_PubID.csv', dtype=object)
all_fos['pub_name'] = ['pub_'+str(i) for i in all_fos.publication_id]
fos_edges = [('pub_'+str(x),y) for x,y in zip(all_fos.publication_id, all_fos.NormalizedName)]

def addFoS(g):
    g.add_edges_from(fos_edges)
    
def addCommunity(g):
    g.remove_nodes_from([i for i in g.nodes if str(i)=='nan']+['pub_nan'])
    partition = community.best_partition(g)
    for i in g.nodes:
        g.nodes[i]['community'] = partition.get(i)
    
def buildG(c=True):
    g = startG(c)
    addST(g, c)
    addAuth(g)
    addPubSim(g)
    addFoS(g)
    return g