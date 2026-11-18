# BÁO CÁO TOÀN DIỆN: KỊCH BẢN NGHIỆP VỤ OOAD HỆ THỐNG REPOATLAS

> **Vai trò:** Business Analyst (BA), OOAD Specialist & Software Architect  
> **Dự án đối chiếu:** [RepoAtlas (Wiki Generation)](file:///e:/FPT/Wiki%20Generation/README.md)  
> **Thư mục lưu trữ tài liệu:** [`docs/uml-analysis/business-scenarios/`](file:///e:/FPT/Wiki%20Generation/docs/uml-analysis/business-scenarios/)  
> **Mục tiêu:** Cung cấp tài liệu kịch bản nghiệp vụ bằng văn bản làm đầu vào chuẩn xác để người đọc tự vẽ:
> 1. Use Case Diagram
> 2. Activity Diagram
> 3. State Machine Diagram

> **Chỉ dẫn chung cho người vẽ**
> 1. Làm theo bộ file 00 → 04. README chỉ là bản rút gọn, không đủ 14 Use Case.
> 2. Mã UC không liên tục (thiếu 07, 09, 11–14, 17, 19) do giữ nguyên mã từ danh mục gốc; các mã thiếu không thuộc phạm vi vẽ.
> 3. Khi văn xuôi và bảng chuyển trạng thái khác nhau, **bảng chuyển trạng thái là chuẩn**.
> 4. Mục ghi "chưa xác nhận" thì không vẽ, hoặc vẽ nét đứt kèm ghi chú.
> 5. Các hàng "(Terminal)" trong bảng chuyển trạng thái: chỉ vẽ mũi tên từ trạng thái đó tới Final State, **không ghi nhãn**.
> 6. Chấm đen (Initial) nối vào: `Idle` (SD-01, SD-05), `Unallocated` (SD-02), `Discovered` (SD-03), `Initialized` (SD-04).
> 7. Mũi tên Generalization: từ Software Engineer (con) trỏ tới Wiki User (cha). Mũi tên `<<include>>`: từ UC gốc tới UC được include. Mũi tên `<<extend>>`: từ UC mở rộng tới UC gốc.
> 8. Khi mục “Actor” trong từng UC khác Bảng nối Actor–UC, bảng nối là chuẩn.
> 9. Các hàng chuyển tiếp từ trạng thái ban đầu (Initial / Chấm đen) tới trạng thái đầu tiên chỉ là mũi tên trần không ghi nhãn sự kiện.

---

## MỤC LỤC BÁO CÁO

- [PHẦN 1: KỊCH BẢN TỔNG QUAN BÀI TOÁN (ĐỀ BÀI THỰC TẾ OOAD)](#phần-1-kịch-bản-tổng-quan-bài-toán-đề-bài-thực-tế-ooad)
- [PHẦN 2: CÁC KỊCH BẢN USE CASE CHO MỤC TIÊU NGƯỜI DÙNG](#phần-2-các-kịch-bản-use-case-cho-mục-tiêu-người-dùng)
  - [1. Danh sách Tác nhân và Phân nhóm Chức năng](#1-danh-sách-tác-nhân-và-phân-nhóm-chức-năng)
  - [2. Đặc tả Kịch bản Use Case Trọng tâm](#2-đặc-tả-kịch-bản-use-case-trọng-tâm)
- [PHẦN 3: CÁC KỊCH BẢN QUY TRÌNH ĐỦ CHI TIẾT ĐỂ VẼ ACTIVITY DIAGRAM](#phần-3-các-kịch-bản-quy-trình-đủ-chi-tiết-để-vẽ-activity-diagram)
  - [Quy trình 1 (AD-01): Toàn bộ Đường ống Phân tích Repository và Khởi chạy Wiki](#quy-trình-1-ad-01-toàn-bộ-đường-ống-phân-tích-repository-và-khởi-chạy-wiki)
  - [Quy trình 2 (AD-02): Nhận diện URL và Clone Kho Mã nguồn Từ xa](#quy-trình-2-ad-02-nhận-diện-url-và-clone-kho-mã-nguồn-từ-xa)
  - [Quy trình 3 (AD-03): Quét Thư mục, Lọc Rác và Phân tích Cú pháp AST Đa Ngôn ngữ](#quy-trình-3-ad-03-quét-thư-mục-lọc-rác-và-phân-tích-cú-pháp-ast-đa-ngôn-ngữ)
  - [Quy trình 4 (AD-04): Phân khúc Cú pháp và Tóm tắt Phân cấp Bottom-Up với Quản trị Token](#quy-trình-4-ad-04-phân-khúc-cú-pháp-và-tóm-tắt-phân-cấp-bottom-up-với-quản-trị-token)
  - [Quy trình 5 (AD-05): Xây dựng, Bù trừ Nút Ngoại vi và Lưu trữ Đồ thị Tri thức Nguyên tử](#quy-trình-5-ad-05-xây-dựng-bù-trừ-nút-ngoại-vi-và-lưu-trữ-đồ-thị-tri-thức-nguyên-tử)
  - [Quy trình 6 (AD-06): Biên dịch Gói Tài liệu HTML và Tạo Chỉ mục Song song](#quy-trình-6-ad-06-biên-dịch-gói-tài-liệu-html-và-tạo-chỉ-mục-song-song)
  - [Quy trình 7 (AD-07): Điều hướng Thanh bên và Tìm kiếm Trực tiếp Ngoại tuyến Phía Trình duyệt](#quy-trình-7-ad-07-điều-hướng-thanh-bên-và-tìm-kiếm-trực-tiếp-ngoại-tuyến-phía-trình-duyệt)
  - [Quy trình 8 (AD-08): Tương tác Hỏi đáp Codebase và Truyền luồng Thời gian thực với Trợ lý AI](#quy-trình-8-ad-08-tương-tác-hỏi-đáp-codebase-và-truyền-luồng-thời-gian-thực-với-trợ-lý-ai)
  - [Quy trình 9 (AD-09): Thăm dò Sức khỏe Máy chủ Ollama và Hạ cấp An toàn sang Cấu trúc](#quy-trình-9-ad-09-thăm-dò-sức-khỏe-máy-chủ-ollama-và-hạ-cấp-an-toàn-sang-cấu-trúc)
  - [Quy trình 10 (AD-10): Thu hồi Tài nguyên Tạm thời và Xử lý Lỗi Toàn cục trong Pipeline](#quy-trình-10-ad-10-thu-hồi-tài-nguyên-tạm-thời-và-xử-lý-lỗi-toàn-cục-trong-pipeline)
- [PHẦN 4: CÁC KỊCH BẢN VÒNG ĐỜI ĐỐI TƯỢNG ĐỦ RÕ ĐỂ VẼ STATE MACHINE DIAGRAM](#phần-4-các-kịch-bản-vòng-đời-đối-tượng-đủ-rõ-để-vẽ-state-machine-diagram)
  - [Đối tượng 1: Phiên làm việc Phân tích (`AnalysisSession`)](#đối-tượng-1-phiên-làm-việc-phân-tích-analysissession)
  - [Đối tượng 2: Không gian Làm việc Git Tạm thời (`GitCloneWorkspace`)](#đối-tượng-2-không-gian-làm-việc-git-tạm-thời-gitcloneworkspace)
  - [Đối tượng 3: Ký hiệu Cú pháp Mã nguồn (`ASTSymbolNode`)](#đối-tượng-3-ký-hiệu-cú-pháp-mã-nguồn-astsymbolnode)
  - [Đối tượng 4: Đồ thị Tri thức Dự án (`KnowledgeGraph`)](#đối-tượng-4-đồ-thị-tri-thức-dự-án-knowledgegraph)
  - [Đối tượng 5: Phiên Tương tác Trợ lý AI trên Wiki (`AskAIWidgetSession`)](#đối-tượng-5-phiên-tương-tác-trợ-lý-ai-trên-wiki-askaiwidgetsession)
- [PHẦN 5: MA TRẬN ĐỐI CHIẾU VÀ HƯỚNG DẪN DỰNG MÔ HÌNH UML](#phần-5-ma-trận-đối-chiếu-và-hướng-dẫn-dựng-mô-hình-uml)

---

## PHẦN 1: KỊCH BẢN TỔNG QUAN BÀI TOÁN (ĐỀ BÀI THỰC TẾ OOAD)

Trong các doanh nghiệp phần mềm và các tổ chức công nghệ quy mô lớn, việc tiếp nhận, bảo trì hoặc tái cấu trúc các dự án mã nguồn khổng lồ là thách thức thường trực của các kỹ sư phần mềm. Thực tế cho thấy, tài liệu kỹ thuật của hầu hết các hệ thống thường bị bỏ quên, thiếu đồng bộ hoặc nhanh chóng trở nên lạc hậu so với mã nguồn thực tế đang vận hành. Khi một kỹ sư mới gia nhập dự án, họ thường phải mất nhiều tuần lễ chỉ để đọc lướt mã nguồn, cố gắng phỏng đoán cách tổ chức các gói phần mềm, lần theo các lời gọi hàm và tự phác thảo sơ đồ kiến trúc bằng tay. Các công cụ sinh tài liệu truyền thống chỉ dừng lại ở việc trích xuất văn bản ghi chú thủ công gắn liền với từng hàm hoặc lớp (như Javadoc hay XML Comments), hoàn toàn bất lực trong việc cung cấp một bức tranh toàn cảnh về kiến trúc đa tầng, sự phân rã mô-đun và các mối quan hệ phụ thuộc liên tệp của toàn bộ hệ thống.

Để giải quyết triệt để vấn đề này, một nhóm kiến trúc sư phần mềm quyết định xây dựng **RepoAtlas** — một hệ thống tự động phân tích sâu mã nguồn phần mềm và sản sinh bộ tài liệu kỹ thuật tĩnh đa trang tương tác (Static Wiki). Hệ thống phục vụ hai nhóm đối tượng người dùng chính: **Kỹ sư vận hành hệ thống** (Software Engineer) — người trực tiếp ra lệnh phân tích dự án thông qua giao diện dòng lệnh (CLI), và **Người đọc tài liệu kỹ thuật** (Wiki User / Solution Architect / QA Engineer) — những người khai thác, tra cứu và nghiên cứu kho tri thức dự án thông qua trình duyệt web trực quan. Giữa hai vai trò này tồn tại mối quan hệ kế thừa và mở rộng tự nhiên: chính kỹ sư phần mềm sau khi thực thi lệnh phân tích xong cũng sẽ trở thành người đọc tài liệu để kiểm tra và nghiên cứu kiến trúc dự án.

Để bắt đầu quá trình lập tài liệu, kỹ sư vận hành chỉ cần cung cấp địa chỉ của kho mã nguồn mục tiêu. Hệ thống hỗ trợ xử lý linh hoạt cả các thư mục dự án đang lưu trữ cục bộ trên máy tính lẫn các kho mã nguồn từ xa lưu trữ trên máy chủ Git thông qua giao thức truyền tải trực tuyến hoặc định danh rút gọn (`owner/repo`). Nếu đầu vào là một kho mã nguồn từ xa, hệ thống sẽ tự động khởi tạo một không gian làm việc an toàn, tiến hành tải bản sao tinh gọn của mã nguồn về đĩa cục bộ, thực hiện phân tích và cam kết dọn dẹp triệt để dữ liệu tạm thời ngay khi phiên làm việc kết thúc, bảo đảm không làm rò rỉ dữ liệu hoặc chiếm dụng bộ nhớ của máy trạm.

Quy trình phân tích mã nguồn được tổ chức theo đường ống xử lý một chiều tuần tự, phân tách nghiêm ngặt thành các giai đoạn nghiệp vụ độc lập nhưng kết nối chặt chẽ. Đầu tiên, hệ thống duyệt quét toàn bộ cấu trúc thư mục của dự án, tự động loại trừ các tệp tin rác, thư mục thư viện phụ thuộc và áp dụng triệt để các quy tắc bỏ qua đặc thù của dự án (từ tệp `.gitignore`). Tiếp theo, thay vì đọc chuỗi ký tự thô hay sử dụng các mẫu tìm kiếm biểu thức chính quy dễ sai sót, hệ thống sử dụng các bộ phân tích cú pháp chuyên biệt theo từng ngôn ngữ lập trình (hỗ trợ nền tảng Java và C#) để mổ xẻ cây cú pháp trừu tượng (Abstract Syntax Tree - AST). Quá trình này giúp nhận diện chính xác từng thực thể trong mã nguồn như gói không gian tên, lớp, giao diện, bảng liệt kê, cấu trúc dữ liệu, hàm xử lý, thuộc tính, trường dữ liệu, chú thích định danh kiến trúc đặc thù, cùng mạng lưới quan hệ đa chiều như kế thừa, cài đặt giao diện, lời gọi hàm và truy cập trường dữ liệu.

Sau khi đã hoàn tất lập chỉ mục ký hiệu cú pháp, dữ liệu được chuyển giao cho phân hệ phân tích phân cấp và tóm tắt thông minh. Hệ thống tự động phân loại cấu trúc mã nguồn theo một cây phân cấp sáu tầng chặt chẽ — từ cấp độ toàn bộ kho mã nguồn, xuống các phân hệ lớn, đơn vị triển khai phần mềm độc lập, nhóm thành phần chức năng, lớp cụ thể, và kết thúc ở từng phương thức chi tiết. Tại đây, hệ thống cho phép kỹ sư vận hành linh hoạt lựa chọn: kích hoạt trợ lý trí tuệ nhân tạo cục bộ (mô hình ngôn ngữ nhỏ chạy qua máy chủ Ollama trên máy trạm) để sinh tóm tắt ngôn ngữ tự nhiên từ dưới lên theo từng tầng phân cấp với sự quản lý nghiêm ngặt về giới hạn dung lượng từ ngữ (ngân sách không quá 2000 tokens cho mỗi yêu cầu), hoặc tự động hạ cấp an toàn sang chế độ tóm tắt cấu trúc xác định nếu máy chủ mô hình ngôn ngữ không khả dụng. Toàn bộ thông tin cấu trúc, mạng lưới phụ thuộc và nội dung tóm tắt sau đó được hội tụ vào một **Đồ thị Tri thức** (Knowledge Graph) duy nhất, được thẩm định tính toàn vẹn đa thực thể (nghiêm cấm cạnh mồ côi và trùng lặp định danh nút) và lưu trữ nguyên tử xuống ổ đĩa.

Tại giai đoạn hoàn tất, hệ thống chuyển hóa đồ thị tri thức và chỉ mục cú pháp thành một bộ trang web tài liệu tĩnh đa trang hoàn chỉnh và chuyên nghiệp. Bộ tài liệu bao gồm: Bảng điều khiển trung tâm hiển thị các chỉ số định lượng của dự án (Dashboard), Trang thông tin ngăn xếp công nghệ (Tech Stack), Trang kiến trúc đa tầng (Architecture), Trang phân rã các phân hệ và đơn vị triển khai (Modules), Trang hướng dẫn kiểm thử tự động (Tests), cùng hàng loạt trang hồ sơ chi tiết cho từng lớp và hàm nghiệp vụ. Đồng thời, hệ thống tự động khởi tạo một chỉ mục tìm kiếm ngoại tuyến siêu tốc và một tệp ngữ cảnh mở rộng, phục vụ tiện ích Trợ lý AI Cục bộ nhúng trực tiếp trên giao diện wiki. Tiện ích này cho phép người đọc đặt câu hỏi tự nhiên về dự án, tra cứu vị trí mã nguồn, nhận câu trả lời kèm siêu liên kết chính xác đến trang hồ sơ của ký hiệu mà không đòi hỏi bất kỳ dịch vụ máy chủ đám mây hay kết nối Internet nào.

Toàn bộ giải pháp hoạt động theo nguyên lý tự vận hành cục bộ (local-first, self-contained), bảo mật tuyệt đối mã nguồn độc quyền của doanh nghiệp, loại bỏ hoàn toàn chi phí bản quyền điện toán đám mây và mang lại tốc độ phản hồi tức thì cho người dùng.

### Căn cứ Phân tích từ Dự án
- [backend/src/cli.py](file:///e:/FPT/Wiki%20Generation/backend/src/cli.py#L43-L145): Điều phối 4 giai đoạn đường ống phân tích từ một lệnh duy nhất.
- [backend/src/core_indexing/scanner.py](file:///e:/FPT/Wiki%20Generation/backend/src/core_indexing/scanner.py#L89-L118): Xử lý phân giải URL Git từ xa và quét thư mục cục bộ.
- [backend/src/ai_analysis/models.py](file:///e:/FPT/Wiki%20Generation/backend/src/ai_analysis/models.py#L25-L53): Mô hình phân loại 6 tầng từ Repository đến Method.
- [backend/src/knowledge_graph/builder.py](file:///e:/FPT/Wiki%20Generation/backend/src/knowledge_graph/builder.py#L334-L360): Lưu trữ nguyên tử Đồ thị Tri thức.
- [backend/src/wiki_generation/templates/base.html](file:///e:/FPT/Wiki%20Generation/backend/src/wiki_generation/templates/base.html#L305-L604): Giao diện tương tác trực tiếp và widget Trợ lý AI.

---

## PHẦN 2: CÁC KỊCH BẢN USE CASE CHO MỤC TIÊU NGƯỜI DÙNG

### 1. Danh sách Tác nhân và Phân nhóm Chức năng

#### 1.1. Tác nhân (Actors)
- **Software Engineer (Kỹ sư Phần mềm - Actor chính):** Vận hành công cụ dòng lệnh (CLI), cung cấp đường dẫn mã nguồn, cấu hình tùy chọn và kích hoạt đường ống.
- **Wiki User (Người đọc Tài liệu - Actor chính):** Duyệt cây cấu trúc, tìm kiếm ký hiệu ngoại tuyến, đọc tài liệu chuyên đề và tương tác với Trợ lý AI.
  - *Mối quan hệ:* **Software Engineer kế thừa (Generalization) từ Wiki User.**
- **Git Remote Server (Máy chủ Git từ xa - Hệ thống ngoài):** Tiếp nhận yêu cầu tải mã nguồn tinh gọn (`git clone --depth 1`).
- **Ollama LLM Server (Máy chủ AI Cục bộ - Hệ thống ngoài):** Cung cấp API suy luận mô hình ngôn ngữ cục bộ tại cổng `11434`.
- **Web Browser & Host OS (Trình duyệt & Hệ điều hành - Hệ thống ngoài):** Khởi động hiển thị tệp HTML và cung cấp môi trường thực thi JavaScript.

#### 1.2. Phân nhóm Chức năng
1. *Core Indexing Subsystem:* Quét repository, lọc tệp, phân tích cú pháp AST Java/C#.
2. *AI Analysis Subsystem:* Phân khúc phân cấp 6 tầng, quản trị ngân sách token, tóm tắt bottom-up và hạ cấp cấu trúc.
3. *Knowledge Graph Subsystem:* Hợp nhất thực thể, bù trừ nút ngoại vi, thẩm định toàn vẹn và lưu trữ nguyên tử.
4. *Wiki Generation Subsystem:* Render HTML đa trang, render trang ký hiệu, sinh chỉ mục tìm kiếm và ngữ cảnh AI.
5. *CLI Orchestration Subsystem:* Đóng gói lệnh đơn, điều phối 4 phân hệ và khởi chạy trình duyệt.
6. *Wiki Interaction Subsystem:* Duyệt thanh bên, tìm kiếm trực tiếp và hội thoại AI trên web.

#### 1.3. Ma trận Quan hệ giữa các Use Case và Bảng nối Actor

##### 1. Quan hệ Bao gồm (`<<include>>`)
| Use Case Cơ sở | Quan hệ | Use Case Được bao gồm | Giải thích nghiệp vụ |
|---|:---:|---|---|
| **UC-18** | `<<include>>` | **UC-01** | Mọi lần chạy pipeline đều phải quét và lập chỉ mục mã nguồn trước tiên. |
| **UC-18** | `<<include>>` | **UC-05** | Mọi lần chạy đều phải tạo tóm tắt (UC-06 là phần mở rộng của UC-05, xem bên dưới). |
| **UC-18** | `<<include>>` | **UC-08** | Mọi lần chạy đều phải hợp nhất thành Đồ thị Tri thức. |
| **UC-18** | `<<include>>` | **UC-10, UC-15, UC-16** | Mọi lần chạy đều phải sinh các trang HTML, trang ký hiệu và chỉ mục. |
| **UC-01** | `<<include>>` | **UC-03, UC-04** | Quét thư mục luôn gọi parser AST cho từng tệp `.java` / `.cs`. |

##### 2. Quan hệ Mở rộng (`<<extend>>`)
| Use Case Mở rộng | Quan hệ | Use Case Cơ sở | Điều kiện kích hoạt (extension point) |
|---|:---:|---|---|
| **UC-06** (Tóm tắt cấu trúc) | `<<extend>>` | **UC-05** (Tóm tắt AI) | Cờ `--no-llm` được bật, hoặc kiểm tra sức khỏe Ollama thất bại. |
| **UC-02** (Phân tích từ Git URL) | `<<extend>>` | **UC-01** (Phân tích cục bộ) | Đầu vào được nhận diện là Git URL / shorthand `owner/repo`. |

> **Lưu ý:** không vẽ quan hệ nào giữa UC-21 và UC-22. UC-21 dùng `search_index.json`, UC-22 dùng `wiki_context.json`, hai UC độc lập. UC-16 chỉ là tiền điều kiện (cung cấp dữ liệu) cho UC-21 và UC-22, không vẽ mũi tên.

##### 3. Bảng nối Actor – Use Case
| Actor | Loại | Nối với UC |
|---|:---:|---|
| Software Engineer | Chính | UC-18, UC-01, UC-02 |
| Wiki User | Chính | UC-20, UC-21, UC-22 |
| Git Remote Server | Phụ | UC-02 |
| Ollama LLM Server | Phụ | UC-05, UC-22 |
| Web Browser & Host OS | Phụ | UC-18, UC-20, UC-21, UC-22 |

UC-03, 04, 06, 08, 10, 15, 16 là UC nội bộ do pipeline gọi: **không nối actor**, chỉ nối bằng include/extend.

---

### 2. Đặc tả Kịch bản Use Case Trọng tâm

#### UC-01: Phân tích Repository Cục bộ (Analyze Local Repository)
1. **Mã và tên:** UC-01 — Phân tích Repository Cục bộ.
2. **Mục tiêu nghiệp vụ:** Quét cấu trúc thư mục, nhận diện toàn bộ tệp nguồn Java/C# trên máy tính và trích xuất bảng chỉ mục ký hiệu AST.
3. **Actor:** Software Engineer (A1).
4. **Bối cảnh sử dụng:** Kỹ sư phần mềm cần lập tài liệu cho một thư mục dự án đang có sẵn trên máy làm việc.
5. **Tiền điều kiện:** Đường dẫn thư mục cục bộ tồn tại, có quyền đọc và chứa ít nhất một tệp `.java` hoặc `.cs`.
6. **Sự kiện kích hoạt:** Kỹ sư phần mềm chạy lệnh `repoatlas analyze <local_path>`.
7. **Luồng xử lý chính:**
   - *Bước 1:* CLI tiếp nhận tham số và xác định đây là đường dẫn thư mục cục bộ.
   - *Bước 2:* Hệ thống kiểm tra sự tồn tại và tính hợp lệ của thư mục trên đĩa cứng.
   - *Bước 3:* Hệ thống tải các quy tắc loại trừ trong tệp `.gitignore` (nếu có).
   - *Bước 4:* Hệ thống duyệt đệ quy cây thư mục, bỏ qua các thư mục trong danh sách loại trừ mặc định (`DEFAULT_EXCLUDES`), dựng cây thư mục `DirectoryNode`.
   - *Bước 5:* Hệ thống ghi cây cấu trúc ra tệp `indexes/structure.json`.
   - *Bước 6:* Hệ thống duyệt từng tệp nguồn `.java` và `.cs`, kích hoạt bộ phân tích AST tương ứng (gọi UC-03 hoặc UC-04) để trích xuất ký hiệu và quan hệ.
   - *Bước 7:* Hệ thống tổng hợp các chỉ mục tệp thành `RepositoryIndex`.
   - *Bước 8:* Hệ thống xuất khẩu dữ liệu ra `indexes/repository_index.json` và `indexes/structure_overview.json`.
8. **Luồng thay thế:**
   - *Alt 1a — Không có tệp `.gitignore`:* Hệ thống bỏ qua bộ lọc tùy biến và chỉ áp dụng danh sách loại trừ mặc định.
   - *Alt 1b — Một số tệp bị lỗi cú pháp:* Hệ thống ghi nhận cảnh báo cho tệp đó, bỏ qua và tiếp tục phân tích các tệp còn lại.
9. **Luồng ngoại lệ:**
   - *Exc 1a — Đường dẫn cục bộ không tồn tại:* Hệ thống thông báo lỗi `Khong tim thay duong dan`, dừng phiên làm việc.
   - *Exc 1b — Không có quyền truy cập thư mục:* Hệ thống dừng lại và thông báo lỗi phân quyền hệ điều hành.
10. **Hậu điều kiện:** Thư mục `indexes/` chứa đầy đủ 3 tệp tin `structure.json`, `repository_index.json` và `structure_overview.json`.
11. **Quy tắc nghiệp vụ:** Chỉ nhận diện tệp đuôi `.java` và `.cs`. Bắt buộc cô lập lỗi từng tệp để không làm gián đoạn toàn bộ dự án.
12. **Điểm chưa xác nhận:** Chưa xác nhận cơ chế quét tăng dần (incremental indexing) khi chỉ một vài tệp bị sửa đổi.
13. **Căn cứ phân tích:** [backend/src/core_indexing/scanner.py:113-118](file:///e:/FPT/Wiki%20Generation/backend/src/core_indexing/scanner.py#L113-L118), [scanner.py:184-219](file:///e:/FPT/Wiki%20Generation/backend/src/core_indexing/scanner.py#L184-L219), [backend/src/core_indexing/ir_generator.py:17-48](file:///e:/FPT/Wiki%20Generation/backend/src/core_indexing/ir_generator.py#L17-L48).

---

#### UC-02: Phân tích Repository từ Git URL (Analyze Remote Git Repository)
1. **Mã và tên:** UC-02 — Phân tích Repository từ Git URL.
2. **Mục tiêu nghiệp vụ:** Tải bản sao tinh gọn của repository từ xa vào không gian tạm thời, thực hiện phân tích cú pháp và đảm bảo dọn dẹp sạch sẽ thư mục tạm sau khi hoàn tất.
3. **Actor chính và phụ:** Software Engineer (Actor chính), Git Remote Server (Actor phụ).
4. **Bối cảnh sử dụng:** Kỹ sư phần mềm cần lập tài liệu cho một dự án lưu trên GitHub/GitLab mà chưa tải về máy trạm.
5. **Tiền điều kiện:** Máy trạm có kết nối mạng Internet, đã cài đặt công cụ dòng lệnh Git; địa chỉ URL hợp lệ và có quyền truy cập.
6. **Sự kiện kích hoạt:** Kỹ sư chạy lệnh `repoatlas analyze <git_url>` hoặc `repoatlas analyze owner/repo`.
7. **Luồng xử lý chính:**
   - *Bước 1:* CLI nhận diện chuỗi tham số là URL Git hoặc định danh rút gọn.
   - *Bước 2:* Nếu là dạng shorthand `owner/repo`, hệ thống chuẩn hóa thành `https://github.com/owner/repo.git`.
   - *Bước 3:* Hệ thống cấp phát thư mục tạm thời trên ổ đĩa (`tempfile.mkdtemp(prefix="repoatlas_repo_")`).
   - *Bước 4:* Hệ thống gọi tiến trình Git tải bản sao nông: `git clone --depth 1 <url> <temp_dir>`.
   - *Bước 5:* Máy chủ Git từ xa truyền dữ liệu commit mới nhất về thư mục tạm.
   - *Bước 6:* Sau khi tải xong, hệ thống thiết lập đường dẫn dự án trỏ vào thư mục tạm và tiến hành quét như UC-01.
   - *Bước 7:* Khối kết thúc bắt buộc (`finally`) triệu gọi hàm dọn dẹp để xóa sạch thư mục tạm thời trên đĩa.
8. **Luồng thay thế:**
   - *Alt 2a — Chuỗi URL sử dụng giao thức SSH (`git@...`):* Hệ thống giữ nguyên chuỗi kết nối và thực thi clone qua SSH.
9. **Luồng ngoại lệ:**
   - *Exc 2a — Lỗi kết nối mạng, sai URL hoặc kho private không có quyền:* Lệnh clone trả về lỗi, hệ thống xóa ngay thư mục tạm, ném `ValueError` kèm thông báo stderr từ Git và dừng pipeline.
10. **Hậu điều kiện:** Dữ liệu chỉ mục được ghi trọn vẹn vào `indexes/`; thư mục tạm thời được xóa sạch hoàn toàn khỏi ổ đĩa.
11. **Quy tắc nghiệp vụ:** Bắt buộc dùng cờ `--depth 1` để tiết kiệm băng thông và dung lượng đĩa. Thao tác dọn dẹp thư mục tạm phải nằm trong khối `finally`.
12. **Điểm chưa xác nhận:** Chưa có giao diện dòng lệnh cho phép nhập mật khẩu / Token cá nhân tương tác nếu kho Git ở chế độ riêng tư.
13. **Căn cứ phân tích:** [backend/src/core_indexing/scanner.py:70-87](file:///e:/FPT/Wiki%20Generation/backend/src/core_indexing/scanner.py#L70-L87), [scanner.py:89-111](file:///e:/FPT/Wiki%20Generation/backend/src/core_indexing/scanner.py#L89-L111), [scanner.py:221-226](file:///e:/FPT/Wiki%20Generation/backend/src/core_indexing/scanner.py#L221-L226).

---

#### UC-05: Tóm tắt Phân cấp Mã nguồn bằng AI (Hierarchical Summarization via Local LLM)
1. **Mã và tên:** UC-05 — Tóm tắt Phân cấp Mã nguồn bằng Mô hình Ngôn ngữ Cục bộ.
2. **Mục tiêu nghiệp vụ:** Sử dụng máy chủ Ollama chạy trên máy trạm để sinh tóm tắt ngôn ngữ tự nhiên từ dưới lên theo 6 tầng phân cấp, kiểm soát chặt chẽ ngân sách token dưới 2000 tokens và kiểm tra chống ảo giác.
3. **Actor chính và phụ:** Software Engineer (Actor chính), Ollama LLM Server (Actor phụ).
4. **Bối cảnh sử dụng:** Được kích hoạt ở giai đoạn 2 của pipeline khi chế độ AI được bật (`use_llm = True`).
5. **Tiền điều kiện:** Tệp `indexes/repository_index.json` đã tồn tại; Ollama đang chạy tại `http://localhost:11434` với model `qwen2.5-coder:3b`.
6. **Sự kiện kích hoạt:** Hệ thống chuyển sang giai đoạn AI Analysis trong pipeline.
7. **Luồng xử lý chính:**
   - *Bước 1:* Hệ thống thực hiện kiểm tra kết nối (health check) đến cổng dịch vụ Ollama.
   - *Bước 2:* Hệ thống nạp bảng chỉ mục và dựng cây phân cấp 6 tầng (`Repository → Module → Container → Component → Class → Method`).
   - *Bước 3:* Hệ thống sắp xếp các nút theo thứ tự duyệt từ dưới lên (Bottom-Up: Method trước, rồi Class, Component, Container, Module, Repository).
   - *Bước 4:* Với mỗi nút tầng Method và Class, hệ thống trích xuất khung xương cú pháp AST (loại bỏ phần thân hàm).
   - *Bước 5:* Hệ thống tính toán lượng token ước tính; nếu vượt quá 2000 tokens, tự động cắt tỉa phần chữ ký phụ để đảm bảo vừa ngân sách.
   - *Bước 6:* Hệ thống đóng gói prompt và gửi yêu cầu suy luận đến Ollama API.
   - *Bước 7:* Ollama trả về văn bản tóm tắt tự nhiên giải thích vai trò của thành phần.
   - *Bước 8:* Hệ thống thẩm định chống ảo giác: đối chiếu các tên ký hiệu được nhắc đến trong văn bản với bảng chỉ mục; chỉ lưu các ký hiệu thực sự tồn tại vào `referenced_symbols`.
   - *Bước 9:* Với các tầng cao hơn, hệ thống sử dụng bản tóm tắt tổng hợp từ các nút con cấp dưới làm ngữ cảnh tóm tắt cho nút cha.
   - *Bước 10:* Bộ sinh nội dung chuyên đề tạo 4 phần nội dung (`tech`, `tests`, `architecture`, `modules`) và ghi toàn bộ ra `analysis/summaries.json`.
8. **Luồng thay thế:**
   - *Alt 5a — Dịch vụ Ollama ngoại tuyến hoặc thiếu model:* Hệ thống tự động kích hoạt quan hệ `<<extend>>` chuyển sang UC-06 (Tóm tắt Cấu trúc Dự phòng).
9. **Luồng ngoại lệ:**
   - *Exc 5a — Tệp chỉ mục đầu vào bị thiếu:* Hệ thống ném `FileNotFoundError` và dừng quy trình.
10. **Hậu điều kiện:** Tệp `analysis/summaries.json` được tạo thành công, chứa toàn bộ tóm tắt AI cho từng nút và nội dung 4 chuyên đề wiki.
11. **Quy tắc nghiệp vụ:** Mọi prompt gửi cho Ollama không được vượt quá 2000 tokens. Quá trình tóm tắt bắt buộc phải theo chiều Bottom-Up.
12. **Điểm chưa xác nhận:** Chưa xác nhận cơ chế lưu cache tóm tắt giữa các lần chạy khác nhau nếu mã nguồn phương thức không đổi.
13. **Căn cứ phân tích:** [backend/src/ai_analysis/__main__.py:93-167](file:///e:/FPT/Wiki%20Generation/backend/src/ai_analysis/__main__.py#L93-L167), [backend/src/ai_analysis/summarizer.py](file:///e:/FPT/Wiki%20Generation/backend/src/ai_analysis/summarizer.py), [backend/src/ai_analysis/chunker.py](file:///e:/FPT/Wiki%20Generation/backend/src/ai_analysis/chunker.py), [backend/src/ai_analysis/llm/ollama.py](file:///e:/FPT/Wiki%20Generation/backend/src/ai_analysis/llm/ollama.py).

---

#### UC-08: Xây dựng và Thẩm định Đồ thị Tri thức Đa thực thể (Build & Validate Knowledge Graph)
1. **Mã và tên:** UC-08 — Xây dựng và Thẩm định Đồ thị Tri thức Đa thực thể.
2. **Mục tiêu nghiệp vụ:** Hợp nhất siêu dữ liệu mã nguồn AST và nội dung tóm tắt phân cấp thành một đồ thị tri thức duy nhất, tự động bù trừ các nút thư viện ngoài, thẩm định tính toàn vẹn và ghi tệp nguyên tử xuống đĩa.
3. **Actor:** Software Engineer (thông qua điều phối pipeline).
4. **Bối cảnh sử dụng:** Kích hoạt tại Giai đoạn 3 của pipeline.
5. **Tiền điều kiện:** Thư mục `indexes/` và `analysis/` đã có dữ liệu hợp lệ.
6. **Sự kiện kích hoạt:** Giai đoạn AI Analysis hoàn tất.
7. **Luồng xử lý chính:**
   - *Bước 1:* Phân hệ nạp dữ liệu từ `repository_index.json` và `summaries.json`.
   - *Bước 2:* Khởi tạo nút gốc đại diện cho toàn bộ kho mã nguồn (`repository:<name>`).
   - *Bước 3:* Tạo các nút tệp nguồn (`file:<path>`) và nút ký hiệu AST (`symbol:<fqn>`).
   - *Bước 4:* Hệ thống nạp cây phân loại, tạo các nút nhóm cấu trúc Module, Container, Component và gắn quan hệ chứa đựng.
   - *Bước 5:* Hệ thống duyệt danh sách quan hệ và tạo các cạnh có hướng: chứa đựng (`contains`), kế thừa (`extends`), cài đặt (`implements`), gọi phương thức (`calls`), sử dụng trường (`uses_field`).
   - *Bước 6:* Với mỗi cạnh trỏ đến lớp/thư viện ngoài dự án (SDK, thư viện bên thứ ba), hệ thống tự động sinh nút giả lập ngoại vi (`type = EXTERNAL`, `external = True`) rồi mới tạo cạnh.
   - *Bước 7:* Hệ thống gắn nội dung tóm tắt vào thuộc tính `metadata.summary` của từng nút.
   - *Bước 8:* Hệ thống thẩm định tính toàn vẹn: không trùng `id` nút, không có cạnh mồ côi.
   - *Bước 9:* Hệ thống ghi đĩa nguyên tử: ghi vào tệp tạm `.graph.tmp` trong `graphs/`, rồi `os.replace` thành `graphs/graph.json`.
8. **Luồng thay thế:**
   - *Alt 8a — Chạy ở chế độ không có AI:* Đồ thị vẫn được xây dựng từ chỉ mục và cây thư mục, bỏ trống trường summary.
9. **Luồng ngoại lệ:**
   - *Exc 8a — Thẩm định toàn vẹn thất bại (trùng ID nút hoặc cạnh mồ côi):* ném `ValueError`, dừng pipeline. Lúc này **chưa tạo tệp tạm** nên chưa có gì để hủy.
   - *Exc 8b — Lỗi ghi đĩa khi đang ghi tệp tạm:* xóa tệp tạm trong khối `finally`, dừng pipeline.
10. **Hậu điều kiện:** Tệp `graphs/graph.json` được tạo thành công, đảm bảo 100% tính toàn vẹn cấu trúc.
11. **Quy tắc nghiệp vụ:** Tuyệt đối cấm tồn tại cạnh mồ côi. Quá trình ghi tệp bắt buộc phải là thao tác nguyên tử.
12. **Điểm chưa xác nhận:** Chưa xác nhận API truy vấn đồ thị độc lập theo chuẩn GraphQL hoặc SPARQL.
13. **Căn cứ phân tích:** [backend/src/knowledge_graph/builder.py:64-322](file:///e:/FPT/Wiki%20Generation/backend/src/knowledge_graph/builder.py#L64-L322), [builder.py:334-360](file:///e:/FPT/Wiki%20Generation/backend/src/knowledge_graph/builder.py#L334-L360), [backend/src/knowledge_graph/models.py:74-95](file:///e:/FPT/Wiki%20Generation/backend/src/knowledge_graph/models.py#L74-L95).

---

#### UC-18: Thực thi Toàn bộ Đường ống Phân tích Tự động (Run Full Analysis Pipeline)
1. **Mã và tên:** UC-18 — Thực thi Toàn bộ Đường ống Phân tích Tự động.
2. **Mục tiêu nghiệp vụ:** Cho phép kỹ sư phần mềm chạy toàn bộ quy trình 4 giai đoạn và tự động mở trình duyệt hiển thị kết quả chỉ bằng một lệnh dòng lệnh duy nhất.
3. **Actor chính và phụ:** Software Engineer (Actor chính), Git Server, Ollama Server, Web Browser & Host OS (Các hệ thống ngoài).
4. **Bối cảnh sử dụng:** Kỹ sư phần mềm cần lập tài liệu nhanh chóng cho một codebase.
5. **Tiền điều kiện:** Máy trạm đã cài đặt Python 3.10+ cùng các thư viện phụ thuộc.
6. **Sự kiện kích hoạt:** Kỹ sư gõ lệnh `repoatlas analyze <path|url> [--no-llm]`.
7. **Luồng xử lý chính:**
   - *Bước 1:* CLI tiếp nhận tham số và phân tích các cờ tùy chọn.
   - *Bước 2:* Gọi UC-01 (UC-02 mở rộng khi là Git URL) để xác định loại địa chỉ, quét mã nguồn và lập chỉ mục AST ra `indexes/`.
   - *Bước 3 (Gọi UC-05/UC-06):* Phân cấp taxonomy và tóm tắt theo chế độ tương ứng ra `analysis/`.
   - *Bước 4 (Gọi UC-08):* Hợp nhất tri thức và xây dựng Đồ thị Tri thức ra `graphs/`.
   - *Bước 5:* Kết xuất toàn bộ các trang chuyên đề, các trang chi tiết ký hiệu, sinh `search_index.json` và `wiki_context.json` ra thư mục `wiki/`.
   - *Bước 6:* In thông báo phân tích thành công lên terminal.
   - *Bước 7:* Nhận diện hệ điều hành: nếu là Windows dùng `os.startfile(wiki/index.html)`, nếu là Linux/macOS dùng `webbrowser.open()`.
   - *Bước 8:* Trình duyệt web tự động khởi động và hiển thị Bảng điều khiển `wiki/index.html`.
   - *Bước 9:* Thực thi khối `finally` dọn dẹp thư mục tạm nếu có tải từ Git.
8. **Luồng thay thế:**
   - *Alt 8a — Trình duyệt không thể tự mở (môi trường server không có GUI):* Bắt ngoại lệ, in đường dẫn tuyệt đối hướng dẫn người dùng tự mở tệp.
9. **Luồng ngoại lệ:**
   - *Exc 9a — Lỗi tại bất kỳ giai đoạn nào:* Pipeline dừng ngay, khối `finally` vẫn dọn dẹp tài nguyên và in lỗi ra màn hình.
10. **Hậu điều kiện:** Bộ wiki tĩnh hoàn chỉnh sẵn sàng phục vụ và hiển thị ngay trên trình duyệt máy trạm.
11. **Quy tắc nghiệp vụ:** Khối dọn dẹp `cleanup` bắt buộc phải luôn luôn được thực thi trong khối `finally`.
12. **Điểm chưa xác nhận:** Chưa xác nhận tùy chọn chạy dưới dạng máy chủ dịch vụ nền (daemon service) với lệnh `repoatlas serve`.
13. **Căn cứ phân tích:** [backend/src/cli.py:43-145](file:///e:/FPT/Wiki%20Generation/backend/src/cli.py#L43-L145), [cli.py:152-179](file:///e:/FPT/Wiki%20Generation/backend/src/cli.py#L152-L179).

---

#### UC-21: Tìm kiếm Ký hiệu Trực tiếp Ngoại tuyến (Client-side Live Search)
1. **Mã và tên:** UC-21 — Tìm kiếm Ký hiệu Trực tiếp Ngoại tuyến.
2. **Mục tiêu nghiệp vụ:** Cung cấp thanh tìm kiếm nhanh trên giao diện web, lọc và hiển thị tức thời danh sách các lớp, phương thức hoặc trang chuyên đề khớp với từ khóa mà không cần gọi máy chủ backend.
3. **Actor chính và phụ:** Wiki User (Actor chính), Web Browser (Actor phụ).
4. **Bối cảnh sử dụng:** Người đọc cần định vị nhanh vị trí của một lớp hoặc hàm nghiệp vụ khi đang xem wiki.
5. **Tiền điều kiện:** Trang wiki đã tải xong và đã nạp `search_index.json` vào bộ nhớ RAM của trình duyệt.
6. **Sự kiện kích hoạt:** Người đọc nhấp chuột vào ô tìm kiếm và bắt đầu gõ ký tự.
7. **Luồng xử lý chính:**
   - *Bước 1:* Người đọc gõ ký tự vào ô tìm kiếm ở thanh đầu trang.
   - *Bước 2:* Sự kiện `input` kích hoạt, mã JavaScript chuyển chuỗi tìm kiếm thành chữ thường và cắt bỏ khoảng trắng.
   - *Bước 3:* Nếu ô tìm kiếm rỗng, danh sách kết quả tự động ẩn đi.
   - *Bước 4:* Nếu có từ khóa, thuật toán duyệt qua mảng `searchIndex` trong bộ nhớ, lọc ra tối đa 15 mục có tên chứa chuỗi từ khóa.
   - *Bước 5:* Hệ thống hiển thị hộp danh sách kết quả thả xuống ngay dưới ô tìm kiếm.
   - *Bước 6:* Người đọc nhấp chuột vào một kết quả mong muốn trong danh sách.
   - *Bước 7:* Trình duyệt chuyển hướng ngay sang trang chi tiết của ký hiệu hoặc trang chuyên đề tương ứng.
8. **Luồng thay thế:**
   - *Alt 21a — Không tìm thấy kết quả phù hợp:* Hiển thị thông báo "No results found".
   - *Alt 21b — Nhấp chuột ra ngoài ô tìm kiếm:* Hộp danh sách tự động ẩn đi.
9. **Luồng ngoại lệ:**
   - *Exc 21a — `search_index.json` không nạp được:* trình duyệt ghi lỗi vào Console, tìm kiếm tạm thời không khả dụng. **Lưu ý kỹ thuật (cần kiểm tra khi chạy thật):** khi mở wiki bằng giao thức `file://`, nhiều trình duyệt hiện đại (đặc biệt Chrome) chặn `fetch` tệp cục bộ.
10. **Hậu điều kiện:** Người đọc định vị và mở được trang tài liệu của ký hiệu mong muốn tức thì.
11. **Quy tắc nghiệp vụ:** Tìm kiếm không phân biệt chữ hoa/thường; giới hạn tối đa 15 kết quả hàng đầu.
12. **Điểm chưa xác nhận:** Chưa xác nhận thuật toán tìm kiếm mờ (Fuzzy search theo khoảng cách Levenshtein).
13. **Căn cứ phân tích:** [backend/src/wiki_generation/templates/base.html:240-244](file:///e:/FPT/Wiki%20Generation/backend/src/wiki_generation/templates/base.html#L240-L244), [base.html:251-290](file:///e:/FPT/Wiki%20Generation/backend/src/wiki_generation/templates/base.html#L251-L290).

---

#### UC-22: Tương tác Hỏi đáp Codebase với Trợ lý AI Cục bộ Nhúng (Ask Local AI Widget)
1. **Mã và tên:** UC-22 — Tương tác Hỏi đáp Codebase với Trợ lý AI Cục bộ Nhúng.
2. **Mục tiêu nghiệp vụ:** Cung cấp tiện ích hội thoại thông minh nhúng trên từng trang wiki, cho phép người đọc hỏi về kiến trúc, luồng xử lý hoặc vị trí thành phần bằng ngôn ngữ tự nhiên; trợ lý sẽ tự động trích xuất ngữ cảnh liên quan và truyền luồng câu trả lời thời gian thực từ Ollama hoặc cung cấp câu trả lời từ tri thức nội bộ nếu Ollama ngoại tuyến.
3. **Actor chính và phụ:** Wiki User (Actor chính), Ollama LLM Server, Web Browser (Các actor phụ).
4. **Bối cảnh sử dụng:** Người đọc cần một trợ lý giải thích nghiệp vụ tổng thể hoặc chỉ dẫn cụ thể về chức năng của codebase.
5. **Tiền điều kiện:** Người đọc đang mở trang wiki; tệp `wiki_context.json` đã được nạp thành công vào trình duyệt.
6. **Sự kiện kích hoạt:** Người đọc nhấp vào nút nổi (Floating Button) Trợ lý AI ở góc dưới bên phải màn hình.
7. **Luồng xử lý chính:**
   - *Bước 1:* Khung trò chuyện hiển thị trên màn hình.
   - *Bước 2:* JavaScript gửi yêu cầu ngầm kiểm tra sức khỏe dịch vụ Ollama (`fetch("http://localhost:11434/api/tags")`): cập nhật chấm trạng thái màu xanh ("Ollama online") hoặc màu đỏ ("Ollama offline").
   - *Bước 3:* Người đọc nhập câu hỏi tự nhiên và nhấn nút Gửi (hoặc nhấn Enter).
   - *Bước 4:* Câu hỏi hiển thị vào khung chat và xuất hiện bong bóng thông báo "Đang suy nghĩ...".
   - *Bước 5:* Hệ thống phân tích ý định (Intent Detection) và tách từ khóa từ câu hỏi (loại bỏ từ dừng thông thường).
   - *Bước 6:* Thuật toán tính điểm (Scoring Algorithm) rà soát các ký hiệu và chuyên đề trong `wiki_context.json`, chọn lọc ra 12 ký hiệu và 3 chuyên đề có điểm số cao nhất.
   - *Bước 7:* Hệ thống đóng gói câu lệnh nhắc kèm ngữ cảnh và gửi yêu cầu dạng luồng (`stream: true`) đến cổng API Ollama.
   - *Bước 8:* Ollama tiếp nhận và truyền từng đoạn token văn bản trả lời về trình duyệt; khung chat hiển thị văn bản theo thời gian thực.
   - *Bước 9:* Câu trả lời hoàn tất hiển thị kèm theo các liên kết có thể nhấp vào để mở ngay trang chi tiết ký hiệu liên quan.
8. **Luồng thay thế:**
   - *Alt 22a — Dịch vụ Ollama ngoại tuyến (CORS hoặc server tắt):* Kích hoạt cơ chế Chuyển đổi Dự phòng Thông minh (Intelligent Fallback):
     - Nếu hỏi thống kê/đếm: Hiển thị tổng số lớp, số hàm, ngôn ngữ và danh sách 30 ký hiệu tiêu biểu kèm liên kết.
     - Nếu có ký hiệu khớp từ khóa: Hiển thị danh thiếp tóm tắt của các ký hiệu khớp (tên, chữ ký, đường dẫn tệp, docstring) kèm siêu liên kết mở trang chi tiết.
     - Nếu không có ký hiệu khớp: Hiển thị bản tóm tắt tổng quan kiến trúc codebase.
     - Hiển thị hộp chỉ dẫn lệnh PowerShell để người dùng khởi động Ollama khi cần thiết.
     - Cập nhật nội dung dự phòng vào khung chat.
   - *Alt 22b — Ollama trực tuyến nhưng thiếu model `qwen2.5-coder:3b`:* hiển thị chấm đỏ, xử lý như Alt 22a (dùng tri thức nội bộ).
   - *Alt 22c — Kiểm tra sức khỏe định kỳ mỗi 30 giây:* chấm trạng thái tự cập nhật khi Ollama bật/tắt. (Ghi nhận từ SD-05; chưa xác nhận trong mô tả mã ở UC.)
9. **Luồng ngoại lệ:** Trình duyệt chặn truy vấn Cross-Origin (CORS) khi gọi đến cổng 11434 (hướng dẫn cấu hình `$env:OLLAMA_ORIGINS="*" ; ollama serve`).
10. **Hậu điều kiện:** Người đọc nhận được câu trả lời chính xác giải đáp thắc mắc về codebase kèm siêu liên kết dẫn chứng cụ thể.
11. **Quy tắc nghiệp vụ:** Trợ lý AI cam kết không bịa đặt: chỉ trả lời dựa trên thông tin chỉ mục thực tế trong `wiki_context.json`. Nếu không có AI, hệ thống hoạt động như một công cụ tìm kiếm ngữ nghĩa nội bộ.
12. **Điểm chưa xác nhận:** Chưa xác nhận tính năng lưu lại lịch sử các phiên chat trước đó vào LocalStorage của trình duyệt khi đóng trang web.
13. **Căn cứ phân tích:** [backend/src/wiki_generation/templates/base.html:305-604](file:///e:/FPT/Wiki%20Generation/backend/src/wiki_generation/templates/base.html#L305-L604).

---

## PHẦN 3: CÁC KỊCH BẢN QUY TRÌNH ĐỦ CHI TIẾT ĐỂ VẼ ACTIVITY DIAGRAM

### Quy trình 1 (AD-01): Toàn bộ Đường ống Phân tích Repository và Khởi chạy Wiki
- **Mục tiêu:** Điều phối tự động chuỗi 4 phân hệ chức năng từ tiếp nhận đầu vào đến khi website tài liệu HTML tĩnh được khởi chạy trên trình duyệt người dùng.
- **Swimlanes (06 Phân làn):**
  1. `Software Engineer`: Nhập lệnh và tiếp nhận giao diện tài liệu.
  2. `CLI Orchestrator`: Điều phối trung tâm, kiểm tra tham số, phân luồng thực thi.
  3. `Core Indexing Engine`: Quét cấu trúc thư mục và phân tích AST Java/C#.
  4. `AI Analysis Engine`: Phân khúc 6 tầng và sinh tóm tắt thông minh.
  5. `Knowledge Graph Builder`: Hợp nhất tri thức và thẩm định đồ thị.
  6. `Wiki Generator & Browser`: Render HTML đa trang và hiển thị trên trình duyệt.
- **Trình tự hành động và rẽ nhánh chi tiết:**
  1. `[Software Engineer]` Nhập lệnh `repoatlas analyze <path|url> [--no-llm]`.
  2. `[CLI Orchestrator]` Phân tích đối số: lấy `target_path` và thiết lập `use_llm = not args.no_llm`.
  3. `[CLI Orchestrator]` **[Điểm quyết định 1]:** `target_path` có phải là Git URL hoặc GitHub shorthand không?
     - *Đúng:* Chuyển sang Quy trình 2 để clone mã nguồn từ xa về máy cục bộ.
     - *Sai:* Kiểm tra đường dẫn trên ổ đĩa máy tính:
       - **[Điểm quyết định 2]:** Thư mục cục bộ có tồn tại không?
         - *Không tồn tại:* In thông báo lỗi `ERROR: Khong tim thay duong dan`, dừng tiến trình với mã lỗi `sys.exit(1)` **[Điểm kết thúc thất bại 1]**.
         - *Tồn tại:* Ghi nhận đường dẫn tuyệt đối của thư mục mục tiêu.
  4. `[CLI Orchestrator]` In thông báo bắt đầu phân tích và hiển thị trạng thái `AI MODE: ON/OFF`.
  5. `[Core Indexing Engine]` Khởi tạo `RepositoryScanner`, đọc `.gitignore`, quét cấu trúc thư mục và lưu ra `indexes/structure.json`.
  6. `[Core Indexing Engine]` Phân tích AST từng tệp `.java` và `.cs`, tổng hợp `RepositoryIndex` và ghi ra `indexes/repository_index.json`, `indexes/structure_overview.json`.
  7. `[AI Analysis Engine]` Nạp dữ liệu từ `indexes/`, dựng cây phân loại 6 tầng `TaxonomyTree`.
  8. `[AI Analysis Engine]` **[Điểm quyết định 3]:** `use_llm` có bằng `True` không?
     - *Đúng:* Kiểm tra kết nối mạng (health check) đến máy chủ Ollama tại cổng `11434`.
       - **[Điểm quyết định 4]:** Dịch vụ Ollama và model `qwen2.5-coder:3b` có sẵn sàng không?
         - *Có:* Khởi tạo `OllamaClient`, tóm tắt phân cấp Bottom-Up với ngân sách token <= 2000.
         - *Không:* Ghi log cảnh báo ngoại tuyến, tự động chuyển đổi sang `NullLLMClient` để tóm tắt cấu trúc xác định.
     - *Sai:* Khởi tạo `NullLLMClient`, tóm tắt cấu trúc thuần túy từ siêu dữ liệu.
  9. `[AI Analysis Engine]` Sinh nội dung 4 chuyên đề kiến trúc (`tech`, `tests`, `architecture`, `modules`) và lưu ra `analysis/summaries.json`.
  10. `[Knowledge Graph Builder]` Nạp dữ liệu từ `indexes/` và `analysis/`, tạo các nút repository, tệp, ký hiệu và nối các cạnh quan hệ; tự động bù đắp nút `external` cho thư viện bên ngoài.
  11. `[Knowledge Graph Builder]` **[Điểm quyết định 5]:** Thẩm định tính toàn vẹn (Integrity Validation) có đạt chuẩn không?
      - *Không đạt:* Ném `ValueError`, dừng pipeline → đi qua hành động Cleanup (AD-10) rồi mới tới **[Điểm kết thúc thất bại 2]**.
      - *Đạt chuẩn:* Thực hiện ghi đĩa nguyên tử thông qua tệp hoán đổi tạm ra `graphs/graph.json`.
  12. `[Wiki Generator & Browser]` Render 4 trang chuyên đề HTML, render toàn bộ các trang chi tiết ký hiệu trong `wiki/symbols/`, render trang Bảng điều khiển `wiki/index.html`, sinh `search_index.json` và `wiki_context.json`.
  13. `[CLI Orchestrator]` In thông báo thành công: `SUCCESS: Phan tich hoan tat!`.
  14. `[CLI Orchestrator]` **[Điểm quyết định 6]:** Hệ điều hành máy trạm là Windows (`os.name == 'nt'`)?
      - *Đúng:* Gọi API hệ thống `os.startfile(wiki_index_path)`.
      - *Sai:* Gọi thư viện `webbrowser.open(wiki_index_path.as_uri())`.
  15. `[Wiki Generator & Browser]` Trình duyệt web tự động khởi động và tải trang `wiki/index.html`.
  16. `[CLI Orchestrator]` Khối kết thúc bắt buộc `finally`: Nếu clone từ Git, gọi `scanner.cleanup()` xóa sạch thư mục làm việc tạm thời trên đĩa.
  17. `[Software Engineer]` Quan sát giao diện wiki trực quan trên trình duyệt **[Điểm kết thúc thành công]**.
- **Ghi chú vẽ (AD-01):**
  - **Quy trình con:** AD-02, AD-03, AD-04, AD-05, AD-06, AD-09 vẽ bằng **Call Behavior Action** (ký hiệu cái chĩa), mỗi quy trình có sơ đồ riêng.
  - **Quyết định 3 và 4 (chế độ AI)** chính là AD-09: trong AD-01 chỉ vẽ một Call Behavior Action "Chọn chế độ AI (AD-09)" cho gọn.
  - **Merge Node bắt buộc:**
    1. Sau Quyết định 1/2: nhánh Git (sau AD-02) và nhánh thư mục cục bộ hợp nhất trước bước 4.
    2. Nhánh `use_llm = False`, nhánh Ollama khả dụng và nhánh Ollama không khả dụng hợp nhất trước bước 9 (cùng đi tiếp sang sinh 4 chuyên đề).
  - **Luồng lỗi:**
    - Đường dẫn cục bộ không tồn tại: kết thúc thất bại 1 (chưa có tài nguyên tạm nên **không** qua Cleanup).
    - Clone Git lỗi: Cleanup (đã nằm trong AD-02) rồi kết thúc thất bại.
    - Lỗi bất kỳ ở giai đoạn 1–4 (quét, AI, đồ thị, wiki) và KeyboardInterrupt: đi qua hành động **Cleanup** (`finally`, AD-10) rồi tới kết thúc thất bại.
    - Thành công: bước 16 (Cleanup) chạy rồi mới tới kết thúc thành công.
  - **Không mở được trình duyệt** (môi trường không có GUI): bắt ngoại lệ, in đường dẫn tuyệt đối, **vẫn coi là thành công**.
- **Căn cứ phân tích:** [backend/src/cli.py:43-145](file:///e:/FPT/Wiki%20Generation/backend/src/cli.py#L43-L145).

---

### Quy trình 2 (AD-02): Nhận diện URL và Clone Kho Mã nguồn Từ xa
- **Mục tiêu:** Phân giải các định dạng URL khác nhau, cấp phát thư mục tạm thời an toàn, tải mã nguồn commit mới nhất và xử lý lỗi mạng.
- **Swimlanes (03 Phân làn):**
  1. `CLI Scanner`: Tiếp nhận yêu cầu, phân tích định dạng chuỗi và ra lệnh clone.
  2. `Git Remote Server`: Máy chủ từ xa xử lý yêu cầu tải dữ liệu.
  3. `Host File System`: Hệ thống tệp đĩa máy trạm cấp phát và xóa thư mục tạm.
- **Trình tự hành động:**
  1. `[CLI Scanner]` Tiếp nhận chuỗi `target` từ tham số dòng lệnh.
  2. `[CLI Scanner]` **[Điểm quyết định 1 (Phân loại mẫu chuỗi URL)]:**
     - *URL đầy đủ:* Khớp `https?://.*\.git` hoặc `git@.*:.*\.git` -> Giữ nguyên.
     - *GitHub Web:* Khớp `https?://github\.com/.*` -> Tự động thêm đuôi `.git` nếu chưa có.
     - *Shorthand:* Khớp `owner/repo` và không tồn tại thư mục tương ứng trên máy cục bộ -> Ghép thành `https://github.com/owner/repo.git`.
     > **Lưu ý:** Quyết định 1 chỉ chạy khi AD-01 đã xác định đầu vào là Git URL / shorthand. Chuỗi không khớp mẫu nào được coi là đường dẫn cục bộ và xử lý ở AD-01.
  3. `[Host File System]` Gọi `tempfile.mkdtemp(prefix="repoatlas_repo_")` cấp phát thư mục rỗng tạm thời.
  4. `[CLI Scanner]` In thông báo: `Dang clone git repository tu: <url>...`.
  5. `[CLI Scanner]` Khởi chạy tiến trình con: `git clone --depth 1 <url> <temp_dir>`.
  6. `[Git Remote Server]` Tiếp nhận yêu cầu tải bản sao nông (depth = 1).
  7. `[Git Remote Server]` **[Điểm quyết định 2]:** Kết nối mạng và quyền truy cập kho mã nguồn có hợp lệ không?
     - *Thất bại:* Trả về mã lỗi khác 0 và thông điệp lỗi stderr.
     - *Thành công:* Đóng gói dữ liệu commit mới nhất và truyền về cho máy trạm.
  8. `[CLI Scanner]` Kiểm tra mã thoát của lệnh Git con:
     - *Nếu có lỗi (`CalledProcessError`):* Gọi `cleanup()` xóa ngay thư mục tạm vừa tạo trên `Host File System`, ném `ValueError` kèm thông báo stderr và dừng quy trình tải **[Điểm kết thúc lỗi]**.
     - *Nếu thành công (Exit Code = 0):* Gán `self.repo_path` bằng đường dẫn tuyệt đối của thư mục tạm, trả về đường dẫn để tiếp tục quét mã nguồn **[Điểm kết thúc thành công]**.
- **Căn cứ phân tích:** [backend/src/core_indexing/scanner.py:70-111](file:///e:/FPT/Wiki%20Generation/backend/src/core_indexing/scanner.py#L70-L111), [scanner.py:221-226](file:///e:/FPT/Wiki%20Generation/backend/src/core_indexing/scanner.py#L221-L226).

---

### Quy trình 3 (AD-03): Quét Thư mục, Lọc Rác và Phân tích Cú pháp AST Đa Ngôn ngữ
- **Mục tiêu:** Xây dựng cây cấu trúc thư mục, nhận diện các tệp nguồn hợp lệ và sử dụng bộ phân tích cú pháp AST chuyên biệt (Java/C#) để trích xuất ký hiệu và quan hệ.
- **Swimlanes (04 Phân làn):**
  1. `Repository Scanner`: Điều phối duyệt thư mục và nạp bộ lọc `.gitignore`.
  2. `Java Parser`: Bộ phân tích cú pháp cho tệp nguồn Java.
  3. `CSharp Parser`: Bộ phân tích cú pháp cho tệp nguồn C#.
  4. `Local File System`: Đọc nội dung tệp và ghi tệp chỉ mục.
- **Trình tự hành động:**
  1. `[Repository Scanner]` Đọc tệp `.gitignore` từ thư mục gốc của repository (nếu có) và biên dịch thành bộ lọc `pathspec`.
  2. `[Repository Scanner]` Duyệt đệ quy cây thư mục dự án, bỏ qua các thư mục trong `DEFAULT_EXCLUDES` (`.git`, `bin`, `obj`, `target`, `node_modules`...) và các đường dẫn khớp với `.gitignore`.
  3. `[Local File System]` Ghi cấu trúc cây thư mục ra tệp `indexes/structure.json`.
  4. `[Repository Scanner]` Khởi tạo danh sách rỗng chứa các chỉ mục tệp (`file_indexes = []`).
  5. `[Repository Scanner]` **Vòng lặp duyệt từng tệp tin trong repository (Loop over files):**
     - Lấy tệp tiếp theo.
     - **[Điểm quyết định 1]:** Phần mở rộng của tệp có nằm trong danh mục parser hỗ trợ (`.java`, `.cs`) không?
       - *Không:* Bỏ qua, chuyển sang tệp tiếp theo trong vòng lặp.
       - *Có:* Kiểm tra xem tệp có bị loại trừ bởi `.gitignore` không? Nếu bị loại trừ thì bỏ qua; nếu hợp lệ thì tiếp tục.
     - `[Local File System]` Đọc toàn bộ nội dung văn bản UTF-8 của tệp tin.
     - `[Repository Scanner]` **[Điểm quyết định 2]:** Ngôn ngữ của tệp tin là gì?
       - *Nhánh Java (`.java`):* Chuyển nội dung cho `Java Parser`.
       - *Nhánh C# (`.cs`):* Chuyển nội dung cho `CSharp Parser`.
     - `[Java Parser / CSharp Parser]` Tạo cây cú pháp AST; trích xuất package/namespace, import/using; trích xuất các kiểu dữ liệu (Class, Interface, Enum, Record, Struct) và thành viên (Method, Field, Property); trích xuất chú thích framework (`@RestController`, `[ApiController]`), docstring và phạm vi dòng mã nguồn; trích xuất quan hệ `extends`, `implements`, `calls`, `uses_field`; đóng gói thành đối tượng `FileIndex`.
     - `[Repository Scanner]` Đưa `FileIndex` vào danh sách `file_indexes`.
     - *Xử lý lỗi cục bộ trong vòng lặp:* Nếu quá trình đọc hoặc parse một tệp phát sinh ngoại lệ, bắt giữ lỗi, ghi nhật ký cảnh báo và tiếp tục vòng lặp với các tệp còn lại (không dừng pipeline).
     > **Ghi chú vòng lặp:** Mọi nhánh sau đây đều có **mũi tên quay lại đầu vòng lặp** "Lấy tệp tiếp theo": đuôi không được hỗ trợ; tệp bị `.gitignore` loại trừ; ngoại lệ đọc/parse một tệp (ghi cảnh báo rồi tiếp tục). Kết thúc vòng lặp khi không còn tệp nào.
  6. `[Repository Scanner]` Kết thúc vòng lặp duyệt tệp tin.
  7. `[Repository Scanner]` Khởi tạo bộ lập chỉ mục `RepositoryIndexer`, liên kết cây thư mục và danh sách `file_indexes` để tổng hợp thành đối tượng thống nhất `RepositoryIndex`.
  8. `[Local File System]` Xuất khẩu dữ liệu ra 2 tệp tin: `indexes/repository_index.json` và `indexes/structure_overview.json` **[Điểm kết thúc thành công]**.
- **Căn cứ phân tích:** [backend/src/core_indexing/scanner.py:120-220](file:///e:/FPT/Wiki%20Generation/backend/src/core_indexing/scanner.py#L120-L220), [backend/src/core_indexing/indexer.py](file:///e:/FPT/Wiki%20Generation/backend/src/core_indexing/indexer.py).

---

### Quy trình 4 (AD-04): Phân khúc Cú pháp và Tóm tắt Phân cấp Bottom-Up với Quản trị Token
- **Mục tiêu:** Phân đoạn mã nguồn theo cây phân loại 6 tầng, thực hiện tóm tắt từ tầng sâu nhất lên tầng cao nhất thông qua Ollama LLM, áp dụng trần ngân sách 2000 tokens và kiểm tra chống ảo giác.
- **Swimlanes (04 Phân làn):**
  1. `Taxonomy & Chunker`: Xây dựng cây phân loại và trích xuất khung xương cú pháp.
  2. `Summarizer Engine`: Điều phối luồng duyệt Bottom-Up, kiểm tra ngân sách và tạo prompt.
  3. `Local Ollama Server`: Máy chủ LLM thực hiện suy luận văn bản.
  4. `Analysis Output`: Lưu kết quả tóm tắt và báo cáo ngân sách token.
- **Trình tự hành động:**
  1. `[Taxonomy & Chunker]` Nạp `repository_index.json` và dựng cây phân cấp 6 tầng (`Repository → Module → Container → Component → Class → Method`).
  2. `[Summarizer Engine]` Lấy danh sách toàn bộ các nút trong cây và sắp xếp theo thứ tự độ sâu giảm dần (Bottom-Up: Method trước, rồi Class, Component, Container, Module, Repository).
  3. `[Summarizer Engine]` **Vòng lặp duyệt từng nút trong cây phân cấp (Loop over taxonomy nodes):**
     - Lấy nút tiếp theo cần tóm tắt.
     - **[Điểm quyết định 1]:** Nút hiện tại thuộc tầng nào?
       - *Tầng 6 (Method):* tạo chunk khung xương cú pháp (chữ ký, docstring, chú thích, bỏ thân hàm).
       - *Tầng 5 (Class):* tạo chunk khung xương của lớp **và** thu thập digest tóm tắt các Method con đã sinh.
       - *Tầng 4 trở lên (Component, Container, Module, Repository):* chỉ thu thập digest tóm tắt các nút con trực thuộc.
     > **Ghi chú:** Chế độ `NullLLMClient` (không AI) không đi qua AD-04; tóm tắt cấu trúc do UC-06 tạo. Nếu Ollama lỗi giữa chừng khi đang chạy vòng lặp thì **chưa xác nhận** trong mã.
     - `[Summarizer Engine]` Tính toán số lượng token ước tính của ngữ cảnh prompt (`tokens.count_tokens`).
     - **[Điểm quyết định 2]:** Số token ước tính có vượt quá ngân sách quy định (2000 tokens) không?
       - *Có vượt quá:* Thực hiện cắt tỉa khung xương cú pháp, gắn cờ `was_degraded = True` cho đến khi token <= 2000.
       - *Không vượt quá:* Giữ nguyên toàn bộ ngữ cảnh chi tiết.
     - `[Summarizer Engine]` Đóng gói câu lệnh nhắc hoàn chỉnh (System prompt + Context + Task).
     - `[Local Ollama Server]` Nhận yêu cầu tại endpoint `/api/generate`, sinh chuỗi văn bản tóm tắt tự nhiên và trả về phản hồi.
     - `[Summarizer Engine]` Kiểm tra chống ảo giác (Hallucination Validation): quét văn bản tóm tắt vừa nhận, trích xuất các FQN được nhắc đến và đối chiếu với bảng chỉ mục ký hiệu; chỉ lưu các ký hiệu thực sự có thật vào `referenced_symbols`.
     - `[Summarizer Engine]` Tạo đối tượng `SummaryNode` kèm theo báo cáo token `TokenReport` ghi nhận số lượng token thực tế và thời gian thực thi.
  4. `[Summarizer Engine]` Kết thúc vòng lặp duyệt nút.
  5. `[Summarizer Engine]` Kích hoạt bộ sinh nội dung chuyên đề `ContentGenerator`, tổng hợp các phát hiện kiến trúc để sinh phần thân văn bản cho 4 chuyên đề: `tech`, `tests`, `architecture`, `modules`.
  6. `[Analysis Output]` Đóng gói đối tượng `AnalysisResult` và ghi ra tệp `analysis/summaries.json` **[Điểm kết thúc thành công]**.
- **Căn cứ phân tích:** [backend/src/ai_analysis/models.py:25-53](file:///e:/FPT/Wiki%20Generation/backend/src/ai_analysis/models.py#L25-L53), [backend/src/ai_analysis/chunker.py:80-140](file:///e:/FPT/Wiki%20Generation/backend/src/ai_analysis/chunker.py#L80-L140), [backend/src/ai_analysis/summarizer.py:50-180](file:///e:/FPT/Wiki%20Generation/backend/src/ai_analysis/summarizer.py#L50-L180).

---

### Quy trình 5 (AD-05): Xây dựng, Bù trừ Nút Ngoại vi và Lưu trữ Đồ thị Tri thức Nguyên tử
- **Mục tiêu:** Kết hợp chỉ mục mã nguồn và kết quả phân tích AI thành Đồ thị Tri thức, tự động bù đắp nút cho thư viện ngoài, thẩm định tính toàn vẹn và ghi tệp an toàn chống hỏng dữ liệu.
- **Swimlanes (03 Phân làn):**
  1. `Knowledge Graph Builder`: Tạo nút, gắn tóm tắt và nối cạnh quan hệ.
  2. `Schema Validator`: Thẩm định tính toàn vẹn đa thực thể của đồ thị.
  3. `Host File System`: Ghi tệp đệm tạm thời và thực thi hoán đổi tệp nguyên tử.
- **Trình tự hành động:**
  1. `[Knowledge Graph Builder]` Nạp `repository_index.json` và `summaries.json`.
  2. `[Knowledge Graph Builder]` Tạo nút gốc `GraphNode(id="repository:<name>", type="repository")`.
  3. `[Knowledge Graph Builder]` Duyệt danh sách tệp nguồn: tạo nút `file:<path>` và nối cạnh `contains` từ repository tới từng tệp.
  4. `[Knowledge Graph Builder]` Duyệt danh sách ký hiệu: tạo nút `symbol:<fqn>` và nối cạnh `contains` hoặc `declares`.
  5. `[Knowledge Graph Builder]` Nạp cây phân loại: tạo nút Module, Container, Component và gắn quan hệ chứa đựng.
  6. `[Knowledge Graph Builder]` **Vòng lặp** duyệt các quan hệ phụ thuộc (`extends`, `implements`, `calls`, `uses_field`):
     - **[Điểm quyết định 1]:** `target` có tồn tại trong danh mục nút không?
       - *Có:* tạo `GraphEdge(source, target, kind)`.
       - *Không (thư viện ngoài/SDK):* tạo nút `GraphNode(id=target, type="EXTERNAL", metadata.external=True)` rồi tạo cạnh.
  7. `[Knowledge Graph Builder]` Nạp `summaries.json`, đối chiếu theo mã định danh nút, gán vào `metadata.summary`.
  8. `[Schema Validator]` `validate_graph_integrity`:
     - **[Điểm quyết định 2]:** có hai nút trùng `id` không? *Có:* ném `ValueError("Graph node IDs must be unique")`, dừng **[Điểm kết thúc lỗi 1, chưa ghi đĩa]**.
     - **[Điểm quyết định 3]:** có cạnh nào có `source`/`target` không thuộc tập ID nút không? *Có:* ném `ValueError("Edge endpoint is missing")`, dừng **[Điểm kết thúc lỗi 2, chưa ghi đĩa]**.
  9. `[Host File System]` Mở tệp tạm `tempfile.NamedTemporaryFile(prefix=".graph.", suffix=".tmp")` trong `graphs/`.
  10. `[Host File System]` Ghi toàn bộ đồ thị JSON vào tệp tạm. Lỗi I/O: nhảy tới bước 12 rồi **[Điểm kết thúc lỗi 3]**.
  11. `[Host File System]` `os.replace(tệp_tạm, "graphs/graph.json")`.
  12. `[Host File System]` Khối `finally`: xóa tệp tạm nếu còn sót. Sau finally: nếu bước 10/11 thành công → **[Điểm kết thúc thành công]**; nếu có lỗi I/O → **[Điểm kết thúc lỗi 3]**.
- **Căn cứ phân tích:** [backend/src/knowledge_graph/builder.py:64-322](file:///e:/FPT/Wiki%20Generation/backend/src/knowledge_graph/builder.py#L64-L322), [builder.py:334-360](file:///e:/FPT/Wiki%20Generation/backend/src/knowledge_graph/builder.py#L334-L360), [backend/src/knowledge_graph/models.py:74-95](file:///e:/FPT/Wiki%20Generation/backend/src/knowledge_graph/models.py#L74-L95).

---

### Quy trình 6 (AD-06): Biên dịch Gói Tài liệu HTML và Tạo Chỉ mục Song song
- **Mục tiêu:** Nạp khuôn mẫu Jinja2, phân nhánh kết xuất đồng thời các trang chuyên đề và các trang chi tiết ký hiệu, sau đó hợp nhất dữ liệu để xuất bản chỉ mục tìm kiếm và ngữ cảnh AI.
- **Swimlanes (03 Phân làn):**
  1. `Wiki Renderer`: Điều phối toàn bộ quy trình biên dịch tài liệu.
  2. `Jinja2 Engine`: Nạp khuôn mẫu và kết xuất chuỗi HTML từ dữ liệu ngữ cảnh.
  3. `Local File System`: Tạo thư mục và ghi các tệp `.html`, `.json`.
- **Trình tự hành động:**
  1. `[Local File System]` Tạo thư mục `wiki/` và thư mục con `wiki/symbols/` nếu chưa có.
  2. `[Wiki Renderer]` Nạp môi trường khuôn mẫu Jinja2 từ thư mục `templates/`.
  3. `[Wiki Renderer]` **Thanh phân nhánh song song (Fork Node):** Tách thành 2 nhánh xử lý đồng thời:
     - **Nhánh A (Kết xuất các Trang Chuyên đề và Bảng điều khiển):**
       - Lần lượt lấy dữ liệu nội dung từ `analysis_result.content`.
       - Với mỗi phần nội dung (`tech`, `architecture`, `modules`, `tests`): Gọi `Jinja2 Engine` nạp template tương ứng, render HTML và ghi xuống `wiki/<section.key>.html`.
       - Trích xuất dữ liệu tổng quan dự án từ `repository_index` và gọi `Jinja2 Engine` render trang trung tâm `wiki/index.html`.
     - **Nhánh B (Kết xuất Trang Hồ sơ Ký hiệu Cú pháp):**
       - Lấy danh sách ký hiệu `symbols` từ `repository_index`.
       - Gọi `Jinja2 Engine` nạp template `symbol.html`.
       - **Vòng lặp duyệt từng ký hiệu (Loop over symbols):**
         - Kiểm tra ký hiệu có `fully_qualified_name` không?
         - Nếu có: Chuẩn hóa tên tệp an toàn (thay thế `<` và `>` bằng `_`).
         - Render template với `rel_prefix="../"` và ghi ra `wiki/symbols/<safe_filename>.html`.
  4. `[Wiki Renderer]` **Thanh hợp nhất luồng song song (Join Node):** Chờ cả Nhánh A và Nhánh B hoàn thành toàn bộ thao tác kết xuất HTML.
  5. `[Wiki Renderer]` Tiếp tục luồng tuần tự tạo dữ liệu phụ trợ:
     - **Tạo Search Index:** Thu thập URL của 5 trang chính và toàn bộ URL các trang ký hiệu `symbols/<safe_filename>.html`, đóng gói và ghi ra `wiki/search_index.json`.
     - **Tạo AI Context:** Thu thập toàn bộ ký hiệu kèm chữ ký phương thức đã định dạng, docstring, chú thích, nội dung các phần chuyên đề và các bản tóm tắt phân cấp, đóng gói và ghi ra `wiki/wiki_context.json`.
  6. `[Wiki Renderer]` Hoàn tất toàn bộ gói tài liệu tĩnh trong thư mục `wiki/` **[Điểm kết thúc thành công]**.
- **Lưu ý vẽ:** Fork/Join thể hiện hai nhánh độc lập về dữ liệu (có thể song song về logic). Mã hiện tại **chưa xác nhận** chạy song song thật. Người vẽ vẫn vẽ Fork/Join theo kịch bản.
- **Căn cứ phân tích:** [backend/src/wiki_generation/renderer.py:20-182](file:///e:/FPT/Wiki%20Generation/backend/src/wiki_generation/renderer.py#L20-L182).

---

### Quy trình 7 (AD-07): Điều hướng Thanh bên và Tìm kiếm Trực tiếp Ngoại tuyến Phía Trình duyệt
- **Mục tiêu:** Cho phép người đọc wiki duyệt các trang chuyên đề qua thanh bên hoặc gõ từ khóa tìm kiếm trực tiếp với tốc độ phản hồi tức thì hoàn toàn phía trình duyệt.
- **Swimlanes (03 Phân làn):**
  1. `Wiki User`: Người đọc tài liệu thao tác nhấp chuột hoặc gõ từ khóa.
  2. `Browser UI & DOM`: Giao diện web hiển thị, bắt sự kiện và cập nhật giao diện.
  3. `Client Search Engine (JS)`: Mã JavaScript nội bộ xử lý nạp chỉ mục và lọc từ khóa.
- **Trình tự hành động:**
  1. `[Browser UI & DOM]` Người dùng mở trang wiki (ví dụ `wiki/index.html`).
  2. `[Client Search Engine (JS)]` Bắt sự kiện `DOMContentLoaded`:
     - Gửi yêu cầu `fetch('search_index.json')` để nạp toàn bộ danh mục tìm kiếm vào biến bộ nhớ `searchIndex`. Nếu `fetch('search_index.json')` thất bại: ghi lỗi Console, tìm kiếm không khả dụng, vẫn cho phép duyệt thanh bên.
     - Phân tích đường dẫn `window.location.pathname`, tìm phần tử thanh bên tương ứng và gắn lớp CSS làm nổi bật mục hiện tại (`active sidebar state`).
  3. `[Wiki User]` **[Điểm quyết định 1 (Lựa chọn thao tác của người dùng)]:**
     - **Nhánh 1 (Điều hướng qua Thanh bên Sidebar):**
       - Người dùng nhấp chuột vào một mục chuyên đề trên thanh bên (ví dụ "Architecture").
       - `[Browser UI & DOM]` Trình duyệt chuyển hướng ngay sang trang `wiki/architecture.html`.
       - Mã JavaScript trên trang mới tự động cập nhật trạng thái nổi bật cho mục thanh bên mới **[Điểm kết thúc nhánh 1 — Flow Final]**.
     - **Nhánh 2 (Tìm kiếm trực tiếp Live Search):**
       - Người dùng nhấp chuột vào ô tìm kiếm trên thanh tiêu đề và gõ ký tự.
       - `[Browser UI & DOM]` Bắt sự kiện `input` trên ô tìm kiếm.
       - `[Client Search Engine (JS)]` Lấy chuỗi tìm kiếm, chuyển thành chữ thường và cắt bỏ khoảng trắng.
       - **[Điểm quyết định 2]:** Chuỗi tìm kiếm có rỗng không?
         - *Rỗng:* Thêm lớp `hidden` vào phần tử kết quả `searchResults` để ẩn danh sách.
         - *Không rỗng:* Tiếp tục lọc.
       - `[Client Search Engine (JS)]` Duyệt mảng `searchIndex`, lọc các phần tử có tên chứa chuỗi từ khóa tìm kiếm và lấy tối đa 15 kết quả hàng đầu (`.slice(0, 15)`).
       - `[Browser UI & DOM]` **[Điểm quyết định 3]:** Có tìm thấy kết quả phù hợp không?
         - *Có:* Tạo các phần tử liên kết thẻ `<a>` cho từng kết quả và gỡ bỏ lớp `hidden` để hiển thị danh sách thả xuống. Nếu người dùng nhấp chuột ra ngoài ô tìm kiếm thì thêm lớp `hidden` để ẩn danh sách.
         - *Không:* Hiển thị thông báo `No results found`.
       - `[Wiki User]` Người dùng quan sát danh sách thả xuống và nhấp chuột vào một kết quả mong muốn.
       - `[Browser UI & DOM]` Trình duyệt chuyển hướng ngay đến trang tài liệu của ký hiệu hoặc chuyên đề tương ứng (`relPrefix + item.url`) **[Điểm kết thúc nhánh 2 — Flow Final]**.
- **Ghi chú vẽ:** "Điểm kết thúc nhánh 1/2" vẽ là **Flow Final** (hoặc quay về chờ thao tác tiếp), không phải Activity Final.
- **Căn cứ phân tích:** [backend/src/wiki_generation/templates/base.html:232-304](file:///e:/FPT/Wiki%20Generation/backend/src/wiki_generation/templates/base.html#L232-L304).

---

### Quy trình 8 (AD-08): Tương tác Hỏi đáp Codebase và Truyền luồng Thời gian thực với Trợ lý AI
- **Mục tiêu:** Phân tích câu hỏi tự nhiên của người dùng, trích xuất ngữ cảnh liên quan nhất từ kho tri thức nội bộ, gửi yêu cầu suy luận đến Ollama và truyền luồng câu trả lời về giao diện hoặc tự động chuyển tiếp sang chế độ dự phòng thông minh nếu Ollama ngoại tuyến.
- **Swimlanes (03 Phân làn):**
  1. `Wiki User`: Người dùng nhập câu hỏi và đọc câu trả lời.
  2. `AI Chat Widget (JS)`: Mã JavaScript quản lý giao diện chat, phân tích ý định, xếp hạng ngữ cảnh và dự phòng.
  3. `Local Ollama Server`: Dịch vụ máy chủ suy luận mô hình ngôn ngữ cục bộ.
- **Trình tự hành động:**
  1. `[Wiki User]` Nhấp vào nút nổi mở bảng chat Trợ lý AI ở góc màn hình.
  2. `[AI Chat Widget (JS)]` Bắt sự kiện, hiển thị khung chat và gửi yêu cầu ngầm kiểm tra sức khỏe dịch vụ: `fetch("http://localhost:11434/api/tags")`:
     - Nếu phản hồi có model `qwen2.5-coder:3b`: Cập nhật chấm trạng thái màu xanh ("Ollama online").
     - Nếu server có nhưng **thiếu model** `qwen2.5-coder:3b`: Cập nhật chấm đỏ, như không kết nối.
     - Nếu không kết nối được: Cập nhật chấm trạng thái màu đỏ ("Ollama offline · dùng tìm kiếm nội bộ").
     > **Lưu ý:** Sau lần kiểm tra đầu, widget kiểm tra lại mỗi 30 giây (chưa xác nhận trong mã).
  3. `[Wiki User]` Gõ câu hỏi tự nhiên vào ô nhập liệu và bấm nút Gửi (hoặc nhấn Enter).
  4. `[AI Chat Widget (JS)]` Hiển thị câu hỏi của người dùng vào khung chat và tạo một bong bóng thông báo "Đang suy nghĩ...".
  5. `[AI Chat Widget (JS)]` Phân tích câu hỏi: phát hiện ý định (Intent Detection: đếm số lượng, hỏi vị trí, hỏi kiểm thử, hỏi kiến trúc); tách từ khóa (Keyword Extraction: chuẩn hóa bỏ dấu tiếng Việt, tách từ độ dài > 2, loại bỏ `STOP_WORDS`).
  6. `[AI Chat Widget (JS)]` Tính điểm liên quan (Scoring):
     - Duyệt mảng ký hiệu trong `wiki_context.json`: cộng điểm nếu tên ký hiệu, FQN, đường dẫn tệp hoặc docstring chứa từ khóa; lấy 12 ký hiệu có điểm cao nhất.
     - Duyệt các phần chuyên đề wiki: cộng điểm cho tiêu đề và nội dung; lấy 3 chuyên đề có điểm cao nhất.
  7. `[AI Chat Widget (JS)]` Đóng gói chuỗi ngữ cảnh tri thức và câu lệnh nhắc yêu cầu AI trả lời trung thực, không bịa đặt.
  8. `[AI Chat Widget (JS)]` Gửi yêu cầu HTTP POST đến `http://localhost:11434/api/generate` kèm cờ `stream: true`.
  9. `[AI Chat Widget (JS)]` **[Điểm quyết định 1]: Yêu cầu kết nối đến Ollama có thành công không?**
     - **Nhánh Thành công (Ollama phản hồi HTTP 200):**
       - Đọc luồng dữ liệu trả về qua `response.body.getReader()`.
       - Xóa dòng chữ "Đang suy nghĩ...".
       - **Vòng lặp đọc gói dữ liệu (Stream Loop):** Nhận từng đoạn dữ liệu (chunks), giải mã UTF-8, phân tích dòng JSON và gắn trực tiếp từ ngữ phản hồi vào khung chat theo thời gian thực cho đến khi kết thúc luồng. (Lưu ý: Lỗi giữa chừng khi đang stream: chưa xác nhận; nếu `fetch` ném ngoại lệ hoặc `response.ok = false` thì chuyển sang nhánh dự phòng).
       - Tự động cuộn khung chat xuống dưới cùng **[Điểm kết thúc nhánh AI]**.
     - **Nhánh Thất bại (Lỗi mạng hoặc CORS):**
       - Kích hoạt cơ chế Chuyển đổi Dự phòng Thông minh (Intelligent Fallback):
         - **[Điểm quyết định 2]:** Ý định câu hỏi là gì?
           - *Nếu là câu hỏi thống kê/đếm:* Hiển thị tổng số lớp, số hàm, ngôn ngữ và danh sách 30 ký hiệu tiêu biểu kèm liên kết.
           - *Nếu có ký hiệu liên quan theo từ khóa:* Hiển thị thẻ tóm tắt chi tiết của từng ký hiệu khớp (chữ ký, đường dẫn tệp, docstring) kèm siêu liên kết mở trang chi tiết.
           - *Nếu không có ký hiệu khớp:* Hiển thị bản tóm tắt tổng quan kiến trúc codebase.
         - Hiển thị hộp chỉ dẫn lệnh PowerShell để người dùng khởi động Ollama khi cần thiết.
         - Cập nhật nội dung dự phòng vào khung chat **[Điểm kết thúc nhánh Dự phòng]**.
  10. `[Wiki User]` Người dùng đọc câu trả lời và nhấp vào các liên kết ký hiệu mã nguồn để xem chi tiết.
- **Căn cứ phân tích:** [backend/src/wiki_generation/templates/base.html:305-604](file:///e:/FPT/Wiki%20Generation/backend/src/wiki_generation/templates/base.html#L305-L604).

---

### Quy trình 9 (AD-09): Thăm dò Sức khỏe Máy chủ Ollama và Hạ cấp An toàn sang Cấu trúc
- **Mục tiêu:** Tự động phát hiện trạng thái máy chủ AI trong quá trình chạy phân tích CLI; nếu dịch vụ gặp sự cố, tự động chuyển đổi sang bộ tóm tắt cấu trúc để đảm bảo tiến trình tạo tài liệu không bao giờ bị dừng giữa chừng.
- **Swimlanes (03 Phân làn):**
  1. `CLI / Pipeline Coordinator`: Tiếp nhận cấu hình và kích hoạt phân hệ AI.
  2. `AI Health Monitor`: Gửi yêu cầu thăm dò mạng và kiểm tra mô hình.
  3. `Local Ollama Daemon`: Máy chủ dịch vụ AI cục bộ.
- **Trình tự hành động:**
  1. `[CLI / Pipeline Coordinator]` Đọc tham số `args.no_llm`.
  2. `[CLI / Pipeline Coordinator]` **[Điểm quyết định 1]:** Người dùng có chỉ định cờ `--no-llm` không?
     - *Có (`args.no_llm = True`):* Ghi log "Running without an LLM; documentation will be structural only", khởi tạo ngay `NullLLMClient` và bỏ qua việc thăm dò mạng **[Điểm kết thúc nhánh Tắt AI]**.
     - *Không (`use_llm = True`):* Tiếp tục bước thăm dò sức khỏe.
  3. `[AI Health Monitor]` Khởi tạo đối tượng `OllamaClient(model, endpoint)`.
  4. `[AI Health Monitor]` Gửi yêu cầu HTTP GET thăm dò đến `http://localhost:11434/api/tags` với thời gian chờ (timeout) quy định.
  5. `[Local Ollama Daemon]` Xử lý yêu cầu thăm dò.
  6. `[AI Health Monitor]` **[Điểm quyết định 2: Kết quả thăm dò có phản hồi thành công không?]:**
     - *Không kết nối được hoặc hết thời gian chờ:* Ghi nhật ký cảnh báo `WARNING: Ollama is not usable at ... falling back to structural mode`, đóng kết nối máy khách (`client.close()`), khởi tạo và trả về đối tượng `NullLLMClient` **[Điểm kết thúc nhánh Hạ cấp 1]**.
     - *Phản hồi thành công (HTTP 200):* Đọc danh sách các mô hình hiện có trên máy chủ Ollama.
       - **[Điểm quyết định 3]:** Mô hình chỉ định (`qwen2.5-coder:3b`) có tồn tại trong danh sách không?
         - *Không tồn tại:* Ghi nhật ký cảnh báo thiếu mô hình, đóng kết nối và trả về `NullLLMClient` **[Điểm kết thúc nhánh Hạ cấp 2]**.
         - *Tồn tại:* Ghi nhật ký xác nhận `Using Ollama model ... at ...`, trả về đối tượng `OllamaClient` hoạt động hoàn chỉnh **[Điểm kết thúc nhánh Sẵn sàng AI]**.
- **Căn cứ phân tích:** [backend/src/ai_analysis/__main__.py:93-114](file:///e:/FPT/Wiki%20Generation/backend/src/ai_analysis/__main__.py#L93-L114), [backend/src/ai_analysis/llm/ollama.py:40-75](file:///e:/FPT/Wiki%20Generation/backend/src/ai_analysis/llm/ollama.py#L40-L75).

---

### Quy trình 10 (AD-10): Thu hồi Tài nguyên Tạm thời và Xử lý Lỗi Toàn cục trong Pipeline
- **Mục tiêu:** Đảm bảo toàn bộ các thư mục làm việc tạm thời được giải phóng hoàn toàn khỏi ổ đĩa máy tính trong mọi tình huống kết thúc của pipeline (hoàn thành, gặp lỗi ngoại lệ hoặc người dùng bấm Ctrl+C).
- **Swimlanes (03 Phân làn):**
  1. `CLI Orchestrator`: Quản lý khối bảo vệ `try...finally` toàn cục.
  2. `Scanner / Workspace Manager`: Lưu trữ tham chiếu đường dẫn tạm và thực thi giải phóng.
  3. `Host File System`: Xóa thư mục vật lý.
- **Trình tự hành động:**
  1. `[CLI Orchestrator]` Mở khối `try` bao bọc 4 giai đoạn pipeline.
  2. `[CLI Orchestrator]` Pipeline kết thúc theo **một trong ba cách** (không vẽ Decision Node, cả ba cùng nối vào `finally`):
     - Hoàn thành bình thường;
     - Ngoại lệ chưa xử lý (lỗi đọc tệp, thẩm định đồ thị…);
     - Người dùng nhấn Ctrl+C (`KeyboardInterrupt`).
  3. `[CLI Orchestrator]` Luồng điều khiển luôn đi vào khối `finally`.
  4. `[Scanner / Workspace Manager]` Kiểm tra `self._temp_dir`.
  5. `[Scanner / Workspace Manager]` **[Điểm quyết định]:** `_temp_dir` có tồn tại không?
     - *Không (phân tích thư mục cục bộ):* bỏ qua việc xóa.
     - *Có (phân tích từ Git):* tiếp tục.
  6. `[Host File System]` Gọi `shutil.rmtree(self._temp_dir, ignore_errors=True)`.
  7. `[Scanner / Workspace Manager]` Đặt `self._temp_dir = None`.
  8. `[CLI Orchestrator]` Giải phóng xong, thoát tiến trình **[Điểm kết thúc quy trình]**.
> **Chưa xác nhận (không vẽ, hoặc vẽ nét đứt):** việc tự gỡ cờ chỉ đọc của tệp trong `.git` trên Windows rồi xóa lại. Vì `ignore_errors=True` nuốt lỗi nên mô tả "bắt lỗi quyền rồi xóa lại" chỉ đúng nếu mã có xử lý `onerror` riêng.
- **Căn cứ phân tích:** [backend/src/cli.py:57-145](file:///e:/FPT/Wiki%20Generation/backend/src/cli.py#L57-L145), [backend/src/core_indexing/scanner.py:221-226](file:///e:/FPT/Wiki%20Generation/backend/src/core_indexing/scanner.py#L221-L226).

---

## PHẦN 4: CÁC KỊCH BẢN VÒNG ĐỜI ĐỐI TƯỢNG ĐỦ RÕ ĐỂ VẼ STATE MACHINE DIAGRAM

### Đối tượng 1: Phiên làm việc Phân tích (`AnalysisSession`)

#### 1. Mục đích và Vòng đời Tổng quát
- **Tên đối tượng:** `AnalysisSession`.
- **Mục đích:** Quản lý toàn bộ tiến trình thực thi của một lần chạy lệnh `repoatlas analyze`, từ khi tiếp nhận tham số dòng lệnh đến khi mở trình duyệt hiển thị kết quả hoặc dọn dẹp khi gặp lỗi.
- **Trạng thái ban đầu:** `Idle` (Chờ lệnh).
- **Trạng thái kết thúc:** `Completed` (Thành công) hoặc `Failed` (Thất bại).

#### 2. Danh sách Trạng thái Đã xác nhận
- `Idle`: Hệ thống đang chờ người dùng nhập lệnh tại terminal.
- `Validating`: Đang thẩm định đường dẫn cục bộ hoặc nhận diện định dạng URL Git.
- `CloningRepository`: Đang tải bản sao nông của repository từ máy chủ Git từ xa vào thư mục tạm.
- `Scanning`: Đang quét thư mục, lọc bỏ tệp rác và phân tích AST các ngôn ngữ Java/C#.
- `Analyzing`: Đang phân khúc 6 tầng và sinh tóm tắt qua Ollama hoặc chế độ cấu trúc.
- `BuildingGraph`: Đang hợp nhất tri thức, bù trừ nút ngoại vi và thẩm định toàn vẹn đồ thị.
- `GeneratingWiki`: Đang kết xuất các trang chuyên đề HTML, trang ký hiệu, chỉ mục tìm kiếm và ngữ cảnh AI.
- `CleaningUp`: Khối kết thúc bắt buộc (`finally`) đang thực thi thu hồi tài nguyên tạm thời.
- `Completed`: Phân tích hoàn tất thành công, trình duyệt web mặc định đã mở trang Dashboard.
- `Failed`: Phân tích thất bại tại một khâu nào đó, lỗi đã được thông báo ra terminal.

#### 3. Câu chuyện Vòng đời
Khi kỹ sư phần mềm gõ lệnh phân tích, một `AnalysisSession` thức dậy từ `Idle` và bước vào `Validating`. Hệ thống kiểm tra xem địa chỉ là đường dẫn máy tính hay kho Git từ xa. Nếu là đường dẫn cục bộ không tồn tại, phiên chuyển thẳng sang `Failed`. Nếu là địa chỉ Git hợp lệ, phiên chuyển sang `CloningRepository` để tải mã nguồn về đĩa; nếu mất mạng hoặc sai địa chỉ, phiên chuyển sang `CleaningUp` rồi kết thúc ở `Failed`. Khi đã có mã nguồn sẵn sàng trên đĩa, phiên chuyển qua tuần tự 4 pha: `Scanning` (quét AST), `Analyzing` (tóm tắt AI), `BuildingGraph` (dựng đồ thị) và `GeneratingWiki` (sinh HTML). Nếu bất kỳ giai đoạn nào phát sinh ngoại lệ không thể xử lý, phiên lập tức bị kéo vào trạng thái `CleaningUp` để dọn dẹp trước khi chuyển sang `Failed`. Khi toàn bộ các trang HTML được ghi thành công, hệ thống tự động kích hoạt trình duyệt và phiên đạt trạng thái `Completed`. Khối dọn dẹp `CleaningUp` luôn được thực thi trước khi phiên kết thúc hoàn toàn.

#### 4. Bảng chuyển trạng thái (State Transition Table)
Quy ước: `hasError` = đã có lỗi ở giai đoạn trước.

| Trạng thái hiện tại | Sự kiện kích hoạt | Điều kiện bảo vệ [guard] | Trạng thái tiếp theo | Hành động /action |
|---|---|---|---|---|
| Initial | Khởi tạo phiên | — | `Idle` | — |
| `Idle` | Nhập lệnh `repoatlas analyze` | Tham số được tiếp nhận | `Validating` | Phân tích đối số CLI |
| `Validating` | Thẩm định địa chỉ | `_is_git_url(target) == True` | `CloningRepository` | Tạo thư mục tạm, chuẩn bị clone |
| `Validating` | Thẩm định địa chỉ | thư mục cục bộ tồn tại | `Scanning` | Khởi tạo `RepositoryScanner` |
| `Validating` | Thẩm định địa chỉ | thư mục cục bộ không tồn tại | `Failed` | In `Khong tim thay duong dan`, `sys.exit(1)` |
| `CloningRepository` | Tải Git hoàn tất | exit code = 0 | `Scanning` | Gán `repo_path` trỏ về thư mục tạm |
| `CloningRepository` | Tải Git thất bại | `CalledProcessError` | `CleaningUp` | Bắt lỗi, `hasError = true` |
| `Scanning` | Quét & parse xong | Tạo xong `RepositoryIndex` | `Analyzing` | Ghi `indexes/` |
| `Scanning` | Lỗi nghiêm trọng | Ngoại lệ chưa bắt | `CleaningUp` | Ghi log, `hasError = true` |
| `Analyzing` | Tóm tắt xong | Tạo xong `AnalysisResult` | `BuildingGraph` | Ghi `analysis/summaries.json` |
| `Analyzing` | Lỗi | `FileNotFoundError` hoặc ngoại lệ khác | `CleaningUp` | Báo lỗi, `hasError = true` |
| `BuildingGraph` | Đồ thị hợp lệ & đã ghi | Thẩm định đạt | `GeneratingWiki` | Ghi nguyên tử `graphs/graph.json` |
| `BuildingGraph` | Thẩm định / ghi đĩa lỗi | Trùng ID, cạnh mồ côi hoặc I/O lỗi | `CleaningUp` | Ném `ValueError`, `hasError = true` |
| `GeneratingWiki` | Render xong tất cả tệp | 5 trang + symbols + 2 JSON đã ghi | `CleaningUp` | In SUCCESS, mở trình duyệt |
| `GeneratingWiki` | Lỗi ghi đĩa / template | Ngoại lệ I/O hoặc Jinja2 | `CleaningUp` | Ghi lỗi, `hasError = true` |
| `CloningRepository`, `Scanning`, `Analyzing`, `BuildingGraph`, `GeneratingWiki` | Ctrl+C | `KeyboardInterrupt` | `CleaningUp` | `hasError = true` |
| `CleaningUp` | Dọn dẹp xong | `hasError == false` | `Completed` | Dashboard đã mở |
| `CleaningUp` | Dọn dẹp xong | `hasError == true` | `Failed` | In thông báo thất bại |
| `Completed` | — | — | Final | (không nhãn) |
| `Failed` | — | — | Final | (không nhãn) |

> **Mẹo cho người vẽ SD-01:** Gộp 5 trạng thái `CloningRepository`…`GeneratingWiki` vào một composite state, rồi vẽ một mũi tên `KeyboardInterrupt` từ composite sang `CleaningUp`.

#### 5. Chuyển trạng thái bị cấm
- Không nhảy từ `Scanning` thẳng sang `GeneratingWiki` (bỏ qua `Analyzing` và `BuildingGraph`).
- Không quay lại `Idle`/khởi động lại phiên từ `Failed` trong cùng một lần chạy.
- Không chuyển sang `Failed` hoặc `Completed` mà không qua `CleaningUp`, **trừ** `Validating → Failed` (chưa có tài nguyên tạm cần dọn).
- **Căn cứ phân tích:** [backend/src/cli.py:43-145](file:///e:/FPT/Wiki%20Generation/backend/src/cli.py#L43-L145).

---

### Đối tượng 2: Không gian Làm việc Git Tạm thời (`GitCloneWorkspace`)

#### 1. Mục đích và Vòng đời Tổng quát
- **Tên đối tượng:** `GitCloneWorkspace`.
- **Mục đích:** Quản lý vòng đời của thư mục làm việc tạm thời trên ổ đĩa máy trạm khi clone repository từ xa.
- **Trạng thái ban đầu:** `Unallocated` (Chưa cấp phát).
- **Trạng thái kết thúc:** `Purged` (Đã xóa hoàn toàn) hoặc `FailedAllocation` (Lỗi cấp phát/clone).

#### 2. Danh sách Trạng thái Đã xác nhận
- `Unallocated`: Thư mục tạm chưa được cấp phát (`_temp_dir is None`).
- `Allocating`: Đang yêu cầu hệ điều hành cấp phát thư mục tạm thời.
- `Cloning`: Thư mục đã tạo, đang tiếp nhận luồng tải dữ liệu từ lệnh `git clone`.
- `InUse`: Tải xong, thư mục đang được sử dụng bởi các bộ đọc AST.
- `Releasing`: Tiến trình phân tích hoàn tất hoặc bị lỗi, bắt đầu quy trình dọn dẹp.
- `Purged`: Toàn bộ thư mục và tệp con đã bị xóa sạch khỏi đĩa cứng (`_temp_dir = None`).
- `FailedAllocation`: Cấp phát hoặc clone thất bại, tài nguyên tạm đã được thu hồi ngay lập tức.

#### 3. Bảng chuyển trạng thái
Quy ước: `cloneFailed` = lệnh clone đã thất bại.

| Trạng thái hiện tại | Sự kiện kích hoạt | Điều kiện bảo vệ | Trạng thái tiếp theo | Hành động |
|---|---|---|---|---|
| Initial | Khởi tạo | — | `Unallocated` | — |
| `Unallocated` | Phát hiện URL Git | `is_remote == True` | `Allocating` | Gọi `tempfile.mkdtemp` |
| `Allocating` | Cấp phát thành công | Thư mục vật lý được tạo | `Cloning` | `git clone --depth 1` |
| `Allocating` | Cấp phát thất bại | `mkdtemp` ném lỗi | `FailedAllocation` | Báo lỗi (chưa có gì để xóa) |
| `Cloning` | Clone thành công | Exit code = 0 | `InUse` | `self.repo_path = temp_dir` |
| `Cloning` | Clone thất bại hoặc Ctrl+C | `CalledProcessError` / `KeyboardInterrupt` | `Releasing` | `cloneFailed = true` (nếu lỗi clone) |
| `InUse` | Pipeline kết thúc hoặc lỗi | gọi `scanner.cleanup()` | `Releasing` | Xóa đệ quy |
| `Releasing` | Xóa xong | `cloneFailed == false` | `Purged` | `_temp_dir = None` |
| `Releasing` | Xóa xong | `cloneFailed == true` | `FailedAllocation` | Ném `ValueError` báo lỗi clone ra CLI |
| `Purged` | — | — | Final | (không nhãn) |
| `FailedAllocation` | — | — | Final | (không nhãn) |

> **Ghi chú cho người vẽ:** Với đường dẫn cục bộ, đối tượng này không được tạo, không vẽ.

#### 4. Chuyển trạng thái bị cấm
- Không xóa thư mục tạm khi tiến trình `git clone` còn đang ghi dữ liệu (chỉ xóa sau khi lệnh Git đã kết thúc/ngắt); không chuyển sang `InUse` khi clone trả mã lỗi khác 0; không tái sử dụng workspace đã `Purged`.
- **Căn cứ phân tích:** [backend/src/core_indexing/scanner.py:100-111](file:///e:/FPT/Wiki%20Generation/backend/src/core_indexing/scanner.py#L100-L111), [scanner.py:221-226](file:///e:/FPT/Wiki%20Generation/backend/src/core_indexing/scanner.py#L221-L226).

---

### Đối tượng 3: Ký hiệu Cú pháp Mã nguồn (`ASTSymbolNode`)

#### 1. Mục đích và Vòng đời Tổng quát
- **Tên đối tượng:** `ASTSymbolNode`.
- **Mục đích:** Đại diện cho một đơn vị mã nguồn độc lập (Lớp, Giao diện, Hàm, Trường dữ liệu, Thuộc tính), quản lý chu trình chuyển hóa từ AST thô đến trang tài liệu HTML hiển thị trước người dùng.
- **Trạng thái ban đầu:** `Discovered` (Vừa phát hiện trong AST).
- **Trạng thái kết thúc:** `Rendered` (Đã render HTML) hoặc `Discarded` (Bị loại bỏ).

#### 2. Danh sách Trạng thái Đã xác nhận
- `Discovered`: Vừa được parser trích xuất từ cây cú pháp AST, chứa thông tin kỹ thuật thô.
- `Indexed`: Đã được chuẩn hóa FQN và đưa vào danh sách chỉ mục toàn dự án `RepositoryIndex.symbols`.
- `Chunked`: Đã được trích xuất khung xương cú pháp AST (loại bỏ thân hàm) để làm prompt AI.
- `Summarized`: Đã được gắn kèm đoạn văn bản tóm tắt chức năng (do AI sinh hoặc cấu trúc tạo).
- `Graphed`: Đã trở thành một nút `GraphNode` liên kết mạng lưới quan hệ trong Knowledge Graph.
- `Rendered`: Đã được Jinja2 biên dịch thành trang tài liệu `wiki/symbols/<safe_filename>.html`.
- `Discarded`: Bị loại bỏ do thiếu hoặc không hợp lệ tên định danh (FQN).

#### 3. Bảng chuyển trạng thái
| Trạng thái hiện tại | Sự kiện kích hoạt | Điều kiện bảo vệ | Trạng thái tiếp theo | Hành động |
|---|---|---|---|---|
| Initial | Parser trích xuất ký hiệu | — | `Discovered` | — |
| `Discovered` | Tổng hợp chỉ mục | FQN hợp lệ | `Indexed` | Thêm vào `RepositoryIndex.symbols` |
| `Discovered` | Tổng hợp chỉ mục | FQN thiếu/không hợp lệ | `Discarded` | Bỏ qua, ghi log cảnh báo |
| `Indexed` | Phân đoạn theo taxonomy | Thuộc tầng `CLASS` hoặc `METHOD` | `Chunked` | Trích xuất khung xương AST |
| `Indexed` | Không có tóm tắt riêng | [còn lại: không phải CLASS/METHOD] | `Graphed` | Nạp thẳng vào đồ thị |
| `Chunked` | Sinh tóm tắt xong | Nhận phản hồi LLM hoặc cấu trúc | `Summarized` | Tạo `SummaryNode` |
| `Summarized` | Nạp vào Knowledge Graph | Tạo nút đồ thị | `Graphed` | `GraphNode(id="symbol:<fqn>")` |
| `Graphed` | Kết xuất trang | Có `fully_qualified_name` | `Rendered` | Ghi `wiki/symbols/<safe_filename>.html` |
| `Rendered` | — | — | Final | (không nhãn) |
| `Discarded` | — | — | Final | (không nhãn) |

**Ghi chú:** lỗi parse một tệp xảy ra **trước** khi ký hiệu được tạo (tệp đó trả chỉ mục rỗng), nên không vẽ chuyển tiếp "lỗi parse → Discarded" cho ký hiệu. Việc renderer kiểm tra lại FQN (`renderer.py:52`) chỉ là phòng vệ bổ sung, không vẽ.

#### 4. Chuyển trạng thái bị cấm
- Không render trực tiếp từ `Discovered`/`Chunked`/`Summarized` mà chưa qua `Graphed`; `FIELD` không bao giờ vào `Chunked`.
- **Căn cứ phân tích:** [backend/src/core_indexing/models.py:121-160](file:///e:/FPT/Wiki%20Generation/backend/src/core_indexing/models.py#L121-L160), [backend/src/ai_analysis/chunker.py:80-96](file:///e:/FPT/Wiki%20Generation/backend/src/ai_analysis/chunker.py#L80-L96), [backend/src/wiki_generation/renderer.py:38-63](file:///e:/FPT/Wiki%20Generation/backend/src/wiki_generation/renderer.py#L38-L63).

---

### Đối tượng 4: Đồ thị Tri thức Dự án (`KnowledgeGraph`)

#### 1. Mục đích và Vòng đời Tổng quát
- **Tên đối tượng:** `KnowledgeGraph`.
- **Mục đích:** Kho dữ liệu trung gian chuẩn hóa duy nhất của hệ thống, hội tụ toàn bộ thông tin cấu trúc, mạng lưới quan hệ đa chiều và văn bản tóm tắt phân cấp trước khi chuyển hóa thành website.
- **Trạng thái ban đầu:** `Initialized` (Vừa khởi tạo).
- **Trạng thái kết thúc:** `Committed` (thành công) hoặc một trong hai lỗi: `ValidationFailed` (thẩm định lỗi), `WriteFailed` (lỗi ghi đĩa).

#### 2. Danh sách Trạng thái Đã xác nhận
- `Initialized`: Đối tượng đồ thị rỗng vừa được tạo trong bộ nhớ.
- `PopulatingCore`: Đang thêm các nút đại diện cho repository, tệp tin và ký hiệu cú pháp.
- `LinkingEdges`: Đang nạp các quan hệ phụ thuộc, nối cạnh và bù trừ nút ngoại vi `EXTERNAL`.
- `AttachingSummaries`: Đang gắn kết các văn bản tóm tắt phân cấp vào metadata của từng nút.
- `ValidatingIntegrity`: Đang chạy hàm kiểm tra toàn vẹn (trùng ID nút, cạnh mồ côi).
- `PersistingAtomic`: Thẩm định đạt chuẩn, đang ghi dữ liệu vào tệp tạm `.graph.tmp`.
- `Committed`: Tệp tạm đã được hoán đổi nguyên tử thành `graphs/graph.json`.
- `ValidationFailed`: Thẩm định thất bại (trùng ID hoặc cạnh mồ côi), ném `ValueError`, chưa tạo tệp tạm.
- `WriteFailed`: Lỗi I/O khi đang ghi tệp tạm, tệp tạm bị xóa trong `finally`.

#### 3. Bảng chuyển trạng thái
| Trạng thái hiện tại | Sự kiện | Guard | Tiếp theo | Hành động |
|---|---|---|---|---|
| Initial | Khởi tạo | — | `Initialized` | — |
| `Initialized` | Bắt đầu xây dựng | Có `RepositoryIndex` hợp lệ | `PopulatingCore` | Tạo nút repository, file, symbol, taxonomy |
| `PopulatingCore` | Nạp xong nút lõi | — | `LinkingEdges` | Duyệt quan hệ |
| `LinkingEdges` | Gặp đích ngoài dự án | đích không có trong đồ thị | `LinkingEdges` | Tạo nút `EXTERNAL` |
| `LinkingEdges` | Nối xong cạnh | tất cả cạnh đã thêm | `AttachingSummaries` | Nạp `summaries.json` |
| `AttachingSummaries` | Gắn xong | — | `ValidatingIntegrity` | `validate_graph_integrity()` |
| `ValidatingIntegrity` | Thẩm định đạt | ID duy nhất VÀ mọi cạnh có 2 đầu mút | `PersistingAtomic` | Mở `NamedTemporaryFile` |
| `ValidatingIntegrity` | Trùng ID | có ≥ 2 nút trùng `id` | `ValidationFailed` | Ném `ValueError("Graph node IDs must be unique")` |
| `ValidatingIntegrity` | Cạnh mồ côi | đỉnh nguồn/đích không tồn tại | `ValidationFailed` | Ném `ValueError("Edge endpoint is missing")` |
| `PersistingAtomic` | Ghi đệm thành công | ghi trọn vẹn | `Committed` | `os.replace` |
| `PersistingAtomic` | Lỗi I/O | không ghi được | `WriteFailed` | Xóa tệp tạm trong `finally` |
| `Committed`, `ValidationFailed`, `WriteFailed` | — | — | Final | (không nhãn) |

#### 4. Chuyển trạng thái bị cấm
- Không vào `PersistingAtomic` khi chưa qua `ValidatingIntegrity`; không ghi đè trực tiếp `graph.json` mà không qua tệp tạm `.graph.tmp`. Khi `ValidationFailed` **chưa có tệp tạm** nào được tạo.
- **Căn cứ phân tích:** [backend/src/knowledge_graph/builder.py:64-322](file:///e:/FPT/Wiki%20Generation/backend/src/knowledge_graph/builder.py#L64-L322), [builder.py:334-360](file:///e:/FPT/Wiki%20Generation/backend/src/knowledge_graph/builder.py#L334-L360), [backend/src/knowledge_graph/models.py:74-95](file:///e:/FPT/Wiki%20Generation/backend/src/knowledge_graph/models.py#L74-L95).

---

### Đối tượng 5: Phiên Tương tác Trợ lý AI trên Wiki (`AskAIWidgetSession`)

#### 1. Mục đích và Vòng đời Tổng quát
- **Tên đối tượng:** `AskAIWidgetSession`.
- **Mục đích:** Quản lý chu trình tiếp nhận câu hỏi tự nhiên của người đọc trên trình duyệt, xếp hạng ngữ cảnh tri thức, duy trì kết nối truyền luồng với Ollama và thực thi cơ chế hạ cấp dự phòng nội bộ khi mất kết nối.
- **Trạng thái ban đầu:** `Idle` (Chờ câu hỏi).
- **Trạng thái kết thúc:** Final State đạt được khi **đóng widget hoặc rời trang** (`Answered` là trạng thái thường ổn định, chờ câu hỏi mới).

#### 2. Danh sách Trạng thái Đã xác nhận
- `Idle`: Widget đang mở ở trạng thái chờ người dùng nhập câu hỏi.
- `ProbingService`: Đang gửi yêu cầu ngầm kiểm tra sức khỏe dịch vụ Ollama cục bộ.
- `ProcessingIntent`: Đã nhận câu hỏi, đang phân tích ý định và lọc từ khóa.
- `RankingContext`: Đang tính điểm và trích xuất tối đa 12 ký hiệu và 3 chuyên đề khớp nhất từ `wiki_context.json`.
- `StreamingAI`: Đang truyền luồng suy luận thời gian thực từ API Ollama về giao diện chat.
- `FallbackLocal`: Đang tổng hợp câu trả lời từ tri thức nội bộ vì Ollama ngoại tuyến hoặc CORS.
- `Answered`: Câu trả lời đã hiển thị trọn vẹn kèm siêu liên kết, ổn định và sẵn sàng cho câu hỏi tiếp theo.

#### 3. Bảng chuyển trạng thái
| Trạng thái hiện tại | Sự kiện | Guard | Tiếp theo | Hành động |
|---|---|---|---|---|
| Initial | Mở widget | Đã nạp trang | `Idle` | Hiển thị khung chat |
| `Idle` | Tự động ngay sau khi mở, hoặc timer 30 giây | Đã nạp trang | `ProbingService` | `fetch(http://localhost:11434/api/tags)` |
| `ProbingService` | Có phản hồi | có model `qwen2.5-coder:3b` | `Idle` | Chấm xanh "Ollama online" |
| `ProbingService` | Có phản hồi | thiếu model | `Idle` | Chấm đỏ "Ollama offline" |
| `ProbingService` | Không kết nối | lỗi mạng / server tắt | `Idle` | Chấm đỏ "Ollama offline" |
| `Idle` | Bấm Gửi / Enter | `text.trim() != ""` | `ProcessingIntent` | Hiển thị câu hỏi, "Đang suy nghĩ..." |
| `ProcessingIntent` | Tách từ khóa xong | có mảng `words` | `RankingContext` | Tính điểm ký hiệu + chuyên đề |
| `RankingContext` | Đóng gói prompt xong | ngữ cảnh sẵn sàng | `StreamingAI` | POST tới `/api/generate` (`stream: true`) |
| `StreamingAI` | Nhận gói stream | `response.ok == true` | `StreamingAI` | Gắn từ vào khung chat |
| `StreamingAI` | Luồng kết thúc | `done == true` | `Answered` | Hoàn tất câu trả lời AI |
| `StreamingAI` | Lỗi kết nối / CORS | `fetch` ném lỗi hoặc không 200 | `FallbackLocal` | Kích hoạt dự phòng thông minh |
| `FallbackLocal` | Tổng hợp xong | dữ liệu nội bộ đã định dạng | `Answered` | Hiển thị ký hiệu + hướng dẫn lệnh |
| `Answered` | Nhập câu hỏi mới | `text.trim() != ""` | `ProcessingIntent` | Lượt hỏi đáp tiếp theo |
| `Idle` / `Answered` | Đóng widget / rời trang | — | Final | (không nhãn) |

#### 4. Chuyển trạng thái bị cấm
- Không gửi câu hỏi rỗng; không để widget treo khi Ollama ngoại tuyến (phải đi qua `FallbackLocal`).
- **Căn cứ phân tích:** [backend/src/wiki_generation/templates/base.html:305-604](file:///e:/FPT/Wiki%20Generation/backend/src/wiki_generation/templates/base.html#L305-L604).

---

## PHẦN 5: MA TRẬN ĐỐI CHIẾU VÀ HƯỚNG DẪN DỰNG MÔ HÌNH UML

### 1. Ma trận Đối chiếu Chéo giữa Use Case, Activity và State Machine

| Phân hệ nghiệp vụ | Use Case liên quan | Activity Diagram liên quan | Đối tượng State Machine liên quan | Trạng thái xác minh trong Codebase |
|---|:---:|:---:|:---:|:---:|
| **Quét & Lập chỉ mục AST (Epic 1)** | UC-01, UC-02, UC-03, UC-04 | AD-01, AD-02, AD-03, AD-10 | `AnalysisSession`, `GitCloneWorkspace` (`InUse`), `ASTSymbolNode` | **Đã xác nhận** (`scanner.py`, `parsers/`) |
| **Phân tích Phân cấp & AI (Epic 3)** | UC-05, UC-06 | AD-01, AD-04, AD-09 | `AnalysisSession`, `ASTSymbolNode` | **Đã xác nhận** (`chunker.py`, `summarizer.py`, `ollama.py`) |
| **Đồ thị Tri thức (Epic 2)** | UC-08 | AD-01, AD-05 | `AnalysisSession`, `KnowledgeGraph` (`ValidationFailed`/`WriteFailed`) | **Đã xác nhận** (`builder.py`, `models.py`) |
| **Sinh Bộ Wiki Tĩnh (Epic 4)** | UC-10, UC-15, UC-16 | AD-01, AD-06 | `AnalysisSession`, `ASTSymbolNode`, `KnowledgeGraph` | **Đã xác nhận** (`renderer.py`, `templates/`) |
| **Điều phối Dòng lệnh (Epic 5)** | UC-18 | AD-01, AD-10 | `AnalysisSession`, `GitCloneWorkspace` | **Đã xác nhận** (`cli.py`) |
| **Tương tác trên Wiki Web** | UC-20, UC-21, UC-22 | AD-07 (UC-21), AD-08 (UC-22) | `AskAIWidgetSession` (SD-05: ProbingService → Answered) | **Đã xác nhận** (`base.html`) |

### 2. Hướng dẫn dành cho Người vẽ Biểu đồ UML
1. **Use Case Diagram:**
   - Vẽ ranh giới hệ thống (System Boundary) bao toàn bộ 14 Use Case (kể cả Gói 6: UC-20, 21, 22).
   - Thể hiện tác nhân chính `Software Engineer` có mũi tên kế thừa (Generalization) trỏ đến `Wiki User`.
   - Nối các quan hệ `<<include>>`:
     - Từ `UC-18` đến `UC-01`, `UC-05`, `UC-08`, `UC-10, UC-15, UC-16`.
     - Từ `UC-01` đến `UC-03, UC-04`.
   - Nối các quan hệ `<<extend>>`:
     - Từ `UC-06` (Tóm tắt cấu trúc) sang `UC-05` (Tóm tắt AI) khi cờ `--no-llm` hoặc Ollama lỗi.
     - Từ `UC-02` (Phân tích Git URL) sang `UC-01` (Phân tích cục bộ) khi đầu vào là Git URL.
     - **Lưu ý:** Không vẽ quan hệ nào giữa UC-21 và UC-22. UC-21 dùng `search_index.json`, UC-22 dùng `wiki_context.json`, hai UC độc lập. UC-16 chỉ là tiền điều kiện (cung cấp dữ liệu) cho UC-21 và UC-22, không vẽ mũi tên.
   - Nối Actor:
     - Software Engineer: UC-18, UC-01, UC-02.
     - Wiki User: UC-20, UC-21, UC-22.
     - Git Remote Server: UC-02.
     - Ollama LLM Server: UC-05, UC-22.
     - Web Browser & Host OS: UC-18, UC-20, UC-21, UC-22.
     - Các UC nội bộ do pipeline gọi (UC-03, 04, 06, 08, 10, 15, 16): không nối actor.
2. **Activity Diagram:**
   - Dựng các làn bơi (Swimlanes) theo đúng danh mục phân làn đã chỉ định ở từng quy trình trong Phần 3.
   - Sử dụng các hình thoi (Decision Node) với điều kiện bảo vệ `[guard]` tương ứng với các điểm quyết định.
   - Sử dụng thanh phân nhánh song song (Fork Node) và hợp nhất (Join Node) cho quy trình AD-06 (thể hiện hai nhánh độc lập về dữ liệu).
   - Dùng Call Behavior Action cho các quy trình con (AD-02, AD-03, AD-04, AD-05, AD-06, AD-09).
   - Vẽ các luồng ngoại lệ dẫn về các điểm kết thúc thất bại đã định nghĩa.
3. **State Machine Diagram:**
   - Chấm đen (Initial) nối vào: `Idle` (SD-01, SD-05), `Unallocated` (SD-02), `Discovered` (SD-03), `Initialized` (SD-04).
   - Các hàng "(Terminal)" trong bảng chuyển trạng thái: chỉ vẽ mũi tên từ trạng thái đó tới Final State, **không ghi nhãn**.
   - SD-05: `Answered` là trạng thái thường ổn định, Final State chỉ đạt khi đóng widget hoặc rời trang.
   - Chuyển mỗi dòng của Bảng chuyển trạng thái thành một cung chuyển tiếp (Transition Arc) theo cú pháp UML:  
     `Sự_kiện [Điều_kiện_bảo_vệ] / Hành_động_thực_thi`.
   - Tuyệt đối không vẽ các đường chuyển tiếp nằm trong danh mục "Chuyển trạng thái bị cấm".
