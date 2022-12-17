from inputreader import get_lines
from json import loads
from functools import reduce, cmp_to_key

input = get_lines(13)

left = list(map(loads, [input[index]
                        for index in range(len(input)) if (index+1) % 3 == 1]))
right = list(map(loads, [input[index]
                         for index in range(len(input)) if (index+1) % 3 == 2]))


left_right_pairs = list(zip(left, right))


def compare(a, b) -> int:
    match a, b:
        case int(a), int(b):
            return (a > b) - (a < b)
        case list(a), list(b):
            a_b = zip(a, b)
            list_order = next(filter(lambda x: x != 0,
                                     (compare(item_a, item_b)
                                      for item_a, item_b in a_b)),
                              None)
            if list_order != None:
                return list_order
            else:
                return compare(len(a), len(b))
        case list(a), int(b):
            return compare(a, [b])
        case int(a), list(b):
            return compare([a], b)
        case _:
            raise RuntimeError("Unexpected comparison", a, b)


comparison_with_index = enumerate(map(lambda x: compare(*x), left_right_pairs))

increasing_order_index_sum = reduce(lambda count, index_value: count + index_value[0] + 1 if index_value[1] == -1 else count,
                                    comparison_with_index,
                                    0)

print("Part 1:", increasing_order_index_sum)

marker_packets = [[[2]], [[6]]]

sorted_packets = sorted(left + right + marker_packets, key=cmp_to_key(compare))

marker_packet_indexes = map(lambda x: x[0] + 1, filter(lambda x: x[1] in marker_packets,
                                                       enumerate(sorted_packets)))

print("Part 2:", next(marker_packet_indexes) * next(marker_packet_indexes))
