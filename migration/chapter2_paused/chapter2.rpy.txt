# Chapter 2: imported Vietnamese dialogue, explicit editable Ren'Py flow.
# See tools/build_chapter2.py and CHAPTER2.md before regenerating.


label CH2_00:
    $ ch2_hint_context = None
    scene school_gate_morning
    $ set_stage('player', 'minh')
    with fade
    centered "SÁNG HÔM SAU\nTHE ESCAPE WAS TEMPORARY"
    m "Dậy rồi à, chiến thần vượt ngục?"
    p "Đừng gọi tao như phạm nhân."
    m "Hôm qua mày chạy khỏi trường như đang né truy nã."
    p "Tao đã thoát."
    m "Ừ."
    p "Cuối cùng tao cũng tự do."
    m "...Mày biết hôm nay vẫn có tiết đúng không?"
    p "..."
    m "..."
    p "Tao tưởng Good Ending rồi?"
    m "Good Ending của hôm qua."
    p "Game gì scam vậy?"
    m "Đời."
    pause 0.6
    p "Cho tao quay lại Bad Ending được không?"
    m "Đi học."
    with hpunch
    jump CH2_01

label CH2_01:
    $ ch2_hint_context = None
    scene hallway
    $ set_stage('player', 'minh', 'ngan', visual=('player', 'ngan'))
    with fade
    $ ngan_expression = "excited"
    ngan "Ê."
    p "Ồ."
    ngan "Nghe nói hôm qua có thằng chạy khỏi trường như tội phạm."
    p "Tin giả."
    ngan "Camera quay được."
    p "Tin thật."
    ngan "Lại còn chạy ngang qua chỗ bảo vệ."
    $ ngan_expression = "normal"
    p "Đấy gọi là route tối ưu."
    m "Tối ưu kiểu gì suýt ăn biên bản?"
    p "Dynamic routing."
    ngan "Dynamic cái đầu mày."
    with hpunch
    $ set_shot('player', 'ngan')
    menu:
        "Sáng nay trông mày vui dữ.":
            p "Sáng nay trông mày vui dữ."
            $ ngan_expression = "happy"
            ngan "Vui vì thấy mày vẫn còn sống."
        "Sáng nay trông mày xinh đấy.":
            $ ngan_expression = "embarrassed"
            p "Sáng nay trông mày xinh đấy."
            ngan "..."
            p "Gì?"
            ngan "Không có gì."
            p "Ủa?"
            ngan "Đi học."
            $ NganAffinity += 2
            $ NganSpecialFlags += 1
        "Đi lẹ không trễ.":
            p "Đi lẹ không trễ."
    $ ch2_hint_context = None
    $ ngan_expression = "normal"
    jump CH2_02

label CH2_02:
    $ ch2_hint_context = None
    scene philosophy_morning
    $ set_stage('player', 'minh', 'ngan', 'philosophy', visual=('player', 'philosophy'))
    with fade
    play sound sfx_bell
    philosophy "Ổn định chỗ ngồi."
    philosophy "Hôm nay chúng ta bắt đầu với một khái niệm rất đơn giản."
    philosophy "Mâu thuẫn."
    p "Mâu thuẫn lớn nhất đời tao là muốn ngủ nhưng phải đi học."
    philosophy "Em áo đen cuối lớp."
    $ player_expression = "surprised"
    p "Dạ?"
    philosophy "Ví dụ rất thực tế."
    $ set_shot('player', 'ngan', 'philosophy')
    ngan "Chết chưa."
    p "Cô nghe kiểu gì vậy..."
    philosophy "Cô vẫn nghe."
    p "Dạ em xin lỗi."
    pause 0.6
    $ set_shot('player', 'philosophy')
    philosophy "Trước khi bắt đầu, lớp chúng ta có một sinh viên mới."
    $ set_stage("player", "minh", "ngan", "philosophy", "nghi", visual=("player", "philosophy", "nghi"), entrance="scale")
    nghi "Chào mọi người."
    nghi "Mình là Nghi."
    nghi "Mong được mọi người giúp đỡ."
    $ set_shot("player", "minh", "ngan")
    $ player_expression = "embarrassed"
    play sound sfx_windows_error
    with flash
    centered "[[UNKNOWN PROCESS DETECTED]\nHeart.exe CPU usage: 97%%\nSocialSkill.dll: NOT FOUND"
    m "Ê."
    m "Ê."
    ngan "...Đừng nói với tao."
    p "Tao yêu rồi."
    ngan "Mày còn chưa biết họ người ta."
    p "Tình yêu không cần database đầy đủ."
    ngan "Im."
    m "Mày nhìn người ta lần thứ mấy rồi?"
    p "Tao đang quan sát môi trường."
    m "Môi trường tóc vàng à?"
    jump CH2_03

