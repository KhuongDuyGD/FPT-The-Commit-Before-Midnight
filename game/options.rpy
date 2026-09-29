# Project settings. Copy the whole `game` folder into a Ren'Py 8.x project.
define config.name = "FPT: 23:59 Escape Protocol"
define config.version = "3.1"
define build.name = "FPT2359EscapeProtocol"
define config.save_directory = "FPT2359EscapeProtocol"
define config.screen_width = 1280
define config.screen_height = 720
define config.has_sound = True
define config.has_music = True
define config.has_voice = False
define config.check_conflicting_properties = True
define config.window_icon = "images/backgrounds/GameIcon.png"
define config.auto_load = None
define config.history_length = 250

init python:
    # Launch always offers the menu. Explicit load/Continue and in-game chapter
    # transitions remain player actions, even if a launcher sets these flags.
    renpy.os.environ.pop("RENPY_SKIP_MAIN_MENU", None)
    renpy.os.environ.pop("RENPY_AUTO_LOAD", None)
    # Prevent local playtest ZIPs and screenshot checks entering later builds.
    build.classify("dist/**", None)
    build.classify("tests/**", None)
    build.classify("tools/**", None)
    build.classify("game/*testcases.rpy*", None)
    build.classify("game/saves/**", None)
    build.classify("*Implementation_Prompt.md", None)
    build.classify("*Polish_Improve_Prompt.md", None)
    build.classify("RESUME_CHAPTER2.md", None)
