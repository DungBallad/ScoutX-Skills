---
name: scriptscout-authoring
description: >
  Use this skill when the user provides a slide (PDF/Image/Text) and asks to generate a video script, short video subtitles, or analyze the slide to build a script.
  This skill guides the agent to read the slide, search the web for cross-referencing, and output a valid JSON script conforming to hackathon-kich-ban/1.
---

# ScriptScout Authoring Skill

Kỹ năng này hướng dẫn Agent tự động chuyển đổi thông tin từ tài liệu đầu vào (Slide, PDF, Hình ảnh) thành kịch bản video (schema `hackathon-kich-ban/1`) và hồ sơ trích dẫn (`hackathon-ho-so-nguon/1`).

## Quy Trình Thực Hiện (4 Bước)

### Bước 1: Đọc Dữ Liệu Đầu Vào (Slide)
- Sử dụng công cụ `view_file` hoặc các công cụ phân tích hình ảnh/PDF của bạn để trích xuất văn bản và ý chính từ tài liệu người dùng tải lên.
- Xác định chủ đề (topic), mục tiêu bài học (goal), và đối tượng học (audience) từ tài liệu.

### Bước 2: Tìm Kiếm Mạng & Kiểm Chứng Chéo (Cross-check)
- Sử dụng `search_web` tìm kiếm từ khóa liên quan đến chủ đề để thu thập thêm 1-2 nguồn đáng tin cậy.
- Mục đích: Đạt điều kiện **xác minh chéo >= 2 nguồn** cho các thông tin kỹ thuật, sự kiện, hoặc số liệu quan trọng.

### Bước 3: Lập Hồ Sơ Nguồn (`hoSo`)
Xây dựng block `"hoSo"` chuẩn `hackathon-ho-so-nguon/1`:
- **nguon**: Liệt kê mọi nguồn (Slide và Web).
  - Khai báo `id` (duy nhất), `tieuDe`, `toChuc`, `ngayDang`, `url`.
  - `loai`: "slide" (cho slide) hoặc "tai-lieu-chinh-thuc", "bao-chi", "blog-ca-nhan" (cho nguồn web).
  - `doTinCay`: "cao"/"trung-binh"/"thap", kèm `lyDoTinCay`.
  - `trangThai`: "dang-dung".
  - `ngayLayVe`: Ghi ngày giờ hiện tại.
- **thongTin**: Các ý được trích xuất.
  - `id`, `noiDung`, `loai`, mảng `bangChung` (chứa `nguonId`, `doanTrich` nguyên văn, `viTri`).
  - `soNguonXacNhan`: Đếm số nguồn độc lập (khác `nguonId`) cùng xác nhận nội dung này.
  - `trangThai`: "da-xac-minh" (nếu $\ge 2$ nguồn), "chua-xac-minh" (nếu chỉ 1 nguồn).
  - `moTaMauThuan`: Ghi chú nếu 2 nguồn nói khác nhau.

### Bước 4: Phân Chia Kịch Bản & Viết JSON (`kichBan`)
Thay vì viết toàn bộ slide vào một kịch bản duy nhất, hãy **chia nhỏ bài giảng thành các nội dung lớn** (các topic/chương chính). Với MỖI nội dung lớn, xây dựng một file JSON kịch bản riêng biệt (chuẩn `hackathon-kich-ban/1`). Trong mỗi file JSON:
- `tieuDe`, `mucTieu`: Chỉ tập trung vào nội dung của phần đó.
- Mảng `phan`: chia cấu trúc nhỏ trong nội dung đó.
- Mảng `cau`: Kịch bản chi tiết cho nội dung đó.
  - `n`: Số thứ tự liên tục.
  - `phan`: ID phần tương ứng.
  - `kieu`: "ke", "giang", "nhe", "hoi", "nhan".
  - **`loi` (RẤT QUAN TRỌNG)**: Văn nói tự nhiên. **TUYỆT ĐỐI KHÔNG chứa chữ số** (vd: viết "một trăm hai mươi" thay vì "120"). Nếu không, máy đọc TTS sẽ đọc từng ký tự nghe rất lỗi.
  - `chuTrenManHinh`: Chữ ngắn gọn (tối đa 40 ký tự).
  - `yDoHinh`: Mô tả ý đồ hoạt ảnh/hình minh họa.
  - `nguon`: Mảng ID trỏ về `hoSo.thongTin`. Để mảng rỗng `[]` nếu là câu chuyển ý.

## Hành Động Cuối
- Tạo ra N tệp JSON cho N nội dung lớn, đặt tên theo định dạng `scripts/scriptscout-kich-ban-<ten_chu_de_1>.json`, `scripts/scriptscout-kich-ban-<ten_chu_de_2>.json`,...
- Kiểm tra lại định dạng JSON trước khi báo cáo cho người dùng.
- Gợi ý người dùng chạy bước Render cho từng kịch bản.

---
*Xem cấu trúc chi tiết tại `references/schema-hackathon.md`.*
