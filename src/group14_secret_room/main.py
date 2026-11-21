"""Secret Room Adventure - a text-based escape-room puzzle game.

Run with ``secret-room`` (after ``pip install group14_secret_room``)
or ``python -m group14_secret_room``.
"""

import copy
import os

# --- 1. Global Item Descriptions (For 'i' command) ---
ITEM_DESCRIPTIONS = {
    "Calendar": "A desk calendar. [October 24th] is circled heavily in red ink.",
    "Brass Key": "A heavy, slightly tarnished brass key. It looks like it fits a standard door lock.",
    "Note": "A torn piece of paper: 'The number of corners on a triangle, a square, and a pentagon.'",
    "Silver Key": "A shiny silver key engraved with an exit symbol."
}

# --- 2. Multi-Level Configuration Data (7x13 Maps) ---
LEVELS = {
    1: {
        "title": "Escape the Secret Room: Chapter 1",
        "hint": "Dates can be written as numbers. What would [October 24th] look like as 4 digits?",
        "start_pos":(3, 1),
        "map": [
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
            ["#", " ", " ", " ", "#", " ", " ", " ", " ", " ", "?", " ", "#"],
            ["#", " ", "#", " ", "#", " ", "#", "#", "#", "#", "#", " ", "#"],
            ["#", " ", "#", " ", " ", " ", " ", " ", " ", " ", "#", " ", "D"],
            ["#", " ", "#", "#", "#", "#", " ", "#", "#", " ", "#", " ", "#"],
            ["#", " ", " ", " ", " ", " ", " ", " ", "#", " ", "?", " ", "#"],
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
        ],
        "door": {
            "pos": (3, 12),
            "required_item": "Brass Key",
            "locked_msg": "The door is tightly locked. You need a Brass Key to open it.",
            "unlock_msg": "Click! The Brass Key turns smoothly. You step through the door into the next room..."
        },
        "clues": {
            (1, 10): {
                "type": "pickup",
                "text": "There is a calendar on the desk, with [October 24th] circled in red pen.",
                "item": "Calendar",
                "collected": False
            },
            (5, 10): {
                "type": "lock",
                "text": "A locked iron box with a 4-digit combination lock on it.",
                "password": "1024",
                "reward": "Brass Key",
                "unlocked": False
            }
        }
    },
    2: {
        "title": "Escape the Secret Room: Chapter 2 - The Study",
        "hint": "Count the corners of each shape in order and write the counts side by side.",
        "start_pos":(1,1),
        "map": [
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
            ["#", " ", " ", " ", " ", "#", " ", " ", " ", "?", " ", " ", "#"],
            ["#", " ", "#", "#", " ", "#", " ", "#", "#", "#", "#", " ", "#"],
            ["#", " ", " ", "#", " ", " ", " ", " ", " ", " ", "#", " ", "#"],
            ["#", "#", " ", "#", "#", "#", " ", "#", " ", " ", "#", " ", "#"],
            ["#", "?", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", "D"],
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
        ],
        "door": {
            "pos": (5, 12),
            "required_item": "Silver Key",
            "locked_msg": "A heavy steel door. It requires a Silver Key.",
            "unlock_msg": "With a loud clank, the steel door swings open! You see sunlight outside!"
        },
        "clues": {
            (1, 9): {
                "type": "pickup",
                "text": "You find a crumpled note hidden under a dusty book.",
                "item": "Note",
                "collected": False
            },
            (5, 1): {
                "type": "lock",
                "text": "A wall safe with a 3-digit keypad.",
                "password": "345",
                "reward": "Silver Key",
                "unlocked": False
            }
        }
    }
}

MOVE_OFFSETS = {
    "w": (-1, 0),
    "s": (1, 0),
    "a": (0, -1),
    "d": (0, 1)
}

# --- 3. Screen Rendering Function ---
def clear_screen():
    """Clear the terminal on Windows, macOS and Linux."""
    os.system("cls" if os.name == "nt" else "clear")


def render_screen(level_data, pos, msg, inv, steps=0, clear=True):
    if clear:
        clear_screen()
    print(f"=== {level_data['title']} ===")
    grid = level_data["map"]
    for r in range(len(grid)):
        line = []
        for c in range(len(grid[r])):
            if r == pos[0] and c == pos[1]:
                line.append("@")
            else:
                line.append(grid[r][c])
        print(" ".join(line))
    print("========================================")
    print(f"[Backpack]: {', '.join(inv) if inv else 'Empty'}   [Steps]: {steps}")
    print("Controls: w/a/s/d (Move) | e (Investigate) | i (Inspect Bag) | h (Hint) | q (Quit)")
    print("========================================")
    if msg:
        print(f"> {msg}")


# --- 4. Main Game Engine ---
def run_game(input_func=input, levels=None, clear=True):
    """Run the game loop.

    ``input_func`` and ``levels`` can be replaced for testing. The level data
    is deep-copied so the global ``LEVELS`` is never modified and the game can
    be played again in the same Python session.

    Returns ``True`` if the player escaped all rooms, ``False`` otherwise.
    """
    levels = copy.deepcopy(LEVELS if levels is None else levels)
    current_level_num = min(levels)
    inventory = []
    steps = 0

    # Initialize first level state
    level_data = levels[current_level_num]
    player_pos = list(level_data["start_pos"])
    status_msg = "You wake up in a cold room. Find a way out!"

    while True:
        render_screen(level_data, player_pos, status_msg, inventory, steps, clear)
        try:
            cmd = input_func("Please enter command: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGame exited.")
            return False

        if not cmd:
            continue

        if cmd == "q":
            print("Game exited.")
            return False

        # ========== Hint (h) ==========
        elif cmd == "h":
            status_msg = "Hint: " + level_data.get("hint", "Look around carefully. Every '?' hides something.")

        # ========== Inspect Backpack (i) ==========
        elif cmd == "i":
            if not inventory:
                status_msg = "Your backpack is completely empty."
            else:
                details = ["--- Backpack Details ---"]
                for item in inventory:
                    desc = ITEM_DESCRIPTIONS.get(item, "No description available.")
                    details.append(f"* [{item}]: {desc}")
                status_msg = "\n".join(details)

        # ========== Numeric Password Input ==========
        elif cmd.isdigit():
            pos_tuple = tuple(player_pos)
            clue = level_data["clues"].get(pos_tuple)
            
            if clue and clue["type"] == "lock" and not clue["unlocked"]:
                if cmd == clue["password"]:
                    reward = clue["reward"]
                    clue["unlocked"] = True
                    inventory.append(reward)
                    # Clear the '?' mark on the map once unlocked
                    level_data["map"][pos_tuple[0]][pos_tuple[1]] = " "
                    status_msg = f"Password correct! It clicks open. You obtained [{reward}]!"
                else:
                    status_msg = f"You entered [{cmd}], but the lock buzzes red. Wrong password!"
            else:
                status_msg = "There is no lock here to enter a password into."

        # ========== Movement Logic (w/a/s/d) ==========
        elif cmd in MOVE_OFFSETS:
            dr, dc = MOVE_OFFSETS[cmd]
            next_r = player_pos[0] + dr
            next_c = player_pos[1] + dc
            target_cell = level_data["map"][next_r][next_c]

            steps += 1
            if target_cell == "#":
                status_msg = "Bang! You bumped into a solid wall."
            elif target_cell == "D":
                door_info = level_data["door"]
                req_item = door_info["required_item"]
                if req_item in inventory:
                    print(f"\n*** {door_info['unlock_msg']} ***")
                    # Check if there is a next level
                    if (current_level_num + 1) in levels:
                        try:
                            input_func("Press Enter to continue to the next chapter...")
                        except (EOFError, KeyboardInterrupt):
                            print("\nGame exited.")
                            return False
                        current_level_num += 1
                        level_data = levels[current_level_num]
                        player_pos = list(level_data["start_pos"])
                        status_msg = f"Welcome to Chapter {current_level_num}!"
                    else:
                        print("*** CONGRATULATIONS! You have escaped all rooms and cleared the game! ***")
                        print(f"*** Total steps: {steps} ***\n")
                        return True
                else:
                    status_msg = door_info["locked_msg"]
            else:
                player_pos = [next_r, next_c]
                if target_cell == "?":
                    status_msg = "You stepped onto something suspicious. Press 'e' to investigate."
                else:
                    status_msg = "You take a step forward."

        # ========== Investigation Logic (e) ==========
        elif cmd == "e":
            pos_tuple = tuple(player_pos)
            clue = level_data["clues"].get(pos_tuple)

            if clue:
                if clue["type"] == "pickup":
                    status_msg = clue["text"]
                    if not clue["collected"]:
                        item = clue["item"]
                        inventory.append(item)
                        clue["collected"] = True
                        level_data["map"][pos_tuple[0]][pos_tuple[1]] = " "
                        status_msg += f"\n[OK] Obtained: [{item}] (Press 'i' anytime to inspect)"
                elif clue["type"] == "lock":
                    if clue["unlocked"]:
                        status_msg = "This lock is already open and empty."
                    else:
                        status_msg = f"{clue['text']} (Type the numbers directly to unlock)"
            else:
                status_msg = "Nothing noteworthy here."

        else:
            status_msg = "Invalid command! Use w/a/s/d, e, i, h, q, or enter a password."

def main():
    """Console entry point (``secret-room`` command)."""
    run_game()


if __name__ == "__main__":
    main()
