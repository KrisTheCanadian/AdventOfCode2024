"""AoC 8, 2024."""

# Standard library imports
import pathlib
import sys

def parse_data(puzzle_input):
    """Parse input."""
    antennas = {}
    lines = puzzle_input.splitlines()
    for y, row in enumerate(lines):
        for x, char in enumerate(row):
            if char.isalnum():  # Identifies a valid frequency character
                antennas.setdefault(char, []).append((x, y))
    width = len(lines[0])
    height = len(lines)
    return antennas, width, height

def calculate_antinodes(antennas, width, height):
    """Calculate all unique antinode positions for antennas of the same frequency."""
    antinodes = set()
    
    for freq, positions in antennas.items():
        n = len(positions)
        for i in range(n):
            for j in range(i + 1, n):
                # Positions of the two antennas
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                # Calculate the direction vector
                dx = x2 - x1
                dy = y2 - y1

                # from x2, y2 we need to add 2dx and 2dy
                antinode1 = (x2 - 2*dx, y2 - 2*dy)
                antinode2 = (x1 + 2*dx, y1 + 2*dy)

                # Only include valid antinodes within the bounds of the map
                for ax, ay in [antinode1, antinode2]:
                    if 0 <= ax < width and 0 <= ay < height:
                        antinodes.add((int(ax), int(ay)))

    return antinodes

def calculate_antinodes2(antennas, width, height):
    """Calculate all unique antinode positions for antennas of the same frequency."""
    antinodes = set()
    
    for freq, positions in antennas.items():
        n = len(positions)
        for i in range(n):
            for j in range(i + 1, n):
                # Positions of the two antennas
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                # Calculate the direction vector
                dx = x2 - x1
                dy = y2 - y1

                # from x2, y2 we need to add 2dx and 2dy
                antinode1 = (x2 - 2*dx, y2 - 2*dy)

                antinodes.add((x1, y1))
                antinodes.add((x2, y2))
                
                while antinode_is_within_bounds(antinode1, width, height):
                    antinodes.add((int(antinode1[0]), int(antinode1[1])))
                    antinode1 = (antinode1[0] - dx, antinode1[1] - dy)


                antinode2 = (x1 + 2*dx, y1 + 2*dy)
                while antinode_is_within_bounds(antinode2, width, height):
                    antinodes.add((int(antinode2[0]), int(antinode2[1])))
                    antinode2 = (antinode2[0] + dx, antinode2[1] + dy)


    return antinodes

def antinode_is_within_bounds(antinode, width, height) -> bool:
    return 0 <= antinode[0] < width and 0 <= antinode[1] < height
        

def print_map_with_antinodes(antennas, antinodes, width, height):
    """Print the map with antennas and antinodes for visual debugging."""
    # Create an empty map
    map_grid = [['.' for _ in range(width)] for _ in range(height)]

    # Place antennas on the map
    for freq, positions in antennas.items():
        for x, y in positions:
            map_grid[y][x] = freq

    # Place antinodes on the map
    for x, y in antinodes:
        if map_grid[y][x] == '.':
            map_grid[y][x] = '#'

    # Print the map
    for row in map_grid:
        print(''.join(row))

def part1(data):
    """Solve part 1."""
    antennas, width, height = data
    antinodes = calculate_antinodes(antennas, width, height)
    print_map_with_antinodes(antennas, antinodes, width, height)
    return len(antinodes)


def part2(data):
    """Solve part 2."""
    antennas, width, height = data
    antinodes = calculate_antinodes2(antennas, width, height)
    print('\n')
    print_map_with_antinodes(antennas, antinodes, width, height)
    return len(antinodes)


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
