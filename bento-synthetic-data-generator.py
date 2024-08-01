#!/usr/bin/env python
# coding: utf-8

# In[1]:


from dataclasses import dataclass, field, fields, asdict
import yaml
from typing import List
from collections import namedtuple, defaultdict, Counter
import random
import pandas as pd
import sys
from openpyxl import load_workbook, Workbook
import pprint
import os
import argparse
import logging
from datetime import datetime, timedelta
import uuid
import copy

# In[2]:


#DEFINE CLASSES
#dataclass for model properties
@dataclass
class ModelProperty:
    name: str = field(default = "")
    desc: str = field(default = "")
    value_type: str = field(default = "")
    value_list: List[str] = field(default_factory=list)
    synthetic_value_list: List[str] = field(default_factory=list)
    units: List[str] = field(default_factory=list)
    pattern: str = field(default = "")
    url: str = field(default = "")
    req: bool = field(default = False)
    private: bool = field(default = False)
    minimum: str = field(default = "")
    maximum: str = field(default = "")
    exclusiveMinimum:  str = field(default = "")
    exclusiveMaximum:  str = field(default = "")
    
    def emit_value(self, test_pop):
        if test_pop and self.synthetic_value_list:
            property_data_value = random.choice(self.synthetic_value_list)
            return property_data_value
        if not test_pop and self.synthetic_value_list:
            #property_data_value = random.choice(self.synthetic_value_list)
            property_data_value = self.synthetic_value_list.pop()
            return property_data_value
        if self.value_list:
            property_data_value = random.choice(self.value_list)
            return property_data_value
        if self.value_type == 'string':
            base_list = ["a_bene_placito",
                         "barba_crescit_caput_nescit",
                         "cacatum_non_est_pictum",
                         "damnant_quod_non_intellegunt","e_causa_ignota",
                         "faber_est_suae_quisque_fortunae",
                         "Gallia_est_omnis_divisa_in_partes_tres","haec_olim_meminisse_iuvabit",
                         "id_quod_plerumque_accidit","imperium_in_imperio","labor_ipse_voluptas",
                         "Macte_animo_Generose_puer_sic_itur_ad_astra","nanos_gigantum_humeris_insidentes",
                         "nascentes_morimur_finisque_ab_origine_pendet","O_Tite_tute_Tati_tibi_tanta_tyranne_tulisti",
                         "Obedientia_civium_urbis_felicitas","pace_tua","saltus_in_demonstrando",
                         "salus_in_arduis","sapiens_qui_prospicit","scientia_et_labor","scientia_et_sapientia",
                         "scientia_imperii_decus_et_tutamen","scientia,_aere_perennius","scientiae_cedit_mare",
                         "scientiae_et_patriae"]
            property_data_value = random.choice(base_list)
            return property_data_value
        if self.value_type == 'number':
            if type(self.minimum) == float and type(self.maximum) == float:
                property_data_value = random.uniform(self.minimum, self.maximum)
            elif type(self.minimum) == int and type(self.maximum) == int:
                property_data_value = random.uniform(float(self.minimum), float(self.maximum))
            else:
                property_data_value = random.uniform(10.0,1000.0)
            property_data_value = round(property_data_value, 2)
            return property_data_value
        if self.value_type == 'boolean':
            property_data_value = random.choice([True, False])
            return property_data_value
        if self.value_type == 'integer':
            if type(self.minimum) == int and type(self.maximum) == int:
                property_data_value = random.randint(self.minimum, self.maximum)
            else:
                property_data_value = random.randint(10,1000)
            return property_data_value
        if self.value_type == 'date' or self.value_type == 'datetime':
            start_date = datetime(2019, 1, 1)
            end_date = datetime(2023, 12, 31)
            days_between = (end_date - start_date).days
            random_days = random.randint(0, days_between)
            property_data_value = start_date + timedelta(days=random_days)
            return property_data_value


# In[3]:


#dataclass for model nodes
@dataclass
class ModelNode:
    name: str = field(default = "")
    properties: List[ModelProperty] = field(default_factory=list)


# In[4]:


#dataclass for the ends of a model relationship
@dataclass
class ModelEnds:
    source_node: ModelNode
    destination_node: ModelNode
    multiplicity: str = field(default = "")


# In[5]:


#dataclass for model relationships
@dataclass
class ModelEdge:
    name: str
    ends_list: List[ModelEnds] = field(default_factory=list)
    properties_list: List[ModelProperty] = field(default_factory=list)


# In[6]:


