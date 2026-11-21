# Content for the Moodle "Project Presentation Page" wiki

Copy the section below into the group14 wiki page.

---

## Secret Room Adventure — Group 14

A text-based escape-room puzzle game in pure Python, published on PyPI.

- **Repository:** https://github.com/zekaipeng14-netizen/1302A-Group14
- **PyPI:** https://pypi.org/project/group14_secret_room/
- **Install and play:** `pip install group14_secret_room`, then `secret-room`

**Motivation:** Escape rooms train observation and deduction. We wanted to build a complete, replayable puzzle game using only core Python data structures.

**Innovation:**
- Data-driven levels: each room is a dictionary, so you can add rooms without touching the engine.
- A clue chain of pickup items → deduced passwords → keys → doors.
- Backpack inspection, a hint system and a step counter.
- Fully automated tests that play the whole game (GitHub Actions CI).

**Example use cases:** a quick puzzle break, teaching lists, dictionaries and game loops, and designing your own escape room.

**Team:** zekaipeng14-netizen, Fenice723, guiyifei1014-boop, guosonglin999-hue

**Demo materials:** see `docs/DEMO.md` in the repository.
