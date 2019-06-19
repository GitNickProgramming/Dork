# -*- coding: utf-8 -*-
"""Basic tests for the dork map generator
"""

import map_parser.map_generator as map
import networkx as nx
import os
from tests.utils import is_a

def test_map_generator_exists():
    """Test if the map generator has a main"""
    assert "main" in vars(map)


def test_file_path():
    """Test File Path"""
    assert os.path.isfile('jabba') == False
    assert os.path.isfile('./map_parser/yaml/dork.yml') == True

def test_cardinals():
    """ Test Cardinals"""
    is_a(map.CARDINALS, list)
    assert map.CARDINALS == ['north', 'east', 'south', 'west']


def test_nodes():
    """Test Nodes"""
    assert map.nodes is not None
    is_a(map.nodes, list)


def test_edges():
    """Test Edges"""
    assert map.edges is not None
    is_a(map.edges, list)


def test_functions_exist():
    """Test Functions exist"""
    assert "_load_data" in vars(map)
    assert "convert_dict_edges" in vars(map)
    assert "convert_dict_nodes" in vars(map)
    assert "_check_data" in vars(map)
    assert "_generate_map" in vars(map)


def test_load_data():
    """Test Load Data"""
    assert map._load_data() is not None
    assert map._load_data() != ""
    is_a(map._load_data(), dict)


def test_convert_dict_edges():
    """Test Convert Dictionary Edges"""
    assert map.convert_dict_edges(map._load_data()) != None
    assert map.convert_dict_edges(map._load_data()) != ""
    is_a(map.convert_dict_edges(map._load_data()), list)


def test_convert_dict_nodes():
    """Test Convert Dictionary Nodes"""
    assert map.convert_dict_nodes(map._load_data()) is not None
    assert map.convert_dict_nodes(map._load_data()) != ""
    assert map.convert_dict_nodes(map._load_data()) == ['Entrance', 'Boss',
                                                                'Cave', 'Armory',
                                                                'Gold']
    is_a(map.convert_dict_nodes(map._load_data()), list)


def test__check_data():
    """Test Check Data"""
    assert map._check_data(map._load_data()) == True
    assert map._check_data("string") == False
    is_a(map._check_data(map._load_data()), bool)


def test_generate_map():
    """Test Generate Map"""
    assert map._generate_map("", "") is None
    is_a(map._generate_map(map.convert_dict_nodes(map._load_data()),
        map.convert_dict_edges(map._load_data())), nx.classes.graph.Graph)
