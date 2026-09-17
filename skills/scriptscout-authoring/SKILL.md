---
name: scriptscout-authoring
description: >
  Use this skill when the user provides a slide (PDF/Image/Text) and asks to generate a video script, short video subtitles, or analyze the slide to build a script.
  This skill guides the agent to read the slide, search the web for cross-referencing, directly embed discovered citations and scientific evidence into the script dialogue and visual cues, and output valid JSON scripts conforming to hackathon-kich-ban/1.
---

# ScriptScout Authoring Skill (Tích Hợp Dẫn Chứng Khoa Học)

Kỹ năng này hướng dẫn Agent tự động chuyển đổi thông tin từ tài liệu đầu vào (Slide, PDF, Hình ảnh) thành kịch bản video (schema `hackathon-kich-ban/1`) và hồ sơ trích dẫn (`hackathon-ho-so-nguon/1`), **bắt buộc đưa trực tiếp các dẫn chứng khoa học tìm được vào nội dung lời thoại và thẻ trích dẫn nguồn trên video**.

---

## 🎯 NGUYÊN TẮC CỐT LÕI: ĐƯA DẪN CHỨNG TÌM ĐƯỢC VÀO KỊCH BẢN

> [!IMPORTANT]
> **Không chỉ liên kết mã ID trừu tượng (`"nguon": ["tt-1"]`), kịch bản BẮT BUỘC phải đưa trực tiếp các bằng chứng và trích dẫn khoa học tìm được vào:**
> 1. **Lời thoại voiceover (`loi`)**: Lồng ghép tự nhiên tên tác giả, tên công trình nghiên cứu, hội nghị khoa học hoặc số liệu đối chiếu chéo (chuyển 100% chữ số thành chữ viết).
>    - *Ví dụ mẫu*: Thay vì nói chung chung *"Năm 2017 Transformer ra đời"*, hãy viết: *"Theo bài báo khoa học kinh điển 'Attention Is All You Need' của các nhà nghiên cứu Google công bố tại hội nghị Niu-Ríp năm hai nghìn không trăm mười bảy..."*.
> 2. **Gợi ý hiển thị nguồn (`goiYHienNguon`)**: Bắt buộc ghi rõ nhãn trích dẫn học thuật hoàn chỉnh: `Tác giả (Năm), "Tên bài báo / Nghiên cứu", Hội nghị / Tạp chí · DOI/URL`.
> 3. **Chữ trên màn hình (`chuTrenManHinh`) & Ý đồ hình (`yDoHinh`)**: Thể hiện trực tiếp tên bài báo, logo tổ chức nghiên cứu hoặc biểu đồ số liệu chứng minh.

---

## Quy Trình Thực Hiện (4 Bước)

### Bước 1: Đọc Dữ Liệu Đầu Vào (Slide)
- Sử dụng công cụ `view_file` hoặc các công cụ phân tích hình ảnh/PDF để trích xuất văn bản và ý chính từ tài liệu người dùng tải lên.
- Xác định chủ đề (topic), mục tiêu bài học (goal), và đối tượng học (audience) từ tài liệu.

### Bước 2: Tìm Kiếm Mạng & Kiểm Chứng Chéo (Cross-check)
- Sử dụng `search_web` tìm kiếm từ khóa liên quan đến chủ đề để thu thập thêm 1-2 nguồn đáng tin cậy.
- Thu thập đầy đủ siêu dữ liệu (metadata): Tên tác giả, Tên bài báo gốc, Năm công bố, Hội nghị / Tạp chí xuất bản (CVPR, NeurIPS, ICML, Nature, arXiv...), DOI/URL chính thức.
- Mục đích: Đạt điều kiện **xác minh chéo >= 2 nguồn** cho các thông tin kỹ thuật, sự kiện, hoặc số liệu quan trọng.