label CH2_03:
    $ ch2_hint_context = None
    scene philosophy_morning
    $ set_stage('player', 'minh', 'ngan', 'nghi', 'philosophy', visual=('player', 'philosophy'))
    with fade
    $ player_expression = "normal"
    philosophy "Ba người một nhóm."
    philosophy "Trả lời câu hỏi này."
    n "Mâu thuẫn có phải lúc nào cũng mang ý nghĩa tiêu cực?"
    $ set_shot('player', 'ngan', 'nghi')
    ngan "Nghi nghĩ sao?"
    nghi "Không hẳn."
    nghi "Nếu không có mâu thuẫn thì nhiều sự vật cũng không có động lực để thay đổi."
    nghi "Quan trọng là mâu thuẫn đó phát triển theo hướng nào."
    ngan "Ê."
    p "Hả?"
    ngan "Nghe người ta nói kìa."
    $ ch2_hint_context = 'first_contact'
    menu:
        "A. Ý bạn khá giống sự thống nhất và đấu tranh giữa các mặt đối lập.":
            $ nghi_expression = "confused"
            p "Ý bạn khá giống sự thống nhất và đấu tranh giữa các mặt đối lập."
            nghi "Ừ."
            nghi "Bạn có nghe bài."
            p "...Tất nhiên."
            ngan "Xạo."
            $ NghiAffinity += 2
            $ NghiComfort += 1
        "B. Ừ, mình cũng nghĩ vậy.":
            p "Ừ, mình cũng nghĩ vậy."
            nghi "Ừm."
            $ NghiAffinity += 1
        "C. Bạn nói hay thật.":
            $ player_expression = "embarrassed"
            p "Bạn nói hay thật."
            nghi "...Cảm ơn."
            $ NghiAffinity += 1
            $ NghiComfort += -1
        "D. Bạn có người yêu chưa?":
            $ CH2MajorFail = True
            $ ngan_expression = "angry"
            with hpunch
            p "Bạn có người yêu chưa?"
            pause 0.6
            ngan "..."
            nghi "Không."
            p "Ồ."
            ngan "Xin lỗi Nghi."
            ngan "Nó bị lỗi firmware."
            $ NghiComfort += -3
    $ ch2_hint_context = None
    $ ngan_expression = nghi_expression = "normal"
    jump CH2_04

label CH2_04:
    $ ch2_hint_context = None
    scene hallway
    $ set_stage('player', 'ngan')
    with fade
    p "Ngân."
    ngan "Không."
    p "Tao còn chưa nói."
    ngan "Tao biết."
    p "Biết gì?"
    ngan "‘Dạy tao tán Nghi.’"
    pause 0.6
    p "...Dạy tao tán Nghi."
    ngan "Biết ngay."
    p "Cứu tao."
    ngan "Kinh nghiệm yêu đương?"
    p "Không."
    ngan "Không là bao nhiêu?"
    p "Không có."
    ngan "Thế bắt đầu bằng việc đừng nói mấy câu ngu."
    p "Cụ thể?"
    ngan "Ví dụ như hỏi người ta có người yêu chưa sau bốn phút quen biết."
    if CH2MajorFail:
        p "Đó là data collection."
        ngan "Đấy là phá hoại xã hội."
    else:
        p "Tao đâu có ngu vậy."
        ngan "Chưa thôi."
    ngan "Được rồi."
    ngan "Tao cứu mày ba lần."
    p "Ba?"
    ngan "Ba."
    p "Sao ít vậy?"
    ngan "Vì tao còn phải sống cuộc đời của tao."
    pause 0.6
    p "Deal."
    centered "NGÂN HINT UNLOCKED\n[NganHintsRemaining]/3 LƯỢT CÒN LẠI"
    p "Chào Nghi, hôm nay—"
    ngan "Không."
    p "Cái gì?"
    ngan "Nghe như NPC."
    jump CH2_05

