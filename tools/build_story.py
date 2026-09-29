"""Convert the supplied v2 screenplay into editable Ren'Py scene files.

Run this only when VisualNovelContent.txt changes. The generated .rpy files are
committed game source, so Ren'Py does not need this tool at runtime. Scene and
choice boundaries below refer to the supplied v2 screenplay.
"""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "VisualNovelContent.txt").read_text(encoding="utf-8-sig").splitlines()
GAME = ROOT / "game"

# The import ranges below are tied to this screenplay revision. Fail clearly
# if someone edits the document before rerunning the importer.
for line_number, heading in {
    183: "# SCENE 00 — 06:29 AM",
    387: "# SCENE 01 — 07:28 AM",
    527: "# SCENE 02 — 07:30 AM",
    790: "# SCENE 03 — 09:30 AM",
    1022: "# SCENE 04 — 11:00 AM",
    1263: "# SCENE 05 — 12:00",
    1448: "# SCENE 06 — 13:30",
    1657: "# SCENE 07 — 15:45",
    1829: "# SCENE 08 — 16:55",
    1996: "# GOOD ENDING ROUTE",
    2272: "# BAD ENDING ROUTE",
    2821: "# POST-CREDIT",
}.items():
    if len(SOURCE) < line_number or SOURCE[line_number - 1] != heading:
        raise SystemExit("Screenplay structure changed; review tools/build_story.py ranges before regenerating.")

SPEAKERS = {
    "PLAYER": "p",
    "MINH": "m",
    "LINH": "l",
    "THẦY DEV": "dev",
    "CÔ LMS": "lms",
    "CHÚ BẢO VỆ": "guard",
    "NARRATOR": "n",
    "CLASS": "crowd",
    "Sinh viên phía sau": "student",
    "FRIEND": "friend",
    "VOICE CHAT": "voice_chat",
}
SOUNDS = {
    "ALARM": "sfx_alarm",
    "NOTIFICATION": "sfx_notification",
    "HARD CUT": "sfx_windows_error",
}


def quote(value):
    return json.dumps(value, ensure_ascii=False)


def clean(value):
    value = value.strip()
    if value.startswith("> "):
        value = value[2:]
    value = value.replace("**", "").replace("`", "")
    if value.startswith("*") and value.endswith("*"):
        value = value[1:-1]
    if len(value) >= 2 and value[0] in "“\"" and value[-1] in "”\"":
        value = value[1:-1]
    # Ren'Py's old-style text interpolation treats a lone % as formatting.
    return value.strip().replace("%", "%%")


def prose(first, last, level=4):
    """Emit screenplay lines from an inclusive 1-based range as Ren'Py."""
    out = []
    prefix = " " * level
    speaker = None
    in_fence = False
    for raw in SOURCE[first - 1:last]:
        line = raw.strip()
        if not line or line == "---":
            continue
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue  # Choice state updates are written beside menu entries.
        if line.startswith("# "):
            continue
        if line.startswith("### Background:"):
            continue
        if line.startswith("## ") or line.startswith("### "):
            heading = line.lstrip("# ").strip()
            if heading.startswith("[") or heading.startswith("SCENE "):
                continue
            if heading in ("CANTEEN", "BREAK", "COMPUTER LAB", "FINAL CLASS", "FINAL FIVE MINUTES", "MORNING CLASS", "GROUP PROJECT"):
                continue
            if heading == "DEADLINE — TODAY 23:59":
                out.append(prefix + "with flash")
                out.append(prefix + "play sound sfx_notification")
            if heading == "02:41 AM":
                out.append(prefix + "scene bedroom_gaming with fade")
                out.append(prefix + '$ player_expression = "happy"')
            out.append(prefix + "centered " + quote(heading))
            continue
        if line.startswith("SFX: "):
            cue = SOUNDS.get(line[5:].strip())
            if cue:
                out.append(prefix + "play sound " + cue)
            continue
        if line == "FLASHBACK." or line == "CUT.":
            continue
        if line == "CUT TO PRESENT.":
            out.append(prefix + "scene bedroom_morning with fade")
            out.append(prefix + '$ player_expression = "exhausted"')
            continue
        if line in ("Pause.", "Silence."):
            out.append(prefix + "pause 0.3")
            continue
        if line == "UI:":
            continue
        match = re.fullmatch(r"([^:]+):", line)
        if match:
            key = match.group(1).split(",")[0].strip()
            if key in SPEAKERS:
                speaker = SPEAKERS[key]
                continue
        text = clean(line)
        if not text:
            continue
        out.append(prefix + (speaker or "n") + " " + quote(text))
        speaker = None
    return out


