from inputreader import get_lines
from collections.abc import Iterable
from itertools import chain, accumulate

input = get_lines(10)


def get_instruction_computation(instruction: str) -> Iterable[int]:
    match (instruction.split()):
        case ["noop"]:
            return (0,)
        case ["addx", value]:
            return (0, int(value))
        case _:
            raise RuntimeError(f'Unexpected instruction {instruction}')


cycle_transition_register_deltas = chain.from_iterable(
    get_instruction_computation(instruction) for instruction in input)

register_value_sequence = list(accumulate(cycle_transition_register_deltas,
                                          initial=1))

signal_strength_sum = sum(map(lambda x: x * register_value_sequence[x-1],
                              (20, 60, 100, 140, 180, 220)))


print(f'Part 1: {signal_strength_sum}')

pixels = ['⬜️' if abs((pixel % 40) - x_register) <= 1 else '⬛️'
          for (pixel, x_register) in enumerate(register_value_sequence)]

scan_lines = [pixels[start:end]
              for (start, end) in zip(range(0, 201, 40), range(40, 241, 40))]

rendered_pixels = "\n".join("".join(line) for line in scan_lines)

print('Part 2:')
print(rendered_pixels)
