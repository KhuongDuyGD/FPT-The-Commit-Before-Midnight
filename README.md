# FPT: The Commit Before Midnight

Dự án Ren’Py phát triển Chapter 1 — **Một ngày rất bình thường của sinh viên IT**.
Resolution 1920×1080; cửa sổ và fullscreen do Ren’Py tự scale.
Repository: [KhuongDuyGD/FPT-The-Commit-Before-Midnight](https://github.com/KhuongDuyGD/FPT-The-Commit-Before-Midnight).

## Mở game

**Cách nhanh trên máy này:** mở thư mục project rồi nhấp đúp `Choi-Game.cmd`.
Game vào main menu mới; chọn **New Game** để bắt đầu. File này dùng Ren’Py SDK đã cài trong `%TEMP%` hoặc thư mục do biến `RENPY_SDK` chỉ tới.

Nếu không dùng file đó, mở Ren’Py Launcher 8.5.3 hoặc mới hơn, chọn project ở
`D:\Game_Project\FPTChaosVisualNovel\fpt-2359-escape-protocol` rồi nhấn **Launch Project**.

Có thể chạy trực tiếp từ PowerShell bằng `./launch-game.ps1 -SdkPath 'đường dẫn RenPy SDK'`.
Script tự nhận `$env:RENPY_SDK`, hoặc SDK kiểm thử trong `%TEMP%/fpt-commit-rebuild-sdk/renpy-8.5.3-sdk` nếu có.
Không cần build/package/export.

## Nội dung và hệ thống

Chapter 1 được rebuild từ tài liệu cũ, rồi polish theo `../FPT_The_Commit_Before_Midnight_CH1_POLISH_UPDATE_PROMPT.md`.
Kịch bản đang chạy trong `game/chapters/chapter_01.rpy` là bản chuẩn nội dung: giữ nguyên 318 khối thoại, 34 lựa chọn và các flag. Chỉ ba Energy delta được phép đã đổi.
Importer đời đầu được lưu trong `migration/legacy_chapter1/`; không chạy lại trên tài liệu rebuild cũ đã đổi định dạng vì có thể làm mất thoại nhiều dòng.

Energy bắt đầu 60/100, clamp 0–100. Trust Linh/Ngân là stat ẩn, dùng cùng state với affinity đời đầu để save cũ vẫn tương thích.
Route ưu tiên: **INFIRMARY → BLACK_ALLOY_CLUB → WALKING_CORPSE → HOME_SAFE**.
Infirmary chỉ mở trước encounter thầy thể dục và khóa các route khác khi trigger. Sau thời điểm này, Energy thấp đi Walking Corpse nếu chưa bị PE Club bắt. Mọi playthrough state dùng `default` để hỗ trợ save/load/rollback.

Main menu dùng năm artwork ứng với Chapter 1–5 dựa trên persistent chapter entry; Chapter 2 vẫn tạm đóng. Menu, Gallery, Load, Save, Preferences, History, About dùng action Ren’Py chuẩn.
Continue bị vô hiệu khi chưa có save phù hợp. Textbox luôn cố định dưới màn hình;
choice nằm phía trên, có hover/focus và thao tác chuột/bàn phím.

Click/Enter/Space để tiếp tục; Page Up hoặc Back để rollback; Esc/right click mở game menu.
Quick menu có History, Skip, Auto, Save, Load và Prefs.

## Chapter cũ và save

Chapter 1 cũ không còn runtime path. Bản lưu nằm trong `migration/legacy_chapter1/`.
Theo yêu cầu mới, **Chapter 2 tạm bị gỡ khỏi game**. Bản lưu nằm trong `migration/chapter2_paused/`;
không có nút tiếp tục Chapter 2 hoặc Chapter Select. Artwork Chapter 2 vẫn được giữ.
Các bản lưu mã có đuôi `.rpy.txt`/`.py.txt`, nằm ngoài `game/` nên Ren’Py không nạp.

Thư mục save `FPT2359EscapeProtocol` được giữ cho game và các trường persistent unlock cũ.
Save của kịch bản cũ không thể tải trong bản rebuild vì label cũ đã bị loại bỏ.
Load hiển thị các slot đó là `Previous version save`; Continue chỉ chọn save Chapter 1 mới.
New Game reset state của lượt chơi và giữ persistent unlock.

## Asset và giới hạn

Dùng artwork tại các thư mục mới `Main_Home`, `School_Map`, `Outside`, `MainMenu`, `GameIcon_Logo`, `GalleryImage`, `characters/Main` và các folder cast liên quan. `DreamPlace.png` là nền cả ba dream scene.
20 expression Main dùng một image tag, đổi theo emotional beat. Bốn CG xuất hiện trong story và chỉ unlock trong Gallery khi đã được xem; slot Nurse khóa chỉ hiện `???`.
Logo trong suốt là layer riêng trên menu, icon mới dùng cho cửa sổ game. Không đổi tên, duplicate, tải Internet hoặc sinh artwork mới.
Hai cảnh đường về chưa có hình riêng nên vẫn dùng nền màu an toàn.
Alarm và notification dùng WAV hiện có. Các sound/ambience chưa có file được bỏ qua an toàn.
Font DejaVu Sans và Twemoji có sẵn trong Ren’Py, đủ tiếng Việt và emoji trong nguồn.

**Đường vào Infirmary:** ngủ tiếp `+5`, bỏ ăn sáng `−10`, chạy nước rút `−15`, tự làm lab `−8`, bỏ bữa trưa `−10`, lớp chiều `−10` đưa Energy từ 60 xuống **12** trước khi gặp thầy thể dục. Route vẫn cần Energy ≤15 và chỉ hoạt động khi cửa sổ Infirmary còn mở.

## File chính

- `game/script.rpy`: New Game entry.
- `game/chapters/chapter_01.rpy`: Chapter 1 mới.
- `game/systems/`: state, Energy, Trust/affinity compatibility, route, asset, Gallery unlock, audio, save compatibility, transitions, navigation.
- `game/characters.rpy`, `game/characters/chapter1_cast.rpy`: background, sprite và speaker.
- `game/stage.rpy`: staging, expression, focus, giới hạn ba sprite.
- `game/screens/`: menu động, Gallery, dialogue/choice, HUD, route completion, Save/Load/Preferences/History/About.
- `game/styles/styles.rpy`, `game/options.rpy`: font, style và cấu hình.
- `tools/verify_chapter1.py`: đối chiếu dialogue/choice với bản Chapter 1 đã ghi nhận, kiểm tra ba delta được phép, asset và route.
- `tools/check_rebuild.ps1`: lint và kiểm thử bằng SDK trên bản sao dự án, cách ly save/persistent.

## Kết quả kiểm thử

Ren’Py lint sạch. 21/21 engine tests và 133/133 assertions qua, gồm bốn route,
Infirmary đạt tự nhiên với Energy 12, ngưỡng Walking Corpse sau khi đóng cửa sổ Infirmary,
CG unlock, expression, menu động, replay/reset, Save/Load/Continue, rollback, history, UI và Preferences.
Kiểm tra cửa sổ 960×540, 1280×720, 1024×768 và 1920×1080.
Lần boot bình thường mở main menu, không auto-start, kể cả khi có biến môi trường auto-load.

Báo cáo hiện tại: `tests/rebuild/POLISH_RESULTS.md`, `lint.txt`, `engine-tests.txt`, `static-validation.json`,
`font-validation.json`, `startup.json`; ảnh QA trong `tests/rebuild/screenshots/`.
Để chạy lại: `./tools/check_rebuild.ps1 -SdkPath 'đường dẫn RenPy SDK'`.
Script tạo bản sao trong `tests/rebuild/runner-*`, dùng namespace save riêng và chép ảnh QA về báo cáo.
Không chạy test runner trực tiếp trên project gốc: Ren’Py vẫn có thể ghi vào `game/saves` dù có `--savedir`.

Trong lần kiểm thử đầu, Ren’Py đã ghi save playtest vào `game/saves` của project gốc.
Dữ liệu thư mục đó và bản persistent lúc phát hiện được giữ tại `migration/rebuild_playtest_saves/`.
Gallery Chapter 1 do playtest tạo đã được làm sạch; xem báo cáo rebuild ban đầu trong `tests/rebuild/RESULTS.md` để biết chi tiết.
