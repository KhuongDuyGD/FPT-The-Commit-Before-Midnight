# Keep the existing save directory and persistent unlocks, but exclude saves
# whose statement paths refer to the deprecated Chapter 1.
init python:
    def rebuild_save_metadata(data):
        data["rebuild_schema"] = 1
        data["chapter"] = current_chapter
        data["route"] = current_route

    config.save_json_callbacks.append(rebuild_save_metadata)

    def compatible_save(slot):
        data = renpy.slot_json(slot)
        return bool(data and data.get("rebuild_schema") == 1 and data.get("chapter") == 1)

    def latest_compatible_save():
        slots = renpy.list_slots(r"^(\d+|auto|quick)-\d+$")
        valid = [(renpy.slot_json(slot).get("_ctime", 0), slot)
                 for slot in slots if compatible_save(slot)]
        return max(valid)[1] if valid else None
