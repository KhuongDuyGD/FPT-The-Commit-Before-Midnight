# Chapter navigation uses Ren'Py Start so direct selection gets a fresh save
# context. Continuing after Chapter 1 uses Jump within the current playthrough.
screen chapter_select():
    tag menu
    add "game_main_menu_background"
    add Solid("#0b1327e8")
    text "CHAPTER SELECT" xalign 0.5 ypos 64 size 46 bold True
    vbox:
        xalign 0.5
        yalign 0.48
        spacing 24
        textbutton "Chương 1 — ESCAPE PROTOCOL":
            action Start("start")
            xsize 860
            padding (30, 22)
            text_size 29
            background Solid("#253659")
            hover_background Solid("#426195")
        textbutton ("Chương 2 — LOVE PROTOCOL" if chapter2_is_unlocked() else "Chương 2 — LOCKED"):
            action Start("chapter2_start")
            sensitive chapter2_is_unlocked()
            xsize 860
            padding (30, 22)
            text_size 29
            text_insensitive_color "#929aaa"
            background Solid("#253659")
            hover_background Solid("#426195")
        if not chapter2_is_unlocked():
            text "Hoàn thành Good Ending Chương 1 để mở Chương 2." size 23 color "#bac7dc" xalign 0.5
    textbutton "Return" action Return() xalign 0.5 yalign 0.90 text_size 25

screen chapter1_good_actions():
    modal True
    add Solid("#080d18ed")
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 24
        text "CHƯƠNG 2 ĐÃ MỞ" size 44 bold True xalign 0.5 color "#a7f0be"
        textbutton "Tiếp tục Chương 2" action Jump("chapter2_start") xalign 0.5 text_size 30
        textbutton "Trở về Menu Chính" action MainMenu(confirm=False) xalign 0.5 text_size 27
        textbutton "Start New Game+" action Jump("new_game_plus") xalign 0.5 text_size 24

screen ngan_hint_message(message):
    modal True
    zorder 130
    add Solid("#0509159c")
    frame:
        xalign 0.5
        ypos CHOICE_BOTTOM
        yanchor 1.0
        xsize 680
        padding (32, 28)
        background Solid("#162944")
        vbox:
            spacing 22
            text "NGÂN · TIN NHẮN" size 25 color "#94dcff"
            text message size 28 xmaximum 616
            text "[NganHintsRemaining]/3 lượt còn lại" size 20 color "#a0b1ca"
            textbutton "Đã hiểu" action Hide("ngan_hint_message") text_size 25 xalign 1.0

screen chapter2_cg(kind, title, subtitle=""):
    # Keep the supplied CG visible. Unlike Chapter 1's opaque card, this panel
    # leaves the characters and scene readable above its bottom strip.
    modal True
    frame:
        yalign 1.0
        xfill True
        padding (30, 18)
        background Solid("#081020ed")
        vbox:
            xalign 0.5
            spacing 7
            text kind size 26 bold True xalign 0.5 color "#ffce83"
            text title size 37 xalign 0.5
            if subtitle:
                text subtitle size 20 text_align 0.5 xalign 0.5
            textbutton "Continue" action Return() xalign 0.5 text_size 24

screen chapter2_end_menu():
    modal True
    add Solid("#080d18ec")
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 22
        text ("ROUTE COMPLETE" if game_route_complete else "CHƯƠNG 2 — THE END") xalign 0.5 size 42 bold True
        textbutton "Trở về Menu Chính" action MainMenu(confirm=False) xalign 0.5 text_size 28
        textbutton "Chapter Select" action ShowMenu("chapter_select") xalign 0.5 text_size 28
        textbutton "Ending Gallery" action ShowMenu("ending_gallery") xalign 0.5 text_size 25

screen chapter_gallery_contents():
    # All five rows fit at 720p; a fixed list avoids viewport style defaults
    # that depend on the GUI files in a template Ren'Py project.
    vbox:
        xpos 105
        ypos 125
        spacing 14
        for title, ending_id, unlocked in [
            ("GOOD ENDING — ESCAPE SUCCESSFUL", "good", persistent.good_ending_unlocked),
            ("BAD ENDING — FPT HAS CONSUMED YOU", "bad", persistent.bad_ending_unlocked),
            ("GOOD ENDING — LOVE PROTOCOL ESTABLISHED", "nghi_good", persistent.ending_nghi_good_unlocked),
            ("BAD ENDING — 404 — LOVE NOT FOUND", "nghi_bad", persistent.ending_nghi_bad_unlocked),
            ("SECRET ENDING — YOU WERE NEVER LOST", "ngan", persistent.ending_ngan_unlocked)]:
            frame:
                xsize 1070
                ysize 78
                padding (24, 14)
                background Solid("#253a50" if unlocked else "#29303c")
                hbox:
                    yalign 0.5
                    spacing 22
                    fixed:
                        xsize 780
                        ysize 50
                        text title size 25 xmaximum 780 yalign 0.5
                    if unlocked:
                        textbutton "View ending" action Show("gallery_detail", ending=ending_id) yalign 0.5 text_size 22
                    else:
                        text "LOCKED" color "#9ba6b7" size 22 yalign 0.5
