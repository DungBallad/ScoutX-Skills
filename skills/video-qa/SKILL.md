---
name: video-qa
description: >
  QA and audit HyperFrames video projects and HTML compositions using an independent evaluator model.
  Enforces Dual-Model Separation: the QA model MUST be different from the authoring/generator model.
  Detects visual defects, audio-caption desync, layout overflow, missing templates,
  WCAG AA contrast violations, and generates comprehensive quality feedback reports with scores.
  Use whenever asked to QA, audit, inspect, review, or evaluate a generated video or HTML composition.
---

# Video & HTML QA Skill (Dual-Model Architecture)

Skill này cung cấp quy trình và công cụ tự động để **kiểm tra chất lượng (QA)** toàn diện cho video và mã nguồn HTML/GSAP tạo bởi HyperFrames, phát hiện lỗi hiển thị, lệch đồng bộ âm thanh - hình ảnh và xuất báo cáo phản hồi (Feedback) chuyên sâu.

---

## ⚠️ NGUYÊN TẮC BẮT BUỘC: PHÂN TÁCH MÔ HÌNH ĐỘC LẬP (DUAL-MODEL SEPARATION)

> [!IMPORTANT]
> **Mô hình thực hiện thẩm định QA BẮT BUỘC phải là một mô hình KHÁC BIỆT với mô hình đã tạo kịch bản và sinh video.**

### Vì sao cần 2 mô hình độc lập?
1. **Triệt tiêu Thiên kiến Xác nhận (Confirmation Bias)**: Mô hình tự sinh sản phẩm sẽ có xu hướng bỏ qua các lỗi logic, ngộ nhận hoặc điểm mù do chính mình tạo ra.
2. **Tiêu chuẩn Trọng tài Độc lập (LLM-as-a-Judge)**: Đánh giá kịch bản văn phong tiếng Việt, cấu trúc câu thoại, và thẩm mỹ đồ họa cần cái nhìn phản biện khắt khe từ một kiến trúc AI độc lập.

### Ma Trận Phân Bổ Mô Hình (Counter-Model Matrix):

| Model Tạo Kịch Bản & Video (Generator) | Model Thẩm Định QA Bắt Buộc (Reviewer / Judge) |
|:---|:---|
| **Google Gemini** *(Gemini 3.8 Flash, Gemini 2.5 Pro)* | **Anthropic Claude** *(Claude 3.7 / 3.5 Sonnet)* hoặc **OpenAI** *(GPT-4o / GPT-4.5 / o1)* |
| **Anthropic Claude** *(Claude 3.5 Sonnet, Claude 3.7)* | **OpenAI** *(GPT-4o)* hoặc **Google Gemini** *(Gemini 2.5 Pro / Flash)* |
| **OpenAI** *(GPT-4o, GPT-4.5, o3-mini)* | **Anthropic Claude** *(Claude 3.5 Sonnet)* hoặc **Google Gemini** *(Gemini 2.5 Pro)* |
| **Mã Nguồn Mở** *(DeepSeek R1/V3, Qwen 2.5)* | **Frontier Model** *(Claude Sonnet, GPT-4o, hoặc Gemini Pro)* |

---

## 1. Khi Nào Kích Hoạt Skill Này?
- Khi người dùng yêu cầu: *"QA lại video"*, *"Kiểm tra lỗi hiển thị trong file HTML"*, *"Đánh giá chất lượng video vừa tạo"*, *"Review sản phẩm"*, *"Tìm lỗi desync audio hoặc phụ đề"*.
- Sau khi hoàn thành một video mới hoặc sau khi thêm voiceover để đảm bảo không có lỗi trước khi bàn giao.
- **Trước khi chạy QA**: Luôn xác định rõ:
  - Model nào đã tạo kịch bản / video (`--generator-model`).
  - Chỉ định model đối trọng độc lập để thực hiện QA (`--qa-model`).

---

## 2. Quy Trình QA 3 Bước

### Bước 1: Chạy Công Cụ Kiểm Tra Tự Động (`qa_audit.py`)
Chạy script kiểm tra với thông số khai báo rõ ràng 2 mô hình độc lập:
```bash
python .agents/scoutx-skills/skills/video-qa/scripts/qa_audit.py . \
  --generator-model "gemini-3.8-flash" \
  --qa-model "claude-3-7-sonnet" \
  --output qa-report.md
```