label CH2_05:
    $ ch2_hint_context = None
    scene library_afternoon
    $ set_stage('player', 'nghi')
    with fade
    centered "THƯ VIỆN — CHIỀU"
    p "Chỗ này có ai ngồi chưa?"
    nghi "Chưa."
    pause 0.6
    $ ch2_hint_context = 'library'
    menu:
        "A. Bạn đang đọc gì vậy?":
            $ nghi_expression = "soft_smile"
            p "Bạn đang đọc gì vậy?"
            nghi "Tài liệu cho bài Triết."
            p "Bạn học trước luôn à?"
            nghi "Ừ."
            p "Tôi thường học sau khi deadline đã nhìn thấy tôi."
            nghi "Nghe không hiệu quả lắm."
            p "Không hiệu quả thật."
            $ NghiAffinity += 2
            $ NghiComfort += 1
        "B. Hôm nay bạn xinh thật.":
            $ nghi_expression = "confused"
            p "Hôm nay bạn xinh thật."
            nghi "...Cảm ơn."
            $ NghiAffinity += 1
            $ NghiComfort += -2
        "C. Tôi cũng đọc nhiều lắm.":
            $ nghi_expression = "soft_smile"
            p "Tôi cũng đọc nhiều lắm."
            nghi "Bạn hay đọc gì?"
            p "...Documentation."
            nghi "Documentation?"
            p "Vẫn là chữ."
            $ NghiAffinity += 2
        "D. Im lặng ngồi cạnh.":
            n "PLAYER mở laptop, yên lặng ngồi cạnh Nghi."
            pause 0.6
            nghi "Bạn không định nói gì à?"
            p "Tôi sợ làm phiền."
            nghi "Không sao."
            $ NghiAffinity += 1
            $ NghiComfort += 2
    $ ch2_hint_context = None
    $ nghi_expression = "normal"
    nghi "Bạn thân với Ngân à?"
    p "Ừ."
    p "Thân tới mức nó biết tao sắp nói ngu trước cả tao."
    nghi "Có vẻ tiện."
    p "Đôi lúc đáng sợ."
    nghi "Nhưng tốt."
    p "Ừ."
    p "Bạn mới chuyển tới... ổn không?"
    nghi "Chưa quen lắm."
    p "Với trường?"
    nghi "Với mọi người."
    nghi "Tôi không giỏi bắt chuyện."
    p "Ờ."
    p "Tôi cũng không."
    nghi "Bạn nói khá nhiều mà."
    p "Đó là do lỗi hệ thống."
    $ nghi_expression = "soft_smile"
    $ refresh_stage()
    $ NghiAffinity += 2
    $ NghiComfort += 2
    nghi "Bạn đang làm gì vậy?"
    p "Fix bug."
    nghi "Khó không?"
    p "Bug không khó."
    p "Không biết bug ở đâu mới khó."
    nghi "Nghe giống nhiều chuyện khác."
    p "...Sao tự nhiên sâu vậy?"
    menu:
        "Giải thích bug cho Nghi, rồi hỏi ý kiến bạn ấy.":
            p "Bạn muốn thử tìm cùng tôi không?"
            nghi "Tôi không biết code."
            p "Không sao. Tôi giải thích."
            nghi "Ừ. Nhưng chậm thôi."
            $ nghi_expression = "soft_smile"
            $ NghiAffinity += 3
            $ NghiComfort += 1
        "Tắt laptop, cùng Nghi tìm tài liệu cho buổi học tới.":
            p "Bug để sau. Bạn cần tìm thêm tài liệu không?"
            nghi "Có. Cảm ơn."
            $ NghiAffinity += 3
            $ NghiComfort += 1
        "Tiếp tục code một mình.":
            p "Để tôi fix nốt đã."
            nghi "Ừ."
    $ ch2_hint_context = None
    jump CH2_06