#dataclass for mock data nodes
@dataclass
class DataNode:
    node_id: str
    parent_node_id_list: list
    child_node_id_list: list
    node_type: str
    node_attributes: dict
    edge_id_list: list


# In[7]:


#dataclass for mock data relationships
@dataclass
class DataEdge:
    edge_id: str
    edge_type: str
    edge_attributes: dict
    source_node: DataNode
    destination_node: DataNode


# In[8]:


@dataclass
class Graph:
    dict_of_data_nodes: defaultdict(list)
    dict_of_data_edges: {}
    
    def print_data(self, node_type = 'all'):
        if node_type == 'all':
            for node_type_key in data_graph.dict_of_data_nodes:
                node_values_dict = defaultdict(list)
                df = pd.DataFrame()
                for node in data_graph.dict_of_data_nodes[node_type_key]:
                    node_values_dict['type'].append(node.node_type)
                
                if  node.parent_node_id_list:
                    node_values_dict['parent_id'].append(node.parent_node_id_list[0])

                node_values_dict['node_id'].append(node.node_id)
                for node_prop in node.node_attributes:
                    node_values_dict[node_prop].append(node.node_attributes[node_prop])
                
                for node_values_key in node_values_dict:
                    df[node_values_key] = node_values_dict[node_values_key]
                
                file_name = node_type_key + ".csv"
                df.to_csv(file_name)
            
            return
        else:
            if node_type in data_graph.dict_of_data_nodes:
                node_values_dict = defaultdict(list)
                df = pd.DataFrame()
                for node in data_graph.dict_of_data_nodes[node_type]:
                    node_values_dict['type'].append(node.node_type)
                
                if  node.parent_node_id_list:
                    node_values_dict['parent_id'].append(node.parent_node_id_list[0])
                
                node_values_dict['node_id'].append(node.node_id)
                
                for node_prop in node.node_attributes:
                    node_values_dict[node_prop].append(node.node_attributes[node_prop])
                
                for node_values_key in node_values_dict:
                    df[node_values_key] = node_values_dict[node_values_key]
                
                file_name = node_type_key + ".csv"
                df.to_csv(file_name)
                return
            else:
                print("node type not found in graph.")
                return
    
    def fill_graph(self, listOfProps, model_nodes_dict, model_props_dict):
        for node_type in self.dict_of_data_nodes:
            listOfNodeProps = model_nodes_dict[node_type].properties
            listOfDataNodes = self.dict_of_data_nodes[node_type]
            created_node_id_list = []
            created_node_list = []
            for data_node in listOfDataNodes:
                if data_node.node_id not in created_node_id_list:
                    created_node_id_list.append(data_node.node_id)
                    for prop in listOfNodeProps:
                        if prop.name in listOfProps[data_node.node_type]:
                            if model_props_dict[prop.name].emit_value(True) != None:
                                data_node.node_attributes[prop.name] = model_props_dict[prop.name].emit_value(False)

                            else:
                                # if the value type can no be identified, then change type to string
                                base_string_list = ["a_bene_placito",
                                "barba_crescit_caput_nescit",
                                "cacatum_non_est_pictum",
                                "damnant_quod_non_intellegunt","e_causa_ignota",
                                "faber_est_suae_quisque_fortunae",
                                "Gallia_est_omnis_divisa_in_partes_tres","haec_olim_meminisse_iuvabit",
                                "id_quod_plerumque_accidit","imperium_in_imperio","labor_ipse_voluptas",
                                "Macte_animo_Generose_puer_sic_itur_ad_astra","nanos_gigantum_humeris_insidentes",
                                "nascentes_morimur_finisque_ab_origine_pendet","O_Tite_tute_Tati_tibi_tanta_tyranne_tulisti",
                                "Obedientia_civium_urbis_felicitas","pace_tua","saltus_in_demonstrando",
                                "salus_in_arduis","sapiens_qui_prospicit","scientia_et_labor","scientia_et_sapientia",
                                "scientia_imperii_decus_et_tutamen","scientia,_aere_perennius","scientiae_cedit_mare",
                                "scientiae_et_patriae"]
                                property_data_string_value = random.choice(base_string_list)
                                data_node.node_attributes[prop.name] = property_data_string_value
                    created_node_list.append(data_node)
                else:
                    for created_node in created_node_list:
                        if data_node.node_id == created_node.node_id:
                            data_node.node_attributes = created_node.node_attributes

            
        return
    
    def get_dict_of_data_nodes(self):
        return self.dict_of_data_nodes
    
    def get_dict_of_data_edges(self):
        return self.dict_of_data_edges
    
    def get_in_degree(self, input_node_id):
        for key in self.dict_of_data_nodes:
            for node in dict_of_data_nodes[key]:
                if node.node_id == input_node_id:
                    return len(node.parent_node_id_list)
    
    def get_out_degree(self, input_node_id):
        for key in self.dict_of_data_nodes:
            for node in dict_of_data_nodes[key]:
                if node.node_id == input_node_id:
                    return len(node.child_node_id_list)
    
    def summary(self):
        summary = {}
        summary['Nodes Summary'] = {}
        summary['Edges Summary']  = {}
        
        for node_type in self.dict_of_data_nodes:
            node_count = len(dict_of_data_nodes[node_type])
            summary['Nodes Summary'].update({node_type: node_count})
        
        edge_type_list = []
        for edge in dict_of_data_edges.values():
            edge_type_list.append(edge.edge_type)
        edge_type_counter = Counter(edge_type_list)
        for edge_type, edge_type_count in edge_type_counter.items():
            summary['Edges Summary'].update({edge_type: edge_type_count})
        
        return summary
            
            


