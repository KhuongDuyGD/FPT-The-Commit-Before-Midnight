# Use existing artwork; unavailable assets fall back without network downloads.
init -30 python:
    def background_asset(filename, fallback=None, color="#162235"):
        path = "images/backgrounds/" + filename
        if not renpy.loadable(path) and fallback:
            path = "images/backgrounds/" + fallback
        if not renpy.loadable(path):
            return Solid(color)
        return Transform(path, xysize=(1920, 1080), fit="cover")

    def gallery_asset(filename):
        path = "images/GalleryImage/" + filename
        if not renpy.loadable(path):
            return Solid("#17233a")
        return Transform(path, xysize=(1920, 1080), fit="cover")

image dream_place = background_asset("Outside/DreamPlace.png")
image homeward_sunset = Solid("#40394c")
image homeward_dusk = Solid("#17233a")

image cg_pe_intro = gallery_asset("FirstTimeMeetPhysicalTeacher.png")
image cg_nurse_intro = gallery_asset("FirstTimeMeetNurse.png")
image cg_good_sleep = gallery_asset("GoodRouteChapter1.png")
image cg_walking_corpse = gallery_asset("BadRouteChapter1.png")

image menu_chapter_1 = background_asset("MainMenu/MainMenu1.png")
image menu_chapter_2 = background_asset("MainMenu/MainMenu2.png")
image menu_chapter_3 = background_asset("MainMenu/MainMenu3.png")
image menu_chapter_4 = background_asset("MainMenu/MainMenu4.png")
image menu_chapter_5 = background_asset("MainMenu/MainMenu5.png")
image game_logo = Transform("images/backgrounds/GameIcon_Logo/LogoGame.png",
                            xysize=(650, 217), fit="contain")