label CH2_06:
    $ ch2_hint_context = None
    scene sports_morning
    $ set_stage('player', 'minh', 'ngan', 'nghi', 'pe', visual=('player', 'minh', 'pe'))
    with fade
    centered "NGÀY TIẾP THEO — THỂ DỤC"
    $ player_expression = "normal"
    $ nghi_expression = "normal"
    play sound sfx_boss
    call screen boss_title("PHYSICAL EDUCATION", "Class: Game Developer  •  Stamina: NOT FOUND")
    p "...Đây là giảng viên?"
    m "Tao nghĩ đây là raid boss."
    pe "KHỞI ĐỘNG!"
    p "Đúng rồi. Boss thật."
    pe "HÔM NAY CHÚNG TA CHẠY!"
    p "Bao nhiêu vòng ạ?"
    pe "ĐẾN KHI NÀO TÔI THẤY Ý CHÍ!"
    p "Có option nộp ý chí dạng PDF không thầy?"
    pe "CHẠY!"
    $ set_shot('player', 'ngan')
    ngan "Chậm thế?"
    p "Tao là Game Developer."
    ngan "Thì?"
    p "Class tao không có stamina."
    $ set_shot('player', 'ngan', 'nghi')
    menu:
        "A. Cố chạy cạnh Nghi.":
            $ ch2_sports_choice = "A"
            $ player_expression = "exhausted"
            $ set_shot('player', 'nghi')
            nghi "Bạn ổn chứ?"
            p "Rất ổn."
            nghi "...Không giống lắm."
            $ NghiAffinity += 1
        "B. Chạy đúng sức.":
            $ ch2_sports_choice = "B"
            n "PLAYER giữ nhịp chạy vừa sức."
            $ NghiComfort += 1
        "C. Cố vượt Nghi để gây ấn tượng.":
            $ ch2_sports_choice = "C"
            $ player_expression = "exhausted"
            with hpunch
            $ set_shot('player', 'minh', 'ngan')
            m "Ủa nó chạy đi đâu vậy?"
            ngan "Đi gặp tổ tiên."
            $ NghiAffinity += 1
            $ NghiComfort += -1
        "D. Khi Ngân hụt chân, dừng lại hỏi cô ấy có ổn không.":
            $ ch2_sports_choice = "D"
            $ ngan_expression = "embarrassed"
            p "Ê, ổn không?"
            ngan "Ổn."
            p "Chắc chưa?"
            ngan "Chắc."
            p "Đi chậm thôi."
            ngan "...Ừ."
            $ set_shot('player', 'ngan', 'pe')
            pe "HAI EM KIA!"
            p "Chạy."
            ngan "Chạy."
            $ NganAffinity += 3
            $ NganSpecialFlags += 1
    $ ch2_hint_context = None
    if ch2_sports_choice == "C":
        n "PLAYER tăng tốc. Màn hình trước mắt bắt đầu mất frame."
        with vpunch
    else:
        n "Sau buổi chạy, PLAYER chóng mặt. Cô y tá đưa cậu vào phòng nghỉ."
    jump CH2_07

