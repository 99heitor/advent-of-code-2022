from inputreader import get_lines
from typing import NamedTuple
import re

input = get_lines(4)


class SectionRange(NamedTuple):
    start: int
    end: int

    def __contains__(self, other: 'SectionRange') -> bool:
        return self.start <= other.start and self.end >= other.end

    def intersects(self, other: 'SectionRange') -> bool:
        return self.end >= other.start and other.end >= self.start


split_input = [re.split('[-,]', line) for line in input]

section_range_pair_list = [(SectionRange(int(start1), int(end1)), SectionRange(int(start2), int(end2)))
                           for [start1, end1, start2, end2] in split_input]

number_of_redundant_sections = sum([first in second or second in first
                                    for (first, second) in section_range_pair_list])

print(f'Part 1: {number_of_redundant_sections}')

number_of_intersecting_sections = sum([first.intersects(second)
                                       for (first, second) in section_range_pair_list])

print(f'Part 2: {number_of_intersecting_sections}')
