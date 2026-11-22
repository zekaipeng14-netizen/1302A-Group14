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
        "start_pos": (3, 1),
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
        "start_pos": (1, 1),
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
    "w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)
}
DEFAULT_SAVE_PATH = "secret_room_save.txt"
DEFAULT_SCORES_PATH = "secret_room_scores.txt"


def clear_screen():
    """Clear the terminal on Windows, macOS and Linux."""
    os.system("cls" if os.name == "nt" else "clear")


def format_duration(seconds):
    """Return elapsed seconds as HH:MM:SS or MM:SS."""
    seconds = max(0, int(seconds))
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes:02d}:{seconds:02d}"


def calculate_score(elapsed_seconds, steps, hints_used, wrong_passwords):
    """Calculate a reproducible score from the player's performance."""
    return max(0, 10000 - int(elapsed_seconds) * 2 - steps * 10
                - hints_used * 100 - wrong_passwords * 50)


def score_grade(score):
    if score >= 9000:
        return "A"
    if score >= 7500:
        return "B"
    if score >= 6000:
        return "C"
    return "D"


def render_screen(level_data, pos, msg, inv, steps=0, elapsed_seconds=0,
                  hints_used=0, wrong_passwords=0, clear=True):
    if clear:
        clear_screen()
    print(f"=== {level_data['title']} ===")
    grid = level_data["map"]
    for r in range(len(grid)):
        line = []
        for c in range(len(grid[r])):
            line.append("@" if (r, c) == tuple(pos) else grid[r][c])
        print(" ".join(line))
    current_score = calculate_score(elapsed_seconds, steps, hints_used, wrong_passwords)
    print("========================================")
    print(f"[Backpack]: {', '.join(inv) if inv else 'Empty'}   [Steps]: {steps}")
    print(f"[Time]: {format_duration(elapsed_seconds)}   [Score]: {current_score}")
    print("Controls: w/a/s/d (Move) | e (Investigate) | i (Bag) | h (Hint) | save | load | q (Quit)")
    print("========================================")
    if msg:
        print(f"> {msg}")


def _save_game(path, levels, current_level_num, player_pos, inventory, steps,
               elapsed_seconds, hints_used, wrong_passwords):
    collected = []
    unlocked = []
    for number, level in levels.items():
        for row, col in level["clues"]:
            clue = level["clues"][(row, col)]
            if clue.get("collected"):
                collected.append(f"{number},{row},{col}")
            if clue.get("unlocked"):
                unlocked.append(f"{number},{row},{col}")
    lines = [
        "version=1",
        f"level={current_level_num}",
        f"position={player_pos[0]},{player_pos[1]}",
        f"inventory={'|'.join(inventory)}",
        f"steps={steps}",
        f"elapsed={elapsed_seconds}",
        f"hints={hints_used}",
        f"wrong_passwords={wrong_passwords}",
        f"collected={';'.join(collected)}",
        f"unlocked={';'.join(unlocked)}",
    ]
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")


def _load_game(path, original_levels):
    values = {}
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if "=" in line:
                key, value = line.rstrip("\n").split("=", 1)
                values[key] = value
    required = {"level", "position", "inventory", "steps", "elapsed",
                "hints", "wrong_passwords", "collected", "unlocked"}
    if not required.issubset(values):
        raise ValueError("save file is missing required data")
    levels = copy.deepcopy(original_levels)
    level = int(values["level"])
    if level not in levels:
        raise ValueError("save file contains an invalid chapter")
    position = [int(part) for part in values["position"].split(",")]
    if len(position) != 2:
        raise ValueError("save file contains an invalid position")
    for key, flag in (("collected", "collected"), ("unlocked", "unlocked")):
        for entry in values[key].split(";") if values[key] else []:
            number, row, col = [int(part) for part in entry.split(",")]
            clue = levels[number]["clues"][(row, col)]
            clue[flag] = True
            levels[number]["map"][row][col] = " "
    return {
        "level": level,
        "position": position,
        "inventory": values["inventory"].split("|") if values["inventory"] else [],
        "steps": int(values["steps"]),
        "elapsed_seconds": float(values["elapsed"]),
        "hints_used": int(values["hints"]),
        "wrong_passwords": int(values["wrong_passwords"]),
        "levels": levels,
    }


def _record_score(path, score_entry):
    scores = []
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 6:
                    scores.append({"score": int(parts[0]), "seconds": int(parts[1]),
                                   "steps": int(parts[2]), "hints": int(parts[3]),
                                   "wrong_passwords": int(parts[4]), "grade": parts[5]})
    except (OSError, ValueError):
        scores = []
    scores.append(score_entry)
    scores.sort(key=lambda item: (-item["score"], item["seconds"]))
    with open(path, "w", encoding="utf-8") as file:
        for item in scores[:10]:
            file.write(f"{item['score']}|{item['seconds']}|{item['steps']}|"
                       f"{item['hints']}|{item['wrong_passwords']}|{item['grade']}\n")
    return scores[:10]


def _score_message(elapsed_seconds, steps, hints_used, wrong_passwords):
    score = calculate_score(elapsed_seconds, steps, hints_used, wrong_passwords)
    grade = score_grade(score)
    return ("*** FINAL SCORE ***\n"
            f"Time: {format_duration(elapsed_seconds)} | Steps: {steps}\n"
            f"Hints: {hints_used} | Wrong passwords: {wrong_passwords}\n"
            f"Score: {score} ({grade})")


