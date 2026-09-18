# VinUni Academic Light Theme — Quy Chuẩn Thiết Kế Video & Slide

Tài liệu này định nghĩa hệ thống thiết kế thị giác chuẩn (**Design System**) cho toàn bộ video, slide và sub-composition tạo bởi ScoutX hoặc bất kỳ công cụ IDE / AI Agent nào (Cursor, Windsurf, Claude Code, VS Code, v.v.).

---

## 1. Triết Lý Thiết Kế
- **Phong cách**: Academic Light Theme — Sáng sủa, Hàn lâm, Hiện đại, Chuẩn thương hiệu giáo trình **VinUni · AI in Action**.
- **Mục tiêu**: Video tạo ra phải đem lại cảm giác như một bản chuyển động hóa chuyên nghiệp (motion-graphic extension) của chính bài giảng gốc, tối ưu độ tương phản văn bản theo chuẩn **WCAG AA** và tích hợp tài liệu khoa học tự nhiên nhất.

---

## 🚫 NGUYÊN TẮC BẮT BUỘC: TUYỆT ĐỐI KHÔNG SỬ DỤNG EMOJI (NO EMOJIS)

> [!CAUTION]
> **Tuyệt đối KHÔNG sử dụng ký tự Emoji hệ điều hành (như 🌐, 📊, 🧠, 🎨, ⚡, 💡, 💬, 💻, 🚀) trong toàn bộ video và kịch bản.**
> Việc dùng Emoji khiến sản phẩm mang cảm giác "AI tạo sẵn, chất lượng thấp, thiếu chuyên nghiệp".

### 3 Giải pháp thay thế chuẩn Studio:
1. **Sơ đồ đồ họa / Hình học kỹ thuật (Schematics / Nested Diagrams)**:
   - Thay vì dán icon emoji, vẽ trực tiếp sơ đồ bản chất: vd các vòng tròn đồng tâm lồng nhau (Concentric Circles) cho các tầng bậc AI, đồ thị nơ-ron cho mạng sâu, hoặc luồng mũi tên cho quy trình.
2. **Typography & Chỉ số vi mô (Technical Numbering & Monospace Badges)**:
   - Dùng các số đếm tối giản: `01`, `02`, `03`, `04`, `05` hoặc nhãn rút gọn `[ AI ]`, `[ ML ]`, `[ DL ]`, `[ GEN ]`, `[ LLM ]`.
3. **Biểu tượng Vector SVG Monoline (Đơn sắc, Nét mảnh 1.5px – 2px)**:
   - Nếu cần biểu tượng, chỉ dùng SVG nội tuyến đơn sắc, cùng tông màu nhận diện (`#0c2340`, `#2563eb`, `#c5221f`), không đổ màu gradient sặc sỡ như emoji điện thoại.

---

## 2. Bảng Màu Chuẩn (Color Palette & CSS Variables)

```css
:root {
  /* 1. Nền tổng thể */
  --bg-main: #ffffff;                    /* Nền trắng tinh khiết */
  --bg-canvas: #f8fafc;                  /* Nền phụ slate siêu nhẹ */
  --grid-line: rgba(15, 23, 42, 0.04);   /* Lưới kỹ thuật tinh tế */

  /* 2. Điểm nhấn thương hiệu VinUni (Brand Crimson Red) */
  --brand-red: #c5221f;                  /* Màu đỏ cờ chuẩn VinUni */
  --brand-red-light: rgba(197, 34, 31, 0.08); /* Nền mờ cho badge đỏ */
  --brand-red-border: rgba(197, 34, 31, 0.35); /* Viền cho badge đỏ */

  /* 3. Tiêu đề & Typography Hàn Lâm (Academic Navy) */
  --text-heading: #0c2340;               /* Xanh Navy đậm cho tiêu đề chính */
  --text-subheading: #1e3a8a;            /* Xanh Blue đậm cho tiêu đề phụ */
  --text-body: #1e293b;                  /* Than xám đậm cho nội dung (WCAG AA > 9:1) */
  --text-muted: #475569;                 /* Xám trung tính cho chú thích phụ */

  /* 4. Thẻ chứa thông tin (Cards & Containers) */
  --card-bg: #f0f6fc;                    /* Nền Ice-Blue dịu mắt */
  --card-border: #2563eb;                /* Viền xanh dương sắc nét */
  --card-border-subtle: rgba(37, 99, 235, 0.3);
  --card-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);

  /* 5. Phân nhánh & Kết quả */
  --connector-blue: #2563eb;             /* Đường dẫn đầu vào / xử lý */
  --connector-red: #c5221f;              /* Đường dẫn nhãn kết quả đầu ra */
  --accent-gold: #d97706;                /* Màu vàng hổ phách cho trích dẫn/cột mốc */
  --accent-emerald: #059669;             /* Màu xanh ngọc cho kết quả thành công/AlexNet */

  /* 6. Thanh phụ đề (Live Caption Pill) */
  --caption-bg: rgba(255, 255, 255, 0.95);
  --caption-border: rgba(148, 163, 184, 0.4);
  --caption-text: #0c2340;
  --caption-shadow: 0 15px 35px rgba(15, 23, 42, 0.12);
}
```

