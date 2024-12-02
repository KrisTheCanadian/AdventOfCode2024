"""AoC 1, 2024: first."""

# Standard library imports
import pathlib
import sys


def parse_data(puzzle_input):
    """Parse input."""
    lines = []
    right = []
    left = []  

    lines = puzzle_input.split("\n")

    for line in lines:
        line = line.strip()
        split = line.split(' ')
        left.append(int(split[0]))
        right.append(int(split[-1]))
    
    return (left, right)

def part1(data):
    left = data[0]
    right = data[1]

    # sort from smallest to greatest
    right.sort()
    left.sort()
    
    distances = []

    for index, _ in enumerate(left):
        distances.append(abs(left[index] - right[index]))
    
    return sum(distances)


def part2(data):
    left = data[0]
    right = data[1]

    similarity = []
    for num in left:
        similarity.append(num * right.count(num))

    return sum(similarity)
    


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
