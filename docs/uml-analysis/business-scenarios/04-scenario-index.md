# 04 — DANH MỤC KỊCH BẢN VÀ MA TRẬN ĐỐI CHIẾU TRUY VẾT (TRACEABILITY MATRIX)

> **Tài liệu:** Danh mục Tổng hợp Kịch bản và Ma trận Đối chiếu (Scenario Index & Traceability)  
> **Chuyên môn:** Phân tích và Thiết kế Hướng đối tượng (OOAD) & Quản lý Yêu cầu Phần mềm  
> **Dự án đối chiếu:** RepoAtlas (Automated AST-Grounded Repository Documentation Generator)  
> **Mục tiêu:** Cung cấp danh mục tra cứu tập trung cho toàn bộ các kịch bản nghiệp vụ đã xây dựng (Use Case, Activity, State Machine), thiết lập ma trận truy vết chéo hai chiều (Bidirectional Traceability) và phân định rõ ràng trạng thái xác minh trong mã nguồn thực tế.

---

## I. DANH MỤC TỔNG HỢP CÁC KỊCH BẢN NGHIỆP VỤ

### 1. Bảng Danh mục Toàn diện (Master Scenario Catalog)

| Mã kịch bản | Tên kịch bản | Phân nhóm UML | Đối tượng / Chức năng nghiệp vụ liên quan | Các kịch bản liên kết | Bằng chứng mã nguồn / Tài liệu dự án | Trạng thái xác minh |
|:---:|---|:---:|---|---|---|:---:|
| **UC-01** | Phân tích Repository Cục bộ | Use Case | Quét thư mục, phân tích AST trên máy cục bộ | AD-01, AD-03, SD-01 | `scanner.py:113-118`, `ir_generator.py:17-48`, `docs/user-stories.md:US-1.1` | **Đã xác nhận** |
| **UC-02** | Phân tích Repository từ Git URL | Use Case | Cấp phát temp dir, clone nông từ xa, dọn dẹp | AD-01, AD-02, AD-10, SD-01, SD-02 | `scanner.py:89-111`, `scanner.py:221-226`, `docs/user-stories.md:US-1.1` | **Đã xác nhận** |
| **UC-03** | Phân tích Cú pháp Java | Use Case | Phân tích AST Java, trích xuất FQN, class, method | AD-03, SD-03 | `parsers/java_parser.py`, `models.py:121-160`, `docs/designs/ast-parser-design.md` | **Đã xác nhận** |
| **UC-04** | Phân tích Cú pháp C# | Use Case | Phân tích AST C#, namespace, property, async | AD-03, SD-03 | `parsers/csharp_parser.py`, `models.py:109-115`, `docs/designs/ast-parser-design.md` | **Đã xác nhận** |
| **UC-05** | Tóm tắt Phân cấp bằng AI (Ollama) | Use Case | Tóm tắt Bottom-Up qua cây 6 tầng và Ollama | AD-01, AD-04, AD-09, SD-01, SD-03 | `summarizer.py:50-180`, `ollama.py:40-75`, `docs/designs/hierarchical-prompting-chunking.md` | **Đã xác nhận** |
| **UC-06** | Tóm tắt Cấu trúc Dự phòng (No-LLM) | Use Case | Tóm tắt siêu dữ liệu xác định khi mất LLM | AD-01, AD-09, SD-01, SD-03 | `null.py`, `content_generator.py`, `docs/adrs.md:ADR-006` | **Đã xác nhận** |
| **UC-08** | Xây dựng & Thẩm định Knowledge Graph | Use Case | Hợp nhất IR + summary, bù trừ nút EXTERNAL | AD-01, AD-05, SD-01, SD-04 | `builder.py:64-322`, `builder.py:334-360`, `models.py:74-95` | **Đã xác nhận** |
| **UC-10** | Sinh Bộ Trang Wiki Chuyên đề & Dashboard | Use Case | Render 4 trang chuyên đề và index.html | AD-01, AD-06, SD-01 | `renderer.py:20-83`, `cli.py:104-124`, `docs/designs/html-wiki-storage.md` | **Đã xác nhận** |
| **UC-15** | Sinh Trang Hồ sơ Ký hiệu Cú pháp | Use Case | Render hàng loạt trang `symbols/<fqn>.html` | AD-01, AD-06, SD-01, SD-03 | `renderer.py:38-63`, `docs/designs/html-wiki-storage.md:Section 4` | **Đã xác nhận** |
| **UC-16** | Sinh Chỉ mục Tìm kiếm & Ngữ cảnh AI | Use Case | Xuất bản `search_index.json` và `wiki_context.json` | AD-01, AD-06, SD-01, SD-05 | `renderer.py:84-182`, `docs/user-stories.md:US-4.5, US-4.6` | **Đã xác nhận** |
| **UC-18** | Thực thi Toàn bộ Pipeline Phân tích | Use Case | Điều phối 4 giai đoạn và mở trình duyệt | AD-01, SD-01 | `cli.py:43-145`, `docs/architecture.md:Section 6` | **Đã xác nhận** |
| **UC-20** | Điều hướng Khám phá Cây Tài liệu | Use Case | Duyệt web qua thanh bên và thẻ liên kết | AD-07 | `templates/base.html:292-304`, `docs/user-stories.md:US-4.1` | **Đã xác nhận** |
| **UC-21** | Tìm kiếm Ký hiệu Ngoại tuyến | Use Case | Live search 15 kết quả hàng đầu trên RAM | AD-07 | `templates/base.html:251-290`, `docs/user-stories.md:US-4.5` | **Đã xác nhận** |
| **UC-22** | Hỏi đáp với Trợ lý AI Cục bộ | Use Case | Chat widget nhúng streaming + intelligent fallback | AD-08, SD-05 | `templates/base.html:305-604`, `README.md:Line 14` | **Đã xác nhận** |
| **AD-01** | Toàn bộ Pipeline Phân tích Repository | Activity | Chuỗi 4 phân hệ chính từ CLI đến Web | UC-18, SD-01 | `backend/src/cli.py:43-145` | **Đã xác nhận** |
| **AD-02** | Nhận diện URL & Clone Git Từ xa | Activity | Phân giải regex URL, mkdtemp, git clone | UC-02, SD-02 | `core_indexing/scanner.py:70-111` | **Đã xác nhận** |
| **AD-03** | Quét Thư mục & Phân tích Cú pháp AST | Activity | Lọc `.gitignore`, vòng lặp file, trích xuất AST | UC-01, UC-03, UC-04, SD-03 | `core_indexing/scanner.py:120-220` | **Đã xác nhận** |
| **AD-04** | Tóm tắt Phân cấp Bottom-Up & Token | Activity | Duyệt 6 tầng, cắt tỉa token <= 2000, chống ảo giác | UC-05, SD-03 | `ai_analysis/summarizer.py:50-180`, `chunker.py` | **Đã xác nhận** |
| **AD-05** | Xây dựng & Lưu trữ Đồ thị Nguyên tử | Activity | Bù trừ nút EXTERNAL, thẩm định toàn vẹn, atomic replace | UC-08, SD-04 | `knowledge_graph/builder.py:64-360` | **Đã xác nhận** |
| **AD-06** | Biên dịch HTML & Chỉ mục Song song | Activity | Fork/Join render trang chuyên đề & symbol pages | UC-10, UC-15, UC-16, SD-01 | `wiki_generation/renderer.py:20-182` | **Đã xác nhận (Fork/Join là mô hình hóa; chưa xác nhận chạy song song thật)** |
| **AD-07** | Điều hướng & Tìm kiếm Ngoại tuyến | Activity | Active sidebar state, client live search | UC-20, UC-21 | `wiki_generation/templates/base.html:232-304` | **Đã xác nhận** |
| **AD-08** | Hỏi đáp AI & Truyền luồng Thời gian thực | Activity | Hybrid context retrieval, streaming reader, fallback | UC-22, SD-05 | `wiki_generation/templates/base.html:305-604` | **Đã xác nhận** |
| **AD-09** | Thăm dò Sức khỏe Ollama & Hạ cấp | Activity | Ping cổng 11434, kiểm tra model, fallback NullLLM | UC-05, UC-06 | `ai_analysis/__main__.py:93-114`, `ollama.py` | **Đã xác nhận** |
| **AD-10** | Thu hồi Tài nguyên Tạm & Xử lý Lỗi | Activity | try...finally hook, rmtree; gỡ cờ chỉ đọc: chưa xác nhận | UC-02, UC-18, SD-01, SD-02 | `backend/src/cli.py:57-145`, `scanner.py:221-226` | **Đã xác nhận (gỡ cờ chỉ đọc khi rmtree trên Windows: chưa xác nhận, mã dùng ignore_errors=True)** |
| **SD-01** | Vòng đời Phiên phân tích (`AnalysisSession`) | State Machine | Vòng đời 10 trạng thái từ Idle đến Completed/Failed | UC-18, AD-01, AD-10 | `backend/src/cli.py:43-145` | **Đã xác nhận** |
| **SD-02** | Vòng đời Không gian Git (`GitCloneWorkspace`) | State Machine | Vòng đời 7 trạng thái từ Unallocated đến Purged (`InUse`) | UC-02, AD-02, AD-10 | `core_indexing/scanner.py:89-111, 221-226` | **Đã xác nhận** |
| **SD-03** | Vòng đời Ký hiệu Cú pháp (`ASTSymbolNode`) | State Machine | Vòng đời 7 trạng thái từ Discovered đến Rendered | UC-03, UC-04, UC-05, UC-15, AD-03, AD-04, AD-06 | `core_indexing/models.py:121-160`, `renderer.py:38-63` | **Đã xác nhận** |
| **SD-04** | Vòng đời Đồ thị Tri thức (`KnowledgeGraph`) | State Machine | Vòng đời 9 trạng thái từ Initialized đến Committed / ValidationFailed / WriteFailed | UC-08, AD-05 | `knowledge_graph/builder.py:64-360`, `models.py:74-95` | **Đã xác nhận** |
| **SD-05** | Vòng đời Trợ lý AI (`AskAIWidgetSession`) | State Machine | Vòng đời 7 trạng thái từ Idle đến Answered (Final khi đóng widget) | UC-22, AD-08 | `wiki_generation/templates/base.html:305-604` | **Đã xác nhận** |

