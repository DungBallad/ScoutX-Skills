---
name: video-qa
description: >
  QA and audit HyperFrames video projects and HTML compositions.
  Detect visual defects, audio-caption desync, layout overflow, missing templates,
  WCAG AA contrast violations, and generate comprehensive quality feedback reports with scores.
  Use whenever asked to QA, audit, inspect, review, or evaluate a generated video or HTML composition.
---

# Video & HTML QA Skill

Skill này cung cấp quy trình và công cụ tự động để **kiểm tra chất lượng (QA)** toàn diện cho video và mã nguồn HTML/GSAP tạo bởi HyperFrames, phát hiện lỗi hiển thị, lệch đồng bộ âm thanh - hình ảnh và xuất báo cáo phản hồi (Feedback) chuyên sâu.

---

## 1. Khi Nào Kích Hoạt Skill Này?
- Khi người dùng yêu cầu: *"QA lại video"*, *"Kiểm tra lỗi hiển thị trong file HTML"*, *"Đánh giá chất lượng video vừa tạo"*, *"Review sản phẩm"*, *"Tìm lỗi desync audio hoặc phụ đề"*.
- Sau khi hoàn thành một video mới hoặc sau khi thêm voiceover để đảm bảo không có lỗi trước khi bàn giao.

---

## 2. Quy Trình QA 3 Bước

### Bước 1: Chạy Công Cụ Kiểm Tra Tự Động (`qa_audit.py`)
Chạy script kiểm tra tự động tích hợp sẵn trong skill:
```bash
python .agents/skills/video-qa/scripts/qa_audit.py . --snapshots --output qa-report.md
```

Công cụ sẽ tự động rà soát:
1. **Cấu trúc HTML & Sub-Compositions**:
   - Kiểm tra xem mọi file trong `compositions/*.html` có được bọc trong thẻ `<template>` hay không.
   - Kiểm tra bộ chọn `#root`, khai báo `data-duration`, `data-width`, `data-height`.
   - Quét lỗi GSAP: không dùng `repeat: -1`, không tween `autoAlpha/visibility` trên thẻ `.clip`.
2. **Độ Khớp Âm Thanh & Phụ Đề**:
   - Dùng `ffprobe` đo thời lượng từng tệp mp3 và so sánh với thuộc tính `data-duration` (cảnh báo nếu lệch $> 0.08s$).
   - Phát hiện xung đột đè tiếng giữa các câu thoại kế tiếp.
   - So khớp thời điểm xuất hiện của phụ đề với thời gian bắt đầu của âm thanh voiceover.
3. **Lỗi Runtime & Độ Tương Phản Màu**:
   - Tự động gọi `npx hyperframes check` để xác minh tương phản WCAG AA, phát hiện tràn màn hình (overflow) và lỗi tải tài nguyên.
4. **Kiểm Tra Khung Hình (Visual Snapshots)**:
   - Tự động trích xuất các khung hình tiêu biểu ở các phân cảnh để rà soát bố cục trực quan.

---

### Bước 2: Phân Tích Danh Sách Vấn Đề (Findings)

Khi đọc báo cáo `qa-report.md`, phân loại các vấn đề theo 3 mức độ:
- 🔴 **Lỗi Nghiêm Trọng (Critical)**:
  - Cần sửa ngay lập tức trước khi xuất bản (ví dụ: mất tệp âm thanh, thiếu `<template>`, `repeat: -1`, lỗi runtime).
- 🟡 **Cảnh Báo Cần Tinh Chỉnh (Warning)**:
  - Lệch nhẹ thời lượng giữa HTML và tệp mp3 thực tế.
  - Phụ đề xuất hiện sớm hoặc trễ hơn giọng nói $> 0.5s$.
  - Font chữ thiếu fallback hệ thống an toàn.
- ℹ️ **Gợi Ý Nâng Cấp (Optimization)**:
  - Thêm hiệu ứng vi mô (micro-animations), điều chỉnh khoảng lặng giữa các câu để nhịp điệu sinh động hơn.

---

### Bước 3: Đánh Giá & Phản Hồi Sản Phẩm (Feedback Matrix)

Tổng hợp nhận xét theo 5 trụ cột tiêu chuẩn (thang điểm 10):
1. **Kiến Trúc Mã & Tiêu Chuẩn HyperFrames** (Đạt chuẩn modular, clean code).
2. **Đồng Bộ Âm Thanh & Phụ Đề** (Khớp tiếng, khớp chữ, nhịp dẫn tự nhiên).
3. **Thẩm Mỹ Đồ Họa & Độ Tương Phản** (Dark theme hiện đại, đạt chuẩn WCAG AA).
4. **Hoạt Ảnh & Nhịp Chuyển Động** (Mượt mà, có phân tầng thị giác).
5. **Độ Hoàn Thiện Tệp Xuất Bản** (Video MP4 1080p sắc nét, âm thanh rõ ràng).

Tham khảo chi tiết tiêu chí chấm điểm tại:
- [Bảng Kiểm Tra QA Chi Tiết](./references/qa-checklist.md)
- [Ma Trận Đánh Giá & Phản Hồi](./references/feedback-rubric.md)

---

## 3. Các Lệnh Khắc Phục Nhanh Thường Dùng

- **Xem trực quan trên trình duyệt (Studio Preview)**:
  ```bash
  npx hyperframes preview --background
  ```
- **Chụp ảnh kiểm tra các mốc thời gian cụ thể**:
  ```bash
  npx hyperframes snapshot . --at 5,15,30,45 --no-end
  ```
- **Xuất video hoàn chỉnh sau khi chỉnh sửa**:
  ```bash
  npx hyperframes render -o <ten_video>.mp4
  ```
