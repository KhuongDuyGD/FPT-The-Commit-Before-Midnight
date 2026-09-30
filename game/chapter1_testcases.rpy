# Engine integration checks. Run through tools/check_rebuild.ps1 in a project copy.
testsuite global:
    teardown:
        exit

init python:
    _test.screenshot_directory = "tests/rebuild/screenshots"
    def rebuild_panel_geometry(screen):
        panel = renpy.get_displayable(screen, "window")
        return panel.get_placement(), renpy.render(panel, 1920, 1080, 0, 0).get_size()

    # A separate normal-launch probe verifies boot without the test runner.
    if renpy.os.environ.get("FPT_REBUILD_STARTUP_REPORT"):
        def rebuild_startup_probe():
            import json
            path = renpy.os.environ["FPT_REBUILD_STARTUP_REPORT"]
            menu_visible = bool(renpy.get_screen("main_menu"))
            gameplay = bool(energy_visible or renpy.get_screen("energy_hud"))
            if not menu_visible and not gameplay:
                return
            renpy.screenshot(path + ".png")
            with open(path, "w", encoding="utf-8") as report:
                json.dump(dict(main_menu=menu_visible, gameplay=gameplay,
                               continue_available=latest_compatible_save() is not None,
                               version=config.version), report)
            renpy.quit(status=0 if menu_visible and not gameplay else 1, save=False)
        config.periodic_callbacks.append(rebuild_startup_probe)

testcase ch1_home_safe:
    parameter cosmetic = ["Tắt Discord.", "Nhìn tin nhắn 10 giây.", "Gõ “không” rồi xóa."]
    run ShowMenu("main_menu")
    click "New Game"
    pause 0.15
    advance until screen "choice"
    assert eval (energy == 60 and not overslept and current_route == 'NORMAL')
    click "“Dậy ngay. Không ngu nữa.”"
    advance until screen "choice"
    click "Ăn sáng tử tế."
    advance until screen "choice"
    assert eval (energy == 75 and breakfast_eaten and responsible_once)
    click "“Mua tao chai nước đi, người anh em.”"
    advance until screen "choice"
    click "“Có đồ ăn không?”"
    advance until screen "choice"
    click "Nhìn sang Linh với ánh mắt cầu cứu."
    advance until screen "choice"
    assert eval (energy == 83 and affinity_linh == 1)
    click "“Status gì?”"
    advance until screen "choice"
    click "Ăn một bữa tử tế."
    advance until screen "choice"
    assert eval (energy == 90 and affinity_ngan == 1 and len(stage_visual) <= 3)
    click "“Dạ em còn deadline.”"
    advance until screen "choice"
    assert eval (current_route == 'HOME_SAFE' and not route_locked and not pe_club_captured)
    click expression cosmetic
    advance until "Ta mong rằng cậu vẫn"
    pause 0.4
    screenshot "rebuild-long-dialogue.png"
    advance until screen "chapter1_end"
    assert eval (chapter1_completed and current_route == 'HOME_SAFE' and energy == 90)
    assert eval ('HOME_SAFE' in persistent.chapter1_routes and not energy_visible)
    assert eval (chapter1_cg_seen('pe_intro') and chapter1_cg_seen('good_sleep'))
    assert not "Tiếp tục Chương 2"
    click "New Game"
    advance until screen "choice"
    assert eval (energy == 60 and not chapter1_completed and current_route == 'NORMAL' and affinity_linh == 0 and affinity_ngan == 0)
    assert eval ('HOME_SAFE' in persistent.chapter1_routes)

testcase ch1_black_alloy:
    run ShowMenu("main_menu")
    click "New Game"
    pause 0.15
    advance until screen "choice"
    click "“Dậy ngay. Không ngu nữa.”"
    advance until screen "choice"
    click "Uống cà phê thay cơm."
    advance until screen "choice"
    click "“Tối nay tao ngủ sớm.”"
    advance until screen "choice"
    click "“Nếu tôi ngã, nhớ save project trước.”"
    advance until screen "choice"
    click "Trao đổi với Minh."
    advance until screen "choice"
    click "“Cho tôi dựa bàn ngủ 5 phút.”"
    advance until screen "choice"
    click "Cà phê lần hai."
    advance until screen "choice"
    click "“Dạ em rất thích thể thao ạ.”"
    advance until screen "chapter1_end"
    assert eval (current_route == 'BLACK_ALLOY_CLUB' and pe_club_captured and not route_locked and energy == 66)
    assert eval (coffee_only and fake_promise and too_much_coffee and affinity_linh == 1)
    assert eval (chapter1_cg_seen('pe_intro') and get_trust('linh') == 1)
    assert eval ('BLACK_ALLOY_CLUB' in persistent.chapter1_routes)

