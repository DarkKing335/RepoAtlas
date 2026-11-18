# 01 — ĐẶC TẢ KỊCH BẢN USE CASE: HỆ THỐNG REPOATLAS

> **Tài liệu:** Kịch bản Chi tiết Ca sử dụng (Use Case Scenarios Specification)  
> **Chuyên môn:** Phân tích và Thiết kế Hướng đối tượng (OOAD) & Kiến trúc Phần mềm  
> **Dự án đối chiếu:** RepoAtlas (Automated AST-Grounded Repository Documentation Generator)  
> **Mục tiêu:** Cung cấp đặc tả văn bản đầy đủ, chi tiết và chuẩn hóa cho toàn bộ các chức năng đã xác nhận trong hệ thống, làm căn cứ trực tiếp để vẽ Use Case Diagram và thiết lập ma trận truy vết (Traceability Matrix).

---

## I. XÁC ĐỊNH TÁC NHÂN (ACTORS) VÀ CÁC NHÓM CHỨC NĂNG NGHIỆP VỤ

### 1. Danh sách Tác nhân (Actors)

#### 1.1. Tác nhân Người dùng Trực tiếp (Human Actors)
1. **Software Engineer (Kỹ sư Phần mềm - A1):**  
   - *Mô tả:* Lập trình viên, trưởng nhóm kỹ thuật hoặc kỹ sư tích hợp hệ thống. Là người trực tiếp vận hành công cụ dòng lệnh (CLI), cung cấp đường dẫn mã nguồn, thiết lập tham số thực thi (bật/tắt AI) và kích hoạt đường ống phân tích repository.
   - *Mục tiêu:* Tự động trích xuất toàn bộ cấu trúc và sinh tài liệu kỹ thuật hoàn chỉnh cho dự án phần mềm mà không phải viết tài liệu thủ công.
2. **Wiki User (Người đọc Tài liệu Kỹ thuật - A2):**  
   - *Mô tả:* Kỹ sư phần mềm mới tiếp nhận dự án, kiến trúc sư giải pháp (Solution Architect), kỹ sư kiểm thử (QA/QC Engineer) hoặc lập trình viên cần tìm hiểu chức năng codebase. Tác nhân này tương tác với bộ tài liệu tĩnh đã sinh thông qua trình duyệt web.
   - *Mục tiêu:* Duyệt cấu trúc phân cấp, tra cứu nhanh vị trí các lớp/hàm, đọc hướng dẫn công nghệ, kiến trúc, kiểm thử và đặt câu hỏi cho trợ lý AI nhúng trên trang.
   - *Quan hệ kế thừa (Generalization):* **Software Engineer IS-A Wiki User.** Sau khi hoàn thành việc chạy lệnh phân tích, kỹ sư phần mềm sẽ trực tiếp mở trình duyệt và sử dụng tài liệu như một người đọc wiki thông thường.

#### 1.2. Tác nhân Hệ thống Bên ngoài (External System Actors)
1. **Git Remote Server (Máy chủ Lưu trữ Git Từ xa - EX1):**  
   - *Mô tả:* Các nền tảng lưu trữ mã nguồn trực tuyến như GitHub, GitLab hoặc máy chủ Git nội bộ của doanh nghiệp.
   - *Vai trò:* Tiếp nhận yêu cầu tải mã nguồn tinh gọn (`git clone --depth 1`) khi người dùng cung cấp URL thay vì đường dẫn cục bộ.
2. **Ollama LLM Server (Máy chủ Mô hình Ngôn ngữ Cục bộ - EX2):**  
   - *Mô tả:* Dịch vụ máy chủ suy luận mô hình ngôn ngữ chạy trực tiếp trên máy cục bộ của người dùng (mặc định tại cổng `11434` với mô hình mã nguồn `qwen2.5-coder:3b`).
   - *Vai trò:* Cung cấp API suy luận để sinh tóm tắt ngôn ngữ tự nhiên cho các nút cây phân cấp và giải đáp câu hỏi của người dùng trên giao diện widget wiki.
3. **Web Browser & Host OS (Trình duyệt Web và Môi trường Hệ điều hành - EX3):**  
   - *Mô tả:* Ứng dụng duyệt web mặc định của hệ thống cùng giao diện gọi lệnh hệ điều hành máy trạm (Windows, Linux, macOS).
   - *Vai trò:* Tự động kích hoạt mở tệp `wiki/index.html` sau khi sinh xong tài liệu và môi trường thực thi mã nguồn JavaScript phía máy trạm.

---

### 2. Phân nhóm Chức năng Nghiệp vụ (Use Case Packages)

Hệ thống được tổ chức thành 6 nhóm chức năng nghiệp vụ tương ứng với kiến trúc module:
- **Gói 1: Quét và Phân tích Cú pháp Mã nguồn (Core Indexing Subsystem - Epic 1):** Bao gồm việc tiếp nhận mã nguồn cục bộ/từ xa, duyệt cấu trúc cây thư mục, bỏ qua tệp rác và phân tích AST các ngôn ngữ Java, C#.
- **Gói 2: Phân tích Phân cấp và Tóm tắt Nội dung bằng AI (AI Analysis Subsystem - Epic 3):** Bao gồm chia nhỏ cú pháp theo 6 tầng phân cấp, quản lý hạn mức ngân sách token và tóm tắt bottom-up qua AI hoặc hạ cấp cấu trúc.
- **Gói 3: Xây dựng và Quản trị Đồ thị Tri thức (Knowledge Graph Subsystem - Epic 2):** Bao gồm việc hợp nhất siêu dữ liệu chỉ mục và tóm tắt thành đồ thị đa thực thể, bù trừ nút ngoại vi và ghi tệp nguyên tử.
- **Gói 4: Sinh Bộ Tài liệu Wiki Tĩnh Đa trang (Wiki Generation Subsystem - Epic 4):** Bao gồm việc nạp khuôn mẫu Jinja2, kết xuất các trang chuyên đề, kết xuất trang ký hiệu, sinh chỉ mục tìm kiếm và ngữ cảnh AI.
- **Gói 5: Điều phối Dòng lệnh và Khởi chạy Hệ thống (CLI Orchestration Subsystem - Epic 5):** Đóng gói toàn bộ quy trình thành một lệnh duy nhất, điều phối 4 phân hệ và mở trình duyệt tự động.
- **Gói 6: Tra cứu, Khám phá và Tương tác Ngoại tuyến (Wiki Exploration & Interaction):** Các tương tác phía người đọc trên trình duyệt: duyệt thanh bên, tìm kiếm trực tiếp và trò chuyện với trợ lý AI.

---

## II. ĐẶC TẢ CHI TIẾT CÁC KỊCH BẢN USE CASE

---

### GÓI 1: QUÉT VÀ PHÂN TÍCH CÚ PHÁP MÃ NGUỒN (CORE INDEXING)

#### UC-01: Phân tích Repository Cục bộ (Analyze Local Repository)
1. **Mã và tên kịch bản:** UC-01 — Phân tích Repository Cục bộ.
2. **Mục tiêu nghiệp vụ:** Quét cấu trúc thư mục, nhận diện toàn bộ tệp nguồn được hỗ trợ trên ổ đĩa máy tính, phân tích cú pháp AST và sản sinh bảng chỉ mục trung gian thống nhất.
3. **Actor chính và actor phụ:**  
   - Actor chính: Software Engineer (A1).  
   - Actor phụ: Không có.
4. **Bối cảnh sử dụng:** Kỹ sư phần mềm cần lập tài liệu cho một dự án mã nguồn đang có sẵn trên máy tính làm việc.
5. **Điều kiện trước khi thực hiện (Preconditions):**  
   - Đường dẫn thư mục cung cấp phải tồn tại trên hệ điều hành và có quyền đọc dữ liệu.
   - Dự án chứa ít nhất một tệp tin nguồn có phần mở rộng `.java` hoặc `.cs`.
6. **Sự kiện kích hoạt (Trigger):** Kỹ sư phần mềm gõ lệnh phân tích kèm đường dẫn thư mục cục bộ (hoặc để mặc định thư mục hiện tại `.`).
7. **Luồng xử lý chính (Main Flow):**  
   - *Bước 1:* Hệ thống nhận tham số đường dẫn và xác minh đây là đường dẫn thư mục nội bộ (không phải URL Git).
   - *Bước 2:* Hệ thống kiểm tra sự tồn tại và tính hợp lệ của thư mục.
   - *Bước 3:* Hệ thống tải và phân tích các quy tắc loại trừ trong tệp `.gitignore` nếu có tại thư mục gốc của repository.
   - *Bước 4:* Hệ thống duyệt đệ quy cây thư mục, bỏ qua các thư mục hệ thống/bản dựng mặc định (`.git`, `node_modules`, `bin`, `obj`, `target`, `build`...), xây dựng cây cấu trúc thư mục.
   - *Bước 5:* Hệ thống lưu trữ cây cấu trúc thư mục ra tệp `indexes/structure.json`.
   - *Bước 6:* Hệ thống duyệt từng tệp nguồn `.java` và `.cs`, kích hoạt bộ phân tích AST tương ứng để trích xuất toàn bộ ký hiệu mã nguồn và quan hệ.
   - *Bước 7:* Hệ thống tổng hợp danh sách chỉ mục tệp thành một bảng chỉ mục ký hiệu duy nhất của toàn bộ kho mã nguồn.
   - *Bước 8:* Hệ thống xuất khẩu bảng chỉ mục ra tệp `indexes/repository_index.json` và tệp tổng quan `indexes/structure_overview.json`.
