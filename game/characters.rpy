# Shared artwork and character definitions for Chapter 1.
# Existing image filenames are retained; missing art uses the safe asset helpers.
image bedroom_morning = background_asset("Main_Home/KTXDay.png")
image bedroom_gaming = background_asset("Main_Home/KTXNight.png")
image school_gate_morning = background_asset("School_Map/FPTUGateDay.png")
image school_gate_afternoon = background_asset("School_Map/FPTUGateAfternoon.png")
image hallway = background_asset("School_Map/HallwayFPTUDay.png")
image canteen = background_asset("School_Map/CanteenFPTUDay.png")
image computer_lab = background_asset("School_Map/ComputerLabDay.png")
image classroom_afternoon = background_asset("School_Map/ClassroomAfternoon.png")
image black = Solid("#000000")

define CHARACTER_HEIGHT = 930

init -15 python:
    def character_sprite(filename):
        path = "images/characters/" + filename
        if not renpy.loadable(path):
            return Solid("#53647a", xsize=260, ysize=CHARACTER_HEIGHT)
        return Transform(path, ysize=CHARACTER_HEIGHT, fit="contain")

image player normal = character_sprite("Main/Normal.png")
image player sleepy = character_sprite("Main/Sleepy.png")
image player annoyed = character_sprite("Main/Annoyed.png")
image player smug = character_sprite("Main/Smug.png")
image player surprised = character_sprite("Main/Surpised.png")
image player thinking = character_sprite("Main/Thinking.png")
image player deadpan = character_sprite("Main/Deadpan.png")
image player confused = character_sprite("Main/Confused.png")
image player nervous = character_sprite("Main/Nervous.png")
image player veryhappy = character_sprite("Main/VeryHappy.png")
image player panic = character_sprite("Main/Panic.png")
image player goodmood = character_sprite("Main/GoodMood.png")
image player determined = character_sprite("Main/Determined.png")
image player serious = character_sprite("Main/Serious.png")
image player embarrassed = character_sprite("Main/Embarrassed.png")
image player exhaust = character_sprite("Main/Exhaust.png")
image player sad = character_sprite("Main/Sad.png")
image player cry = character_sprite("Main/Cry.png")
image player empathy = character_sprite("Main/Empathy.png")
image player angry = character_sprite("Main/Angry.png")
# Compatibility for Chapter 1 saves created before the polish pass.
image player exhausted = character_sprite("Main/Exhaust.png")
image minh = character_sprite("Linh_and_Minh/MinhAnime.png")
image linh = character_sprite("Linh_and_Minh/LinhAnime.png")
image thaydev = character_sprite("Teacher/TeacherDev.png")

define m = Character("MINH", color="#91d4ff", callback=partial(stage_speaker, "minh"))
define l = Character("LINH", color="#d0a7ff", callback=partial(stage_speaker, "linh"))
define dev = Character("THẦY DEV", color="#aef0c3", callback=partial(stage_speaker, "thaydev"))
define n = Character(None, callback=partial(stage_speaker, None))
define crowd = Character("CẢ LỚP", callback=partial(stage_speaker, None))
