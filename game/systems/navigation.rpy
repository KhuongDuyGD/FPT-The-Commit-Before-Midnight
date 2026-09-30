label before_main_menu:
    $ scene_ambience()
    hide screen energy_hud
    hide screen device_panel
    return

label main_menu:
    while True:
        call screen main_menu

label after_load:
    $ migrate_stage()
    $ enter_chapter(current_chapter)
    return
