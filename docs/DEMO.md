# 1-Minute Demo Script

**Before class:** run `pip install group14_secret_room` on the lecture-room computer, open a terminal, and make the font large.

| Time | Say | Do |
|---|---|---|
| 0:00–0:10 | "We built **Secret Room Adventure**, a terminal escape-room game published on PyPI. Anyone can install it with one command." | Show `pip install group14_secret_room`, then type `secret-room`. |
| 0:10–0:35 | "You are `@`. Walk around, investigate `?` tiles, and deduce passwords from the clues." | Pick up the calendar (`e`), press `i` to show *October 24th*, walk to the box, and type `1024` to get the Brass Key. |
| 0:35–0:45 | "Use the key on the door to reach the next chapter. Press `h` any time for a hint." | Walk into `D`, then press `h` in Chapter 2. |
| 0:45–1:00 | "The innovation is data-driven design: each level is just a dictionary, so new rooms need no engine changes. The whole game is automatically tested on GitHub Actions." | Show the "Adding your own level" section of the README, or `pytest` passing. |

**Fast route for Chapter 1:**
`w w d d s s d d w w d d d d d e` → `d s s s s a e` → `1024` → `d w w d`

## Possible Q&A

- **Why a terminal game?** It needs no dependencies, runs anywhere Python runs, and lets the player focus on logic.
- **How do you add a level?** Add a dictionary to `LEVELS`. The test suite validates it automatically.
- **How do you test an interactive game?** `run_game()` takes an `input_func`. The tests feed it a scripted list of commands and check that the player wins.
- **What would you add next?** More chapters, a save/load feature, a timer leaderboard, and loading levels from JSON files.
