> Status 2026-09-29: Chapter 2 is temporarily removed from the game at the user’s request. Archived source is in `migration/chapter2_paused/`; the historical handoff below does not describe the active Chapter 1 rebuild.

# Resume Chapter 2 — saved before lunch, 2026-09-29

## Current status

Chapter 2 source implementation is finished. The Windows v3.0 ZIP was built
successfully and saved at:

`D:/Duy/VisualCoding/fpt-2359-escape-protocol/dist/FPT2359EscapeProtocol-3.0-win.zip`

Size: 169,968,796 bytes (about 162 MiB). It has **not yet been extracted or
launched**. The existing extracted `2.0-win` folder is the older release.

Do not confuse that older executable with the new Chapter 2 build.

## Remaining work when the user returns

1. Inspect the v3.0 ZIP contents to confirm all Chapter 2 source/art is included
   and testcases, test screenshots, player saves and the implementation brief
   are excluded. Build exclusion rules are implemented, but the resulting ZIP
   has not yet been inspected.
2. Extract the entire ZIP into `dist`, preserving the older v2.0 build.
3. Launch the extracted **v3.0** `FPT2359EscapeProtocol.exe` and confirm startup
   without an exception. This packaged-executable smoke check is pending.
4. Check the packaged main menu, Chapter Select and Ending Gallery. Source
   engine tests already cover these, but the packaged build has not been
   played yet. If an issue appears, fix it and rebuild the ZIP.
5. Append the package verification results to `tests/CHAPTER2_RESULTS.md` and
   provide the user with the final executable/ZIP links and short play steps.

The last README edit clarified that the source project needs Ren'Py 8.5 or
newer. It occurred just after packaging, so the ZIP may contain the preceding
README wording. Sync that documentation if rebuilding/repacking the release.

## Completed and verified

- Thirteen main Chapter 2 scene labels and all supplied Vietnamese dialogue.
- Nghi Good/Bad and Ngân secret endings, with provided CGs and pub scene.
- Persistent chapter unlock and canonical Good continuation from Chapter 1.
- Chapter Select and direct Chapter 2 initialization.
- Three shared Ngân hints, marked choice eligibility, exhaustion, no automatic
  answer selection, save/load count restoration and rollback protection.
- Hidden relationship state and reachable secret branch.
- Recoverable first-contact disaster and balanced thresholds.
- Physical cast stays visible; inactive actors dim/scale back smoothly in
  both chapters, with explicit entrances/exits and remote messages.
- Five gallery cards and main menu with LogoGame.png.
- Ren'Py lint passed. Every referenced image and audio path exists.
- Main engine regression: **14/14 tests, 74/74 assertions passed**.
- Additional hint rollback test: **1/1 test, 2/2 assertions passed**.
- Combined: **15 tests, 76 assertions passed**.
- A real save produced by the unmodified v2.0 build was loaded and continued
  in v3.0. This checks the original first-choice checkpoint; it is not an
  exhaustive test of every possible older save position.
- All 712 original Chapter 1 dialogue/title lines are unchanged.
- Visual screenshots reviewed for menu, gallery, hints, choices, focus and
  all three endings. They are saved under `tests/screenshots`.

## Future content/art work, separate from remaining release checks

- Chapter 3 is only teased; no Chapter 3 screenplay was supplied or implemented.
- Audio currently reuses existing placeholder WAV cues. No new music tracks
  were supplied; final audio/music can be added later.
- MissPhilosophy.png is an opaque supplied portrait. A transparent standee
  export would allow later art polish; the current game retains the original.
- Unused morning/night map variants are declared for future scenes.

These are content/asset limitations, not missing Chapter 2 branches.

## Developer handoff

Project: `D:/Duy/VisualCoding/fpt-2359-escape-protocol`.
Do not work in the older sibling `VisualNovelGame` folder by mistake.
Implementation audit: `CHAPTER2.md`. Verification notes:
`tests/CHAPTER2_RESULTS.md`. No commit or push was requested or performed.
User-supplied new art and the brief remain in the working tree.

Ren'Py SDK:
`%TEMP%/renpy-sdk-8.5.3-check/renpy-8.5.3-sdk`.
Engine tests use isolated `%TEMP%/fpt2359-ch2-test-saves` so their unlocks do
not affect the player's actual persistent data. The legacy fixture remains in
that test savedir under `chapter1-v2-compatibility`.

For runtime tests, use `test --overwrite-screenshots` so captured transition
frames are not compared against a previous parameterized route. Tests and
fixtures are excluded by the release build rules.

No game test or build process was left running at the pause. The pre-existing
user change to root `log.txt` was preserved; temporary test changes to root
`traceback.txt` were restored. Source and the new ZIP are saved on disk.
