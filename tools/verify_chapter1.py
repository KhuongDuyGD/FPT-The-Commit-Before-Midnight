"""Audit the current Chapter 1 dialogue baseline, allowed balance edits and assets.

The older Markdown brief was reformatted after the first rebuild. Its recorded
manifest represents the shipped Chapter 1 wording, which this polish must keep.
"""
from collections import Counter
from itertools import product
from pathlib import Path
import ast
import json
import re
import textwrap

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "FPT_The_Commit_Before_Midnight_MASTER_REBUILD_PROMPT.md"


def verify():
    manifest = json.loads((ROOT / "tests/rebuild/source_manifest.json").read_text(encoding="utf-8"))["content"]
    chapter = (ROOT / "game/chapters/chapter_01.rpy").read_text(encoding="utf-8")
    expected_speech = [(item["character"], item["text"]) for item in manifest if item["kind"] != "choice"]
    expected_choices = [item["text"] for item in manifest if item["kind"] == "choice"]
    actual_speech, actual_choices = [], []
    for line in chapter.splitlines():
        say = re.fullmatch(r'\s+(\w+) ("(?:[^"\\]|\\.)*")', line)
        if say:
            spoken = ast.literal_eval(say[2]).replace("%%", "%").replace("[[", "[").replace("{{", "{")
            if (say[1], spoken) != ("system_msg", "SPECIAL ROUTE UNLOCKED: INFIRMARY"):
                actual_speech.append((say[1], spoken))
        choice = re.fullmatch(r'\s+("(?:[^"\\]|\\.)*"):', line)
        if choice:
            actual_choices.append(ast.literal_eval(choice[1]))
    assert actual_speech == expected_speech, "Chapter 1 dialogue or system text changed"
    assert actual_choices == expected_choices, "Chapter 1 choice text/order changed"

    # Only three Energy values may differ from the recorded screenplay.
    original = SOURCE.read_text(encoding="utf-8").split("\n# FPT: The Commit Before Midnight\n", 1)[1]
    original = original.split("\n# 16. ROUTE SUMMARY", 1)[0]
    energy_expected = Counter(int(x) for x in re.findall(r"\[ENERGY ([+-]?\d+)\]", original))
    for before, after in ((-5, -10), (-10, -15), (-8, -10)):
        assert energy_expected[before] > 0
        energy_expected[before] -= 1
        energy_expected[after] += 1
    energy_actual = Counter(int(x) for x in re.findall(r"change_energy\(([+-]?\d+)\)", chapter))
    assert energy_actual == energy_expected, "An unauthorized Energy delta was changed"
    assert re.search(r'"Bỏ luôn, chạy đi học\.":\s+.*?change_energy\(-10\)', chapter, re.S)
    assert re.search(r'"Chạy nước rút ra ngoài\.":\s+.*?change_energy\(-15\)', chapter, re.S)
    assert re.search(r'"Bỏ bữa để làm task\.":\s+.*?change_energy\(-10\)', chapter, re.S)

    affinities = {"LINH": "linh", "NGÂN": "ngan"}
    trust_expected = Counter((affinities[name], int(amount)) for name, amount in
                             re.findall(r"\[AFFINITY: (LINH|NGÂN) ([+-]\d+)\]", original))
    trust_actual = Counter((name, int(amount)) for name, amount in
                           re.findall(r'change_trust\("(\w+)", ([+-]\d+)\)', chapter))
    assert trust_actual == trust_expected, "A hidden relationship delta changed"

    flag_expected = Counter()
    for name, enabled, amount in re.findall(r"\[FLAG: ([A-Z_]+) (?:= (TRUE)|([+]\d+))\]", original):
        flag_expected[(name.lower(), "True" if enabled else str(int(amount)))] += 1
    for name, enabled, amount in re.findall(r"^\[FLAG\] `([A-Z_]+) (?:= (TRUE)|([+]\d+))`", original, re.M):
        flag_expected[(name.lower(), "True" if enabled else str(int(amount)))] += 1
    names = {name for name, _ in flag_expected}
    flag_actual = Counter((name, "True" if enabled else str(int(amount))) for name, enabled, amount in
                          re.findall(r"^\s*\$ (\w+) (?:= (True)|\+= ([+]\d+))$", chapter, re.M)
                          if name in names)
    assert flag_actual == flag_expected, "A source flag changed"

    scripts = {p: p.read_text(encoding="utf-8") for p in (ROOT / "game").rglob("*.rpy")}
    runtime_text = "\n".join(scripts.values())
    labels = re.findall(r"^label ([\w]+):", runtime_text, re.M)
    assert len(labels) == len(set(labels)), "Duplicate labels"
    for target in re.findall(r"^\s*(?:jump|call) (\w+)$", runtime_text, re.M):
        assert target in labels, "Missing label: " + target
    assert not re.search(r"label (?:CH2_|chapter2|scene_\d|good_ending|bad_ending)", runtime_text)
    assert "chapter2_start" not in runtime_text and "chapter2_is_unlocked" not in runtime_text
    assert "GameMainMenu.png" not in runtime_text and "dream_void" not in runtime_text
    assert not list((ROOT / "game").glob("chapter2*.rpyc"))
    assert not (ROOT / "game/endings.rpyc").exists()

    # Same actor image tag, all 20 expressions; old misspelling is the real filename.
    actors = scripts[ROOT / "game/characters.rpy"]
    expressions = re.findall(r'^image player (\w+) = character_sprite\("Main/([^"/]+\.png)"\)', actors, re.M)
    assert len(expressions) == 21 and len({name for name, _ in expressions}) == 21
    required_files = [ROOT / "game/images/characters/Main" / filename for _, filename in expressions]
    required_files += [ROOT / "game/images/backgrounds" / name for name in (
        "Main_Home/KTXDay.png", "Main_Home/KTXNight.png", "School_Map/FPTUGateDay.png",
        "School_Map/FPTUGateAfternoon.png", "School_Map/HallwayFPTUDay.png",
        "School_Map/ComputerLabDay.png", "School_Map/CanteenFPTUDay.png",
        "School_Map/ClassroomAfternoon.png", "School_Map/SportsGroundAfternoon.png",
        "School_Map/MedicalRoomDay.png", "School_Map/MedicalRoomAfternoon.png",
        "Outside/DreamPlace.png", "GameIcon_Logo/LogoGame.png", "GameIcon_Logo/GameIcon.png",
        *(f"MainMenu/MainMenu{i}.png" for i in range(1, 6)),
    )]
    required_files += [ROOT / "game/images/GalleryImage" / name for name in (
        "FirstTimeMeetPhysicalTeacher.png", "FirstTimeMeetNurse.png",
        "GoodRouteChapter1.png", "BadRouteChapter1.png")]
    missing = [str(p.relative_to(ROOT)) for p in required_files if not p.is_file()]
    assert not missing, "Missing actual art: " + repr(missing)
    assert chapter.count("scene dream_place") == 3
    cg_pairs = (("cg_pe_intro", "pe_intro"), ("cg_nurse_intro", "nurse_intro"),
                ("cg_good_sleep", "good_sleep"), ("cg_walking_corpse", "walking_corpse"))
    for image, key in cg_pairs:
        assert re.search(r"scene " + image + r"\b[\s\S]{0,120}\$ unlock_chapter1_cg\(\"" + key + r"\"\)", chapter)
    assert chapter.count("call ch1_campus_checkpoint") == 3
    assert "call ch1_campus_checkpoint" not in chapter.split("label ch1_after_class:", 1)[1]

    # Run the actual pure resolver, including the post-window 10-Energy case.
    route_source = scripts[ROOT / "game/systems/route.rpy"].split("init python:\n", 1)[1]
    route_ast = ast.parse(textwrap.dedent(route_source))
    route_ast.body = [node for node in route_ast.body if isinstance(node, ast.Assign) or
                      isinstance(node, ast.FunctionDef) and node.name == "resolve_day_route"]
    scope = {}
    exec(compile(route_ast, "route.rpy", "exec"), scope)
    resolve = scope["resolve_day_route"]
    assert resolve(12, False, True) == "INFIRMARY"
    assert resolve(10, False, False, True) == "WALKING_CORPSE"
    assert resolve(20, False, False, True) == "WALKING_CORPSE"
    assert resolve(10, True, False, True) == "BLACK_ALLOY_CLUB"
    assert resolve(100, True, False, True, True, "INFIRMARY") == "INFIRMARY"
    assert resolve(31, False, False, True) == "HOME_SAFE"

    def change(value, amount):
        return max(0, min(100, value + amount))

    outcomes = Counter()
    min_break, min_after_class = 100, 100
    for wake, food, minh, linh, lab, ngan, lunch, pe in product(
        ("awake", "sprint", "late"), (15, 8, -10), (3, 0, 0), (0, 7, 0),
        (-8, -3, -2, 4), (0, 0, 5, -3), (20, 10, -10, 6), range(4)):
        value = change(60, 0 if wake == "awake" else 5)
        value = change(value, food)
        value = change(value, -15 if wake == "sprint" else -2 if wake == "late" else 0)
        for amount in (minh, linh, lab, ngan):
            value = change(value, amount)
        min_break = min(min_break, value)
        if value <= 15:
            outcomes["INFIRMARY"] += 1
            continue
        value = change(value, lunch)
        if value <= 15:
            outcomes["INFIRMARY"] += 1
            continue
        value = change(value, -10)
        min_after_class = min(min_after_class, value)
        if value <= 15:
            outcomes["INFIRMARY"] += 1
            continue
        if pe == 3:
            for signed in (True, False):
                final = value if signed else change(value, -5)
                captured = signed or final <= 20
                outcomes[resolve(final, captured, False, True)] += 1
        else:
            outcomes[resolve(value, pe == 2, False, True)] += 1
    assert change(change(change(change(change(change(60, 5), -10), -15), -8), -10), -10) == 12
    assert outcomes["INFIRMARY"] > 0
    assert outcomes["WALKING_CORPSE"] > 0

    result = dict(dialogue=sum(i["kind"] == "say" for i in manifest), choices=len(expected_choices),
                  energy_deltas=sum(energy_actual.values()), trust_deltas=sum(trust_actual.values()),
                  flag_changes=sum(flag_actual.values()), runtime_labels=len(labels),
                  chapter2_in_runtime=False, legacy_chapter1_in_runtime=False,
                  enumerated_combinations=sum(outcomes.values()), outcomes=dict(outcomes),
                  minimum_break_energy=min_break, minimum_after_class_energy=min_after_class,
                  missing_artwork=missing, infirmary_naturally_reachable=True)
    (ROOT / "tests/rebuild/static-validation.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    verify()
