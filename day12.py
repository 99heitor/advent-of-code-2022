from inputreader import get_lines
from math import floor
from typing import Iterator, NamedTuple, Optional, Callable

input = get_lines(12)


def value(i: complex) -> str:
    return input[floor(i.imag)][floor(i.real)]


def height(i: complex) -> int:
    match value(i):
        case 'S':
            return 0
        case 'E':
            return 26
        case _:
            return ord(value(i)) - 96


all_coordinates = [complex(x, y) for x in range(len(input[0]))
                   for y in range(len(input))]


def get_start_end() -> tuple[complex, complex]:
    start, end = None, None
    for coord in all_coordinates:
        match value(coord):
            case 'S':
                start = coord
            case 'E':
                end = coord
        if start != None and end != None:
            return (start, end)
    raise RuntimeError("Couldn't find start and end in the input")


def possible_steps_from(coord: complex) -> Iterator[complex]:
    def is_valid_coordinate(candidate: complex) -> bool:
        return candidate.real >= 0 and candidate.real < len(input[0]) and candidate.imag >= 0 and candidate.imag < len(input)
    cardinal_directions = [1, -1, 1j, -1j]
    candidates = map(lambda x: x + coord, cardinal_directions)
    return filter(is_valid_coordinate, candidates)


def going_up(from_coord: complex, to_coord: complex) -> bool:
    return height(to_coord) - height(from_coord) <= 1


def going_down(from_coord: complex, to_coord: complex) -> bool:
    return height(from_coord) - height(to_coord) <= 1


def valid_steps_from(coord: complex, visited: set[complex], step_condition: Callable[[complex, complex], bool]) -> Iterator[complex]:
    possible_steps = list(possible_steps_from(coord))

    def is_valid(possible_target: complex):
        return (step_condition(coord, possible_target)) and possible_target not in visited

    return filter(is_valid, possible_steps)


start, end = get_start_end()


class Path(NamedTuple):
    coord: complex
    previous: Optional['Path']


def flatten_path(path: Optional[Path]) -> list[complex]:
    flat_path: list[complex] = []
    while path != None:
        flat_path.append(path.coord)
        path = path.previous
    return flat_path


def breadth_first_search(frontier: list[Path], end_condition: Callable[[complex], bool], step_condition: Callable[[complex, complex], bool], visited=set()) -> Optional[Path]:
    while frontier != []:
        new_frontier = []
        for path in frontier:
            next_steps = valid_steps_from(path.coord, visited, step_condition)
            for step in next_steps:
                if end_condition(step):
                    return Path(step, path)
                else:
                    new_frontier.append(Path(step, path))
                    visited.add(step)
        frontier = new_frontier


def find_shortest_path(start_from: complex, end_condition: Callable[[complex], bool], step_condition: Callable[[complex, complex], bool]) -> Optional[Path]:
    return breadth_first_search([Path(start_from, None)], end_condition, step_condition, set())


path_to_end = find_shortest_path(start, lambda x: x == end, going_up)

print('Part 1:', len(flatten_path(path_to_end)) - 1)

path_to_height_a = find_shortest_path(
    end, lambda x: value(x) == 'a', going_down)

print('Part 2:', len(flatten_path(path_to_height_a)) - 1)