8. **Các luồng thay thế (Alternative Flows):**  
   - *Alt 1a — Không tìm thấy tệp `.gitignore`:* Hệ thống bỏ qua bước nạp bộ lọc tùy biến và áp dụng danh sách loại trừ mặc định của hệ thống để tiếp tục quét.
   - *Alt 1b — Một số tệp tin bị lỗi cú pháp cục bộ:* Hệ thống ghi nhận cảnh báo lỗi cho tệp đó, bỏ qua và tiếp tục phân tích các tệp còn lại trong dự án.
9. **Các luồng ngoại lệ (Exception Flows):**  
   - *Exc 1a — Đường dẫn cục bộ không tồn tại:* Hệ thống thông báo lỗi đường dẫn không hợp lệ, dừng phiên làm việc ngay lập tức.
   - *Exc 1b — Thư mục không có quyền truy cập:* Hệ thống thông báo lỗi phân quyền hệ thống và kết thúc phiên làm việc.
10. **Điều kiện thành công và kết quả sau khi thực hiện (Postconditions):**  
    - Tệp `indexes/structure.json`, `indexes/repository_index.json` và `indexes/structure_overview.json` được tạo thành công, chứa toàn bộ ký hiệu của dự án.
11. **Quy tắc nghiệp vụ liên quan:**  
    - Chỉ nhận diện và phân tích các tệp có đuôi `.java` và `.cs`.
    - Bắt buộc lọc bỏ các thư mục rác theo danh sách loại trừ mặc định (`DEFAULT_EXCLUDES`).
12. **Những chức năng chưa được xác nhận:** Chưa xác nhận cơ chế theo dõi thay đổi tệp (file watcher) để chỉ quét lại các tệp đã sửa đổi (incremental indexing).
13. **Căn cứ phân tích:**  
    - Code: `backend/src/core_indexing/scanner.py:89-118` (hàm `prepare_repository`), `scanner.py:120-129` (hàm `load_gitignore`), `scanner.py:184-219` (hàm `scan_and_parse`), `backend/src/core_indexing/ir_generator.py:17-48`.
    - Tài liệu: `docs/user-stories.md` US-1.1, US-1.2, `docs/designs/ast-parser-design.md`.

---

#### UC-02: Phân tích Repository từ Git URL (Analyze Remote Git Repository)
1. **Mã và tên kịch bản:** UC-02 — Phân tích Repository từ Git URL.
2. **Mục tiêu nghiệp vụ:** Tiếp nhận địa chỉ repository từ xa, tải bản sao tinh gọn vào không gian tạm thời trên máy cục bộ, thực hiện phân tích cú pháp và đảm bảo thu hồi toàn bộ tài nguyên tạm thời.
3. **Actor chính và actor phụ:**  
   - Actor chính: Software Engineer (A1).  
   - Actor phụ: Git Remote Server (EX1).
4. **Bối cảnh sử dụng:** Kỹ sư phần mềm cần lập tài liệu cho một dự án mã nguồn mở hoặc kho mã nguồn nội bộ công ty được lưu trữ trên GitHub/GitLab mà chưa tải về máy.
5. **Điều kiện trước khi thực hiện:**  
   - Máy trạm có kết nối mạng Internet và đã cài đặt công cụ dòng lệnh Git.
   - Địa chỉ URL Git hợp lệ và kho mã nguồn ở chế độ công khai (hoặc máy trạm đã thiết lập khóa truy cập SSH/Personal Access Token hợp lệ).
6. **Sự kiện kích hoạt:** Kỹ sư phần mềm gõ lệnh phân tích kèm một đường dẫn dạng URL (`https://...`, `git@...`) hoặc định danh rút gọn (`owner/repo`).
7. **Luồng xử lý chính:**  
   - *Bước 1:* Hệ thống kiểm tra chuỗi đầu vào và nhận diện đây là một địa chỉ kho lưu trữ Git từ xa.
   - *Bước 2:* Nếu đầu vào là định danh rút gọn (`owner/repo`), hệ thống tự động chuẩn hóa thành URL Git đầy đủ (`https://github.com/owner/repo.git`).
   - *Bước 3:* Hệ thống tạo một thư mục tạm thời độc lập trên ổ đĩa máy tính với tiền tố định danh an toàn.
   - *Bước 4:* Hệ thống phát lệnh gọi tiến trình Git để tải bản sao nông của repository với độ sâu lịch sử bằng 1 (`git clone --depth 1`).
   - *Bước 5:* Máy chủ Git từ xa tiếp nhận và truyền dữ liệu mã nguồn về thư mục tạm.
   - *Bước 6:* Sau khi tải hoàn tất, hệ thống chuyển giao đường dẫn thư mục tạm cho quy trình phân tích nội bộ (thực hiện theo các bước từ Bước 3 đến Bước 8 của UC-01).
   - *Bước 7:* Sau khi toàn bộ quy trình kết thúc (dù thành công hay thất bại), hệ thống kích hoạt cơ chế dọn dẹp để xóa bỏ toàn bộ thư mục tạm thời trên đĩa.
8. **Các luồng thay thế:**  
   - *Alt 2a — Chuỗi URL kết thúc bằng `.git` hoặc sử dụng giao thức SSH:* Hệ thống giữ nguyên chuỗi kết nối và thực thi clone trực tiếp.
9. **Các luồng ngoại lệ:**  
   - *Exc 2a — Lỗi kết nối mạng hoặc kho mã nguồn không tồn tại:* Lệnh clone thất bại, hệ thống bắt giữ lỗi từ Git, ngay lập tức xóa thư mục tạm đã tạo, in thông báo lỗi và kết thúc phiên làm việc.
   - *Exc 2b — Máy trạm chưa cài đặt Git:* Hệ thống thông báo không thể tìm thấy lệnh Git và dừng phiên làm việc.
10. **Điều kiện thành công và kết quả sau khi thực hiện:**  
    - Bảng chỉ mục ký hiệu và cấu trúc dự án từ xa được tạo hoàn chỉnh trong thư mục `indexes/`.
    - Thư mục tạm thời được xóa sạch hoàn toàn khỏi ổ đĩa máy tính.
11. **Quy tắc nghiệp vụ liên quan:**  
    - Bắt buộc chỉ lấy commit gần nhất (`--depth 1`) để tối ưu hóa thời gian tải và giảm thiểu dung lượng đĩa sử dụng.
    - Cơ chế dọn dẹp thư mục tạm phải luôn được đảm bảo thực thi trong khối xử lý kết thúc bắt buộc (`finally block`).
12. **Những chức năng chưa được xác nhận:** Chưa xác nhận cơ chế nhập tài khoản/mật khẩu tương tác trong phiên CLI nếu repository là kho riêng tư (private) và máy trạm chưa lưu chứng thư xác thực.
13. **Căn cứ phân tích:**  
    - Code: `backend/src/core_indexing/scanner.py:70-87` (hàm `_is_git_url`), `scanner.py:89-111` (hàm `prepare_repository`), `scanner.py:221-226` (hàm `cleanup`), `backend/src/cli.py:141-144`.
    - Tài liệu: `docs/user-stories.md` US-1.1.

---

#### UC-03: Phân tích Cú pháp Mã nguồn Java (Parse Java Source Code)
1. **Mã và tên kịch bản:** UC-03 — Phân tích Cú pháp Mã nguồn Java.
2. **Mục tiêu nghiệp vụ:** Sử dụng bộ phân tích cú pháp chuyên biệt theo chuẩn văn phạm Java để mổ xẻ cây cú pháp trừu tượng (AST), trích xuất thông tin các lớp, phương thức, chú thích kiến trúc và tạo lập quan hệ liên kết.
3. **Actor chính và actor phụ:**  
   - Actor chính: Software Engineer (thông qua hệ thống quét mã nguồn).  
   - Actor phụ: Không có.
4. **Bối cảnh sử dụng:** Được tự động triệu gọi (thông qua quan hệ `<<include>>` từ UC-01/UC-02) mỗi khi hệ thống phát hiện một tệp tin có phần mở rộng `.java`.
5. **Điều kiện trước khi thực hiện:** Tệp tin `.java` tồn tại, có thể đọc được nội dung văn bản dưới dạng UTF-8.
6. **Sự kiện kích hoạt:** Hệ thống duyệt đến một tệp có phần mở rộng `.java` trong cây thư mục dự án.
7. **Luồng xử lý chính:**  
   - *Bước 1:* Hệ thống đọc nội dung tệp mã nguồn Java.
   - *Bước 2:* Bộ phân tích Java khởi tạo cây cú pháp AST của tệp thông qua thư viện phân tích cú pháp.
   - *Bước 3:* Hệ thống trích xuất khai báo gói (`package`) và danh sách các chỉ thị nhập khẩu thư viện (`import`).
   - *Bước 4:* Hệ thống duyệt các nút định nghĩa kiểu dữ liệu trong AST: Lớp (`class`), Giao diện (`interface`), Bảng liệt kê (`enum`), Bản ghi (`record`).
   - *Bước 5:* Với mỗi kiểu dữ liệu, hệ thống trích xuất tên đầy đủ (FQN = package + type name), phạm vi truy cập (`public`, `protected`, `private`), ghi chú tài liệu Javadoc, các chú thích framework (`@RestController`, `@Service`, `@Entity`...) cùng danh sách lớp cha (`extends`) và giao diện cài đặt (`implements`).
   - *Bước 6:* Hệ thống duyệt các nút con bên trong kiểu dữ liệu: Phương thức (`method`), Hàm khởi tạo (`constructor`), Trường dữ liệu (`field`).
   - *Bước 7:* Với mỗi phương thức, hệ thống trích xuất kiểu trả về, danh sách tham số (kiểu và tên), danh sách ngoại lệ ném ra (`throws`), phạm vi dòng mã nguồn trong tệp và các lời gọi hàm bên trong thân phương thức.
   - *Bước 8:* Hệ thống đóng gói toàn bộ dữ liệu thành một đối tượng chỉ mục tệp Java và trả về cho phân hệ lập chỉ mục repository.
