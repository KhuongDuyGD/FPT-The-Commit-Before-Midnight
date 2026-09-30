define DIALOGUE_HEIGHT = 330
define DIALOGUE_TOP = config.screen_height - DIALOGUE_HEIGHT
define CHOICE_BOTTOM = DIALOGUE_TOP - 66

init python:
    # Both fonts ship with Ren'Py under its bundled font licenses.
    vn_font = FontGroup().add("TwemojiCOLRv0.ttf", 0x1f000, 0x1ffff).add("DejaVuSans.ttf", 0, 0x10ffff)

style default:
    font vn_font
    size 30
    color "#edf1f7"

style button:
    padding (20, 12)
    background Solid("#182539")
    hover_background Solid("#2c405a")
    insensitive_background Solid("#131e2b")

style button_text:
    color "#dce5f1"
    hover_color "#ffffff"
    insensitive_color "#677486"

style menu_button is button:
    ysize 56
    padding (18, 10)
    background Solid("#1b2a3edb")
    hover_background Solid("#345275")

style menu_button_text is button_text:
    size 28

style choice_button is button:
    xsize 1340
    padding (28, 17)
    background Solid("#162439f5")
    hover_background Solid("#345275")

style choice_button_text is button_text:
    size 32
    xmaximum 1284

style quick_button is button:
    background None
    hover_background Solid("#2c405a")
    padding (12, 5)

style quick_button_text is button_text:
    size 22

style bar:
    ysize 16
    left_bar Solid("#f3b47b")
    right_bar Solid("#344357")
    thumb None

style scrollbar:
    xsize 12
    base_bar Solid("#1e2b3e")
    thumb Solid("#75869d")

style slider is bar:
    ysize 24
    left_bar Solid("#f3b47b")
    right_bar Solid("#344357")
    thumb Solid("#edf1f7", xsize=16, ysize=24)
    thumb_offset 0

style vscrollbar:
    xsize 12
    base_bar Solid("#1e2b3e")
    thumb Solid("#75869d")