# In[9]:


######BEGIN READ SECTION######
print('BEGIN READ SECTION')
dict_of_model_properties = {}
dict_of_model_nodes = {}
model_graph = {}


# In[10]:

parser = argparse.ArgumentParser()
parser.add_argument('configuration_file')
args = parser.parse_args()
# configuration_files = 'configuration_files_bento.yaml'
configuration_files = args.configuration_file
with open(configuration_files) as f:
    configuration_files = yaml.load(f, Loader=yaml.FullLoader)

ID_FILE = configuration_files['ID_FILE']
with open(ID_FILE) as f:
    id_field_data = yaml.load(f, Loader=yaml.FullLoader)

# In[11]:


#READ MODEL FILES AND FILE WITH SYNTHETIC VALUES
#FOR BENTO
NODE_FILE = configuration_files['NODE_FILE']
PROP_FILE = configuration_files['PROP_FILE']
SYNTHETIC_DATA_FILE = configuration_files['SYNTHETIC_DATA_FILE']


# In[12]:


synthetic_values_df = pd.read_excel(io = SYNTHETIC_DATA_FILE,
                        sheet_name = "Sheet1",
                        engine = "openpyxl",
                        keep_default_na = False)


# In[13]:


with open(PROP_FILE) as f:
    property_data = yaml.load(f, Loader=yaml.FullLoader)
for property_name in property_data['PropDefinitions'].keys():
    try:
        property_value_type = property_data['PropDefinitions'][property_name]['Type']
    except:
        try:
            property_value_type = property_data['PropDefinitions'][property_name]['Enum']
        except:
            property_value_type = 'string'
    name = property_name
    desc = ""
    req= ""
    value_type = ""
    value_list = []
    synthetic_value_list = []
    units = []
    private = ""
    pattern = ""
    url = ""
    minimum = ""
    maximum = ""
    exclusiveMinimum = ""
    exclusiveMaximum = ""
    #print(property_value_type)
    if type(property_value_type) is str:
        name = property_name
        value_type = property_value_type
        if 'Desc' in property_data['PropDefinitions'][property_name]:
            desc = property_data['PropDefinitions'][property_name]['Desc']
        if 'Req' in property_data['PropDefinitions'][property_name]:
            req = property_data['PropDefinitions'][property_name]['Req']
        if 'Private' in property_data['PropDefinitions'][property_name]:
            private = property_data['PropDefinitions'][property_name]['Private']
        if 'minimum' in property_data['PropDefinitions'][property_name]:
            minimum = property_data['PropDefinitions'][property_name]['minimum']
        if 'maximum' in property_data['PropDefinitions'][property_name]:
            maximum = property_data['PropDefinitions'][property_name]['maximum']
        if property_name in synthetic_values_df.columns:
            synthetic_value_list = [x for x in synthetic_values_df[property_name].tolist() if x != '']
            
    if type(property_value_type) is list:
        value_type = "list"
        if "NON_PERMISSIVE_VALUE" not in configuration_files.keys():
            value_list = property_value_type
        else:
            if not configuration_files["NON_PERMISSIVE_VALUE"]:
                value_list = property_value_type
        #add section on reading the url to create a value list if property_value_type contains a url.
        if 'Desc' in property_data['PropDefinitions'][property_name]:
            desc = property_data['PropDefinitions'][property_name]['Desc']
        if 'Req' in property_data['PropDefinitions'][property_name]:
            req = property_data['PropDefinitions'][property_name]['Req']
        if 'Private' in property_data['PropDefinitions'][property_name]:
            private = property_data['PropDefinitions'][property_name]['Private']
        if property_name in synthetic_values_df.columns:
            synthetic_value_list = [x for x in synthetic_values_df[property_name].tolist() if x != '']
            
    if type(property_value_type) is dict:
        if 'Desc' in property_data['PropDefinitions'][property_name]:
            desc = property_data['PropDefinitions'][property_name]['Desc']
        if 'value_type' in property_value_type:
            value_type = property_value_type['value_type']
        if 'units' in property_value_type:
            units = property_value_type['units']
        if 'pattern' in property_value_type:
            pattern = property_value_type['pattern']
            value_type = "regex"
        if 'Req' in property_data['PropDefinitions'][property_name]:
            req = property_data['PropDefinitions'][property_name]['Req']
        if 'Private' in property_data['PropDefinitions'][property_name]:
            private = property_data['PropDefinitions'][property_name]['Private']
        if 'minimum' in property_data['PropDefinitions'][property_name]:
            minimum = property_data['PropDefinitions'][property_name]['minimum']
        if 'maximum' in property_data['PropDefinitions'][property_name]:
            maximum = property_data['PropDefinitions'][property_name]['maximum']
        if property_name in synthetic_values_df.columns:
            synthetic_value_list = [x for x in synthetic_values_df[property_name].tolist() if x != '']
        
    dict_of_model_properties[property_name] = ModelProperty(name = name, desc = desc, 
                                                                value_type = value_type, value_list = value_list,
                                                                units = units, url = url, req = req, private = private, minimum = minimum, maximum = maximum,
                                                                exclusiveMinimum = exclusiveMinimum, exclusiveMaximum = exclusiveMaximum, synthetic_value_list = synthetic_value_list)

