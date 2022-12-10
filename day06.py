from inputreader import get_lines


def find_first_index_of_unique_signals(length: int, signals: str):
    for index in range(length-1, len(input)):
        if len(set(signals[index-length:index])) == length:
            return index


input = get_lines(6)[0]


print(f'Part 1: {find_first_index_of_unique_signals(4, input)}')
print(f'Part 2: {find_first_index_of_unique_signals(14, input)}')
