
from inputreader import get_lines

game_rules = {
    'A': {
        'A': 3,
        'B': 6,
        'C': 0,
        'X': 'C',
        'Y': 'A',
        'Z': 'B'
    },
    'B': {
        'A': 0,
        'B': 3,
        'C': 6,
        'X': 'A',
        'Y': 'B',
        'Z': 'C'
    },
    'C': {
        'A': 6,
        'B': 0,
        'C': 3,
        'X': 'B',
        'Y': 'C',
        'Z': 'A'
    }
}

move_value = {
    'A': 1,
    'B': 2,
    'C': 3
}


def get_round_score_part_1(opponent_move: str, my_move: str) -> int:
    move_mapping = {
        'X': 'A',
        'Y': 'B',
        'Z': 'C'
    }
    my_decoded_move = move_mapping[my_move]
    return game_rules[opponent_move][my_decoded_move] + move_value[my_decoded_move]


def get_round_score_part_2(opponent_move: str, round_result: str) -> int:
    my_move = game_rules[opponent_move][round_result]
    return game_rules[opponent_move][my_move] + move_value[my_move]


input = get_lines(2)

first_column, second_column = zip(*(round.split(' ') for round in input))

round_point_part_1 = map(get_round_score_part_1, first_column, second_column)
print(f'Part 1: {sum(round_point_part_1)}')

round_point_part_2 = map(get_round_score_part_2, first_column, second_column)
print(f'Part 2: {sum(round_point_part_2)}')
