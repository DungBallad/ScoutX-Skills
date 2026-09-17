# ScoutX-Skills 🚀

> **Bộ Skills tự động hoá cao cấp dành cho Antigravity & AI Coding Assistants** trong quy trình sáng tạo kịch bản, sản xuất video động HyperFrames và kiểm định chất lượng (QA).

---

## 📦 Danh Sách Skills

### 1. scriptscout-authoring
* **Mục đích**: Tự động chuyển hoá tài liệu/slide bài giảng (PDF, ảnh, văn bản) thành kịch bản video ngắn chuẩn mực.
* **Tính năng nổi bật**:
  - Trích xuất nội dung cốt lõi từ slide bài giảng.
  - Tự động dùng công cụ tìm kiếm web (\search_web\) để đối chiếu, kiểm chứng sự kiện và xác minh độ tin cậy nguồn.
  - Xuất tệp kịch bản định dạng JSON tuân thủ chuẩn \hackathon-kich-ban/1\ và \hackathon-ho-so-nguon/1\.
  - **Quy tắc nghiêm ngặt**: Chuyển hoá toàn bộ số thành chữ đọc (\loi\) giúp mô hình TTS phát âm chuẩn xác, không bị vấp.

### 2. ideo-qa
* **Mục đích**: Công cụ Audit & QA toàn diện cho video sản xuất bằng HyperFrames và mã nguồn HTML/GSAP.
* **5 Trụ cột đánh giá (Quality Matrix)**:
  1. **Cấu trúc mã & HTML**: Xác minh Sub-Compositions modular bọc thẻ \<template>\, định danh ID duy nhất.
  2. **Đồng bộ âm thanh & phụ đề**: Kiểm tra độ lệch thời lượng giữa \fprobe\ và thuộc tính \data-duration\, cảnh báo khoảng lặng và chồng chéo voiceover.
  3. **Thẩm mỹ & Tương phản WCAG AA**: Đảm bảo toàn bộ văn bản đạt độ tương phản chuẩn WCAG AA trên nền tối (Dark Theme).
  4. **Hoạt ảnh & GSAP**: Đảm bảo timeline tất định (\gsap.fromTo\), không chứa vòng lặp vô hạn.
  5. **Thành phẩm video MP4**: Kiểm tra video kết xuất chuẩn 1080p, đầy đủ hình và tiếng.
* **Thực thi nhanh**:
  \\\ash
  python skills/video-qa/scripts/qa_audit.py <duong_dan_project> --output qa-report.md
  \\\

---

## 🛠️ Hướng Dẫn Cài Đặt & Sử Dụng

### Cách 1: Cài đặt cho riêng một dự án (Project-level)
Sao chép thư mục \skills/\ vào thư mục \.agents/skills/\ trong project của bạn:
\\\ash
# Di chuyển vào thư mục dự án
cd /path/to/your/project

# Clone kỹ năng vào thư mục .agents/skills
git clone https://github.com/DungBallad/ScoutX-Skills.git .agents/scoutx-skills
\\\

### Cách 2: Cài đặt Toàn cục (Global - dùng cho tất cả dự án)
Cài đặt trực tiếp vào thư mục cấu hình toàn cục của Antigravity để Agent luôn luôn tự nhận diện ở mọi workspace:

* **Windows**:
  \\\powershell
  git clone https://github.com/DungBallad/ScoutX-Skills.git "C:\Users\Dung\.gemini\config\scoutx-skills"
  \\\
* **macOS / Linux**:
  \\\ash
  git clone https://github.com/DungBallad/ScoutX-Skills.git ~/.gemini/config/scoutx-skills
  \\\

---

## 📄 Bản quyền & Giấy phép
Phát triển bởi **DungBallad** - Được phát hành theo giấy phép MIT.
