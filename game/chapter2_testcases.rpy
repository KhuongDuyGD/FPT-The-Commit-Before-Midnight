# Run with an isolated --savedir so test unlocks cannot change a player's gallery.
# Tests use real menu clicks and real save/load, rather than jumping to endings.
testcase chapter2_locked:
    python:
        persistent.good_ending_unlocked = False
        persistent.chapter2_unlocked = False
        persistent.chapter1_canonical_result = None
    run ShowMenu("chapter_select")
    assert screen "chapter_select"
    assert eval (not chapter2_is_unlocked())
    run Jump("chapter2_start")
    pause 0.2
    assert eval (not chapter2_started)

testcase chapter2_good:
    parameter first_answer = ["A. Ý bạn khá giống", "D. Bạn có người yêu chưa?"]
    python:
        persistent.good_ending_unlocked = True
        unlock_chapter2()
    run ShowMenu("chapter_select")
    click "Chương 2 — LOVE PROTOCOL"
    pause 0.3
    advance until screen "choice"
    assert eval (chapter1_canonical_result == 'good' and NganHintsRemaining == 3 and not renpy.get_screen('stats_hud'))
    click "Đi lẹ không trễ."
    advance until screen "choice"
    assert eval (set(stage_cast) == {'player', 'minh', 'ngan', 'nghi', 'philosophy'} and stage_visual == ('player', 'ngan', 'nghi') and all(renpy.showing('cast_' + a) for a in stage_visual) and not renpy.showing('cast_philosophy') and not renpy.showing('cast_minh'))
    pause 1.0
    screenshot "ch2-first-choice.png"
    click "Hỏi Ngân (3/3)"
    assert screen "ngan_hint_message"
    assert eval (NganHintsUsed == 1 and NganHintsRemaining == 2)
    pause 1.0
    screenshot "ch2-hint.png"
    click "Đã hiểu"
    assert screen "choice"
    assert not "Hỏi Ngân (2/3)"
    click expression first_answer
    advance until screen "choice"
    click "Hỏi Ngân (2/3)"
    assert eval (NganHintsUsed == 2 and NganHintsRemaining == 1)
    click "Đã hiểu"
    click "A. Bạn đang đọc gì vậy?"
    advance until screen "choice"
    click "Giải thích bug cho Nghi"
    advance until screen "choice"
    click "A. Cố chạy cạnh Nghi."
    advance until screen "choice"
    click "Hỏi Ngân (1/3)"
    click "Đã hiểu"
    assert eval (NganHintsRemaining == 0 and NganHintsUsed == 3)
    run Function(use_ngan_hint)
    assert eval (NganHintsRemaining == 0 and NganHintsUsed == 3)
    click "A. Ổn. Chỉ hơi xấu hổ thôi."
    advance until screen "choice"
    click "Cảm ơn Nghi đã tới thăm"
    advance until screen "choice"
    click "Nhờ Ngân xem Nghi"
    advance until screen "choice"
    click "A. Chắc bạn chỉ không biết"
    advance until screen "choice"
    click "A. Mày đúng là best wingman."
    advance until screen "choice"
    assert not "Gọi Ngân lại."
    click "Đợi Nghi trên sân thượng."
    advance until screen "choice"
    assert eval ((NghiAffinity, NghiComfort) == ((16, 8) if CH2MajorFail else (18, 12)) and NganHintsRemaining == 0)
    assert not "Hỏi Ngân"
    click "Tôi thích bạn."
    advance until screen "chapter2_cg"
    assert eval (chapter2_completed and chapter2_ending == 'nghi_good' and persistent.ending_nghi_good_unlocked and renpy.showing('cg_nghi_good'))
    pause 1.0
    screenshot "ch2-good-ending.png"
    click "Continue"
    advance until "TO BE CONTINUED IN CHAPTER 3"
    advance until screen "chapter2_end_menu"
    assert eval (not game_route_complete and not chapter3_route_locked_for_this_save)

