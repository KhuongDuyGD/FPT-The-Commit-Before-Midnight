init python:
    ROUTE_PRIORITY = {"NORMAL": 0, "HOME_SAFE": 1, "WALKING_CORPSE": 2,
                      "BLACK_ALLOY_CLUB": 3, "INFIRMARY": 4}

    def resolve_day_route(value, captured=False, infirmary_window=True, end_of_day=False,
                          locked=False, previous="NORMAL"):
        if locked:
            return previous
        if value <= 15 and infirmary_window:
            result = "INFIRMARY"
        elif captured:
            result = "BLACK_ALLOY_CLUB"
        elif end_of_day:
            result = "WALKING_CORPSE" if value <= 30 else "HOME_SAFE"
        else:
            result = "NORMAL"
        return result if ROUTE_PRIORITY[result] > ROUTE_PRIORITY[previous] else previous

    def update_day_route(end_of_day=False):
        global current_route, route_locked, infirmary_window_open
        current_route = resolve_day_route(energy, pe_club_captured, infirmary_window_open,
                                          end_of_day, route_locked, current_route)
        if current_route == "INFIRMARY":
            route_locked = True
            infirmary_window_open = False
        return current_route

    def finish_chapter1():
        global chapter1_completed, energy_visible, player_is_on_campus
        chapter1_completed, energy_visible, player_is_on_campus = True, False, False
        persistent.chapter1_routes.add(current_route)
        renpy.save_persistent()
