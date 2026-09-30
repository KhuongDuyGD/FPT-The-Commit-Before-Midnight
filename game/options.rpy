# Development settings. Retain the original player-save namespace.
define config.name = "FPT: The Commit Before Midnight"
define config.version = "4.0"
define build.name = "FPTCommitBeforeMidnight"
define config.save_directory = "FPT2359EscapeProtocol"
define config.screen_width = 1920
define config.screen_height = 1080
define config.has_sound = True
define config.has_music = True
define config.has_voice = False
define config.check_conflicting_properties = True
define config.window_icon = "images/backgrounds/GameIcon_Logo/GameIcon.png"
define config.auto_load = None
define config.history_length = 250

init python:
    # Launch always offers the menu; loading a save remains a player action.
    renpy.os.environ.pop("RENPY_SKIP_MAIN_MENU", None)
    renpy.os.environ.pop("RENPY_AUTO_LOAD", None)
    # Prevent local playtest ZIPs and screenshot checks entering later builds.
    build.classify("dist/**", None)
    build.classify("tests/**", None)
    build.classify("tools/**", None)
    build.classify("game/**testcases.rpy*", None)
    build.classify("migration/**", None)
    build.classify("game/saves/**", None)
    build.classify("*Implementation_Prompt.md", None)
    build.classify("*Polish_Improve_Prompt.md", None)
    build.classify("RESUME_CHAPTER2.md", None)
