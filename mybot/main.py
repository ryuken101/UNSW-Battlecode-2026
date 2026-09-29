import helper as unswbc
from helper import Direction, EdgeType
import random

ct: unswbc.Controller
game: unswbc.Game

# Seed so we get the same random generator every time.
random.seed(0)

DIRS = Direction.get_direction_list()
_nbr_cache = {}

# Checking for wall
def neighbours(pos):
    """Safe (direction, tile) moves from pos. Cached for the turn so repeated searches are cheap.
    Returns a list of moves that are safe (direction, tile)
    _nbr_cache remembers the answer for each position so the same tile isn't re-checked several times in one turn. 
    It's cleared at the start of each turn because the board changes between turns. 
    This matters because since computation is paid for in points."""
    k = (pos.x, pos.y)
    out = _nbr_cache.get(k)

    if out is None:
        out = []
        current_pos = ct.get_tile(pos)
        if current_pos is not None: 
            for d in DIRS: 
                edge = here.get_edge(d)
                if not edge.ispassable() or edge.is_portal():
                    continue
                nxt = ct.get_tile(pos.add_dir(d))
                if nxt is not None and nxt.get_dragon() is None:
                    out.append((d, nxt))
        _nbr_cache[k] = out
    return out




def execute_turn() -> None:
    """Step onto the first open neighbouring tile."""
    here = ct.get_position()
    here_tile = ct.get_tile(here)

    directions = Direction.get_direction_list()
    random.shuffle(directions)

    for direction in directions:
        
        edge = here_tile.get_edge(direction).get_edge_type()
        if edge == EdgeType.KELP:
            continue

        ahead = ct.get_tile(here.add_dir(direction))
        if ahead.get_dragon() is not None:
            continue

        ct.output_log("Moving in", direction.value)
        ct.make_move(direction)
        return

    ct.make_move(Direction.NORTH)

def main() -> None:
    global ct, game
    ct, game = unswbc.init()

    while unswbc.update(ct, game):
        execute_turn()
        unswbc.end_turn()

if __name__ == "__main__":
    main()
