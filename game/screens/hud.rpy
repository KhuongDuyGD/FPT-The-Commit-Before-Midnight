transform energy_delta_fade:
    alpha 1.0
    pause 1.0
    linear 0.4 alpha 0.0

screen energy_hud():
    zorder 80
    if energy_visible and not main_menu and not renpy.get_screen("chapter1_end"):
        frame:
            xalign 0.98
            yalign 0.025
            xsize 292
            padding (22, 17)
            background Solid("#101c2bea")
            vbox:
                spacing 10
                hbox:
                    xfill True
                    text "ENERGY" size 21 color "#a5b6cb"
                    text "[energy] / 100" size 23 xalign 1.0 color "#ffffff"
                bar value StaticValue(energy, 100) xsize 248 ysize 8 left_bar Solid("#ed987f" if energy <= 30 else "#9dd6bb")
        if energy_feedback:
            text ("%+d" % energy_feedback):
                id ("energy_delta_%d" % energy_feedback_serial)
                at energy_delta_fade
                xalign 0.97
                ypos 112
                size 25
                color ("#a8e7c7" if energy_feedback > 0 else "#efa58e")

screen device_panel():
    frame:
        xalign 0.5
        yalign 0.31
        xsize 860
        padding (38, 30)
        background Solid("#101626f5")
        vbox:
            spacing 20
            text "DISCORD   /   1:58 AM" size 26 color "#98afd5"
            text "GAME SESSION" size 44 color "#ffffff"
            text "Find Match" size 28 color "#c4b1f5"

