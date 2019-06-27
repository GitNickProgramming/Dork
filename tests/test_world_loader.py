import dork.game_utils.world_loader as _mg
import dork.types
import tests.utils

def test_making_items():
    assert "_making_items" in vars(_mg)
    assert isinstance(_mg._making_items("sword"), dork.types.Item)

