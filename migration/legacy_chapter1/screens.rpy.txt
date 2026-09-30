# Self-contained 1280x720 UI. The default Ren'Py keyboard and mouse bindings
# still supply normal advance, rollback, skip, and auto-forward behavior.

define DIALOGUE_HEIGHT = 204
define DIALOGUE_TOP = config.screen_height - DIALOGUE_HEIGHT
define CHOICE_BOTTOM = DIALOGUE_TOP - 52

init python:
    def choice_dialogue():
        if _history_list:
            return _history_list[-1].who, _history_list[-1].what
        # Older saves were made with history disabled.
        speaker = getattr(renpy.store, _last_say_who, None) if isinstance(_last_say_who, str) else _last_say_who
        return getattr(speaker, "name", None), _last_say_what or ""

screen dialogue_panel(who, what, instant=False):
    # The master layer owns the directed shot; stage.rpy only changes focus.
    # Keep the speaker and every wrapped line inside one fixed dialogue panel.
    # Reserving the name row also keeps narrator text aligned with dialogue.
    window:
        id "window"
        xalign 0.5
        yalign 1.0
        xsize config.screen_width - 40
        ysize DIALOGUE_HEIGHT
        xpadding 30
        ypadding 20
        background Solid("#101827f2")
        vbox:
            xfill True
            spacing 8
            if who is not None:
                text who id "who" size 26 color "#ffd37b"
            else:
                null height 31
            text what id "what" xsize config.screen_width - 100 size 27 color "#f4f6fb" text_align 0.0 slow_cps (0 if instant else True) substitute (not instant)

screen say(who, what):
    use dialogue_panel(who, what)
    use quick_menu


screen choice(items):
    modal True
    # Menus without a spoken prompt normally clear Ren'Py's say screen.
    # Render the last line in the same panel, without replaying its callback.
    if not renpy.get_screen("say"):
        $ choice_who, choice_what = choice_dialogue()
        use dialogue_panel(choice_who, choice_what, instant=True)
    vbox:
        id "choice_list"
        xalign 0.5
        ypos CHOICE_BOTTOM
        yanchor 1.0
        spacing 12
        for item in items:
            textbutton item.caption:
                action item.action
                xsize 920
                text_size 25
                text_xmaximum 872
                text_color ("#ffe1a5" if item.caption == "Gọi Ngân lại." else "#ffffff")
                padding (24, 14)
                background Solid("#594439ef" if item.caption == "Gọi Ngân lại." else "#253659ef")
                hover_background Solid("#426195")
        if hint_available():
            textbutton "Hỏi Ngân ([NganHintsRemaining]/3)":
                action Function(use_ngan_hint)
                xalign 1.0
                text_size 23
                text_color "#a9dfff"
                padding (20, 12)
                background Solid("#172844f5")
                hover_background Solid("#335479")
    use quick_menu


screen quick_menu():
    zorder 90
    frame:
        xalign 0.5
        ypos DIALOGUE_TOP
        yanchor 1.0
        yoffset -8
        xpadding 16
        ypadding 5
        background Solid("#101827e8")
        hbox:
            spacing 14
            textbutton "Back" action Rollback() text_size 16
            textbutton "History" action ShowMenu("history") text_size 16
            textbutton "Skip" action Skip() text_size 16
            textbutton "Auto" action Preference("auto-forward", "toggle") text_size 16
            textbutton "Save" action ShowMenu("save") text_size 16
            textbutton "Load" action ShowMenu("load") text_size 16
            textbutton "Prefs" action ShowMenu("preferences") text_size 16


screen stats_hud():
    zorder 80
    frame:
        xalign 0.99
        yalign 0.02
        xpadding 16
        ypadding 10
        background Solid("#0c1421dc")
        vbox:
            spacing 2
            text "ENERGY  [energy]" size 20 color "#b2f5cb"
            text "SANITY  [sanity]" size 20 color "#d2c5ff"
            text "PENDING TASKS  [pending_tasks]" size 20 color "#ffcf9c"
            text "ESCAPE POINTS  [escape_point]" size 20 color "#91ddff"


screen boss_title(title, subtitle):
    modal True
    zorder 100
    add Solid("#090e1bf4")
    vbox:
        xalign 0.5
        yalign 0.48
        spacing 24
        text "BOSS ENCOUNTER" xalign 0.5 size 26 color "#ff6577"
        text title xalign 0.5 size 66 bold True color "#ffffff"
        text subtitle xalign 0.5 size 23 color "#ffcf86"
    text "Click to continue" xalign 0.5 yalign 0.91 size 18 color "#9faec3"
    key "dismiss" action Return()
    button:
        xfill True
        yfill True
        background None
        action Return()


