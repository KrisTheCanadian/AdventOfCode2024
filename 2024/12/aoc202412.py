"""AoC 12, 2024."""

# Standard library imports
import pathlib
import sys


def parse_data(puzzle_input: str) -> list[str]:
    """Parse input."""
    return puzzle_input.splitlines()


def part1(terrain: list[str]):
    """Solve part 1."""
    regions: dict[int, set[tuple[int, int]]] = {}
    visited: set[tuple[int, int]] = set()
    # we get a point (x, y) and we look for all their neighbours
    # we update the visited set and we create a region with in
    
    region_id = 0
    for x, value in enumerate(terrain):
        for y in range(len(value)):
            if (x, y) in visited:
                continue
            
            region = find_region_of_unvisited_point((x, y), terrain)
            visited |= region

            regions[region_id] = region

            region_id += 1

    # calculate the sum of perimeters multiplied by the region area
    total = 0
    for region_id, region in regions.items():
        perimeter = calculate_perimeter_of_region(region, terrain)
        area = len(region)
        total += perimeter * area

    return total
    


def calculate_perimeter_of_region(region: set[tuple[int, int]], terrain: list[str]) -> int:
    """Calculate the perimeter of a region."""
    perimeter = 0

    for point in region:
        x, y = point
        if x == 0 or (x - 1, y) not in region:
            perimeter += 1
        if x == len(terrain) - 1 or (x + 1, y) not in region:
            perimeter += 1
        if y == 0 or (x, y - 1) not in region:
            perimeter += 1
        if y == len(terrain[0]) - 1 or (x, y + 1) not in region:
            perimeter += 1

    return perimeter
            

def find_region_of_unvisited_point(point: tuple[int, int], map: list[str]) -> set[tuple[int, int]]:
    """Find the region of a point."""
    region = set()
    region.add(point)
    visited = set()
    while region:
        point = region.pop()
        visited.add(point)
        region |= get_neighbours(point, map) - visited

    return visited

def get_neighbours(point: tuple[int, int], map: list[str]) -> set[tuple[int, int]]:
    """Get the neighbours of a point that has the same value as it."""
    neighbours = set()
    x, y = point
    point_value = map[x][y]
    if x > 0:
        if map[x - 1][y] == point_value:
            neighbours.add((x - 1, y))
    if x < len(map) - 1:
        if map[x + 1][y] == point_value:
            neighbours.add((x + 1, y))
    if y > 0:
        if map[x][y - 1] == point_value:
            neighbours.add((x, y - 1))
    if y < len(map[0]) - 1:
        if map[x][y + 1] == point_value:
            neighbours.add((x, y + 1))
    return neighbours

def part2(terrain: list[str]):
    """Solve part 2."""
    regions: dict[int, set[tuple[int, int]]] = {}
    visited: set[tuple[int, int]] = set()
    # we get a point (x, y) and we look for all their neighbours
    # we update the visited set and we create a region with in
    
    region_id = 0
    for x, value in enumerate(terrain):
        for y in range(len(value)):
            if (x, y) in visited:
                continue
            
            region = find_region_of_unvisited_point((x, y), terrain)
            visited |= region

            regions[region_id] = region

            region_id += 1

    # calculate the sum of perimeters multiplied by the region area
    total = 0
    for region_id, region in regions.items():
        sides = calculate_the_number_of_sides(region, terrain)
        area = len(region)
        total += sides * area

    return total

def calculate_the_number_of_sides(region: set[tuple[int, int]], terrain: list[str]) -> int:
    """Calculate the perimeter of a region."""
    pass


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
