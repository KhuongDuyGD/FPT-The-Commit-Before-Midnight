define mc = Character("MC", color="#ffd493", callback=partial(stage_speaker, "player"))
define mc_thought = Character("MC (thought)", color="#ffd493", callback=partial(stage_speaker, "player"))
define mc_whisper = Character("MC (whisper)", color="#ffd493", callback=partial(stage_speaker, "player"))
define minh_discord = Character("MINH (Discord)", color="#91d4ff", callback=partial(stage_speaker, None))
define minh_message = Character("MINH (message)", color="#91d4ff", callback=partial(stage_speaker, None))
define minh_whisper = Character("MINH (whisper)", color="#91d4ff", callback=partial(stage_speaker, "minh"))
define linh_whisper = Character("LINH (whisper)", color="#d0a7ff", callback=partial(stage_speaker, "linh"))
define unknown_woman = Character("GIỌNG NỮ LẠ", color="#dfc9ff", callback=partial(stage_speaker, None))
define goddess = Character("NỮ THẦN", color="#dfc9ff", callback=partial(stage_speaker, "necrass"))
define necrass_sim = Character("NECRASS_SIM", color="#dfc9ff", callback=partial(stage_speaker, "necrass"))
define necrass = Character("Necrass", color="#dfc9ff", callback=partial(stage_speaker, "necrass"))
define pe_offscreen = Character("??? (off-screen)", color="#ffd495", callback=partial(stage_speaker, None))
define pe_message = Character("THẦY THỂ DỤC (message)", color="#ffd495", callback=partial(stage_speaker, None))
define nurse_voice = Character("GIỌNG NỮ", color="#bcf6d9", callback=partial(stage_speaker, None))
define system_note = Character("SYSTEM NOTE", color="#9db6ce", callback=partial(stage_speaker, None))
# Ren'Py supports ADVCharacter subclasses for specialized history behavior.
init -5 python:
    class SystemMessageCharacter(renpy.character.ADVCharacter):
        def add_history(self, *args, **kwargs):
            pass

        def pop_history(self):
            pass

define system_msg = SystemMessageCharacter(None, what_color="#bdcceb", callback=partial(stage_speaker, None))
image necrass = character_sprite("OtherNPC/IngameSystem.png")
image ngan = character_sprite("Ngan/Normal.png")
image nurse = character_sprite("Nurse/Nurse.png")
image pe = character_sprite("Teacher/PhysicalTeacher.png")
image sports_afternoon = background_asset("School_Map/SportsGroundAfternoon.png")
image infirmary_morning = background_asset("School_Map/MedicalRoomDay.png")
image infirmary_afternoon = background_asset("School_Map/MedicalRoomAfternoon.png")
define ngan = Character("NGÂN", color="#94dcff", callback=partial(stage_speaker, "ngan"))
define nurse = Character("CÔ Y TÁ", color="#bcf6d9", callback=partial(stage_speaker, "nurse"))
define pe = Character("THẦY THỂ DỤC", color="#ffd495", callback=partial(stage_speaker, "pe"))
