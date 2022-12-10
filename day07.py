from inputreader import get_lines

input = get_lines(7)

root_directory = {'children': {}, 'absolute_name': '/'}
current_directory = {}

all_directories = {'/': root_directory}

for line in input:
    match line.split(' '):
        case ["$", "cd", '/']:
            current_directory = root_directory
        case ["$", "cd", ".."]:
            current_directory = current_directory['parent']
        case ["$", "cd", destination]:
            current_directory = current_directory['children'][destination]
        case ["$", "ls"]:
            pass
        case ["dir", name]:
            child_absolute_name = f'{current_directory["absolute_name"]}{name}/'
            child = {'children': {}, 'parent': current_directory,
                     'absolute_name': child_absolute_name}

            current_directory['children'][name] = child
            all_directories[child_absolute_name] = child

        case [size, name]:
            current_directory['children'][name] = {'size': int(size)}


def compute_directory_size(directory: dict) -> int:
    match directory:
        case {'children': children}:
            directory['size'] = sum(
                map(compute_directory_size, children.values()))
            return directory['size']
        case {'size': size}:
            return size
        case _:
            raise RuntimeError(f'Unexpected node format: {directory}')


compute_directory_size(root_directory)

directory_sizes_smaller_than_100000: list[int] = [dir['size'] for dir in all_directories.values()
                                                  if dir['size'] <= 100000]

print(f'Part 1: {sum(directory_sizes_smaller_than_100000)}')

DISK_SIZE = 70000000
TARGET_FREE_SPACE = 30000000

disk_used = root_directory['size']
free_space = DISK_SIZE - disk_used

space_to_free = TARGET_FREE_SPACE - free_space

target_for_deletion = min([dir['size'] for dir in all_directories.values()
                           if dir['size'] >= space_to_free])

print(f'Part 2: {target_for_deletion}')
