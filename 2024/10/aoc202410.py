"""AoC 10, 2024."""

# Standard library imports
import pathlib
import sys


def parse_data(puzzle_input: str) -> list[str]:
    """Parse input."""
    return puzzle_input.splitlines()


def part1(data: list[str]):
    """Solve part 1."""
    
    zeros: list[tuple[int, int]] = [] # we want to store the positions (x, y) of all the zeros
    nines: dict[tuple[int, int], set[tuple[int, int]]] = {} # we will store all the nines we visited successfully here
    for x, line in enumerate(data):
        for y, digit in enumerate(line):
            
            # we check if its a digit if its not we skip it
            if not digit.isdigit():
                continue
            
            if digit == "0":
                zeros.append((x, y))
            
    for zero in zeros:
        perform_walk(data, zero, nines, zero)
        
    # calculate the score of each trailhead
    total = 0
    for k, v in nines.items():
        total += len(v)
    
    return total

def check_bounds(index, lower_bound, upper_bound):
    """
    Checks if the given index is within the specified bounds.
    
    :param index: The index to check
    :param lower_bound: The lower bound (inclusive)
    :param upper_bound: The upper bound (inclusive)
    :return: True if the index is within bounds, False otherwise
    """
    return lower_bound <= index <= upper_bound

def perform_walk(data: list[str], target: tuple[int, int], nines: dict[tuple[int, int], set[tuple[int, int]]], trailhead: tuple[int, int]):
    # we want to find all our neighbours (up, down, right, left) which is 1 more than us
    target_value = int(data[target[0]][target[1]])

    if target_value == 9:
        if trailhead not in nines:
            nines[trailhead] = set()
        nines[trailhead].add(target)
        return

    neighbors: list[tuple[int, int]] = []
    
    up = (target[0] + 1, target[1]) # add (1, 0) to target for up
    down = (target[0] - 1, target[1]) # add (-1, 0) to target for down
    right = (target[0], target[1] + 1) # add (0, 1) to target for right
    left = (target[0], target[1] - 1) # add (0, -1) to target for left
    
    rows = len(data)
    cols = len(data[0]) if rows > 0 else 0
    
    if check_bounds(up[0], 0, rows - 1) and check_bounds(up[1], 0, cols - 1):
        value = data[up[0]][up[1]]
        if value.isdigit() and int(value) == target_value + 1:
            neighbors.append(up)
    
    if check_bounds(down[0], 0, rows - 1) and check_bounds(down[1], 0, cols - 1):
        value = data[down[0]][down[1]]
        if value.isdigit() and int(value) == target_value + 1:
            neighbors.append(down)
    
    if check_bounds(right[0], 0, rows - 1) and check_bounds(right[1], 0, cols - 1):
        value = data[right[0]][right[1]]
        if value.isdigit() and int(value) == target_value + 1:
            neighbors.append(right)
    
    if check_bounds(left[0], 0, rows - 1) and check_bounds(left[1], 0, cols - 1):
        value = data[left[0]][left[1]]
        if value.isdigit() and int(value) == target_value + 1:
            neighbors.append(left)
        
    for neighbor in neighbors:
        perform_walk(data, neighbor, nines, trailhead)

def part2(data):
    """Solve part 2."""


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
