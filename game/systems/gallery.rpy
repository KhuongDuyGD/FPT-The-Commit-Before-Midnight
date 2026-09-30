# CG access is earned at the moment the corresponding story image is shown.
default persistent.chapter1_cg_seen = set()

init python:
    CHAPTER1_CG = {
        "pe_intro": ("images/GalleryImage/FirstTimeMeetPhysicalTeacher.png", "The Encounter"),
        "nurse_intro": ("images/GalleryImage/FirstTimeMeetNurse.png", "First Aid"),
        "good_sleep": ("images/GalleryImage/GoodRouteChapter1.png", "A Real Rest"),
        "walking_corpse": ("images/GalleryImage/BadRouteChapter1.png", "One Percent Left"),
    }

    def chapter1_cg_seen(cg_id):
        return cg_id in (persistent.chapter1_cg_seen or set())

    def unlock_chapter1_cg(cg_id):
        if cg_id not in CHAPTER1_CG:
            raise ValueError("Unknown Chapter 1 CG: " + str(cg_id))
        if not chapter1_cg_seen(cg_id):
            persistent.chapter1_cg_seen.add(cg_id)
            renpy.save_persistent()

    def chapter1_cg_thumb(cg_id):
        path = CHAPTER1_CG[cg_id][0]
        if renpy.loadable(path):
            return Transform(path, xysize=(752, 226), fit="cover")
        return Solid("#19283d", xsize=752, ysize=226)

    def chapter1_cg_full(cg_id):
        path = CHAPTER1_CG[cg_id][0]
        if renpy.loadable(path):
            return Transform(path, xysize=(1920, 1080), fit="contain")
        return Solid("#19283d")
