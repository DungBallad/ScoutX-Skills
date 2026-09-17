# Tham Chiếu Lược Đồ JSON (Hackathon Schema)

## 1. Schema: `hackathon-ho-so-nguon/1`
Dùng để mô tả các nguồn dữ liệu và thông tin trích xuất.

```json
{
  "nguon": [
    {
      "id": "slide-1",
      "tieuDe": "Tên bài giảng",
      "toChuc": "Tên tác giả / Slide bài giảng khoá học",
      "ngayDang": "2024-01-01",
      "url": "",
      "doTinCay": "cao",
      "lyDoTinCay": "Tài liệu chính thức",
      "loai": "slide", 
      "trangThai": "dang-dung",
      "ngayLayVe": "2024-10-31"
    }
  ],
  "thongTin": [
    {
      "id": "tt-1",
      "noiDung": "Transformer ra đời năm 2017.",
      "loai": "su-kien",
      "bangChung": [
        {
          "nguonId": "slide-1",
          "doanTrich": "...ra đời năm 2017 bởi Google...",
          "viTri": "Slide 3"
        }
      ],
      "soNguonXacNhan": 1,
      "trangThai": "chua-xac-minh",
      "moTaMauThuan": ""
    }
  ]
}
```
*(Ghi chú: Giá trị `loai` của nguồn gồm: "slide", "tai-lieu-chinh-thuc", "bai-bao-khoa-hoc", "bao-chi", "blog-ca-nhan").*

## 2. Schema: `hackathon-kich-ban/1`
Dùng để mô tả kịch bản video dựa trên hồ sơ nguồn.

```json
{
  "tieuDe": "Giới thiệu Transformer",
  "mucTieu": "Giải thích cách Transformer hoạt động",
  "phan": [
    { "so": 1, "ten": "Mở đầu" },
    { "so": 2, "ten": "Cơ chế" }
  ],
  "cau": [
    {
      "n": 1,
      "phan": 1,
      "kieu": "giang",
      "loi": "Chào các bạn, hôm nay chúng ta sẽ tìm hiểu về mô hình ra đời năm hai nghìn không trăm mười bảy.",
      "chuTrenManHinh": "Ra đời năm 2017",
      "yDoHinh": "Hiển thị dòng thời gian năm 2017",
      "nguon": ["tt-1"]
    }
  ]
}
```

**LƯU Ý QUAN TRỌNG:**
- `loi`: PHẢI viết các chữ số bằng chữ (vd: "hai nghìn không trăm mười bảy"). KHÔNG dùng số học (2017) trong lời đọc.
- `nguon` trong mảng `cau` có thể là `[]` nếu đó là câu chuyển tiếp hoặc ví dụ giả định không cần chứng minh.
