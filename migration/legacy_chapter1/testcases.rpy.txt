# Engine-level smoke tests for the two complete branches. Run with:
#   renpy.py <project-directory> test good_route
#   renpy.py <project-directory> test bad_route

testcase good_route:
    run Jump("start")
    advance until screen "choice"
    click "Dậy. Ngay."
    advance until screen "choice"
    click "Đọc đề trước khi hoảng."
    advance until screen "choice"
    click "Đi ăn trước."
    advance until screen "choice"
    click "Fix luôn."
    advance until screen "choice"
    click "Ăn như một con người bình thường."
    advance until screen "choice"
    click "Rút laptop cá nhân."
    advance until screen "choice"
    click "Về."
    advance until screen "ending_card"
    assert eval (escaped_school and persistent.good_ending_unlocked and escape_point >= 4 and final_choice == 'leave')
    click "Continue"
    assert screen "chapter1_good_actions"
    assert eval (persistent.chapter2_unlocked and persistent.chapter1_canonical_result == 'good')
    click "Tiếp tục Chương 2"
    advance until screen "choice"
    assert eval (current_chapter == 2 and chapter2_started and NganHintsRemaining == 3 and chapter1_canonical_result == 'good')


testcase bad_route:
    python:
        persistent.good_ending_unlocked = False
        persistent.chapter2_unlocked = False
    run Jump("start")
    advance until screen "choice"
    click "Dậy. Ngay."
    advance until screen "choice"
    click "Đọc đề trước khi hoảng."
    advance until screen "choice"
    click "Đi ăn trước."
    advance until screen "choice"
    click "Fix luôn."
    advance until screen "choice"
    click "Ăn như một con người bình thường."
    advance until screen "choice"
    click "Rút laptop cá nhân."
    advance until screen "choice"
    click "Ở lại thêm chút."
    advance until screen "ending_card"
    assert eval (not escaped_school and persistent.bad_ending_unlocked and assignment_uploaded and final_choice == 'stay')
    assert eval (not chapter2_is_unlocked())
    click "Continue"
    advance until screen "post_ending_actions"
    assert screen "post_ending_actions"


testcase failed_escape:
    # Leaving without enough Escape Points still reaches the night route.
    run Jump("start")
    advance until screen "choice"
    click "Năm phút nữa thôi."
    advance until screen "choice"
    click "Panic trước, đọc đề sau."
    advance until screen "choice"
    click "Join meeting."
    advance until screen "choice"
    click "Để chiều."
    advance until screen "choice"
    click "Vừa ăn vừa code."
    advance until screen "choice"
    click "Chờ."
    advance until screen "choice"
    click "Về."
    advance until screen "ending_card"
    assert eval (final_choice == 'leave' and not escaped_school and persistent.bad_ending_unlocked)


testcase ui_screens:
    run Jump("start")
    assert eval (active_speaker_image("PLAYER") == "player exhausted" and active_speaker_image("MINH") == "minh" and active_speaker_image(None) is None)
    run SetVariable("player_expression", "angry")
    assert eval (active_speaker_image("PLAYER") == "player angry")
    run SetVariable("player_expression", "cry")
    assert eval (active_speaker_image("PLAYER") == "player cry")
    run ShowMenu("save")
    assert screen "save"
    run ShowMenu("load")
    assert screen "load"
    run ShowMenu("preferences")
    assert screen "preferences"
    run ShowMenu("history")
    assert screen "history"
    run ShowMenu("ending_gallery")
    assert screen "ending_gallery"


testcase main_menu_assets:
    run ShowMenu("main_menu")
    assert screen "main_menu"
    assert eval (renpy.loadable("images/backgrounds/GameMainMenu.png") and renpy.loadable("images/backgrounds/LogoGame.png") and renpy.loadable("images/backgrounds/GameIcon.png"))
    pause 1.0
    screenshot "ch2-main-menu.png"
