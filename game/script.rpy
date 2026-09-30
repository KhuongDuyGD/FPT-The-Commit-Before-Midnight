# The only New Game entry. No legacy Chapter 1 labels remain in game/.
label start:
    $ reset_chapter1_state()
    $ scene_ambience()
    hide screen energy_hud
    hide screen device_panel
    jump chapter_01
