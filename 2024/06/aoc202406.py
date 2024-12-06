"""AoC 6, 2024."""

# Standard library imports
import pathlib
import sys


def parse_data(puzzle_input: str):
    """Parse input."""
    return puzzle_input.splitlines()


def part1(map: list[str]):
    """Solve part 1."""
    guard_position: tuple[int, int] = find_guard_position_on_map(map)
    guard_direction: tuple[int, int] = (-1, 0) # starts heading north
    
    visited: set[tuple[int, int]] = set()
    
    while not is_guard_out_of_map(map, guard_position):
        # check space above guard
        if is_space_infront_guard_obstructed(map, guard_position, guard_direction):
            # turn 90 degrees right (change of direction)
            guard_direction = change_guard_direction(guard_direction)
        else:
            # walk forward (in current direction) and mark that location with an X
            guard_position = walk_one_step_in_direction(guard_position, guard_direction, visited)
        
    return len(visited)
    
def change_guard_direction(guard_direction: tuple[int, int]):
    """Change direction 90 degrees to the right."""
    x, y = guard_direction
    # print(f"guard changed direction by 90 degrees from ({x}, {y}) to ({y}, {-x})")
    return (y, -x)
    
def walk_one_step_in_direction(guard_position: tuple[int, int], guard_direction: tuple[int, int], visited: set[tuple[int, int]]) -> tuple[int, int]:
    x, y = guard_position
    visited.add((x, y))
    
    nx, ny = guard_position[0] + guard_direction[0], guard_position[1] + guard_direction[1]
    # print(f"guard moved from ({x}, {y}) to ({nx}, {ny})")
    return (nx, ny)
    
def is_space_infront_guard_obstructed(map: list[str], guard_position: tuple[int, int], guard_direction: tuple[int, int]) -> bool:
    x, y = (guard_position[0] + guard_direction[0], guard_position[1] + guard_direction[1])
    
    # Handles the bounds check as well
    if is_guard_out_of_map(map, (x, y)):
        return False
    
    if map[x][y] == "#":
        return True
    
    return False

def find_guard_position_on_map(map: list[str]) -> tuple[int, int]:
    # find the guard
    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y] == '^':
                return (x, y)
    
    return (-1, -1)

def is_guard_out_of_map(map: list[str], guard_position: tuple[int, int]) -> bool:
    x, y = guard_position
    
    if not (0 <= x < len(map)):
        return True
    
    if not (0 <= y < len(map[0])):
        return True
    
    return False


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
