# Save-local relationship state. Affinity stays hidden from the player.
default current_chapter = 1
default save_schema_version = 3
default chapter1_canonical_result = None
default chapter2_started = False
default chapter2_completed = False
default chapter2_ending = None
default game_route_complete = False
default chapter3_route_locked_for_this_save = False
default NghiAffinity = 0
default NghiComfort = 0
default NganAffinity = 0
default NganSpecialFlags = 0
default NganHintsRemaining = 3
default NganHintsUsed = 0
default NganEndingAvailable = False
default CH2MajorFail = False
default ch2_hint_context = None
default ch2_hint_used_choices = []
default ch2_sports_choice = None
default ngan_expression = "normal"
default nghi_expression = "normal"

# Existing players who already obtained Chapter 1's Good Ending qualify too.
default persistent.chapter2_unlocked = False
default persistent.chapter1_canonical_result = None
default persistent.ending_nghi_good_unlocked = False
default persistent.ending_nghi_bad_unlocked = False
default persistent.ending_ngan_unlocked = False

init python:
    CH2_HINTS = {
        "first_contact": "Nếu mày chọn D tao sẽ tự tay đẩy mày ra khỏi nhóm.",
        "library": "Đừng chọn B.\nTao nghiêm túc.",
        "infirmary": "Đừng có flex.",
        "confession": "Đừng cố nói câu gì hay.\nNói thật thôi.",
    }

    def chapter2_is_unlocked():
        return bool(persistent.chapter2_unlocked or persistent.good_ending_unlocked)

    def unlock_chapter2():
        changed = not persistent.chapter2_unlocked or persistent.chapter1_canonical_result != "good"
        persistent.chapter2_unlocked = True
        persistent.chapter1_canonical_result = "good"
        if changed:
            renpy.save_persistent()

    def reset_chapter2_state():
        # Only a new chapter playthrough refills hints. Neither a scene change
        # nor asking Ngân for ordinary advice invokes this function.
        global NghiAffinity, NghiComfort, NganAffinity, NganSpecialFlags
        global NganHintsRemaining, NganHintsUsed, NganEndingAvailable, CH2MajorFail
        global chapter2_started, chapter2_completed, chapter2_ending
        global game_route_complete, chapter3_route_locked_for_this_save
        global ch2_hint_context, ch2_hint_used_choices, ch2_sports_choice
        global ngan_expression, nghi_expression
        NghiAffinity = NghiComfort = NganAffinity = NganSpecialFlags = 0
        NganHintsRemaining, NganHintsUsed = 3, 0
        NganEndingAvailable = CH2MajorFail = False
        chapter2_started = chapter2_completed = False
        chapter2_ending = None
        game_route_complete = chapter3_route_locked_for_this_save = False
        ch2_hint_context, ch2_hint_used_choices, ch2_sports_choice = None, [], None
        ngan_expression = nghi_expression = "normal"

    def hint_available():
        return (current_chapter == 2 and ch2_hint_context in CH2_HINTS
                and NganHintsRemaining > 0
                and ch2_hint_context not in ch2_hint_used_choices)

    def use_ngan_hint():
        global NganHintsRemaining, NganHintsUsed
        if not hint_available():
            return
        key = ch2_hint_context
        NganHintsRemaining -= 1
        NganHintsUsed += 1
        ch2_hint_used_choices.append(key)
        # Normal rollback cannot refund a consumed hint. Loading a save restores
        # that save's exact chapter state, as it does for every other choice.
        renpy.block_rollback()
        renpy.sound.play(sfx_notification)
        renpy.show_screen("ngan_hint_message", message=CH2_HINTS[key])
        renpy.restart_interaction()

    def ngan_route_available():
        return NganAffinity >= 10 and NganSpecialFlags >= 3 and NganHintsUsed <= 1

    def resolve_chapter2(sincere=True):
        return "nghi_good" if sincere and NghiAffinity >= 12 and NghiComfort >= 8 else "nghi_bad"

    def finish_chapter2(ending):
        global chapter2_completed, chapter2_ending, game_route_complete
        global chapter3_route_locked_for_this_save, ch2_hint_context
        chapter2_completed, chapter2_ending, ch2_hint_context = True, ending, None
        if ending == "ngan":
            persistent.ending_ngan_unlocked = True
            game_route_complete = chapter3_route_locked_for_this_save = True
        elif ending == "nghi_good":
            persistent.ending_nghi_good_unlocked = True
        else:
            persistent.ending_nghi_bad_unlocked = True
        renpy.save_persistent()

    def migrate_chapter_state():
        global save_schema_version
        save_schema_version = 3
        if chapter2_is_unlocked():
            unlock_chapter2()
        # Old v2 saves predate stage_cast. Infer physical cast from the saved
        # background, then later scene entrances/exits use the explicit script.
        if current_chapter == 1 and not stage_cast:
            if renpy.showing("bedroom_morning") or renpy.showing("bedroom_gaming"):
                set_stage("player")
            elif renpy.showing("school_gate_night") or renpy.showing("school_gate_afternoon"):
                set_stage("player", "baove")
            elif renpy.showing("classroom") or renpy.showing("classroom_afternoon"):
                set_stage("player", "minh", "thaydev")
            elif renpy.showing("classroom_evening"):
                set_stage("player", "minh", "linh")
            else:
                set_stage("player", "minh")
        migrate_stage()

label before_main_menu:
    if chapter2_is_unlocked():
        $ unlock_chapter2()
    return

label main_menu:
    # This minimal custom UI doesn't load Ren'Py's template menu layout module.
    # An explicit entry point prevents its fallback from returning into start.
    while True:
        call screen main_menu

label after_load:
    $ migrate_chapter_state()
    return

label chapter2_start:
    if not chapter2_is_unlocked():
        $ renpy.notify("Hoàn thành Good Ending Chương 1 để mở Chương 2.")
        return
    $ reset_chapter2_state()
    $ current_chapter = 2
    $ chapter2_started = True
    $ chapter1_canonical_result = "good"
    $ escaped_school = True
    $ final_choice = "leave"
    $ energy, sanity, academic_progress, escape_point, pending_tasks = 100, 100, 8, 4, 1
    $ attendance_done = quiz_done = group_task_done = True
    $ assignment_uploaded = False
    $ player_expression = "normal"
    $ new_game_plus = False
    hide screen stats_hud
    $ set_stage()
    centered "CHƯƠNG 2\nLOVE PROTOCOL"
    jump CH2_00
