from inputreader import get_lines
from typing import NamedTuple

input = get_lines(5)

input_separator_index = next(index for (index, item)
                             in enumerate(input) if item == '')

initial_condition_input = input[:input_separator_index]
instructions_input = input[input_separator_index+1:]


def generate_input_stacks(initial_condition_input: list[str]) -> list[list[str]]:
    stack_lines = initial_condition_input[::-1][1:]

    transposed_stack_lines = list(map(list, zip(*stack_lines)))

    return [list(filter(lambda x: x != ' ', column))
            for (index, column) in enumerate(transposed_stack_lines)
            if ((index-1) % 4 == 0)]


stacks = generate_input_stacks(initial_condition_input)


class Instruction(NamedTuple):
    amount: int
    origin: int
    destination: int


def parse_instruction(line: str) -> Instruction:
    split_line = line.split(' ')
    return Instruction(int(split_line[1]), int(split_line[3])-1, int(split_line[5])-1)


instructions = [parse_instruction(line)
                for line in instructions_input]


def run_crate_mover(stacks: list[list[str]], instructions: list[Instruction], is_advanced: bool) -> list[list[str]]:
    stacks = [stack[:] for stack in stacks]
    transfer_order = 1 if is_advanced else -1

    for instruction in instructions:
        stacks[instruction.destination].extend(
            stacks[instruction.origin][-instruction.amount:][::transfer_order])
        del stacks[instruction.origin][-instruction.amount:]
    return stacks


final_state_part_1 = run_crate_mover(stacks, instructions, is_advanced=False)

print(f'Part 1: {"".join([stack[-1] for stack in final_state_part_1])}')

final_state_part_2 = run_crate_mover(stacks, instructions, is_advanced=True)

print(f'Part 2: {"".join([stack[-1] for stack in final_state_part_2])}')
