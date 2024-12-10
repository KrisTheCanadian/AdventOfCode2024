"""Tests for AoC 9, 2024."""

# Standard library imports
import pathlib

# Third party imports
import aoc202409
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202409.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202409.parse_data(puzzle_input)

@pytest.fixture
def example_one():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202409.parse_data2(puzzle_input)


@pytest.fixture
def example_two():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202409.parse_data2(puzzle_input)


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == ...


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202409.part1(example1) == 1928


def test_part2_example1(example_one):
    """Test part 2 on example input."""
    assert aoc202409.part2(example_one) == 2858


def test_part2_example2(example_two):
    """Test part 2 on example input."""
    assert aoc202409.part2(example_two) == 6204
