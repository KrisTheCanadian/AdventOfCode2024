"""AoC 13, 2024."""

# Standard library imports
import pathlib
import re
import sys

import numpy as np


def parse_data(puzzle_input: str) -> dict[int, list[tuple[int, int], tuple[int, int], tuple[int, int]]]:
    """Parse input."""
    lines = puzzle_input.splitlines()
    id = 0
    # we need to save the button a, button b, prize position
    puzzles: dict[int, list[tuple[int, int], tuple[int, int], tuple[int, int]]] = {}
    button_a: tuple[int, int]
    button_b: tuple[int, int]
    prize_location: tuple[int, int]
    for line in lines:
        pattern = r"X([+-]?\d+), Y([+-]?\d+)"
        if "Button A" in line:
            match = re.search(pattern, line)
            x_value = int(match.group(1))
            y_value = int(match.group(2))
            button_a = (x_value, y_value)
        elif "Button B" in line:
            match = re.search(pattern, line)
            x_value = int(match.group(1))
            y_value = int(match.group(2))
            button_b = (x_value, y_value)
        elif "Prize" in line:
            pattern = r"X=([+-]?\d+), Y=([+-]?\d+)"
            match = re.search(pattern, line)
            
            x_value = int(match.group(1))
            y_value = int(match.group(2))
            
            prize_location = (x_value, y_value)

            puzzles[id] = [button_a, button_b, prize_location]
            id += 1
    
    return puzzles

def part1(puzzles: dict[int, list[tuple[int, int], tuple[int, int], tuple[int, int]]]) -> int:
    """Solve part 1."""
    # costs 3 tokens for button A
    # costs 1 token for button B
    button_a_cost = 3
    button_b_cost = 1
    
    total_button_a_pressed = 0
    total_button_b_pressed = 0
    
    solutions: dict[int, tuple[int, int]] = {}
    for puzzle_id, puzzle in puzzles.items():
        button_a, button_b, prize_location = puzzle
        solution = solve_system_with_min_cost(button_a, button_b, prize_location, button_a_cost, button_b_cost)
        if solution:
            A_value, B_value = solution
            solutions[puzzle_id] = (A_value, B_value)
            total_button_a_pressed += A_value
            total_button_b_pressed += B_value
        else:
            solutions[puzzle_id] = None
    
    return (button_a_cost * total_button_a_pressed) + (button_b_cost * total_button_b_pressed)
    
def solve_system_with_min_cost(button_a, button_b, prize_location, button_a_cost, button_b_cost):
    """Solve the system of equations for A and B, minimizing cost if there are multiple solutions."""
    A = np.array([[button_a[0], button_b[0]], [button_a[1], button_b[1]]])
    B = np.array([prize_location[0], prize_location[1]])
    
    try:
        # Check the determinant to determine the type of solution
        determinant = np.linalg.det(A)
        
        if np.isclose(determinant, 0, rtol=1e-13):
            # Infinite solutions case: calculate valid integer solutions
            solutions = []
            a_coeff, b_coeff = button_a[0], button_b[0]
            c_coeff, d_coeff = button_a[1], button_b[1]
            prize_x, prize_y = prize_location

            # Calculate bounds for A
            max_a = prize_x // a_coeff if a_coeff > 0 else prize_y // c_coeff
            for A_value in range(1, int(max_a) + 1):
                # Solve for B using the first equation
                B_value = (prize_x - a_coeff * A_value) / b_coeff
                if B_value > 0 and np.isclose(B_value, round(B_value), rtol=1e-13):
                    B_value = round(B_value)
                    # Validate with the second equation
                    check_y = c_coeff * A_value + d_coeff * B_value
                    if np.isclose(check_y, prize_y, rtol=1e-13):
                        solutions.append((A_value, B_value))
            
            if solutions:
                # Find the solution with the minimum cost
                return min(solutions, key=lambda sol: sol[0] * button_a_cost + sol[1] * button_b_cost)
            else:
                return None
        else:
            # Unique solution case
            solution = np.linalg.solve(A, B)
            A_value, B_value = solution
            if np.isclose(A_value, round(A_value), rtol=1e-13) and np.isclose(B_value, round(B_value), rtol=1e-13):
                A_rounded, B_rounded = round(A_value), round(B_value)
                if A_rounded > 0 and B_rounded > 0:
                    return int(A_rounded), int(B_rounded)
            return None
    except np.linalg.LinAlgError:
        return None


def part2(puzzles):
    """Solve part 2."""
    button_a_cost = 3
    button_b_cost = 1
    
    total_button_a_pressed = 0
    total_button_b_pressed = 0
    
    # we need to add 10000000000000 to each prize location
    for puzzle in puzzles.values():
        puzzle[2] = (puzzle[2][0] + 10000000000000, puzzle[2][1] + 10000000000000)
    
    solutions: dict[int, tuple[int, int]] = {}
    for puzzle_id, puzzle in puzzles.items():
        button_a, button_b, prize_location = puzzle
        solution = solve_system_with_min_cost(button_a, button_b, prize_location, button_a_cost, button_b_cost)
        if solution:
            A_value, B_value = solution
            solutions[puzzle_id] = (A_value, B_value)
            total_button_a_pressed += A_value
            total_button_b_pressed += B_value
        else:
            solutions[puzzle_id] = None
    
    return (button_a_cost * total_button_a_pressed) + (button_b_cost * total_button_b_pressed)


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
