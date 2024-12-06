"""AoC 5, 2024."""

# Standard library imports
import pathlib
import sys


def parse_data(puzzle_input: str) -> tuple[list[list[int]], dict[list[int]]]:
    """Parse input."""
    numbers: list[list[int]] = []
    before_rules: dict[list[int]] = {}
    lines: list[str] = puzzle_input.splitlines()
    
    placeholder = -1

    for index, line in enumerate(lines):
        split = line.split('|')
        
        if len(split) < 2:
            placeholder = index
            break
        
        first_number = int(split[0])
        second_number = int(split[1])
        
        if first_number in before_rules:
            # append to list
            before_rules[first_number].append(second_number)
        else:
            before_rules[first_number] = [second_number]
    
        
    for i in range(placeholder + 1, len(lines)):
        data = lines[i]
        
        split = data.split(",")
        line = []
        for number in split:
            line.append(int(number))
        
        numbers.append(line)
            
    return (numbers, before_rules)


def part1(data: tuple[list[list[int]], dict[list[int]]]):
    """Solve part 1."""
    numbers: list[list[int]] = data[0]
    before_rules: dict[list[int]] = data[1]

    total = 0
    
    for page in numbers:
        total = total + check_rules(before_rules, page)

    return total

def check_rules(before_rules, page):
    for target, list_of_after_numbers in before_rules.items():
        if target in page:
                # find the number index
            index = page.index(target)
            before_numbers = {}
            for i in range(0, index):
                # add all the numbers to the dict before target
                before_numbers[page[i]] = True
                # now we check if any of those numbers are before the target
            if check_if_occurs_before(list_of_after_numbers, before_numbers):
                return 0
                
    return page[int(len(page)/2)]
                    
                
def check_if_occurs_before(list_of_after_numbers, before_numbers) -> bool:
    for after_num in list_of_after_numbers:
        if after_num in before_numbers:
            return True
    return False

def part2(data: tuple[list[list[int]], dict[list[int]]]):
    """Solve part 2."""
    numbers: list[list[int]] = data[0]
    before_rules: dict[list[int]] = data[1]
    total = 0
    
    incorrect_pages = []

    for page in numbers:
        if check_rules(before_rules, page) == 0:
            incorrect_pages.append(page)
            
    # given the incorrect lists we must sort them in the correct order
    
    for page in incorrect_pages:
        x = len(page)
        while x > 1:
            x = x - 1
            furthest_index = -1
            
            if page[x] not in before_rules:
                continue # we don't care

            after_numbers = before_rules[page[x]]
            for y in range(x - 1, -1, -1):
                if page[y] in after_numbers:
                    furthest_index = y
            
            if furthest_index != -1:
                # perform a swam
                page[x], page[furthest_index] = page[furthest_index], page[x]
                x = x + 1
        # add the total middle thingy
        total = total + page[int(len(page)/2)]
    
    return total

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
