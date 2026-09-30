transform menu_reveal:
    alpha 0.0
    ease 0.45 alpha 1.0

screen main_menu():
    tag menu
    $ chapter = menu_chapter_index(persistent.last_played_chapter)
    $ menu_background = "menu_chapter_%d" % chapter
    add menu_background
    add "game_logo" xpos 1230 ypos 22
    frame at menu_reveal:
        xfill True
        yalign 1.0
        ysize 254
        padding (42, 20)
        background Solid("#0c1726e8")
        vbox:
            xalign 0.5
            spacing 13
            text ("CHAPTER %02d  ·  FPT: The Commit Before Midnight" % chapter) size 22 color "#b9cbe0" xalign 0.5
            $ recent_save = latest_compatible_save()
            hbox:
                spacing 14
                textbutton "New Game" style "menu_button" xsize 420 action Start()
                textbutton "Continue" style "menu_button" xsize 420 action (FileLoad(recent_save, slot=True, confirm=False) if recent_save else None)
                textbutton "Load" style "menu_button" xsize 420 action ShowMenu("load")
                textbutton "Gallery" style "menu_button" xsize 420 action ShowMenu("gallery")
            hbox:
                spacing 14
                textbutton "Preferences" style "menu_button" xsize 420 action ShowMenu("preferences")
                textbutton "History" style "menu_button" xsize 420 action ShowMenu("history")
                textbutton "About" style "menu_button" xsize 420 action ShowMenu("about")
                textbutton "Quit" style "menu_button" xsize 420 action Quit(confirm=True)
