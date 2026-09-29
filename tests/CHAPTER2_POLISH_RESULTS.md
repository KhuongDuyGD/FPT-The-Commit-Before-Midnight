# Chapter 2 polish — version 3.1

Implemented September 29, 2026; verified with Ren'Py 8.5.3 on Windows 11.

1. **Files changed:** game/stage.rpy, game/screens.rpy,
   game/chapter_screens.rpy, game/chapter2_state.rpy, game/chapter2.rpy,
   game/characters.rpy, game/chapter2_assets.rpy, game/options.rpy,
   game/chapter2_testcases.rpy, game/polish_testcases.rpy,
   tools/build_chapter2.py, README.md and CHAPTER2.md.
   The generated ending script retains its narrative and route logic.
2. **Composition:** stage_cast records story presence; stage_visual records the
   active shot. set_shot changes presentation without a physical exit. Normal
   compositions are capped at three; most authored shots show two. Offscreen
   story-present speakers can receive a brief cutaway. Active participants
   retain their sprites when focus changes; the speaker gets foreground order,
   full brightness and a small scale emphasis.
3. **Transitions:** 0.25-second fade entrances/exits; a 3% scale fade for Nghi's
   introduction; a 20-pixel soft rise for her infirmary arrival; 0.15-second
   expression crossfades; 0.2-second focus adjustments. New actors start at their
   assigned horizontal position. Expression transitions do not retain stale
   child timing across focus updates.
4. **Dialogue UI:** dialogue and choices share a 204-pixel bottom-anchored panel.
   Choices expand upward above the quick menu. The preceding line stays visible
   while selecting. Hint messages overlay the choices without moving the panel
   or adding an actor. History is enabled, with a fallback for older saves.
5. **Startup:** an explicit main_menu label keeps the custom main-menu screen
   open instead of letting Ren'Py's missing template-layout fallback enter
   gameplay. Auto-load/menu-skip environment overrides are cleared. Continue
   loads the latest save only after selection. Existing chapter continuation,
   New Game, New Game+ and Chapter Select behavior are preserved.
6. **Cleaned scenes:** hallway banter/choices; philosophy lecture, introduction,
   group discussion and afternoon lecture; PE instructions, running and branch
   reactions; infirmary arrival, Nghi conversation, Ngân conversation and nurse
   closing. Quiet library, courtyard, canteen, rooftop and ending shots remain
   focused on their conversation partners.
7. **Slides:** no current shot uses a slide entrance. The optional short
   35-pixel slide remains available for a future motivated entrance.
8. **Regression:** the full engine run passed **23/23 cases and 133/133
   assertions**. It covers both Chapter 1 endings, failed escape, all Chapter 2
   endings, relationship thresholds/recovery, hints/exhaustion/rollback,
   real save/load, Chapter Select/unlock, Continue, gallery, New Game+, and
   genuine v2.0 and v3.0 saves. Presentation checks cover 960×540, 1280×720 and
   1024×768 windows, matching dialogue/choice/hint panel geometry, story-present
   offscreen actors, focus without entrance resets, expression changes and
   migration from a crowded v3.0 stage. Source launch was independently checked
   in a normal process with menu-skip/auto-load flags: main menu visible,
   gameplay absent. Logs: polish-verified-regression.txt and
   polish-startup-report.json. Screenshots were inspected.
9. **Teacher/nurse height fix:** every actor and expression uses proportional
   scaling to the same 620-pixel base height. The philosophy teacher's smaller
   portrait box and the PE teacher's width constraint are removed. At equal
   focus, rendered player/teacher/nurse heights differ by less than one pixel.
   Horizontal spacing accommodates the PE teacher's wider artwork.

Final height/spacing recheck: 1/1 testcase, 3/3 assertions passed
(polish-height-final.txt). The compact seven-button menu was checked in a
normal process after its final spacing adjustment. Final lint exited 0.
Windows ZIP validation passed: CRC integrity, byte-for-byte equality with the
updated game sources, and exclusion of project tests, saves and prompt files.
The extracted version 3.1 executable exited 0 after the startup probe recorded
main_menu=true and gameplay=false. The temporary probe was removed from the
extracted game; it was never included in the ZIP. Package verification:
polish-package-startup-report.json and its PNG.

No known gameplay or layout failures remain after these checks. Original
artwork is preserved, including backgrounds baked into portrait assets.
Audio remains the existing placeholder cues, and Chapter 3 remains a teaser.
Older-save checks cover the supplied v2.0 first-choice and v3.0 library
checkpoints; they do not establish compatibility at every historical position.

Release: dist/FPT2359EscapeProtocol-3.1-win.zip. Extract the whole package and
launch FPT2359EscapeProtocol.exe. Old packages are retained.
