from inputreader import get_lines
from typing import Callable
from operator import mul, add
from math import prod


class Monkey:
    item_worry_levels: list[int]
    operation: Callable[[int], int]
    throw_test_divisibility_factor: int
    target_monkey: dict[bool, int]
    number_of_inspections = 0

    def __init__(self) -> None:
        self.target_monkey = {}

    def throw_test(self, worry_level) -> bool:
        return worry_level % self.throw_test_divisibility_factor == 0

    def evaluate_items(self):
        new_worry_levels = map(self.operation, self.item_worry_levels)

        self.item_worry_levels = list(new_worry_levels)
        self.number_of_inspections += len(self.item_worry_levels)

    def get_targets_and_worry_levels(self) -> list[tuple[int, int]]:
        return [(self.target_monkey[self.throw_test(worry_level)],
                 worry_level)
                for worry_level in self.item_worry_levels]


def generate_operation(input: tuple[str, str, str]) -> Callable[[int], int]:
    operator_mapper = {"*": mul, "+": add}

    def operation(worry_level: int) -> int:
        def arg_mapper(x): return worry_level if x == "old" else int(x)
        first_arg, operator, second_arg = input
        return operator_mapper[operator](arg_mapper(first_arg), arg_mapper(second_arg))

    return operation


def parse_monkey(monkey_lines: list[str]) -> Monkey:
    monkey = Monkey()
    for line in monkey_lines:
        match line.split():
            case ["Starting", "items:", *items]:
                monkey.item_worry_levels = [
                    int(item.rstrip(",")) for item in items]
            case ["Operation:", "new", "=", *operation]:
                monkey.operation = generate_operation(tuple(operation))
            case ["Test:", "divisible", "by", argument]:
                monkey.throw_test_divisibility_factor = int(argument)
            case ["If", "true:", "throw", "to", "monkey", index]:
                monkey.target_monkey[True] = int(index)
            case ["If", "false:", "throw", "to", "monkey", index]:
                monkey.target_monkey[False] = int(index)

    return monkey


def execute_round(monkeys: list[Monkey], relax_after_evaluation=True):
    for monkey in monkeys:
        monkey.evaluate_items()
        if relax_after_evaluation:
            monkey.item_worry_levels = list(
                map(lambda x: x // 3, monkey.item_worry_levels))
        for target, level in monkey.get_targets_and_worry_levels():
            monkeys[target].item_worry_levels.append(level)
        monkey.item_worry_levels = []


def keep_worry_under_control(monkeys: list[Monkey], max_worry: int):
    for monkey in monkeys:
        monkey.item_worry_levels = list(
            map(lambda x: x % max_worry, monkey.item_worry_levels))


def calculate_monkey_business(monkeys: list[Monkey]):
    two_most_active_monkeys = sorted(
        monkeys, key=lambda x: x.number_of_inspections)[-2:]
    return prod(monkey.number_of_inspections
                for monkey in two_most_active_monkeys)


input = get_lines(11)

lines_by_monkey = [input[start:end] for (start, end) in zip(
    range(0, len(input) - 5, 7), range(7, len(input) + 2, 7))]

monkeys_part_1 = [parse_monkey(monkey_lines)
                  for monkey_lines in lines_by_monkey]

for _ in range(20):
    execute_round(monkeys_part_1)

print("Part 1:", calculate_monkey_business(monkeys_part_1))

monkeys_part_2 = [parse_monkey(monkey_lines)
                  for monkey_lines in lines_by_monkey]

max_worry = prod(monkey.throw_test_divisibility_factor
                 for monkey in monkeys_part_2)

for _ in range(10000):
    execute_round(monkeys_part_2, relax_after_evaluation=False)
    keep_worry_under_control(monkeys_part_2, max_worry)

print("Part 2:", calculate_monkey_business(monkeys_part_2))
