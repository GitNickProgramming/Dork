"""Generate players for a room"""

from random import randint
from dork.game_utils.item_factory import main as ItemFactory

def main(i, room) -> dict:
    """Make a player, give them items"""

    new_player = {
        "name": f"placeholder player name {i}",
        "description": f"placeholder player description",
        "locataion": room,
        "items": {},
        "equipped": {}
    }

    for _ in range(randint(1, 3)):
        new_item = ItemFactory("player")
        new_player["items"][new_item["name"]] = new_item

    for key, val in new_player["items"].items():
        new_player["equipped"][key] = val

    return new_player

