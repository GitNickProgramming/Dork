# -*- coding: utf-8 -*-
"""Generates map from yaml data
"""
import networkx as nx
import matplotlib.pyplot as plt
import dork.yaml_parser as yml_parse


__all__ = ["generate_map"]


CARDINALS = ["north", "east", "south", "west"]


def generate_map():
    """Returns a map from the nodes and edges lists"""
    data = yml_parse.load("map")
    nodes = _convert_dict_nodes(data)
    edges = _convert_dict_edges(data)
    nx.empty_graph()
    map_graph = nx.Graph()
    map_graph.add_nodes_from(nodes)
    map_graph.add_edges_from(edges)
    # nx.draw(map_graph, with_labels=True)
    plt.show()
    return map_graph


def _convert_dict_edges(data):
    """Convert Dictionary to edges"""
    edges = []
    rooms = data["Rooms"]
    for name in rooms:
        room = rooms[name]
        for direction in CARDINALS:
            if direction in room and room[direction]is not None:
                edges.append((room[direction], name))
    return edges


def _convert_dict_nodes(data):
    """Convert Dictionary to Nodes"""
    nodes = []
    rooms = data["Rooms"]
    for name in rooms:
        nodes.append(name)
    return nodes


def _check_data(data):
    """Tests yaml file to see if it is a correct format"""
    print("\nChecking that 'data' contains a dictionary of rooms... \n")
    if "Rooms" not in data:
        print("No Rooms found.")
        return False

    if not isinstance(data["Rooms"], dict):
        print("Rooms in data was not proper data.")
        return False

    print("Rooms found with proper data.\n")
    return True
