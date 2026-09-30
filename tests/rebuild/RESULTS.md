# Chapter 1 rebuild — FPT: The Commit Before Midnight

**Báo cáo lịch sử trước đợt polish Chapter 1.** Các số liệu 17/17, 110/110 và kết luận Infirmary chưa thể đạt bên dưới chỉ mô tả bản rebuild ban đầu. Kết quả hiện tại, gồm Infirmary đạt tự nhiên và 21/21 test, nằm trong [POLISH_RESULTS.md](POLISH_RESULTS.md).

Nguồn: `../../../FPT_The_Commit_Before_Midnight_MASTER_REBUILD_PROMPT.md`.
Yêu cầu bổ sung: tạm gỡ Chapter 2 khỏi game, giữ lại để cập nhật sau.

## Phạm vi

- New Game vào `start → chapter_01`, Energy 60/100.
- Main menu mới, textbox cố định, choice modal, HUD Energy, Preferences, History, About.
- Hệ thống `default` cho state, helper clamp Energy, affinity ẩn, resolver ưu tiên và khóa Infirmary.
- Chapter 1 cũ nằm trong `migration/legacy_chapter1`, đuôi `.rpy.txt`, ngoài runtime.
- Chapter 2 nằm trong `migration/chapter2_paused`, đuôi `.rpy.txt`, ngoài runtime. Artwork giữ nguyên.
- Load/Continue chỉ nhận save có metadata rebuild Chapter 1. Game giữ tên thư mục save hiện có và các trường persistent unlock cũ; lưu ý dữ liệu playtest bên dưới.

## Đối chiếu tĩnh

`tools/verify_chapter1.py` đối chiếu độc lập nguồn Markdown với mã sinh ra:

- 318 khối lời thoại và 34 lựa chọn đúng nguyên văn, đúng thứ tự nhánh.
- 21 thay đổi Energy và 6 thay đổi affinity đúng nguồn.
- Không còn label Chapter 1 cũ, Chapter 2, orphan bytecode hoặc reference menu cũ trong runtime.
- Đủ artwork chính; `FPTUGate.png` được ánh xạ sang `FPTUGateDay.png` đang có trong dự án.

## Giới hạn từ nguồn

Duyệt 25.920 đường lựa chọn: HOME_SAFE 15.241, BLACK_ALLOY_CLUB 10.382, WALKING_CORPSE 297. Energy thấp nhất ở checkpoint nghỉ là 39; thấp nhất cuối ngày là 16. Không thể tự nhiên đạt Infirmary ≤15 với các giá trị nguồn hiện tại. Không đổi giá trị để che mâu thuẫn này. Các test Infirmary đưa Energy thấp vào checkpoint thật, kiểm tra ba tình trạng ăn sáng và khả năng override/lock các route khác.

Fantasy void và hai cảnh đường về chưa có artwork riêng: dùng nền màu an toàn. Alarm và notification dùng WAV đã có; các ambience, door, whistle, shoulder pat, bag drop chưa có file tương ứng nên phát im lặng. Không tải hoặc tạo artwork mới.

## Kiểm thử

Ren'Py 8.5.3; virtual resolution 1920×1080. Lint sạch; 17/17 engine tests và 110/110 assertions qua. Báo cáo lint trong `lint.txt`, kiểm thử engine trong `engine-tests.txt`, khởi động bình thường trong `startup.json`, audit tĩnh trong `static-validation.json`. `font-validation.json` xác nhận đủ cả 208 codepoint dùng trong nguồn, gồm tiếng Việt và emoji.

Test engine chạy trên bản sao project trong `runner-*`, với namespace persistent và thư mục save riêng. Gồm bốn route, ngưỡng 15/16/20/21/30/31, ưu tiên route, khóa Infirmary, lựa chọn cosmetic, replay/reset, Save/Load, Continue, rollback, history và UI ở 960×540, 1280×720, 1024×768, 1920×1080. Kiểm tra ảnh thực tế main menu, choice, thoại dài và Preferences trong `screenshots/`. Lần chạy cuối trả exit code 0 và tự thoát bằng teardown chuẩn của Ren’Py.

## Dữ liệu playtest

Lần kiểm thử đầu dùng `--savedir` trên project gốc. Ren’Py 8.5.3 vẫn ghi bản sao save/persistent vào `game/saves`; do đó cách này không cách ly hoàn toàn dữ liệu người chơi. Đã sửa harness để lint và test đều chạy trên bản sao project, có namespace save riêng.

Toàn bộ `game/saves` tại thời điểm phát hiện đã được chuyển vào `migration/rebuild_playtest_saves/game-local/`. Bản persistent trong AppData lúc đó được sao lưu tại `migration/rebuild_playtest_saves/appdata-persistent-before-cleanup`. Các bản sao này nằm ngoài runtime, được Git bỏ qua. Không có bản chụp trước kiểm thử, nên không khẳng định dữ liệu trước đó còn nguyên từng byte. Chỉ gallery `persistent.chapter1_routes` mới được playtest tạo đã được reset; các trường unlock cũ được giữ. Game hiện không có slot playtest để Continue tự nhận nhầm.

Không build, package hoặc export game.
