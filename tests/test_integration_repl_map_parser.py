"""Testing program for integration between command_parser and map_generator"""
import networkx
import dork.command_parser as _cp



def test_map_gen_returns_graph():
    """create map should make a graph"""
    assert isinstance(_cp.create_map(), networkx.Graph), \
        "Command Parser failed to create Graph type"

def test_load_map_returns_dict():
    """load map should create dict of yaml"""
    assert isinstance(_cp.load_map(), dict),\
         "load_map call doesn't return yaml dictionary as it should"


def test_verify_map():
    """testing verify map works on current map"""
    assert(_cp.verify_map(_cp.load_map())), "Current test map fails to work"
