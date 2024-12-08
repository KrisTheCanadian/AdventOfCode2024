"""AoC 7, 2024."""

# Standard library imports
import pathlib
import sys
from itertools import product


def parse_data(puzzle_input: str) -> list[tuple[str, list[str]]]:
    """Parse input."""
    lines = puzzle_input.splitlines()

    data: list[tuple[int, list[int]]] = []
    for line in lines:
        s = line.split(": ")
        target_value = s[0]
        numbers = s[1].split(" ")
        data.append((target_value, numbers))

    return data



def part1(data: list[tuple[str, list[str]]]):
    """Solve part 1."""
    possible_operators: list[str] = ["+", "*"]
    total_calibration_result = 0
    for equation_data in data:
        target_value: int = int(equation_data[0])
        list_of_numbers: list[str] = equation_data[1]
        perm = generate_permutations(possible_operators, len(list_of_numbers) - 1)

        total_calibration_result = total_calibration_result + bruteforce(target_value, list_of_numbers, perm)

    return total_calibration_result

def bruteforce(target_value, list_of_numbers, perm):
    for p in perm:
            total = compute_calibration(target_value, list_of_numbers, p)
            if total > 0:
                return total
    
    return 0

def compute_calibration(target_value, list_of_numbers, operators):
    total = int(list_of_numbers[0])  # Start with the first number
    for i, operator in enumerate(operators):
        next_number = int(list_of_numbers[i + 1])  # Get the next number in the list
        if operator == "*":
            total *= next_number  # Perform multiplication
        elif operator == "#": # perform a concat
            total_str = str(total)
            total = int(total_str + str(next_number))
        else:  # operator == "+"
            total += next_number  # Perform addition
        
        # If total exceeds the target, stop early
        if total > target_value:
            return 0
    
    # Check if we matched the target value
    if total == target_value:
        return target_value
    return 0

            
        
def generate_permutations(operators, length):
    return ["".join(p) for p in product(operators, repeat=length)]

def part2(data):
    """Solve part 2."""
    possible_operators: list[str] = ["+", "*", "#"]
    total_calibration_result = 0
    for equation_data in data:
        target_value: int = int(equation_data[0])
        list_of_numbers: list[str] = equation_data[1]
        perm = generate_permutations(possible_operators, len(list_of_numbers) - 1)

        total_calibration_result = total_calibration_result + bruteforce(target_value, list_of_numbers, perm)

    return total_calibration_result


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
