# 01 — Danh mục Use Case: RepoAtlas

> **Môn học:** Phân tích và Thiết kế Hướng đối tượng (OOAD)
> **Nguồn bằng chứng:** `docs/user-stories.md`, `backend/src/cli.py`, `backend/src/`

---

## 1. Danh sách Actor

### Actor Chính

| ID | Actor | Mô tả | Mục tiêu sử dụng |
|---|---|---|---|
| A1 | **Software Engineer** | Kỹ sư phần mềm — người vận hành CLI để phân tích repo | Tạo tài liệu wiki kỹ thuật từ source code |
| A2 | **Wiki User** | Người đọc tài liệu wiki đã được tạo | Tìm hiểu kiến trúc, modules, symbols của project |

### Hệ thống Bên ngoài

| ID | Hệ thống | Mô tả |
|---|---|---|
| EX1 | **Git Remote Server** | Cung cấp repository khi người dùng nhập URL Git |
| EX2 | **Ollama LLM Server** | Cung cấp khả năng tóm tắt AI cho code |
| EX3 | **Web Browser** | Hiển thị wiki HTML sau khi tạo xong |

---

## 2. Danh mục Use Case

### Nhóm 1: Phân tích Repository (Epic 1 — Core Indexing)

| ID | Tên Use Case | Actor chính | Mục tiêu | Tiền điều kiện | Hậu điều kiện | Độ ưu tiên |
|---|---|---|---|---|---|---|
| UC-01 | Phân tích Repository Cục bộ | Software Engineer | Quét và phân tích AST repo từ đường dẫn cục bộ | Đường dẫn repo hợp lệ, có file .java hoặc .cs | `repository_index.json` được tạo | **Cao** |
| UC-02 | Phân tích Repository từ Git URL | Software Engineer, Git Remote Server | Clone và phân tích AST repo từ URL Git | URL Git hợp lệ, có kết nối mạng | `repository_index.json` được tạo, temp dir được dọn sạch | **Cao** |
| UC-03 | Phân tích Java Source Code | Software Engineer | Trích xuất ký hiệu AST từ file .java | File .java hợp lệ | `FileIndex` với Java symbols được tạo | **Cao** |
| UC-04 | Phân tích C# Source Code | Software Engineer | Trích xuất ký hiệu AST từ file .cs | File .cs hợp lệ | `FileIndex` với C# symbols được tạo | **Cao** |

### Nhóm 2: AI Analysis và Tóm tắt (Epic 3 — AI Analysis)

| ID | Tên Use Case | Actor chính | Mục tiêu | Tiền điều kiện | Hậu điều kiện | Độ ưu tiên |
|---|---|---|---|---|---|---|
| UC-05 | Tóm tắt Code bằng LLM Cục bộ | Software Engineer, Ollama LLM Server | Sử dụng Ollama để tóm tắt từng ký hiệu AST | `repository_index.json` đã tồn tại, Ollama đang chạy | `summaries.json` với AI-generated descriptions | **Cao** |
| UC-06 | Tóm tắt Code không có LLM | Software Engineer | Tạo tài liệu cấu trúc khi không có LLM | `repository_index.json` đã tồn tại | `summaries.json` với structural-only descriptions | **Cao** |
| UC-07 | Phân khúc AST theo Taxonomy 6 tầng | Hệ thống | Chia nhỏ code theo 6 tầng phân cấp AST | `repository_index.json` đã tồn tại | `TaxonomyTree` với chunks theo 6 tầng | **Cao** |

### Nhóm 3: Knowledge Graph (Epic 2 — Knowledge Graph)

| ID | Tên Use Case | Actor chính | Mục tiêu | Tiền điều kiện | Hậu điều kiện | Độ ưu tiên |
|---|---|---|---|---|---|---|
| UC-08 | Tạo Knowledge Graph | Hệ thống | Kết hợp IR và summaries thành đồ thị tri thức | `repository_index.json` và `summaries.json` đã tồn tại | `graph.json` được tạo với nodes và edges hợp lệ | **Cao** |
| UC-09 | Truy vấn Knowledge Graph | Software Engineer | Tìm kiếm quan hệ giữa các ký hiệu trong graph | `graph.json` đã tồn tại | Kết quả truy vấn quan hệ dependencies | **Trung bình** |

### Nhóm 4: Tạo Tài liệu Wiki (Epic 4 — Wiki Generation)

| ID | Tên Use Case | Actor chính | Mục tiêu | Tiền điều kiện | Hậu điều kiện | Độ ưu tiên |
|---|---|---|---|---|---|---|
| UC-10 | Tạo Trang Dashboard (index.html) | Hệ thống | Render trang tổng quan với Bento Grid metrics | `graph.json`, `repository_index.json` đã tồn tại | `wiki/index.html` được tạo | **Cao** |
| UC-11 | Tạo Tài liệu Technology Stack | Hệ thống | Render trang tech.html | `summaries.json` đã tồn tại | `wiki/tech.html` được tạo | **Cao** |
| UC-12 | Tạo Tài liệu Architecture | Hệ thống | Render trang architecture.html | `summaries.json` đã tồn tại | `wiki/architecture.html` được tạo | **Cao** |
| UC-13 | Tạo Tài liệu Modules | Hệ thống | Render trang modules.html | `summaries.json` đã tồn tại | `wiki/modules.html` được tạo | **Cao** |
| UC-14 | Tạo Tài liệu Tests | Hệ thống | Render trang tests.html | `summaries.json` đã tồn tại | `wiki/tests.html` được tạo | **Cao** |
| UC-15 | Tạo Trang Chi tiết Symbol | Hệ thống | Render trang `symbols/<fqn>.html` cho mỗi ký hiệu | `repository_index.json` đã tồn tại | `wiki/symbols/*.html` được tạo | **Cao** |
| UC-16 | Tạo Search Index | Hệ thống | Sinh file `search_index.json` phục vụ tìm kiếm | `repository_index.json` đã tồn tại | `wiki/search_index.json` được tạo | **Cao** |
| UC-17 | Tạo AI Context | Hệ thống | Sinh file `wiki_context.json` cho AI Widget | `repository_index.json` và `summaries.json` đã tồn tại | `wiki/wiki_context.json` được tạo | **Cao** |