label CH2_07:
    $ ch2_hint_context = None
    scene infirmary_afternoon
    $ set_stage('player', 'nurse', 'ngan', visual=('player', 'nurse'))
    with fade
    centered "PHÒNG Y TẾ — CHIỀU"
    $ player_expression = "exhausted"
    $ ngan_expression = "normal"
    p "..."
    nurse "Em tỉnh rồi à?"
    p "Em đang ở thiên đường?"
    nurse "Phòng y tế."
    p "À."
    nurse "Nếu đây là thiên đường thì cơ sở vật chất hơi thiếu."
    ngan "Mày chạy có mấy vòng."
    p "Mấy vòng cuối đời."
    $ set_stage("player", "nurse", "ngan", "nghi", visual=("player", "nurse", "nghi"), entrance="rise")
    nghi "Bạn ổn không?"
    nurse "Không cần diễn."
    $ set_shot('player', 'nghi')
    $ ch2_hint_context = 'infirmary'
    menu:
        "A. Ổn. Chỉ hơi xấu hổ thôi.":
            $ player_expression = "embarrassed"
            $ nghi_expression = "soft_smile"
            p "Ổn. Chỉ hơi xấu hổ thôi."
            nghi "Không cần xấu hổ."
            nghi "Ít nhất bạn đã cố."
            p "Đừng động viên. Tôi sẽ tưởng mình có năng lực."
            $ NghiAffinity += 3
            $ NghiComfort += 2
        "B. Chuyện nhỏ.":
            $ nghi_expression = "confused"
            p "Chuyện nhỏ."
            nurse "Huyết áp lúc nãy tụt."
            p "...Chuyện vừa."
            $ NghiComfort += -1
        "C. Tôi cố chạy vì bạn.":
            $ nghi_expression = "confused"
            p "Tôi cố chạy vì bạn."
            pause 0.6
            nghi "...Bạn không cần làm vậy."
            $ NghiAffinity += 1
            $ NghiComfort += -3
        "D. Tôi nghĩ thầy thể dục muốn giết tôi.":
            $ nghi_expression = "happy"
            p "Tôi nghĩ thầy thể dục muốn giết tôi."
            ngan "Không."
            ngan "Thầy muốn mày khỏe."
            p "Cách triển khai hơi cực đoan."
            $ NghiAffinity += 2
            $ NghiComfort += 1
    $ ch2_hint_context = None
    menu:
        "Cảm ơn Nghi đã tới thăm, hỏi bạn ấy muốn nghỉ một lát không.":
            $ player_expression = "empathy"
            p "Cảm ơn bạn tới thăm. Bạn cũng mệt không?"
            nghi "Một chút."
            p "Vậy cứ ngồi nghỉ. Không cần nói gì đâu."
            $ nghi_expression = "soft_smile"
            nghi "Ừ. Thế cũng tốt."
            $ NghiAffinity += 3
            $ NghiComfort += 2
        "Xin lỗi vì câu hỏi quá riêng tư hồi sáng.":
            p "Hồi sáng tôi hỏi hơi vô duyên. Xin lỗi bạn."
            nghi "Ừ. Đừng vội vậy."
            p "Tôi sẽ nhớ."
            $ nghi_expression = "soft_smile"
            $ NghiAffinity += 3
            $ NghiComfort += 2
        "Cố gây ấn tượng thêm.":
            p "Lần sau tôi chạy gấp đôi."
            nurse "Em nghỉ đã."
            $ NghiComfort += -1
    $ ch2_hint_context = None
    n "Nghi chào mọi người rồi trở về lớp."
    $ set_stage("player", "nurse", "ngan", visual=("player", "ngan"))
    ngan "Thấy chưa?"
    p "Thấy gì?"
    ngan "Người ta tới thăm mày."
    p "Có hi vọng?"
    ngan "Có."
    pause 0.6
    ngan "Nếu mày đừng có ngu."
    if NganAffinity >= 4:
        $ ngan_expression = "thinking"
        $ refresh_stage()
        pause 0.6
    menu:
        "Hỏi thăm chân Ngân và cảm ơn vì đã ở lại.":
            $ player_expression = "empathy"
            p "Còn chân mày? Hết đau chưa?"
            ngan "Hết rồi. Lo cho mày trước đi."
            p "Cảm ơn vì ở lại. Không phải chuyện Nghi. Chuyện tao ấy."
            $ ngan_expression = "embarrassed"
            ngan "...Biết rồi."
            $ NganAffinity += 2
            $ NganSpecialFlags += 1
        "Nhờ Ngân xem Nghi đã nhắn gì chưa.":
            p "Nghi có nhắn gì nữa không?"
            $ ngan_expression = "normal"
            ngan "Tự xem đi."
    $ ch2_hint_context = None
    $ set_shot('player', 'nurse')
    nurse "Lần sau đừng cố chứng minh bản thân bằng cách ngất."
    p "Em ghi nhận."
    nurse "Em nói câu đó như chuẩn bị làm lại."
    $ player_expression = "normal"
    $ ngan_expression = "normal"
    jump CH2_08

