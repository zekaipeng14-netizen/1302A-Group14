# Content for the Moodle "Project Presentation Page" wiki

Two ways to update the group14 wiki page:

- **Easiest:** open the page editor, switch to the HTML / source-code view (the `</>` or `<>` button; on some editors it is under the `...` menu), delete everything, paste the HTML block below, then switch back and save.
- Or copy the text in the "Plain version" section and format the lists by hand.

## HTML version

```html
<h3>Secret Room Adventure — Group 14</h3>
<p>A text-based escape-room puzzle game in pure Python, published on PyPI.</p>
<ul>
  <li><strong>Repository:</strong> <a href="https://github.com/zekaipeng14-netizen/1302A-Group14">https://github.com/zekaipeng14-netizen/1302A-Group14</a></li>
  <li><strong>PyPI:</strong> <a href="https://pypi.org/project/group14_secret_room/">https://pypi.org/project/group14_secret_room/</a> (version 0.1.1)</li>
  <li><strong>Install and play:</strong> <code>pip install group14_secret_room</code>, then run <code>secret-room</code></li>
  <li><strong>Demo video (20 s):</strong> <a href="https://github.com/zekaipeng14-netizen/1302A-Group14/blob/main/docs/demo.mp4">docs/demo.mp4</a></li>
</ul>
<p><strong>Motivation:</strong> Escape rooms train observation and deduction. We wanted to build a complete, replayable puzzle game using only core Python data structures.</p>
<p><strong>Innovation:</strong></p>
<ul>
  <li>Data-driven levels: each room is a dictionary, so you can add rooms without touching the engine.</li>
  <li>A clue chain: pickup items → deduced passwords → keys → doors.</li>
  <li>Backpack inspection, a hint system and a step counter.</li>
  <li>Save/load progress, plus a score system (time, hints, wrong passwords) with a top-10 leaderboard.</li>
  <li>Fully automated tests that play the whole game (GitHub Actions CI).</li>
</ul>
<p><strong>Example use cases:</strong> a quick puzzle break; teaching lists, dictionaries and game loops; designing your own escape room; a challenge mode where you compete for a high score.</p>
<p><strong>Team:</strong> PENG Zekai, HE Tsz Fei, GUI Yifei, GUO Songlin, LI Jianheng</p>
<p><strong>Demo materials:</strong> demo video <code>docs/demo.mp4</code> and demo script <code>docs/DEMO.md</code> in the repository.</p>
```

## Plain version

**Secret Room Adventure — Group 14**

A text-based escape-room puzzle game in pure Python, published on PyPI.

- **Repository:** https://github.com/zekaipeng14-netizen/1302A-Group14
- **PyPI:** https://pypi.org/project/group14_secret_room/ (version 0.1.1)
- **Install and play:** `pip install group14_secret_room`, then run `secret-room`
- **Demo video (20 s):** https://github.com/zekaipeng14-netizen/1302A-Group14/blob/main/docs/demo.mp4

**Motivation:** Escape rooms train observation and deduction. We wanted to build a complete, replayable puzzle game using only core Python data structures.

**Innovation:**
- Data-driven levels: each room is a dictionary, so you can add rooms without touching the engine.
- A clue chain: pickup items → deduced passwords → keys → doors.
- Backpack inspection, a hint system and a step counter.
- Save/load progress, plus a score system (time, hints, wrong passwords) with a top-10 leaderboard.
- Fully automated tests that play the whole game (GitHub Actions CI).

**Example use cases:** a quick puzzle break; teaching lists, dictionaries and game loops; designing your own escape room; a challenge mode where you compete for a high score.

**Team:** PENG Zekai, HE Tsz Fei, GUI Yifei, GUO Songlin, LI Jianheng

**Demo materials:** demo video `docs/demo.mp4` and demo script `docs/DEMO.md` in the repository.
