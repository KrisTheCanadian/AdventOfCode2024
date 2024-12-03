"""AoC 3, 2024."""

# Standard library imports
import pathlib
import re
import sys


def parse_data(puzzle_input: str) -> str:
    """Parse input."""
    return puzzle_input


def part1(data: str) -> int:
    """Solve part 1."""
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    matches = re.findall(pattern, data)

    sum: int = 0

    for match in matches:
        x, y = match
        sum = sum + (int(x) * int(y))

    return sum


def part2(data: str) -> int:
    """Solve part 2."""
    sum = 0
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    matches = []
    for match in re.finditer(pattern, data):
        x = int(match.group(1))  # Convert X to an integer
        y = int(match.group(2))  # Convert Y to an integer
        start = match.start(0)
        end = match.end(0)
        matches.append(((x, y), start, end))

    pattern_for_do_and_dont = r"do((?:n't)?)\(\)"

    for match in re.finditer(pattern_for_do_and_dont, data):
        group0 = match.group(0)
        start = match.start(0)
        end = match.end(0)
        if group0 == 'do()':
            matches.append(((float('inf'), float('inf')), start, end))
        else:
            matches.append(((float('-inf'), float('-inf')), start, end))

    matches.sort(key=lambda m: m[1])  # Sort by the start position of each match

    # for (x, y), start, end in matches:
    #     print(f"mul({x},{y}) at {start}-{end}")

    need_to_skip = False
    for (x, y), start, end in matches:

        
        if x == float('-inf'):
            # print(f"mul({x},{y}) at {start}-{end}. Set need_to_skip to True")
            need_to_skip = True
            continue

        if x == float('inf'):
            need_to_skip = False
            # print(f"mul({x},{y}) at {start}-{end}. Set need_to_skip to False")
            continue

        if need_to_skip:
            # print(f"mul({x},{y}) at {start}-{end} skipped...")
            continue

        # print(f"mul({x},{y}) at {start}-{end}. Has been added to the sum.")
        sum = sum + (x * y)
        # print(f"sum: {sum}")
        
        

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
