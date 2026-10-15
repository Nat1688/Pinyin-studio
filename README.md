# Pinyin Studio — GitHub Pages

Website luyện phát âm Pinyin, gồm 406 ô âm tiết và nút nghe 4 thanh điệu. Tất cả giao diện và JS ở `index.html`; không cần build, Node.js, Python hay VPS để chạy online.

## Đăng lên GitHub Pages

1. Tạo repository **Public** tên `pinyin-studio` trên GitHub (không khởi tạo README hay .gitignore từ giao diện GitHub nếu sẽ đẩy toàn bộ thư mục này bằng Git).
2. Tại thư mục đã giải nén (chứa `index.html`) chạy:

```bash
git init
git branch -M main
git add .
git commit -m "Initial Pinyin Studio GitHub Pages"
git remote add origin https://github.com/Nat1688/pinyin-studio.git
git push -u origin main
```

3. Mở repo trên GitHub → **Settings** → **Pages** → phần Build and deployment chọn **Deploy from a branch** → **main** → **/(root)** → **Save**.
4. Khi GitHub Pages xuất bản xong, đường dẫn sẽ có dạng: `https://nat1688.github.io/pinyin-studio/`. Người xem không cần đăng nhập GitHub.

Nếu GitHub username khác `Nat1688` hoặc repo không tên `pinyin-studio`, hãy sửa URL ở lệnh `git remote add origin` và URL website tương ứng.

## Hoạt động âm thanh

Trang **không phân phối file MP3** trong repository này. Khi người dùng nhấn, trình duyệt thử đường dẫn MP3 công khai đến `raw.githubusercontent.com/qhmusiccorner/Chinese-HSK/main/HSK1/fullpinyinwithtones/`, rồi CDN dự phòng. Nếu không tải được sẽ thử `audio/` cục bộ (nếu có) và cuối cùng thử giọng đọc TTS nếu trình duyệt có hỗ trợ. Chất lượng âm thanh và tính sẵn có phụ thuộc vào nguồn bên ngoài.

Quy ước: `ü` → `v`; `lü3` tải `lv3.mp3`. Bộ nguồn có 1.618 MP3; bảng gồm 406 ô âm tiết và 14 tổ hợp thanh không có bản ghi, những trường hợp này dùng TTS.

### Dùng MP3 offline trên máy cá nhân

Trên máy của bạn, chạy `python download_audio.py` để tải vào `audio/`, sau đó mở file `index.html` trực tiếp bằng trình duyệt. Thư mục `audio/` được `.gitignore` bỏ qua khi push.

## Bản quyền / quyền tái sử dụng

- Giao diện HTML/JS được xây dựng độc lập, không sao chép mã nguồn website tham khảo.
- MP3 từ [qhmusiccorner/Chinese-HSK](https://github.com/qhmusiccorner/Chinese-HSK/tree/main/HSK1/fullpinyinwithtones) **chưa xác nhận được giấy phép**. Repository công khai KHÔNG đồng nghĩa cho phép sử dụng lại; cần xin phép tác giả trước khi dùng nguồn này cho website công khai (kể cả liên kết phát trực tiếp). Nếu không được phép, hãy thay nguồn bằng bản ghi của bạn hoặc nguồn có license phù hợp.
- Các bản ghi âm từ bên thứ ba không nằm trong gói phát hành này.

## Tệp

- `index.html`: website, tự chạy.
- `.nojekyll`: để Pages xuất bản HTML tĩnh không qua Jekyll.
- `.gitignore`: tránh push MP3 tải về và tệp phát sinh.
- `download_audio.py`: công cụ tải MP3 cho sử dụng cá nhân sau khi kiểm tra quyền sử dụng.