---

## II. MA TRẬN TRUY VẾT HAI CHIỀU (BIDIRECTIONAL TRACEABILITY MATRIX)

### 1. Ma trận Use Case ↔ Quy trình Hoạt động (Use Case vs Activity Diagram)

| Use Case | AD-01 (Pipeline) | AD-02 (Git Clone) | AD-03 (AST Parse) | AD-04 (AI Bottom-Up) | AD-05 (Graph Build) | AD-06 (Wiki Render) | AD-07 (Search/Nav) | AD-08 (AI Chat) | AD-09 (Ollama Probe) | AD-10 (Cleanup) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **UC-01** (Scan Local) | ⬤ | | ⬤ | | | | | | | |
| **UC-02** (Scan Git) | ⬤ | ⬤ | ⬤ | | | | | | | ⬤ |
| **UC-03** (Java Parse) | | | ⬤ | | | | | | | |
| **UC-04** (C# Parse) | | | ⬤ | | | | | | | |
| **UC-05** (AI Summarize)| ⬤ | | | ⬤ | | | | | ⬤ | |
| **UC-06** (No-LLM) | ⬤ | | | | | | | | ⬤ | |
| **UC-08** (Build Graph) | ⬤ | | | | ⬤ | | | | | |
| **UC-10** (Wiki Pages) | ⬤ | | | | | ⬤ | | | | |
| **UC-15** (Symbol Pages)| ⬤ | | | | | ⬤ | | | | |
| **UC-16** (Search Index)| ⬤ | | | | | ⬤ | | | | |
| **UC-18** (CLI Run) | ⬤ | ⬤ | ⬤ | ⬤ | ⬤ | ⬤ | | | ⬤ | ⬤ |
| **UC-20** (Navigation) | | | | | | | ⬤ | | | |
| **UC-21** (Live Search) | | | | | | | ⬤ | | | |
| **UC-22** (Ask Local AI)| | | | | | | | ⬤ | | |

*Ghi chú:* Ký hiệu `⬤` biểu thị mối quan hệ phụ thuộc hoặc thực thi trực tiếp giữa Ca sử dụng và Quy trình Hoạt động.

---

### 2. Ma trận Quy trình Hoạt động ↔ Biểu đồ Trạng thái (Activity vs State Machine)

| Quy trình Hoạt động (Activity) | SD-01 (`AnalysisSession`) | SD-02 (`GitCloneWorkspace`) | SD-03 (`ASTSymbolNode`) | SD-04 (`KnowledgeGraph`) | SD-05 (`AskAIWidgetSession`) |
|---|:---:|:---:|:---:|:---:|:---:|
| **AD-01** (Pipeline Toàn bộ) | ⬤ (Quản lý toàn bộ vòng đời) | ⬤ (Cấp phát & dọn dẹp) | ⬤ (Chuyển tiếp ký hiệu) | ⬤ (Khởi tạo đến commit) | |
| **AD-02** (Git Clone) | ⬤ (Pha CloningRepository) | ⬤ (Allocating -> InUse) | | | |
| **AD-03** (AST Parse) | ⬤ (Pha Scanning) | ⬤ (Đọc tệp khi ở InUse) | ⬤ (Discovered -> Indexed) | | |
| **AD-04** (AI Bottom-Up) | ⬤ (Pha Analyzing) | | ⬤ (Chunked -> Summarized) | | |
| **AD-05** (Graph Build) | ⬤ (Pha BuildingGraph) | | ⬤ (Chuyển thành Graphed) | ⬤ (Initialized -> Committed) | |
| **AD-06** (Wiki Render) | ⬤ (Pha GeneratingWiki) | | ⬤ (Rendered trang symbol) | ⬤ (Nguồn dữ liệu kết xuất) | |
| **AD-07** (Search & Nav) | | | | | |
| **AD-08** (AI Chat Widget) | | | | | ⬤ (ProbingService → Answered) |
| **AD-09** (Ollama Health) | ⬤ (Quyết định chế độ AI, pha Analyzing) | | | | |
| **AD-10** (Cleanup Safe) | ⬤ (CleaningUp -> Terminals) | ⬤ (Releasing -> Purged) | | | |

---

## III. PHÂN LOẠI TRẠNG THÁI XÁC MINH CÁC CHỨC NĂNG NGHIỆP VỤ

Để tuân thủ tuyệt đối chuẩn mực Business Analysis chuyên nghiệp, chúng tôi phân loại toàn bộ các phát hiện và yêu cầu nghiệp vụ theo 3 nhóm minh bạch:

### 1. Nhóm Chức năng ĐÃ ĐƯỢC XÁC NHẬN trong Codebase (Confirmed Features)
- **Hỗ trợ 2 ngôn ngữ:** Chỉ có parser cho Java (`.java`) và C# (`.cs`) qua Tree-sitter.
- **Xử lý URL Git:** Tự động clone với `--depth 1` và dọn dẹp an toàn trong `finally`.
- **Phân cấp 6 tầng:** `Repository → Module → Container → Component → Class → Method`.
- **Trần ngân sách Token:** Giới hạn nghiêm ngặt 2000 tokens/prompt và cơ chế cắt tỉa khung xương.
- **Thẩm định tính toàn vẹn Đồ thị:** Cấm ID nút trùng lặp, cấm cạnh mồ côi, tự sinh nút `EXTERNAL` cho thư viện ngoài.
- **Lưu trữ nguyên tử:** Ghi tệp đệm tạm thời `.graph.tmp` rồi gọi `os.replace`.
- **Giao diện M3 Bento Grid:** Render 5 trang chính + các trang ký hiệu độc lập.
- **Tìm kiếm ngoại tuyến:** Tải `search_index.json` vào RAM, lọc 15 kết quả hàng đầu không cần server.
- **Widget AI nhúng:** Streaming phản hồi từ Ollama kèm cơ chế Intelligent Fallback khi mất mạng.

### 2. Nhóm Chức năng SUY LUẬN TỪ CODE nhưng Cần Lưu ý (Inferred Features)
- **Tương thích hệ điều hành Windows:** Lệnh gọi `os.startfile` được phân nhánh riêng cho Windows, trong khi Linux/macOS dùng `webbrowser.open`. (Mã nguồn đã chứng minh ở `cli.py:133-137`).
- **Gỡ cờ chỉ đọc khi `rmtree` trên Windows:** Chưa xác nhận (mã hiện tại dùng `shutil.rmtree(..., ignore_errors=True)` nuốt lỗi quyền chứ không chủ động gỡ cờ Read-Only rồi xóa lại).
- **Bộ nhớ đệm tóm tắt AI:** Hiện tại chưa có cơ chế lưu bộ đệm kết quả tóm tắt giữa các lần chạy khác nhau; mỗi lần chạy đều phân tích lại từ đầu.

### 3. Nhóm Chức năng CHƯA XÁC ĐỊNH hoặc ĐỀ XUẤT HOÀN THIỆN (Unverified / Proposals)
- **Kiểm tra sức khỏe Ollama định kỳ mỗi 30 giây:** Widget chat tự động thăm dò lại cổng 11434 sau mỗi 30s để cập nhật chấm xanh/đỏ (được ghi nhận từ kịch bản SD-05; chưa xác nhận trong mô tả mã ở UC).
- **Lỗi kết nối giữa chừng khi đang stream AI:** Phản hồi Ollama bị gián đoạn giữa luồng chưa có xử lý rõ ràng trong mã JS (chưa xác nhận; nếu `fetch` ném ngoại lệ hoặc `response.ok = false` thì chuyển sang nhánh dự phòng).
- **Ollama lỗi giữa chừng trong AD-04:** Xử lý khi Ollama gặp sự cố giữa chừng khi đang chạy vòng lặp tóm tắt phân cấp chưa được xác nhận trong mã.
- **Tải `search_index.json` qua giao thức `file://`:** Khi mở wiki bằng giao thức `file://`, nhiều trình duyệt hiện đại (đặc biệt Chrome) chặn `fetch` tệp cục bộ (cần lưu ý kiểm tra khi chạy thật).
- **Hỗ trợ ngôn ngữ bổ sung:** Các tài liệu sơ khai có nhắc đến C/C++, TypeScript hoặc Python nhưng trong source code hiện tại **hoàn toàn chưa có parser**.
- **Chế độ máy chủ thường trực (`repoatlas serve`):** Chưa tìm thấy mã nguồn triển khai cho lệnh `serve` để chia sẻ wiki qua mạng LAN.
- **Cơ chế xác thực tài khoản Git riêng tư:** Chưa có giao diện nhập token hoặc SSH passphrase nếu máy trạm chưa cấu hình trước.

---

## IV. HƯỚNG DẪN DÀNH CHO NGƯỜI VẼ BIỂU ĐỒ UML

Người tiếp nhận tài liệu kịch bản này có thể dựa trực tiếp vào các thông tin đã chuẩn hóa để vẽ các biểu đồ mà không cần đọc lại source code:

1. **Khi vẽ Use Case Diagram:**
   - Dùng mục **I của File 01** để xác định danh sách Actor (Kỹ sư phần mềm, Người đọc wiki, Git Server, Ollama Server, Browser/OS).
   - Kẻ đường bao hệ thống (System Boundary) bao toàn bộ 14 Use Case (kể cả Gói 6: UC-20, 21, 22).
   - Sử dụng quan hệ `<<include>>` và `<<extend>>` chính xác theo bảng tại **Mục III của File 01**.
   - Vẽ mũi tên kế thừa (Generalization) từ `Software Engineer` trỏ đến `Wiki User`.

2. **Khi vẽ Activity Diagram:**
   - Thiết lập số lượng và tên các **Swimlane** chính xác theo từng đề mục trong **File 02** (ví dụ AD-01 có 6 swimlanes, AD-03 có 4 swimlanes).
   - Đặt các **Decision Node** (hình thoi) với điều kiện bảo vệ ghi trong ngoặc vuông `[điều kiện]` tương ứng với các "Điểm quyết định" đã đánh số.
   - Sử dụng thanh **Fork / Join** song song cho quy trình AD-06 (biên dịch HTML chuyên đề và symbols).
   - Vẽ mũi tên luồng ngoại lệ dẫn về các điểm kết thúc thất bại đã định nghĩa rõ trong kịch bản.

3. **Khi vẽ State Machine Diagram:**
   - Xác định trạng thái ban đầu (Initial Pseudostate - chấm đen) và các trạng thái kết thúc (Final State - vòng tròn kép) theo danh mục trong **File 03**.
   - Chuyển từng dòng trong **Bảng chuyển trạng thái** thành một cung chuyển tiếp (Transition Arc).
   - Ghi nhãn chuyển trạng thái theo đúng chuẩn cú pháp UML:  
     `Sự_kiện [Điều_kiện_bảo_vệ] / Hành_động_thực_thi`.
   - Tuyệt đối không vẽ các đường chuyển tiếp nằm trong danh mục "Chuyển trạng thái bị cấm".
