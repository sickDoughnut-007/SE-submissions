# Lab 4 - VibeCoding: Target Aim Trainer

**Name:** Akshay V Gudur  
**SRN:** PES1UG24CS047  
**Assigned project:** https://github.com/SETAPESU26/47_target-aim-trainer  
**Personal game repository:** https://github.com/sickDoughnut-007/47_target-aim-trainer

## Completed implementation

The `target-aim-trainer/` folder contains the updated Python/Pygame game and its tests.

| Task | Implemented behavior |
| --- | --- |
| Collision detection | Hit testing and drawing share the same integer shrinking radius; expired targets cannot be hit. |
| Game over | Results show score, accuracy, hits, and misses, and wait for input. |
| Replay and difficulty | Buttons or keys 1 / 2 / 3 start Easy / Medium / Hard rounds with reset statistics and timer. |
| Sound feedback | Distinct hit, miss, timeout, and round-end effects; M toggles mute. |

Controls: left click to shoot, M to mute/unmute, and Q / Esc to exit.
The first round starts on Medium; replay difficulty is selected at game over.

## Implementation commits

The required one debugging fix and three feature commits are published on `main`:

1. [f9bbbe9 - Collision fix](https://github.com/sickDoughnut-007/SE-submissions/commit/f9bbbe94282c0a29315a6842ae1fe81aa61e2793)
2. [7e5bbf1 - Game-over screen](https://github.com/sickDoughnut-007/SE-submissions/commit/7e5bbf1e23db245aba5703497518f4c675da7655)
3. [1c302a7 - Replay and difficulty](https://github.com/sickDoughnut-007/SE-submissions/commit/1c302a7dc5774cea5f487ec7ebe84c511c110b2d)
4. [9bdd092 - Sound feedback](https://github.com/sickDoughnut-007/SE-submissions/commit/9bdd092ee6b4a5af94c604b970a38f5d22657c65)

Additional commits upload the recordings, chat link, and submission documentation.

## Run and test

From `LAB 4/target-aim-trainer/`, with Python 3.10+ installed:

```text
python -m pip install -r requirements.txt
python main.py
python -m unittest discover -s tests -v
```

The implementation passed 14 automated checks and rendered-screen review.
Checks cover visible hit boundaries, expired targets, score freezing, timeout
misses, replay resets, target bounds, sound event dispatch, valid audio, mute,
and unavailable audio. Automated audio checks used an SDL dummy audio device.

The original 60 FPS frame-based timing is retained: each round lasts 1,800
updates, nominally 30 seconds; a slow machine can take longer in wall-clock time.

## Uploaded submission evidence

| File | Purpose | Status |
| --- | --- | --- |
| [videos/before.mp4](videos/before.mp4) | Original-game recording | Uploaded |
| [videos/after.mp4](videos/after.mp4) | Updated-game recording | Uploaded |
| [videos/push_recording.mp4](videos/push_recording.mp4) | Push and GitHub verification recording | Uploaded |
| [Chat_History.pdf](Chat_History.pdf) | Visible user/assistant conversation at export time | Uploaded |
| [Chat_Link.txt](Chat_Link.txt) | Shared ChatGPT conversation URL | Added |
| [Implementation_Notes.md](Implementation_Notes.md) | Task mapping, validation, and timing limitations | Included |

All listed evidence files are present in this repository. The PDF is the
conversation snapshot created during implementation; the shared link is supplied
alongside it. File presence was checked on GitHub; video playback, duration, and
audible feedback have not been independently reviewed.
