import copy

import pytest

from group14_secret_room import LEVELS, run_game

# Optimal-ish walkthrough of both chapters.
CHAPTER_1_TO_CALENDAR = ["w", "w", "d", "d", "s", "s", "d", "d", "w", "w",
                         "d", "d", "d", "d", "d", "e"]
CHAPTER_1_TO_BOX = ["d", "s", "s", "s", "s", "a", "e"]
CHAPTER_1_TO_DOOR = ["d", "w", "w", "d"]

# Full walkthrough of both chapters ("" = press Enter between chapters).
SOLUTION = (
    CHAPTER_1_TO_CALENDAR + CHAPTER_1_TO_BOX + ["1024"] + CHAPTER_1_TO_DOOR + [""]
    + ["d", "d", "d", "s", "s", "d", "d", "w", "w", "d", "d", "d", "e",   # note
       "a", "a", "a", "s", "s", "s", "s", "a", "a", "a", "a", "a", "e",   # safe
       "345",
       "d", "d", "d", "d", "d", "w", "w", "d", "d", "s", "s", "d", "d", "d", "d"]
)


def feeder(commands):
    it = iter(commands)

    def _input(_prompt=""):
        try:
            return next(it)
        except StopIteration:
            raise EOFError
    return _input


@pytest.mark.parametrize("num", sorted(LEVELS))
def test_level_data_is_valid(num):
    level = LEVELS[num]
    grid = level["map"]
    assert len({len(row) for row in grid}) == 1, "map rows must be equal length"
    r, c = level["start_pos"]
    assert grid[r][c] == " ", "start position must be an empty floor tile"
    dr, dc = level["door"]["pos"]
    assert grid[dr][dc] == "D"
    for (cr, cc), clue in level["clues"].items():
        assert grid[cr][cc] == "?", f"clue at {(cr, cc)} must be marked '?'"
        assert clue["type"] in {"pickup", "lock"}
    rewards = {cl.get("reward") for cl in level["clues"].values()}
    assert level["door"]["required_item"] in rewards, "door key must be obtainable"


def test_full_walkthrough_wins(capsys):
    assert run_game(feeder(SOLUTION), clear=False) is True
    assert "CONGRATULATIONS" in capsys.readouterr().out


def test_global_levels_not_mutated_and_replayable():
    before = copy.deepcopy(LEVELS)
    assert run_game(feeder(SOLUTION), clear=False) is True
    assert LEVELS == before
    assert run_game(feeder(SOLUTION), clear=False) is True


def test_wrong_password_and_locked_door(capsys):
    cmds = (CHAPTER_1_TO_CALENDAR + CHAPTER_1_TO_BOX + ["0000"]
            + CHAPTER_1_TO_DOOR + ["q"])
    assert run_game(feeder(cmds), clear=False) is False
    out = capsys.readouterr().out
    assert "Wrong password" in out
    assert "You need a Brass Key" in out


def test_quit_and_eof():
    assert run_game(feeder(["q"]), clear=False) is False
    assert run_game(feeder([]), clear=False) is False


def test_hint_command(capsys):
    run_game(feeder(["h", "q"]), clear=False)
    assert "Hint:" in capsys.readouterr().out


def test_save_and_load(tmp_path, capsys):
    save_file = tmp_path / "save.txt"
    run_game(feeder(["w", "save", "q"]), clear=False,
             save_path=save_file, scores_path=tmp_path / "scores.txt")
    assert save_file.exists()
    run_game(feeder(["load", "i", "q"]), clear=False,
             save_path=save_file, scores_path=tmp_path / "scores.txt")
    assert "Game loaded" in capsys.readouterr().out


def test_score_helpers():
    from group14_secret_room.main import calculate_score, format_duration, score_grade

    assert format_duration(65) == "01:05"
    assert format_duration(3661) == "01:01:01"
    assert calculate_score(10, 20, 1, 2) == 9580
    assert score_grade(9500) == "A"
    assert score_grade(8000) == "B"
    assert score_grade(6500) == "C"
    assert score_grade(100) == "D"
