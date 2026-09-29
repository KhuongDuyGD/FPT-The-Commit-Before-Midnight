# Presentation regressions. Use an isolated --savedir, never player saves.
init python:
    def polish_panel_geometry(screen):
        panel = renpy.get_displayable(screen, "window")
        return panel.get_placement(), renpy.render(panel, config.screen_width, config.screen_height, 0, 0).get_size()

    # Optional normal-process startup probe; testcases are excluded from release.
    if renpy.os.environ.get("FPT_POLISH_STARTUP_REPORT"):
        def polish_probe_startup():
            import json
            report_path = renpy.os.environ["FPT_POLISH_STARTUP_REPORT"]
            menu_visible = bool(renpy.get_screen("main_menu"))
            # Ren'Py's first-launch graphics check can briefly use a say screen.
            gameplay_visible = bool(renpy.get_screen("stats_hud") or chapter2_started)
            if not menu_visible and not gameplay_visible:
                return
            renpy.screenshot(report_path + ".png")
            with open(report_path, "w", encoding="utf-8") as report:
                json.dump({"main_menu": menu_visible, "gameplay": gameplay_visible,
                           "chapter2_started": chapter2_started, "version": config.version}, report)
            renpy.quit(status=0 if menu_visible and not gameplay_visible else 1, save=False)
        config.periodic_callbacks.append(polish_probe_startup)

testcase polish_startup:
    # Menu controls; a separate normal-launch probe verifies the startup path.
    run ShowMenu("main_menu")
    pause 0.5
    assert screen "main_menu"
    assert eval (config.auto_load is None)
    assert "Continue"
    assert "New Game"
    assert "Chapter Select"
    pause 0.6
    screenshot "polish-startup.png"
    click "New Game"
    advance until screen "choice"
    assert eval (current_chapter == 1 and stage_visual == ('player',))

testcase polish_composition_and_layout:
    parameter window_size = [(960, 540), (1280, 720), (1024, 768)]
    run Function(renpy.set_physical_size, window_size)
    python:
        persistent.chapter2_unlocked = True
    run Jump("chapter2_start")
    advance until screen "choice"
    click "Đi lẹ không trễ."
    advance until "Ổn định chỗ ngồi."
    pause 0.4
    assert eval (stage_visual == ('player', 'philosophy') and set(stage_cast) == {'player', 'minh', 'ngan', 'philosophy'})
    python:
        dialogue_geometry = polish_panel_geometry("say")
    assert eval (dialogue_geometry[1] == (1240, 204))
    screenshot "polish-lecture.png"
    advance until "Mình là Nghi."
    pause 0.4
    assert eval (stage_visual == ('player', 'philosophy', 'nghi') and len(stage_cast) == 5)
    screenshot "polish-introduction.png"
    advance until screen "choice"
    pause 0.4
    assert eval (stage_visual == ('player', 'ngan', 'nghi') and len(stage_cast) == 5 and not renpy.showing('cast_philosophy'))
    assert eval (polish_panel_geometry("choice") == dialogue_geometry and choice_dialogue() == ('NGÂN', 'Nghe người ta nói kìa.'))
    assert eval (renpy.get_displayable("choice", "choice_list").get_placement()[1:4:2] == (CHOICE_BOTTOM, 1.0))
    screenshot "polish-choice.png"
    assert eval (renpy.get_displayable("choice", "what").text == ['Nghe người ta nói kìa.'])
    python:
        shot_before_hint = stage_visual
    click "Hỏi Ngân (3/3)"
    pause 0.3
    assert screen "ngan_hint_message"
    assert eval (stage_visual == shot_before_hint and polish_panel_geometry("choice") == dialogue_geometry)
    screenshot "polish-hint.png"
    click "Đã hiểu"
    click "A. Ý bạn khá giống"
    advance until screen "choice"
    assert eval (stage_visual == ('player', 'nghi') and polish_panel_geometry("choice") == dialogue_geometry)
    click "Hỏi Ngân (2/3)"
    assert eval (stage_visual == ('player', 'nghi') and 'ngan' not in stage_cast and not renpy.showing('cast_ngan'))
    click "Đã hiểu"
    run Function(renpy.set_physical_size, (1280, 720))