---

## 3. Quy Tắc Bố Cục Khung Hình (Layout & Component Rules)

### A. Thanh Thương Hiệu Trên Cùng (Top Brand Header)
- **Vị trí**: Cố định ở đỉnh khung hình (`top: 32px; left: 60px; right: 60px;`).
- **Phía trái**:
  - Dòng Kicker chữ in hoa màu đỏ VinUni: `NGÀY 01 · AI, MACHINE LEARNING, GENERATIVE AI & LLM`.
  - Font chữ: Sans-serif đậm, `font-weight: 800`, `letter-spacing: 2px`, `font-size: 15px`.
- **Phía phải**:
  - Dấu chấm tròn đỏ + Chữ thương hiệu: `• VinUni · AI in Action 20K`.
  - Dấu chấm đỏ: `width: 8px; height: 8px; background: #c5221f; border-radius: 50%;`.

### B. Tiêu Đề Phân Cảnh (Scene Main Title)
- **Vị trí**: Đặt giữa (`text-align: center`), cách đỉnh `60px – 80px`.
- **Màu sắc**: Xanh Navy đậm `#0c2340`.
- **Kích thước**: `font-size: 44px – 52px; font-weight: 800;`.
- **Badge phân cảnh**: Nền đỏ nhạt `rgba(197, 34, 31, 0.08)`, viền đỏ `rgba(197, 34, 31, 0.3)`, chữ hoa đỏ `#c5221f`.

### C. Thẻ Nội Dung & Luồng Xử Lý (Flow & Process Cards)
- Mô phỏng chính xác sơ đồ khối từ slide:
  1. **Khối Đầu Vào (Input)**: Thẻ nền Ice-Blue `#f0f6fc`, viền xanh `#2563eb`, chữ `#0c2340`. Kèm icon đại diện (✉️ email, 💬 chat, 🖼️ ảnh).
  2. **Khối Xử Lý (Processing)**: Nối bởi đường kẻ xanh `#2563eb`, nhãn "Xử lý ?".
  3. **Khối Đầu Ra (Output)**: Nối bởi đường kẻ đỏ `#c5221f`. Nhãn loại kết quả in hoa màu đỏ (`NHÃN`, `ĐOẠN VĂN`, `ẢNH MỚI`). Hộp kết quả viền xám/xanh bo tròn.

### D. Khung Trưng Bày Bài Báo & Dẫn Chứng Khoa Học (Evidence Cards)
- Do tài liệu PDF / Paper có trang bìa nền trắng, đặt trên nền sáng VinUni sẽ đạt độ liền mạch và mỹ thuật tối đa:
  - Khung bao: Nền trắng `#ffffff`, viền xanh nhạt hoặc viền vàng hổ phách `2px solid rgba(217, 119, 6, 0.4)`.
  - Bóng đổ mềm: `box-shadow: 0 15px 35px rgba(15, 23, 42, 0.08);`.
  - Tag nguồn bài báo: Đặt ở góc hoặc chân ảnh với nhãn rõ ràng (vd: `📄 IEEE CVPR 2009`).

### E. Thanh Phụ Đề Nổi (Live Floating Subtitle Pill)
- **Vị trí**: Đặt ở đáy màn hình (`bottom: 40px; left: 100px; right: 100px;`).
- **Nền**: Trắng bán trong suốt `rgba(255, 255, 255, 0.96)`, hiệu ứng kính mờ `backdrop-filter: blur(16px)`.
- **Viền**: `1px solid rgba(148, 163, 184, 0.35)`.
- **Chữ phụ đề**: Màu Navy đậm `#0c2340`, `font-size: 20px - 22px; font-weight: 600;`.
- **Icon phát loa**: Vòng tròn xanh `#2563eb` hoặc đỏ `#c5221f` có biểu tượng mic/speaker.

---

## 4. Bảng Kiểm Tra Tuân Thủ (Compliance Checklist Cho Mọi IDE)
- [ ] Nền là màu trắng hoặc màu sáng (`#ffffff` / `#f8fafc`), không dùng nền đen/cyberpunk tối.
- [ ] Xuất hiện Kicker đỏ VinUni `#c5221f` và nhãn `• VinUni · AI in Action 20K`.
- [ ] Tiêu đề có màu xanh Navy đậm `#0c2340`.
- [ ] Thẻ hộp có nền Ice-Blue `#f0f6fc` với viền xanh `#2563eb`.
- [ ] 100% chữ đọc được với độ tương phản WCAG AA >= 4.5:1 (toàn bộ text thông thường đạt > 8:1).
- [ ] Mọi con số trong lời thoại voiceover (`loi`) được viết bằng chữ tiếng Việt (0 chữ số 0-9).
