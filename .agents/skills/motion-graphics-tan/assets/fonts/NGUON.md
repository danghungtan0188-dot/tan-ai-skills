# Nguồn font

Montserrat, Inter, Playfair Display, Nunito, VT323, Patrick Hand, Tilt Neon, giấy phép SIL Open Font License 1.1, tải từ Google Fonts ngày 2026-11-02
(bản variable, các bộ chữ `latin`, `latin-ext`, `vietnamese`).

Đặt tên riêng có đuôi ` VN` (`Montserrat VN`, `VT323 VN`...): tên gốc bị HyperFrames thay bằng bộ font đi kèm chỉ có chữ Latin,
khi đó ư, ơ, ự... hiện bằng font khác.

`font-face.json`: các khối `@font-face` theo từng họ font, chép vào `<style>` của thẻ mới. File `.woff2` phải nằm ở
`assets/fonts/` của dự án (`render_mau.py` tự chép).
