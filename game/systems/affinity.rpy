init python:
    def get_affinity(character):
        if character in ("linh", "ngan"):
            return getattr(renpy.store, "affinity_" + character)
        return extra_affinity.get(character, 0)

    def change_affinity(character, amount):
        if character in ("linh", "ngan"):
            name = "affinity_" + character
            setattr(renpy.store, name, get_affinity(character) + amount)
        else:
            extra_affinity[character] = get_affinity(character) + amount

    def affinity_at_least(character, threshold):
        return get_affinity(character) >= threshold

    # Existing Chapter 1 saves own affinity_* values. Trust is a safe alias
    # until a future chapter introduces distinct relationship dimensions.
    def get_trust(character):
        return get_affinity(character)

    def change_trust(character, amount):
        change_affinity(character, amount)

    def trust_at_least(character, threshold):
        return get_trust(character) >= threshold
