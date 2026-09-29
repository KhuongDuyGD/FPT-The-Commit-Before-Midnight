# Generated from VisualNovelContent.txt v2.0. Dialogue remains in source order.
# Change scene art, stats, and route logic here; rerun tools/build_story.py only
# when replacing the screenplay with a new version.

label start:
    $ current_chapter = 1
    $ chapter1_canonical_result = None
    $ reset_chapter2_state()
    $ set_stage()
    # Explicit resets make Start Game and New Game+ share the same baseline.
    $ energy = 100
    $ sanity = 100
    $ academic_progress = 0
    $ escape_point = 0
    $ pending_tasks = 0
    $ attendance_done = False
    $ quiz_done = False
    $ group_task_done = False
    $ assignment_uploaded = False
    $ escaped_school = False
    $ final_choice = None
    $ player_expression = "exhausted"
    show screen stats_hud
    if new_game_plus:
        centered "NEW GAME+\nDifficulty Unlocked: SENIOR YEAR."
        $ new_game_plus = False
    jump scene_00_alarm

label scene_00_alarm:
    scene bedroom_morning
    $ set_stage('player')
    with fade
    n "Ánh sáng buổi sáng lọt qua rèm."
    n "Laptop trên bàn vẫn còn mở."
    n "Màn hình hiển thị launcher game."
    n "Một lon nước nằm cạnh chuột."
    n "Điện thoại:"
    n "06:29"
    n "PLAYER ngủ bất động."
    n "Thứ Sáu."
    n "Một ngày mới."
    n "Một cơ hội mới."
    n "Một buổi sáng tuyệt đẹp để một sinh viên trẻ tuổi học tập, phát triển bản thân và tiến gần hơn đến tương lai."
    pause 0.3
    n "Đáng tiếc, nhân vật chính của chúng ta đi ngủ lúc 2 giờ 47 phút sáng."
    scene bedroom_gaming
    $ set_stage('player')
    with fade
    $ player_expression = "happy"
    centered "02:41 AM"
    voice_chat "Trận cuối nha."
    p "Ừ."
    centered "02:47 AM"
    voice_chat "Thua cay quá."
    p "Rematch."
    n "Đây được giới sử học hiện đại gọi là:"
    n "Sai lầm chiến lược."
    scene bedroom_morning
    $ set_stage('player')
    with fade
    $ player_expression = "exhausted"
    n "06:30."
    n "Điện thoại rung dữ dội."
    play sound sfx_alarm
    p "..."
    n "Alarm tiếp tục."
    p "Biết rồi…"
    n "Alarm tiếp tục."
    n "PLAYER mở mắt."
    p "...mình ghét công nghệ."
    play sound sfx_boss
    call screen boss_title("THE ALARM CLOCK", "Threat: ★★★★★  •  Special Ability: Snooze")
    menu:
        "Năm phút nữa thôi.":
            n "PLAYER tắt báo thức."
            p "05 phút."
            p "Đúng 05 phút."
            p "Mình là người trưởng thành."
            n "Màn hình tối."
            n "TIME SKIP."
            centered "07:18"
            n "PLAYER bật dậy."
            p "..."
            n "Nhìn điện thoại."
            p "Không."
            n "Nhìn lại."
            n "07:18."
            p "Không không không."
            n "Một giây im lặng."
            p "ĐỆ—"
            play sound sfx_windows_error
            $ energy -= 20
            $ escape_point -= 1
        "Dậy. Ngay.":
            n "PLAYER nhìn trần nhà."
            p "Cơ thể."
            p "Chúng ta cần nói chuyện."
            n "Không phản hồi."
            p "Tao biết mày muốn ngủ."
            n "PLAYER ngồi dậy."
            p "Nhưng nếu nghỉ hôm nay thì attendance của chúng ta sẽ cùng chết."
            n "PLAYER đứng lên."
            n "Một khoảnh khắc trưởng thành hiếm hoi."
            n "Hãy tận hưởng nó."
            n "Khả năng cao hôm nay sẽ không có lần thứ hai."
            $ escape_point += 1
    jump scene_01_gate

