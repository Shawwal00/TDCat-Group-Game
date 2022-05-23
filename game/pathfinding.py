# This code is adapted from redblobgames and therefore cannot be claimed as my own (john)
# (although edited slightly to suit this project)

import queue
import pyasge
import heapq
from typing import Dict, List, Tuple, TypeVar, Optional
from game.gamedata import GameData

T = TypeVar('T')
Location = TypeVar('Location')


class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, T]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.elements)[1]


def resolve(xy: pyasge.Point2D, data: GameData, start_loc, hidden_routes: bool):
    """
    Resolves the path needed to get to the destination point.

    Making use of the cost map, a suitable search algorithm should
    be used to create a series of tiles that the ship may pass
    through. These tiles should then be returned as a series of
    positions in world space.

    :param xy: The destination for the ship
    :param data: The game data, needed for access to the game map
    :return: list[pyasge.Point2D]
    """

    # convert point to tile location
    tile_loc = data.game_map.tile(xy)  # Final position
    current_loc = data.game_map.tile(start_loc)  # Your position
    # current_loc = data.game_map.tile(data.player.position)  # Your position
    tile_cost = data.game_map.costs[tile_loc[1]][tile_loc[0]]
    tiles_to_visit = []
    trip_cost = 0

    if tile_cost < 100:
        search, cost = a_star(data, current_loc, tile_loc, hidden_routes)
        trip_cost = cost
        coordinate_list = reconstruct_path(search, current_loc, tile_loc)
        for coordinates in coordinate_list:
            tiles_to_visit.append(data.game_map.world(coordinates))

    # return a list of tile positions to follow
    path = []
    for tile in tiles_to_visit:
        path.append(tile)
    path.append(trip_cost)
    return path


def neighbours(data, current_pos, map_width, map_height) -> List:
    neighbour_list = []

    for new_pos in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        node_pos = (current_pos[0] + new_pos[0], current_pos[1] + new_pos[1])
        if node_pos[0] > map_width - 1 or node_pos[0] < 0 or node_pos[1] > map_height - 1 or node_pos[1] < 0:
            continue
        if data.game_map.costs[node_pos[1]][node_pos[0]] > 100:
            continue
        neighbour_list.append(node_pos)
    return neighbour_list


def reconstruct_path(came_from: Dict[Location, Location], start: Location, goal: Location) -> List[Location]:
    current: Location = goal
    path: List[Location] = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


def heuristic(a, b) -> float:
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star(data, start: Location, goal: Location, hidden_routes):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: Dict[Location, Optional[Location]] = {}
    came_from[start] = None
    cost_so_far: Dict[Location, float] = {}
    cost_so_far[start] = 0
    current_priority = 0

    # use these to make sure you don't go out of bounds when checking neighbours
    map_width = data.game_map.width
    map_height = data.game_map.height

    while not frontier.empty():
        current: Location = frontier.get()
        if current == goal:
            break
        for next in neighbours(data, current, map_width, map_height):
            if hidden_routes and data.game_map.costs[current[1]][current[0]] == 29:
                new_cost = cost_so_far[current] + 1
            else:
                new_cost = cost_so_far[current] + data.game_map.costs[current[1]][current[0]]
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current
                current_priority = priority
    return came_from, current_priority
