# Implementation notes

Akshay V Gudur - PES1UG24CS047

## Task 1: collision bug

At age 80 of 90 frames, the original target draws a circle with an integer radius
of 15 px but accepts a hit 30 px away, because it checks against its initial
40 px radius. `Target.drawn_radius()` now supplies the same integer radius for
drawing and hit testing. Expired targets are rejected. Only left clicks score.

## Task 2: game over

The results screen replaces the playfield after the countdown reaches zero and
shows score, accuracy, hits, and misses. Updates and shooting cannot change the
finished statistics. Q / Esc or the window close button exits gracefully.

## Task 3: replay and difficulty

Easy, Medium, and Hard use different starting/minimum radii and lifespans.
Buttons and keys 1/2/3 restart the game after the results screen. Score, hits,
misses, time remaining, and target age are reset. A replay click does not count
as a shot. Easy target bounds leave space for the bottom control text.

## Task 4: sound

Standard-library code produces WAV tones in memory for hit, miss, and round end.
The timeout path plays the miss effect. Round end fires once. M toggles mute and
stops effects already playing; audio initialization failure leaves gameplay usable.
No downloaded media assets or extra dependency is required beyond pygame.

## Validation

14 tests passed with Python 3.12.14 and pygame 2.6.1 using SDL dummy display/audio.
All three difficulties were simulated for a complete 1,800-update round.
The gameplay and game-over screens were rendered and visually inspected.
The original bug was reproduced before editing and is covered by a regression test.
This is simulated validation, not a recording of the student's laptop.

## Limits and student completion

Original frame-based timing is retained: nominal round length is 30 seconds at
60 FPS; lag can extend elapsed wall-clock time. Check audible feedback locally.
The actual recordings, real shared-chat link, personal fork creation, and recorded
push remain to be performed by the student. The four implementation commits are
prepared locally and have not been pushed. Adding video evidence may create a
fifth or later commit, which still satisfies the minimum of four.
