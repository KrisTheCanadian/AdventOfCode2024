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


def part2(data):
    """Solve part 2."""
    # print("\nStarting the disk compaction process...")

    disk = list(data[0])  # Ensure the disk is mutable
    max_id = data[1]
    print(f"Initial disk state: {''.join(disk)}")

    # Loop over file IDs in descending order
    for current_id in range(max_id - 1, -1, -1):
        current_id_str = str(current_id)
        print(f"\nProcessing file ID: {current_id_str}")

        # Find all file blocks and free space blocks
        file_blocks = find_contiguous_blocks(disk, current_id_str)
        free_blocks = find_contiguous_blocks(disk, ".")
        
        # Store the indices of the free blocks
        original_free_blocks = free_blocks.copy()
        
        # Debug output: show the identified blocks
        print(f"File blocks for ID {current_id_str}: {file_blocks}")
        print(f"Free space blocks: {free_blocks}")

        # We need to attempt moving the files one by one
        for file_start, file_end in file_blocks:
            file_size = file_end - file_start + 1
            print(f"File block found from {file_start} to {file_end} (size {file_size})")

            # Find leftmost free block that can fit the file
            for free_start, free_end in free_blocks:
                free_size = free_end - free_start + 1
                print(f"Checking free block from {free_start} to {free_end} (size {free_size})")

                if free_size >= file_size:
                    print(f"Found enough free space for file ID {current_id_str} in block from {free_start} to {free_end}")
                    if free_start > file_start and free_end > file_end:
                        print(f"Skipping free block starting at {free_start} because it starts after the file block at {file_start}")
                        continue
                    # Move file to free space, from left to right
                    for i in range(file_size):
                        disk[free_start + i] = current_id_str
                        disk[file_start + i] = "."
                    print(f"Moved file ID {current_id_str} to position {free_start}")

                    # Update free space after file movement
                    free_blocks = find_contiguous_blocks(disk, ".")
                    print(f"Updated free blocks after move: {free_blocks}")

                    # Check that free blocks have not been shifted to the right
                    if free_blocks != original_free_blocks:
                        print(f"Warning: Free blocks have been modified unexpectedly!")
                        print(f"Original free blocks: {original_free_blocks}")
                        print(f"Current free blocks: {free_blocks}")
                        pass
                    
                    # Stop moving this file, since it's already moved
                    break  # Move to the next file block

        # Visualize the disk after processing each file ID
        print(f"Disk state after processing file ID {current_id_str}: {''.join(disk)}")

    print("\nFinal disk state:", ''.join(disk))
    total = 0
    for i, digit in enumerate(disk):
        if digit == ".":
            continue
        total = total + (i * int(digit))
    return total

def find_contiguous_blocks(disk, char):
    """Find all contiguous blocks of a given character in the disk."""
    blocks = []
    start = None
    for i, c in enumerate(disk):
        if c == char:
            if start is None:
                start = i
        else:
            if start is not None:
                blocks.append((start, i - 1))
                start = None
    if start is not None:
        blocks.append((start, len(disk) - 1))
    return blocks



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
