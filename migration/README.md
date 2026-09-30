# Migration archive

`legacy_chapter1/`: kịch bản Chapter 1, ending, menu, test và importer cũ đã loại khỏi runtime.
Importer `compile_chapter1_old_source.py.txt` chỉ để tra cứu lịch sử. Tài liệu Markdown rebuild cũ đã đổi định dạng sau khi Chapter 1 hiện tại được tạo; không chạy lại importer này để thay thế kịch bản đang chạy.
`chapter2_paused/`: Chapter 2, state, screen, asset declaration, test và importer được tạm gỡ theo yêu cầu cập nhật sắp tới.

Các file `.rpy.txt`/`.py.txt` không được Ren’Py nạp. Không có script/bytecode của Chapter 2 trong `game/`.
Artwork Chapter 2 được giữ nguyên ở `game/images/`.
Khi cập nhật Chapter 2, hãy tích hợp nó với hệ thống và GUI mới; không chép lại toàn bộ menu/state cũ.

`rebuild_playtest_saves/` (Git bỏ qua): bản sao dữ liệu save/persistent sau lần playtest đầu ghi vào project gốc. Harness hiện chạy hoàn toàn trên bản sao project. Chi tiết trong `tests/rebuild/RESULTS.md`.