8. **Các luồng thay thế:**  
   - *Alt 3a — Tệp Java không có khai báo package:* Hệ thống tự động gán kiểu dữ liệu vào không gian gói mặc định (`default package`).
9. **Các luồng ngoại lệ:**  
   - *Exc 3a — Tệp tin bị lỗi cú pháp nghiêm trọng (syntax error):* Bộ phân tích AST không thể tạo cây cú pháp trọn vẹn; hệ thống bắt ngoại lệ, ghi nhận cảnh báo vào nhật ký và trả về chỉ mục rỗng cho tệp đó để không làm gián đoạn toàn bộ dự án.
10. **Điều kiện thành công và kết quả sau khi thực hiện:** Một đối tượng `FileIndex` chứa đầy đủ danh sách các `ASTSymbolNode` của tệp Java được bổ sung vào bộ nhớ hệ thống.
11. **Quy tắc nghiệp vụ liên quan:**  
    - Tên định danh toàn cục (`symbol_id` và `fully_qualified_name`) của ký hiệu Java phải được ghép chuẩn hóa: `package.ClassName.methodName(ParamType1,ParamType2)`.
12. **Những chức năng chưa được xác nhận:** Chưa xác nhận khả năng phân tích cú pháp các tính năng mới nhất của Java 21+ như Virtual Threads hay Pattern Matching mở rộng.
13. **Căn cứ phân tích:**  
    - Code: `backend/src/core_indexing/parsers/java_parser.py`, `backend/src/core_indexing/models.py:121-160`.
    - Tài liệu: `docs/designs/ast-parser-design.md:Section 3, Section 6`.

---

#### UC-04: Phân tích Cú pháp Mã nguồn C# (Parse C# Source Code)
1. **Mã và tên kịch bản:** UC-04 — Phân tích Cú pháp Mã nguồn C#.
2. **Mục tiêu nghiệp vụ:** Sử dụng bộ phân tích cú pháp chuyên biệt theo chuẩn văn phạm C# để mổ xẻ cây cú pháp trừu tượng (AST), trích xuất thông tin các không gian tên, lớp, giao diện, cấu trúc, thuộc tính với accessor, hàm bất đồng bộ và chú thích XML Doc.
3. **Actor chính và actor phụ:**  
   - Actor chính: Software Engineer (thông qua hệ thống quét mã nguồn).  
   - Actor phụ: Không có.
4. **Bối cảnh sử dụng:** Được tự động triệu gọi (thông qua quan hệ `<<include>>` từ UC-01/UC-02) mỗi khi hệ thống phát hiện một tệp tin có phần mở rộng `.cs`.
5. **Điều kiện trước khi thực hiện:** Tệp tin `.cs` tồn tại, có thể đọc được nội dung văn bản dưới dạng UTF-8.
6. **Sự kiện kích hoạt:** Hệ thống duyệt đến một tệp có phần mở rộng `.cs` trong cây thư mục dự án.
7. **Luồng xử lý chính:**  
   - *Bước 1:* Hệ thống đọc nội dung tệp mã nguồn C#.
   - *Bước 2:* Bộ phân tích C# khởi tạo cây cú pháp AST của tệp.
   - *Bước 3:* Hệ thống trích xuất không gian tên (`namespace` truyền thống dạng khối hoặc file-scoped namespace) và các chỉ thị sử dụng thư viện (`using`).
   - *Bước 4:* Hệ thống duyệt các nút định nghĩa kiểu dữ liệu trong AST: Lớp (`class`), Giao diện (`interface`), Bảng liệt kê (`enum`), Cấu trúc (`struct`), Bản ghi (`record`, `record struct`).
   - *Bước 5:* Với mỗi kiểu dữ liệu, hệ thống trích xuất tên đầy đủ (FQN = namespace + type name), các bổ từ truy cập (`public`, `internal`, `private`, `protected`), ghi chú XML Doc (`/// <summary>`), các thuộc tính framework (`[ApiController]`, `[HttpGet]`, `[Table]`...) và danh sách kiểu cơ sở/giao diện kế thừa.
   - *Bước 6:* Hệ thống duyệt các nút con: Phương thức (`method`), Hàm khởi tạo (`constructor`), Thuộc tính (`property`), Trường dữ liệu (`field`).
   - *Bước 7:* Với mỗi thuộc tính, hệ thống trích xuất thông tin accessor chi tiết: có getter (`get`), có setter (`set`), có init-only setter (`init`). Với phương thức, nhận diện cờ bất đồng bộ (`is_async = True` nếu có từ khóa `async`).
   - *Bước 8:* Hệ thống đóng gói toàn bộ dữ liệu thành một đối tượng chỉ mục tệp C# và trả về cho phân hệ lập chỉ mục repository.