### Bước 3: Lập Hồ Sơ Nguồn (`hoSo`)
Xây dựng block `"hoSo"` chuẩn `hackathon-ho-so-nguon/1`:
- **nguon**: Liệt kê mọi nguồn (Slide và Web).
  - Khai báo `id` (duy nhất), `tieuDe`, `toChuc`, `ngayDang`, `url`.
  - `loai`: "slide" (cho slide) hoặc "tai-lieu-chinh-thuc", "bai-bao-khoa-hoc", "bao-chi", "blog-ca-nhan" (cho nguồn web).
  - `doTinCay`: "cao"/"trung-binh"/"thap", kèm `lyDoTinCay`.
  - `trangThai`: "dang-dung".
  - `ngayLayVe`: Ghi ngày giờ hiện tại.
- **thongTin**: Các ý được trích xuất.
  - `id`, `noiDung`, `loai`, mảng `bangChung` (chứa `nguonId`, `doanTrich` nguyên văn, `viTri`).
  - `soNguonXacNhan`: Đếm số nguồn độc lập (khác `nguonId`) cùng xác nhận nội dung này.
  - `trangThai`: "da-xac-minh" (nếu $\ge 2$ nguồn), "chua-xac-minh" (nếu chỉ 1 nguồn).
  - `moTaMauThuan`: Ghi chú nếu 2 nguồn nói khác nhau.

### Bước 4: Phân Chia Kịch Bản & Viết JSON Có Chứa Dẫn Chứng (`kichBan`)
Chia nhỏ bài giảng thành các nội dung lớn (các topic/chương chính). Với MỖI nội dung lớn, xây dựng một file JSON kịch bản riêng biệt (chuẩn `hackathon-kich-ban/1`). Trong mỗi file JSON:
- `tieuDe`, `mucTieu`: Tập trung vào nội dung của phần đó.
- Mảng `phan`: chia cấu trúc nhỏ trong nội dung đó.
- Mảng `cau`: Kịch bản chi tiết cho nội dung đó.
  - `n`: Số thứ tự liên tục.
  - `phan`: ID phần tương ứng.
  - `kieu`: "ke", "giang", "nhe", "hoi", "nhan".
  - **`loi` (RẤT QUAN TRỌNG)**: Văn nói tự nhiên. **TUYỆT ĐỐI KHÔNG chứa chữ số** (vd: viết "hai nghìn không trăm mười bảy" thay vì "2017"). **Phải lồng ghép tên tác giả / công trình / số liệu dẫn chứng cụ thể**.
  - `chuTrenManHinh`: Chữ ngắn gọn (tối đa 40 ký tự), thể hiện trọng tâm kiến thức và tên công trình/năm.
  - `yDoHinh`: Mô tả hình ảnh minh họa, chỉ định rõ đồ họa xuất hiện (sơ đồ, trích dẫn bài báo, tài liệu gốc).
  - **`goiYHienNguon` (BẮT BUỘC KHI CÓ NGUỒN)**: Nhãn trích dẫn học thuật chi tiết (vd: `"Deng, J. et al. (2009), 'ImageNet', CVPR · doi.org/10.1109/CVPR.2009.5206848"`).
  - `nguon`: Mảng ID trỏ về `hoSo.thongTin`. Để mảng rỗng `[]` nếu là câu nối/chuyển ý.

---

## Hành Động Cuối
- Tạo ra N tệp JSON cho N nội dung lớn, đặt tên theo định dạng `scripts/scriptscout-kich-ban-<ten_chu_de_1>.json`, `scripts/scriptscout-kich-ban-<ten_chu_de_2>.json`,...
- Kiểm tra lại định dạng JSON: đảm bảo mọi câu có nguồn đều có đầy đủ dẫn chứng trong `loi` và trường `goiYHienNguon`.
- Gợi ý người dùng chạy bước Render cho từng kịch bản.

---
*Xem cấu trúc chi tiết tại `references/schema-hackathon.md`.*
