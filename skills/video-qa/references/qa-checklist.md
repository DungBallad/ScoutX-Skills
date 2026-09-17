# HyperFrames QA Inspection Checklist

Bảng kiểm tra chất lượng toàn diện dành cho video và mã nguồn HTML/GSAP tạo bởi HyperFrames.

---

## 1. Cấu Trúc HTML & HyperFrames Contract
- [ ] **Root Element**: `<div id="root">` có đầy đủ `data-duration`, `data-width="1920"`, `data-height="1080"`.
- [ ] **Sub-Compositions**:
  - Toàn bộ nội dung trong `compositions/*.html` được bọc trọn trong `<template>`.
  - Bộ chọn CSS cho container gốc là `#root`.
  - Có khai báo `data-composition-id` khớp giữa file mount và file nguồn.
- [ ] **Clip Lifecycle**:
  - Mọi phần tử có `class="clip"` phải có `id` duy nhất.
  - Không tự ý điều khiển CSS `visibility`, `display`, hoặc `autoAlpha` trên `.clip` vì HyperFrames độc quyền quản lý chu kỳ sống của clip.

---

## 2. Đồng Bộ Âm Thanh & Phụ Đề (Audio & Captions)
- [ ] **Thời lượng Audio (`data-duration`)**:
  - Giá trị `data-duration` của thẻ `<audio>` phải khớp tuyệt đối với thời lượng tệp mp3 thực tế (sai số $\le 0.05s$ đo bằng `ffprobe`).
- [ ] **Tránh Xung Đột (No Audio Overlap)**:
  - Các đoạn voiceover nối tiếp nhau không được bắt đầu trước khi đoạn trước kết thúc.
- [ ] **Khoảng Lặng (Pacing & Gaps)**:
  - Khoảng lặng giữa các câu thoại nên dao động từ `0.4s` đến `1.2s`. Khoảng trống $> 2.0s$ mà không có chuyển động thị giác sẽ gây cảm giác chùng nhịp.
- [ ] **Khớp Phụ Đề (Subtitle Sync)**:
  - Thời điểm bắt đầu của từng câu thoại trên Live Caption Bar phải khớp với `data-start` của đoạn voiceover tương ứng.

---

## 3. Hoạt Ảnh GSAP & Tính Tất Định (Deterministic Motion)
- [ ] **Đăng Ký Timeline**:
  - Mỗi sub-composition đăng ký timeline vào `window.__timelines["scene-id"]`.
  - Timeline được khởi tạo với `{ paused: true }`.
- [ ] **Không Dùng Vô Hạn (No Infinite Loops)**:
  - Tuyệt đối không dùng `repeat: -1` trong animation video.
- [ ] **Thuộc Tính Chuyển Động An Toàn**:
  - Dùng `gsap.fromTo()` hoặc thiết lập thuộc tính trực tiếp qua `gsap.set()` thay vì kết hợp CSS transform tĩnh và GSAP tweening trên cùng một thuộc tính.

---

## 4. Bố Cục Thị Giác & Vùng An Toàn (Visual & Safe Zones)
- [ ] **Vùng An Toàn Tiêu Đề (Title Safe Area)**:
  - Giữ toàn bộ chữ, nhãn, số liệu nằm trong vùng 90% trung tâm ($1728 \times 972$, lề tối thiểu 96px trái/phải, 54px trên/dưới).
- [ ] **Tương Phản Màu (WCAG AA Contrast)**:
  - Tỷ lệ tương phản giữa chữ và nền tối thiểu $4.5:1$ cho chữ thông thường và $3.0:1$ cho chữ lớn ($\ge 24px$).
- [ ] **Font Chữ Hệ Thống (Safe Typography)**:
  - Ưu tiên font an toàn: `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif` và `monospace` để tránh lỗi thiếu font khi render serverless/cloud.
- [ ] **Không Tràn Màn Hình (No Overflow/Clipping)**:
  - Text không bị cắt cụt bất thường hoặc tràn ra ngoài khung nhìn 1080p.
