"""Render the ~20 s how-to-play demo video (docs/demo.mp4) from the real game.

Usage: python scripts/make_demo.py <frames_dir> <output.mp4>   (needs Pillow and ffmpeg)
"""
import io
import os
import subprocess
import sys
from contextlib import redirect_stdout

from PIL import Image, ImageDraw, ImageFont

from group14_secret_room import run_game

OUT_DIR = sys.argv[1]
VIDEO = sys.argv[2]
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1280, 720
BG = (18, 20, 28)
TERM_BG = (28, 31, 42)
BAR = (44, 48, 62)
FG = (220, 223, 228)
DIM = (130, 136, 150)
ACCENT = (255, 196, 64)
GREEN = (120, 220, 140)
CYAN = (110, 200, 240)
RED = (240, 110, 110)

MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype("DejaVuSansMono.ttf", size)


F_TERM = font(MONO, 20)
F_TERM_B = font(MONO_B, 20)
F_CAP = font(SANS_B, 30)
F_TITLE = font(SANS_B, 64)
F_SUB = font(SANS, 30)
F_SMALL = font(SANS, 24)
F_CODE = font(MONO_B, 30)

# ---------------------------------------------------------------- capture
CMDS = (["w", "w", "d", "d", "s", "s", "d", "d", "w", "w", "d", "d", "d", "d", "d", "e", "i"]
        + ["d", "s", "s", "s", "s", "a", "e", "1024"]
        + ["d", "w", "w", "d", ""]
        + ["h", "q"])

screens = []  # (screen_text, prompt, command_typed)
buf = io.StringIO()
cmd_iter = iter(CMDS)


def fake_input(prompt=""):
    text = buf.getvalue()
    buf.seek(0)
    buf.truncate()
    cmd = next(cmd_iter)
    screens.append((text.rstrip("\n"), prompt, cmd))
    return cmd


with redirect_stdout(buf):
    run_game(fake_input, clear=False)
final_text = buf.getvalue()

# ---------------------------------------------------------------- drawing
frames = []  # (PIL image, seconds)


def color_for(line):
    if line.startswith("===") and "Chapter" in line:
        return ACCENT
    if line.startswith(">"):
        if "Wrong" in line or "bumped" in line:
            return RED
        return GREEN
    if line.startswith("*") or "[OK]" in line or "***" in line:
        return GREEN
    if line.startswith("[Backpack]"):
        return CYAN
    if line.startswith("Controls") or line.startswith("====="):
        return DIM
    return FG