testcase chapter2_bad:
    python:
        persistent.chapter2_unlocked = True
    run Jump("chapter2_start")
    pause 0.2
    advance until screen "choice"
    click "Sáng nay trông mày vui dữ."
    advance until screen "choice"
    click "D. Bạn có người yêu chưa?"
    advance until screen "choice"
    click "B. Hôm nay bạn xinh thật."
    advance until screen "choice"
    click "Tiếp tục code một mình."
    advance until screen "choice"
    click "C. Cố vượt Nghi"
    advance until screen "choice"
    click "C. Tôi cố chạy vì bạn."
    advance until screen "choice"
    click "Cố gây ấn tượng thêm."
    advance until screen "choice"
    click "Nhờ Ngân xem Nghi"
    advance until screen "choice"
    click "C. Vì bạn dễ thương."
    advance until screen "choice"
    click "D. Mai giúp tao tiếp nha."
    advance until screen "choice"
    assert not "Gọi Ngân lại."
    click "Đợi Nghi trên sân thượng."
    advance until screen "choice"
    click "Tôi thích bạn."
    advance until screen "chapter2_cg"
    assert eval (chapter2_ending == 'nghi_bad' and persistent.ending_nghi_bad_unlocked and CH2MajorFail and renpy.showing('nearby_pub_night') and stage_cast == ('player', 'minh'))
    pause 1.0
    screenshot "ch2-bad-ending.png"

testcase chapter2_ngan:
    python:
        persistent.chapter2_unlocked = True
    run Jump("chapter2_start")
    pause 0.2
    advance until screen "choice"
    click "Sáng nay trông mày xinh đấy."
    advance until screen "choice"
    click "B. Ừ, mình cũng nghĩ vậy."
    advance until screen "choice"
    click "D. Im lặng ngồi cạnh."
    advance until screen "choice"
    click "Tắt laptop, cùng Nghi"
    advance until screen "choice"
    click "D. Khi Ngân hụt chân"
    advance until screen "choice"
    click "D. Tôi nghĩ thầy thể dục"
    advance until screen "choice"
    click "Cảm ơn Nghi đã tới thăm"
    advance until screen "choice"
    click "Hỏi thăm chân Ngân"
    advance until screen "choice"
    click "B. Tôi thấy bạn bình thường mà."
    advance until screen "choice"
    click "C. Mà... dạo này"
    advance until screen "choice"
    assert eval (NganAffinity == 10 and NganSpecialFlags == 4 and NganEndingAvailable and NganHintsUsed == 0)
    pause 1.0
    screenshot "ch2-secret-choice.png"
    click "Gọi Ngân lại."
    advance until screen "chapter2_cg"
    assert eval (chapter2_ending == 'ngan' and persistent.ending_ngan_unlocked and game_route_complete and chapter3_route_locked_for_this_save and renpy.showing('cg_ngan'))
    pause 1.0
    screenshot "ch2-ngan-ending.png"
    click "Continue"
    advance until screen "chapter2_end_menu"
    assert not "TO BE CONTINUED IN CHAPTER 3"
    click "Chapter Select"
    assert screen "chapter_select"
    click "Return"

testcase chapter2_save_load:
    python:
        persistent.chapter2_unlocked = True
    run Jump("chapter2_start")
    pause 0.2
    advance until screen "choice"
    click "Đi lẹ không trễ."
    advance until screen "choice"
    click "Hỏi Ngân (3/3)"
    click "Đã hiểu"
    click "A. Ý bạn khá giống"
    advance until screen "choice"
    assert eval (ch2_hint_context == 'library' and NghiAffinity == 2 and NghiComfort == 1 and NganHintsRemaining == 2)
    python:
        renpy.save('ch2-exact-state')
        NghiAffinity = 99
        NghiComfort = -99
        NganHintsRemaining = 0
    run Function(renpy.load, 'ch2-exact-state')
    pause 0.4
    assert screen "choice"
    assert eval (ch2_hint_context == 'library' and NghiAffinity == 2 and NghiComfort == 1 and NganHintsRemaining == 2 and NganHintsUsed == 1 and stage_cast == ('player', 'nghi'))
    # Chapter Select starts a clean chapter without carrying over terminal flags.
    run ShowMenu("chapter_select")
    click "Chương 2 — LOVE PROTOCOL"
    pause 0.3
    advance until screen "choice"
    assert eval (NghiAffinity == 0 and NganHintsRemaining == 3 and not game_route_complete)