def run_game(input_func=input, levels=None, clear=True,
             save_path=DEFAULT_SAVE_PATH, scores_path=DEFAULT_SCORES_PATH,
             clock=None):
    """Run the game loop.

    ``input_func`` and ``levels`` can be replaced for testing. The level data is
    deep-copied so the global ``LEVELS`` is never modified. ``save_path`` and
    ``scores_path`` control local JSON files. ``clock`` is injectable for tests.
    """
    clock = clock or (lambda: os.times().elapsed)
    levels = copy.deepcopy(LEVELS if levels is None else levels)
    current_level_num = min(levels)
    inventory = []
    steps = 0
    hints_used = 0
    wrong_passwords = 0
    stored_elapsed = 0.0
    session_started = clock()

    def elapsed_seconds():
        return stored_elapsed + clock() - session_started

    level_data = levels[current_level_num]
    player_pos = list(level_data["start_pos"])
    status_msg = "You wake up in a cold room. Find a way out!"

    while True:
        render_screen(level_data, player_pos, status_msg, inventory, steps,
                      elapsed_seconds(), hints_used, wrong_passwords, clear)
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
        if cmd == "h":
            hints_used += 1
            status_msg = "Hint: " + level_data.get("hint", "Look around carefully. Every '?' hides something.")
        elif cmd == "save":
            try:
                _save_game(save_path, levels, current_level_num, player_pos, inventory,
                           steps, elapsed_seconds(), hints_used, wrong_passwords)
                status_msg = f"Game saved to {save_path}."
            except OSError as exc:
                status_msg = f"Could not save the game: {exc}"
        elif cmd == "load":
            try:
                state = _load_game(save_path, levels)
                levels = state["levels"]
                current_level_num = int(state["level"])
                level_data = levels[current_level_num]
                player_pos = list(state["position"])
                inventory = list(state["inventory"])
                steps = int(state["steps"])
                stored_elapsed = float(state["elapsed_seconds"])
                hints_used = int(state.get("hints_used", 0))
                wrong_passwords = int(state.get("wrong_passwords", 0))
                session_started = clock()
                status_msg = f"Game loaded from {save_path}."
            except (OSError, ValueError, TypeError) as exc:
                status_msg = f"Could not load the game: {exc}"
        elif cmd == "i":
            if not inventory:
                status_msg = "Your backpack is completely empty."
            else:
                details = ["--- Backpack Details ---"]
                for item in inventory:
                    details.append(f"* [{item}]: {ITEM_DESCRIPTIONS.get(item, 'No description available.')}")
                status_msg = "\n".join(details)
        elif cmd.isdigit():
            clue = level_data["clues"].get(tuple(player_pos))
            if clue and clue["type"] == "lock" and not clue["unlocked"]:
                if cmd == clue["password"]:
                    reward = clue["reward"]
                    clue["unlocked"] = True
                    inventory.append(reward)
                    level_data["map"][player_pos[0]][player_pos[1]] = " "
                    status_msg = f"Password correct! It clicks open. You obtained [{reward}]!"
                else:
                    wrong_passwords += 1
                    status_msg = f"You entered [{cmd}], but the lock buzzes red. Wrong password!"
            else:
                status_msg = "There is no lock here to enter a password into."
        elif cmd in MOVE_OFFSETS:
            dr, dc = MOVE_OFFSETS[cmd]
            next_r, next_c = player_pos[0] + dr, player_pos[1] + dc
            target_cell = level_data["map"][next_r][next_c]
            steps += 1
            if target_cell == "#":
                status_msg = "Bang! You bumped into a solid wall."
            elif target_cell == "D":
                door_info = level_data["door"]
                req_item = door_info["required_item"]
                if req_item in inventory:
                    print(f"\n*** {door_info['unlock_msg']} ***")
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
                        total_time = elapsed_seconds()
                        final_score = calculate_score(total_time, steps, hints_used, wrong_passwords)
                        print(_score_message(total_time, steps, hints_used, wrong_passwords))
                        _record_score(scores_path, {
                            "seconds": int(total_time),
                            "steps": steps,
                            "hints": hints_used,
                            "wrong_passwords": wrong_passwords,
                            "score": final_score,
                            "grade": score_grade(final_score),
                        })
                        print("*** CONGRATULATIONS! You have escaped all rooms and cleared the game! ***")
                        print(f"*** Total steps: {steps} | Total time: {format_duration(total_time)} ***\n")
                        return True
                else:
                    status_msg = door_info["locked_msg"]
            else:
                player_pos = [next_r, next_c]
                status_msg = ("You stepped onto something suspicious. Press 'e' to investigate."
                              if target_cell == "?" else "You take a step forward.")
        elif cmd == "e":
            clue = level_data["clues"].get(tuple(player_pos))
            if clue:
                if clue["type"] == "pickup":
                    status_msg = clue["text"]
                    if not clue["collected"]:
                        item = clue["item"]
                        inventory.append(item)
                        clue["collected"] = True
                        level_data["map"][player_pos[0]][player_pos[1]] = " "
                        status_msg += f"\n[OK] Obtained: [{item}] (Press 'i' anytime to inspect)"
                elif clue["type"] == "lock":
                    status_msg = ("This lock is already open and empty." if clue["unlocked"]
                                  else f"{clue['text']} (Type the numbers directly to unlock)")
            else:
                status_msg = "Nothing noteworthy here."
        else:
            status_msg = "Invalid command! Use w/a/s/d, e, i, h, save, load, q, or enter a password."


def main():
    """Console entry point (``secret-room`` command)."""
    run_game()


if __name__ == "__main__":
    main()
