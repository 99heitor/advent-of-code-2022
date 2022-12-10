from inputreader import get_lines
from string import ascii_letters

type_priority_map = {type: priority for (type,
                     priority) in zip(ascii_letters, range(1, 53))}


def find_common_letters(*args: str) -> set[str]:
    if (len(args) == 1):
        return {letter for letter in args[0]}
    else:
        return {letter for letter in find_common_letters(*args[:-1]) if letter in args[-1]}


input = get_lines(3)

group_compartments = ((line[:len(line)//2], line[len(line)//2:])
                      for line in input)

common_type_list = [find_common_letters(*compartments).pop()
                    for compartments in group_compartments]

common_type_priority_list = [type_priority_map[type]
                             for type in common_type_list]

print(f'Part 1: {sum(common_type_priority_list)}')

elf_groups = [(input[index], input[index+1], input[index+2])
              for index in range(len(input)-1) if index % 3 == 0]

badge_types = [find_common_letters(*group).pop()
               for group in elf_groups]

badge_priority_list = [type_priority_map[badge_type]
                       for badge_type in badge_types]

print(f'Part 2: {sum(badge_priority_list)}')