testcase polish_focus_and_migration:
    run Jump("start")
    advance until screen "choice"
    run Function(set_stage, 'player', 'ngan', 'nghi', 'philosophy', visual=('player', 'ngan', 'nghi'))
    run Function(stage_speaker, 'ngan', 'begin')
    pause 0.4
    python:
        original_images = dict(stage_images)
        original_shot = stage_visual
    run Function(stage_speaker, 'nghi', 'begin')
    pause 0.3
    assert eval (stage_visual == original_shot and stage_images == original_images and stage_focus == 'nghi')
    assert eval (all(renpy.game.context().scene_lists.get_displayable_by_tag('master', 'cast_' + a).alpha >= 0.99 for a in stage_visual))
    assert eval (renpy.get_image_bounds('cast_nghi')[2] > renpy.get_image_bounds('cast_ngan')[2])
    run SetVariable("nghi_expression", "happy")
    run Function(refresh_stage)
    pause 0.3
    assert eval (stage_images['nghi'] == 'nghi happy')
    run Function(stage_speaker, 'ngan', 'begin')
    assert eval (stage_visual == original_shot)
    run Function(set_shot, 'player', 'nghi')
    pause 0.3
    assert eval ('ngan' in stage_cast and 'philosophy' in stage_cast and not renpy.showing('cast_ngan'))
    run Function(stage_speaker, None, 'begin')
    assert eval (stage_visual == ('player', 'nghi') and stage_focus is None)
    python:
        # Emulate a v3.0 crowded save; migration should remove stale standees.
        stage_visual = ()
        renpy.show('philosophy', tag='cast_philosophy')
    run Function(migrate_stage)
    pause 0.4
    assert eval (len(stage_visual) == 3 and len(stage_cast) == 4 and not renpy.showing('cast_philosophy'))

testcase polish_continue:
    python:
        persistent.chapter2_unlocked = True
    run Jump("chapter2_start")
    advance until screen "choice"
    click "Đi lẹ không trễ."
    advance until screen "choice"
    click "A. Ý bạn khá giống"
    advance until screen "choice"
    python:
        renpy.save('polish-continue')
    run MainMenu(confirm=False)
    pause 0.8
    assert screen "main_menu"
    click "Continue"
    pause 0.5
    assert screen "choice"
    assert eval (current_chapter == 2 and ch2_hint_context == 'library' and NghiAffinity == 2 and stage_visual == ('player', 'nghi'))

testcase polish_v3_save:
    # Real unmodified v3.0 fixture, copied into the isolated test savedir.
    if not eval (renpy.can_load('chapter2-v3-compatibility')):
        exit
    run Function(renpy.load, 'chapter2-v3-compatibility')
    pause 0.4
    assert screen "choice"
    assert eval (current_chapter == 2 and ch2_hint_context == 'library' and NghiAffinity == 2 and NghiComfort == 1 and NganHintsRemaining == 2 and stage_visual == ('player', 'nghi'))
    assert eval (polish_panel_geometry("choice")[1] == (1240, 204) and bool(choice_dialogue()[1]))
    click "A. Bạn đang đọc gì vậy?"
    advance until screen "choice"
    assert eval (NghiAffinity == 6 and NghiComfort == 4 and NganHintsRemaining == 2)

testcase polish_teacher_heights:
    run SetVariable("current_chapter", 2)
    run SetVariable("player_expression", "normal")
    # A narrated title holds neutral emphasis while the comparison is rendered.
    run Jump("CH2_09")
    pause 0.5
    # Compare equal focus states so normal speaker emphasis isn't mistaken for
    # an asset-size mismatch. Also measure the image before the stage transform.
    assert eval (all(renpy.render(renpy.display.image.ImageReference(a), 1280, 720, 0, 0).get_size()[1] == CHARACTER_HEIGHT for a in STAGE_ACTORS))
    run Function(set_stage, 'player', 'philosophy', 'nurse')
    pause 0.5
    assert eval (max(renpy.get_image_bounds('cast_' + a)[3] for a in stage_visual) - min(renpy.get_image_bounds('cast_' + a)[3] for a in stage_visual) < 1.0)
    screenshot "polish-teacher-nurse-heights.png"
    run Function(set_stage, 'player', 'pe')
    pause 0.5
    assert eval (abs(renpy.get_image_bounds('cast_player')[3] - renpy.get_image_bounds('cast_pe')[3]) < 1.0)
    screenshot "polish-pe-height.png"
