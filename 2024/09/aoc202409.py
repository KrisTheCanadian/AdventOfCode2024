"""AoC 9, 2024."""

# Standard library imports
import pathlib
import sys


def parse_data(puzzle_input):
    """Parse input."""
    compressed_disk = list(puzzle_input)
    disk = []
    id = 0
    for i, digit in enumerate(compressed_disk):
        is_file = i % 2 == 0
        if is_file:
            for _ in range(int(digit)):
                disk.append(str(id))
            
            id = id + 1
        else:
            for _ in range(int(digit)):
                disk.append(".")
                
    return disk, id


def part1(data):
    """Solve part 1."""
    disk = data[0]
    left_pointer = 0
    right_pointer = len(disk) - 1

    while(left_pointer < right_pointer):
        # do stuff
        while disk[left_pointer] != "." and left_pointer < right_pointer:
            left_pointer = left_pointer + 1 
            
        while disk[right_pointer] == "." and left_pointer < right_pointer:
            right_pointer = right_pointer - 1
            
        # we should be in a state of swapping now
        disk[left_pointer], disk[right_pointer] = disk[right_pointer], disk[left_pointer]
        
        left_pointer = left_pointer + 1
        right_pointer = right_pointer - 1
    
    total = 0
    # calculate the filesystem checksum
    for i, digit in enumerate(disk):
        if digit == ".":
            break

        total = total + (i * int(digit))
        
    return total

def parse_data2(puzzle_input):
    """Parse input."""

                
    return puzzle_input



def part2(data):
    """Solve part 2."""
    files = {}
    blanks = []
    id = 0
    position = 0
    
    for i, digit in enumerate(data):
        d = int(digit)
        is_file = i % 2 == 0
        if is_file:
            files[id] = (position, d)
            id = id + 1
        else:
            if d != 0:
                blanks.append((position, d))
        position += d

    while id > 0:
        id -= 1
        pos, size = files[id]
        for i, (start, length) in enumerate(blanks):
            if start >= pos:
                blanks = blanks[:i]
                break
            if size <= length:
                files[id] = (start, size)
                if size == length:
                    blanks.pop(i)
                else:
                    blanks[i] = (start + size, length - size)
                break
    
    total = 0
    for id, (pos, size) in files.items():
        for x in range(pos, pos + size):
            total += x * id
    
    return total

    


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    yield part1(parse_data(puzzle_input))
    yield part2(parse_data2(puzzle_input))


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
