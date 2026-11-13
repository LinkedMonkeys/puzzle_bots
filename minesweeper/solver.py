from bs4 import BeautifulSoup
from dotenv import load_dotenv

import os
import re
import requests
import sys

load_dotenv()

# Extracts the puzzle from the HTML.  Written by Claude.  Apparently the puzzle is run length encoded with letters a, b, c, d representing 1, 2, 3, 4 clues.
def get_puzzle(html: str) -> list[list[int | None]]:
    """Extract a Minesweeper puzzle from page HTML as a 2D list.

    Cells are an int (revealed number of neighbouring mines) or None (unknown).
    """
    m = re.search(r"var\s+task\s*=\s*'([^']*)'", html)
    if not m:
        raise ValueError("task variable not found")
    task = m.group(1)

    w = re.search(r"puzzleWidth\s*:\s*(\d+)", html)
    h = re.search(r"puzzleHeight\s*:\s*(\d+)", html)
    if not (w and h):
        raise ValueError("puzzle dimensions not found")
    width, height = int(w.group(1)), int(h.group(1))

    cells: list[int | None] = []
    for ch in task:
        if ch.isdigit():
            cells.append(int(ch))
        elif ch.isalpha():
            cells.extend([None] * (ord(ch.lower()) - ord('a') + 1))
        else:
            raise ValueError(f"unexpected character {ch!r} in task")

    if len(cells) != width * height:
        raise ValueError(f"expected {width * height} cells, got {len(cells)}")

    return [cells[r * width:(r + 1) * width] for r in range(height)]

# There is a 'param' field in the form on the page.  I am assuming it is a puzzle identifier.
def get_param(html):
    soup = BeautifulSoup(html, "html.parser")
    form = soup.find("form", id="puzzleForm")
    tag = form.find("input", attrs={"name": "param"})
    return tag["value"]

# Prints a puzzle in a 2d fashion.
def pretty_print(puzzle):
    puzzle_string = ''
    for row in puzzle:
        for col in row:
            if (col == None):
                puzzle_string += 'X '
            else:
                puzzle_string += str(col) + ' '
        puzzle_string += '\n'

    return puzzle_string

def main():
    pass

if __name__ == "__main__":
    sys.exit(main())