label CH2_08:
    $ ch2_hint_context = None
    scene philosophy_afternoon
    $ set_stage('player', 'minh', 'ngan', 'nghi', 'philosophy', visual=('player', 'philosophy'))
    with fade
    philosophy "Bạn cuối lớp."
    p "Dạ?"
    philosophy "Nếu chuyện của em hay hơn bài giảng, mời em lên đây giảng."
    p "Dạ bài cô hay hơn."
    philosophy "Cô biết."
    philosophy "Con người có thể đồng thời muốn tiến lại gần một người..."
    philosophy "...và sợ bị chính người đó từ chối hay không?"
    p "Gì?"
    $ set_shot('player', 'minh', 'ngan')
    m "Không có gì."
    ngan "Không có gì hết."
    $ set_shot('player', 'philosophy')
    philosophy "Em kia."
    p "Dạ?"
    philosophy "Có vẻ em hiểu ví dụ."
    p "Em xin quyền không phát biểu."
    philosophy "Không được."
    philosophy "Mâu thuẫn không phải lúc nào cũng cần bị loại bỏ."
    philosophy "Đôi khi chính mâu thuẫn buộc con người phải lựa chọn."
    philosophy "Và lựa chọn khiến con người thay đổi."
    pause 1.0
    $ nghi_expression = "soft_smile"
    $ set_shot('player', 'nghi')
    n "Nghi lặng lẽ nhìn về phía PLAYER."
    jump CH2_09

label CH2_09:
    $ ch2_hint_context = None
    scene campus_day
    $ set_stage('player', 'nghi')
    with fade
    centered "SAU GIỜ HỌC — SÂN TRƯỜNG"
    p "Mọi người hay nghĩ bạn khó gần à?"
    nghi "Có."
    p "Ban đầu tôi cũng nghĩ vậy."
    p "Nhưng giờ thì không."
    nghi "Vì sao?"
    menu:
        "A. Chắc bạn chỉ không biết phải nói gì thôi.":
            $ nghi_expression = "soft_smile"
            p "Chắc bạn chỉ không biết phải nói gì thôi."
            nghi "...Có lẽ."
            p "Tôi hiểu cảm giác đó."
            nghi "Bạn?"
            p "Tôi chỉ giỏi nói linh tinh."
            $ NghiAffinity += 2
            $ NghiComfort += 3
        "B. Tôi thấy bạn bình thường mà.":
            $ nghi_expression = "relaxed"
            p "Tôi thấy bạn bình thường mà."
            nghi "Bình thường?"
            p "Ý tốt."
            nghi "...Cảm ơn."
            $ NghiAffinity += 2
            $ NghiComfort += 1
        "C. Vì bạn dễ thương.":
            $ nghi_expression = "embarrassed"
            p "Vì bạn dễ thương."
            nghi "...Bạn nói thẳng thật."
            $ NghiAffinity += 2
            $ NghiComfort += -1
        "D. Tôi quen rồi.":
            $ nghi_expression = "confused"
            p "Tôi quen rồi."
            nghi "Nghe như tôi là lỗi phần mềm."
            p "Không, không phải ý đó."
    $ ch2_hint_context = None
    jump CH2_10

