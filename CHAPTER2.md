# Chapter 2 implementation audit — v3.0

## Files created

| File | Responsibility |
| --- | --- |
| `game/chapter2.rpy` | Thirteen main scene labels, menus, relationship deltas |
| `game/chapter2_endings.rpy` | Nghi acceptance/refusal, pub scene, Ngân ending |
| `game/chapter2_state.rpy` | Defaults, unlock migration, hint budget, ending checks |
| `game/chapter2_assets.rpy` | Five new Characters, remote message Character, images |
| `game/stage.rpy` | Physical presence, speaker focus, expression mapping |
| `game/chapter_screens.rpy` | Chapter Select, continuation, hints, gallery rows, CG cards |
| `game/chapter2_testcases.rpy` | Engine tests using menu clicks and saved games |
| `tools/build_chapter2.py` | Reproducible import of attributed Vietnamese dialogue |
| `CHAPTER2.md` | This audit and tuning notes |

## Files modified

`characters.rpy` connects the existing cast to the focus callback and resizes
the menu logo to accommodate Chapter Select. `screens.rpy` removes the old
single-speaker-only sprite, wraps long choices and adds hints and five gallery
entries. `script.rpy` and `endings.rpy` gain physical cast annotations and the
Chapter 1 continuation/unlock. Their original dialogue and choice deltas are
preserved. `tools/build_story.py` retains these annotations on regeneration.
`options.rpy` changes the release version to 3.0 and excludes tests, saves and
the implementation brief from builds. `testcases.rpy` checks Chapter 1
regressions and the new continuation. README documents play and development.

## New state

Ren'Py `default` makes these save-local values serializable and rollback aware:

- `current_chapter`, `save_schema_version = 3`, `chapter1_canonical_result`;
- `chapter2_started`, `chapter2_completed`, `chapter2_ending`;
- `NghiAffinity`, `NghiComfort`, `NganAffinity`, `NganSpecialFlags`;
- `NganHintsRemaining = 3`, `NganHintsUsed = 0`, `NganEndingAvailable`;
- `CH2MajorFail`, `game_route_complete`, `chapter3_route_locked_for_this_save`;
- `ch2_hint_context`, `ch2_hint_used_choices`, `ch2_sports_choice`;
- `ngan_expression`, `nghi_expression`, `stage_cast`, `stage_visual`, `stage_focus`, `stage_images`.

Persistent values: `chapter2_unlocked`, `chapter1_canonical_result`,
`ending_nghi_good_unlocked`, `ending_nghi_bad_unlocked`, `ending_ngan_unlocked`.
Existing Chapter 1 ending flags remain compatible. On startup, an existing
`good_ending_unlocked` migrates to the Chapter 2 unlock. Older saves receive
the new defaults; `after_load` restores the stage and schema version.

## Scene flow

| Label | Location/event |
| --- | --- |
| `CH2_00` | Next morning gate; escape was temporary |
| `CH2_01` | Hallway reunion with Ngân; hidden compliment |
| `CH2_02` | Philosophy morning; Nghi's introduction |
| `CH2_03` | Group discussion; first contact |
| `CH2_04` | Hallway; dating assistant and rehearsal joke |
| `CH2_05` | Afternoon library; quiet bonding and coding conversation |
| `CH2_06` | Following morning sports field; PE boss and Ngân help |
| `CH2_07` | Afternoon infirmary; honesty and supportive follow-ups |
| `CH2_08` | Philosophy afternoon; contradictions |
| `CH2_09` | Afternoon courtyard; understanding Nghi |
| `CH2_10` | Canteen afternoon; drink and Ngân character event |
| `CH2_11` | Rooftop afternoon; advice and eligible hidden branch |
| `CH2_12` | Rooftop sunset; final confession |
| `CH2_nghi_good` | Rooftop CG, post-credit conversation, Chapter 3 tease |
| `CH2_nghi_bad`, `CH2_pub` | Gentle refusal and nighttime pub with Minh |
| `CH2_ngan_ending` | Sincere realization and school-gate hand-pull CG |

The library afternoon precedes PE the following morning, avoiding a backwards
time jump. CH2_09 uses the brief's permitted afternoon courtyard alternative.

## UI and staging

Main menu offers Continue, New Game, Chapter Select, Load, Ending Gallery, Settings, Quit.
Chapter Select displays Chapter 2 locked until Chapter 1 Good Ending. Direct
selection initializes a fresh, canonical Chapter 1 Good result. Continuing
after Chapter 1 does the same initialization in the current playthrough.

The story cast (`stage_cast`) is separate from the active shot (`stage_visual`).
Directed shots usually contain two actors and never exceed three. Active:
full tint/opacity, normal scale, z-order 20. Inactive: tint `#b8b8c4`,
scale 0.96 and lower z-order, with a 0.2-second focus tween. Narration restores
neutral emphasis. Story-present offscreen speakers can receive a brief cutaway.
Normal focus changes reuse sprites; entrances/exits fade for 0.25 seconds and
expressions crossfade for 0.15 seconds. Nghi's introduction uses a subtle scale
fade and her infirmary arrival uses a 20-pixel rise. The optional 35-pixel slide
remains available but no current scene needs it.
All actors/expressions use proportional 620-pixel height scaling, including
MissPhilosophy, PhysicalTeacher and Nurse. Nghi's medical-room exit explicitly
removes her from story presence; camera changes do not. Phone messages are
remote. Chapter 1 dialogue and route logic remain unchanged.

