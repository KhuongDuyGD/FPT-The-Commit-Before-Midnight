# Three independent Chapter 2 endings. Persistent flags unlock the gallery.


label CH2_nghi_good:
    $ ch2_hint_context = None
    scene rooftop_afternoon
    $ set_stage('player', 'nghi')
    with fade
    $ player_expression = "embarrassed"
    stop sound
    p "Nghi."
    nghi "Ừ?"
    p "Tôi không giỏi nói mấy chuyện này."
    p "Thật ra là... cực kỳ không giỏi."
    p "Nhưng tôi thích bạn."
    pause 0.6
    p "Nếu bạn cần thời gian thì—"
    nghi "Tôi biết."
    $ player_expression = "surprised"
    p "...Hả?"
    $ nghi_expression = "soft_smile"
    nghi "Không khó đoán lắm."
    p "Thế sao bạn không nói?"
    nghi "Tôi muốn xem bao giờ bạn tự nói."
    p "..."
    p "Tôi bị test à?"
    $ nghi_expression = "soft_smile"
    nghi "Có thể."
    $ player_expression = "embarrassed"
    p "Vậy..."
    p "Câu trả lời là?"
    nghi "Ừ."
    p "‘Ừ’?"
    nghi "Tôi cũng thích bạn."
    pause 0.6
    $ player_expression = "very_happy"
    nghi "Cuối tuần này..."
    nghi "Bạn có rảnh không?"
    p "RẢNH."
    nghi "Tôi còn chưa nói đi đâu."
    p "Đi đâu cũng rảnh."
    $ nghi_expression = "happy"
    $ set_stage()
    scene cg_nghi_good with dissolve
    $ finish_chapter2("nghi_good")
    play sound sfx_success
    call screen chapter2_cg("GOOD ENDING", "LOVE PROTOCOL ESTABLISHED")
    stop sound
    scene rooftop_afternoon
    $ set_stage("nghi")
    with fade
    ngan_message "Sao rồi?"
    nghi "Ổn."
    $ set_stage()
    scene canteen_afternoon
    $ ngan_expression = "sad"
    $ set_stage("ngan")
    with dissolve
    n "Ngân gửi một biểu tượng đồng ý, rồi nhìn màn hình thêm một lúc."
    pause 1.0
    $ set_stage()
    scene black with fade
    centered "TO BE CONTINUED IN CHAPTER 3"
    call screen chapter2_end_menu
    return

label CH2_nghi_bad:
    $ ch2_hint_context = None
    scene rooftop_afternoon
    $ set_stage('player', 'nghi')
    with fade
    stop sound
    $ player_expression = "sad"
    p "Nghi."
    nghi "Ừ?"
    p "Tôi thích bạn."
    $ nghi_expression = "sad"
    pause 0.6
    nghi "Xin lỗi."
    nghi "Tôi thật sự quý bạn."
    nghi "Nhưng tôi không nghĩ mình có thể trả lời bạn theo cách bạn mong muốn."
    $ player_expression = "happy"
    p "Ừ."
    p "Không sao."
    nghi "...Xin lỗi."
    p "Thật mà."
    jump CH2_pub

label CH2_pub:
    $ ch2_hint_context = None
    scene nearby_pub_night
    $ set_stage('player', 'minh')
    with fade
    centered "TỐI — QUÁN GẦN TRƯỜNG"
    $ player_expression = "sad"
    m "Uống đi."
    p "Tình yêu là gì?"
    m "Tao không biết."
    p "Cuộc đời là gì?"
    m "Tao càng không biết."
    p "Mày biết gì?"
    m "Mai có deadline."
    pause 0.6
    p "Cho tao thêm chai."
    m "Ờ."
    $ finish_chapter2("nghi_bad")
    play sound sfx_bad
    call screen chapter2_cg("BAD ENDING", "404 — LOVE NOT FOUND")
    call screen chapter2_end_menu
    return

label CH2_ngan_ending:
    $ ch2_hint_context = None
    scene rooftop_afternoon
    $ set_stage('player', 'ngan')
    with fade
    stop sound
    $ player_expression = "empathy"
    p "Ngân."
    ngan "Hử?"
    p "Tao nghĩ tao vừa nhận ra một chuyện."
    ngan "Chuyện gì?"
    p "Bữa giờ tao cứ nghĩ tao đang chạy theo Nghi."
    ngan "Ừ?"
    p "Nhưng người tao muốn kể chuyện mỗi ngày..."
    pause 0.6
    p "Người tao tự nhiên tìm đầu tiên mỗi khi có chuyện..."
    p "Hình như không phải Nghi."
    $ ngan_expression = "confused"
    ngan "...Mày đang nói gì vậy?"
    p "Tao thích mày."
    pause 0.6
    pause 0.8
    $ ngan_expression = "embarrassed"
    ngan "..."
    p "..."
    ngan "..."
    ngan "ĐM."
    p "Đấy không phải response tao mong đợi."
    ngan "Mày cho tao thời gian load được không?!"
    p "Xin lỗi."
    ngan "Đồ ngu."
    $ player_expression = "sad"
    $ ngan_expression = "happy"
    ngan "...Nhưng tao cũng thích mày."
    $ player_expression = "surprised"
    p "Thật?"
    ngan "Không."
    $ player_expression = "sad"
    $ ngan_expression = "big_laugh"
    ngan "Đùa thôi!"
    p "Ngân!"
    $ ngan_expression = "big_laugh"
    $ player_expression = "very_happy"
    ngan "Đi."
    p "Đi đâu?"
    ngan "Đi chơi."
    p "Bây giờ?"
    ngan "Bây giờ."
    p "Tao còn balo—"
    ngan "Có tay còn lại."
    $ set_stage()
    scene cg_ngan with dissolve
    $ finish_chapter2("ngan")
    play sound sfx_success
    call screen chapter2_cg("SECRET ENDING", "YOU WERE NEVER LOST", "Some escape routes don't lead outside.\nSometimes they lead home.")
    centered "ROUTE COMPLETE"
    call screen chapter2_end_menu
    return
