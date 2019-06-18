
import map.map_generator as map
import networkx as nx 
import os

def test_map_generator_exists():
    assert "main" in vars(map)

def test_file_path():
    assert os.path.isfile('jabba') == False
    assert os.path.isfile('./map/yaml/dork.yml') == True

def test_cardinals():
    assert type(map.CARDINALS) is list
    assert map.CARDINALS == ['north', 'east', 'south', 'west']

def test_nodes():
    assert map.nodes is not None
    assert type(map.nodes) is list
    

def test_edges():
    assert map.edges is not None
    assert type(map.edges) is list

    
def test_functions_exist():
    assert "_load_data" in vars(map)
    assert "convert_dict_edges" in vars(map)
    assert "convert_dict_nodes" in vars(map)
    assert "_check_data" in vars(map)
    assert "_generate_map" in vars(map) 
   
def test_load_data():
    assert map._load_data() != None
    assert map._load_data() != ""
    assert type(map._load_data()) is dict

def test_convert_dict_edges():
    assert map.convert_dict_edges(map._load_data()) != None
    assert map.convert_dict_edges(map._load_data()) != ""
    assert type(map.convert_dict_edges(map._load_data())) is list

def test_convert_dict_nodes():
    assert map.convert_dict_nodes(map._load_data()) != None
    assert map.convert_dict_nodes(map._load_data()) != ""
    assert map.convert_dict_nodes(map._load_data()) == ['Entrance', 'Boss', 'Cave', 'Armory', 'Gold']
    assert type(map.convert_dict_nodes(map._load_data())) is list

def test__check_data():
    assert map._check_data(map._load_data()) == True
    assert map._check_data("string") == False
    assert type(map._check_data(map._load_data())) is bool

def test_generate_map():
    assert map._generate_map("", "") is None 
    assert type(map._generate_map(map.convert_dict_nodes(map._load_data()), map.convert_dict_edges(map._load_data()))) is nx.classes.graph.Graph