label scene_01_gate:
    scene school_gate_morning
    $ set_stage('player')
    with fade
    $ player_expression = "normal"
    centered "CAMPUS GATE"
    n "PLAYER chạy từ ngoài cổng vào."
    n "Balo nảy liên tục sau lưng."
    p "Hai phút."
    n "Thở."
    p "Hai phút là rất nhiều."
    n "Thở mạnh hơn."
    p "Speedrunner làm được."
    n "Kỷ lục chạy 100 mét thế giới chưa từng được thiết lập bởi một người có attendance treo trên đầu."
    n "PLAYER chạy vào tòa nhà."
    centered "ELEVATOR"
    n "Cửa thang máy đang đóng."
    p "GIỮ CỬA—"
    n "Một bàn tay thò ra."
    n "Cửa mở."
    n "MINH đứng bên trong."
    $ set_stage("player", "minh")
    m "Ê."
    n "PLAYER bước vào, cúi người thở."
    p "Cảm ơn."
    m "Sáng nay ông—"
    n "PLAYER giơ tay."
    p "Khoan."
    m "?"
    p "Cho tôi đoán."
    n "PLAYER hít sâu."
    p "Bài."
    m "..."
    p "Project."
    m "..."
    p "Hay meeting?"
    m "Tôi định hỏi ông ăn sáng chưa."
    p "..."
    m "Nhưng bài làm chưa?"
    n "PLAYER nhắm mắt."
    p "Tôi biết ngay mà."
    n "DING."
    centered "07:30"
    n "PLAYER nhìn bảng tầng."
    p "Perfect."
    m "Ông tới đúng giờ mà."
    p "Không."
    p "Tôi tới vào đúng frame cuối cùng."
    play sound sfx_bell
    $ attendance_done = True
    jump scene_02_quiz

label scene_02_quiz:
    scene classroom
    $ set_stage('player', 'minh', 'thaydev')
    with dissolve
    n "THẦY DEV bước vào."
    dev "Good morning."
    n "Cả lớp phản hồi với mức năng lượng của một nghĩa trang."
    crowd "Morning…"
    dev "Sáng nay mọi người khỏe không?"
    p "Không."
    m "Cũng không."
    dev "Rất tốt."
    p "Thầy nghe kiểu gì ra chữ tốt vậy?"
    n "THẦY DEV mở laptop."
    dev "Khởi động nhẹ bằng quiz nhé."
    n "Không khí trong phòng thay đổi."
    p "..."
    m "..."
    student "Em xin đổi câu trả lời. Em đang không khỏe."
    dev "Mười câu thôi."
    n "PLAYER thở ra."
    dev "Open book."
    n "Một vài người bắt đầu hồi sinh."
    dev "Hai mươi phút."
    p "Ổn."
    dev "Có coding."
    pause 0.3
    n "PLAYER quay sang Minh."
    n "MINH nhìn PLAYER."
    p "Ông có muốn nói gì trước khi chúng ta chết không?"
    m "Tôi để lại Steam Library cho ông."
    p "Cảm động quá."
    with flash
    menu:
        "Đọc đề trước khi hoảng.":
            n "PLAYER nhìn màn hình."
            p "Bình tĩnh."
            p "Đề hỏi gì?"
            pause 0.3
            p "Input."
            p "Output."
            p "Edge case."
            p "Rồi."
            n "PLAYER mở IDE."
            n "MINH liếc sang."
            m "Ủa hôm nay chuyên nghiệp vậy?"
            p "Im."
            p "Tôi đang có momentum."
            n "Một lúc sau."
            p "Compile."
            n "ERROR."
            p "Expected."
            n "Sửa."
            n "Compile."
            n "PASS."
            p "..."
            p "Không thể tin được."
            m "Gì?"
            p "Tôi đọc đề trước khi code."
            m "Character development."
            n "ACHIEVEMENT:"
            centered "READ THE DOCUMENTATION"
            n "Bạn vừa vô tình hành xử như một developer chuyên nghiệp."
            $ sanity -= 5
            $ academic_progress += 2
            $ quiz_done = True
        "Panic trước, đọc đề sau.":
            n "PLAYER mở đề."
            p "Ok."
            n "Ba giây sau."
            p "Tôi không biết gì cả."
            m "Ông mới đọc tiêu đề."
            p "Tiêu đề đã rất đáng sợ."
            n "PLAYER mở IDE."
            m "Ông định code gì?"
            p "Chưa biết."
            m "Vậy mở IDE làm gì?"
            p "Tạo cảm giác mình đang làm việc."
            n "PLAYER nhìn error console trống."
            p "Stack Overflow…"
            m "Ông còn chưa có error."
            p "Tôi chuẩn bị trước."
            $ sanity -= 20
            $ pending_tasks += 1
    jump scene_03_break

