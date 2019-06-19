# -*- coding: utf-8 -*-
"""Generates map from yaml data
"""

from pprint import pprint
import networkx as nx
import yaml
import matplotlib.pyplot as plt


CARDINALS = ["north", "east", "south", "west"]


edges = []
nodes = []


def load_data(file_name_and_path= "./dork/dork.yml"):
    """Loads data from yaml file into data"""
    with open(file_name_and_path) as file:
        data = yaml.safe_load(file.read())

    return data


def convert_dict_edges(data):
    """Convert Dictionary to edges"""
    edges = []
    rooms = data["Rooms"]
    for name in rooms:
        room = rooms[name]
        for direction in CARDINALS:
            if direction in room and room[direction]is not None:
                edges.append((room[direction], name))
    return edges

def convert_dict_nodes(data):
    """Convert Dictionary to Nodes"""
    nodes = []
    rooms = data["Rooms"]
    for name in rooms:
        nodes.append(name)
        room = rooms[name]
    return nodes


def generate_map(nodes, edges):
    """Returns a map from the nodes and edges lists"""
    if nodes and edges:
        nx.empty_graph()
        map_graph = nx.Graph()
        map_graph.add_nodes_from(nodes)
        map_graph.add_edges_from(edges)
        # nx.draw(map_graph, with_labels=True)
        plt.show()
        return map_graph

# def _check_path():
#     data = load_data()
#     rooms = data["Rooms"]
#     room = rooms[name]
#     if direction not in room:
#         print(f"{name} does not have {direction} as a key.")
#     elif room[direction] is None:
#         print(f"There is nothing {direction} of {name}.")
#     elif room[direction] not in rooms:
#         print(f"Going {direction} of {name} leads to an error!")
#     else:
#         other = room[direction]
#         print(f"{other} is {direction} of {name}")

def check_data(data):
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

def main():
    """Runnable main of map_generator, requires correctly formatted yaml file, returns"""
    data = load_data()
    print("loaded this data: ")
    pprint(data)
    print(convert_dict_nodes(load_data()))

    if check_data(load_data()):
        generate_map(convert_dict_nodes(load_data()), convert_dict_edges(load_data()))
        # _check_path()


if __name__ == "__main__":
    main()
