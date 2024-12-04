"""AoC 4, 2024."""

# Standard library imports
import pathlib
import sys


def parse_data(puzzle_input: str) -> list[list[str]]:
    """Parse input."""
    # we are going to make an array of chars
    lines: list[str] = puzzle_input.splitlines()
    array: list[list[str]] = []
    for line in lines:
        chars: list[str] = [char for char in line]
        array.append(chars)
    
    return array

def part1(data: list[list[str]]) -> int:
    """Solve part 1."""
    sum = 0

    indexes_of_x: list[tuple[int, int]] = []
    for x in range(len(data)):
        for y in range(len(data[0])):
            if data[x][y] == "X":
                indexes_of_x.append((x, y))
    
    for x, y in indexes_of_x:
        sum += scan_neighboring_cells(x, y, data)

    return sum

def scan_neighboring_cells(x: int, y: int, data: list[list[str]], letter: str = "M", direction: tuple[int, int] | None = None) -> int:
    """Scan neighboring cells for the given letter."""
    directions = None
    if letter == 'M':
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    else:
        directions = [direction]

    sum_matches = 0

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(data) and 0 <= ny < len(data[0]):
            if data[nx][ny] == letter:
                if letter == "M":
                    sum_matches += scan_neighboring_cells(nx, ny, data, "A", (dx, dy))
                elif letter == "A":
                    sum_matches += scan_neighboring_cells(nx, ny, data, "S", (dx, dy))
                elif letter == "S":
                    sum_matches += 1

    return sum_matches

def check_neighbor_similarity(x: int, y: int, data: list[list[str]], letter: str = "M") -> int:
    """Scan neighboring cells for the given letter."""
    directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]

    # bounds check
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        # Check if the neighboring cell is within the bounds of the data array
        if not (0 <= nx < len(data) and 0 <= ny < len(data[0])):
            return 0

    tl: str = data[x-1][y-1]
    tr: str = data[x-1][y+1]
    bl: str = data[x+1][y-1]
    br: str = data[x+1][y+1]

    target_letters = ["M", "S"]

    if tl not in target_letters or tr not in target_letters or bl not in target_letters or br not in target_letters:
        return 0
        
    if tl == br:
        return 0
    
    if bl == tr:
        return 0

    return 1


def part2(data: list[list[str]]) -> int:
    """Solve part 2."""
    sum = 0

    indexes_of_a: list[tuple[int, int]] = []
    for x in range(len(data)):
        for y in range(len(data[0])):
            if data[x][y] == "A":
                indexes_of_a.append((x, y))
    
    for x, y in indexes_of_a:
        sum += check_neighbor_similarity(x, y, data)

    return sum

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse_data(puzzle_input)
    yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
