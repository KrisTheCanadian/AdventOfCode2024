"""AoC 2, 2024."""

# Standard library imports
import pathlib
import sys


def parse_data(puzzle_input: str) -> list[list[int]]:
    """Parse input."""
    reports: list[list[int]] = []
    lines = puzzle_input.split('\n')
    for line in lines:
        reports.append([int(num) for num in line.split()])
    
    return reports
        


def part1(reports: list[list[int]]):
    """Solve part 1."""
    safe_reports: int = 0
    for report in reports:
        # Safe if both of the following is true:
        # All levels are either all increasing or decreasing
        # Any two adjacent levels differ by at least one and at most three

        # check if all increasing or decreasing
        
        if (not is_numbers_increasing(report) and not is_numbers_decreasing(report)):
            # not safe since its not increasing or decreasing
            continue # not safe

        # check if any two adjacent levels differ by at least one and at most three
        if(not is_safe_level_check(report)):
            continue # not safe

        safe_reports = safe_reports + 1
    
    return safe_reports

def is_safe_level_check(data: list[int]) -> bool:
    # two adjacent differ by at least one and at most three
    for index in range(0, len(data) - 1):
        left = data[index]
        right = data[index + 1]
        diff = abs(left - right)

        if diff > 3:
            return False
    
    return True


def is_numbers_increasing(data: list[int]) -> bool:
    # checks to see if all numbers in the list are increasing
    previous: int = data[0]

    for index in range(1, len(data)):
        # previous should be smaller than current
        current = data[index]
        if previous >= current:
            return False
        
        previous = current
    
    return True


def is_numbers_decreasing(data: list[int]) -> bool:
    # checks to see if all numbers in the list are decreasing
    previous: int = data[0]

    for index in range(1, len(data)):
        # previous should be bigger than current
        current = data[index]
        if previous <= current:
            return False
        
        previous = current
    
    return True

def part2(reports: list[list[int]]):
    safe_reports: int = 0
    for report in reports:
        safe = check_safety(report)
        if not safe:
            work = bruteforce(report)
            if not work:
                continue

        safe_reports = safe_reports + 1
    
    return safe_reports

def bruteforce(report):
    for index in range(len(report)):
        modified_report = reconstruct_list_given_problematic_index(report, index)
        if check_safety(modified_report):
            return True
    return False

def reconstruct_list_given_problematic_index(data: list[int], problematic_index: int) -> list[int]:
    return data[:problematic_index] + data[problematic_index+1:]

def check_safety(report: list[int]) -> bool:
    if (not is_numbers_increasing(report) and not is_numbers_decreasing(report)):
        # not safe since its not increasing or decreasing
        return False # not safe

    # check if any two adjacent levels differ by at least one and at most three
    if(not is_safe_level_check(report)):
        return False # not safe

    return True

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
