# 1302A-Group14: Secret Room Adventure (`group14_secret_room`)

A text-based secret room puzzle and adventure game implemented in Python for **CS1302A (Agentic Coding)** by **Group 14**[span_2](start_span)[span_2](end_span)[span_3](start_span)[span_3](end_span)[span_4](start_span)[span_4](end_span)[span_5](start_span)[span_5](end_span).

## Motivation
Text-based puzzle games allow players to focus on logic, observation, and clue deduction without heavy graphical overhead. Our motivation is to build an interactive, multi-level secret room escape experience in Python where players explore rooms, collect items, inspect clues, and unlock doors to progress[span_6](start_span)[span_6](end_span).

## Innovation
- **Structured Multi-Level & Clue System**: Organizes room maps, doors, required items, and interactive clues cleanly so new rooms and puzzles can be expanded easily[span_7](start_span)[span_7](end_span).
- **Interactive Inventory & Inspection**: Combines movement, item collection, item inspection (`ITEM_DESCRIPTIONS`), and lock-and-key progression into a clear terminal gameplay loop[span_8](start_span)[span_8](end_span).

## Setup & Usage Guide

### 1. Install from PyPI
```bash
pip install group14_secret_room
```

### 2. Or Run from Source
Clone the public repository[span_9](start_span)[span_9](end_span)[span_10](start_span)[span_10](end_span):
```bash
git clone [https://github.com/zekaipeng14-netizen/1302A-Group14.git](https://github.com/zekaipeng14-netizen/1302A-Group14.git)
cd 1302A-Group14
```

Run the game script:
```bash
python src/group14_secret_room/main.py
```

## Example Use Cases
1. **Explore the Room & Collect Clues**: Start in `"Escape the Secret Room: Chapter 1"`, move through the map, and inspect clues (such as checking the desk calendar or torn note) to gather hints[span_11](start_span)[span_11](end_span).
2. **Unlock Progression Doors**: Pick up required items (such as a key) and use them at the locked door to advance through the room[span_12](start_span)[span_12](end_span).
