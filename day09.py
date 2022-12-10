from inputreader import get_lines
from itertools import chain, repeat, accumulate, tee
from functools import reduce
from collections.abc import Iterable
from operator import add, sub

input = get_lines(9)


def generate_movement_vectors(instruction) -> Iterable[tuple[int, int]]:
    match instruction.split():
        case ['U', steps]:
            return repeat((0, 1), int(steps))
        case ['D', steps]:
            return repeat((0, -1), int(steps))
        case ['R', steps]:
            return repeat((1, 0), int(steps))
        case ['L', steps]:
            return repeat((-1, 0), int(steps))
        case _:
            raise RuntimeError(f'Unexpected instruction {instruction}')


head_vectors = chain.from_iterable(generate_movement_vectors(instruction)
                                   for instruction in input)


def point_operation(ab, xy, func) -> tuple[int, int]:
    (a, b), (x, y) = ab, xy
    return (func(a, x), func(b, y))


def add_vector_to_point(ab, xy) -> tuple[int, int]:
    return point_operation(ab, xy, add)


def get_diff_vector(ab, xy) -> tuple[int, int]:
    return point_operation(ab, xy, sub)


def compare(a, b) -> int:
    return (a > b) - (a < b)


head_coordinates_part_1, head_coordinates_part_2 = tee(
    accumulate(head_vectors, add_vector_to_point))


def tail_movement_vector(tail_position, head_position) -> tuple[int, int]:
    (dx, dy) = get_diff_vector(head_position, tail_position)
    within_range = abs(dx) <= 1 and abs(dy) <= 1

    if within_range:
        return (0, 0)
    else:
        return point_operation((dx, dy), (0, 0), compare)


def move_tail(tail_position, head_position) -> tuple[int, int]:
    return add_vector_to_point(tail_position,
                               tail_movement_vector(tail_position,
                                                    head_position))


tail_coordinates = accumulate(
    head_coordinates_part_1, move_tail, initial=(0, 0))

print(f'Part 1: {len(set(tail_coordinates))}')

ninth_tail_coordinates = reduce(lambda xth_tail, _: accumulate(xth_tail, move_tail, initial=(0, 0)),
                                range(9),
                                head_coordinates_part_2)

print(f'Part 2: {len(set(ninth_tail_coordinates))}')