label scene_03_break:
    scene hallway
    $ set_stage('player', 'minh')
    with fade
    n "PLAYER bước ra hành lang."
    p "Coffee."
    m "Căn tin?"
    p "Coffee."
    m "Ăn gì không?"
    p "Coffee có nước."
    m "Đó không phải bữa sáng."
    n "Điện thoại PLAYER rung."
    play sound sfx_notification
    n "PLAYER nhìn xuống."
    l "@everyone mọi người đang ở trường đúng không?"
    p "Không."
    m "Ông đang đứng trong trường mà."
    p "Về mặt tinh thần thì không."
    n "Điện thoại rung lần nữa."
    l "Meeting nhanh 10 phút được không?"
    n "PLAYER nhìn Minh."
    p "Cô ấy nói câu cấm."
    m "Câu gì?"
    p "‘10 phút.’"
    n "Thông báo thứ ba."
    l "Có một vấn đề hơi quan trọng."
    p "Đó."
    p "Boss music."
    play sound sfx_boss
    call screen boss_title("QUICK MEETING", "Threat: ★★★★★★  •  Passive: Nhân tiện…")
    menu:
        "Đi ăn trước.":
            n "PLAYER khóa màn hình điện thoại."
            p "Không."
            m "Không meeting?"
            p "Không meeting khi bụng rỗng."
            m "Nghe hợp lý."
            p "Nếu project chết thì còn cứu được."
            p "Nếu tôi chết thì project mất developer."
            m "Lập luận ích kỷ nhưng hợp lý."
            $ energy += 20
            $ sanity += 10
            $ escape_point += 1
        "Join meeting.":
            n "Video call mở."
            l "Hello."
            p "Hello."
            m "Hello."
            l "Ok nhanh thôi nha."
            n "PLAYER nhìn thẳng camera."
            p "Lịch sử sẽ phán xét câu nói đó."
            centered "TIME — 09:35"
            l "Đầu tiên là API."
            l "Tiếp theo UI."
            l "À còn database."
            centered "TIME — 10:47"
            n "PLAYER nhìn đồng hồ."
            p "Linh."
            l "Hử?"
            p "Chúng ta bắt đầu lúc mấy giờ?"
            l "Chín rưỡi."
            p "Meeting này đã sống lâu hơn bữa sáng của tôi."
            l "Còn một cái cuối thôi."
            p "Câu đó còn đáng sợ hơn ‘meeting nhanh’."
            $ energy -= 25
            $ sanity -= 15
            $ academic_progress += 1
            $ pending_tasks = max(0, pending_tasks - 1)
    jump scene_04_project

