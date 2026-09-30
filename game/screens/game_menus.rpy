screen menu_shell(title):
    add Solid("#0f1b2b")
    text title xpos 110 ypos 60 size 46 bold True
    use menu_navigation

screen menu_navigation():
    hbox:
        xalign 0.5
        yalign 0.935
        spacing 14
        textbutton "Return" action Return() text_size 24
        if not main_menu:
            textbutton "Save" action ShowMenu("save") text_size 24
        textbutton "Load" action ShowMenu("load") text_size 24
        textbutton "History" action ShowMenu("history") text_size 24
        textbutton "Preferences" action ShowMenu("preferences") text_size 24
        textbutton "About" action ShowMenu("about") text_size 24
        if not main_menu:
            textbutton "Main Menu" action MainMenu(confirm=True) text_size 24

screen save():
    tag menu
    use menu_shell("SAVE GAME")
    use file_slot_grid("save")

screen load():
    tag menu
    use menu_shell("LOAD GAME")
    use file_slot_grid("load")

screen file_slot_grid(mode):
    grid 3 2:
        xalign 0.5
        ypos 168
        spacing 24
        for slot in range(1, 7):
            $ is_compatible = FileJson(slot, "rebuild_schema") == 1 and FileJson(slot, "chapter") == 1
            button:
                xsize 510
                ysize 300
                padding (20, 18)
                action (FileSave(slot) if mode == "save" else FileLoad(slot))
                sensitive (mode == "save" or is_compatible)
                alternate FileDelete(slot)
                vbox:
                    spacing 10
                    text "SLOT [slot]" size 25
                    add FileScreenshot(slot) xysize (470, 206)
                    text ("Previous version save" if FileLoadable(slot) and not is_compatible else FileTime(slot, format="%d/%m/%Y %H:%M", empty="Empty")) size 20 color "#a8bbd2"
    hbox:
        xalign 0.5
        ypos 830
        spacing 12
        textbutton "<" action FilePagePrevious()
        textbutton "Auto" action FilePage("auto")
        textbutton "Quick" action FilePage("quick")
        for page in range(1, 6):
            textbutton str(page) action FilePage(page)
        textbutton ">" action FilePageNext()

screen preferences():
    tag menu
    use menu_shell("PREFERENCES")
    frame:
        id "preferences_panel"
        xalign 0.5
        ypos 175
        xsize 1120
        padding (44, 34)
        background Solid("#19283d")
        vbox:
            spacing 22
            hbox:
                spacing 25
                text "Display" size 28 yalign 0.5
                textbutton "Window" action Preference("display", "window")
                textbutton "Fullscreen" action Preference("display", "fullscreen")
            text "Text Speed" size 26
            bar id "text_speed_slider" value Preference("text speed") xsize 1032
            text "Auto Speed" size 26
            bar value Preference("auto-forward time") xsize 1032
            text "Music Volume" size 26
            bar value Preference("music volume") xsize 1032
            text "Sound Volume" size 26
            bar value Preference("sound volume") xsize 1032
            hbox:
                spacing 24
                text "Skip" size 26 yalign 0.5
                textbutton "Unseen Text" action Preference("skip", "toggle") text_size 24
                textbutton "After Choices" action Preference("after choices", "toggle") text_size 24
                textbutton "Mute All" action Preference("all mute", "toggle") text_size 24

screen history():
    tag menu
    use menu_shell("DIALOGUE HISTORY")
    frame:
        xpos 110
        ypos 155
        xsize 1700
        ysize 745
        padding (30, 25)
        background Solid("#19283d")
        viewport:
            scrollbars "vertical"
            mousewheel True
            draggable True
            pagekeys True
            vbox:
                spacing 18
                if not _history_list:
                    text "Chưa có hội thoại trong lượt chơi này." size 28 color "#a8bbd2"
                for entry in _history_list:
                    if entry.who:
                        text entry.who size 25 color "#f3be85" substitute False
                    text entry.what size 29 substitute False xmaximum 1600

screen about():
    tag menu
    use menu_shell("ABOUT")
    vbox:
        xpos 160
        ypos 240
        spacing 30
        text "FPT: The Commit Before Midnight" size 46 bold True
        text "Chapter 1 — Một ngày rất bình thường của sinh viên IT" size 30
        text "Đời sinh viên, deadline, Energy và những lựa chọn nhỏ." size 28 color "#a8bbd2"
        text "Version [config.version]\nRen'Py [renpy.version_only]" size 26 color "#a8bbd2"
        textbutton "Ren'Py credits & licenses" action OpenURL("https://www.renpy.org/doc/html/license.html") text_size 25

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    add Solid("#080e19d9")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1020
        padding (50, 38)
        background Solid("#19283d")
        vbox:
            spacing 32
            text message size 30 xmaximum 920
            hbox:
                xalign 0.5
                spacing 30
                textbutton "Yes" action yes_action
                textbutton "No" action no_action

screen notify(message):
    zorder 210
    frame:
        xalign 0.98
        yalign 0.12
        padding (22, 16)
        background Solid("#263b54ed")
        text message size 25
    timer 2.5 action Hide("notify")
