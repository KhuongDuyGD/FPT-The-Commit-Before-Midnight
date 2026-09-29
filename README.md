# FPT: 23:59 Escape Protocol

A complete Ren'Py visual novel with the original escape story and Chapter 2,
**LOVE PROTOCOL**, based on the supplied Chapter 2 narrative brief.
The game now follows the new full-day screenplay, preserving its Vietnamese
dialogue, jokes, choices, and extended night route. The supplied FPTU/KTX art
is used for the cast and locations, with generated placeholder WAV cues. The
bad ending uses `MainExhaust.png`; the old skeleton image is not displayed.

## Run

Open this folder as a project in Ren'Py 8.5 or newer and choose **Launch Project**. The
project uses a 1280×720 virtual resolution. Ren'Py itself is not included.

To use this inside another normal Ren'Py project, copy the entire `game` folder
and replace that project's starter `script.rpy`, `screens.rpy`, and `options.rpy`
with the files here. Avoid keeping duplicate screen or label definitions.

## Controls

- Click, Enter, or Space: advance dialogue
- Mouse wheel up, Page Up, or **Back**: rollback
- **Skip** and **Auto**: quick menu above the dialogue box
- **Save**, **Load**, **History**, **Prefs**: quick menu above the dialogue box
- Esc or right click: game menu

The Ending Gallery records all five endings across playthroughs. Chapter 1
endings offer **Return to Main Menu** and **Start New Game+**. New Game+ resets
the starting stats and shows “Difficulty Unlocked: SENIOR YEAR.”

Chapter 1's Good Ending opens **Tiếp tục Chương 2**. After unlocking it, choose
**Chapter Select → Chương 2 — LOVE PROTOCOL** to start it directly. Players who
already obtained the original Good Ending automatically qualify. Chapter 2
has hidden relationship stats and a shared allowance of three **Hỏi Ngân**
hints. Ordinary dialogue with Ngân does not spend a hint. Chapter 3 is teased
after Nghi's Good Ending; it has no playable content in this release.

Windows playtest builds are in `dist`. Extract the entire `3.1-win.zip` package
and open `FPT2359EscapeProtocol.exe`; keep its `game`, `lib`, and `renpy` folders
beside it. See [CHAPTER2.md](CHAPTER2.md) for implementation and route details.

## Files

- `game/script.rpy`: prologue, scenes, choices, and route checks
- `game/variables.rpy`: story stats, flags, gallery state, ending condition
- `game/characters.rpy`: cast and image declarations
- `game/screens.rpy`: HUD, dialogue, menus, gallery, ending cards
- `game/endings.rpy`: both endings and New Game+
- `game/audio.rpy`: sound cue names and flash transition
- `game/options.rpy`: project settings
- `tools/build_story.py`: one-time importer for this exact v2.0 screenplay
- `game/chapter2.rpy`: scenes CH2_00–CH2_12 and relationship choices
- `game/chapter2_endings.rpy`: Nghi Good/Bad and Ngân secret endings
- `game/chapter2_state.rpy`: save defaults, migration, hints, unlocks, resolver
- `game/chapter2_assets.rpy`: new characters, expressions, maps and CGs
- `game/stage.rpy`: story presence, directed shots, fades and speaker focus
- `game/chapter_screens.rpy`: Chapter Select, hint messages and ending UI
- `game/chapter2_testcases.rpy`: chapter, hint, save and ending engine tests
- `game/polish_testcases.rpy`: composition, layout, height and Continue regressions
- `tools/build_chapter2.py`: attributed dialogue importer for the supplied brief
- `tools/generate_placeholders.py`: reproducible placeholder assets

## Character visibility

Scene labels call `set_stage(...)` with the story-present cast and an optional
`visual=(...)` composition. `set_shot(...)` changes the camera composition
without making anyone leave the room. Most shots contain two characters;
normal shots are capped at three. `stage.rpy` brightens the current speaker,
draws them in front, and gently dims/scales other visible participants over
0.2 seconds. Entrances/exits fade over 0.25 seconds; expressions crossfade over
0.15 seconds. Phone hints leave the physical shot unchanged. All standees,
including the philosophy teacher, PE teacher and nurse, scale proportionally
to the same 620-pixel base height. The PLAYER expression changes by scene, so
the morning and night route use `MainExhaust.png`, the Windows and LMS conflicts
use `MainAngry.png`, the deadline shock uses `MainCry.png`, and the successful
escape uses `MainGoodMood.png`. Chapter 2 adds empathy, embarrassment, sadness,
surprise and delight using the new expression artwork.

## Main menu art

`GameMainMenu.png` supplies the title-screen backdrop. `LogoGame.png` replaces
the menu's text title, and the menu buttons remain clickable Ren'Py controls.
`GameIcon.png` is the game window icon.

Normal launches always open the main menu. Continue loads the latest save
only when selected. New Game, Chapter Select and in-game chapter continuation
retain their existing behavior. Dialogue uses a fixed 204-pixel bottom panel;
choices expand upward above the quick menu, and hints overlay the choice area.

## Tuning the routes

Choice deltas are next to their menu entries in `game/script.rpy`. The GOOD
ENDING requires choosing **Về.**, `escape_point >= 4`, `energy > 0`, and
`pending_tasks <= 2`. Choosing to stay, running out of energy, reaching six
pending tasks, or attempting to leave without the required stats enters the
BAD ENDING route. The screenplay's morning attendance is recorded on arrival;
the late assignment adds one pending task and is marked uploaded in the night
route. The meeting's `PendingTasks -1` is clamped to zero so the HUD never shows
a negative task count.

`characters.rpy` maps `FPTUday.png` to the daytime campus view (replacing the
missing `FPTUanime.png`). `KTXAfternoon.png` is declared for a future afternoon
dorm scene; the 18:02 ending uses `KTXNight.png`. The afternoon gate and
classroom scenes reuse their day paintings until dedicated assets exist. Extra
canteen time-of-day variants are declared for future scenes. To replace a sound
cue, update its path in `audio.rpy`.

## Verification

`game/testcases.rpy` contains Ren'Py engine tests for both endings, a failed
escape, and the supporting menus. In a Ren'Py 8.5 SDK, run
`renpy.py <project> lint --error-code` and
`renpy.py --savedir <isolated-test-folder> <project> test --overwrite-screenshots`.
Use a separate save folder for tests so simulated ending unlocks do not alter
your actual gallery. Screenshot captures are for visual inspection; overwrite
them when testing different parameterized routes or transition timing.
