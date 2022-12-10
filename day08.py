
from functools import reduce
from inputreader import get_lines

input = get_lines(8)

map_size = (len(input[0]), len(input))


def get_tree_height(x, y) -> int:
    return int(input[y][x])


left_to_right = range(map_size[0])
up_to_down = range(map_size[1])

look_from_north = (((x, y) for y in up_to_down)
                   for x in left_to_right)
look_from_south = (((x, y) for y in reversed(up_to_down))
                   for x in left_to_right)
look_from_west = (((x, y) for x in left_to_right)
                  for y in up_to_down)
look_from_east = (((x, y) for x in reversed(left_to_right))
                  for y in up_to_down)


visible_trees: set[tuple[int, int]] = set()


def get_visible_trees_from_direction(direction, result):
    for line in direction:
        highest_seen_height = -1
        for coordinate in line:
            height = get_tree_height(*coordinate)
            if height > highest_seen_height:
                result.add(coordinate)
                highest_seen_height = height


get_visible_trees_from_direction(look_from_north, visible_trees)
get_visible_trees_from_direction(look_from_south, visible_trees)
get_visible_trees_from_direction(look_from_west, visible_trees)
get_visible_trees_from_direction(look_from_east, visible_trees)


print(f'Part 1: {len(visible_trees)}')


def all_directions_from_coordinate(x, y):
    return (
        ((a, y) for a in range(x+1, map_size[0])),
        ((a, y) for a in range(x-1, -1, -1)),
        ((x, b) for b in range(y+1, map_size[1])),
        ((x, b) for b in range(y-1, -1, -1))
    )


def visible_towards_direction(direction, my_height) -> int:
    visible_distance = 0
    for coordinate in direction:
        visible_distance += 1
        if get_tree_height(*coordinate) >= my_height:
            return visible_distance
    return visible_distance


def calculate_scenic_score(x, y) -> int:
    return reduce(lambda a, b: a*b, (visible_towards_direction(direction, get_tree_height(x, y))
                                     for direction in all_directions_from_coordinate(x, y)))


all_coordinates = ((x, y) for x in left_to_right for y in up_to_down)

maximum_scenic_score = max((calculate_scenic_score(*coordinate)
                            for coordinate in all_coordinates))

print(f'Part 2: {maximum_scenic_score}')
