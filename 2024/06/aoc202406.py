"""AoC 6, 2024."""

# Standard library imports
import pathlib
import sys
import copy


def parse_data(puzzle_input: str):
    """Parse input."""
    return puzzle_input.splitlines()


def part1(map: list[str]) -> int:
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
            guard_position = walk_one_step_in_direction2(guard_position, guard_direction, visited)
        
    return len(visited)
    
def change_guard_direction(guard_direction: tuple[int, int]):
    """Change direction 90 degrees to the right."""
    x, y = guard_direction
    # print(f"guard changed direction by 90 degrees from ({x}, {y}) to ({y}, {-x})")
    return (y, -x)
    
def walk_one_step_in_direction2(guard_position: tuple[int, int], guard_direction: tuple[int, int], visited: set[tuple[int, int]]) -> tuple[int, int]:
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
    
    if map[x][y] == "#" or map[x][y] == "O":
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


def part2(map: list[str]) -> int:
    """Solve part 2."""
    guard_position: tuple[int, int] = find_guard_position_on_map(map)
    guard_direction: tuple[int, int] = (-1, 0) # starts heading north
    visited: set[tuple[tuple[int, int], tuple[int, int]]] = set() # position, direction
    
    obstables: list[tuple[int, int]] = []
    
    guard_start_position = guard_position
    
    while not is_guard_out_of_map(map, guard_position):
        if is_in_loop(guard_position, guard_direction, visited, guard_direction):
            obstables = obstables + 1
        # check space above guard
        if is_space_infront_guard_obstructed(map, guard_position, guard_direction):
            # turn 90 degrees right (change of direction)
            guard_direction = change_guard_direction(guard_direction)
        else:
            # walk forward (in current direction) and mark that location with an X
            guard_position = walk_one_step_in_direction2(guard_position, guard_direction, visited)
        
    
    # now that we have the visited positions and directions, we can place an obstable infront of each one and see if it loops
    # we cannot but an obstacle on the guard_start_position
    for x, _ in enumerate(map):
        for y, _ in enumerate(map[x]):
            if (x, y) == guard_start_position:
                continue
            
            guard_position = guard_start_position
            guard_direction: tuple[int, int] = (-1, 0)
            
            new_visited = set()
            
            # check if there's a loop
            modified_map = copy.deepcopy(map)
            modified_map[x] = modified_map[x][:y] + "O" + modified_map[x][y + 1:]
            
            while not is_guard_out_of_map(map, guard_position):
                if is_in_loop(guard_position, guard_direction, new_visited, guard_direction):
                    obstables.append((x, y))
                    guard_position = (-100, -100) # exit the simulation loop
                    
                # check space above guard
                if is_space_infront_guard_obstructed(modified_map, guard_position, guard_direction):
                    # turn 90 degrees right (change of direction)
                    guard_direction = change_guard_direction(guard_direction)
                else:
                    # walk forward (in current direction) and mark that location with an X
                    guard_position = walk_one_step_in_direction2(guard_position, guard_direction, new_visited)
                    
    return len(obstables)

# def part2(map: list[str]) -> int:
#     """Solve part 2."""
#     guard_position: tuple[int, int] = find_guard_position_on_map(map)
#     guard_direction: tuple[int, int] = (-1, 0) # starts heading north
#     visited: set[tuple[tuple[int, int], tuple[int, int]]] = set() # position, direction

#     guard_position: tuple[int, int] = find_guard_position_on_map(map)
#     guard_direction: tuple[int, int] = (-1, 0) # starts heading north
    
#     obstables: list[tuple[int, int]] = []
    
#     guard_start_position = guard_position
    
#     while not is_guard_out_of_map(map, guard_position):
#         if is_in_loop(guard_position, guard_direction, visited, guard_direction):
#             obstables = obstables + 1
#         # check space above guard
#         if is_space_infront_guard_obstructed(map, guard_position, guard_direction):
#             # turn 90 degrees right (change of direction)
#             guard_direction = change_guard_direction(guard_direction)
#         else:
#             # walk forward (in current direction) and mark that location with an X
#             guard_position = walk_one_step_in_direction2(guard_position, guard_direction, visited)
        
    
#     # now that we have the visited positions and directions, we can place an obstable infront of each one and see if it loops
#     # we cannot but an obstacle on the guard_start_position
#     for visit in visited:
#         new_visited = set()
#         position = visit[0]
#         direction = visit[0]
        
#         if position == guard_start_position:
#             continue
        
#         # check if there's a loop
#         guard_position = guard_start_position
        
#         x, y = position
        
#         modified_map = copy.deepcopy(map)
#         try:
#             # add the # to the correct index
#             modified_map[x] = modified_map[x][:y] + "O" + modified_map[x][y + 1:]
#         except:
#             continue
        
#         # simulation loop
#         while not is_guard_out_of_map(modified_map, guard_position):
#             # check space above guard
#             if is_space_infront_guard_obstructed(modified_map, guard_position, guard_direction):
#                 # turn 90 degrees right (change of direction)
#                 guard_direction = change_guard_direction(guard_direction)
#                 map[guard_position[0]] = map[guard_position[0]][:guard_position[1]] + '+' + map[guard_position[0]][guard_position[1]+1:]
#             else:
#                 # walk forward (in current direction) and mark that location with an X
#                 guard_position = walk_one_step_in_direction2(guard_position, guard_direction, new_visited)

#             if is_in_loop2(guard_position, guard_direction, visited, direction, new_visited):
#                 obstables.append(position)
#                 guard_position = (-100, -100) # exit the simulation loop
            
#             print_map(modified_map)
        
#     return len(obstables)

def print_map(map: list[str]) -> None:
    """Print the map nicely."""
    for row in map:
        print(row)
    
def is_in_loop(guard_position: tuple[int, int], guard_direction: tuple[int, int], visited: set[tuple[tuple[int, int], tuple[int, int]]], direction: tuple[int, int]) -> bool:
    
    # if the guard position and direction is the same as visited
    target: tuple[tuple[int, int], tuple[int, int]] = (guard_position, guard_direction)
    if target in visited:
        if guard_direction == direction:
            return True
    
    return False

def is_in_loop2(guard_position: tuple[int, int], guard_direction: tuple[int, int], visited: set[tuple[tuple[int, int], tuple[int, int]]], direction: tuple[int, int], new_visited: set[tuple[tuple[int, int], tuple[int, int]]]) -> bool:
    
    def is_same_direction(dir1: tuple[int, int], dir2: tuple[int, int]) -> bool:
        # Check if the directions are the same horizontally or vertically
        return (dir1[0] == dir2[0] and dir1[0] != 0) or (dir1[1] == dir2[1] and dir1[1] != 0)
    
    # if the guard position and direction is the same as visited
    target: tuple[tuple[int, int], tuple[int, int]] = (guard_position, guard_direction)
    if target in visited:
        if is_same_direction(guard_direction, direction):
            return True
        
    if target in new_visited:
        if is_same_direction(guard_direction, direction):
            return True
    
    return False
    
def walk_one_step_in_direction2(guard_position: tuple[int, int], guard_direction: tuple[int, int], visited: set[tuple[tuple[int, int], tuple[int, int]]]) -> tuple[int, int]:
    x, y = guard_position
    visited.add(((x, y), guard_direction))
    
    nx, ny = guard_position[0] + guard_direction[0], guard_position[1] + guard_direction[1]
    # print(f"guard moved from ({x}, {y}) to ({nx}, {ny})")
    return (nx, ny)


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
