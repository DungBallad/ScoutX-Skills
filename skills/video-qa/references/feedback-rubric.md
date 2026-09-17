# Video Production Feedback & Evaluation Rubric

Ma trận đánh giá và tiêu chí phản hồi chất lượng video giáo dục & công nghệ.

---

## Thang Điểm 5 Trụ Cột (Tối đa 10 điểm mỗi trụ cột)

### 1. Kiến Trúc Mã Nguồn & Tiêu Chuẩn HyperFrames (Structure & Standards)
- **10 điểm**: Cấu trúc modular sub-compositions hoàn hảo, bọc trọn `<template>`, không có lỗi lint, khai báo đầy đủ kích thước và id.
- **7-9 điểm**: Cấu trúc tốt, có thể thiếu một vài tối ưu nhỏ về selector hoặc id.
- **< 7 điểm**: Thiếu bọc template, xung đột id, hoặc vi phạm quy tắc vòng đời clip của HyperFrames.

### 2. Âm Thanh & Tính Đồng Bộ (Audio & Sync)
- **10 điểm**: Voiceover trong trẻo, khớp 100% với phụ đề hiển thị, thời lượng tệp khớp `data-duration` tuyệt đối, nhịp điệu tự nhiên.
- **7-9 điểm**: Lệch nhẹ (< 0.2s) giữa phụ đề và tiếng nói, hoặc khoảng lặng giữa các câu hơi dài.
- **< 7 điểm**: Tiếng bị cắt đứt giữa chừng, câu thoại bị chồng lấn, hoặc âm thanh bị lệch pha rõ rệt so với hình ảnh.

### 3. Thẩm Mỹ Đồ Họa & Độ Tương Phản (Aesthetics & Contrast)
- **10 điểm**: Phong cách Cyber/Modern Tech ấn tượng, Dark Theme hài hòa, đạt 100% WCAG AA, hiệu ứng Glassmorphism và ánh sáng nổi bật.
- **7-9 điểm**: Bố cục rõ ràng, dễ nhìn, màu sắc đồng bộ nhưng còn ít điểm nhấn thị giác (micro-visuals).
- **< 7 điểm**: Tương phản kém (chữ chìm vào nền), màu sắc lộn xộn, bố cục dồn cục hoặc sát mép màn hình.

### 4. Hoạt Ảnh & Nhịp Chuyển Động (Motion & Pacing)
- **10 điểm**: Chuyển động mượt mà bằng GSAP eases (`power2.out`, `back.out`), phân tầng logic theo lời dẫn, chuyển cảnh tự nhiên không đột ngột.
- **7-9 điểm**: Hoạt ảnh đầy đủ nhưng nhịp còn đều đều, thiếu điểm nhấn bất ngờ hoặc thời gian dừng hình hơi ngắn/dài.
- **< 7 điểm**: Hoạt ảnh bị giật (jank), dùng vòng lặp vô hạn `repeat: -1`, hoặc các đối tượng nhảy đột ngột vào khung hình.

### 5. Khả Năng Sẵn Sàng Xuất Bản (Production Readiness)
- **10 điểm**: Video MP4 1080p sắc nét, dung lượng tối ưu, âm thanh nổi, không có lỗi render.
- **7-9 điểm**: Video render thành công nhưng thời lượng thực tế hơi lệch so với kịch bản gốc.
- **< 7 điểm**: Chưa render được tệp video hoặc video bị lỗi hình/tiếng.