The shared dialogue panel keeps its 204-pixel height and bottom anchor during
dialogue, choices and hints. Choices wrap inside a 920-pixel panel and expand
upward above the quick menu. The previous line remains readable while choosing.
Hint popups leave the choice pending.
Hints are available only at first contact, the library, the infirmary, and the
final confession. Each choice can use one hint; total budget is three across
the chapter. Zero hides the button. Consumption blocks rollback across that
hint, so normal rollback cannot refund it. Loading restores the exact saved
count. Only beginning a fresh chapter playthrough resets the budget.

The gallery contains the original two endings and all three new endings;
locked cards offer no preview. CG cards preserve the artwork behind a bottom
title strip. Chapter 2 endings offer Main Menu, Chapter Select, and Gallery.
Chapter 1 retains New Game+.

## Ending logic and balancing

- Nghi Good: `NghiAffinity >= 12`, `NghiComfort >= 8`, sincere confession.
- Nghi Bad: either relationship threshold fails, or the demanding confession
  is selected. Refusal remains gentle; Minh's pub dialogue follows.
- Ngân: `NganAffinity >= 10`, `NganSpecialFlags >= 3`, `NganHintsUsed <= 1`,
  then choose **Gọi Ngân lại.** before Nghi arrives. This marks the current
  save terminal: both route-complete and Chapter-3-lock flags become true.
  Chapter Select can still begin another playthrough.

Original scripted choice deltas are preserved. The brief's optional coding
event gets a choice worth +3 Nghi affinity/+1 comfort. An infirmary follow-up
offers +3/+2 for consideration or apology. Maximum affinity is 18; maximum
comfort is 14. The first-contact disaster remains recoverable (an actual test
route finishes at 16 affinity/8 comfort). Repeated intrusive choices fail.

The three specified Ngân events total only 8 affinity; an additional optional
infirmary check-in gives +2 affinity/+1 special flag, allowing 10 affinity and
4 flags. These small additions implement the brief's balancing target and
explicitly permitted supportive event. Stats stay hidden.

## Asset mappings

All supplied files are referenced directly; no generated replacement art.

| Meaning | Supplied files |
| --- | --- |
| Main embarrassment, empathy, sadness, surprise, delight | `MainEmbarrassed.png`, `MainEmpathy.png`, `MainSad.png`, **`MainSurpised.png`**, `MainVeryHappy.png` |
| Ngân normal/happy/excited/sad/angry/laugh/confused/thinking/embarrassed | `NganNormal.png`, `NganHappy.png`, `NganWelcome.png`, `NganSad.png`, `NganAngry.png`, `NganVeryHappyAndBigLaugh.png`, `NganAwkward.png`, `NganThinking.png`, `NganEmbarrassed.png` |
| Nghi normal/soft smile/happy/confused/annoyed/sad/embarrassed/relaxed | `NghiNormal.png`, `NghiSmile.png`, `NghiHappy.png`, `NghiThinking.png`, `NghiAngry.png`, `NghiSad.png`, `NghiEmbarrassed.png`, `NghiNormal2.png` |
| Philosophy teacher, nurse, PE teacher | `MissPhilosophy.png`, `Nurse.png`, `PhysicalTeacher.png` |
| Philosophy, sports, infirmary, library, rooftop | Corresponding `PhilosophyClassroom`, `SportsGround`, `MedicalRoom`, `Library`, `Rooftop` + `Day`, `Afternoon`, `Night` files |
| Pub, Nghi CG, Ngân CG | `DrinkingSpot.png`, `GoodEndingChapter2.png`, `EasterEggEndingChapter2.png` |

All fifteen time variants are declared; unused night/morning variants are ready
for later scenes. Existing hallway, canteen, campus, gate, Main and Minh art is
reused. `NghiSmile.png` supplies the restrained closed-mouth acceptance smile.
Expressions of different source dimensions use proportional containment.
The teacher's supplied opaque image is retained as a smaller portrait rather
than attempting a destructive color key. A transparent teacher export can
replace it later through the same image declaration.

## Tests and release

Run Ren'Py 8.5.3 lint and engine tests with a separate savedir:

```text
renpy.py <project> lint --error-code
renpy.py --savedir <test-saves> <project> test --overwrite-screenshots
```

Tests cover Chapter 1 good/stay/failed escape, locked Chapter 2, Chapter Select,
continuation, all three Chapter 2 routes, recovery from the first-contact
disaster, resolver boundaries, shared hint exhaustion, real save/load, focus,
New Game+, persistent unlock written to disk, gallery and supporting menus.
Screenshots in `tests/screenshots` are reviewed visually after transitions.

Legacy compatibility is tested using a save generated by the unmodified v2.0
build at its first choice, loaded into v3.0 and continued to the next scene.
Place that fixture in the test savedir under Ren'Py's
`chapter1-v2-compatibility` slot. Without a fixture this optional test exits
early. With it, the test checks new defaults, schema migration and continued play.

Windows release: `dist/FPT2359EscapeProtocol-3.1-win.zip`. Extract everything
and run `FPT2359EscapeProtocol.exe`. Save directory stays unchanged so the real
player's gallery and compatible saves remain available. Test saves/unlocks
are isolated and excluded from the package.

## Assumptions / limitations

No new music exists in the audio folder. Existing notification, boss, error,
success and bad-ending WAV cues are reused, with deliberate silence around
confessions/refusal. No fabricated audio paths are introduced. Chapter 3 is a
tease only because no playable Chapter 3 script was supplied. The scheduled
thumbs-up message is described in narration to avoid a missing emoji glyph.
No missing asset paths or known critical gameplay issues remain after checks.
