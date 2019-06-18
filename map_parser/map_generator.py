
import networkx as nx 
import yaml
from pprint import pprint
import matplotlib.pyplot as plt

CARDINALS = ["north", "east", "south", "west"]

edges = []
nodes = []


def _load_data(file_name_and_path="./map_parser/yaml/dork.yml"):
    with open(file_name_and_path) as file:
        data = yaml.safe_load(file.read())

    return data

def convert_dict_edges(data):
    edges = []
   
    rooms = data["Rooms"]
    for name in rooms:  

        room = rooms[name]
        for direction in CARDINALS:
            if direction in room and room[direction]is not None:
                edges.append((room[direction], name))
    
    return edges

def convert_dict_nodes(data):
    nodes = []
  

    rooms = data["Rooms"]
    for name in rooms:
        nodes.append(name)
        room = rooms[name]

    return nodes

def _generate_map(nodes,edges):
    if nodes and edges:
        nx.empty_graph()
        map_graph = nx.Graph()
        map_graph.add_nodes_from(nodes)
        map_graph.add_edges_from(edges)
        # nx.draw(map_graph, with_labels=True)
        plt.show()

        return map_graph

# def _check_path():
#     data = _load_data()
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

def _check_data(data):
  
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
    data = _load_data()
    print("loaded this data: ")
    pprint(data)

    if _check_data(_load_data()):
            _generate_map(convert_dict_nodes( _load_data()), convert_dict_edges( _load_data()))
            # _check_path()
    
    print(convert_dict_nodes(data))
    print(convert_dict_edges(data))

  
if __name__ == "__main__":
    main()