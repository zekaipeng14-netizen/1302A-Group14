# --- 1. Initialize Data ---
room_map = [
    ["#", "#", "#", "#", "#", "#", "#"],
    ["#", ".", ".", ".", "?", ".", "#"], # (1, 4) is the Calendar
    ["#", ".", "#", "#", ".", ".", "D"], # (2, 6) is the Door
    ["#", ".", ".", ".", ".", "?", "#"], # (3, 5) is the Iron Box
    ["#", "#", "#", "#", "#", "#", "#"]
]

player_pos = [3, 3]

# Item descriptions and initial items
clues_data = {
    (1, 4): {
        "text": "There is a calendar on the desk, with [October 24th] circled in red pen.",
        "item": "Calendar"
    },
    (3, 5): {
        "text": "A locked iron box with a 4-digit combination lock on it.",
        "item": None
    }
}

inventory = []  # Backpack
is_box_open = False  # Whether the iron box is open

move_offsets = {
    "w": (-1, 0),
    "s": (1, 0),
    "a": (0, -1),
    "d": (0, 1)
}

# --- 2. Screen Rendering Function ---
def render_screen(grid, pos, msg, inv):
    print("\n" * 20)
    print("=== Escape the Secret Room: Chapter 1 ===")
    for r in range(len(grid)):
        line = []
        for c in range(len(grid[r])):
            if r == pos[0] and c == pos[1]:
                line.append("@")
            elif (r, c) == (3, 5) and is_box_open:
                # If the box is open, turn the iron box into flat ground
                line.append(".")
            else:
                line.append(grid[r][c])
        print(" ".join(line))
    print("========================")
    print(f"[Backpack]: {inv if inv else 'Empty'}")
    print("========================")
    if msg:
        print(f"> {msg}")

# --- 3. Main Game Loop ---
status_msg = "You wake up and find yourself in a secret room. Use w/a/s/d to move, e to investigate, q to quit"

while True:
    render_screen(room_map, player_pos, status_msg, inventory)
    cmd = input("Please enter command: ").strip()

    if cmd == "q":
        print("Game exited.")
        break

    # ========== Handle Numeric Password 1024 ==========
    if cmd == "1024":
        r, c = player_pos
        if (r, c) == (3, 5) and not is_box_open:
            status_msg = "Password correct! With a click, the iron box opens. You find a [Brass Key] lying quietly inside!"
            inventory.append("Brass Key")
            is_box_open = True
        else:
            status_msg = "There is nothing here to enter a password into."
    
    # ========== Handle Movement Logic ==========
    elif cmd in move_offsets:
        dr, dc = move_offsets[cmd]
        next_r = player_pos[0] + dr
        next_c = player_pos[1] + dc
        target_cell = room_map[next_r][next_c]
        
        # Hit a wall
        if target_cell == "#":
            status_msg = "Bang! You bumped into a cold wall. This way is blocked."
        # Hit a door
        elif target_cell == "D":
            if "Brass Key" in inventory:
                print("\n*** You take out the Brass Key and give it a gentle twist. Click, the door is open! ***")
                print("*** You have successfully escaped the secret room! Congratulations on clearing the game! ***\n")
                break
            else:
                status_msg = "The door is tightly locked. You need a key to open it."
        else:
            player_pos = [next_r, next_c]
            status_msg = "You take a step forward."

    # ========== Handle Investigation Logic (e) ==========
    elif cmd == "e":
        r, c = player_pos
        current_pos = (r, c)
        
        if current_pos in clues_data:
            info = clues_data[current_pos]
            
            # If the iron box is already open
            if (r, c) == (3, 5) and is_box_open:
                status_msg = "The iron box is already open, and it is empty inside."
            else:
                status_msg = info["text"]
                # Get item
                item = info["item"]
                if item and item not in inventory:
                    inventory.append(item)
                    status_msg += f"\n[OK] You obtained the item: [{item}]"
                    # After taking the calendar, the calendar disappears from the map
                    if item == "Calendar":
                        room_map[1][4] = "."
        else:
            status_msg = "There is nothing noteworthy here."

    else:
        status_msg = "Invalid command! Please use w/a/s/d to move, e to investigate, or enter the password in front of the iron box."