label CH2_10:
    $ ch2_hint_context = None
    scene canteen_afternoon
    $ set_stage('player', 'ngan')
    with fade
    $ ngan_expression = "happy"
    p "Cho tao?"
    ngan "Ừ."
    p "Sao tốt vậy?"
    ngan "Vì mày đứng nhìn máy bán nước hai phút rồi vẫn chưa mua."
    p "Tao đang suy nghĩ."
    ngan "Mày uống đúng một loại suốt hai năm."
    p "..."
    ngan "Đừng có giả bộ phức tạp."
    p "Cảm ơn."
    p "Mày nghĩ tao có cơ hội không?"
    ngan "Có chứ."
    pause 0.6
    ngan "Nếu mày đừng có ngu."
    p "Câu signature của mày à?"
    ngan "Ừ."
    p "Cảm ơn thật."
    ngan "Vì?"
    p "Bữa giờ giúp tao."
    menu:
        "A. Mày đúng là best wingman.":
            p "Mày đúng là best wingman."
            ngan "Biết vậy trả lương đi."
            $ NganAffinity += 1
        "B. Không có mày chắc tao chết.":
            p "Không có mày chắc tao chết."
            ngan "Dramatic vừa thôi."
            $ NganAffinity += 1
        "C. Mà... dạo này tao toàn nói chuyện với mày về Nghi.":
            $ ngan_expression = "thinking"
            p "Mà... dạo này tao toàn nói chuyện với mày về Nghi."
            ngan "Thì?"
            p "Không biết."
            p "Tự nhiên thấy hơi vô duyên."
            ngan "..."
            ngan "Biết nghĩ vậy là tiến bộ rồi."
            p "Mai tao bao nước."
            ngan "Nhớ đó."
            $ NganAffinity += 3
            $ NganSpecialFlags += 1
        "D. Mai giúp tao tiếp nha.":
            p "Mai giúp tao tiếp nha."
            ngan "...Ừ."
    $ ch2_hint_context = None
    jump CH2_11

label CH2_11:
    $ ch2_hint_context = None
    scene rooftop_afternoon
    $ set_stage('player', 'ngan')
    with fade
    $ player_expression = "embarrassed"
    $ ngan_expression = "normal"
    p "Tao định nói."
    ngan "Nói gì?"
    p "Tỏ tình."
    ngan "Hôm nay?"
    p "Ừ."
    ngan "...Ừ."
    p "‘Ừ’ là sao?"
    ngan "Thì đi nói đi."
    p "Cho tao lời khuyên."
    ngan "Đừng cố nói câu gì hay."
    p "Hả?"
    ngan "Nói thật thôi."
    if NganAffinity >= 7:
        $ ngan_expression = "sad"
        $ refresh_stage()
        pause 0.6
        $ ngan_expression = "normal"
        $ refresh_stage()
    $ NganEndingAvailable = ngan_route_available()
    ngan "Đi tỏ tình à?"
    p "Ừ."
    ngan "Good luck."
    menu:
        "Gọi Ngân lại." if NganEndingAvailable:
            jump CH2_ngan_ending
        "Đợi Nghi trên sân thượng.":
            n "Ngân xuống cầu thang. PLAYER ở lại đợi Nghi."
            $ set_stage("player")
            jump CH2_12

label CH2_12:
    $ ch2_hint_context = None
    scene rooftop_afternoon
    $ set_stage('player', 'nghi')
    with fade
    centered "HOÀNG HÔN"
    $ nghi_expression = "normal"
    nghi "Bạn gọi tôi?"
    p "Ừ."
    nghi "Có chuyện gì sao?"
    stop sound
    $ ch2_hint_context = "confession"
    menu:
        "Tôi thích bạn.":
            $ chapter2_ending = resolve_chapter2(True)
        "Tôi đã làm tất cả vì bạn. Bạn phải hiểu chứ.":
            $ chapter2_ending = resolve_chapter2(False)
    $ ch2_hint_context = None
    if chapter2_ending == "nghi_good":
        jump CH2_nghi_good
    jump CH2_nghi_bad
