# Playthrough state belongs to the rollback-aware Ren'Py store.
default energy = 60
default energy_feedback = 0
default energy_feedback_serial = 0
default energy_visible = False
default overslept = False
default responsible_once = False
default class_late = False
default coffee_only = False
default breakfast_eaten = False
default still_no_regret = False
default fake_promise = False
default deadline_greed = False
default too_much_coffee = False
default dev_respect = 0
default lab_troll = False
default pe_pressure = 0
default pe_club_captured = False
default affinity_linh = 0
default affinity_ngan = 0
default extra_affinity = {}
default route_locked = False
default current_route = "NORMAL"
default player_is_on_campus = False
default infirmary_window_open = False
default campus_period = "day"
default chapter1_completed = False
default rebuild_playthrough = False
default current_chapter = 1
default player_expression = "normal"
default ngan_expression = "normal"
default persistent.chapter1_routes = set()
default persistent.last_played_chapter = 1

init python:
    def menu_chapter_index(value):
        return value if isinstance(value, int) and 1 <= value <= 5 else 1

    def enter_chapter(number):
        global current_chapter
        if menu_chapter_index(number) != number:
            raise ValueError("Chapter must be from 1 to 5.")
        current_chapter = number
        persistent.last_played_chapter = number
        renpy.save_persistent()

    def reset_chapter1_state():
        values = dict(energy=60, energy_feedback=0, energy_feedback_serial=0,
                      energy_visible=False, overslept=False, responsible_once=False,
                      class_late=False, coffee_only=False, breakfast_eaten=False,
                      still_no_regret=False, fake_promise=False, deadline_greed=False,
                      too_much_coffee=False, dev_respect=0, lab_troll=False,
                      pe_pressure=0, pe_club_captured=False, affinity_linh=0,
                      affinity_ngan=0, extra_affinity={}, route_locked=False,
                      current_route="NORMAL", player_is_on_campus=False,
                      infirmary_window_open=False,
                      campus_period="day", chapter1_completed=False,
                      rebuild_playthrough=True, current_chapter=1,
                      player_expression="normal", ngan_expression="normal")
        for name, value in values.items():
            setattr(renpy.store, name, value)
        renpy.store._history_list = []
        set_stage()
