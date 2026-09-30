screen gallery():
    tag menu
    use menu_shell("CHAPTER 1 GALLERY")
    grid 2 2:
        xalign 0.5
        ypos 153
        spacing 22
        for cg_id in ("pe_intro", "good_sleep", "walking_corpse", "nurse_intro"):
            $ unlocked = chapter1_cg_seen(cg_id)
            button:
                xsize 820
                ysize 323
                padding (28, 20)
                action (Show("gallery_view", cg_id=cg_id) if unlocked else None)
                background Solid("#1b2a40")
                hover_background Solid("#304765")
                vbox:
                    spacing 12
                    if unlocked:
                        add chapter1_cg_thumb(cg_id)
                        text CHAPTER1_CG[cg_id][1] size 26
                    else:
                        add Solid("#101b2c", xsize=752, ysize=226)
                        text "???" size 26 color "#8fa1b8"

screen gallery_view(cg_id):
    modal True
    zorder 300
    add Solid("#0a1221")
    add chapter1_cg_full(cg_id) xalign 0.5 yalign 0.5
    frame:
        xpos 25
        ypos 25
        padding (16, 9)
        background Solid("#0d1827e8")
        textbutton "Back to Gallery" action Hide("gallery_view") text_size 24
