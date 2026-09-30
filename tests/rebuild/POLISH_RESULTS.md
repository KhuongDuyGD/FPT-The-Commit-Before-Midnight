# Chapter 1 polish — FPT: The Commit Before Midnight

Phạm vi: nâng cấp Chapter 1 theo `../../../FPT_The_Commit_Before_Midnight_CH1_POLISH_UPDATE_PROMPT.md`. Chapter 2 vẫn tạm ngừng trong `migration/chapter2_paused/`; không build hay package game.

## Đã chỉnh

- 20 expression Main dùng chung tag `player`, mặc định Normal và đổi ở các mốc cảm xúc; fallback Energy chỉ áp dụng tại checkpoint. Stage không làm mới sprite khi focus không đổi.
- `DreamPlace.png` dùng ở ba dream scene với Necrass. Bốn CG được hiển thị trong cảnh tương ứng, ẩn cast khi CG full-screen, và chỉ mở Gallery sau khi người chơi thật sự tới cảnh. Slot chưa mở, gồm Nurse, chỉ hiện `???`.
- Ba thay đổi Energy được chỉ định: bỏ sáng `−10`, chạy nước rút khi dậy muộn `−15`, bỏ trưa `−10`. Không đổi chữ thoại hay choice: audit ghi nhận đúng thứ tự 318 khối thoại và 34 lựa chọn.
- Infirmary có cửa sổ active và ba checkpoint trước PE. Đường tự bào sức chạm Energy 12 sau lớp chiều và khóa Infirmary. Cửa sổ đóng trước PE; Energy 10 hoặc 20 lúc ra về đi Walking Corpse, trừ khi PE Club đã bắt.
- Trust dùng helper tương thích trên dữ liệu affinity cũ; save, load và rollback vẫn chạy.
- Tên game, logo, window icon và main menu cập nhật. Menu chọn một trong năm ảnh từ `persistent.last_played_chapter` với fallback Chapter 1. Chapter 2 chỉ có artwork menu dự phòng, không có runtime Chapter 2.
- GitHub repository đã đổi từ `KhuongDuyGD/fpt-2359-escape-protocol` sang [`KhuongDuyGD/FPT-The-Commit-Before-Midnight`](https://github.com/KhuongDuyGD/FPT-The-Commit-Before-Midnight); `origin` fetch/push dùng URL mới. Thư mục checkout và namespace save cũ được giữ để không phá đường dẫn/dữ liệu người chơi.

## File code chính

- `game/chapters/chapter_01.rpy`
- `game/characters.rpy`, `game/characters/chapter1_cast.rpy`, `game/stage.rpy`
- `game/systems/assets.rpy`, `game/systems/state.rpy`, `game/systems/route.rpy`, `game/systems/affinity.rpy`, `game/systems/gallery.rpy`, `game/systems/navigation.rpy`
- `game/screens/main_menu.rpy`, `game/screens/gallery.rpy`, `game/styles/styles.rpy`, `game/options.rpy`
- `game/chapter1_testcases.rpy`, `tools/verify_chapter1.py`

## Asset mapping thực tế

Tất cả đường dẫn dưới đây nằm trong `game/images/`:

| Nội dung | Đường dẫn |
| --- | --- |
| DreamPlace | `backgrounds/Outside/DreamPlace.png` |
| 20 Main expressions | `characters/Main/{Normal,Sleepy,Annoyed,Smug,Surpised,Thinking,Deadpan,Confused,Nervous,VeryHappy,Panic,GoodMood,Determined,Serious,Embarrassed,Exhaust,Sad,Cry,Empathy,Angry}.png` |
| CG gặp thầy thể dục | `GalleryImage/FirstTimeMeetPhysicalTeacher.png` |
| CG gặp y tá | `GalleryImage/FirstTimeMeetNurse.png` |
| CG ngủ ngon | `GalleryImage/GoodRouteChapter1.png` |
| CG Walking Corpse | `GalleryImage/BadRouteChapter1.png` |
| Menu Chapter 1–5 | `backgrounds/MainMenu/MainMenu1.png` đến `MainMenu5.png` |
| Logo | `backgrounds/GameIcon_Logo/LogoGame.png` |
| Icon | `backgrounds/GameIcon_Logo/GameIcon.png` |

Tên file `Surpised.png` là chính tả thực tế của asset; mã dùng đúng tên đó, không nhân bản ảnh.

## Kiểm thử

Ren'Py 8.5.3; lint sạch; 21/21 engine testcases và 133/133 assertions đạt. Test gồm Home Safe, Black Alloy Club, Walking Corpse ở phase ra về với Energy 10 và 20, Infirmary cực hạn Energy 12 trước PE, ngưỡng route, CG unlock, menu Chapter 1–5/fallback, save/load, rollback, UI 960×540 đến 1920×1080. Static audit duyệt 25.894 tổ hợp, xác nhận Infirmary tự nhiên đạt được (104 tổ hợp), không thiếu artwork và không có Chapter 2 trong runtime. Font audit có 208 codepoint. Khởi động bình thường dừng ở main menu.

File chứng cứ: `lint.txt`, `engine-tests.txt`, `static-validation.json`, `font-validation.json`, `startup.json` và `screenshots/`. Ảnh `polish-menu-chapter-3.png` xác nhận menu art/logo/control; `polish-gallery-locked.png` xác nhận Gallery khóa không lộ Nurse. Harness `tools/check_rebuild.ps1` chạy trên bản sao tách biệt khỏi save của project gốc.

## Chạy game

Nhấp đúp `Choi-Game.cmd` trong thư mục project. Hoặc mở Ren'Py Launcher, chọn project này và bấm **Launch Project**.
