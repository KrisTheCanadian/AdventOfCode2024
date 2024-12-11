"""AoC 11, 2024."""

# Standard library imports
from copy import deepcopy
import pathlib
import sys


def parse_data(puzzle_input: str) -> list[int]:
    """Parse input."""
    # let's convert the puzzle input into a list of numbers (stones)
    return [int(stone) for stone in puzzle_input.split()]


def part1(data: list[int]):
    """Solve part 1."""
    # Rule 1: if the stone is engraved with 0 then replaced with 1
    # Rule 2: if the store is engraved with an even number of digits, then the stone is split
    #         where the left half of the digits are on the left stone, vise versa
    #         and leading zeros are destroyed
    # Rule 3: if not Rule 1 and not Rule 2 then old stone's number * 2024
    stones = deepcopy(data)
    new_stones = []
    blinks = 25
    for _ in range(blinks):
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:
                st = str(stone)
                l = int(len(str(stone)) / 2)
                # split the digits
                left_stone = int(st[:l])
                right_stone = int(st[l:])
                new_stones.extend([left_stone, right_stone])
            else:
                new_stones.append(stone * 2024)
        
        
        stones = new_stones
        new_stones = []

    return len(stones)


def part2(data: list[int]):
    """Solve part 2."""
    # Rule 1: if the stone is engraved with 0 then replaced with 1
    # Rule 2: if the store is engraved with an even number of digits, then the stone is split
    #         where the left half of the digits are on the left stone, vise versa
    #         and leading zeros are destroyed
    # Rule 3: if not Rule 1 and not Rule 2 then old stone's number * 2024
    
    # dynamic programming needed
    stones = deepcopy(data)
    new_stones = []
    blinks = 25
    for _ in range(blinks):
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:
                st = str(stone)
                l = int(len(str(stone)) / 2)
                # split the digits
                left_stone = int(st[:l])
                right_stone = int(st[l:])
                new_stones.extend([left_stone, right_stone])
            else:
                new_stones.append(stone * 2024)
        
        
        stones = new_stones
        new_stones = []

    return len(stones)


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
