init python:
    # Missing recordings are intentionally silent; never substitute unrelated cues.
    CH1_SOUNDS = {"alarm": "audio/alarm.wav", "notification": "audio/notification.wav",
                  "birds": "audio/birds.ogg", "door": "audio/door.ogg",
                  "whistle": "audio/whistle.ogg", "pat": "audio/shoulder_pat.ogg",
                  "bag": "audio/bag_drop.ogg"}
    CH1_AMBIENCE = {"room": "audio/room.ogg", "campus": "audio/campus.ogg",
                    "classroom": "audio/classroom.ogg", "canteen": "audio/canteen.ogg",
                    "sports": "audio/sports.ogg", "infirmary": "audio/infirmary.ogg"}
    renpy.music.register_channel("ambience", mixer="sfx", loop=True)

    def play_scene_sound(cue):
        path = CH1_SOUNDS[cue]
        if renpy.loadable(path):
            renpy.sound.play(path, loop=False)

    def scene_ambience(location=None):
        renpy.sound.stop()
        renpy.music.stop(channel="ambience", fadeout=0.25)
        path = CH1_AMBIENCE.get(location)
        if path and renpy.loadable(path):
            renpy.music.play(path, channel="ambience", fadein=0.35)

