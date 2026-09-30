"""Import only attributed dialogue from the Chapter 2 brief.

The document contains implementation instructions as well as fiction. This
importer deliberately ignores its instructions/prose and explicitly supplies
scene staging, menus, stat changes and ending flow below. Run after reviewing
the ranges if the supplied document changes. Ren'Py needs only the .rpy output.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / 'FPT_Escape_Protocol_Chapter2_Codex6Sol_Implementation_Prompt.md').read_text(encoding='utf-8-sig').splitlines()
SPEAKERS = {'Main': 'p', 'Minh': 'm', 'Ngân': 'ngan', 'Nghi': 'nghi',
            'Cô Triết': 'philosophy', 'Thầy Thể Dục': 'pe', 'Cô Y Tá': 'nurse'}
for number, title in {523: '# CH2_00', 1299: '# CH2_06', 1465: '# CH2_07', 2072: '# CH2_12'}.items():
    assert SOURCE[number - 1].startswith(title), 'Review scene ranges before regenerating.'


def quote(text):
    return json.dumps(text.replace('%', '%%').replace('[', '[['), ensure_ascii=False)


def dialogue(first, last, level=4, cues=None):
    result, speaker = [], None
    cues = cues or {}
    for line in SOURCE[first - 1:last]:
        value = line.strip()
        match = re.fullmatch(r'\*\*([^:]+):\*\*', value)
        if match:
            speaker = SPEAKERS[match.group(1).split(' (')[0]]
        elif speaker and value.startswith('“') and value.endswith('”'):
            result.append(' ' * level + speaker + ' ' + quote(value[1:-1]))
            speaker = None
        elif value in ('Pause.', 'Silence.', 'Small pause.', 'A short beat.', 'Small silence.', 'Long pause.', 'Long silence.'):
            result.append(' ' * level + 'pause 0.6')
        if value in cues:
            for command in cues[value]:
                result.append(' ' * level + command)
    return result


script = ['# Chapter 2: imported Vietnamese dialogue, explicit editable Ren\'Py flow.',
          '# See tools/build_chapter2.py and CHAPTER2.md before regenerating.', '']
out = script


def add(*parts):
    for part in parts:
        out.extend([part] if isinstance(part, str) else part)


def scene(label, background, cast, title=None, visual=None):
    composition = ', visual=' + repr(visual) if visual is not None else ''
    add('', 'label ' + label + ':', '    $ ch2_hint_context = None',
        '    scene ' + background, '    $ set_stage(' + ', '.join(repr(v) for v in cast) + composition + ')', '    with fade')
    if title:
        add('    centered ' + quote(title))


def menu(options, hint=None):
    if hint:
        add('    $ ch2_hint_context = ' + repr(hint))
    add('    menu:')
    for caption, first, last, state, commands in options:
        add('        ' + quote(caption) + ':')
        add(['            ' + c for c in commands])
        if first:
            add(dialogue(first, last, 12))
        for key, value in state.items():
            add('            $ ' + key + ' += ' + str(value))
        if not first and not commands and not state:
            add('            pass')
    add('    $ ch2_hint_context = None')


scene('CH2_00', 'school_gate_morning', ('player', 'minh'), 'SÁNG HÔM SAU\nTHE ESCAPE WAS TEMPORARY')
add(dialogue(523, 585), '    with hpunch', '    jump CH2_01')
scene('CH2_01', 'hallway', ('player', 'minh', 'ngan'), visual=('player', 'ngan'))
add('    $ ngan_expression = "excited"', dialogue(586, 614), '    $ ngan_expression = "normal"', dialogue(616, 628), '    with hpunch')
menu([
    ('Sáng nay trông mày vui dữ.', 638, 642, {}, ['p "Sáng nay trông mày vui dữ."', '$ ngan_expression = "happy"']),
    ('Sáng nay trông mày xinh đấy.', 644, 673, {'NganAffinity': 2, 'NganSpecialFlags': 1}, ['$ ngan_expression = "embarrassed"']),
    ('Đi lẹ không trễ.', None, None, {}, ['p "Đi lẹ không trễ."']),
])
add('    $ ngan_expression = "normal"', '    jump CH2_02')
scene('CH2_02', 'philosophy_morning', ('player', 'minh', 'ngan', 'philosophy'), visual=('player', 'philosophy'))
add('    play sound sfx_bell', dialogue(679, 761, cues={
    'Nghi enters.': ['$ set_stage("player", "minh", "ngan", "philosophy", "nghi", visual=("player", "philosophy", "nghi"), entrance="scale")'],
    'Main freezes.': ['$ player_expression = "surprised"'],
    'Main looks at Nghi.': ['$ set_shot("player", "minh", "ngan")', '$ player_expression = "embarrassed"', 'play sound sfx_windows_error', 'with flash',
                            'centered "[[UNKNOWN PROCESS DETECTED]\\nHeart.exe CPU usage: 97%%\\nSocialSkill.dll: NOT FOUND"'],
}), dialogue(762, 785), dialogue(2629, 2637), '    jump CH2_03')
scene('CH2_03', 'philosophy_morning', ('player', 'minh', 'ngan', 'nghi', 'philosophy'), visual=('player', 'philosophy'))
add('    $ player_expression = "normal"', dialogue(786, 831, cues={
    'Board:': ['n "Mâu thuẫn có phải lúc nào cũng mang ý nghĩa tiêu cực?"'],
}))
menu([
    ('A. Ý bạn khá giống sự thống nhất và đấu tranh giữa các mặt đối lập.', 861, 890, {'NghiAffinity': 2, 'NghiComfort': 1}, ['$ nghi_expression = "confused"']),
    ('B. Ừ, mình cũng nghĩ vậy.', 891, 906, {'NghiAffinity': 1}, []),
    ('C. Bạn nói hay thật.', 907, 923, {'NghiAffinity': 1, 'NghiComfort': -1}, ['$ player_expression = "embarrassed"']),
    ('D. Bạn có người yêu chưa?', 924, 960, {'NghiComfort': -3}, ['$ CH2MajorFail = True', '$ ngan_expression = "angry"', 'with hpunch']),
], 'first_contact')
add('    $ ngan_expression = nghi_expression = "normal"', '    jump CH2_04')
scene('CH2_04', 'hallway', ('player', 'ngan'))
add(dialogue(961, 1019), '    if CH2MajorFail:', dialogue(1022, 1027, 8),
    '    else:', dialogue(1030, 1035, 8), dialogue(1038, 1069),
    '    centered "NGÂN HINT UNLOCKED\\n[NganHintsRemaining]/3 LƯỢT CÒN LẠI"',
    dialogue(2642, 2653), '    jump CH2_05')
scene('CH2_05', 'library_afternoon', ('player', 'nghi'), 'THƯ VIỆN — CHIỀU')
add(dialogue(1070, 1092))
menu([
    ('A. Bạn đang đọc gì vậy?', 1116, 1153, {'NghiAffinity': 2, 'NghiComfort': 1}, ['$ nghi_expression = "soft_smile"']),
    ('B. Hôm nay bạn xinh thật.', 1154, 1174, {'NghiAffinity': 1, 'NghiComfort': -2}, ['$ nghi_expression = "confused"']),
    ('C. Tôi cũng đọc nhiều lắm.', 1175, 1201, {'NghiAffinity': 2}, ['$ nghi_expression = "soft_smile"']),
    ('D. Im lặng ngồi cạnh.', 1202, 1227, {'NghiAffinity': 1, 'NghiComfort': 2}, ['n "PLAYER mở laptop, yên lặng ngồi cạnh Nghi."', 'pause 0.6']),
], 'library')
add('    $ nghi_expression = "normal"', dialogue(1228, 1298, cues={
    "Use `Nghi_SoftSmile`.": ['$ nghi_expression = "soft_smile"', '$ refresh_stage()'],
}), '    $ NghiAffinity += 2', '    $ NghiComfort += 2', dialogue(2658, 2680))
# Brief's optional coding micro-event becomes a small, genuine conversation.
# Original choice deltas remain intact. These additions allow recovery after D.
menu([
    ('Giải thích bug cho Nghi, rồi hỏi ý kiến bạn ấy.', None, None, {'NghiAffinity': 3, 'NghiComfort': 1}, [
        'p "Bạn muốn thử tìm cùng tôi không?"', 'nghi "Tôi không biết code."',
        'p "Không sao. Tôi giải thích."', 'nghi "Ừ. Nhưng chậm thôi."', '$ nghi_expression = "soft_smile"']),
    ('Tắt laptop, cùng Nghi tìm tài liệu cho buổi học tới.', None, None, {'NghiAffinity': 3, 'NghiComfort': 1}, [
        'p "Bug để sau. Bạn cần tìm thêm tài liệu không?"', 'nghi "Có. Cảm ơn."']),
    ('Tiếp tục code một mình.', None, None, {}, ['p "Để tôi fix nốt đã."', 'nghi "Ừ."']),
])
add('    jump CH2_06')
scene('CH2_06', 'sports_morning', ('player', 'minh', 'ngan', 'nghi', 'pe'), 'NGÀY TIẾP THEO — THỂ DỤC', visual=('player', 'minh', 'pe'))
add('    $ player_expression = "normal"', '    $ nghi_expression = "normal"',
    '    play sound sfx_boss', '    call screen boss_title("PHYSICAL EDUCATION", "Class: Game Developer  •  Stamina: NOT FOUND")', dialogue(1299, 1350))
menu([
    ('A. Cố chạy cạnh Nghi.', 1360, 1381, {'NghiAffinity': 1}, ['$ ch2_sports_choice = "A"', '$ player_expression = "exhausted"']),
    ('B. Chạy đúng sức.', None, None, {'NghiComfort': 1}, ['$ ch2_sports_choice = "B"', 'n "PLAYER giữ nhịp chạy vừa sức."']),
    ('C. Cố vượt Nghi để gây ấn tượng.', 1393, 1414, {'NghiAffinity': 1, 'NghiComfort': -1}, ['$ ch2_sports_choice = "C"', '$ player_expression = "exhausted"', 'with hpunch']),
    ('D. Khi Ngân hụt chân, dừng lại hỏi cô ấy có ổn không.', 1415, 1464, {'NganAffinity': 3, 'NganSpecialFlags': 1}, ['$ ch2_sports_choice = "D"', '$ ngan_expression = "embarrassed"']),
])
add('    if ch2_sports_choice == "C":', '        n "PLAYER tăng tốc. Màn hình trước mắt bắt đầu mất frame."',
    '        with vpunch', '    else:', '        n "Sau buổi chạy, PLAYER chóng mặt. Cô y tá đưa cậu vào phòng nghỉ."',
    '    jump CH2_07')
scene('CH2_07', 'infirmary_afternoon', ('player', 'nurse', 'ngan'), 'PHÒNG Y TẾ — CHIỀU', visual=('player', 'nurse'))
add('    $ player_expression = "exhausted"', '    $ ngan_expression = "normal"', dialogue(1465, 1511, cues={
    'Nghi appears at the door.': ['$ set_stage("player", "nurse", "ngan", "nghi", visual=("player", "nurse", "nghi"), entrance="rise")'],
}))
menu([
    ('A. Ổn. Chỉ hơi xấu hổ thôi.', 1532, 1558, {'NghiAffinity': 3, 'NghiComfort': 2}, ['$ player_expression = "embarrassed"', '$ nghi_expression = "soft_smile"']),
    ('B. Chuyện nhỏ.', 1559, 1579, {'NghiComfort': -1}, ['$ nghi_expression = "confused"']),
    ('C. Tôi cố chạy vì bạn.', 1580, 1600, {'NghiAffinity': 1, 'NghiComfort': -3}, ['$ nghi_expression = "confused"']),
    ('D. Tôi nghĩ thầy thể dục muốn giết tôi.', 1601, 1623, {'NghiAffinity': 2, 'NghiComfort': 1}, ['$ nghi_expression = "happy"']),
], 'infirmary')
# Another warm, optional follow-up provides +3/+2 recovery without erasing
# earlier consequences. Repeated boundary-pushing still fails the final gate.
menu([
    ('Cảm ơn Nghi đã tới thăm, hỏi bạn ấy muốn nghỉ một lát không.', None, None, {'NghiAffinity': 3, 'NghiComfort': 2}, [
        '$ player_expression = "empathy"', 'p "Cảm ơn bạn tới thăm. Bạn cũng mệt không?"',
        'nghi "Một chút."', 'p "Vậy cứ ngồi nghỉ. Không cần nói gì đâu."',
        '$ nghi_expression = "soft_smile"', 'nghi "Ừ. Thế cũng tốt."']),
    ('Xin lỗi vì câu hỏi quá riêng tư hồi sáng.' , None, None, {'NghiAffinity': 3, 'NghiComfort': 2}, [
        'p "Hồi sáng tôi hỏi hơi vô duyên. Xin lỗi bạn."', 'nghi "Ừ. Đừng vội vậy."',
        'p "Tôi sẽ nhớ."', '$ nghi_expression = "soft_smile"']),
    ('Cố gây ấn tượng thêm.', None, None, {'NghiComfort': -1}, [
        'p "Lần sau tôi chạy gấp đôi."', 'nurse "Em nghỉ đã."']),
])
add('    n "Nghi chào mọi người rồi trở về lớp."', '    $ set_stage("player", "nurse", "ngan", visual=("player", "ngan"))', dialogue(1628, 1653),
    '    if NganAffinity >= 4:', '        $ ngan_expression = "thinking"', '        $ refresh_stage()', '        pause 0.6')
menu([
    ('Hỏi thăm chân Ngân và cảm ơn vì đã ở lại.', None, None, {'NganAffinity': 2, 'NganSpecialFlags': 1}, [
        '$ player_expression = "empathy"', 'p "Còn chân mày? Hết đau chưa?"',
        'ngan "Hết rồi. Lo cho mày trước đi."', 'p "Cảm ơn vì ở lại. Không phải chuyện Nghi. Chuyện tao ấy."',
        '$ ngan_expression = "embarrassed"', 'ngan "...Biết rồi."']),
    ('Nhờ Ngân xem Nghi đã nhắn gì chưa.', None, None, {}, [
        'p "Nghi có nhắn gì nữa không?"', '$ ngan_expression = "normal"', 'ngan "Tự xem đi."']),
])
add(dialogue(2704, 2712), '    $ player_expression = "normal"', '    $ ngan_expression = "normal"', '    jump CH2_08')
scene('CH2_08', 'philosophy_afternoon', ('player', 'minh', 'ngan', 'nghi', 'philosophy'), visual=('player', 'philosophy'))
add(dialogue(2685, 2699), dialogue(1654, 1719), '    pause 1.0', '    $ nghi_expression = "soft_smile"',
    '    n "Nghi lặng lẽ nhìn về phía PLAYER."', '    jump CH2_09')
scene('CH2_09', 'campus_day', ('player', 'nghi'), 'SAU GIỜ HỌC — SÂN TRƯỜNG')
add(dialogue(1720, 1747))
menu([
    ('A. Chắc bạn chỉ không biết phải nói gì thôi.', 1757, 1786, {'NghiAffinity': 2, 'NghiComfort': 3}, ['$ nghi_expression = "soft_smile"']),
    ('B. Tôi thấy bạn bình thường mà.', 1787, 1809, {'NghiAffinity': 2, 'NghiComfort': 1}, ['$ nghi_expression = "relaxed"']),
    ('C. Vì bạn dễ thương.', 1810, 1828, {'NghiAffinity': 2, 'NghiComfort': -1}, ['$ nghi_expression = "embarrassed"']),
    ('D. Tôi quen rồi.', 1829, 1845, {}, ['$ nghi_expression = "confused"']),
])
add('    jump CH2_10')
scene('CH2_10', 'canteen_afternoon', ('player', 'ngan'))
add('    $ ngan_expression = "happy"', dialogue(1846, 1921))
menu([
    ('A. Mày đúng là best wingman.', 1931, 1940, {'NganAffinity': 1}, ['p "Mày đúng là best wingman."']),
    ('B. Không có mày chắc tao chết.', 1941, 1948, {'NganAffinity': 1}, ['p "Không có mày chắc tao chết."']),
    ('C. Mà... dạo này tao toàn nói chuyện với mày về Nghi.', 1949, 1989, {'NganAffinity': 3, 'NganSpecialFlags': 1}, ['$ ngan_expression = "thinking"']),
    ('D. Mai giúp tao tiếp nha.', None, None, {}, ['p "Mai giúp tao tiếp nha."', 'ngan "...Ừ."']),
])
add('    jump CH2_11')
scene('CH2_11', 'rooftop_afternoon', ('player', 'ngan'))
add('    $ player_expression = "embarrassed"', '    $ ngan_expression = "normal"', dialogue(1995, 2051),
    '    if NganAffinity >= 7:', '        $ ngan_expression = "sad"', '        $ refresh_stage()', '        pause 0.6',
    '        $ ngan_expression = "normal"', '        $ refresh_stage()',
    '    $ NganEndingAvailable = ngan_route_available()', dialogue(2428, 2454),
    '    menu:', '        "Gọi Ngân lại." if NganEndingAvailable:', '            jump CH2_ngan_ending',
    '        "Đợi Nghi trên sân thượng.":', '            n "Ngân xuống cầu thang. PLAYER ở lại đợi Nghi."',
    '            $ set_stage("player")', '            jump CH2_12')
scene('CH2_12', 'rooftop_afternoon', ('player', 'nghi'), 'HOÀNG HÔN')
add('    $ nghi_expression = "normal"', dialogue(2072, 2090), '    stop sound',
    '    $ ch2_hint_context = "confession"', '    menu:',
    '        "Tôi thích bạn.":', '            $ chapter2_ending = resolve_chapter2(True)',
    '        "Tôi đã làm tất cả vì bạn. Bạn phải hiểu chứ.":', '            $ chapter2_ending = resolve_chapter2(False)',
    '    $ ch2_hint_context = None', '    if chapter2_ending == "nghi_good":', '        jump CH2_nghi_good',
    '    jump CH2_nghi_bad')
# Camera directions operate on shots only; they do not rewrite dialogue or stats.
SHOT_DIRECTIONS = {
    'CH2_01': {'    menu:': ('player', 'ngan')},
    'CH2_02': {
        '    ngan "Chết chưa."': ('player', 'ngan', 'philosophy'),
        '    philosophy "Trước khi bắt đầu, lớp chúng ta có một sinh viên mới."': ('player', 'philosophy'),
    },
    'CH2_03': {'    ngan "Nghi nghĩ sao?"': ('player', 'ngan', 'nghi')},
    'CH2_06': {
        '    ngan "Chậm thế?"': ('player', 'ngan'),
        '    menu:': ('player', 'ngan', 'nghi'),
        '            nghi "Bạn ổn chứ?"': ('player', 'nghi'),
        '            m "Ủa nó chạy đi đâu vậy?"': ('player', 'minh', 'ngan'),
        '            pe "HAI EM KIA!"': ('player', 'ngan', 'pe'),
    },
    'CH2_07': {
        "    $ ch2_hint_context = 'infirmary'": ('player', 'nghi'),
        '    nurse "Lần sau đừng cố chứng minh bản thân bằng cách ngất."': ('player', 'nurse'),
    },
    'CH2_08': {
        '    m "Không có gì."': ('player', 'minh', 'ngan'),
        '    philosophy "Em kia."': ('player', 'philosophy'),
        '    n "Nghi lặng lẽ nhìn về phía PLAYER."': ('player', 'nghi'),
    },
}
directed, label = [], None
for line in script:
    if line.startswith('label '):
        label = line.split()[1].rstrip(':')
    shot = SHOT_DIRECTIONS.get(label, {}).get(line)
    if shot is not None:
        indent = line[:len(line) - len(line.lstrip())]
        directed.append(indent + '$ set_shot(' + ', '.join(repr(a) for a in shot) + ')')
    directed.append(line)
(ROOT / 'game/chapter2.rpy').write_text('\n'.join(directed) + '\n', encoding='utf-8')

out = ['# Three independent Chapter 2 endings. Persistent flags unlock the gallery.', '']
scene('CH2_nghi_good', 'rooftop_afternoon', ('player', 'nghi'))
add('    $ player_expression = "embarrassed"', '    stop sound', dialogue(2125, 2241, cues={
    'Main freezes.': ['$ player_expression = "surprised"'],
    'Nghi uses `Nghi_HappySmile`.': ['$ nghi_expression = "soft_smile"'],
    'Nghi gives a small closed-mouth smile.': ['$ nghi_expression = "soft_smile"'],
    'Main visibly blushes.': ['$ player_expression = "embarrassed"'],
    'Main looks absurdly happy but still embarrassed.': ['$ player_expression = "very_happy"'],
    'Nghi laughs softly.': ['$ nghi_expression = "happy"'],
}), '    $ set_stage()', '    scene cg_nghi_good with dissolve',
    '    $ finish_chapter2("nghi_good")', '    play sound sfx_success',
    '    call screen chapter2_cg("GOOD ENDING", "LOVE PROTOCOL ESTABLISHED")',
    '    stop sound', '    scene rooftop_afternoon', '    $ set_stage("nghi")', '    with fade',
    '    ngan_message "Sao rồi?"', '    nghi "Ổn."', '    $ set_stage()', '    scene canteen_afternoon',
    '    $ ngan_expression = "sad"', '    $ set_stage("ngan")', '    with dissolve',
    '    n "Ngân gửi một biểu tượng đồng ý, rồi nhìn màn hình thêm một lúc."', '    pause 1.0', '    $ set_stage()', '    scene black with fade',
    '    centered "TO BE CONTINUED IN CHAPTER 3"', '    call screen chapter2_end_menu', '    return')
scene('CH2_nghi_bad', 'rooftop_afternoon', ('player', 'nghi'))
add('    stop sound', '    $ player_expression = "sad"', dialogue(2290, 2337, cues={
    'Use `Nghi_Sad`.': ['$ nghi_expression = "sad"'],
    'Main forces a small smile.': ['$ player_expression = "happy"'],
}), '    jump CH2_pub')
scene('CH2_pub', 'nearby_pub_night', ('player', 'minh'), 'TỐI — QUÁN GẦN TRƯỜNG')
add('    $ player_expression = "sad"', dialogue(2338, 2384), '    $ finish_chapter2("nghi_bad")',
    '    play sound sfx_bad', '    call screen chapter2_cg("BAD ENDING", "404 — LOVE NOT FOUND")',
    '    call screen chapter2_end_menu', '    return')
scene('CH2_ngan_ending', 'rooftop_afternoon', ('player', 'ngan'))
add('    stop sound', '    $ player_expression = "empathy"', dialogue(2455, 2622, cues={
    'Use `Ngan_Confused`.': ['$ ngan_expression = "confused"'],
    'Switch to `Ngan_Embarrassed`.': ['$ ngan_expression = "embarrassed"'],
    'Silence.': ['pause 0.8'],
    'Main looks worried.': ['$ player_expression = "sad"'],
    'Then Ngân smiles.': ['$ ngan_expression = "happy"'],
    'Main freezes.': ['$ player_expression = "surprised"'],
    "Main's face falls instantly.": ['$ player_expression = "sad"'],
    'Ngân bursts out laughing.': ['$ ngan_expression = "big_laugh"'],
    'Use `Ngan_BigLaugh`.': ['$ ngan_expression = "big_laugh"', '$ player_expression = "very_happy"'],
}), '    $ set_stage()', '    scene cg_ngan with dissolve', '    $ finish_chapter2("ngan")',
    '    play sound sfx_success', '    call screen chapter2_cg("SECRET ENDING", "YOU WERE NEVER LOST", "Some escape routes don\'t lead outside.\\nSometimes they lead home.")',
    '    centered "ROUTE COMPLETE"', '    call screen chapter2_end_menu', '    return')
(ROOT / 'game/chapter2_endings.rpy').write_text('\n'.join(out) + '\n', encoding='utf-8')
print('Wrote chapter2.rpy and chapter2_endings.rpy; dialogue extracted only from explicitly selected narrative ranges.')