screen main_menu():
    tag menu
    add "game_main_menu_background"
    # This opaque panel masks the buttons/logo already printed on the image.
    # The actual logo and controls remain crisp, interactive Ren'Py UI.
    frame:
        xpos 724
        ypos 42
        xsize 496
        ysize 636
        xpadding 34
        ypadding 22
        background Solid("#10121dfc")
        vbox:
            xfill True
            spacing 7
            add "game_logo" xalign 0.5
            null height 3
            textbutton "Continue" action Continue() xfill True ysize 43 text_size 25 text_color "#ffffff" text_insensitive_color "#858998" text_hover_color "#13151d" background Solid("#242331") hover_background Solid("#f89b3c") xpadding 17
            textbutton "New Game" action Start() xfill True ysize 43 text_size 25 text_color "#ffffff" text_hover_color "#13151d" background Solid("#242331") hover_background Solid("#f89b3c") xpadding 17
            textbutton "Chapter Select" action ShowMenu("chapter_select") xfill True ysize 43 text_size 25 text_color "#ffffff" text_hover_color "#13151d" background Solid("#242331") hover_background Solid("#f89b3c") xpadding 17
            textbutton "Load" action ShowMenu("load") xfill True ysize 43 text_size 25 text_color "#ffffff" text_hover_color "#13151d" background Solid("#242331") hover_background Solid("#f89b3c") xpadding 17
            textbutton "Ending Gallery" action ShowMenu("ending_gallery") xfill True ysize 43 text_size 25 text_color "#ffffff" text_hover_color "#13151d" background Solid("#242331") hover_background Solid("#f89b3c") xpadding 17
            textbutton "Settings" action ShowMenu("preferences") xfill True ysize 43 text_size 25 text_color "#ffffff" text_hover_color "#13151d" background Solid("#242331") hover_background Solid("#f89b3c") xpadding 17
            textbutton "Quit" action Quit(confirm=True) xfill True ysize 43 text_size 25 text_color "#ffffff" text_hover_color "#13151d" background Solid("#242331") hover_background Solid("#f89b3c") xpadding 17


screen menu_navigation():
    hbox:
        xalign 0.5
        yalign 0.91
        spacing 26
        textbutton "Return" action Return() text_size 21
        textbutton "Save" action ShowMenu("save") text_size 21
        textbutton "Load" action ShowMenu("load") text_size 21
        textbutton "History" action ShowMenu("history") text_size 21
        textbutton "Preferences" action ShowMenu("preferences") text_size 21
        textbutton "Gallery" action ShowMenu("ending_gallery") text_size 21
        textbutton "Main Menu" action MainMenu(confirm=True) text_size 21


screen save():
    tag menu
    add Solid("#11192b")
    text "SAVE GAME" xalign 0.5 ypos 40 size 42 bold True
    use file_slot_grid("save")
    use menu_navigation


screen load():
    tag menu
    add Solid("#11192b")
    text "LOAD GAME" xalign 0.5 ypos 40 size 42 bold True
    use file_slot_grid("load")
    use menu_navigation


screen file_slot_grid(mode):
    grid 3 2:
        xalign 0.5
        yalign 0.47
        spacing 22
        for slot in range(1, 7):
            frame:
                xsize 355
                ysize 230
                background Solid("#263651")
                if mode == "save":
                    button:
                        xfill True
                        yfill True
                        action FileSave(slot)
                        vbox:
                            spacing 8
                            text "SLOT [slot]" size 23
                            add FileScreenshot(slot) xsize 310 ysize 145
                            text FileTime(slot, format="%d/%m/%Y %H:%M", empty="Empty") size 17
                else:
                    button:
                        xfill True
                        yfill True
                        action FileLoad(slot)
                        sensitive FileLoadable(slot)
                        vbox:
                            spacing 8
                            text "SLOT [slot]" size 23
                            add FileScreenshot(slot) xsize 310 ysize 145
                            text FileTime(slot, format="%d/%m/%Y %H:%M", empty="Empty") size 17


