# Tham Chiếu Lược Đồ JSON (Hackathon Schema - Tích Hợp Hình Ảnh Dẫn Chứng)

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

## 2. Schema: `hackathon-kich-ban/1` (Bắt Buộc Có Hình Ảnh Dẫn Chứng Thực Tế)
Dùng để mô tả kịch bản video, bắt buộc có hình ảnh dẫn chứng (trang bìa paper, ảnh chụp web, biểu đồ, slide) để hiển thị trong video.

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
      "yDoHinh": "Hiển thị khung tài liệu 3D chứa trang bìa bài báo gốc NeurIPS 2017 và sơ đồ Attention phát sáng",
      "hinhAnhDanChung": "assets/evidence/paper-attention-is-all-you-need.png",
      "loaiDanChung": "trang-bia-paper",
      "moTaDanChung": "Ảnh chụp trang bìa đầu tiên của bài báo Attention Is All You Need (NIPS 2017) với danh sách 8 tác giả",
      "goiYHienNguon": "Vaswani et al. (2017), 'Attention Is All You Need', NeurIPS 2017 · arXiv:1706.03762",
      "nguon": ["tt-transformer-2017"]
    }
  ]
}
```

### CÁC TRƯỜNG DẪN CHỨNG BẮT BUỘC:
1. **`hinhAnhDanChung`**:
   - Đường dẫn cục bộ tới tệp hình ảnh bằng chứng (định dạng PNG/JPG sắc nét, lưu trong `assets/evidence/`).
   - Các loại hình ảnh:
     * **Trang bìa Paper**: Ảnh chụp trang đầu tiên của file PDF bài báo khoa học (arXiv/CVPR/NeurIPS) chứa tiêu đề, tác giả, abstract.
     * **Ảnh chụp Slide gốc**: Ảnh chụp trang slide bài giảng chứa thông tin tương ứng.
     * **Ảnh chụp Web / Benchmark / Biểu đồ**: Ảnh chụp màn hình từ các website công cụ chính thức (OpenAI Tokenizer, OpenD5, v.v.).
2. **`loaiDanChung`**:
   - Các giá trị hợp lệ: `"trang-bia-paper"`, `"anh-chup-web"`, `"bieu-do"`, `"trang-slide"`, `"anh-san-pham"`.
3. **`moTaDanChung`**:
   - Mô tả ngắn gọn nội dung của hình ảnh dẫn chứng để người dựng video căn chỉnh bố cục thị giác.
4. **`goiYHienNguon`**:
   - Định dạng chuẩn: `Tác giả (Năm), "Tên bài báo / Nghiên cứu", Hội nghị / Tạp chí · DOI/URL`.
5. **`loi`**:
   - Lồng ghép tên tác giả, tên công trình vào lời thoại văn nói tự nhiên, **TUYỆT ĐỐI KHÔNG chứa chữ số**.