Công cụ sẽ tự động rà soát:
1. **Xác thực Nguyên tắc Dual-Model**:
   - Đối chiếu tên `generator-model` và `qa-model`.
   - Nếu phát hiện trùng họ mô hình (ví dụ cùng là Gemini hoặc cùng là OpenAI), script sẽ kích hoạt cảnh báo nghiêm trọng `[DUAL_MODEL_VIOLATION]`.
2. **Cấu trúc HTML & Sub-Compositions**:
   - Kiểm tra xem mọi file trong `compositions/*.html` có được bọc trong thẻ `<template>` hay không.
   - Kiểm tra bộ chọn `#root`, khai báo `data-duration`, `data-width`, `data-height`.
   - Quét lỗi GSAP: không dùng `repeat: -1`, không tween `autoAlpha/visibility` trên thẻ `.clip`.
3. **Độ Khớp Âm Thanh & Phụ Đề**:
   - Dùng `ffprobe` đo thời lượng từng tệp mp3 và so sánh với thuộc tính `data-duration` (cảnh báo nếu lệch $> 0.08s$).
   - Phát hiện xung đột đè tiếng giữa các câu thoại kế tiếp.
   - So khớp thời điểm xuất hiện của phụ đề với thời gian bắt đầu của âm thanh voiceover.
4. **Lỗi Runtime & Độ Tương Phản Màu**:
   - Tự động gọi `npx hyperframes check` để xác minh tương phản WCAG AA, phát hiện tràn màn hình (overflow) và lỗi tải tài nguyên.
5. **Kiểm Tra Khung Hình (Visual Snapshots)**:
   - Tự động trích xuất các khung hình tiêu biểu ở các phân cảnh để rà soát bố cục trực quan.

---

### Bước 2: Phân Tích Danh Sách Vấn Đề (Findings)

Khi đọc báo cáo `qa-report.md`, phân loại các vấn đề theo 3 mức độ:
- 🔴 **Lỗi Nghiêm Trọng (Critical)**:
  - Vi phạm nguyên tắc Dual-Model Separation (dùng cùng model để tự chấm).
  - Lỗi cấu trúc: mất tệp âm thanh, thiếu `<template>`, `repeat: -1`, lỗi runtime.
- 🟡 **Cảnh Báo Cần Tinh Chỉnh (Warning)**:
  - Lệch nhẹ thời lượng giữa HTML và tệp mp3 thực tế.
  - Phụ đề xuất hiện sớm hoặc trễ hơn giọng nói $> 0.5s$.
  - Font chữ thiếu fallback hệ thống an toàn.
- ℹ️ **Gợi Ý Nâng Cấp (Optimization)**:
  - Thêm hiệu ứng vi mô (micro-animations), điều chỉnh khoảng lặng giữa các câu để nhịp điệu sinh động hơn.

---

### Bước 3: Đánh Giá & Phản Hồi Sản Phẩm Độc Lập (Independent Feedback Matrix)

Model QA độc lập tổng hợp nhận xét theo 5 trụ cột tiêu chuẩn (thang điểm 10):
1. **Kiến Trúc Mã & Tiêu Chuẩn HyperFrames** (Đạt chuẩn modular, clean code).
2. **Đồng Bộ Âm Thanh & Phụ Đề** (Khớp tiếng, khớp chữ, nhịp dẫn tự nhiên).
3. **Thẩm Mỹ Đồ Họa & Độ Tương Phản** (Tuân thủ chuẩn VinUni Academic Light Theme: nền sáng, kicker đỏ #c5221f, tiêu đề navy #0c2340, thẻ ice-blue #f0f6fc; tuyệt đối KHÔNG chứa Emoji hệ điều hành, dùng đồ họa kỹ thuật/SVG/chỉ số tinh tế; đạt 100% chuẩn tương phản WCAG AA).
4. **Hoạt Ảnh & Nhịp Chuyển Động** (Mượt mà, có phân tầng thị giác, thời gian lưu mắt hợp lý).
5. **Độ Hoàn Thiện Tệp Xuất Bản** (Video MP4 1080p sắc nét, âm thanh rõ ràng).

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
