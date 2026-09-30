# Lab 4 - VibeCoding: Target Aim Trainer

**Name:** Akshay V Gudur  
**SRN:** PES1UG24CS047  
**Assigned project:** https://github.com/SETAPESU26/47_target-aim-trainer

## Code and commits

The `target-aim-trainer/` folder contains the updated Python game and its tests.
Four commits implement the assigned tasks independently:

1. `fix(lab4): match hit detection to the visible shrinking target`
2. `feat(lab4): show final score and accuracy on a game-over screen`
3. `feat(lab4): replay rounds with easy medium and hard difficulty`
4. `feat(lab4): add hit miss and round-end sound feedback`

Run from `target-aim-trainer/`:

```text
python -m pip install -r requirements.txt
python main.py
python -m unittest discover -s tests -v
```

The game has been verified with 14 automated checks and rendered-screen review.
The checks cover visible hit boundaries, expired targets, score freezing, timeout
misses, replay resets, target bounds, sound event dispatch, valid audio, mute,
and handling of unavailable audio. Audio must also be heard on the local computer.

## Submission evidence

- `Chat_History.pdf`: the user/assistant conversation available at export time.
- `Implementation_Notes.md`: task mapping, validation, and limitations.
- `videos/`: instructions for the actual before/after and push recordings.
- `Chat_Link.txt`: add the shared link of this ChatGPT conversation, as requested by the assigned README.

The recordings and chat link are pending until supplied by the student. No claim
of a local screen recording or completed remote push is made by these files.
Follow `START_HERE.md` in the handoff ZIP to clone the game on your computer,
record the original version, switch to the finished branch, and push to your
personal fork and this submission repository. Do not raise a PR to SETAPESU26.
