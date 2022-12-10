def get_lines(puzzleIndex: int) -> list[str]:
    with open(f'input/input{puzzleIndex:02d}.txt') as file:
        return file.read().splitlines()