# In[14]:


with open(NODE_FILE) as f:
    node_data = yaml.load(f, Loader=yaml.FullLoader)


# In[15]:


nodes = node_data['Nodes']

for node_name in nodes.keys():
    #print(node_name, nodes[node_name]['Props'])
    if nodes[node_name]['Props']:
        property_list = [dict_of_model_properties[property_name] for property_name in nodes[node_name]['Props']]
    else:
        property_list = []
    dict_of_model_nodes[node_name] = ModelNode(name = node_name, properties = property_list)


# In[16]:


edges = node_data['Relationships']

for edge_name in edges.keys():
    Ends_list = []
    Property_list = []
    edge_multiplicity = edges[edge_name]['Mul']
    
    for edge_pair in edges[edge_name]['Ends']:
        source_node = edge_pair['Src']
        destination_node = edge_pair['Dst']
        if 'Mul' in edge_pair:
            edge_multiplicity = edge_pair['Mul']
        Ends_list.append(ModelEnds(source_node = dict_of_model_nodes[source_node], destination_node = dict_of_model_nodes[destination_node], multiplicity = edge_multiplicity))
        
    
    if 'Props' in edges[edge_name] and edges[edge_name]['Props']:
        property_list = [dict_of_model_properties[property_name] for property_name in edges[edge_name]['Props']]
    else:
        property_list = []
    
    model_graph[edge_name] = ModelEdge(name = edge_name, ends_list = Ends_list, properties_list = Property_list)
#END READ MODEL FILES
print('END READ SECTION')
######END READ SECTION######


# In[17]:


######BEGIN SPAWN SECTION######
print('BEGIN SPAWN SECTION')
dict_of_data_nodes = defaultdict(list)
dict_of_data_edges = {}


# In[18]:


#READ DATA SPECS FILE
#FOR BENTO
DATA_SPEC_FILE = configuration_files['DATA_SPEC_FILE']
def synthetic_node_id_list_func(id_field_data, src_node_type, node_counter, synthetic_values_df):
    if id_field_data['Properties']['id_fields'][src_node_type] in synthetic_values_df.columns:
                        synthetic_node_id_list = [x for x in synthetic_values_df[id_field_data['Properties']['id_fields'][src_node_type]].tolist() if x != '']
                        #if len(synthetic_node_id_list) >= node_counter:
                        return synthetic_node_id_list
    return list()

# In[19]:


with open(DATA_SPEC_FILE) as f:
    data_spec = yaml.load(f, Loader=yaml.FullLoader)


# In[20]:


#Create head data node object
for head_node in data_spec['HeadNode']:
    head_node_type = head_node['name']
    if head_node_type in data_spec['IncludeNodes'].keys():
        logging.error('HeadNode ' + head_node_type + 'is in the IncludeNodes.')
        sys.exit()
    head_node_count = head_node['count']
    id_prefix = head_node['Prefix']
    dst_node_type = head_node_type
    # random a set of id without duplicate
    node_id_number_list = random.sample(range(10**5, 10**6), head_node_count + 1)
    head_node_index = 0
    synthetic_node_id_list = synthetic_node_id_list_func(id_field_data, head_node_type, head_node_count, synthetic_values_df)
    for count in range(head_node_count):
        # node_id = id_prefix + "_" + str(random.randint(10**5, 10**6))
        if len(synthetic_node_id_list) > 0:
            node_id = synthetic_node_id_list.pop()
        else:
            node_id = id_prefix + "-" + str(node_id_number_list[head_node_index])# for bento
        head_node_index += 1
        parent_node_id_list = []
        child_node_id_list = []
        node_type = head_node_type
        node_attributes = {}
        data_node = DataNode(node_id = node_id, parent_node_id_list = parent_node_id_list, child_node_id_list = child_node_id_list,
                             node_type = node_type, node_attributes = {}, edge_id_list = [])
        dict_of_data_nodes[head_node_type].append(data_node)

edge_specs = data_spec['RelationshipSpecs']


# In[21]:


for dst_node_type in edge_specs.keys():
    dst_data_nodes_list = dict_of_data_nodes[dst_node_type]


# In[22]:


includeNodes = data_spec['IncludeNodes']


# In[23]:


def findEdgeType(node_data, src_node_type, dst_node_type):
    for edge_type in node_data['Relationships']:
        for ends in node_data['Relationships'][edge_type]['Ends']:
            if ends['Src'] == src_node_type and ends['Dst'] == dst_node_type:
                return edge_type
    return None
    


# In[24]:

#Function to create a skeleton data graph.
#Create a skeleton data graph.
def SpawnNodes():
    created_children = []
    children = []
    for dst_node_type in edge_specs.keys():
        if dst_node_type in dict_of_data_nodes and dst_node_type not in created_children:
            dst_data_nodes_list = dict_of_data_nodes[dst_node_type]
            # for dst_data_node in dst_data_nodes_list:
            for src_node_type in edge_specs[dst_node_type].keys():
                # print(dst_node_type, src_node_type)
                node_counter = includeNodes[src_node_type]['NodeCount']
                if "Exact_count" in edge_specs[dst_node_type][src_node_type].keys():
                        node_counter = edge_specs[dst_node_type][src_node_type]['Exact_count']
                node_distribution = edge_specs[dst_node_type][src_node_type]['SrcNodeCount']
                try:
                    id_prefix = includeNodes[src_node_type]['Prefix']
                except Exception as e:
                    id_prefix = ""
                # random a set of id without duplicate
                node_id_number_list = random.sample(range(10**5, 10**6), node_counter)
                old_node_id_list = []
                for id in node_id_number_list:
                    old_node_id_list.append(id)
                old_node_id_dict = {}
                node_index = 0
                parent_node_index = 0
                #parent_node_length = len(dst_data_nodes_list)
                if dst_node_type in includeNodes.keys():
                    parent_node_length = includeNodes[dst_node_type]['NodeCount']
                else:
                    parent_node_length = len(dst_data_nodes_list)
                step = int(node_counter / parent_node_length)
                if parent_node_length > node_counter: #fix the parent node count should be bigger than children node count
                    step = 1

                many_to_many_rel = False
                many_to_many = False
                #if "ManyToMany" in edge_specs[dst_node_type][src_node_type].keys():
                #    many_to_many = edge_specs[dst_node_type][src_node_type]['ManyToMany']
                #    many_to_many_list.append(dst_node_type)
                # if the distribution is random
                #print(node_counter, parent_node_length)
                
                if "ManyToManyCount" in includeNodes[src_node_type].keys():
                    node_distribution = 'random'
                    many_to_many = True
                    node_counter = includeNodes[src_node_type]['ManyToManyCount']
                    expand_list = node_id_number_list
                    for i in range(len(node_id_number_list), node_counter):
                        expand_list.append(random.choice(node_id_number_list))
                    node_id_number_list = expand_list
                    if "ManyToMany" in edge_specs[dst_node_type][src_node_type].keys():
                        many_to_many_rel = edge_specs[dst_node_type][src_node_type]["ManyToMany"]


                if node_distribution == 'random':
                    node_counter_list = range(node_counter)
                    random_split_points = random.sample(node_counter_list, parent_node_length - 1)
                    random_split_points.sort()
                    random_split_points_index = 0
                
                    
                synthetic_node_id_list = synthetic_node_id_list_func(id_field_data, src_node_type, node_counter, synthetic_values_df)
                
                if node_distribution == 'random' and not many_to_many_rel and many_to_many:
                    node_counter_list = range(len(old_node_id_list))
                    random_split_points = random.sample(node_counter_list, parent_node_length - 1)
                    random_split_points.sort()
                    random_split_points_index = 0
                    for index in range(0, len(old_node_id_list)):
                        old_node_id = ""
                        if len(synthetic_node_id_list) > 0:
                            old_node_id = synthetic_node_id_list.pop()
                        elif id_prefix != "":
                            old_node_id = id_prefix + "-" + str(old_node_id_list[index])
                        else:
                            old_node_id = old_node_id_list[index]
                        old_node_id_dict[str(old_node_id)] = dst_data_nodes_list[parent_node_index].node_id
                        if index < len(random_split_points):
                            if index == random_split_points[random_split_points_index]:
                                random_split_points_index += 1
                                parent_node_index += 1


                node_id_list = []
                if src_node_type in dict_of_data_nodes.keys():
                    dict_of_data_nodes[src_node_type] = [copy.deepcopy(x) for x in dict_of_data_nodes[src_node_type]]
                for count in range(0, node_counter):
                    if node_distribution == 'fixed' and not many_to_many:
                        if "one_to_one_count" in edge_specs[dst_node_type][src_node_type].keys():
                            if count > edge_specs[dst_node_type][src_node_type]['one_to_one_count']:
                                step = (node_counter - edge_specs[dst_node_type][src_node_type]['one_to_one_count'])/edge_specs[dst_node_type][src_node_type]['many_to_one_count']
                        if node_index % step == 0 and node_index != 0:
                            parent_node_index += 1
                    elif node_distribution == 'random':
                        #print(node_index)
                        if random_split_points_index < len(random_split_points):
                            if node_index == random_split_points[random_split_points_index]:
                                random_split_points_index += 1
                                parent_node_index += 1
                    if parent_node_index > parent_node_length - 1:
                            parent_node_index = parent_node_length - 1
                    # node_id = id_prefix + "_" + str(random.randint(10**5, 10**6))
                    if len(synthetic_node_id_list) > 0:
                        node_id = synthetic_node_id_list.pop()
                    elif id_prefix != "":
                        node_id = id_prefix + "-" + str(node_id_number_list[node_index])
                    else:
                        node_id = node_id_number_list[node_index]
                    edge_id = "edge" + "_" + str(uuid.uuid4())
                    if src_node_type not in children:
                        node_index += 1
                        parent_node_id_list = []
                        edge_id_list = [edge_id]
                        if not many_to_many_rel and many_to_many:
                            parent_node_id_list.append(old_node_id_dict[node_id])
                        else:
                            parent_node_id_list.append(dst_data_nodes_list[parent_node_index].node_id)
                        child_node_id_list = []
                        node_type = src_node_type
                        src_data_node = DataNode(node_id = node_id, parent_node_id_list = parent_node_id_list, child_node_id_list = child_node_id_list,
                                                 node_type = node_type, node_attributes = {}, edge_id_list = edge_id_list) #source node created.
                        if len(dict_of_data_nodes[src_node_type]) > 0:
                            for created_node in dict_of_data_nodes[src_node_type]:
                                if node_id == created_node.node_id and not many_to_many_rel:
                                    src_data_node = created_node
                                else:
                                    node_id_list.append(node_id)
                        dict_of_data_nodes[src_node_type].append(src_data_node) #source node added to the dict of nodes.         
                        dst_data_nodes_list[parent_node_index].child_node_id_list.append(node_id) #add created source node to the child nodes list for dst node.

                    #elif src_node_type in children:
                    elif src_node_type in children: #and not many_to_many_rel:
                        dict_of_data_nodes[src_node_type][node_index].parent_node_id_list.append(dst_data_nodes_list[parent_node_index].node_id)                  
                        dict_of_data_nodes[src_node_type][node_index].edge_id_list.append(edge_id)
                        node_index += 1
                    edge_type = findEdgeType(node_data, src_node_type, dst_node_type)
                    # edge_type = edge_specs[dst_node_type][src_node_type]['EdgeType']
                    edge_attributes = {}
                    data_edge = DataEdge(edge_id = edge_id, edge_type = edge_type, source_node = src_data_node, 
                                     destination_node = dst_data_nodes_list[parent_node_index], edge_attributes = edge_attributes) #edge created.
                    dict_of_data_edges[edge_id] = data_edge #edge added to the dict of edges.
                    #node_index += 1
                if many_to_many:
                    if count == includeNodes[src_node_type]['ManyToManyCount'] - 1:
                        children.append(src_node_type)
                else:
                    if count == includeNodes[src_node_type]['NodeCount'] - 1:
                        children.append(src_node_type)
            created_children.append(dst_node_type)
            
    data_graph = Graph(dict_of_data_nodes = dict_of_data_nodes, dict_of_data_edges = dict_of_data_edges)
    return data_graph