8. **Các luồng thay thế:**  
   - *Alt 4a — Tệp sử dụng File-scoped namespace (C# 10+):* Hệ thống nhận diện cú pháp `namespace MyNamespace;` và áp dụng không gian tên đó cho toàn bộ các kiểu dữ liệu trong tệp.
9. **Các luồng ngoại lệ:**  
   - *Exc 4a — Lỗi cú pháp mã nguồn C#:* Hệ thống bắt lỗi, ghi cảnh báo tệp lỗi và tiếp tục các tệp khác.
10. **Điều kiện thành công và kết quả sau khi thực hiện:** Một đối tượng `FileIndex` chứa đầy đủ danh sách các `ASTSymbolNode` của tệp C# được bổ sung vào bộ nhớ hệ thống.
11. **Quy tắc nghiệp vụ liên quan:**  
    - Tên định danh toàn cục của ký hiệu C# được ghép theo quy tắc: `Namespace.ClassName.MethodName(ParamType1)`.
12. **Những chức năng chưa được xác nhận:** Chưa xác nhận khả năng giải quyết các định nghĩa lớp từng phần (partial class) nằm phân tán trên nhiều tệp tin khác nhau thành một thực thể duy nhất.
13. **Căn cứ phân tích:**  
    - Code: `backend/src/core_indexing/parsers/csharp_parser.py`, `backend/src/core_indexing/models.py:109-115` (`PropertyAccessors`), `models.py:121-160`.
    - Tài liệu: `docs/designs/ast-parser-design.md:Section 4, Section 6`.

---

### GÓI 2: PHÂN TÍCH PHÂN CẤP VÀ TÓM TẮT NỘI DUNG BẰNG AI (AI ANALYSIS)

#### UC-05: Tóm tắt Phân cấp Mã nguồn bằng Mô hình Ngôn ngữ Cục bộ (Ollama)
1. **Mã và tên kịch bản:** UC-05 — Tóm tắt Phân cấp Mã nguồn bằng Mô hình Ngôn ngữ Cục bộ.
2. **Mục tiêu nghiệp vụ:** Sử dụng máy chủ Ollama chạy cục bộ để sinh văn bản giải thích tự nhiên cho toàn bộ các thành phần trong mã nguồn theo chiều từ dưới lên (Bottom-Up), kết hợp kiểm soát ngân sách token để không vượt quá giới hạn xử lý của mô hình nhỏ.
3. **Actor chính và actor phụ:**  
   - Actor chính: Software Engineer (A1).  
   - Actor phụ: Ollama LLM Server (EX2).
4. **Bối cảnh sử dụng:** Được kích hoạt trong đường ống phân tích khi người dùng bật chế độ AI (`use_llm = True`).
5. **Điều kiện trước khi thực hiện:**  
   - Bảng chỉ mục ký hiệu `repository_index.json` đã được tạo thành công từ Phân hệ 1.
   - Dịch vụ Ollama đang chạy tại cổng mạng cục bộ (`http://localhost:11434`) và đã tải trọng số mô hình `qwen2.5-coder:3b`.
6. **Sự kiện kích hoạt:** Hệ thống bước vào giai đoạn 2 của đường ống phân tích.
7. **Luồng xử lý chính:**  
   - *Bước 1:* Hệ thống thực hiện kiểm tra kết nối mạng (health check) đến máy chủ Ollama.
   - *Bước 2:* Hệ thống nạp bảng chỉ mục và xây dựng cây phân cấp mã nguồn 6 tầng (`Repository → Module → Container → Component → Class → Method`).
   - *Bước 3:* Hệ thống lấy danh sách toàn bộ các nút trong cây phân cấp và sắp xếp theo thứ tự duyệt từ dưới lên (sâu nhất trước: tầng Phương thức trước, rồi đến Lớp, Nhóm thành phần, Đơn vị triển khai, Phân hệ và cuối cùng là Kho lưu trữ).
   - *Bước 4:* Với mỗi nút tầng Phương thức và Lớp, hệ thống trích xuất khung xương cú pháp AST (bỏ qua phần thân chi tiết).
   - *Bước 5:* Hệ thống tính toán lượng token ước tính của ngữ cảnh; nếu vượt quá trần ngân sách quy định (2000 tokens), hệ thống tự động cắt tỉa phần chữ ký phụ để đảm bảo vừa khít ngân sách.
   - *Bước 6:* Hệ thống đóng gói câu lệnh nhắc (prompt) và gửi yêu cầu suy luận đến API `/api/generate` của Ollama.
   - *Bước 7:* Ollama trả về chuỗi văn bản tóm tắt tự nhiên giải thích chức năng của thành phần.
   - *Bước 8:* Hệ thống thẩm định chống ảo giác: kiểm tra xem các ký hiệu được nhắc đến trong đoạn văn bản tóm tắt có thực sự tồn tại trong bảng chỉ mục mã nguồn không; chỉ các ký hiệu hợp lệ mới được lưu vết (`referenced_symbols`).
   - *Bước 9:* Khi tóm tắt các tầng cao hơn (Lớp, Nhóm thành phần, Phân hệ), hệ thống tổng hợp phần tóm tắt của các nút con cấp dưới đã tạo ở các bước trước để làm ngữ cảnh tóm tắt cho nút cha.
   - *Bước 10:* Hệ thống kích hoạt bộ sinh nội dung chuyên đề để tạo các khối tài liệu cho 4 trang: công nghệ, kiểm thử, kiến trúc và phân rã phân hệ.
   - *Bước 11:* Toàn bộ kết quả tóm tắt và báo cáo token được lưu trữ vào tệp `analysis/summaries.json`.
8. **Các luồng thay thế:**  
   - *Alt 5a — Dịch vụ Ollama không phản hồi hoặc thiếu mô hình:* Hệ thống tự động kích hoạt quan hệ `<<extend>>` chuyển sang kịch bản UC-06 (Tóm tắt Cấu trúc Dự phòng).
9. **Các luồng ngoại lệ:**  
   - *Exc 5a — Tệp chỉ mục `repository_index.json` bị thiếu hoặc hỏng:* Hệ thống báo lỗi dữ liệu đầu vào và dừng quy trình phân tích.
10. **Điều kiện thành công và kết quả sau khi thực hiện:** Tệp `analysis/summaries.json` được tạo ra, chứa toàn bộ tóm tắt AI cho từng nút cây phân cấp và nội dung của 4 chuyên đề wiki.
11. **Quy tắc nghiệp vụ liên quan:**  
    - Không bao giờ được gửi vượt quá 2000 tokens trong một yêu cầu gửi tới Ollama (ràng buộc ngân sách token).
    - Quy trình tóm tắt bắt buộc phải thực hiện theo thứ tự từ dưới lên (Bottom-Up) để tầng trên tái sử dụng tri thức tầng dưới.
12. **Những chức năng chưa được xác nhận:** Chưa xác nhận cơ chế lưu bộ đệm kết quả tóm tắt (caching) giữa các lần chạy khác nhau nếu mã nguồn phương thức không đổi.
13. **Căn cứ phân tích:**  
    - Code: `backend/src/ai_analysis/__main__.py:93-167`, `backend/src/ai_analysis/summarizer.py`, `backend/src/ai_analysis/chunker.py`, `backend/src/ai_analysis/llm/ollama.py`.
    - Tài liệu: `docs/designs/hierarchical-prompting-chunking.md`, `docs/user-stories.md` US-3.1 - US-3.5.

---

#### UC-06: Tóm tắt Cấu trúc Mã nguồn Dự phòng (Generate Structural Summaries - No-LLM Mode)
1. **Mã và tên kịch bản:** UC-06 — Tóm tắt Cấu trúc Mã nguồn Dự phòng (Chế độ không sử dụng AI).
2. **Mục tiêu nghiệp vụ:** Tự động tạo nội dung tài liệu tổng quan và tóm tắt thành phần dựa trên việc phân tích siêu dữ liệu cấu trúc thuần túy, đảm bảo hệ thống vẫn sinh được đầy đủ tài liệu wiki khi không có kết nối đến mô hình AI.
3. **Actor chính và actor phụ:**  
   - Actor chính: Software Engineer (A1).  
   - Actor phụ: Không có.
4. **Bối cảnh sử dụng:** Kỹ sư phần mềm chỉ định cờ `--no-llm` để chạy nhanh, hoặc hệ thống tự động hạ cấp (thông qua `<<extend>>` từ UC-05) khi máy chủ Ollama ngoại tuyến.
5. **Điều kiện trước khi thực hiện:** Tệp `indexes/repository_index.json` đã tồn tại.
6. **Sự kiện kích hoạt:** Lệnh CLI có cờ `--no-llm` hoặc kiểm tra sức khỏe dịch vụ Ollama thất bại.
7. **Luồng xử lý chính:**  
   - *Bước 1:* Hệ thống khởi tạo đối tượng khách mô hình giả định (`NullLLMClient` với thuộc tính `enabled = False`).
   - *Bước 2:* Hệ thống nạp bảng chỉ mục và dựng cây phân cấp 6 tầng.
   - *Bước 3:* Hệ thống duyệt qua tất cả các nút trong cây phân cấp.
   - *Bước 4:* Với mỗi nút, hệ thống sinh đoạn tóm tắt cấu trúc tiêu chuẩn dựa trên thông tin định lượng sẵn có: kiểu ký hiệu, số lượng phương thức, đường dẫn tệp, các giao diện cài đặt hoặc số lượng thành phần con.
   - *Bước 5:* Bộ sinh nội dung chuyên đề tạo 4 phần nội dung (`tech`, `tests`, `architecture`, `modules`) dựa trên các quy tắc dò tìm dấu hiệu (heuristic rules: phát hiện framework từ chú thích và tệp build).
   - *Bước 6:* Hệ thống ghi nhận kết quả ra tệp `analysis/summaries.json` với trường đánh dấu nguồn gốc `generated_by = "structural"`.
8. **Các luồng thay thế:** Không có.
9. **Các luồng ngoại lệ:** Tệp chỉ mục đầu vào bị thiếu hoặc định dạng không hợp lệ.
10. **Điều kiện thành công và kết quả sau khi thực hiện:** Tệp `analysis/summaries.json` được tạo thành công với các bản tóm tắt cấu trúc xác định, tốc độ thực thi gần như tức thì.
11. **Quy tắc nghiệp vụ liên quan:** Tài liệu sinh ra ở chế độ cấu trúc phải có cùng cấu trúc lược đồ dữ liệu với chế độ AI để không làm lỗi các bước render phía sau.
12. **Những chức năng chưa được xác nhận:** Chưa xác nhận các mẫu văn bản sinh cấu trúc có hỗ trợ tùy biến đa ngôn ngữ (tiếng Việt/tiếng Anh) qua cấu hình người dùng hay không.
13. **Căn cứ phân tích:**  
    - Code: `backend/src/ai_analysis/llm/null.py`, `backend/src/ai_analysis/__main__.py:99-111`, `backend/src/ai_analysis/content_generator.py`.
    - Tài liệu: `docs/epics.md` Epic 3, `docs/adrs.md` ADR-006.

---

### GÓI 3: XÂY DỰNG VÀ QUẢN TRỊ ĐỒ THỊ TRI THỨC (KNOWLEDGE GRAPH)

#### UC-08: Xây dựng và Thẩm định Đồ thị Tri thức Đa thực thể (Build & Validate Knowledge Graph)
1. **Mã và tên kịch bản:** UC-08 — Xây dựng và Thẩm định Đồ thị Tri thức Đa thực thể.
2. **Mục tiêu nghiệp vụ:** Hợp nhất siêu dữ liệu mã nguồn AST và nội dung tóm tắt phân cấp thành một đồ thị tri thức duy nhất, tự động bù trừ các nút thư viện ngoài để chống lỗi tham chiếu mồ côi, thẩm định tính toàn vẹn và lưu trữ nguyên tử xuống đĩa.
3. **Actor chính và actor phụ:**  
   - Actor chính: Software Engineer (thông qua điều phối pipeline).  
   - Actor phụ: Không có.
4. **Bối cảnh sử dụng:** Được tự động triệu gọi tại Giai đoạn 3 của đường ống phân tích repository.
5. **Điều kiện trước khi thực hiện:** Thư mục `indexes/` (chứa `repository_index.json`) và thư mục `analysis/` (chứa `summaries.json`) đã hoàn tất.
6. **Sự kiện kích hoạt:** Hoàn thành bước phân tích AI / tóm tắt cấu trúc.
7. **Luồng xử lý chính:**  
   - *Bước 1:* Phân hệ nạp dữ liệu từ `indexes/repository_index.json` và `analysis/summaries.json`.
   - *Bước 2:* Hệ thống khởi tạo nút gốc đại diện cho toàn bộ kho mã nguồn trong đồ thị (`repository:<name>`).
   - *Bước 3:* Hệ thống tạo các nút đại diện cho từng tệp nguồn (`file:<path>`) và nút ký hiệu AST (`symbol:<fqn>`).
   - *Bước 4:* Hệ thống nạp cây phân loại, tạo các nút nhóm cấu trúc Module, Container, Component và gắn quan hệ chứa đựng.
   - *Bước 5:* Hệ thống duyệt danh sách quan hệ và tạo các cạnh có hướng: chứa đựng (`contains`), kế thừa (`extends`), cài đặt (`implements`), gọi phương thức (`calls`), sử dụng trường (`uses_field`).
   - *Bước 6:* Với mỗi cạnh trỏ đến lớp/thư viện ngoài dự án (SDK, thư viện bên thứ ba), hệ thống tự động sinh nút giả lập ngoại vi (`type = EXTERNAL`, `external = True`) rồi mới tạo cạnh.
   - *Bước 7:* Hệ thống gắn nội dung tóm tắt vào thuộc tính `metadata.summary` của từng nút.
   - *Bước 8:* Hệ thống thẩm định tính toàn vẹn: không trùng `id` nút, không có cạnh mồ côi.
   - *Bước 9:* Hệ thống ghi đĩa nguyên tử: ghi vào tệp tạm `.graph.tmp` trong `graphs/`, rồi `os.replace` thành `graphs/graph.json`.
8. **Các luồng thay thế:**  
   - *Alt 8a — Không có dữ liệu AI Analysis:* Hệ thống vẫn xây dựng đồ thị từ chỉ mục cú pháp và cây cấu trúc thư mục, để trống phần tóm tắt.
9. **Các luồng ngoại lệ:**  
   - *Exc 8a — Thẩm định toàn vẹn thất bại (trùng ID nút hoặc cạnh mồ côi):* ném `ValueError`, dừng pipeline. Lúc này **chưa tạo tệp tạm** nên chưa có gì để hủy.
   - *Exc 8b — Lỗi ghi đĩa khi đang ghi tệp tạm:* xóa tệp tạm trong khối `finally`, dừng pipeline.
10. **Điều kiện thành công và kết quả sau khi thực hiện:** Tệp `graphs/graph.json` được tạo thành công, bảo đảm toàn vẹn cấu trúc và sẵn sàng làm nguồn dữ liệu cho phân hệ hiển thị.
11. **Quy tắc nghiệp vụ liên quan:**  
    - Không cho phép tồn tại cạnh mồ côi (dangling edge) trong đồ thị.
    - Quá trình ghi tệp bắt buộc phải là thao tác nguyên tử để phòng tránh lỗi hỏng tệp khi mất nguồn điện hoặc bị ngắt đột ngột.
12. **Những chức năng chưa được xác nhận:** Chưa xác nhận API truy vấn đồ thị độc lập theo chuẩn GraphQL hoặc SPARQL từ các ứng dụng bên thứ ba.
13. **Căn cứ phân tích:**  
    - Code: `backend/src/knowledge_graph/builder.py:64-322` (lớp `GraphBuilder`), `builder.py:334-360` (hàm `write_graph`), `backend/src/knowledge_graph/models.py:74-95` (hàm `validate_graph_integrity`).
    - Tài liệu: `docs/designs/knowledge-graph-schema.md`, `docs/user-stories.md` US-2.1, US-2.2, US-2.3.

---

### GÓI 4: SINH BỘ TÀI LIỆU WIKI TĨNH ĐA TRANG (WIKI GENERATION)

#### UC-10: Sinh Bộ Trang Wiki Chuyên đề và Dashboard
1. **Mã và tên kịch bản:** UC-10 — Sinh Bộ Trang Wiki Chuyên đề và Dashboard.
2. **Mục tiêu nghiệp vụ:** Sử dụng engine khuôn mẫu Jinja2 để kết xuất toàn bộ các trang tổng quan và chuyên đề kỹ thuật dưới dạng HTML tĩnh, không phụ thuộc máy chủ backend.
3. **Actor chính và actor phụ:**  
   - Actor chính: Software Engineer (thông qua điều phối pipeline).  
   - Actor phụ: Không có.
4. **Bối cảnh sử dụng:** Được kích hoạt tại Giai đoạn 4 của đường ống phân tích repository.
5. **Điều kiện trước khi thực hiện:** Kết quả phân tích nội dung và đồ thị tri thức đã sẵn sàng trong bộ nhớ.
6. **Sự kiện kích hoạt:** Hoàn thành bước tạo đồ thị tri thức.
7. **Luồng xử lý chính:**  
   - *Bước 1:* Phân hệ nạp môi trường khuôn mẫu Jinja2 từ thư mục `templates/`.
   - *Bước 2:* Hệ thống duyệt danh sách các chuyên đề nội dung:
     - Kết xuất `wiki/tech.html` từ khuôn mẫu công nghệ (thống kê ngôn ngữ, framework, môi trường).
     - Kết xuất `wiki/architecture.html` từ khuôn mẫu kiến trúc (phân tầng, luồng dữ liệu).
     - Kết xuất `wiki/modules.html` từ khuôn mẫu mô-đun (bảng phân rã 3 cột: Modules → Containers → Packages/Classes).
     - Kết xuất `wiki/tests.html` từ khuôn mẫu kiểm thử (danh mục test runner, test methods).
   - *Bước 3:* Hệ thống trích xuất các chỉ số định lượng tổng thể của dự án (tổng số lớp, tổng số phương thức, danh sách ngôn ngữ, số lượng quan hệ) và kết xuất trang Bảng điều khiển trung tâm `wiki/index.html` theo bố cục Bento Grid hiện đại.
   - *Bước 4:* Tất cả các trang được ghi xuống thư mục đầu ra `wiki/` với định dạng UTF-8.
8. **Các luồng thay thế:** Không có.
9. **Các luồng ngoại lệ:** Lỗi khuôn mẫu Jinja2 cú pháp không hợp lệ hoặc thiếu dữ liệu bắt buộc.
10. **Điều kiện thành công và kết quả sau khi thực hiện:** 5 trang HTML cốt lõi (`index.html`, `tech.html`, `architecture.html`, `modules.html`, `tests.html`) được sinh ra hoàn chỉnh trong thư mục `wiki/`.
11. **Quy tắc nghiệp vụ liên quan:** Mọi trang HTML sinh ra phải tự chứa hoặc liên kết CDN tin cậy, không yêu cầu thiết lập máy chủ web động (Apache/Nginx/NodeJS) để xem.
12. **Những chức năng chưa được xác nhận:** Chưa xác nhận khả năng xuất bộ tài liệu ra định dạng PDF hoặc tệp nén đơn lẻ.
13. **Căn cứ phân tích:**  
    - Code: `backend/src/wiki_generation/renderer.py:20-37` (hàm `render_html_page`), `renderer.py:64-83` (hàm `render_index_page`), `backend/src/cli.py:104-109`.
    - Tài liệu: `docs/designs/html-wiki-storage.md`, `docs/user-stories.md` US-4.1 - US-4.4.

---

#### UC-15: Sinh Trang Hồ sơ Chi tiết Ký hiệu Cú pháp (Render Symbol Pages)
1. **Mã và tên kịch bản:** UC-15 — Sinh Trang Hồ sơ Chi tiết Ký hiệu Cú pháp.
2. **Mục tiêu nghiệp vụ:** Tự động sinh một trang tài liệu HTML độc lập cho mỗi ký hiệu cú pháp có tên định danh đầy đủ (lớp, giao diện, kiểu dữ liệu, phương thức, trường…), hiển thị chữ ký, bổ từ, chú thích, tài liệu và vị trí mã nguồn.
3. **Actor chính và actor phụ:**  
   - Actor chính: Software Engineer (thông qua điều phối pipeline).  
   - Actor phụ: Không có.
4. **Bối cảnh sử dụng:** Được tự động triệu gọi song song trong giai đoạn sinh wiki.
5. **Điều kiện trước khi thực hiện:** Danh sách ký hiệu cú pháp trong `repository_index` có dữ liệu.
6. **Sự kiện kích hoạt:** Hệ thống bước vào bước kết xuất trang ký hiệu trong Giai đoạn 4.
7. **Luồng xử lý chính:**  
   - *Bước 1:* Hệ thống tạo thư mục con `wiki/symbols/` nếu chưa tồn tại.
   - *Bước 2:* Hệ thống duyệt qua từng ký hiệu trong danh sách ký hiệu toàn cục.
   - *Bước 3:* Hệ thống kiểm tra điều kiện: ký hiệu phải có tên định danh đầy đủ (`fully_qualified_name`). Nếu không có, bỏ qua ký hiệu này.
   - *Bước 4:* Hệ thống chuẩn hóa tên tệp an toàn (Safe Filename Sanitization): thay thế các ký tự đặc biệt nguy hiểm cho hệ thống tệp (như `<` và `>`) bằng ký tự gạch dưới `_`, rồi gắn đuôi `.html`.
   - *Bước 5:* Hệ thống truyền đối tượng ký hiệu vào khuôn mẫu `symbol.html` với tiền tố đường dẫn tương đối trỏ ngược về thư mục gốc (`rel_prefix = "../"`).
   - *Bước 6:* Hệ thống ghi tệp HTML ra đường dẫn `wiki/symbols/<safe_filename>.html`.
   - *Bước 7:* Lặp lại cho đến khi toàn bộ ký hiệu hợp lệ đều có trang tài liệu tương ứng.
8. **Các luồng thay thế:**  
   - *Alt 15a — Dự án không có ký hiệu nào:* Bỏ qua bước này một cách an toàn.
9. **Các luồng ngoại lệ:** Lỗi bộ nhớ hoặc lỗi ghi đĩa khi số lượng ký hiệu quá lớn (hàng chục nghìn tệp).
10. **Điều kiện thành công và kết quả sau khi thực hiện:** Hàng trăm đến hàng nghìn tệp HTML chi tiết ký hiệu được tạo thành công trong thư mục `wiki/symbols/`.
11. **Quy tắc nghiệp vụ liên quan:** Tên tệp HTML phải hoàn toàn tương thích với hệ điều hành Windows (không chứa ký tự cấm `< > : " / \ | ? *`).
12. **Những chức năng chưa được xác nhận:** Chưa xác nhận khả năng phân trang (pagination) cho các lớp có hàng trăm phương thức con.
13. **Căn cứ phân tích:**  
    - Code: `backend/src/wiki_generation/renderer.py:38-63` (hàm `render_symbol_pages`).
    - Tài liệu: `docs/designs/html-wiki-storage.md:Section 4`.

---

#### UC-16: Sinh Chỉ mục Tìm kiếm Ngoại tuyến và Ngữ cảnh AI (Generate Search Index & AI Context)
1. **Mã và tên kịch bản:** UC-16 — Sinh Chỉ mục Tìm kiếm Ngoại tuyến và Ngữ cảnh AI.
2. **Mục tiêu nghiệp vụ:** Xuất bản hai tệp dữ liệu JSON đặc biệt (`search_index.json` và `wiki_context.json`) phục vụ cơ chế tìm kiếm thời gian thực phía máy khách và làm kho ngữ cảnh tri thức cho tiện ích Trợ lý AI nhúng.
3. **Actor chính và actor phụ:**  
   - Actor chính: Software Engineer (thông qua điều phối pipeline).  
   - Actor phụ: Không có.
4. **Bối cảnh sử dụng:** Được tự động triệu gọi ở phần cuối của Giai đoạn 4 để cung cấp năng lực tương tác thông minh cho giao diện web.
5. **Điều kiện trước khi thực hiện:** Bảng chỉ mục ký hiệu và kết quả phân tích nội dung đã hoàn tất.
6. **Sự kiện kích hoạt:** Hoàn thành kết xuất các trang chuyên đề HTML.
7. **Luồng xử lý chính:**  
   - *Bước 1 (Sinh Search Index):* Hệ thống khởi tạo danh mục tìm kiếm gồm 5 trang chính (Dashboard, Tech, Architecture, Modules, Tests).
   - *Bước 2:* Hệ thống duyệt từng ký hiệu trong `repository_index`, trích xuất tên định danh (`fully_qualified_name`) và đường dẫn URL tương ứng (`symbols/<safe_filename>.html`), bổ sung vào danh mục tìm kiếm.
   - *Bước 3:* Hệ thống tuần tự hóa danh mục ra tệp `wiki/search_index.json`.
   - *Bước 4 (Sinh AI Context):* Hệ thống xây dựng cấu trúc ngữ cảnh chuyên sâu: gồm danh sách chi tiết các ký hiệu kèm chữ ký phương thức đã định dạng (`signature`), ghi chú tài liệu (`docstring`), danh sách chú thích (`annotations`), đường dẫn tệp nguồn (`file_path`), nội dung các phần chuyên đề (`sections`) và danh sách tóm tắt phân cấp (`summaries`).
   - *Bước 5:* Hệ thống ghi cấu trúc ngữ cảnh giàu tri thức ra tệp `wiki/wiki_context.json`.
8. **Các luồng thay thế:** Không có.
9. **Các luồng ngoại lệ:** Lỗi tuần tự hóa JSON do ký tự không tương thích Unicode UTF-8 (được bảo vệ bằng `ensure_ascii=False`).
10. **Điều kiện thành công và kết quả sau khi thực hiện:** Tệp `wiki/search_index.json` và `wiki/wiki_context.json` hiện diện đầy đủ trong thư mục `wiki/`.
11. **Quy tắc nghiệp vụ liên quan:** Dung lượng của `search_index.json` phải được tối ưu để trình duyệt có thể tải nhanh chóng qua kết nối cục bộ.
12. **Những chức năng chưa được xác nhận:** Chưa xác nhận cơ chế nén chỉ mục (Gzip/Brotli) tự động khi dự án có quy mô trên 50.000 ký hiệu.
13. **Căn cứ phân tích:**  
    - Code: `backend/src/wiki_generation/renderer.py:84-106` (hàm `generate_search_index`), `renderer.py:122-182` (hàm `generate_ai_context`).
    - Tài liệu: `docs/user-stories.md` US-4.5, US-4.6.

---

### GÓI 5: ĐIỀU PHỐI DÒNG LỆNH VÀ KHỞI CHẠY (CLI ORCHESTRATION)

#### UC-18: Thực thi Toàn bộ Đường ống Phân tích Tự động (Run Full Analysis Pipeline)
1. **Mã và tên kịch bản:** UC-18 — Thực thi Toàn bộ Đường ống Phân tích Tự động.
2. **Mục tiêu nghiệp vụ:** Cho phép kỹ sư phần mềm khởi chạy toàn bộ quy trình từ quét mã nguồn, phân tích cú pháp, tóm tắt AI, xây dựng đồ thị tri thức, sinh tài liệu wiki và tự động mở trình duyệt chỉ bằng một lệnh duy nhất.
3. **Actor chính và actor phụ:**  
   - Actor chính: Software Engineer (A1).  
   - Actor phụ: Git Remote Server (EX1 - nếu là URL), Ollama LLM Server (EX2 - nếu bật AI), Web Browser & Host OS (EX3).
4. **Bối cảnh sử dụng:** Trường hợp sử dụng chính và phổ biến nhất của hệ thống RepoAtlas.
5. **Điều kiện trước khi thực hiện:** Máy tính đã cài đặt Python 3.10+ cùng các thư viện phụ thuộc của dự án.
6. **Sự kiện kích hoạt:** Kỹ sư phần mềm gõ lệnh `repoatlas analyze <path|url> [--no-llm]`.
7. **Luồng xử lý chính:**  
   - *Bước 1:* Phân hệ CLI tiếp nhận tham số dòng lệnh và phân tích cờ tùy chọn.
   - *Bước 2:* Gọi UC-01 (UC-02 mở rộng khi là Git URL) để xác định loại địa chỉ và kích hoạt phân tích cú pháp AST, lưu kết quả vào `indexes/`.
   - *Bước 3 (Thực hiện UC-05 hoặc UC-06):* Kích hoạt phân tích phân cấp và tóm tắt theo chế độ AI tương ứng, lưu kết quả vào `analysis/`.
   - *Bước 4 (Thực hiện UC-08):* Hợp nhất dữ liệu và xây dựng đồ thị tri thức, lưu kết quả vào `graphs/`.
   - *Bước 5 (Thực hiện UC-10, UC-15, UC-16):* Biên dịch toàn bộ các trang HTML, trang ký hiệu, chỉ mục tìm kiếm và ngữ cảnh AI vào thư mục `wiki/`.
   - *Bước 6:* Hệ thống in thông báo phân tích hoàn tất thành công lên màn hình dòng lệnh.
   - *Bước 7:* Hệ thống kiểm tra môi trường hệ điều hành máy trạm:
     - Nếu là hệ điều hành Windows (`os.name == 'nt'`), hệ thống sử dụng lệnh hệ thống `os.startfile(wiki/index.html)`.
     - Nếu là hệ điều hành Linux hoặc macOS, hệ thống gọi thư viện `webbrowser.open()`.
   - *Bước 8:* Trình duyệt web mặc định của người dùng tự động bật lên và hiển thị trang Bảng điều khiển `wiki/index.html`.
   - *Bước 9:* Hệ thống kích hoạt khối dọn dẹp bắt buộc (`finally`) để thu hồi tài nguyên tạm thời nếu có tải từ Git.
8. **Các luồng thay thế:**  
   - *Alt 8a — Trình duyệt không thể tự động mở (môi trường server không có GUI):* Hệ thống bắt ngoại lệ, in thông báo hướng dẫn người dùng tự mở tệp theo đường dẫn tuyệt đối hiển thị trên terminal.
9. **Các luồng ngoại lệ:**  
   - *Exc 9a — Lỗi nghiêm trọng tại bất kỳ giai đoạn nào (quét lỗi, thiếu file, lỗi cú pháp graph):* Pipeline dừng ngay lập tức, khối `finally` vẫn kích hoạt dọn dẹp thư mục tạm và thông báo lỗi ra màn hình.
10. **Điều kiện thành công và kết quả sau khi thực hiện:** Bộ tài liệu wiki hoàn chỉnh sẵn sàng phục vụ và hiển thị ngay trước mắt người dùng trên trình duyệt.
11. **Quy tắc nghiệp vụ liên quan:** Khối dọn dẹp (`cleanup`) bắt buộc phải luôn luôn chạy bất kể pipeline thành công hay xảy ra ngoại lệ.
12. **Những chức năng chưa được xác nhận:** Chưa xác nhận tùy chọn chạy dưới dạng máy chủ dịch vụ nền (daemon service) với lệnh `repoatlas serve`.
13. **Căn cứ phân tích:**  
    - Code: `backend/src/cli.py:43-145` (hàm `run_analysis_pipeline`), `cli.py:152-179` (hàm `main`).
    - Tài liệu: `docs/architecture.md:Section 6`, `docs/user-stories.md` US-5.1, US-5.2.

---

### GÓI 6: TRA CỨU, KHÁM PHÁ VÀ TƯƠNG TÁC NGOẠI TUYẾN (WIKI INTERACTION)

#### UC-20: Điều hướng và Khám phá Cây Tài liệu trên Wiki (Explore Wiki via Sidebar & Links)
1. **Mã và tên kịch bản:** UC-20 — Điều hướng và Khám phá Cây Tài liệu trên Wiki.
2. **Mục tiêu nghiệp vụ:** Cho phép người đọc tài liệu dễ dàng duyệt qua các chuyên đề kiến trúc, xem các chỉ số dự án và truy cập chi tiết các thành phần thông qua thanh bên điều hướng và liên kết nội bộ.
3. **Actor chính và actor phụ:**  
   - Actor chính: Wiki User (A2).  
   - Actor phụ: Web Browser (EX3).
4. **Bối cảnh sử dụng:** Người đọc mở bộ tài liệu wiki trong trình duyệt để nghiên cứu dự án.
5. **Điều kiện trước khi thực hiện:** Bộ tài liệu `wiki/` đã được sinh và tệp `index.html` đang mở trong trình duyệt.
6. **Sự kiện kích hoạt:** Người đọc nhấp chuột vào các mục trên thanh bên (sidebar) hoặc các liên kết thẻ thành phần (card links).
7. **Luồng xử lý chính:**  
   - *Bước 1:* Người đọc quan sát thanh bên điều hướng cố định phía bên trái giao diện.
   - *Bước 2:* Người đọc nhấp chuột vào một mục chuyên đề bất kỳ (ví dụ: "Architecture", "Modules", "Tech Stack" hoặc "Tests").
   - *Bước 3:* Trình duyệt tải trang HTML tương ứng ngay lập tức từ ổ đĩa cục bộ mà không có độ trễ mạng.
   - *Bước 4:* Mã JavaScript trên trang tự động phân tích đường dẫn URL hiện tại, làm nổi bật (highlight active state) mục tương ứng trên thanh bên điều hướng.
   - *Bước 5:* Trong các trang nội dung, người đọc nhấp vào các liên kết ký hiệu mã nguồn để chuyển hướng trực tiếp sang trang chi tiết của ký hiệu đó trong thư mục `symbols/`.
8. **Các luồng thay thế:** Không có.
9. **Các luồng ngoại lệ:** Trang liên kết không tồn tại nếu người dùng tự ý chỉnh sửa URL trên thanh địa chỉ trình duyệt.
10. **Điều kiện thành công và kết quả sau khi thực hiện:** Người đọc xem được nội dung kỹ thuật mong muốn với giao diện phản hồi mượt mà.
11. **Quy tắc nghiệp vụ liên quan:** Không xuất hiện hiện tượng chớp nháy phông chữ hoặc vỡ bố cục khi chuyển đổi giữa các tab (nhờ cơ chế CSS font-fallback và liên kết cục bộ).
12. **Những chức năng chưa được xác nhận:** Chưa xác nhận khả năng ghi nhớ vị trí cuộn trang (scroll position restoration) khi nhấn nút Back trên trình duyệt.
13. **Căn cứ phân tích:**  
    - Code: `backend/src/wiki_generation/templates/base.html:292-304` (logic Highlight Active Sidebar Item).
    - Tài liệu: `docs/designs/html-wiki-storage.md`, `docs/user-stories.md` US-4.1.

---

#### UC-21: Tìm kiếm Ký hiệu Trực tiếp Ngoại tuyến (Client-side Live Search)
1. **Mã và tên kịch bản:** UC-21 — Tìm kiếm Ký hiệu Trực tiếp Ngoại tuyến.
2. **Mục tiêu nghiệp vụ:** Cung cấp thanh tìm kiếm nhanh ngay trên giao diện web, lọc và hiển thị tức thời danh sách các lớp, phương thức hoặc trang chuyên đề khớp với từ khóa mà không cần gửi yêu cầu về máy chủ backend.
3. **Actor chính và actor phụ:**  
   - Actor chính: Wiki User (A2).  
   - Actor phụ: Web Browser (EX3).
4. **Bối cảnh sử dụng:** Người đọc cần tìm nhanh vị trí của một lớp hoặc hàm nghiệp vụ cụ thể (ví dụ: `PaymentProcessor` hay `authenticate`) khi đang duyệt wiki.
5. **Điều kiện trước khi thực hiện:** Trang wiki đã tải xong và đã nạp thành công tệp `search_index.json` vào bộ nhớ RAM của trình duyệt.
6. **Sự kiện kích hoạt:** Người đọc nhấp chuột vào ô tìm kiếm ở thanh đầu trang (header) và bắt đầu gõ ký tự.
7. **Luồng xử lý chính:**  
   - *Bước 1:* Người đọc gõ một hoặc nhiều ký tự vào ô tìm kiếm.
   - *Bước 2:* Sự kiện `input` được kích hoạt; mã JavaScript lấy chuỗi tìm kiếm, chuyển thành chữ thường và cắt bỏ khoảng trắng thừa.
   - *Bước 3:* Nếu ô tìm kiếm rỗng, danh sách kết quả tự động ẩn đi.
   - *Bước 4:* Nếu có từ khóa, thuật toán tìm kiếm duyệt qua mảng `searchIndex` trong bộ nhớ, lọc ra tối đa 15 mục có tên chứa chuỗi từ khóa tìm kiếm.
   - *Bước 5:* Hệ thống hiển thị hộp danh sách kết quả dạng thả xuống (dropdown) ngay dưới ô tìm kiếm.
   - *Bước 6:* Người đọc nhấp chuột vào một kết quả mong muốn trong danh sách.
   - *Bước 7:* Trình duyệt chuyển hướng ngay sang trang chi tiết của ký hiệu hoặc trang chuyên đề tương ứng.
8. **Các luồng thay thế:**  
   - *Alt 21a — Không tìm thấy kết quả phù hợp:* Hộp danh sách hiển thị thông báo "No results found".
   - *Alt 21b — Người đọc nhấp chuột ra ngoài ô tìm kiếm:* Hộp danh sách tự động ẩn đi để không che khuất nội dung trang.
9. **Các luồng ngoại lệ:**  
   - *Exc 21a — `search_index.json` không nạp được:* trình duyệt ghi lỗi vào Console, tìm kiếm tạm thời không khả dụng. **Lưu ý kỹ thuật (cần kiểm tra khi chạy thật):** khi mở wiki bằng giao thức `file://`, nhiều trình duyệt hiện đại (đặc biệt Chrome) chặn `fetch` tệp cục bộ.
10. **Điều kiện thành công và kết quả sau khi thực hiện:** Người đọc định vị và mở được trang tài liệu của ký hiệu mong muốn chỉ trong vài mili-giây.
11. **Quy tắc nghiệp vụ liên quan:** Tìm kiếm không phân biệt chữ hoa/thường; giới hạn tối đa 15 kết quả hàng đầu.
12. **Những chức năng chưa được xác nhận:** Chưa xác nhận thuật toán tìm kiếm mờ nâng cao (Fuzzy search theo khoảng cách Levenshtein) trong tệp kịch bản hiện tại.
13. **Căn cứ phân tích:**  
    - Code: `backend/src/wiki_generation/templates/base.html:240-244` (nạp `search_index.json`), `base.html:251-290` (logic Live Search).
    - Tài liệu: `docs/user-stories.md` US-4.5.

---

#### UC-22: Tương tác Hỏi đáp Codebase với Trợ lý AI Cục bộ Nhúng (Ask Local AI Widget)
1. **Mã và tên kịch bản:** UC-22 — Tương tác Hỏi đáp Codebase với Trợ lý AI Cục bộ Nhúng.
2. **Mục tiêu nghiệp vụ:** Cung cấp tiện ích hội thoại thông minh nhúng trực tiếp trên từng trang wiki, cho phép người đọc hỏi về kiến trúc, luồng xử lý hoặc vị trí thành phần bằng ngôn ngữ tự nhiên; trợ lý sẽ tự động trích xuất ngữ cảnh liên quan và truyền luồng câu trả lời thời gian thực từ Ollama hoặc cung cấp câu trả lời từ tri thức nội bộ nếu Ollama ngoại tuyến.
3. **Actor chính và actor phụ:**  
   - Actor chính: Wiki User (A2).  
   - Actor phụ: Ollama LLM Server (EX2), Web Browser (EX3).
4. **Bối cảnh sử dụng:** Người đọc cần một trợ lý giải thích nghiệp vụ tổng thể hoặc chỉ dẫn cụ thể về chức năng của codebase mà không muốn tự đọc lướt qua hàng trăm trang tài liệu.
5. **Điều kiện trước khi thực hiện:**  
   - Người đọc đang mở một trang wiki bất kỳ.
   - Tệp `wiki_context.json` đã được nạp thành công vào trình duyệt.
6. **Sự kiện kích hoạt:** Người đọc nhấp vào nút nổi (Floating Action Button) có biểu tượng Trợ lý AI ở góc dưới bên phải màn hình.
7. **Luồng xử lý chính:**  
   - *Bước 1:* Bảng hội thoại trò chuyện (chat panel) hiển thị lên màn hình.
   - *Bước 2:* Mã JavaScript chạy tiến trình thăm dò sức khỏe dịch vụ Ollama tại cổng cục bộ (`http://localhost:11434/api/tags`):
     - Nếu phát hiện Ollama trực tuyến và có mô hình phù hợp, chấm trạng thái hiển thị màu xanh lá cây ("Ollama online · qwen2.5-coder:3b").
     - Nếu không kết nối được, chấm trạng thái hiển thị màu đỏ ("Ollama offline · dùng tìm kiếm nội bộ").
   - *Bước 3:* Người đọc nhập câu hỏi tự nhiên vào ô hội thoại (ví dụ: *"Hàm xử lý thanh toán nằm ở lớp nào?"*) và bấm nút Gửi (hoặc nhấn phím Enter).
   - *Bước 4:* Câu hỏi của người dùng được hiển thị trên khung chat và một bong bóng thông báo "Đang suy nghĩ..." xuất hiện.
   - *Bước 5:* Hệ thống phân tích ý định (Intent Detection) và tách từ khóa từ câu hỏi của người dùng (loại bỏ các từ dừng thông thường).
   - *Bước 6:* Thuật toán tính điểm liên quan (Scoring Algorithm) rà soát toàn bộ các ký hiệu và các phần chuyên đề trong `wiki_context.json`, xếp hạng và chọn lọc ra các ký hiệu cùng đoạn văn bản wiki có điểm số cao nhất.
   - *Bước 7:* Hệ thống đóng gói câu lệnh nhắc kèm ngữ cảnh được trích xuất và gửi yêu cầu dạng luồng (`stream: true`) đến cổng API Ollama.
   - *Bước 8:* Ollama tiếp nhận và bắt đầu truyền từng đoạn mã token văn bản trả lời về trình duyệt; khung chat hiển thị văn bản theo hiệu ứng máy đánh chữ thời gian thực.
   - *Bước 9:* Khi luồng suy luận kết thúc, câu trả lời hoàn chỉnh hiển thị kèm theo các liên kết điều hướng có thể nhấp vào để mở ngay trang chi tiết ký hiệu tương ứng.
8. **Các luồng thay thế:**  
   - *Alt 22a — Dịch vụ Ollama ngoại tuyến (CORS hoặc server tắt):* Yêu cầu gửi đến Ollama thất bại; hệ thống tự động kích hoạt cơ chế chuyển tiếp dự phòng thông minh (Intelligent Fallback):
     - Nếu câu hỏi hỏi về số lượng/thống kê: Hệ thống hiển thị tổng số ký hiệu, số lượng lớp, số phương thức và danh sách 30 ký hiệu tiêu biểu kèm liên kết.
     - Nếu tìm thấy ký hiệu liên quan theo từ khóa: Hệ thống hiển thị danh thiếp tóm tắt của các ký hiệu khớp (tên, chữ ký, đường dẫn tệp, docstring) kèm liên kết mở trang chi tiết.
     - Nếu không có ký hiệu khớp: Hệ thống hiển thị tóm tắt tổng quan codebase từ tầng Phân hệ/Đơn vị triển khai kèm hướng dẫn cách khởi động Ollama qua lệnh PowerShell.
   - *Alt 22b — Ollama trực tuyến nhưng thiếu model `qwen2.5-coder:3b`:* hiển thị chấm đỏ, xử lý như Alt 22a (dùng tri thức nội bộ).
   - *Alt 22c — Kiểm tra sức khỏe định kỳ mỗi 30 giây:* chấm trạng thái tự cập nhật khi Ollama bật/tắt. (Ghi nhận từ SD-05; chưa xác nhận trong mô tả mã ở UC.)
9. **Các luồng ngoại lệ:** Lỗi trình duyệt chặn truy vấn Cross-Origin (CORS) khi gọi đến cổng 11434 (được hướng dẫn xử lý bằng cách cấu hình biến môi trường `OLLAMA_ORIGINS="*" ; ollama serve`).
10. **Điều kiện thành công và kết quả sau khi thực hiện:** Người đọc nhận được câu trả lời chính xác, giải đáp thắc mắc về codebase kèm theo siêu liên kết dẫn chứng cụ thể.
11. **Quy tắc nghiệp vụ liên quan:**  
    - Trợ lý AI cam kết không bịa đặt (hallucination): chỉ trả lời dựa trên thông tin chỉ mục thực tế có trong `wiki_context.json`.
    - Trải nghiệm người dùng luôn được bảo đảm: nếu không có AI, hệ thống vẫn hoạt động như một công cụ tìm kiếm ngữ nghĩa nội bộ cực kỳ hiệu quả.
12. **Những chức năng chưa được xác nhận:** Chưa xác nhận tính năng lưu lại lịch sử các phiên chat trước đó vào LocalStorage của trình duyệt khi người dùng đóng trang web.
13. **Căn cứ phân tích:**  
    - Code: `backend/src/wiki_generation/templates/base.html:305-604` (toàn bộ logic Widget Ask Local AI, kiểm tra kết nối Ollama, xếp hạng ngữ cảnh, cơ chế streaming và fallback thông minh).
    - Tài liệu: `docs/user-stories.md` US-4.6, `README.md:Line 14`.

---

## III. MA TRẬN QUAN HỆ GIỮA CÁC USE CASE

### 1. Quan hệ Bao gồm (`<<include>>`)
| Use Case Cơ sở | Quan hệ | Use Case Được bao gồm | Giải thích nghiệp vụ |
|---|:---:|---|---|
| **UC-18** | `<<include>>` | **UC-01** | Mọi lần chạy pipeline đều phải quét và lập chỉ mục mã nguồn trước tiên. |
| **UC-18** | `<<include>>` | **UC-05** | Mọi lần chạy đều phải tạo tóm tắt (UC-06 là phần mở rộng của UC-05, xem bên dưới). |
| **UC-18** | `<<include>>` | **UC-08** | Mọi lần chạy đều phải hợp nhất thành Đồ thị Tri thức. |
| **UC-18** | `<<include>>` | **UC-10, UC-15, UC-16** | Mọi lần chạy đều phải sinh các trang HTML, trang ký hiệu và chỉ mục. |
| **UC-01** | `<<include>>` | **UC-03, UC-04** | Quét thư mục luôn gọi parser AST cho từng tệp `.java` / `.cs`. |

### 2. Quan hệ Mở rộng (`<<extend>>`)
| Use Case Mở rộng | Quan hệ | Use Case Cơ sở | Điều kiện kích hoạt (extension point) |
|---|:---:|---|---|
| **UC-06** (Tóm tắt cấu trúc) | `<<extend>>` | **UC-05** (Tóm tắt AI) | Cờ `--no-llm` được bật, hoặc kiểm tra sức khỏe Ollama thất bại. |
| **UC-02** (Phân tích từ Git URL) | `<<extend>>` | **UC-01** (Phân tích cục bộ) | Đầu vào được nhận diện là Git URL / shorthand `owner/repo`. |

> **Lưu ý:** không vẽ quan hệ nào giữa UC-21 và UC-22. UC-21 dùng `search_index.json`, UC-22 dùng `wiki_context.json`, hai UC độc lập. UC-16 chỉ là tiền điều kiện (cung cấp dữ liệu) cho UC-21 và UC-22, không vẽ mũi tên.

### 3. Bảng nối Actor – Use Case
| Actor | Loại | Nối với UC |
|---|:---:|---|
| Software Engineer | Chính | UC-18, UC-01, UC-02 |
| Wiki User | Chính | UC-20, UC-21, UC-22 |
| Git Remote Server | Phụ | UC-02 |
| Ollama LLM Server | Phụ | UC-05, UC-22 |
| Web Browser & Host OS | Phụ | UC-18, UC-20, UC-21, UC-22 |

UC-03, 04, 06, 08, 10, 15, 16 là UC nội bộ do pipeline gọi: **không nối actor**, chỉ nối bằng include/extend.

---

## IV. BẢNG TỔNG KẾT VÀ TRẠNG THÁI XÁC MINH CÁC USE CASE

| Mã Use Case | Tên Use Case | Phân hệ nghiệp vụ | Tác nhân chính | Trạng thái xác minh trong Codebase |
|---|---|---|---|:---:|
| **UC-01** | Phân tích Repository Cục bộ | Core Indexing | Software Engineer | **Đã xác nhận** (`scanner.py`, `ir_generator.py`) |
| **UC-02** | Phân tích Repository từ Git URL | Core Indexing | Software Engineer, Git Server | **Đã xác nhận** (`scanner.py:89-118`) |
| **UC-03** | Phân tích Cú pháp Java | Core Indexing | Software Engineer | **Đã xác nhận** (`java_parser.py`) |
| **UC-04** | Phân tích Cú pháp C# | Core Indexing | Software Engineer | **Đã xác nhận** (`csharp_parser.py`) |
| **UC-05** | Tóm tắt Phân cấp bằng AI (Ollama) | AI Analysis | Software Engineer, Ollama Server | **Đã xác nhận** (`summarizer.py`, `ollama.py`) |
| **UC-06** | Tóm tắt Cấu trúc Dự phòng (No-LLM) | AI Analysis | Software Engineer | **Đã xác nhận** (`null.py`, `content_generator.py`) |
| **UC-08** | Xây dựng và Thẩm định Knowledge Graph | Knowledge Graph | Software Engineer | **Đã xác nhận** (`builder.py`, `models.py`) |
| **UC-10** | Sinh Bộ Trang Wiki Chuyên đề & Dashboard | Wiki Generation | Software Engineer | **Đã xác nhận** (`renderer.py:20-83`) |
| **UC-15** | Sinh Trang Hồ sơ Ký hiệu Cú pháp | Wiki Generation | Software Engineer | **Đã xác nhận** (`renderer.py:38-63`) |
| **UC-16** | Sinh Chỉ mục Tìm kiếm & Ngữ cảnh AI | Wiki Generation | Software Engineer | **Đã xác nhận** (`renderer.py:84-182`) |
| **UC-18** | Thực thi Toàn bộ Pipeline Phân tích | CLI Orchestration | Software Engineer, All External | **Đã xác nhận** (`cli.py:43-145`) |
| **UC-20** | Điều hướng Khám phá Cây Tài liệu | Wiki Interaction | Wiki User | **Đã xác nhận** (`base.html:292-304`) |
| **UC-21** | Tìm kiếm Ký hiệu Ngoại tuyến | Wiki Interaction | Wiki User | **Đã xác nhận** (`base.html:251-290`) |
| **UC-22** | Hỏi đáp với Trợ lý AI Cục bộ | Wiki Interaction | Wiki User, Ollama Server | **Đã xác nhận** (`base.html:305-604`) |
