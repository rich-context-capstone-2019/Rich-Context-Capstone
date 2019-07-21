import pandas as pd
import difflib
import math
import re
import nltk
import networkx as nx
import NetworkBuilder as nb
from nltk.tokenize import word_tokenize

datasets = pd.read_json('data/train_test/data_sets.json')
publications = pd.read_json('data/train_test/publications.json')
datasets['title_lower'] = datasets['title'].str.lower()
publications['title_lower'] = publications['title'].str.lower()

def generatePairs(firstNode, allDatasets):
    return [(firstNode, i) for i in allDatasets]
def cosineSimilarity(G, pairs):
    preds = []
    for u,v in pairs:
        common = len(list(nx.common_neighbors(G, u, v)))
        s = common / math.sqrt(len(G[u])*len(G[v]))
        preds.append((int(v.replace('data_', '')),s))
    return pd.DataFrame(preds, columns=['data_set_id', 'score']).iloc[:10]

def getNodeSim(node, g, metric):
    allDatasets = [i for i in g.nodes if(str(i).startswith('data_'))]
    pairs = generatePairs(node, [i for i in allDatasets if str(i) != node])
    
    if metric == 'Jaccard':
        preds = nx.jaccard_coefficient(g, pairs)
    elif metric == 'Adamic-Adar':
        preds = nx.adamic_adar_index(g, pairs)
    elif metric == 'Hopcroft':
        preds = nx.ra_index_soundarajan_hopcroft(g, pairs)
    elif metric == 'Cosine':
        return cosineSimilarity(g, pairs)
    else:
        return []
    
    res = []
    for u,v,p in preds:
        if p > 0.0:
            res.append((u,int(v.replace('data_', '')),p))
    df = pd.DataFrame(res, columns=['x', 'data_set_id', 'score'])
    return df[['data_set_id', 'score']].iloc[:10]

def getRecommendations(Search_By='Keyword', search='', metric='Jaccard', G=None):
    all_res =  pd.DataFrame()
    nodes = []
    if search == '':
        print('MISSING ARGUMENT: Specify Search Value!')
        return all_res
    elif G is None:
        G = nb.buildG()
        nb.addCommunity(G)
        
    allDatasets = [i for i in G.nodes if(str(i).startswith('data_'))]
    allPubs = [i for i in G.nodes if(str(i).startswith('pub_'))]
    all_keywords = [str(i) for i in G.nodes if (~str(i).startswith('data_')) & (~str(i).startswith('pub_')) & (~str(i).startswith('auth_'))]
    all_dataTitles = dict(zip(datasets.title_lower, ['data_'+str(i) for i in datasets.data_set_id]))
    all_pubTitles = dict(zip(publications.title_lower, ['pub_'+str(i) for i in publications.publication_id]))
     
    if Search_By == 'Keyword':
        match = difflib.get_close_matches(search, all_keywords)
        if len(match)>0:
            nodes = [i for i in G.neighbors(match[0]) if str(i).startswith('data_')] if len(match)>0 else []
            all_res = pd.DataFrame([int(i.replace('data_','')) for i in nodes], columns =['data_set_id'])
            all_res['score'] = 1.0
            nodes.extend([i for i in G.neighbors(match[0]) if str(i).startswith('pub_')])
    elif Search_By == 'Dataset':
        match = difflib.get_close_matches(search, list(all_dataTitles.keys())+list(all_dataTitles.values()))
        if len(match)>0:
            nodes = [match[0]] if '_' in match[0] else [all_dataTitles[match[0]]] 
    elif Search_By == 'Publication Paper':
        match = difflib.get_close_matches(search, list(all_pubTitles.keys())+list(all_pubTitles.values()))
        if len(match)>0:
            nodes = [match[0]] if '_' in match[0] else [all_pubTitles[match[0]]] 
    else:
        print('MISSING ARGUMENT: Specify Search Criteria!')
        return all_res
    
    if len(match)>0:
        print(match[0])
        
    if all_res.shape[0] < 10:
        for n in nodes:
            res = getNodeSim(n, G, metric)
            all_res = res if res.shape[0] <= 0 else pd.concat([all_res, res], sort=False)
        all_res = all_res.reset_index(drop=True)
    
    if all_res.shape[0]>0:
        all_res = pd.merge(all_res, datasets[['data_set_id', 'title', 'description']], how='left', on='data_set_id')
        all_res = all_res.sort_values(by='score', ascending=False).reset_index(drop=True)
        return all_res.iloc[:10]
    else: 
        return all_res