init python:
    def choice_dialogue():
        # The last say also includes system messages omitted from History.
        speaker = getattr(renpy.store, _last_say_who, None) if isinstance(_last_say_who, str) else _last_say_who
        return getattr(speaker, "name", None), _last_say_what or ""

screen dialogue_panel(who, what, instant=False):
    window:
        id "window"
        xalign 0.5
        yalign 1.0
        xsize config.screen_width - 80
        ysize DIALOGUE_HEIGHT
        padding (40, 25)
        background Solid("#101a29f2")
        vbox:
            xfill True
            spacing 10
            if who is not None:
                text who id "who" size 29 color "#f3be85"
            else:
                null height 34
            text what:
                id "what"
                xsize config.screen_width - 160
                size 34
                line_spacing 5
                color "#edf1f7"
                slow_cps (0 if instant else True)
                substitute (not instant)

screen say(who, what):
    use dialogue_panel(who, what)
    use quick_menu

screen choice(items):
    modal True
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
                style "choice_button"
                action item.action
    use quick_menu

screen quick_menu():
    zorder 90
    frame:
        xalign 0.5
        ypos DIALOGUE_TOP
        yanchor 1.0
        yoffset -8
        padding (15, 4)
        background Solid("#101a29e8")
        hbox:
            spacing 8
            textbutton "Back" style "quick_button" action Rollback()
            textbutton "History" style "quick_button" action ShowMenu("history")
            textbutton "Skip" style "quick_button" action Skip()
            textbutton "Auto" style "quick_button" action Preference("auto-forward", "toggle")
            textbutton "Save" style "quick_button" action ShowMenu("save")
            textbutton "Load" style "quick_button" action ShowMenu("load")
            textbutton "Prefs" style "quick_button" action ShowMenu("preferences")