label scene_04_project:
    scene hallway
    $ set_stage('player', 'minh', 'linh')
    with dissolve
    n "LINH mở laptop."
    l "Có tin tốt và tin xấu."
    p "Tin tốt trước."
    l "Project build được."
    p "Nice."
    l "Tin xấu là chạy không được."
    n "PLAYER im lặng."
    p "Linh."
    l "Hử?"
    p "Định nghĩa ‘build được’ của chúng ta hơi rộng."
    m "Máy tôi chạy mà."
    n "PLAYER quay sang."
    p "Commit?"
    m "Có."
    p "Push?"
    n "MINH đứng yên."
    p "..."
    m "Ờ…"
    p "Minh."
    m "Tôi tưởng push rồi."
    p "Minh."
    m "Tôi có commit."
    p "Git không phải Google Drive."
    m "Biết rồi mà."
    n "PLAYER nhìn trần nhà."
    n "Developer trải qua năm giai đoạn đau buồn."
    n "Denial."
    n "Anger."
    n "Bargaining."
    n "Depression."
    n "git pull"
    menu:
        "Fix luôn.":
            p "Đưa branch đây."
            m "Giờ á?"
            p "Giờ."
            p "Nếu tôi để cái này tới chiều, chiều nó sẽ đẻ thêm ba bug."
            l "Chuẩn."
            p "Đừng đồng ý nhanh thế. Tôi đang cố tự an ủi."
            n "Một đoạn montage debug."
            p "Null."
            m "Ở đâu?"
            p "Ở nơi null luôn xuất hiện."
            m "...?"
            p "Chỗ không ai check."
            n "Fix hoàn tất."
            p "Done."
            l "Nice."
            p "Không thêm scope."
            l "Tôi chưa nói gì."
            p "Tôi thấy ánh mắt."
            n "PLAYER vừa đưa ra quyết định rất tốt."
            n "Điều này chắc chắn sẽ không khiến cậu chủ quan vào buổi chiều."
            $ energy -= 15
            $ academic_progress += 2
            $ group_task_done = True
            $ escape_point += 1
        "Để chiều.":
            p "Chiều làm."
            l "Chắc không?"
            p "Chắc."
            m "Chắc thật?"
            p "Các người đừng khiến tôi nghi ngờ quyết định của mình."
            n "Quá muộn."
            n "Quyết định đã được lưu."
            n "Game sẽ nhớ điều này."
            $ pending_tasks += 2
    jump scene_05_lunch

label scene_05_lunch:
    scene canteen
    $ set_stage('player', 'minh')
    with fade
    n "PLAYER ngồi xuống."
    n "Trước mặt là đồ ăn."
    n "PLAYER nhìn khay cơm như nhìn thấy người thân thất lạc."
    p "Cuối cùng."
    m "Ăn xong làm assignment nha."
    n "PLAYER từ từ ngẩng đầu."
    p "Minh."
    m "Gì?"
    p "Ông có sở thích nào không?"
    m "Có chứ."
    p "Ví dụ?"
    m "Game."
    p "Hay."
    m "Nhưng tối nay deadline nên—"
    p "Không."
    m "?"
    p "Một câu."
    p "Một câu không nhắc tới deadline."
    n "MINH suy nghĩ."
    m "Hôm nay thời tiết đẹp."
    p "Cảm ơn."
    pause 0.3
    m "Thích hợp ngồi làm bài."
    n "PLAYER đặt muỗng xuống."
    p "Tôi bỏ cuộc."
    menu:
        "Ăn như một con người bình thường.":
            p "Laptop đóng."
            m "Ông không làm hả?"
            p "Tôi đang làm."
            m "Làm gì?"
            p "Bảo trì hardware."
            n "PLAYER chỉ vào bản thân."
            $ energy += 30
            $ sanity += 10
        "Vừa ăn vừa code.":
            n "Laptop mở cạnh khay cơm."
            p "Function."
            n "Ăn một muỗng."
            p "Cơm."
            n "Gõ."
            p "Function."
            n "Ăn."
            p "Cơm."
            m "Ông biết nước mắm đang cách touchpad khoảng 12 centimet không?"
            n "PLAYER dừng."
            n "Nhìn laptop."
            n "Nhìn chén nước mắm."
            n "PLAYER nhẹ nhàng đẩy chén ra xa."
            p "Cảm ơn."
            m "Tôi vừa cứu cả semester của ông."
            p "Ông vừa cứu SSD của tôi."
            $ academic_progress += 1
            $ energy += 10
            $ sanity -= 10
    jump scene_06_windows

