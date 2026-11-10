# IT Quiz • 600 câu trắc nghiệm CNTT

Web luyện tập bám sát tài liệu **Cẩm nang ôn thi cuối học phần** (198 trang, 47 bài, 10 session) và có câu hỏi mở rộng rõ nhãn.

## Nội dung

| Session | Chủ đề | Số câu |
|---|---|---:|
| 02 | Nhập môn CNTT và dữ liệu | 60 |
| 03 | Hệ điều hành, đường dẫn và tệp tin | 60 |
| 05 | Terminal cơ bản | 60 |
| 07 | Dòng lệnh nâng cao và script an toàn | 60 |
| 09 | Markdown và tài liệu kỹ thuật | 60 |
| 11 | Word, Excel và PowerPoint | 60 |
| 15 | Phân quyền và Hybrid Workflow | 60 |
| 17 | Trình duyệt và DevTools | 60 |
| 19 | An toàn thông tin và Secrets | 60 |
| 21 | Tìm kiếm và báo lỗi kỹ thuật | 60 |
| **Tổng** | **47 bài** | **600** |

- **399 câu theo PDF**: nội dung chính, ví dụ và lưu ý theo đúng bài; mỗi câu chỉ rõ trang PDF.
- **141 câu vận dụng**: tình huống, lệnh, cách giải quyết vấn đề từ chủ đề bài học.
- **60 câu mở rộng**: kiến thức bổ sung, được đánh dấu riêng, không mạo nhận là nội dung nằm trong PDF.

## Sử dụng

1. Giải nén ZIP, mở `index.html` bằng Chrome, Edge, Firefox hoặc Safari. **Không cần cài đặt, không cần Internet**.
2. Chọn session ở cạnh trái (trên điện thoại, chọn thanh session ngang).
3. Chọn đáp án A/B/C/D, bấm **Hoàn thành** để kiểm tra ngay câu đang làm. Lời giải sẽ xuất hiện ngay phía dưới.
4. Dùng **Câu tiếp**, **Câu trước** hoặc ô số câu để chuyển câu. Có thể lọc theo bài học.
5. Bấm **Làm lại toàn bộ** và xác nhận để xóa toàn bộ đáp án đã chọn (kể cả câu chưa chấm), kết quả và tiến độ của cả 600 câu; về Session 02 – Câu 1, bỏ lọc bài.
6. Màn hình ưu tiên **hiển thị câu hỏi và 4 đáp án** ngay dưới tên session; thống kê và lưới điều hướng được đặt bên dưới quiz.

Hệ thống tự lưu câu đã chọn, câu đã chấm và session gần nhất trong bộ nhớ trình duyệt (localStorage) khi trình duyệt cho phép. Chấm rồi sẽ khóa đáp án đến khi làm lại toàn bộ.

## Deploy lên Vercel / Netlify / hosting tĩnh

Upload toàn bộ nội dung thư mục này lên hosting tĩnh với `index.html` ở thư mục gốc.

- Web không dùng server, API, database, CDN hoặc thư viện ngoài.
- Trên HTTPS, service worker lưu sẵn giao diện và toàn bộ **600 câu** trong cache. Sau khi mở online thành công một lần, có thể mở lại web để làm bài offline trong trình duyệt có hỗ trợ service worker.
- `tai-lieu-goc.pdf` được phân phối riêng (36 MB). **PDF không được tự động lưu offline khi deploy trên web** để tránh chiếm tài nguyên; nếu dùng từ ZIP, PDF nằm sẵn bên cạnh website nên vẫn mở offline.
- Trên Safari/iPhone, khả năng lưu trữ offline và Add to Home Screen phụ thuộc hệ điều hành, quyền cấp và trạng thái bộ nhớ. Không thể bảo đảm lần truy cập đầu tiên offline từ một URL chưa tải trước.

## Các tệp chính

- `index.html`: Web **độc lập**, chứa sẵn 600 câu, CSS và JavaScript; có thể mở riêng mà không cần file câu hỏi ngoài.
- `tai-lieu-goc.pdf`: Tài liệu PDF để tra cứu trang gốc.
- `service-worker.js`, `manifest.webmanifest`, `icon-*`: Hỗ trợ web app khi host HTTPS.
- `questions.json`: Ngân hàng câu hỏi ở dạng JSON để rà soát hoặc nhập vào hệ thống khác.

## Thông tin học thuật

Câu hỏi và lời giải được xây dựng từ phần diễn giải/ghi chú ôn tập của 47 bài trong PDF; các ảnh chụp gốc nằm ở những trang kế tiếp để đối chiếu. Câu vận dụng là cách diễn giải và bài tập thực hành dựa trên nội dung cốt lõi, không phải trích nguyên văn đề thi của trường.

Web được xây dựng để tự luyện, kết quả lưu cục bộ, không thu thập hay gửi đáp án lên máy chủ.

## Bản sửa lỗi đặt lại toàn bộ

- Xóa cả dữ liệu cũ trong `localStorage`/`sessionStorage` chỉ thuộc ứng dụng IT Quiz, không ảnh hưởng website khác.
- Trở về câu đầu tiên của Session 02, 0/600 đã làm, 0 đúng, 0% tiến độ; xóa lựa chọn, màu đúng/sai, giải thích, lọc bài.
- Đóng/mở lại web hoặc tải lại trang vẫn giữ trạng thái **chưa làm** sau khi reset.
- Nếu triển khai lên hosting, tải lên **toàn bộ** thư mục bản mới (đặc biệt `service-worker.js`) để cập nhật cache từ v3 sang v4.
