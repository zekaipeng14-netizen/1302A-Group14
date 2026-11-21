# 1302A-Group14: Secret Room Adventure (`group14_secret_room`)

A text-based secret room puzzle and adventure game implemented in Python for **CS1302A (Agentic Coding)** by **Group 14**.

## Motivation
Text-based puzzle games allow players to focus on logic, observation, and clue deduction without heavy graphical overhead. Our motivation is to build an interactive, multi-level secret room escape experience in Python where players explore rooms, collect items, inspect clues, and unlock doors to progress.

## Innovation
- **Structured Multi-Level & Clue System**: Organizes room maps, doors, required items, and interactive clues cleanly so new rooms and puzzles can be expanded easily.
- **Interactive Inventory & Inspection**: Combines movement, item collection, item inspection (`ITEM_DESCRIPTIONS`), and lock-and-key progression into a clear terminal gameplay loop.

## Setup & Usage Guide

### 1. Install from PyPI
```bash
pip install group14_secret_room
```

### 2. Or Run from Source
Clone the public repository:
```bash
git clone https://github.com/zekaipeng14-netizen/1302A-Group14.git
cd 1302A-Group14
```

Run the game script:
```bash
python src/group14_secret_room/main.py
```

## Example Use Cases
1. **Explore the Room & Collect Clues**: Start in `"Escape the Secret Room: Chapter 1"`, move through the map, and inspect clues (such as checking the desk calendar or torn note) to gather hints.
2. **Unlock Progression Doors**: Pick up required items (such as a key) and use them at the locked door to advance through the room.