# In[25]:


#Create skeleton data graph
data_graph = SpawnNodes()


# In[26]:


#Examine skeleton data graph
# data_graph.summary()
summary = data_graph.summary()
pprint.pprint(summary)
print('END SPAWN SECTION')
######END SPAWN SECTION######


# In[27]:



relationship_node_dict = {}
node_id_field_dict = {}
node_list = []
for parent_id in data_spec['RelationshipSpecs']:
    for node_id in data_spec['RelationshipSpecs'][parent_id]:
        relationship_node = {}
        relationship_node['parent_id'] = []
        relationship_node['parent_id_field'] = []
        relationship_node['node_id'] = node_id
        relationship_node['parent_id'].append(parent_id)
        if node_id in id_field_data['Properties']['id_fields']:
            relationship_node['node_id_field'] = id_field_data['Properties']['id_fields'][node_id]
        else:
            relationship_node['node_id_field'] ='node_id'
        if parent_id in id_field_data['Properties']['id_fields']:
            relationship_node['parent_id_field'].append(id_field_data['Properties']['id_fields'][parent_id])
        else:
            relationship_node['parent_id_field'].append('parent_id')
        if node_id not in relationship_node_dict.keys():
            relationship_node_dict[node_id] = relationship_node
        else:
            relationship_node_dict[node_id]['parent_id'].append(relationship_node['parent_id'][0])
            relationship_node_dict[node_id]['parent_id_field'].append(relationship_node['parent_id_field'][0])

for node_type in data_graph.dict_of_data_nodes:
    if node_type in id_field_data['Properties']['id_fields']:
        node_id_field_dict[node_type] = id_field_data['Properties']['id_fields'][node_type]


# In[28]:
def GetParentIDField(node_type, index):
    if node_type in relationship_node_dict:
        return relationship_node_dict[node_type]['parent_id'][index]+'.'+relationship_node_dict[node_type]['parent_id_field'][index]
    else:
        return 'parent_id'
def GetNodeIDField(node_type):
    if node_type in node_id_field_dict:
        return node_id_field_dict[node_type]
    else:
        return 'node_id'


# In[29]:


######BEGIN FILL SECTION######
print('BEGIN FILL SECTION')
includePropsList = data_spec['IncludeProperties']


# In[30]:


data_graph.fill_graph(listOfProps = includePropsList, 
                      model_nodes_dict = dict_of_model_nodes, 
                      model_props_dict = dict_of_model_properties)
print('END FILL SECTION')
######END FILL SECTION######


# In[31]:


######PRINT DATA FILES######
print('PRINT DATA FILES')
for node_type in data_graph.dict_of_data_nodes:
    node_values_dict = defaultdict(list)
    df = pd.DataFrame()
    position = 0
    for node in data_graph.dict_of_data_nodes[node_type]:
        parent_node_type_list = []
        for parent_node_type in edge_specs.keys():
            for source_node_type in edge_specs[parent_node_type].keys():
                if source_node_type == node_type:
                    parent_node_type_list.append(parent_node_type)
        #print(node_type)
        #print(parent_node_type_list)
        edge_specs[dst_node_type]
        node_values_dict['type'].append(node.node_type)
        '''if node.node_type == "data_file":
            
            if node.node_attributes['data_file_type'] == 'Clinical Report':
                #node.parent_node_id_list = [item if "SPECIMEN" not in item else None for item in node.parent_node_id_list]
                print(node)
            
            if node.node_attributes['data_file_type'] != 'Clinical Report':
                #node.parent_node_id_list = [item if "SUBJECT" not in item else None for item in node.parent_node_id_list]
                #print(node)
                print(dict_of_data_edges[node.edge_id_list[0]].destination_node)'''
        if node.parent_node_id_list:
            index = 0
            created_parent_list = []
            for parent_node_id in node.parent_node_id_list:
                parent_id_field = dict_of_data_edges[node.edge_id_list[index]].destination_node.node_type + "." + GetNodeIDField(dict_of_data_edges[node.edge_id_list[index]].destination_node.node_type)
                node_values_dict[parent_id_field].append(parent_node_id) #parent
                if dict_of_data_edges[node.edge_id_list[index]].destination_node.node_type not in created_parent_list:
                    created_parent_list.append(dict_of_data_edges[node.edge_id_list[index]].destination_node.node_type)
                index += 1
            for ct in created_parent_list:
                parent_node_type_list.remove(ct)
            if len(parent_node_type_list)>0:
                for pt in parent_node_type_list:
                    full_pt = pt + "." + GetNodeIDField(pt)
                    node_values_dict[full_pt].append(None)
                
        if GetNodeIDField(node_type) not in node.node_attributes:
            node_values_dict[GetNodeIDField(node_type)].append(node.node_id) #node
        if GetNodeIDField(node_type) in node.node_attributes: # and GetNodeIDField(node_type) not in synthetic_values_df.keys():
            # if the user adds the id field into the data spec document accidentally
            del node.node_attributes[GetNodeIDField(node_type)]
            node_values_dict[GetNodeIDField(node_type)].append(node.node_id) #node
        for node_prop in node.node_attributes:
            # print(node_type)
            # print(node.node_attributes)
            node_values_dict[node_prop].append(node.node_attributes[node_prop])
        position+=1
    for node_values_key in node_values_dict:
        #print(len(node_values_dict[node_values_key]))
        df[node_values_key] = node_values_dict[node_values_key]
        #print(node_values_dict[node_values_key])
    #df = pd.DataFrame({ key:pd.Series(value) for key, value in  node_values_dict.items() })
    
    file_name = configuration_files['OUTPUT_FOLDER'] + node_type + ".tsv"
    if not os.path.exists(configuration_files['OUTPUT_FOLDER']):
        os.mkdir(configuration_files['OUTPUT_FOLDER'])
    df.to_csv(file_name, sep = "\t", index = False)


# In[32]:


######VALIDATE DATA FILES######

print('VALIDATE DATA FILES')
from data_loader import DataLoader
from icdc_schema import ICDC_Schema
from neo4j import GraphDatabase
from props import Props


# In[33]:

file_list = [f for f in os.listdir(configuration_files['OUTPUT_FOLDER']) if f.endswith('.tsv')]
for i in range(0, len(file_list)):
    file_list[i] = configuration_files['OUTPUT_FOLDER'] + file_list[i]
props = Props(configuration_files['ID_FILE'])
schema = ICDC_Schema([configuration_files['NODE_FILE'], configuration_files['PROP_FILE']], props)
loader = DataLoader(None, schema)
fileValidationResult = loader.validate_files(False, file_list, 1000000000, 'tmp', True)


# In[34]:


def relationshipValidation(dict_of_data_edges, node_data, includeNodes):
    for edge in dict_of_data_edges.values():
        mul = node_data['Relationships'][edge.edge_type]['Mul']
        prefix = includeNodes[edge.source_node.node_type]['Prefix']
        child_node_id_list = []
        #print(edge.destination_node)
        for child_node_id in edge.destination_node.child_node_id_list:
            try:
                if prefix in child_node_id:
                    child_node_id_list.append(child_node_id)
            except Exception as e:
                a=1
        if mul == 'one_to_one' and len(child_node_id_list) > 1:
            logging.error(edge.source_node.node_type + ' ' + 'one_to_one relationship failed, parent already has a child!')
            return False
    return True


# In[35]:

relationshipValidationResult = relationshipValidation(dict_of_data_edges, node_data, includeNodes)
delete_error_file = True
if "DELETE_ERROR_FILE" in configuration_files.keys():
    delete_error_file = configuration_files["DELETE_ERROR_FILE"]

if delete_error_file:
    if not relationshipValidationResult or not fileValidationResult:
        print('Validation fail, delete all files inside the data folder.')
        mydir = os.path.abspath(configuration_files['OUTPUT_FOLDER'])
        filelist = [ f for f in os.listdir(mydir) if f.endswith(".tsv") ]
        for f in filelist:
            os.remove(os.path.join(mydir, f))
    else:
        print('Validation success')
else:
    if not relationshipValidationResult or not fileValidationResult:
        print('Validation fail')
    else:
        print('Validation success')
