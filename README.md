# Secret Room Adventure (`group14_secret_room`)

[![PyPI](https://img.shields.io/pypi/v/group14_secret_room)](https://pypi.org/project/group14_secret_room/)
[![Python](https://img.shields.io/pypi/pyversions/group14_secret_room)](https://pypi.org/project/group14_secret_room/)
[![tests](https://github.com/zekaipeng14-netizen/1302A-Group14/actions/workflows/tests.yml/badge.svg)](https://github.com/zekaipeng14-netizen/1302A-Group14/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/zekaipeng14-netizen/1302A-Group14/blob/main/LICENSE)

A text-based escape-room puzzle game that runs in any terminal. It needs no dependencies beyond Python's standard library.
Built for **CS1302A Intro to Computer Programming (Agentic Coding)** by **Group 14**.

```
=== Escape the Secret Room: Chapter 1 ===
# # # # # # # # # # # # #
#       #           ?   #
#   #   #   # # # # #   #
# @ #               #   D
#   # # # #   # #   #   #
#               #   ?   #
# # # # # # # # # # # # #
========================================
[Backpack]: Empty   [Steps]: 0
Controls: w/a/s/d (Move) | e (Investigate) | i (Inspect Bag) | h (Hint) | q (Quit)
========================================
> You wake up in a cold room. Find a way out!
Please enter command:
```

## Motivation

Escape-room games train observation and logical deduction. Most of them need a graphics engine or a web browser. We wanted to show that a complete, replayable puzzle experience can be built with **pure Python**: lists for maps, dictionaries for clues, and a single game loop. The result is small enough for a beginner to read end to end, and fun enough to play.

## Innovation

- **Data-driven level design.** Each chapter is a plain Python dictionary with a map, a start position, a door and its clues. Adding a new room means adding data. You don't touch the game engine. See [Adding your own level](#adding-your-own-level).
- **Two kinds of interactive clues.** *Pickup* clues give the player items with readable descriptions. *Lock* clues need a password that the player deduces from those items. Together they form a chain: clue → deduction → key → door.
- **Inventory and inspection.** Press `i` at any time to re-read item descriptions, so the puzzles can be solved by reasoning, not by memory.
- **Hint system and step counter.** Stuck players can press `h` for a nudge. The step counter gives experienced players a score to beat.
- **Replayable and testable.** The engine never mutates the level data. `run_game()` accepts a custom input function, so the whole game can be played automatically in unit tests (see `tests/`).
- **Cross-platform.** The screen is cleared correctly on Windows, macOS and Linux, and Ctrl+C or Ctrl+D quits cleanly.

## Installation

Requires Python 3.8 or newer.

```bash
pip install group14_secret_room
```

## Usage

After installing, start the game with either command:

```bash
secret-room
```

```bash
python -m group14_secret_room
```

You can also run it from Python code:

```python
from group14_secret_room import run_game
run_game()
```

### Controls

| Key | Action |
|---|---|
| `w` `a` `s` `d` | Move up / left / down / right (type the letter, then press Enter) |
| `e` | Investigate the tile you are standing on |
| `i` | Inspect the items in your backpack |
| `h` | Get a hint for the current chapter |
| digits, e.g. `1234` | Enter a password while standing on a lock |
| `q` | Quit |

### Map legend

| Symbol | Meaning |
|---|---|
| `@` | You |
| `#` | Wall |
| `?` | Something suspicious: a clue, item or lock |
| `D` | Door to the next chapter |

## Example Use Cases

1. **Casual puzzle break.** Run `secret-room` in any terminal and escape both chapters in a few minutes.
2. **Teaching Python data structures.** The game shows nested lists (2-D maps), dictionaries keyed by tuples (clue positions), and a state machine (the game loop) in about 250 lines of readable code.
3. **Designing your own escape room.** Students or teachers can write new chapters as data and share them. No game engine knowledge is needed.
4. **Automated testing example.** `tests/test_game.py` plays the entire game with scripted input. It is a practical example of testing an interactive program with `pytest`.

### Sample walkthrough (spoiler!)

<details>
<summary>Chapter 1</summary>

1. Walk to the top-right `?` and press `e`. You pick up a **Calendar** with *October 24th* circled.
2. Walk to the bottom-right `?` and press `e`. You find an iron box with a 4-digit lock.
3. Type `1024` (10/24) to get the **Brass Key**.
4. Walk into the `D` on the right wall to go to Chapter 2.
</details>

<details>
<summary>Chapter 2</summary>

1. Pick up the **Note**: *"The number of corners on a triangle, a square, and a pentagon."*
2. At the wall safe, type `345` to get the **Silver Key**.
3. Walk through the steel door to escape!
</details>

## Adding your own level

Add a new entry to `LEVELS` in `src/group14_secret_room/main.py`. Chapters are played in numeric order:

```python
LEVELS[3] = {
    "title": "Escape the Secret Room: Chapter 3 - The Vault",
    "hint": "Optional hint shown when the player presses 'h'.",
    "start_pos": (1, 1),
    "map": [
        ["#", "#", "#", "#", "#", "#", "#"],
        ["#", " ", " ", "?", " ", "?", "#"],
        ["#", " ", "#", "#", " ", " ", "D"],
        ["#", "#", "#", "#", "#", "#", "#"],
    ],
    "door": {
        "pos": (2, 6),
        "required_item": "Gold Key",
        "locked_msg": "The vault door needs a Gold Key.",
        "unlock_msg": "The vault swings open!",
    },
    "clues": {
        (1, 3): {"type": "pickup", "text": "A sticky note says 7-7-7.",
                 "item": "Sticky Note", "collected": False},
        (1, 5): {"type": "lock", "text": "A keypad with three buttons.",
                 "password": "777", "reward": "Gold Key", "unlocked": False},
    },
}
```

Remember to add a description for every new item to `ITEM_DESCRIPTIONS`. Then run `pytest`: `test_level_data_is_valid` checks that your map, door and clues are consistent.

## Development

```bash
git clone https://github.com/zekaipeng14-netizen/1302A-Group14.git
cd 1302A-Group14
pip install -e ".[dev]"
pytest
```

Project layout:

```
src/group14_secret_room/
    main.py        # level data + game engine
    __main__.py    # enables `python -m group14_secret_room`
    __init__.py    # public API: run_game, LEVELS, ITEM_DESCRIPTIONS
tests/             # pytest suite (runs on GitHub Actions)
prototype/         # our first single-room prototype, kept for reference
docs/              # demo script and presentation notes
```

## Team (Group 14)

| GitHub | Contributions |
|---|---|
| [@zekaipeng14-netizen](https://github.com/zekaipeng14-netizen) | Project setup, game engine, packaging, documentation |
| [@Fenice723](https://github.com/Fenice723) | Game logic (`main.py`) |
| [@guiyifei1014-boop](https://github.com/guiyifei1014-boop) | Game logic (`main.py`) |
| [@guosonglin999-hue](https://github.com/guosonglin999-hue) | Initial prototype |

## License

[MIT](https://github.com/zekaipeng14-netizen/1302A-Group14/blob/main/LICENSE)