testcase ch1_walking_corpse:
    run ShowMenu("main_menu")
    click "New Game"
    pause 0.15
    advance until screen "choice"
    click "“Dậy ngay. Không ngu nữa.”"
    advance until screen "choice"
    click "Bỏ luôn, chạy đi học."
    advance until screen "choice"
    click "“Tối nay làm thêm vài ván?”"
    advance until screen "choice"
    click "“Yên tâm, tôi khỏe.”"
    advance until screen "choice"
    click "Tự làm nghiêm túc."
    advance until screen "choice"
    click "“Tôi đi mua nước. Ai uống gì không?”"
    advance until screen "choice"
    click "Bỏ bữa để làm task."
    advance until screen "choice"
    click "“Dạ em không chơi môn nào hết.”"
    advance until screen "chapter1_end"
    assert eval (current_route == 'WALKING_CORPSE' and energy == 19 and not pe_club_captured and not route_locked)
    assert eval (not overslept and still_no_regret and deadline_greed and dev_respect == 1 and affinity_linh == 1 and affinity_ngan == 1)
    assert eval (chapter1_cg_seen('walking_corpse'))

testcase ch1_final_resistance:
    parameter starting_energy = [26, 25, 20]
    run ShowMenu("main_menu")
    click "New Game"
    pause 0.15
    advance until screen "choice"
    python:
        energy = starting_energy
        player_is_on_campus = True
        campus_period = 'afternoon'
    run Jump("ch1_after_class")
    advance until screen "choice"
    click "Giả vờ nhận điện thoại rồi lùi dần."
    advance until screen "choice"
    assert eval (pe_pressure == 2)
    click "Từ chối lịch sự lần cuối."
    advance until screen "chapter1_end"
    assert eval (energy == starting_energy - 5)
    assert eval (current_route == ('WALKING_CORPSE' if starting_energy == 26 else 'BLACK_ALLOY_CLUB'))
    assert eval (not route_locked and not infirmary_window_open)

testcase ch1_infirmary:
    parameter breakfast = ['food', 'coffee', 'skip']
    # This fixture exercises the early checkpoint and nurse dialogue variants.
    run ShowMenu("main_menu")
    click "New Game"
    pause 0.15
    advance until screen "choice"
    python:
        energy = 15
        breakfast_eaten = breakfast == 'food'
        coffee_only = breakfast == 'coffee'
        pe_club_captured = True
        player_is_on_campus = True
        infirmary_window_open = True
    run Jump("ch1_break")
    advance until screen "choice"
    click "“Status gì?”"
    advance until screen "chapter1_end"
    assert eval (current_route == 'INFIRMARY' and route_locked and not infirmary_window_open and chapter1_completed and energy == 15)
    assert eval (renpy.showing('infirmary_afternoon') and 'pe' not in stage_cast and affinity_ngan == 1)
    assert eval (chapter1_cg_seen('nurse_intro'))
    run Function(change_energy, 100)
    run Function(update_day_route, True)
    assert eval (energy == 100 and current_route == 'INFIRMARY' and route_locked)

testcase ch1_infirmary_natural:
    run ShowMenu("main_menu")
    python:
        persistent.chapter1_cg_seen = set()
    click "New Game"
    pause 0.15
    advance until screen "choice"
    click "“Ngủ tiếp. Gặp lại nữ thần.”"
    advance until screen "choice"
    click "Bỏ luôn, chạy đi học."
    advance until screen "choice"
    click "Chạy nước rút ra ngoài."
    advance until screen "choice"
    click "“Tối nay làm thêm vài ván?”"
    advance until screen "choice"
    click "“Yên tâm, tôi khỏe.”"
    advance until screen "choice"
    click "Tự làm nghiêm túc."
    advance until screen "choice"
    click "“Status gì?”"
    advance until screen "choice"
    assert eval (energy == 32 and not route_locked and infirmary_window_open)
    click "Bỏ bữa để làm task."
    advance until screen "chapter1_end"
    assert eval (energy == 12 and current_route == 'INFIRMARY' and route_locked and not infirmary_window_open)
    assert eval (chapter1_cg_seen('nurse_intro') and not chapter1_cg_seen('pe_intro') and 'pe' not in stage_cast)
    run ShowMenu("main_menu")
    click "Gallery"
    assert screen "gallery"
    assert "First Aid"
    assert not "The Encounter"

testcase ch1_leaving_low_energy:
    parameter starting_energy = [10, 20]
    run ShowMenu("main_menu")
    click "New Game"
    pause 0.15
    advance until screen "choice"
    python:
        energy = starting_energy
        player_is_on_campus = True
        infirmary_window_open = False
        pe_club_captured = False
    run Jump("ch1_leaving_campus")
    advance until screen "chapter1_end"
    assert eval (current_route == 'WALKING_CORPSE' and energy == starting_energy and not route_locked)
    assert eval (chapter1_cg_seen('walking_corpse'))