def add(lines, *items):
    for item in items:
        if isinstance(item, str):
            lines.append(item)
        else:
            lines.extend(item)


script = [
    "# Generated from VisualNovelContent.txt v2.0. Dialogue remains in source order.",
    "# Change scene art, stats, and route logic here; rerun tools/build_story.py only",
    "# when replacing the screenplay with a new version.",
    "",
    "label start:",
    "    # Explicit resets make Start Game and New Game+ share the same baseline.",
    "    $ energy = 100",
    "    $ sanity = 100",
    "    $ academic_progress = 0",
    "    $ escape_point = 0",
    "    $ pending_tasks = 0",
    "    $ attendance_done = False",
    "    $ quiz_done = False",
    "    $ group_task_done = False",
    "    $ assignment_uploaded = False",
    "    $ escaped_school = False",
    "    $ final_choice = None",
    '    $ player_expression = "exhausted"',
    "    show screen stats_hud",
    "    if new_game_plus:",
    '        centered "NEW GAME+\\nDifficulty Unlocked: SENIOR YEAR."',
    "        $ new_game_plus = False",
    "    jump scene_00_alarm",
    "",
    "label scene_00_alarm:",
    "    scene bedroom_morning with fade",
]
add(script, prose(183, 274),
    "    play sound sfx_boss",
    '    call screen boss_title("THE ALARM CLOCK", "Threat: ★★★★★  •  Special Ability: Snooze")',
    "    menu:",
    '        "Năm phút nữa thôi.":',
    prose(288, 344, 12),
    "            $ energy -= 20",
    "            $ escape_point -= 1",
    '        "Dậy. Ngay.":',
    prose(345, 386, 12),
    "            $ escape_point += 1",
    "    jump scene_01_gate",
    "",
    "label scene_01_gate:",
    "    scene school_gate_morning with fade",
    '    $ player_expression = "normal"',
    prose(387, 526),
    "    play sound sfx_bell",
    "    $ attendance_done = True",
    "    jump scene_02_quiz",
    "",
    "label scene_02_quiz:",
    "    scene classroom with dissolve",
    prose(527, 628),
    "    with flash",
    "    menu:",
    '        "Đọc đề trước khi hoảng.":',
    prose(631, 728, 12),
    "            $ sanity -= 5",
    "            $ academic_progress += 2",
    "            $ quiz_done = True",
    '        "Panic trước, đọc đề sau.":',
    prose(729, 789, 12),
    "            $ sanity -= 20",
    "            $ pending_tasks += 1",
    "    jump scene_03_break",
    "",
    "label scene_03_break:",
    "    scene hallway with fade",
    prose(790, 881),
    "    play sound sfx_boss",
    '    call screen boss_title("QUICK MEETING", "Threat: ★★★★★★  •  Passive: Nhân tiện…")',
    "    menu:",
    '        "Đi ăn trước.":',
    prose(895, 934, 12),
    "            $ energy += 20",
    "            $ sanity += 10",
    "            $ escape_point += 1",
    '        "Join meeting.":',
    prose(935, 1021, 12),
    "            $ energy -= 25",
    "            $ sanity -= 15",
    "            $ academic_progress += 1",
    "            $ pending_tasks = max(0, pending_tasks - 1)",
    "    jump scene_04_project",
    "",
    "label scene_04_project:",
    "    scene hallway with dissolve",
    prose(1022, 1133),
    "    menu:",
    '        "Fix luôn.":',
    prose(1136, 1222, 12),
    "            $ energy -= 15",
    "            $ academic_progress += 2",
    "            $ group_task_done = True",
    "            $ escape_point += 1",
    '        "Để chiều.":',
    prose(1223, 1262, 12),
    "            $ pending_tasks += 2",
    "    jump scene_05_lunch",
    "",
    "label scene_05_lunch:",
    "    scene canteen with fade",
    prose(1263, 1356),
    "    menu:",
    '        "Ăn như một con người bình thường.":',
    prose(1359, 1389, 12),
    "            $ energy += 30",
    "            $ sanity += 10",
    '        "Vừa ăn vừa code.":',
    prose(1390, 1447, 12),
    "            $ academic_progress += 1",
    "            $ energy += 10",
    "            $ sanity -= 10",
    "    jump scene_06_windows",
    "",
    "label scene_06_windows:",
    "    scene computer_lab with fade",
    prose(1448, 1467),
    '    $ player_expression = "angry"',
    prose(1468, 1507),
    "    play sound sfx_windows_error",
    "    with hpunch",
    "    play sound sfx_boss",
    '    call screen boss_title("WINDOWS UPDATE", "Defense: 9999  •  Weakness: Laptop cá nhân")',
    prose(1519, 1572),
    "    menu:",
    '        "Rút laptop cá nhân.":',
    prose(1575, 1608, 12),
    "            $ energy -= 5",
    "            $ academic_progress += 2",
    "            $ escape_point += 1",
    '        "Chờ.":',
    prose(1609, 1656, 12),
    "            $ sanity -= 20",
    "    jump scene_07_final_class",
    "",
    "label scene_07_final_class:",
    "    scene classroom_afternoon with fade",
    '    $ player_expression = "normal"',
    prose(1657, 1758),
    '    $ player_expression = "cry"',
    prose(1759, 1828),
    "    $ pending_tasks += 1",
    "    jump scene_08_final_choice",
    "",
    "label scene_08_final_choice:",
    "    scene classroom_afternoon with dissolve",
    '    $ player_expression = "normal"',
    prose(1829, 1934),
    "    menu:",
    '        "Về.":',
    "            $ final_choice = 'leave'",
    prose(1937, 1995, 12),
    "            $ escape_point += 2",
    "            if can_escape_school():",
    "                $ escaped_school = True",
    "                jump good_ending",
    "            else:",
    '                n "Deadline và những việc chưa xong vẫn giữ PLAYER lại trường."',
    "                jump bad_ending",
    '        "Ở lại thêm chút.":',
    "            $ final_choice = 'stay'",
    prose(2234, 2271, 12),
    "            jump bad_ending",
    "",
    "label new_game_plus:",
    "    $ new_game_plus = True",
    "    jump start",
)

