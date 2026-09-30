# stage_cast is story presence; stage_visual is the current camera composition.
# Both, including expression transitions, restore with saves and rollback.
default stage_cast = ()
default stage_visual = ()
default stage_focus = None
default stage_images = {}
default stage_entrance = "fade"

transform stage_pose(position=0.5, scale=1.0, tint="#ffffff", entrance="fade"):
    xanchor 0.5
    yanchor 1.0
    ypos 1.0
    # Set position immediately: a new sprite must not travel from xpos=0.
    xpos position
    on show:
        alpha 0.0
        matrixcolor TintMatrix(tint)
        zoom (scale * 0.97 if entrance == "scale" else scale)
        yoffset (20 if entrance == "rise" else 0)
        xoffset (-35 if entrance == "slide" else 0)
        ease 0.25 alpha 1.0 zoom scale yoffset 0 xoffset 0
    on replace:
        ease 0.2 alpha 1.0 zoom scale matrixcolor TintMatrix(tint) yoffset 0 xoffset 0
    on hide:
        ease 0.25 alpha 0.0

transform stage_expression(old_image, new_image):
    old_image
    new_image with Dissolve(0.15, alpha=True)

init -20 python:
    from functools import partial

    STAGE_ACTORS = ("player", "minh", "linh", "thaydev", "ngan", "nurse", "pe", "necrass")
    STAGE_MAX_VISIBLE = 3
    MC_EXPRESSIONS = ("normal", "sleepy", "annoyed", "smug", "surprised", "thinking",
                      "deadpan", "confused", "nervous", "veryhappy", "panic", "goodmood",
                      "determined", "serious", "embarrassed", "exhaust", "sad", "cry",
                      "empathy", "angry")

    def stage_image(actor):
        if actor == "player":
            expression = player_expression if player_expression in MC_EXPRESSIONS else "normal"
            return "player " + expression
        expression = ngan_expression if actor == "ngan" else "normal"
        return actor if expression == "normal" else actor + " " + expression

    def set_player_expression(expression):
        global player_expression
        if expression not in MC_EXPRESSIONS:
            raise ValueError("Unknown MC expression: " + str(expression))
        if player_expression != expression:
            player_expression = expression
            if "player" in stage_visual:
                refresh_stage()

    def set_energy_expression(context="ordinary"):
        # Evaluate at checkpoints; explicit scene direction takes priority.
        if energy <= 15 or (energy <= 25 and context == "fatigue"):
            set_player_expression("exhaust")
        elif energy <= 45:
            set_player_expression("sleepy")
        else:
            set_player_expression("normal")

    def refresh_stage():
        count = len(stage_visual)
        for index, actor in enumerate(stage_visual):
            # Leave room for the PE teacher's broad, height-matched artwork.
            position = 0.5 if count == 1 else 0.22 + 0.52 * index / (count - 1)
            focused = actor == stage_focus
            image = stage_image(actor)
            present = renpy.showing("cast_" + actor)
            previous = stage_images.get(actor)
            if present and previous is not None and previous != image:
                child = stage_expression(previous, image)
            else:
                # Fresh image references avoid retaining a completed ATL child
                # transition's timing/state across focus updates and saved games.
                child = renpy.display.image.ImageReference(image)
            stage_images[actor] = image
            renpy.show(image, tag="cast_" + actor, what=child,
                       at_list=[stage_pose(position, 1.0 if focused else 0.96,
                                           "#ffffff" if focused or stage_focus is None else "#b8b8c4",
                                           stage_entrance)],
                       zorder=20 if focused else 5 + index)

    def set_shot(*actors, entrance="fade"):
        """Change visual focus without making anyone leave the story location."""
        global stage_visual, stage_focus, stage_entrance
        actors = tuple(dict.fromkeys(actors))
        if len(actors) > STAGE_MAX_VISIBLE or any(a not in stage_cast for a in actors):
            raise ValueError("A shot needs at most three story-present characters.")
        if entrance not in ("fade", "scale", "rise", "slide"):
            raise ValueError("Unknown stage entrance: " + entrance)
        for actor in STAGE_ACTORS:
            if actor not in actors:
                renpy.hide("cast_" + actor)
                stage_images.pop(actor, None)
        stage_visual, stage_entrance = actors, entrance
        if stage_focus not in actors:
            stage_focus = None
        refresh_stage()

    def set_stage(*actors, visual=None, entrance="fade"):
        """Call for a scene change or an actual entrance/exit."""
        global stage_cast, stage_focus
        if any(a not in STAGE_ACTORS for a in actors):
            raise ValueError("Unknown stage actor.")
        stage_cast = tuple(dict.fromkeys(actors))
        stage_focus = None
        set_shot(*(stage_cast[:STAGE_MAX_VISIBLE] if visual is None else visual),
                 entrance=entrance)

    def stage_speaker(actor, event, **kwargs):
        if event == "begin":
            global stage_focus
            # A brief cutaway for an offscreen participant. Existing active-shot
            # speakers only change emphasis; remote messages never add a sprite.
            if actor in stage_cast and actor not in stage_visual:
                partners = [a for a in stage_visual if a != actor]
                if "player" in partners:
                    partners.remove("player")
                    partners.insert(0, "player")
                set_shot(*(partners[:STAGE_MAX_VISIBLE - 1] + [actor]))
            new_focus = actor if actor in stage_visual else None
            if new_focus != stage_focus:
                stage_focus = new_focus
                refresh_stage()

    def migrate_stage():
        # Restore the saved composition and reconcile scene tags after load.
        if player_expression == "exhausted":
            set_player_expression("exhaust")
        if not stage_visual or any(a not in stage_cast for a in stage_visual):
            set_shot(*stage_cast[:STAGE_MAX_VISIBLE])
        else:
            set_shot(*stage_visual[:STAGE_MAX_VISIBLE])

    def active_speaker_image(who):
        actor = {"PLAYER": "player", "MC": "player", "MINH": "minh", "LINH": "linh",
                 "THẦY DEV": "thaydev", "NGÂN": "ngan"}.get(who)
        return stage_image(actor) if actor else None
