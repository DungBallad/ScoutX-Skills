---
name: scriptscout-authoring
description: >
  Use this skill when the user provides a slide (PDF/Image/Text) and asks to generate a video script, short video subtitles, or analyze the slide to build a script.
  This skill guides the agent to read the slide, search the web for cross-referencing, harvest visual evidence assets (paper covers, charts, web screenshots, slide snips),
  directly embed discovered citations and visual evidence into the script dialogue and visual cues, and output valid JSON scripts conforming to hackathon-kich-ban/1.
---

# ScriptScout Authoring Skill (Tích Hợp Dẫn Chứng & Hình Ảnh Bằng Chứng)

Kỹ năng này hướng dẫn Agent tự động chuyển đổi thông tin từ tài liệu đầu vào (Slide, PDF, Hình ảnh) thành kịch bản video (schema `hackathon-kich-ban/1`) và hồ sơ trích dẫn (`hackathon-ho-so-nguon/1`), **bắt buộc thu thập hình ảnh dẫn chứng trực quan (trang bìa paper, biểu đồ, ảnh chụp web, trang slide) và đưa trực tiếp vào kịch bản để hiển thị trong video**.

---

## 🎯 NGUYÊN TẮC CỐT LÕI: DẪN CHỨNG KHOA HỌC & HÌNH ẢNH TRỰC QUAN

> [!IMPORTANT]
> **Một kịch bản đạt chuẩn Studio không chỉ có lời thoại và ID nguồn, mà BẮT BUỘC phải có:**
> 1. **Hình ảnh dẫn chứng thực tế (`hinhAnhDanChung`)**:
>    - Nếu dẫn chứng từ một **Paper khoa học**: Chụp/tải ảnh trang bìa đầu tiên của Paper (ví dụ: file PDF arXiv hoặc IEEE/NeurIPS) với tiêu đề, tác giả và abstract.
>    - Nếu dẫn chứng từ **Giáo trình / Slide**: Trích xuất ảnh chụp của đúng trang slide gốc từ tài liệu đầu vào.
>    - Nếu dẫn chứng từ **Website / Benchmark / Sản phẩm**: Chụp ảnh màn hình thực tế (web screenshot, leaderboard, biểu đồ thống kê).
>    - Lưu toàn bộ tài sản hình ảnh vào thư mục: `assets/evidence/<ten-dan-chung>.png`.
> 2. **Lời thoại voiceover (`loi`)**: Lồng ghép tự nhiên tên tác giả, tên công trình, hội nghị hoặc số liệu đối chiếu chéo (chuyển 100% chữ số thành chữ viết).
> 3. **Gợi ý hiển thị nguồn (`goiYHienNguon`)**: Ghi rõ nhãn trích dẫn học thuật hoàn chỉnh: `Tác giả (Năm), "Tên bài báo / Nghiên cứu", Hội nghị / Tạp chí · DOI/URL`.

---

## Quy Trình Thực Hiện (5 Bước Chuẩn)

### Bước 1: Đọc Dữ Liệu Đầu Vào (Slide)
- Sử dụng `view_file` hoặc các công cụ phân tích hình ảnh/PDF để trích xuất văn bản, cấu trúc chương mục từ tài liệu.
- Trích xuất sẵn các trang slide tiêu biểu làm tư liệu hình ảnh dẫn chứng gốc vào `assets/evidence/slide-<trang>.png`.

### Bước 2: Tìm Kiếm Mạng & Kiểm Chứng Chéo (Cross-check)
- Tìm kiếm từ khóa liên quan đến chủ đề để thu thập thêm 1-2 nguồn khoa học độc lập.
- Thu thập siêu dữ liệu: Tác giả, Tên bài báo gốc, Năm, Hội nghị/Tạp chí (CVPR, NeurIPS, ICML, arXiv...), DOI/URL.

### Bước 3: Thu Thập Hình Ảnh Bằng Chứng (Visual Evidence Harvesting)
- Tự động thu thập hình ảnh minh họa dẫn chứng lưu vào `assets/evidence/`:
  - Dùng công cụ kết xuất PDF (`fitz` / `playwright`) để chụp trang bìa đầu tiên của bài báo khoa học.
  - Chụp ảnh biểu đồ thống kê, bảng giá hoặc trang web công cụ chính thức.
  - Đặt tên rõ ràng: `paper-<ten_paper>.png`, `chart-<ten_bieu_do>.png`, `web-<ten_trang>.png`.

### Bước 4: Lập Hồ Sơ Nguồn (`hoSo`)
Xây dựng block `"hoSo"` chuẩn `hackathon-ho-so-nguon/1` với đầy đủ nguồn Slide và Web, ghi chú đường dẫn ảnh bằng chứng nếu có.

