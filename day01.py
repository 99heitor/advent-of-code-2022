from inputreader import get_lines

input = get_lines(1) + ['']

calory_list_by_elf: list[list[int]] = []
current_elf_calories: list[int] = []
for line in input:
    if line == '':
        calory_list_by_elf.append(current_elf_calories)
        current_elf_calories = []
    else:
        current_elf_calories.append(int(line))

calory_sum_by_elf = map(sum, calory_list_by_elf)

sorted_calories = sorted(calory_sum_by_elf, reverse=True)
print(f'Part 1: {sorted_calories[0]}')
print(f'Part 2: {sum(sorted_calories[:3])}')
