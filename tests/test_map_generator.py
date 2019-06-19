# -*- coding: utf-8 -*-
"""Basic tests for the dork map generator
"""

import networkx as nx
import os
import map_parser.map_generator as map_graph
from tests.utils import is_a

def test_map_generator_exists():
    """Test if the map generator has a main"""
    assert "main" in vars(map_graph)


def test_file_path():
    """Test File Path"""
    assert os.path.isfile('jabba') is False
    assert os.path.isfile('./map_parser/yaml/dork.yml') is True

def test_cardinals():
    """ Test Cardinals"""
    is_a(map_graph.CARDINALS, list)
    assert map_graph.CARDINALS == ['north', 'east', 'south', 'west']


def test_nodes():
    """Test Nodes"""
    assert map_graph.nodes is not None
    is_a(map_graph.nodes, list)


def test_edges():
    """Test Edges"""
    assert map_graph.edges is not None
    is_a(map_graph.edges, list)


def test_functions_exist():
    """Test Functions exist"""
    assert "load_data" in vars(map_graph)
    assert "convert_dict_edges" in vars(map_graph)
    assert "convert_dict_nodes" in vars(map_graph)
    assert "check_data" in vars(map_graph)
    assert "generate_map" in vars(map_graph)


def testload_data():
    """Test Load Data"""
    assert map_graph.load_data() is not None
    assert map_graph.load_data() != ""
    is_a(map_graph.load_data(), dict)


def test_convert_dict_edges():
    """Test Convert Dictionary Edges"""
    assert map_graph.convert_dict_edges(map_graph.load_data()) != None
    assert map_graph.convert_dict_edges(map_graph.load_data()) != ""
    is_a(map_graph.convert_dict_edges(map_graph.load_data()), list)


def test_convert_dict_nodes():
    """Test Convert Dictionary Nodes"""
    assert map_graph.convert_dict_nodes(map_graph.load_data()) is not None
    assert map_graph.convert_dict_nodes(map_graph.load_data()) != ""
    assert map_graph.convert_dict_nodes(map_graph.load_data()) == ['Entrance', 'Boss',
                                                        'Cave', 'Armory',
                                                        'Gold']
    is_a(map_graph.convert_dict_nodes(map_graph.load_data()), list)


def test_check_data():
    """Test Check Data"""
    assert map_graph.check_data(map_graph.load_data()) == True
    assert map_graph.check_data("string") == False
    is_a(map_graph.check_data(map_graph.load_data()), bool)


def testgenerate_map():
    """Test Generate Map"""
    assert map_graph.generate_map("", "") is None
    is_a(map_graph.generate_map(map_graph.convert_dict_nodes(map_graph.load_data()),
                           map_graph.convert_dict_edges(map_graph.load_data())), 
                           nx.classes.graph.Graph)
