"""AoC 14, 2024."""

# Standard library imports
import pathlib
import re
import sys
from PIL import Image, ImageDraw
import imageio


def parse_data(puzzle_input: str) -> dict[int, tuple[tuple[int, int], tuple[int, int]]]:
    """Parse input."""
    # Key -> Robot ID
    # Value -> tuple of list[position] where the index is the seconds and velocity
    robots: dict[int, tuple[list[tuple[int, int]], tuple[int, int]]] = {}

    # regex
    pattern = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')

    robot_id = 0
    for line in puzzle_input.splitlines():
        match = pattern.match(line)
        x, y, vx, vy = map(int, match.groups())
        robots[robot_id] = [[(x, y)], (vx, vy)]
        robot_id += 1

    return robots


def part1(robots: dict[int, tuple[list[tuple[int, int]], tuple[int, int]]]):
    """Solve part 1."""
    width, height = (101, 103) # example is 11, 7, real input is 101, 103
    # 0,0 is top left corner
    # x is right, y is down
    # v=1, -2 means move 1 right, 2 up

    # robots teleport from one edge to another

    simulation_seconds = 100000
    seconds = 0

    # we will store each position of each robot for each second
    # key = second, value = id, position

    # Directory to save frames
    frame_dir = "frames"
    pathlib.Path(frame_dir).mkdir(exist_ok=True)

    while seconds <= simulation_seconds:
        for _, (positions, velocity) in robots.items():
            x, y = positions[-1]
            vx, vy = velocity
            x, y = update_position(x, y, vx, vy, width, height)

            positions.append((x, y))
        
        # print the positions of the robots
        print(f"Second {seconds}:")
        visualize_map(robots, width, height, seconds, frame_dir)
        print()

        seconds += 1

    # create an animation
    create_animation(frame_dir, "robots_animation.gif")

    # we need to calculate the number of robots in each quadrant
    # To determine the safest area, count the number of robots in each quadrant after 100 seconds.
    # Robots that are exactly in the middle (horizontally or vertically) don't count as being in any quadrant
    quadrants = count_robots_in_quadrants(robots, width, height, simulation_seconds)
    print("Quadrants:", quadrants)

    return quadrants["top_left"] * quadrants["top_right"] * quadrants["bottom_left"] * quadrants["bottom_right"]
    

def update_position(x, y, vx, vy, width, height):
    """Update the position of a robot and handle edge wrap-around while keeping the velocity offset."""
    x += vx
    y += vy

    # Wrap around horizontally
    if x < 0:
        x = (width + (x % width)) % width
    elif x >= width:
        x = x % width

    # Wrap around vertically
    if y < 0:
        y = (height + (y % height)) % height
    elif y >= height:
        y = y % height

    return x, y



def count_robots_in_quadrants(robots, width, height, seconds):
    """Count the number of robots in each quadrant after a given number of seconds."""
    mid_x = width // 2
    mid_y = height // 2

    quadrants = {
        'top_left': 0,
        'top_right': 0,
        'bottom_left': 0,
        'bottom_right': 0
    }

    for _, (positions, _) in robots.items():
        x, y = positions[seconds]

        if x == mid_x or y == mid_y:
            continue  # Skip robots exactly in the middle

        if x < mid_x and y < mid_y:
            quadrants['top_left'] += 1
        elif x >= mid_x and y < mid_y:
            quadrants['top_right'] += 1
        elif x < mid_x and y >= mid_y:
            quadrants['bottom_left'] += 1
        elif x >= mid_x and y >= mid_y:
            quadrants['bottom_right'] += 1

    return quadrants

def visualize_map(robots, width, height, seconds, frame_dir):
    """Visualize the map with robot positions and counts."""
    # Create an empty map
    map_grid = [[0 for _ in range(width)] for _ in range(height)]

    # Count the number of robots in each cell
    for _, (positions, _) in robots.items():
        x, y = positions[seconds]
        map_grid[y][x] += 1

    # Create an image
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Draw the robots on the image
    for y in range(height):
        for x in range(width):
            if map_grid[y][x] > 0:
                draw.point((x, y), fill='black')

    # Save the image
    img.save(f"{frame_dir}/frame_{seconds:04d}.png")

def create_animation(frame_dir, output_file, duration=0.1):
    """Create an animated GIF from the saved frames."""
    frames = []
    for i in range(1001):  # Adjust the range based on the number of frames
        frame_path = f"{frame_dir}/frame_{i:04d}.png"
        frames.append(imageio.imread(frame_path))
    imageio.mimsave(output_file, frames, duration=duration)

def part2(data):
    """Solve part 2."""


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