label scene_06_windows:
    scene computer_lab
    $ set_stage('player', 'minh')
    with fade
    n "PLAYER ngồi xuống máy lab."
    p "Ok."
    n "PLAYER đặt tay lên chuột."
    p "Chỉ cần hoàn thiện phần này."
    n "Màn hình bật."
    $ player_expression = "angry"
    centered "WINDOWS IS UPDATING"
    n "3%%"
    p "..."
    n "PLAYER chớp mắt."
    p "Không."
    n "4%%."
    p "Không."
    n "5%%."
    p "Máy."
    p "Hôm nay tao không có thời gian chơi trò này."
    n "Màn hình:"
    n "Working on updates."
    p "TAO CŨNG ĐANG WORKING."
    play sound sfx_windows_error
    with hpunch
    play sound sfx_boss
    call screen boss_title("WINDOWS UPDATE", "Defense: 9999  •  Weakness: Laptop cá nhân")
    n "MINH ngồi máy kế bên."
    m "Máy tôi lên rồi."
    n "PLAYER từ từ quay sang."
    p "Minh."
    m "Hử?"
    p "Trong tình bạn có những thứ không cần chia sẻ."
    m "..."
    p "Đây là một trong số đó."
    centered "15 MINUTES LATER"
    n "7%%."
    p "Tiến bộ."
    m "Có bốn phần trăm thôi mà."
    p "MINH."
    m "Ok."
    p "Cho tôi hy vọng."
    menu:
        "Rút laptop cá nhân.":
            n "PLAYER kéo balo lên bàn."
            p "Được."
            p "Muốn chiến tranh?"
            n "PLAYER mở laptop."
            p "Ta chơi theo luật của tao."
            m "Ông đang nói chuyện với Windows Update à?"
            p "Đừng xen vào."
            $ energy -= 5
            $ academic_progress += 2
            $ escape_point += 1
        "Chờ.":
            n "PLAYER chống cằm."
            n "Update:"
            n "8%%."
            p "Có lẽ đây là cơ hội."
            m "Cơ hội gì?"
            p "Suy ngẫm."
            m "Về?"
            p "Tại sao tôi chọn ngành này."
            n "Một khoảng im lặng."
            p "Lúc nhỏ tôi thích game."
            m "Ờ."
            p "Không ai nói với tôi sẽ có database."
            $ sanity -= 20
    jump scene_07_final_class

label scene_07_final_class:
    scene classroom_afternoon
    $ set_stage('player', 'minh', 'thaydev')
    with fade
    $ player_expression = "normal"
    n "Ánh nắng chiều tràn vào lớp."
    n "PLAYER nhìn đồng hồ."
    n "15:45."
    p "Một tiếng mười lăm."
    m "Gì?"
    p "Không có gì."
    n "PLAYER nhìn ra cửa sổ."
    p "Mình chỉ đang đếm khoảng cách tới tự do."
    n "THẦY DEV tiếp tục giảng."
    dev "Rồi, phần hôm nay đến đây thôi."
    n "PLAYER lập tức ngồi thẳng."
    p "..."
    m "Đừng vui sớm."
    p "Đừng nguyền."
    dev "Trước khi kết thúc…"
    n "PLAYER nhắm mắt."
    p "Minh."
    m "Ừ."
    p "Ông nói đúng."
    dev "Thầy có một assignment nhỏ."
    n "Cả phòng phát ra tiếng rên tập thể."
    dev "Không khó đâu."
    p "Thầy."
    dev "Hử?"
    p "Với tất cả sự kính trọng…"
    p "Câu đó chưa bao giờ khiến tụi em bình tĩnh hơn."
    n "Cả lớp cười."
    dev "Thật mà."
    n "THẦY DEV click slide."
    $ player_expression = "cry"
    with flash
    play sound sfx_notification
    centered "DEADLINE — TODAY 23:59"
    n "Không khí chết lặng."
    p "..."
    m "..."
    dev "Có gì không?"
    p "Không thầy."
    p "Tụi em chỉ vừa nhìn thấy tương lai."
    n "Màn hình điện thoại sáng."
    n "Một notification."
    n "CÔ LMS xuất hiện như bóng ma phía sau giao diện."
    $ set_stage("player", "minh", "thaydev", "colms")
    lms "Assignment published."
    p "Không."
    lms "Deadline."
    pause 0.3
    lms "23:59."
    p "Cô có thể nói nhỏ hơn không?"
    lms "23:59."
    p "Cô cố tình đúng không?"
    lms "Reminder scheduled."
    p "CÔ CÒN REMIND NỮA?"
    $ pending_tasks += 1
    jump scene_08_final_choice

