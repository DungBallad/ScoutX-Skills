# Tham Chiếu Lược Đồ JSON (Hackathon Schema)

## 1. Schema: `hackathon-ho-so-nguon/1`
Dùng để mô tả các nguồn dữ liệu và thông tin trích xuất đối chiếu chéo ($\ge 2$ nguồn độc lập).

```json
{
  "schema": "hackathon-ho-so-nguon/1",
  "nguon": [
    {
      "id": "slide-hackathon-d1",
      "tieuDe": "Tên bài giảng",
      "toChuc": "Tên tác giả / Ban tổ chức Hackathon",
      "ngayDang": "2026-09-17",
      "url": "file:///path/to/slide.pdf",
      "doTinCay": "cao",
      "lyDoTinCay": "Tài liệu giáo trình chính thức",
      "loai": "slide", 
      "trangThai": "dang-dung",
      "ngayLayVe": "2026-09-17"
    },
    {
      "id": "neurips-2017-transformer",
      "tieuDe": "Attention Is All You Need",
      "toChuc": "Google Brain / NeurIPS",
      "ngayDang": "2017-06-12",
      "url": "https://arxiv.org/abs/1706.03762",
      "doTinCay": "cao",
      "lyDoTinCay": "Bài báo khoa học gốc của nhóm tác giả",
      "loai": "bai-bao-khoa-hoc",
      "trangThai": "dang-dung",
      "ngayLayVe": "2026-09-17"
    }
  ],
  "thongTin": [
    {
      "id": "tt-transformer-2017",
      "noiDung": "Năm 2017, kiến trúc Transformer ra đời thay thế cơ chế tuần tự bằng Attention.",
      "loai": "su-kien",
      "bangChung": [
        {
          "nguonId": "slide-hackathon-d1",
          "doanTrich": "2017: Transformer là bước ngoặt vì nó cho mô hình hiểu ngôn ngữ linh hoạt hơn...",
          "viTri": "Slide 8"
        },
        {
          "nguonId": "neurips-2017-transformer",
          "doanTrich": "The Transformer is the first transduction model relying entirely on self-attention...",
          "viTri": "NeurIPS 2017 Abstract"
        }
      ],
      "soNguonXacNhan": 2,
      "trangThai": "da-xac-minh",
      "moTaMauThuan": ""
    }
  ]
}
```

---

## 2. Schema: `hackathon-kich-ban/1` (Bắt Buộc Đưa Dẫn Chứng Vào Kịch Bản)
Dùng để mô tả kịch bản video, bắt buộc tích hợp trực tiếp dẫn chứng vào lời thoại và nhãn nguồn video.

```json
{
  "schema": "hackathon-kich-ban/1",
  "tieuDe": "Giới thiệu Transformer",
  "mucTieu": "Giải thích bước ngoặt lịch sử và cơ chế hoạt động của Transformer",
  "phan": [
    { "so": 1, "ten": "Mở đầu" },
    { "so": 2, "ten": "Cơ chế" }
  ],
  "cau": [
    {
      "n": 1,
      "phan": 1,
      "kieu": "giang",
      "loi": "Theo bài báo khoa học kinh điển 'Attention Is All You Need' công bố tại hội nghị Niu-Ríp năm hai nghìn không trăm mười bảy của nhóm tác giả Google, kiến trúc Transformer đã ra đời và tạo nên bước ngoặt thay đổi toàn bộ ngành trí tuệ nhân tạo.",
      "chuTrenManHinh": "Transformer: Attention Is All You Need",
      "yDoHinh": "Hiển thị tiêu đề bài báo NeurIPS 2017 và dòng thời gian phát sáng",
      "nguon": ["tt-transformer-2017"],
      "goiYHienNguon": "Vaswani et al. (2017), 'Attention Is All You Need', NeurIPS 2017 · arXiv:1706.03762"
    }
  ]
}
```

### CÁC NGUYÊN TẮC BẮT BUỘC:
1. **`loi` (Lời thoại voiceover)**:
   - **BẮT BUỘC** lồng ghép dẫn chứng cụ thể: Tên tác giả (vd: giáo sư Phi Phi Li, nhóm nghiên cứu Google, Đại học Xtan-phớt...), Tên bài báo/nghiên cứu, Tên hội nghị/tạp chí uy tín (NeurIPS, CVPR, arXiv...).
   - **TUYỆT ĐỐI KHÔNG chứa chữ số học**: Viết "hai nghìn không trăm mười bảy" thay vì "2017", "mười bốn triệu" thay vì "14 triệu".
2. **`goiYHienNguon` (Nhãn trích dẫn học thuật)**:
   - BẮT BUỘC có khi `nguon` không rỗng.
   - Định dạng chuẩn: `Tác giả (Năm), "Tên bài báo / Nghiên cứu", Hội nghị / Tạp chí · DOI/URL`.
   - Renderer video sẽ đọc trường này để hiển thị citation badge hoặc subtitle source trực quan.
3. **`nguon`**: Mảng ID trỏ chính xác về các mục trong `hoSo.thongTin`. Để `[]` nếu là câu kết hoặc câu chuyển ý.