### Bước 5: Phân Chia Kịch Bản & Viết JSON Kèm Hình Ảnh Dẫn Chứng (`kichBan`)
Chia nhỏ bài giảng thành các nội dung lớn. Với MỖI nội dung lớn, xây dựng một file JSON kịch bản riêng biệt (chuẩn `hackathon-kich-ban/1`). Trong mỗi câu (`cau`):
- `n`: Số thứ tự liên tục.
- `phan`: ID phần tương ứng.
- `kieu`: "ke", "giang", "nhe", "hoi", "nhan".
- **`loi` (RẤT QUAN TRỌNG)**: Văn nói tự nhiên. **TUYỆT ĐỐI KHÔNG chứa chữ số**. Lồng ghép tên tác giả/công trình nghiên cứu.
- `chuTrenManHinh`: Chữ ngắn gọn (tối đa 40 ký tự), thể hiện trọng tâm kiến thức và tên công trình/năm.
- `yDoHinh`: Mô tả hình ảnh và chỉ định hoạt ảnh xuất hiện của khung hình bằng chứng.
- **`hinhAnhDanChung`**: Đường dẫn tệp ảnh dẫn chứng thực tế (vd: `"assets/evidence/paper-imagenet-cvpr2009.png"`).
- **`loaiDanChung`**: `"trang-bia-paper"` | `"anh-chup-web"` | `"bieu-do"` | `"trang-slide"` | `"anh-san-pham"`.
- **`moTaDanChung`**: Mô tả nội dung hình ảnh bằng chứng hiển thị.
- **`goiYHienNguon`**: Nhãn trích dẫn học thuật chi tiết (vd: `"Deng, J. et al. (2009), 'ImageNet', CVPR · doi.org/10.1109/CVPR.2009.5206848"`).
- `nguon`: Mảng ID trỏ về `hoSo.thongTin`.

---

## 🎨 QUY CHUẨN THIẾT KẾ THỊ GIÁC: VINUNI ACADEMIC LIGHT THEME

Mọi kịch bản và composition video khi xây dựng trong bất kỳ môi trường IDE nào (Cursor, Windsurf, VS Code, v.v.) **BẮT BUỘC** áp dụng phong cách thiết kế **VinUni Academic Light Theme** (xem chi tiết tại `references/theme-guidelines.md`):
- **Nền chính**: Nền trắng sáng `#ffffff` / `#f8fafc` kèm lưới kỹ thuật siêu nhẹ `rgba(15, 23, 42, 0.04)`.
- **Thanh thương hiệu đỉnh (Header)**:
  - Trái: Kicker đỏ VinUni `#c5221f` chữ in hoa: `NGÀY 01 · AI, MACHINE LEARNING, GENERATIVE AI & LLM`.
  - Phải: Dấu chấm đỏ tròn + `• VinUni · AI in Action 20K`.
- **Tiêu đề chính**: Xanh Navy học thuật `#0c2340`, sắc nét và trang trọng.
- **Thẻ nội dung (Cards)**: Nền xanh Ice-Blue nhạt `#f0f6fc`, viền xanh sắc nét `#2563eb`, bo góc 12px – 16px.
- **Văn bản nội dung**: Màu than tối `#1e293b` (đảm bảo 100% đạt chuẩn tương phản WCAG AA).
- **Thanh phụ đề nổi (Floating Pill)**: Nền kính trắng sáng `rgba(255, 255, 255, 0.96)`, viền xám mảnh, chữ xanh navy `#0c2340`.
- **Dẫn chứng khoa học**: Tài liệu bài báo nghiên cứu (Paper CVPR, NeurIPS) hiển thị trên nền sáng có viền xanh/vàng thanh lịch, tạo cảm giác tài liệu học thuật thực tế.
- **TUYỆT ĐỐI KHÔNG DÙNG EMOJI**: Không dùng emoji hệ điều hành (🌐, 🧠, 📊, 🎨, ⚡, 💡, 💬...). Thay thế hoàn toàn bằng: Sơ đồ tương tác (Concentric Circles / Diagrams), Chỉ số thập phân `01, 02..`, hoặc Vector SVG Monoline nét mảnh (1.5px – 2px).

---

## Hành Động Cuối
- Kiểm tra lại các file hình ảnh trong `assets/evidence/` đảm bảo tồn tại và sắc nét.
- Đảm bảo các sub-composition video khi dựng sẽ nhúng các ảnh dẫn chứng này qua thẻ `<img>` với hiệu ứng zoom/tilt đẹp mắt.
- Tuân thủ nghiêm ngặt bảng màu VinUni Academic Light Theme khi viết CSS cho sub-compositions.
- Gợi ý người dùng chạy bước Render cho từng kịch bản.

---
*Xem cấu trúc chi tiết tại `references/schema-hackathon.md` và quy chuẩn thẩm mỹ tại `references/theme-guidelines.md`.*