endings = [
    "# Version 2.0 ending routes. Gallery flags persist after the title card.",
    "",
    "label good_ending:",
    "    scene school_gate_afternoon with fade",
    '    $ player_expression = "happy"',
]
add(endings, prose(1998, 2089),
    "    scene bedroom_gaming with fade",
    prose(2092, 2211),
    "    hide screen stats_hud",
    "    play sound sfx_success",
    "    $ persistent.good_ending_unlocked = True",
    "    $ renpy.save_persistent()",
    '    call screen ending_card("GOOD ENDING", "ESCAPE SUCCESSFUL", "Student Status: ALIVE\\nEnergy: Enough for one ranked match\\nSanity: Functioning within acceptable parameters\\nAssignments: Technically under control\\nTomorrow: Future Me\'s problem\\n\\nAchievement: LOG OUT SUCCESSFULLY")',
    "    call screen post_ending_actions",
    "    return",
    "",
    "label bad_ending:",
    "    scene classroom_afternoon with fade",
    prose(2274, 2325),
    "    $ group_task_done = True",
    "    scene classroom_evening with fade",
    prose(2326, 2369),
    "    scene computer_lab with fade",
    '    $ player_expression = "angry"',
    prose(2370, 2455),
    "    play sound sfx_windows_error",
    prose(2456, 2517),
    "    $ assignment_uploaded = True",
    "    $ pending_tasks = max(0, pending_tasks - 1)",
    "    scene classroom_evening with fade",
    "    $ energy = min(energy, 12)",
    "    $ sanity = min(sanity, 4)",
    '    $ player_expression = "exhausted"',
    prose(2518, 2578),
    prose(2579, 2684),
    "    $ energy = 0",
    "    scene school_gate_night with fade",
    prose(2685, 2794),
    "    hide screen stats_hud",
    "    play sound sfx_bad",
    "    $ persistent.bad_ending_unlocked = True",
    "    $ renpy.save_persistent()",
    '    call screen ending_card("BAD ENDING", "FPT HAS CONSUMED YOU", "Student Status: Technically Alive\\nEnergy: 0%%\\nSanity: SEGMENTATION FAULT\\nPhysical Condition: Dried student\\nAssignment: SUBMITTED\\nPresentation: UPDATED\\nGroup Project: Somehow still has one bug\\nTomorrow\'s Meeting: 07:00\\n\\nAchievement: JUST ONE MORE TASK")',
    "    scene bedroom_morning with fade",
    "    play sound sfx_alarm",
    prose(2821, 2842),
    '    centered "NEW GAME+\\nDIFFICULTY UNLOCKED\\nSENIOR YEAR"',
    '    n "Good luck."',
    "    call screen post_ending_actions",
    "    return",
)

