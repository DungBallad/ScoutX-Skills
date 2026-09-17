# Quy Trình Xây Dựng Video HyperFrames Từ Kịch Bản (Schema: hackathon-kich-ban/1)

Tài liệu này ghi nhớ toàn bộ quy trình chuẩn để tự động chuyển hóa kịch bản JSON (`hackathon-kich-ban/1`) thành video đồ họa chuyển động chất lượng cao (16:9 1920x1080) bằng HyperFrames và GSAP.

---

## 1. Cấu Trúc Kịch Bản Đầu Vào (`hackathon-kich-ban/1`)

Kịch bản JSON có định dạng:
```json
{
  "schema": "hackathon-kich-ban/1",
  "tieuDe": "Tiêu đề video",
  "mucTieu": "Mục tiêu truyền tải",
  "phan": [ { "so": 1, "ten": "Tên phần" } ],
  "cau": [
    {
      "n": 1,
      "phan": 1,
      "kieu": "ke | giang",
      "loi": "Lời thoại dẫn chuyện / voiceover",
      "chuTrenManHinh": "Tiêu đề hoặc chữ hiển thị trọng tâm",
      "yDoHinh": "Mô tả hình ảnh hoặc sơ đồ cần minh họa",
      "nguon": [],
      "goiYHienNguon": "Vị trí & nội dung nguồn (nếu có)"
    }
  ]
}
```

---

## 2. Nguyên Tắc Thiết Kế & Cấu Trúc Dự Án (Sub-Compositions)

Để tránh cảnh báo `composition_file_too_large` và dễ bảo trì, **luôn phân chia theo kiến trúc Modular**:

### Thư mục dự án:
```text
├── compositions/
│   ├── scene-1.html     # Sub-composition phân cảnh 1
│   ├── scene-2.html     # Sub-composition phân cảnh 2
│   └── ...
├── snapshots/           # Ảnh snapshot kiểm tra
├── index.html           # Master Host Composition
├── hyperframes.json     # Cấu hình HyperFrames
├── package.json         # Scripts lệnh
└── <output>.mp4         # Video thành phẩm
```

### Quy tắc quan trọng cho Sub-Composition (`compositions/*.html`):
1. Toàn bộ nội dung (`<style>`, `<div id="root">`, `<script>`) **PHẢI** nằm trong thẻ `<template>`.
2. Định kiểu cho root element bằng bộ chọn `#root`, không dùng class.
3. Timeline GSAP đăng ký độc lập:
   ```javascript
   const tl = gsap.timeline({ paused: true });
   // Các tween chuyển động...
   window.__timelines["scene-name"] = tl;
   ```
4. `data-composition-id` trong file sub-comp phải trùng khớp với `data-composition-id` trên thẻ mount ở `index.html`.

### Quy tắc cho File Chủ (`index.html`):
1. Root standalone: `<div id="root" data-composition-id="main" data-start="0" data-duration="<tổng_thời_lượng>" data-width="1920" data-height="1080">`.
2. Nhúng các scene qua:
   ```html
   <div id="scene-1" data-composition-id="scene-1" data-composition-src="compositions/scene-1.html" data-start="0" data-duration="7" data-track-index="0" data-width="1920" data-height="1080"></div>
   ```
3. Giữ nền Persistent Ambient Layer (Cyber Grid / Gradient Orb) và Thanh phụ đề (Live Caption Bar) đồng bộ `loi` và trích dẫn nguồn `goiYHienNguon`.

---

## 3. Quy Chuẩn Kỹ Thuật (Lint & Typography)

- **Typography**: Dùng font hệ thống an toàn để không kích hoạt lỗi `font_family_without_font_face`:
  `font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;` và `monospace`.
- **Motion & GSAP**:
  - Không đặt `transform` ban đầu trong CSS khi tween cùng thuộc tính (dùng `fromTo` hoặc `xPercent`/`yPercent`).
  - Không tween `autoAlpha`, `visibility`, `display` trực tiếp trên phần tử có `class="clip"` (HyperFrames sở hữu vòng đời clip).
  - Không dùng `repeat: -1` vô hạn; mọi hoạt ảnh phải mang tính tất định (deterministic).

---

## 4. Quy Trình Kiểm Tra & Xuất Video (3 Bước Chuẩn)

### Bước 1: Kiểm tra hợp lệ (Check)
```bash
npx hyperframes check
```
Yêu cầu: Đạt 0 error, 0 warning, kiểm tra tương phản WCAG AA đạt 100%.

### Bước 2: Chụp ảnh Snapshot để xác nhận hình ảnh (Snapshots)
```bash
npx hyperframes snapshot . --at <t_scene1>,<t_scene2> --no-end
```
Kiểm tra độ sắc nét, bố cục và tính thẩm mỹ của từng phân cảnh.

### Bước 3: Xuất Video MP4 (Render)
```bash
npx hyperframes render -o <ten_video>.mp4
```
Chạy render đa luồng, tự động xuất video MP4 1080p sắc nét và hoàn chỉnh.

### Bước 4: Đánh Giá & QA Toàn Diện (Skill `video-qa`)
```bash
python .agents/skills/video-qa/scripts/qa_audit.py . --output qa-report.md
```
Tự động quét cấu trúc HTML, kiểm tra độ lệch âm thanh vs phụ đề, xác minh WCAG AA và sinh báo cáo phản hồi (Feedback report) chi tiết.