def terminal(lines, caption=None, cursor=True):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = 36, 30, W - 36, H - 100
    d.rounded_rectangle((x0, y0, x1, y1), 14, fill=TERM_BG)
    d.rounded_rectangle((x0, y0, x1, y0 + 36), 14, fill=BAR)
    d.rectangle((x0, y0 + 22, x1, y0 + 36), fill=BAR)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse((x0 + 18 + i * 24, y0 + 11, x0 + 32 + i * 24, y0 + 25), fill=c)
    d.text(((x0 + x1) // 2, y0 + 18), "secret-room — Terminal", font=F_SMALL,
           fill=DIM, anchor="mm")
    lh = 27
    max_lines = (y1 - y0 - 60) // lh
    lines = lines[-max_lines:]
    y = y0 + 50
    for ln in lines:
        x = x0 + 24
        if "@" in ln and ln.startswith("#"):
            # map row: highlight player and special tiles
            for ch in ln:
                col = {"@": ACCENT, "?": CYAN, "D": GREEN, "#": DIM}.get(ch, FG)
                f = F_TERM_B if ch in "@?D" else F_TERM
                d.text((x, y), ch, font=f, fill=col)
                x += d.textlength(ch, font=F_TERM)
        elif ln.startswith("#"):
            for ch in ln:
                col = {"?": CYAN, "D": GREEN, "#": DIM}.get(ch, FG)
                f = F_TERM_B if ch in "?D" else F_TERM
                d.text((x, y), ch, font=f, fill=col)
                x += d.textlength(ch, font=F_TERM)
        else:
            d.text((x, y), ln, font=F_TERM, fill=color_for(ln))
        y += lh
    if cursor:
        last = lines[-1] if lines else ""
        cx = x0 + 24 + d.textlength(last, font=F_TERM) + 2
        d.rectangle((cx, y - lh + 3, cx + 10, y - 3), fill=FG)
    if caption:
        d.text((W // 2, H - 50), caption, font=F_CAP, fill=ACCENT, anchor="mm")
    return img


def card(title, subtitle_lines, code=None):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((W // 2, 230), title, font=F_TITLE, fill=ACCENT, anchor="mm")
    y = 320
    for s in subtitle_lines:
        d.text((W // 2, y), s, font=F_SUB, fill=FG, anchor="mm")
        y += 46
    if code:
        y += 30
        for c in code:
            tw = d.textlength(c, font=F_CODE)
            d.rounded_rectangle((W / 2 - tw / 2 - 24, y - 30, W / 2 + tw / 2 + 24, y + 30),
                                10, fill=TERM_BG)
            d.text((W // 2, y), c, font=F_CODE, fill=GREEN, anchor="mm")
            y += 80
    return img


def add(img, sec):
    frames.append((img, sec))


def how_to_play():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((W // 2, 70), "How to Play", font=F_TITLE, fill=ACCENT, anchor="mm")
    d.text((W // 2, 135), "Goal: find clues, crack the lock, take the key, escape through the door",
           font=F_SMALL, fill=FG, anchor="mm")
    left = [("w a s d", "Move"), ("e", "Investigate a ? tile"), ("i", "Inspect your backpack"),
            ("1234", "Type digits to enter a password"), ("h", "Get a hint"), ("q", "Quit")]
    right = [("@", "You", ACCENT), ("?", "Clue / item / lock", CYAN),
             ("D", "Door to next chapter", GREEN), ("#", "Wall", DIM)]
    d.text((150, 190), "Controls", font=F_CAP, fill=CYAN)
    y = 245
    for k, v in left:
        tw = d.textlength(k, font=F_CODE)
        d.rounded_rectangle((150, y - 22, 150 + tw + 24, y + 22), 8, fill=TERM_BG)
        d.text((162, y), k, font=F_CODE, fill=GREEN, anchor="lm")
        d.text((330, y), v, font=F_SMALL, fill=FG, anchor="lm")
        y += 62
    d.text((790, 190), "Map", font=F_CAP, fill=CYAN)
    y = 245
    for sym, v, col in right:
        d.rounded_rectangle((790, y - 24, 838, y + 24), 8, fill=TERM_BG)
        d.text((814, y), sym, font=F_CODE, fill=col, anchor="mm")
        d.text((862, y), v, font=F_SMALL, fill=FG, anchor="lm")
        y += 62
    d.text((W // 2, H - 50), "Type a command, then press Enter", font=F_CAP,
           fill=ACCENT, anchor="mm")
    return img


# 1. Title (1.5 s)
add(card("Secret Room Adventure",
         ["A text-based escape-room puzzle game in Python",
          "CS1302A · Group 14"]), 1.5)

# 1b. How to play (3.2 s)
add(how_to_play(), 3.2)

# 2. Install + launch (2.6 s)
shell = []
for typed, out, hold in [("$ pip install group14_secret_room",
                          ["Successfully installed group14_secret_room-0.1.0"], 0.5),
                         ("$ secret-room", [], 0.25)]:
    for k in range(0, len(typed) + 1, 3):
        add(terminal(shell + [typed[:k]], "Install from PyPI with one command"), 0.028)
    shell += [typed] + out
    add(terminal(shell, "Install from PyPI with one command"), hold)

# 3. Gameplay
CAPTIONS = {
    15: "Press e to investigate the ? tile",
    16: "You found a Calendar! Press i to read it",
    17: "October 24th is circled... remember it!",
    23: "Investigate the locked box",
    24: "The password is the date: 10/24 -> 1024",
    25: "Correct! You got the Brass Key",
    29: "Walk into the door D to unlock it",
    30: "Chapter 2! Stuck? Press h for a hint",
    31: "Chapter 2! Stuck? Press h for a hint",
}
HOLD = {15: 0.5, 16: 0.6, 17: 1.2, 23: 0.5, 24: 0.9, 25: 0.8, 29: 1.0, 30: 0.5, 31: 1.3}


def caption_for(idx):
    if idx in CAPTIONS:
        return CAPTIONS[idx]
    if idx < 15:
        return "Move with w / a / s / d  -  walk to a ? tile"
    if idx < 23:
        return "Next ? tile: a locked box"
    return "Now head for the door D"


prev = []
for idx, (text, prompt, cmd) in enumerate(screens):
    cap = caption_for(idx)
    if not text.startswith("==="):
        # e.g. the door-unlock message: show it below the previous screen, as a real terminal would
        text = "\n".join(prev + text.lstrip("\n").split("\n"))
    lines = text.split("\n") + [prompt]
    prev = text.split("\n") + [prompt + cmd]
    add(terminal(lines, cap), HOLD.get(idx, 0.11))
    if cmd and cmd != "q":
        add(terminal(text.split("\n") + [prompt + cmd], cap, cursor=False),
            0.06 if idx not in HOLD else (0.12 if len(cmd) == 1 else 0.45))

# 4. End card (3.0 s)
add(card("Try it yourself!", ["pypi.org/project/group14_secret_room",
                              "github.com/zekaipeng14-netizen/1302A-Group14"],
         ["pip install group14_secret_room", "secret-room"]), 2.6)

# ---------------------------------------------------------------- encode
total = sum(s for _, s in frames)
print(f"{len(frames)} frames, {total:.1f} s")
listing = os.path.join(OUT_DIR, "list.txt")
with open(listing, "w") as fh:
    for i, (img, sec) in enumerate(frames):
        p = os.path.join(OUT_DIR, f"f{i:04d}.png")
        img.save(p)
        fh.write(f"file '{p}'\nduration {sec:.3f}\n")
    fh.write(f"file '{p}'\n")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                "-i", listing, "-vf", "fps=30,format=yuv420p", "-c:v", "libx264",
                "-crf", "20", "-movflags", "+faststart", VIDEO], check=True)
print("wrote", VIDEO)
