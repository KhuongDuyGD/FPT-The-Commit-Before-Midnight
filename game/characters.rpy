# New backgrounds are 1672x941. Scale them to the project's 1280x720 stage.
# Time-of-day variants are declared even where the screenplay has no scene for them.
image bedroom_morning = Transform("images/backgrounds/KTXDay.png", size=(1280, 720))
image bedroom_afternoon = Transform("images/backgrounds/KTXAfternoon.png", size=(1280, 720))  # Reserved for a future afternoon dorm scene.
image bedroom_gaming = Transform("images/backgrounds/KTXNight.png", size=(1280, 720))
image dorm_morning = "bedroom_morning"
image dorm_night = "bedroom_gaming"
image campus_day = Transform("images/backgrounds/FPTUday.png", size=(1280, 720))  # Daytime FPTU view; replaces FPTUanime.png.
image campus_night = Transform("images/backgrounds/FPTUnight.png", size=(1280, 720))
image school_gate = Transform("images/backgrounds/FPTUGate.png", size=(1280, 720))
image school_night = Transform("images/backgrounds/FPTUGateNight.png", size=(1280, 720))
image school_gate_morning = "school_gate"
image school_gate_afternoon = "school_gate"  # No separate afternoon gate painting yet.
image school_gate_night = "school_night"
image classroom = Transform("images/backgrounds/ClassroomDay.png", size=(1280, 720))
image classroom_evening = Transform("images/backgrounds/ClassroomNight.png", size=(1280, 720))
image classroom_day = "classroom"
image classroom_afternoon = "classroom"  # Day painting is still appropriate at 15:45.
image classroom_night = "classroom_evening"
image hallway = Transform("images/backgrounds/HallwayFPTU.png", size=(1280, 720))
image hallway_afternoon = Transform("images/backgrounds/HallwayFPTUAfternoon.png", size=(1280, 720))
image hallway_night = Transform("images/backgrounds/HallwayFPTUNight.png", size=(1280, 720))
image canteen = Transform("images/backgrounds/CanteenFPTU.png", size=(1280, 720))
image canteen_afternoon = Transform("images/backgrounds/CanteenFPTUAfternoon.png", size=(1280, 720))
image canteen_night = Transform("images/backgrounds/CanteenFPTUNight.png", size=(1280, 720))
image computer_lab = Transform("images/backgrounds/ComputerLabDay.png", size=(1280, 720))

# Title-screen art. GameMainMenu.png has decorative baked-in buttons; the
# clickable controls in screens.rpy sit in a panel above those decorations.
image game_main_menu_background = Transform("images/backgrounds/GameMainMenu.png", size=(1280, 720))
image game_logo = Transform("images/backgrounds/LogoGame.png", zoom=0.22)

define CHARACTER_HEIGHT = 620

init -15 python:
    def character_sprite(filename):
        # Match height, preserve aspect ratio, and allow broad characters to be
        # wider. A fixed width/height contain box shrank the PE teacher to 448px.
        return Transform("images/characters/" + filename, ysize=CHARACTER_HEIGHT, fit="contain")

# Every standee shares the same baseline and height, including all expressions.
# Image tags are unchanged so existing saves still resolve the same artwork.
image player = character_sprite("MainNormal.png")
image player happy = character_sprite("MainGoodMood.png")
image player exhausted = character_sprite("MainExhaust.png")
image player angry = character_sprite("MainAngry.png")
image player cry = character_sprite("MainCry.png")
image minh = character_sprite("MinhAnime.png")
image linh = character_sprite("LinhAnime.png")
image thaydev = character_sprite("TeacherDev.png")
image colms = character_sprite("MissLMS.png")
image baove = character_sprite("MrSercurity.png")
image black = Solid("#000000")

# Character color identifies speakers even while placeholder sprites are used.
define p = Character("PLAYER", color="#ffcc72", callback=partial(stage_speaker, "player"))
define m = Character("MINH", color="#91d4ff", callback=partial(stage_speaker, "minh"))
define l = Character("LINH", color="#d0a7ff", callback=partial(stage_speaker, "linh"))
define dev = Character("THẦY DEV", color="#aef0c3", callback=partial(stage_speaker, "thaydev"))
define lms = Character("CÔ LMS", color="#ff667a", callback=partial(stage_speaker, "colms"))
define guard = Character("CHÚ BẢO VỆ", color="#f5dda1", callback=partial(stage_speaker, "baove"))
define n = Character(None, callback=partial(stage_speaker, None))
define crowd = Character("CẢ LỚP", callback=partial(stage_speaker, None))
define student = Character("MỘT SINH VIÊN", callback=partial(stage_speaker, None))
define friend = Character("BẠN BÈ DISCORD", callback=partial(stage_speaker, None))
define voice_chat = Character("VOICE CHAT", callback=partial(stage_speaker, None))