def integrate_chapters(lines):
    """Keep Ch1 dialogue verbatim while annotating physical entrances/exits."""
    result, label = [], ""
    casts = {
        "scene_00_alarm": ('player',), "scene_01_gate": ('player',),
        "scene_02_quiz": ('player', 'minh', 'thaydev'),
        "scene_03_break": ('player', 'minh'),
        "scene_04_project": ('player', 'minh', 'linh'),
        "scene_05_lunch": ('player', 'minh'), "scene_06_windows": ('player', 'minh'),
        "scene_07_final_class": ('player', 'minh', 'thaydev'),
        "scene_08_final_choice": ('player', 'minh'),
    }
    for line in lines:
        if line.startswith('label '):
            label = line.split()[1].rstrip(':')
        if label == 'good_ending' and line == '    call screen post_ending_actions':
            line = '    call screen chapter1_good_actions'
        if label == 'good_ending' and line == '    $ renpy.save_persistent()':
            result.extend(['    $ chapter1_canonical_result = "good"', '    $ unlock_chapter2()'])
        result.append(line)
        indent = line[:len(line) - len(line.lstrip())]
        if line == 'label start:':
            result.extend(['    $ current_chapter = 1', '    $ chapter1_canonical_result = None',
                           '    $ reset_chapter2_state()', '    $ set_stage()'])
        if line.lstrip().startswith('scene '):
            background = line.split()[1]
            transition = line.split(' with ', 1)[1] if ' with ' in line else None
            if transition:
                result[-1] = indent + 'scene ' + background
            cast = casts.get(label, ('player',))
            if label == 'good_ending':
                cast = ('player',) if background == 'bedroom_gaming' else ('player', 'baove')
            elif label == 'bad_ending':
                cast = ('player', 'minh', 'linh')
                if background == 'computer_lab':
                    cast += ('colms',)
                elif background == 'school_gate_night':
                    cast = ('player', 'baove')
                elif background == 'bedroom_morning':
                    cast = ('player',)
            result.append(indent + '$ set_stage(' + ', '.join(repr(v) for v in cast) + ')')
            if transition:
                result.append(indent + 'with ' + transition)
        if line.strip() == 'n "MINH đứng bên trong."':
            result.append(indent + '$ set_stage("player", "minh")')
        if line.strip() == 'n "CÔ LMS xuất hiện như bóng ma phía sau giao diện."':
            result.append(indent + '$ set_stage("player", "minh", "thaydev", "colms")')
        if line.strip() == 'n "CÔ LMS xuất hiện ở góc màn hình."':
            result.append(indent + '$ set_stage("player", "minh", "colms")')
        if line.strip() == 'centered "23:47"':
            result.append(indent + '$ set_stage("player")')
    return result

(GAME / "script.rpy").write_text("\n".join(integrate_chapters(script)) + "\n", encoding="utf-8")
(GAME / "endings.rpy").write_text("\n".join(integrate_chapters(endings)) + "\n", encoding="utf-8")
print("Wrote game/script.rpy and game/endings.rpy from screenplay v2.0")
