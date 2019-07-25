from os.path import dirname, join

import pandas as pd
import numpy as np

import json
import logging
import NetworkBuilder as nb
import RecommendationSystem as rs

from bokeh.layouts import row, column, layout
from bokeh.models import ColumnDataSource, Button
from bokeh.events import ButtonClick
from bokeh.models.widgets import TextInput, Button, DataTable, TableColumn, HTMLTemplateFormatter, RadioButtonGroup, PreText, AutocompleteInput
from bokeh.io import curdoc
from bokeh.plotting import output_file, show
output_file("RS_System.html")


template = """<span href="#" data-toggle="tooltip" title="<%= value %>"><%= value %></span>"""
byButton = True
curr = 0

title = PreText(text = "Search Rich Context Archive")
rs_title = PreText(text = "Recommendation Results: ")

df = pd.read_csv('data/ICPSR_ARCHIVE.csv')
df = df.replace(np.nan, '', regex=True)
with open('data/dataset_focals.json') as fl:
    focals = json.load(fl)
G = nb.readNX('data/network_v2.5_contract.json')
all_keywords = [str(i) for i in G.nodes if (~str(i).startswith('data_')) & (~str(i).startswith('pub_')) & (~str(i).startswith('auth_'))]
output_file('ICPSR_Archive.html',mode='inline',root_dir=None)

source = ColumnDataSource(data=dict())
rs_source = ColumnDataSource(data=dict())


def update():    
    t = menu[nmenu.active][1]
    logging.info(t)
    current = df.sample(10)
    if search.value != "":
        if t != "":
            current = df.loc[(df.ID.str.startswith(t))&(df.title.str.contains(search.value, case=False)==True)]
        else:
            current = df.loc[df.title.str.contains(search.value, case=False)==True]
    else:
        current = df.loc[df.ID.str.startswith(t)].sample(10)

    print (current.shape[0])
    source.data = {
        'ID'             : current.ID,
        'title'           : current.title,
        'description' : current.description,
    }

def rs_update():
    byButton = True
    rs_button.label = "Calculating..."
    logging.info("RS_Button: %s, %s"%(str(rs_search.value), how[nhow.active]))
    res = pd.DataFrame()
    rs_source.data = dict()
    if rs_search.value != "":
        res = rs.getRecommendations('Keyword', rs_search.value, how[nhow.active], G)
    
    if res.shape[0] > 0:
        rs_source.data = {
            'data_set_id': res.data_set_id,
            'rs_score': res.score,
            'rs_title': res.title,
            'rs_description': res.description,
        }
    rs_button.label = "Recommend"

def byRow(id):
    logging.info("RS_byRow: %s, %s"%(id, how[nhow.active]))
    res = pd.DataFrame()
    rs_source.data = dict()
    if id.startswith('data_'):
        res = rs.getRecommendations('Dataset', focals[id], how[nhow.active], G)
    elif id.startswith('pub_'):
        res = rs.getRecommendations('Publication Paper', id, how[nhow.active], G)   
    logging.info('RS Results: '+str(res.shape[0]))
    if res.shape[0] > 0:
        rs_source.data = {
            'data_set_id': res.data_set_id,
            'rs_score': res.score,
            'rs_title': res.title,
            'rs_description': res.description,
        }
    
def callback(attr, old, new):
    byButton = False
    print(old, new)
    curr = source.data['ID'].iloc[new[0]]
    byRow(curr)
source.selected.on_change('indices', callback)

def cHow():
    if byButton:
        return rs_update()
    else:
        return byRow(source.data['ID'].iloc[source.selected.indices[0]])
        
    

menu = [('Publication Paper', 'pub'), ('Dataset', 'data'), ('All', '')]
nmenu = RadioButtonGroup(labels=['Publication', 'Dataset', 'Keyword'], active=0)
how = ['Jaccard', 'Cosine', 'Hopcroft', 'Adamic-Adar']
nhow = RadioButtonGroup(labels=['Jaccard', 'Cosine', 'Hopcroft', 'Adamic-Adar'], active=0)
nhow.on_change('active', lambda attr, old, new: cHow())

search = TextInput(title="Search Archive")
rs_search = AutocompleteInput(title="Recommend by Keyword", completions=all_keywords)

button = Button(label="Search", button_type="warning")
button.on_event(ButtonClick, update)
rs_button = Button(label="Recommend", button_type="success")
rs_button.on_event(ButtonClick, rs_update)

columns = [
    TableColumn(field="ID", title="ID", width=20),
    TableColumn(field="title", title="Title", width=300, formatter=HTMLTemplateFormatter(template=template)),
    TableColumn(field="description", title="Description", width=200, formatter=HTMLTemplateFormatter(template=template))
]
data_table = DataTable(source=source, columns=columns, width=800)
rs_columns = [
    TableColumn(field="data_set_id", title="Data ID", width=20),
    TableColumn(field="rs_score", title="RS Score", width=20),
    TableColumn(field="rs_title", title="Data Title", width=300, formatter=HTMLTemplateFormatter(template=template)),
    TableColumn(field="rs_description", title="Data Description", width=100, formatter=HTMLTemplateFormatter(template=template))
]
rs_table = DataTable(source=rs_source, columns=rs_columns, width=800)
 
controls = column(nmenu, search, button)
rs_controls = column(rs_search, nhow, rs_button)
SE = row(controls, data_table)
RS = row(rs_controls, rs_table)

l = layout([column(title, SE, rs_title, RS)])

curdoc().add_root(l)
curdoc().title = "Rich Context Recommendation System"

show(l)
update()