testcase ch1_menu_and_gallery:
    python:
        assert [menu_chapter_index(i) for i in range(1, 6)] == [1, 2, 3, 4, 5]
        assert menu_chapter_index(None) == 1 and menu_chapter_index(9) == 1
        persistent.last_played_chapter = 3
        persistent.chapter1_cg_seen = set()
    run ShowMenu("main_menu")
    pause 0.4
    screenshot "polish-menu-chapter-3.png"
    assert eval (persistent.last_played_chapter == 3)
    click "Gallery"
    assert screen "gallery"
    pause 0.3
    screenshot "polish-gallery-locked.png"
    assert not "First Aid"
    assert eval (not chapter1_cg_seen('nurse_intro'))
    run ShowMenu("main_menu")
    click "New Game"
    pause 0.15
    advance until screen "choice"
    assert eval (persistent.last_played_chapter == 1 and player_expression == 'thinking')

testcase ch1_save_load_rollback:
    run ShowMenu("main_menu")
    click "New Game"
    pause 0.15
    advance until screen "choice"
    python:
        renpy.save('1-6')
    assert eval (compatible_save('1-6') and latest_compatible_save() == '1-6')
    click "“Ngủ tiếp. Gặp lại nữ thần.”"
    advance until "Tôi quay lại rồi."
    assert eval (energy == 65 and overslept and Rollback().get_sensitive() and stage_image('player') == 'player goodmood')
    keysym "K_PAGEUP"
    pause 0.2
    advance until screen "choice"
    assert eval (energy == 60 and not overslept and not responsible_once)
    click "“Dậy ngay. Không ngu nữa.”"
    advance until screen "choice"
    python:
        energy = 1
        affinity_linh = 99
        route_locked = True
    run Function(renpy.load, '1-6')
    pause 0.4
    assert screen "choice"
    assert eval (energy == 60 and not overslept and not route_locked and affinity_linh == 0)
    run ShowMenu("main_menu")
    click "Continue"
    pause 0.3
    assert screen "choice"
    assert eval (energy == 60 and current_route == 'NORMAL')

testcase ch1_ui:
    parameter window_size = [(960, 540), (1280, 720), (1024, 768), (1920, 1080)]
    run Function(renpy.set_physical_size, window_size)
    run ShowMenu("main_menu")
    pause 0.5
    screenshot "rebuild-main-menu.png"
    click "New Game"
    pause 0.2
    advance until "…Hay ngủ thêm đúng năm phút?"
    python:
        panel_geometry = rebuild_panel_geometry('say')
    advance until screen "choice"
    assert eval (rebuild_panel_geometry('choice') == panel_geometry and panel_geometry[1] == (1840, 330))
    assert eval (renpy.get_displayable('choice', 'choice_list').get_placement()[1:4:2] == (CHOICE_BOTTOM, 1.0))
    pause 0.4
    screenshot "rebuild-choice.png"
    run ShowMenu("save")
    assert screen "save"
    click "SLOT 1"
    if screen "confirm":
        click "Yes"
    assert eval (compatible_save('1-1'))
    run ShowMenu("load")
    assert screen "load"
    run ShowMenu("preferences")
    assert screen "preferences"
    pause 0.4
    assert eval (renpy.render(renpy.get_displayable('preferences', 'text_speed_slider'), 1920, 1080, 0, 0).get_size() == (1032, 24))
    assert eval (renpy.render(renpy.get_displayable('preferences', 'preferences_panel'), 1920, 1080, 0, 0).get_size()[1] < 750)
    screenshot "rebuild-preferences.png"
    run ShowMenu("history")
    assert screen "history"
    assert eval (not any(h.what in ('FIRST CHOICE', 'SYSTEM ENTITY: NECRASS_SIM.exe') for h in _history_list))
    run ShowMenu("about")
    assert screen "about"
    run Function(renpy.set_physical_size, (1280, 720))

testcase ch1_route_boundaries:
    python:
        assert resolve_day_route(15, True, True, True) == 'INFIRMARY'
        assert resolve_day_route(16, True, False, True) == 'BLACK_ALLOY_CLUB'
        assert resolve_day_route(10, False, False, True) == 'WALKING_CORPSE'
        assert resolve_day_route(20, False, False, True) == 'WALKING_CORPSE'
        assert resolve_day_route(30, False, False, True) == 'WALKING_CORPSE'
        assert resolve_day_route(31, False, False, True) == 'HOME_SAFE'
        assert resolve_day_route(100, True, False, True, True, 'INFIRMARY') == 'INFIRMARY'
        assert resolve_day_route(100, False, False, True, False, 'BLACK_ALLOY_CLUB') == 'BLACK_ALLOY_CLUB'
    run ShowMenu("main_menu")
    click "New Game"
    pause 0.15
    advance until screen "choice"
    run Function(change_energy, -1000)
    assert eval (energy == 0)
    run Function(change_energy, 1000)
    assert eval (energy == 100)
    run Function(change_trust, 'future_character', 2)
    assert eval (trust_at_least('future_character', 2))