label scene_08_final_choice:
    scene classroom_afternoon
    $ set_stage('player', 'minh')
    with dissolve
    $ player_expression = "normal"
    n "Laptop đã đóng."
    n "Balo đã đeo."
    n "PLAYER nhìn đồng hồ."
    n "16:55."
    p "Năm phút."
    m "Ông chuẩn bị về thật à?"
    p "Tôi đã chuẩn bị tinh thần từ 7 giờ 30."
    n "Thông báo Discord."
    play sound sfx_notification
    n "PLAYER nhìn điện thoại."
    centered "LINH — GROUP PROJECT"
    n "@everyone"
    p "Không."
    n "Tin nhắn tiếp theo."
    n "Có ai ở lại fix giúp mình một chút không?"
    n "PLAYER nhìn màn hình."
    n "Một khoảng im lặng."
    m "Ông tính sao?"
    p "Tôi đang đấu tranh nội tâm."
    m "Bên nào thắng?"
    p "Bên muốn về nhà đang có lợi thế áp đảo."
    m "Assignment?"
    p "Có laptop ở nhà."
    m "Project?"
    p "GitHub tồn tại."
    m "Meeting?"
    p "Discord tồn tại."
    m "Lab?"
    p "Remote desktop tồn tại."
    m "Thầy?"
    p "Thầy cũng có gia đình, Minh."
    menu:
        "Về.":
            $ final_choice = 'leave'
            n "PLAYER nhìn tin nhắn Linh."
            n "Gõ:"
            n "Tui về trước nha. Có gì tối ping tui, phần cần fix tui xử lý ở nhà."
            n "Send."
            l "oke, về đi :))"
            p "..."
            p "Ủa."
            m "Gì?"
            p "Tôi tưởng sẽ có boss fight."
            m "Linh có bắt ông ở lại đâu."
            n "PLAYER đứng im."
            p "Vậy nãy giờ…"
            m "Ông tự stress."
            p "..."
            p "Character development hơi đau."
            $ escape_point += 2
            if can_escape_school():
                $ escaped_school = True
                jump good_ending
            else:
                n "Deadline và những việc chưa xong vẫn giữ PLAYER lại trường."
                jump bad_ending
        "Ở lại thêm chút.":
            $ final_choice = 'stay'
            n "PLAYER nhìn tin nhắn."
            p "Thôi."
            n "PLAYER tháo balo."
            m "Ở lại à?"
            p "Fix cho xong."
            m "Nice."
            l "Cảm ơn nha."
            n "CÔ LMS xuất hiện ở góc màn hình."
            $ set_stage("player", "minh", "colms")
            lms "Excellent decision."
            p "Cô đừng tham gia vào chuyện này."
            jump bad_ending

label new_game_plus:
    $ new_game_plus = True
    jump start