testcase chapter2_resolver_and_focus:
    python:
        # Boundary and recovery checks complement the full playthroughs above.
        NghiAffinity, NghiComfort, CH2MajorFail = 12, 8, True
    assert eval (resolve_chapter2(True) == 'nghi_good' and resolve_chapter2(False) == 'nghi_bad')
    python:
        NghiAffinity, NghiComfort = 11, 8
    assert eval (resolve_chapter2() == 'nghi_bad')
    python:
        NghiAffinity, NghiComfort = 12, 7
        NganAffinity, NganSpecialFlags, NganHintsUsed = 10, 3, 1
    assert eval (resolve_chapter2() == 'nghi_bad' and ngan_route_available())
    python:
        NganHintsUsed = 2
    assert eval (not ngan_route_available())
    run Jump("start")
    pause 1.0
    run Function(set_stage, 'player', 'minh')
    run Function(stage_speaker, 'minh', 'begin')
    pause 0.3
    assert eval (stage_focus == 'minh' and renpy.showing('cast_player') and renpy.showing('cast_minh'))
    pause 1.0
    screenshot "ch1-speaker-focus.png"
    run Function(stage_speaker, None, 'begin')
    pause 0.3
    assert eval (stage_focus is None and renpy.showing('cast_player') and renpy.showing('cast_minh'))
    pause 1.0
    screenshot "ch1-narration-focus.png"
    run Function(set_stage, 'player')
    assert eval (not renpy.showing('cast_minh') and renpy.showing('cast_player'))
    run Jump("new_game_plus")
    advance until screen "choice"
    assert eval (current_chapter == 1 and energy == 100 and pending_tasks == 0 and not escaped_school and not chapter2_started)

testcase chapter2_unlock_persistence:
    python:
        persistent.good_ending_unlocked = True
        persistent.chapter2_unlocked = False
    assert eval (chapter2_is_unlocked())
    run Function(unlock_chapter2)
    python:
        import os
        saved_persistent = renpy.persistent.load(os.path.join(config.savedir, 'persistent'))
    assert eval (saved_persistent.chapter2_unlocked and saved_persistent.chapter1_canonical_result == 'good')
    run ShowMenu("ending_gallery")
    assert screen "ending_gallery"
    pause 1.0
    assert "View ending"
    screenshot "ch2-gallery.png"

testcase chapter1_v2_save_compatibility:
    # Supply a save produced by the unmodified v2 build in the isolated test
    # savedir. Developers without that fixture exit this optional check.
    if not eval (renpy.can_load('chapter1-v2-compatibility')):
        exit
    run Function(renpy.load, 'chapter1-v2-compatibility')
    pause 0.3
    assert screen "choice"
    assert eval (current_chapter == 1 and save_schema_version == 3 and energy == 100 and pending_tasks == 0 and NganHintsRemaining == 3)
    click "Dậy. Ngay."
    advance until screen "choice"
    assert eval (attendance_done and stage_cast == ('player', 'minh', 'thaydev'))

testcase chapter2_hint_rollback:
    python:
        persistent.chapter2_unlocked = True
    run Jump("chapter2_start")
    pause 1.0
    advance until screen "choice"
    click "Đi lẹ không trễ."
    advance until screen "choice"
    click "Hỏi Ngân (3/3)"
    click "Đã hiểu"
    assert eval (not Rollback().get_sensitive())
    keysym "K_PAGEUP"
    pause 0.3
    assert eval (NganHintsRemaining == 2 and NganHintsUsed == 1 and 'first_contact' in ch2_hint_used_choices)