### Nhóm 5: CLI Orchestration (Epic 5 — CLI)

| ID | Tên Use Case | Actor chính | Mục tiêu | Tiền điều kiện | Hậu điều kiện | Độ ưu tiên |
|---|---|---|---|---|---|---|
| UC-18 | Thực thi Pipeline Phân tích Đầy đủ | Software Engineer | Chạy toàn bộ workflow từ một lệnh duy nhất | Python 3.10+ được cài đặt | Toàn bộ wiki/ được tạo, trình duyệt mở | **Cao** |
| UC-19 | Cấu hình Chế độ LLM | Software Engineer | Chọn bật/tắt LLM khi chạy phân tích | Không có | Pipeline chạy với LLM mode được chọn | **Trung bình** |

### Nhóm 6: Sử dụng Wiki Tĩnh

| ID | Tên Use Case | Actor chính | Mục tiêu | Tiền điều kiện | Hậu điều kiện | Độ ưu tiên |
|---|---|---|---|---|---|---|
| UC-20 | Điều hướng Wiki với Sidebar | Wiki User | Duyệt qua cây tài liệu sử dụng sidebar | `wiki/` đã được tạo và mở trong trình duyệt | Người dùng xem được trang mong muốn | **Trung bình** |
| UC-21 | Tìm kiếm Ký hiệu trong Wiki | Wiki User | Tìm kiếm class/method cụ thể bằng live search | `search_index.json` đã tồn tại | Người dùng điều hướng đến trang ký hiệu | **Trung bình** |
| UC-22 | Hỏi AI Widget về Codebase | Wiki User, Ollama LLM Server | Đặt câu hỏi về kiến trúc/code qua AI chat widget | `wiki_context.json` đã tồn tại, Ollama đang chạy | AI Widget trả lời câu hỏi với symbol links | **Trung bình** |
| UC-23 | Xem Chi tiết Symbol | Wiki User | Xem thông tin chi tiết về class/method cụ thể | Trang `symbols/<fqn>.html` tồn tại | Người dùng thấy signature, docstring, annotations | **Thấp** |

---

## 3. Quan hệ giữa các Use Case

### Quan hệ `<<include>>`

| Use Case Gốc | Quan hệ | Use Case Được Bao gồm | Lý do |
|---|---|---|---|
| UC-18 (Pipeline Đầy đủ) | `<<include>>` | UC-01 hoặc UC-02 | Pipeline luôn phải quét repo |
| UC-18 (Pipeline Đầy đủ) | `<<include>>` | UC-05 hoặc UC-06 | Pipeline luôn phải chạy AI analysis |
| UC-18 (Pipeline Đầy đủ) | `<<include>>` | UC-08 | Pipeline luôn phải tạo Knowledge Graph |
| UC-18 (Pipeline Đầy đủ) | `<<include>>` | UC-10, UC-11, UC-12, UC-13, UC-14 | Pipeline luôn tạo toàn bộ wiki pages |
| UC-01/UC-02 | `<<include>>` | UC-03 hoặc UC-04 | Quét repo luôn kéo theo parse file nguồn |

### Quan hệ `<<extend>>`

| Use Case Gốc | Quan hệ | Use Case Mở rộng | Điều kiện |
|---|---|---|---|
| UC-05 (Tóm tắt với LLM) | `<<extend>>` | UC-06 (Tóm tắt không LLM) | Khi Ollama không khả dụng, fallback sang chế độ structural |
| UC-02 (Git URL) | `<<extend>>` | UC-01 (Cục bộ) | Sau khi clone xong, xử lý như repo cục bộ |
| UC-22 (AI Widget) | `<<extend>>` | UC-21 (Tìm kiếm) | AI Widget dùng search_index.json để tìm symbols |

### Generalization giữa Actor

| Actor Cha | Actor Con | Lý do |
|---|---|---|
| **Software Engineer** | **Wiki User** | Software Engineer cũng là người đọc wiki (generalization hợp lý vì mọi SE đều có thể là Wiki User) |

---

## 4. Phân nhóm Use Case theo Module

```
Epic 1 (Core Indexing): UC-01, UC-02, UC-03, UC-04
Epic 2 (Knowledge Graph): UC-08, UC-09
Epic 3 (AI Analysis): UC-05, UC-06, UC-07
Epic 4 (Wiki Generation): UC-10, UC-11, UC-12, UC-13, UC-14, UC-15, UC-16, UC-17
Epic 5 (CLI Orchestration): UC-18, UC-19
Wiki Usage: UC-20, UC-21, UC-22, UC-23
```