screen preferences():
    tag menu
    add Solid("#11192b")
    text "PREFERENCES" xalign 0.5 ypos 40 size 42 bold True
    frame:
        xalign 0.5
        yalign 0.43
        xsize 820
        xpadding 40
        ypadding 30
        background Solid("#263651")
        vbox:
            spacing 20
            hbox:
                spacing 25
                text "Display" size 24
                textbutton "Window" action Preference("display", "window")
                textbutton "Fullscreen" action Preference("display", "fullscreen")
            text "Text Speed" size 24
            bar value Preference("text speed") xsize 720
            text "Auto Speed" size 24
            bar value Preference("auto-forward time") xsize 720
            text "Music Volume" size 24
            bar value Preference("music volume") xsize 720
            text "Sound Volume" size 24
            bar value Preference("sound volume") xsize 720
    use menu_navigation


screen history():
    tag menu
    add Solid("#11192b")
    text "DIALOGUE HISTORY" xalign 0.5 ypos 35 size 42 bold True
    frame:
        xpos 110
        ypos 105
        xsize 1060
        ysize 520
        background Solid("#263651")
        viewport:
            scrollbars "vertical"
            mousewheel True
            draggable True
            vbox:
                spacing 18
                for entry in _history_list:
                    if entry.who:
                        text entry.who size 21 color "#ffcf83"
                    text entry.what size 23 substitute False xmaximum 965
    use menu_navigation


screen ending_gallery():
    tag menu
    add Solid("#11192b")
    text "ENDING GALLERY" xalign 0.5 ypos 52 size 46 bold True
    use chapter_gallery_contents
    use menu_navigation


screen gallery_detail(ending):
    modal True
    zorder 120
    add Solid("#080d18ed")
    vbox:
        xalign 0.5
        yalign 0.47
        spacing 25
        if ending == "good":
            text "GOOD ENDING — ESCAPE SUCCESSFUL" xalign 0.5 size 45 color "#a7f0be"
            text "Student Status: ALIVE\nEnergy: Enough for one ranked match\nSanity: Functioning within acceptable parameters\nAssignments: Technically under control\nTomorrow: Future Me's problem\nAchievement: LOG OUT SUCCESSFULLY" xalign 0.5 text_align 0.5 size 23
        elif ending == "bad":
            text "BAD ENDING — FPT HAS CONSUMED YOU" xalign 0.5 size 45 color "#ff8190"
            text "Student Status: Technically Alive\nEnergy: 0%%\nSanity: SEGMENTATION FAULT\nPhysical Condition: Dried student\nAssignment: SUBMITTED\nPresentation: UPDATED\nGroup Project: Somehow still has one bug\nTomorrow's Meeting: 07:00\nAchievement: JUST ONE MORE TASK" xalign 0.5 text_align 0.5 size 22
        else:
            add ("cg_nghi_good" if ending == "nghi_good" else "cg_ngan" if ending == "ngan" else "nearby_pub_night") xysize (896, 504)
            text ({"nghi_good": "LOVE PROTOCOL ESTABLISHED", "nghi_bad": "404 — LOVE NOT FOUND", "ngan": "YOU WERE NEVER LOST"}[ending]) size 32 xalign 0.5
        textbutton "Close" action Hide("gallery_detail") xalign 0.5


screen ending_card(kind, subtitle, details):
    modal True
    add Solid("#080d18")
    vbox:
        xalign 0.5
        yalign 0.45
        spacing 26
        text kind xalign 0.5 size 54 bold True color ("#a7f0be" if kind == "GOOD ENDING" else "#ff8190")
        text subtitle xalign 0.5 size 37 color "#ffffff"
        text details xalign 0.5 text_align 0.5 size 24 color "#dce4ef"
        textbutton "Continue" action Return() xalign 0.5 text_size 23


screen post_ending_actions():
    modal True
    add Solid("#080d18df")
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 22
        text "THE END" xalign 0.5 size 52 bold True
        textbutton "Start New Game+" action Jump("new_game_plus") xalign 0.5 text_size 28
        textbutton "Return to Main Menu" action MainMenu(confirm=False) xalign 0.5 text_size 28


screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    add Solid("#080d18df")
    frame:
        xalign 0.5
        yalign 0.5
        xpadding 45
        ypadding 35
        background Solid("#263651")
        vbox:
            spacing 25
            text message size 26
            hbox:
                xalign 0.5
                spacing 30
                textbutton "Yes" action yes_action
                textbutton "No" action no_action


screen notify(message):
    zorder 210
    frame:
        xalign 0.99
        yalign 0.07
        background Solid("#314460ed")
        text message size 20
    timer 2.5 action Hide("notify")
