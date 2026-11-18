# 02 — KỊCH BẢN BIỂU ĐỒ HOẠT ĐỘNG (ACTIVITY DIAGRAM SCENARIOS)

> **Tài liệu:** Kịch bản Quy trình Hoạt động Chi tiết (Activity Scenarios Specification)  
> **Chuyên môn:** Phân tích và Thiết kế Hướng đối tượng (OOAD) & Kiến trúc Phần mềm  
> **Dự án đối chiếu:** RepoAtlas (Automated AST-Grounded Repository Documentation Generator)  
> **Mục tiêu:** Mô tả chi tiết hành vi động, luồng điều khiển, rẽ nhánh điều kiện, xử lý song song (fork/join), vòng lặp và xử lý ngoại lệ cho các quy trình nghiệp vụ trọng tâm, làm căn cứ đầu vào để vẽ Activity Diagram hoàn chỉnh.

---

## 1. QUY TRÌNH 1 (AD-01): TOÀN BỘ ĐƯỜNG ỐNG PHÂN TÍCH VÀ KHỞI CHẠY WIKI TỰ ĐỘNG

### 1.1. Tên quy trình và mục tiêu
- **Tên quy trình:** Thực thi Toàn bộ Đường ống Phân tích Repository và Khởi chạy Bộ Tài liệu Wiki (`repoatlas analyze`).
- **Mục tiêu nghiệp vụ:** Điều phối tự động chuỗi 4 phân hệ chức năng từ tiếp nhận đầu vào đến khi website tài liệu HTML tĩnh được khởi chạy trên trình duyệt người dùng.

### 1.2. Phân chia Swimlane (Bộ phận tham gia)
Quy trình được phân tách rõ ràng trên **6 Swimlanes**:
1. `Software Engineer`: Người dùng nhập lệnh và tiếp nhận giao diện tài liệu.
2. `CLI Orchestrator`: Bộ điều phối trung tâm nhận tham số và kiểm soát luồng thực thi.
3. `Core Indexing Engine`: Phân hệ quét thư mục và phân tích AST.
4. `AI Analysis Engine`: Phân hệ phân cấp và tóm tắt thông minh.
5. `Knowledge Graph Builder`: Phân hệ hợp nhất và thẩm định đồ thị.
6. `Wiki Generator & Browser`: Phân hệ kết xuất HTML và trình duyệt máy trạm.

### 1.3. Điều kiện bắt đầu
Máy tính đã cài đặt môi trường thực thi của hệ thống và các tệp mã nguồn đầu vào sẵn sàng.

### 1.4. Hành động đầu tiên
Kỹ sư phần mềm nhập câu lệnh `repoatlas analyze <path|url> [--no-llm]` tại cửa sổ dòng lệnh (terminal).

### 1.5. Trình tự hành động chi tiết theo luồng điều khiển
1. **[Software Engineer]** Nhập lệnh và tham số thực thi.
2. **[CLI Orchestrator]** Phân tích cú pháp đối số (`target_path`, `use_llm = not args.no_llm`).
3. **[CLI Orchestrator]** **Điểm quyết định 1 (Decision Point):** Tham số `target_path` có phải là Git URL hoặc GitHub shorthand không?
   - *Nhánh Đúng (Git Remote):* Chuyển quyền sang Quy trình 2 (AD-02) để cấp phát thư mục tạm và clone mã nguồn từ xa về máy cục bộ.
   - *Nhánh Sai (Local Path):* Kiểm tra đường dẫn trên hệ thống tệp đĩa:
     - **Điểm quyết định 2:** Thư mục cục bộ có tồn tại và hợp lệ không?
       - *Không tồn tại:* In thông báo lỗi `ERROR: Khong tim thay duong dan`, dừng tiến trình với mã lỗi `sys.exit(1)`. **(Điểm kết thúc thất bại 1)**.
       - *Tồn tại:* Ghi nhận đường dẫn tuyệt đối của thư mục mục tiêu.
4. **[CLI Orchestrator]** In thông báo bắt đầu phân tích và hiển thị trạng thái chế độ AI (`AI MODE: ON/OFF`).
5. **[Core Indexing Engine]** Khởi tạo bộ quét `RepositoryScanner` với thư mục đầu ra `indexes/`.
6. **[Core Indexing Engine]** Thực thi quy trình phân tích cú pháp (xem chi tiết tại AD-03):
   - Đọc và áp dụng quy tắc `.gitignore`.
   - Quét cấu trúc cây thư mục và lưu ra `indexes/structure.json`.
   - Phân tích AST từng tệp `.java` và `.cs`, trích xuất toàn bộ ký hiệu và quan hệ.
   - Tổng hợp `RepositoryIndex` và ghi ra `indexes/repository_index.json`, `indexes/structure_overview.json`.
7. **[AI Analysis Engine]** Nạp bảng chỉ mục `repository_index.json` và tổng quan cấu trúc từ thư mục `indexes/`.
8. **[AI Analysis Engine]** Xây dựng cây phân cấp mã nguồn 6 tầng (`TaxonomyTree`).
9. **[AI Analysis Engine]** **Điểm quyết định 3:** Tham số `use_llm` có bằng `True` không?
   - *Nhánh Đúng (Bật AI):* Kiểm tra kết nối mạng (health check) đến máy chủ Ollama tại cổng `11434`.
     - **Điểm quyết định 4:** Dịch vụ Ollama và mô hình `qwen2.5-coder:3b` có khả dụng không?
       - *Khả dụng:* Khởi tạo `OllamaClient`, tiến hành tóm tắt phân cấp Bottom-Up có quản trị ngân sách token (xem AD-04).
       - *Không khả dụng:* Ghi cảnh báo ngoại tuyến vào log, tự động chuyển đổi dự phòng sang `NullLLMClient` để tóm tắt cấu trúc thuần túy (AD-09).
   - *Nhánh Sai (Tắt AI):* Khởi tạo `NullLLMClient`, thực hiện tóm tắt cấu trúc xác định.
10. **[AI Analysis Engine]** Sinh nội dung 4 chuyên đề kiến trúc (`tech`, `tests`, `architecture`, `modules`) và lưu kết quả ra `analysis/summaries.json`.
11. **[Knowledge Graph Builder]** Nạp dữ liệu đồng thời từ `indexes/` và `analysis/`.
12. **[Knowledge Graph Builder]** Thực thi xây dựng đồ thị tri thức (xem AD-05):
    - Khởi tạo nút repository, tệp, ký hiệu, phân cấp.
    - Thêm các cạnh quan hệ và tự động bù đắp nút `external` cho thư viện bên ngoài.
    - **Điểm quyết định 5:** Thẩm định tính toàn vẹn (Integrity Validation) có hợp lệ không?
      - *Không hợp lệ:* Ném ngoại lệ `ValueError`, dừng pipeline → đi qua hành động Cleanup (AD-10) rồi mới tới **Điểm kết thúc thất bại 2**.
      - *Hợp lệ:* Thực hiện ghi đĩa nguyên tử thông qua tệp hoán đổi tạm ra `graphs/graph.json`.
13. **[Wiki Generator & Browser]** Nhận dữ liệu phân tích và kết xuất bộ giao diện HTML (xem AD-06):
    - Render 4 trang chuyên đề HTML từ template Jinja2.
    - Render toàn bộ các trang chi tiết ký hiệu trong thư mục con `wiki/symbols/`.
    - Render trang Bảng điều khiển trung tâm `wiki/index.html`.
    - Sinh chỉ mục tìm kiếm `wiki/search_index.json` và tệp ngữ cảnh `wiki/wiki_context.json`.
14. **[CLI Orchestrator]** In thông báo thành công: `SUCCESS: Phan tich hoan tat! Mo thu muc /wiki de xem tai lieu.`
15. **[CLI Orchestrator]** **Điểm quyết định 6:** Hệ điều hành máy trạm là Windows (`os.name == 'nt'`)?
    - *Nhánh Đúng (Windows):* Gọi API hệ thống `os.startfile(wiki_index_path)`.
    - *Nhánh Sai (Linux/macOS):* Gọi hàm `webbrowser.open(wiki_index_path.as_uri())`.
16. **[Wiki Generator & Browser]** Trình duyệt web mặc định khởi động và tải trang `wiki/index.html`.
17. **[CLI Orchestrator]** Thực thi khối kết thúc bắt buộc `finally`: Nếu repository được tải từ Git từ xa, gọi hàm `scanner.cleanup()` để xóa sạch thư mục làm việc tạm thời trên đĩa.
18. **[Software Engineer]** Quan sát giao diện wiki trực quan trên trình duyệt. **(Điểm kết thúc thành công)**.

### 1.5b. Ghi chú vẽ
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

### 1.6. Quy tắc nghiệp vụ chi phối
- Toàn bộ chuỗi xử lý là đường ống một chiều (pipeline), giai đoạn sau phụ thuộc hoàn toàn vào dữ liệu đầu ra của giai đoạn trước.
- Khối dọn dẹp tài nguyên tạm thời (`cleanup`) bắt buộc phải luôn luôn được thực thi trong khối `finally`, kể cả khi pipeline gặp sự cố gián đoạn bất ngờ.

### 1.7. Căn cứ phân tích
- Code: `backend/src/cli.py:43-145` (hàm `run_analysis_pipeline`), `cli.py:152-179`.
- Tài liệu: `docs/architecture.md:Section 6`, `docs/user-stories.md` US-5.1.

---

## 2. QUY TRÌNH 2 (AD-02): NHẬN DIỆN VÀ TẢI REPOSITORY TỪ GIT TỪ XA

### 2.1. Tên quy trình và mục tiêu
- **Tên quy trình:** Phân giải Địa chỉ và Tải Bản sao Tinh gọn từ Kho Git Từ xa.
- **Mục tiêu nghiệp vụ:** Nhận diện các định dạng URL khác nhau, cấp phát thư mục tạm thời an toàn, tải mã nguồn commit mới nhất và xử lý lỗi mạng.

### 2.2. Phân chia Swimlane
1. `CLI Scanner`: Tiếp nhận yêu cầu, phân tích định dạng chuỗi và ra lệnh clone.
2. `Git Remote Server`: Máy chủ từ xa xử lý yêu cầu tải dữ liệu.
3. `Host File System`: Hệ thống tệp đĩa máy trạm cấp phát và xóa thư mục tạm.

### 2.3. Trình tự hành động chi tiết
1. **[CLI Scanner]** Tiếp nhận chuỗi `target` từ tham số dòng lệnh.
2. **[CLI Scanner]** **Điểm quyết định 1 (Phân loại mẫu chuỗi URL):**
   - *Mẫu URL đầy đủ:* Khớp mẫu `https?://.*\.git` hoặc `git@.*:.*\.git` -> Giữ nguyên URL.
   - *Mẫu GitHub Web:* Khớp mẫu `https?://github\.com/.*` -> Tự động thêm đuôi `.git` nếu chưa có.
   - *Mẫu Shorthand:* Khớp mẫu `owner/repo` và không tồn tại thư mục tương ứng trên máy cục bộ -> Ghép tiền tố: `https://github.com/owner/repo.git`.
   > **Lưu ý:** Quyết định 1 chỉ chạy khi AD-01 đã xác định đầu vào là Git URL / shorthand. Chuỗi không khớp mẫu nào được coi là đường dẫn cục bộ và xử lý ở AD-01.
3. **[Host File System]** Gọi hàm hệ điều hành `tempfile.mkdtemp(prefix="repoatlas_repo_")` để cấp phát một thư mục rỗng tạm thời.
4. **[CLI Scanner]** In thông báo: `Dang clone git repository tu: <url>...`
5. **[CLI Scanner]** Khởi chạy tiến trình con thực thi lệnh Git: `git clone --depth 1 <url> <temp_dir>`.
6. **[Git Remote Server]** Tiếp nhận yêu cầu tải bản sao nông (depth = 1).
7. **[Git Remote Server]** **Điểm quyết định 2:** Kết nối mạng và quyền truy cập kho mã nguồn có hợp lệ không?
   - *Nhánh Thất bại (Mất mạng, sai địa chỉ, kho riêng tư không có quyền):* Trả về mã lỗi khác 0 và thông điệp lỗi stderr.
   - *Nhánh Thành công:* Đóng gói dữ liệu commit mới nhất và truyền về cho máy trạm.
8. **[CLI Scanner]** Kiểm tra mã thoát của lệnh Git con:
   - *Nếu có lỗi (`subprocess.CalledProcessError`):*
     - Gọi hàm thu hồi tài nguyên `cleanup()` để xóa ngay thư mục tạm vừa tạo trên `Host File System`.
     - Ném ngoại lệ `ValueError` kèm thông báo lỗi chi tiết từ Git stderr.
     - Dừng quy trình tải **(Điểm kết thúc lỗi)**.
   - *Nếu thành công (Exit Code = 0):*
     - Gán thuộc tính `self.repo_path` bằng đường dẫn tuyệt đối của thư mục tạm.
     - Trả về đường dẫn để tiếp tục quy trình quét mã nguồn **(Điểm kết thúc thành công)**.

### 2.4. Quy tắc nghiệp vụ chi phối
- Bắt buộc dùng cờ `--depth 1` để tối ưu thời gian clone và không tải lịch sử commit dư thừa.
- Nếu clone thất bại, không bao giờ để lại thư mục rác trên đĩa máy trạm.

### 2.5. Căn cứ phân tích
- Code: `backend/src/core_indexing/scanner.py:70-87` (hàm `_is_git_url`), `scanner.py:89-118` (hàm `prepare_repository`), `scanner.py:221-226` (hàm `cleanup`).
- Tài liệu: `docs/user-stories.md` US-1.1.

---

## 3. QUY TRÌNH 3 (AD-03): QUÉT THƯ MỤC VÀ PHÂN TÍCH CÚ PHÁP AST ĐA NGÔN NGỮ

### 3.1. Tên quy trình và mục tiêu
- **Tên quy trình:** Quét Thư mục Dự án, Áp dụng Bộ lọc Loại trừ và Phân tích Cú pháp AST.
- **Mục tiêu nghiệp vụ:** Xây dựng cây cấu trúc thư mục, nhận diện các tệp nguồn hợp lệ và sử dụng bộ phân tích cú pháp AST chuyên biệt (Java/C#) để trích xuất ký hiệu và quan hệ.

### 3.2. Phân chia Swimlane
1. `Repository Scanner`: Điều phối duyệt thư mục và nạp bộ lọc `.gitignore`.
2. `Java Parser`: Bộ phân tích cú pháp cho tệp nguồn Java.
3. `CSharp Parser`: Bộ phân tích cú pháp cho tệp nguồn C#.
4. `Local File System`: Đọc nội dung tệp và ghi tệp chỉ mục.

### 3.3. Trình tự hành động chi tiết
1. **[Repository Scanner]** Đọc tệp `.gitignore` từ thư mục gốc của repository (nếu có).
2. **[Repository Scanner]** Biên dịch các quy tắc loại trừ thành bộ lọc đường dẫn (`pathspec`).
3. **[Repository Scanner]** Duyệt đệ quy cây thư mục dự án để xây dựng cây cấu trúc `DirectoryNode`:
   - Bỏ qua các thư mục nằm trong danh sách loại trừ mặc định (`DEFAULT_EXCLUDES`: `.git`, `bin`, `obj`, `target`, `build`, `node_modules`...).
   - Bỏ qua các đường dẫn khớp với quy tắc `.gitignore`.
4. **[Local File System]** Ghi cấu trúc cây thư mục ra tệp `indexes/structure.json`.
5. **[Repository Scanner]** Khởi tạo danh sách rỗng chứa các chỉ mục tệp (`file_indexes = []`).
6. **[Repository Scanner]** **Bắt đầu vòng lặp duyệt từng tệp tin trong repository (Loop over files):**
   - Lấy tệp tiếp theo.
   - **Điểm quyết định 1:** Phần mở rộng của tệp có nằm trong danh mục parser hỗ trợ (`.java`, `.cs`) không?
     - *Không:* Bỏ qua, chuyển sang tệp tiếp theo trong vòng lặp.
     - *Có:* Kiểm tra xem tệp có bị loại trừ bởi `.gitignore` không?
       - *Bị loại trừ:* Bỏ qua tệp.
       - *Hợp lệ:* Tiếp tục xử lý.
   - **[Local File System]** Đọc toàn bộ nội dung văn bản UTF-8 của tệp tin.
   - **[Repository Scanner]** **Điểm quyết định 2:** Ngôn ngữ của tệp tin là gì?
     - *Nhánh Java (`.java`):* Chuyển nội dung cho `Java Parser`.
     - *Nhánh C# (`.cs`):* Chuyển nội dung cho `CSharp Parser`.
   - **[Java Parser / CSharp Parser]** Phân tích cú pháp AST:
     - Tạo cây cú pháp trừu tượng bằng thư viện parser.
     - Trích xuất thông tin gói/không gian tên, chỉ thị import/using.
     - Trích xuất các kiểu dữ liệu (Class, Interface, Enum, Record, Struct) và thành viên (Method, Field, Property).
     - Trích xuất các chú thích framework (`@RestController`, `[ApiController]`), docstring và phạm vi dòng mã nguồn.
     - Trích xuất các quan hệ: kế thừa (`extends`), cài đặt (`implements`), gọi hàm (`calls`), dùng trường (`uses_field`).
     - Đóng gói thành đối tượng `FileIndex`.
   - **[Repository Scanner]** Đưa `FileIndex` vào danh sách `file_indexes`.
   - *Xử lý lỗi cục bộ trong vòng lặp:* Nếu quá trình đọc hoặc parse một tệp phát sinh ngoại lệ, bắt giữ lỗi, ghi nhật ký cảnh báo và tiếp tục vòng lặp với các tệp còn lại (không dừng pipeline).
   > **Ghi chú vòng lặp:** Mọi nhánh sau đây đều có **mũi tên quay lại đầu vòng lặp** "Lấy tệp tiếp theo": đuôi không được hỗ trợ; tệp bị `.gitignore` loại trừ; ngoại lệ đọc/parse một tệp (ghi cảnh báo rồi tiếp tục). Kết thúc vòng lặp khi không còn tệp nào.
7. **[Repository Scanner]** **Kết thúc vòng lặp duyệt tệp tin.**
8. **[Repository Scanner]** Khởi tạo bộ lập chỉ mục `RepositoryIndexer`, liên kết cây thư mục và danh sách `file_indexes` để tổng hợp thành đối tượng thống nhất `RepositoryIndex`.
9. **[Local File System]** Xuất khẩu dữ liệu ra 2 tệp tin: `indexes/repository_index.json` và `indexes/structure_overview.json`. **(Điểm kết thúc thành công)**.

### 3.4. Quy tắc nghiệp vụ chi phối
- Lỗi cú pháp của một tệp tin đơn lẻ không được phép làm dừng toàn bộ tiến trình quét của dự án (Error Isolation Principle).
- Toàn bộ ký hiệu được trích xuất phải được chuẩn hóa tên định danh toàn cục (`fully_qualified_name`) độc lập với ngôn ngữ.

### 3.5. Căn cứ phân tích
- Code: `backend/src/core_indexing/scanner.py:120-220`, `backend/src/core_indexing/indexer.py:20-80`, `backend/src/core_indexing/ir_generator.py:17-48`.
- Tài liệu: `docs/designs/ast-parser-design.md`, `docs/user-stories.md` US-1.2, US-1.3, US-1.4.

---

## 4. QUY TRÌNH 4 (AD-04): PHÂN KHÚC CÚ PHÁP VÀ TÓM TẮT PHÂN CẤP BOTTOM-UP CÓ QUẢN TRỊ TOKEN

### 4.1. Tên quy trình và mục tiêu
- **Tên quy trình:** Phân khúc Cú pháp và Tóm tắt Phân cấp Bottom-Up với Quản trị Ngân sách Token.
- **Mục tiêu nghiệp vụ:** Phân đoạn mã nguồn theo cây phân loại 6 tầng, thực hiện tóm tắt từ tầng sâu nhất lên tầng cao nhất thông qua Ollama LLM, áp dụng trần ngân sách 2000 tokens và kiểm tra chống ảo giác.

### 4.2. Phân chia Swimlane
1. `Taxonomy & Chunker`: Xây dựng cây phân loại và trích xuất khung xương cú pháp.
2. `Summarizer Engine`: Điều phối luồng duyệt Bottom-Up, kiểm tra ngân sách và tạo prompt.
3. `Local Ollama Server`: Máy chủ LLM thực hiện suy luận văn bản.
4. `Analysis Output`: Lưu kết quả tóm tắt và báo cáo ngân sách token.

### 4.3. Trình tự hành động chi tiết
1. **[Taxonomy & Chunker]** Nạp `repository_index.json` và `structure_overview.json`.
2. **[Taxonomy & Chunker]** Xây dựng cây phân cấp 6 tầng (`TaxonomyTree`):  
   `Tầng 1 (Repository) → Tầng 2 (Module) → Tầng 3 (Container) → Tầng 4 (Component) → Tầng 5 (Class) → Tầng 6 (Method)`.
3. **[Summarizer Engine]** Lấy danh sách toàn bộ các nút trong cây và sắp xếp theo thứ tự độ sâu giảm dần (duyệt từ dưới lên: Method trước, rồi Class, Component, Container, Module, Repository).
4. **[Summarizer Engine]** **Bắt đầu vòng lặp duyệt từng nút trong cây phân cấp (Loop over taxonomy nodes):**
   - Lấy nút tiếp theo cần tóm tắt.
   - **Điểm quyết định 1:** Nút hiện tại thuộc tầng nào?
     - *Tầng 6 (Method):* tạo chunk khung xương cú pháp (chữ ký, docstring, chú thích, bỏ thân hàm).
     - *Tầng 5 (Class):* tạo chunk khung xương của lớp **và** thu thập digest tóm tắt các Method con đã sinh.
     - *Tầng 4 trở lên (Component, Container, Module, Repository):* chỉ thu thập digest tóm tắt các nút con trực thuộc.
   > **Ghi chú:** Chế độ `NullLLMClient` (không AI) không đi qua AD-04; tóm tắt cấu trúc do UC-06 tạo. Nếu Ollama lỗi giữa chừng khi đang chạy vòng lặp thì **chưa xác nhận** trong mã.
   - **[Summarizer Engine]** Tính toán số lượng token ước tính của ngữ cảnh prompt (`tokens.count_tokens`).
   - **[Summarizer Engine]** **Điểm quyết định 2:** Số token ước tính có vượt quá ngân sách quy định (2000 tokens) không?
     - *Có vượt quá:* Thực hiện cắt tỉa khung xương cú pháp (lược bỏ chữ ký phụ hoặc danh sách tham số chi tiết), gắn cờ `was_degraded = True` cho đến khi token <= 2000.
     - *Không vượt quá:* Giữ nguyên toàn bộ ngữ cảnh chi tiết.
   - **[Summarizer Engine]** Đóng gói câu lệnh nhắc hoàn chỉnh (System prompt + Context + Task).
   - **[Local Ollama Server]** Gửi yêu cầu suy luận đến endpoint `/api/generate` của Ollama.
   - **[Local Ollama Server]** Sinh chuỗi văn bản tóm tắt tự nhiên và trả về phản hồi.
   - **[Summarizer Engine]** Kiểm tra chống ảo giác (Hallucination Validation): quét văn bản tóm tắt vừa nhận, trích xuất các FQN được nhắc đến và đối chiếu với bảng chỉ mục ký hiệu; chỉ lưu các ký hiệu thực sự có thật vào `referenced_symbols`.
   - **[Summarizer Engine]** Tạo đối tượng `SummaryNode` kèm theo báo cáo token `TokenReport` ghi nhận số lượng token thực tế và thời gian thực thi.
5. **[Summarizer Engine]** **Kết thúc vòng lặp duyệt nút.**
6. **[Summarizer Engine]** Kích hoạt bộ sinh nội dung chuyên đề (`ContentGenerator`), tổng hợp các phát hiện kiến trúc để sinh phần thân văn bản cho 4 chuyên đề: `tech`, `tests`, `architecture`, `modules`.
7. **[Analysis Output]** Đóng gói đối tượng `AnalysisResult` và ghi ra tệp `analysis/summaries.json`. **(Điểm kết thúc thành công)**.

### 4.4. Quy tắc nghiệp vụ chi phối
- Thứ tự duyệt bắt buộc phải là Bottom-Up để đảm bảo mọi nút cha đều có đầy đủ tóm tắt của các nút con khi xây dựng ngữ cảnh.
- Ngân sách token cho mỗi prompt không bao giờ được vượt quá 2000 tokens để tương thích với các mô hình nhỏ (7B/8B SLM).

### 4.5. Căn cứ phân tích
- Code: `backend/src/ai_analysis/models.py:25-53` (lớp `Tier`), `models.py:113-134` (hàm `bottom_up`), `backend/src/ai_analysis/chunker.py:80-140`, `backend/src/ai_analysis/summarizer.py:50-180`, `backend/src/ai_analysis/content_generator.py`.
- Tài liệu: `docs/designs/hierarchical-prompting-chunking.md`, `docs/user-stories.md` US-3.1 - US-3.5.

---

## 5. QUY TRÌNH 5 (AD-05): XÂY DỰNG VÀ LƯU TRỮ ĐỒ THỊ TRI THỨC NGUYÊN TỬ

### 5.1. Tên quy trình và mục tiêu
- **Tên quy trình:** Hợp nhất Thực thể, Thẩm định Toàn vẹn và Lưu trữ Đồ thị Tri thức Nguyên tử.
- **Mục tiêu nghiệp vụ:** Kết hợp chỉ mục mã nguồn và kết quả phân tích AI thành Đồ thị Tri thức, tự động bù đắp nút cho thư viện ngoài, thẩm định tính toàn vẹn và ghi tệp an toàn chống hỏng dữ liệu.

### 5.2. Phân chia Swimlane
1. `Knowledge Graph Builder`: Tạo nút, gắn tóm tắt và nối cạnh quan hệ.
2. `Schema Validator`: Thẩm định tính toàn vẹn đa thực thể của đồ thị.
3. `Host File System`: Ghi tệp đệm tạm thời và thực thi hoán đổi tệp nguyên tử.

### 5.3. Trình tự hành động chi tiết
1. **[Knowledge Graph Builder]** Nạp `repository_index.json` và `summaries.json`.
2. **[Knowledge Graph Builder]** Tạo nút gốc `GraphNode(id="repository:<name>", type="repository")`.
3. **[Knowledge Graph Builder]** Duyệt danh sách tệp nguồn: tạo nút `file:<path>` và nối cạnh `contains` từ repository tới từng tệp.
4. **[Knowledge Graph Builder]** Duyệt danh sách ký hiệu: tạo nút `symbol:<fqn>` và nối cạnh `contains` hoặc `declares`.
5. **[Knowledge Graph Builder]** Nạp cây phân loại: tạo nút Module, Container, Component và gắn quan hệ chứa đựng.
6. **[Knowledge Graph Builder]** **Vòng lặp** duyệt các quan hệ phụ thuộc (`extends`, `implements`, `calls`, `uses_field`):
   - **Quyết định 1:** `target` có tồn tại trong danh mục nút không?
     - *Có:* tạo `GraphEdge(source, target, kind)`.
     - *Không (thư viện ngoài/SDK):* tạo nút `GraphNode(id=target, type="EXTERNAL", metadata.external=True)` rồi tạo cạnh.
7. **[Knowledge Graph Builder]** Nạp `summaries.json`, đối chiếu theo mã định danh nút, gán vào `metadata.summary`.
8. **[Schema Validator]** `validate_graph_integrity`:
   - **Quyết định 2:** có hai nút trùng `id` không? *Có:* ném `ValueError("Graph node IDs must be unique")`, dừng **(Kết thúc lỗi 1, chưa ghi đĩa)**.
   - **Quyết định 3:** có cạnh nào có `source`/`target` không thuộc tập ID nút không? *Có:* ném `ValueError("Edge endpoint is missing")`, dừng **(Kết thúc lỗi 2, chưa ghi đĩa)**.
9. **[Host File System]** Mở tệp tạm `tempfile.NamedTemporaryFile(prefix=".graph.", suffix=".tmp")` trong `graphs/`.
10. **[Host File System]** Ghi toàn bộ đồ thị JSON vào tệp tạm. Lỗi I/O: nhảy tới bước 12 rồi **(Kết thúc lỗi 3)**.
11. **[Host File System]** `os.replace(tệp_tạm, "graphs/graph.json")`.
12. **[Host File System]** Khối `finally`: xóa tệp tạm nếu còn sót. Sau finally: nếu bước 10/11 thành công → **Điểm kết thúc thành công**; nếu có lỗi I/O → **Điểm kết thúc lỗi 3**.

### 5.4. Quy tắc nghiệp vụ chi phối
- Đồ thị tri thức tuyệt đối không được chứa cạnh mồ côi (Dangling Edges) hoặc nút trùng ID.
- Quá trình ghi đĩa phải luôn sử dụng cơ chế ghi đệm tạm thời rồi đổi tên nguyên tử để ngăn chặn việc tệp `graph.json` bị hỏng khi mất nguồn điện.

### 5.5. Căn cứ phân tích
- Code: `backend/src/knowledge_graph/builder.py:64-322`, `builder.py:334-360` (hàm `write_graph`), `backend/src/knowledge_graph/models.py:74-95` (hàm `validate_graph_integrity`).
- Tài liệu: `docs/designs/knowledge-graph-schema.md`, `docs/user-stories.md` US-2.1, US-2.2.

---

## 6. QUY TRÌNH 6 (AD-06): BIÊN DỊCH GÓI TÀI LIỆU HTML VÀ TẠO CHỈ MỤC SONG SONG

### 6.1. Tên quy trình và mục tiêu
- **Tên quy trình:** Biên dịch Gói Tài liệu Wiki Tĩnh Đa trang và Tạo Chỉ mục Tìm kiếm Ngoại tuyến.
- **Mục tiêu nghiệp vụ:** Nạp khuôn mẫu Jinja2, phân nhánh kết xuất đồng thời các trang chuyên đề và các trang chi tiết ký hiệu, sau đó hợp nhất dữ liệu để xuất bản chỉ mục tìm kiếm và ngữ cảnh AI.

### 6.2. Phân chia Swimlane
1. `Wiki Renderer`: Điều phối toàn bộ quy trình biên dịch tài liệu.
2. `Jinja2 Engine`: Nạp khuôn mẫu và kết xuất chuỗi HTML từ dữ liệu ngữ cảnh.
3. `Local File System`: Tạo thư mục và ghi các tệp `.html`, `.json`.

### 6.3. Trình tự hành động chi tiết
1. **[Local File System]** Tạo thư mục `wiki/` và thư mục con `wiki/symbols/` nếu chưa có.
2. **[Wiki Renderer]** Nạp môi trường khuôn mẫu Jinja2 từ thư mục `templates/`.
3. **[Wiki Renderer]** **Thanh phân nhánh song song (Fork Node):** Tách thành 2 nhánh xử lý đồng thời:
   - **Nhánh A (Kết xuất các Trang Chuyên đề và Bảng điều khiển):**
     - Lần lượt lấy dữ liệu nội dung từ `analysis_result.content`.
     - Với mỗi phần nội dung (`tech`, `architecture`, `modules`, `tests`):
       - Gọi `Jinja2 Engine` nạp template tương ứng (`tech.html`, `architecture.html`...).
       - Render chuỗi HTML và ghi xuống `wiki/<section.key>.html`.
     - Trích xuất dữ liệu tổng quan dự án từ `repository_index` và gọi `Jinja2 Engine` render trang trung tâm `wiki/index.html`.
   - **Nhánh B (Kết xuất Trang Hồ sơ Ký hiệu Cú pháp):**
     - Lấy danh sách ký hiệu `symbols` từ `repository_index`.
     - Gọi `Jinja2 Engine` nạp template `symbol.html`.
     - **Vòng lặp duyệt từng ký hiệu (Loop over symbols):**
       - Kiểm tra ký hiệu có `fully_qualified_name` không?
       - Nếu có: Chuẩn hóa tên tệp an toàn (thay thế `<` và `>` bằng `_`).
       - Render template với `rel_prefix="../"` và ghi ra `wiki/symbols/<safe_filename>.html`.
4. **[Wiki Renderer]** **Thanh hợp nhất luồng song song (Join Node):** Chờ cả Nhánh A và Nhánh B hoàn thành toàn bộ thao tác kết xuất HTML.
5. **[Wiki Renderer]** Tiếp tục luồng tuần tự tạo dữ liệu phụ trợ:
   - **Tạo Search Index:** Thu thập URL của 5 trang chính và toàn bộ URL các trang ký hiệu `symbols/<safe_filename>.html`, đóng gói và ghi ra `wiki/search_index.json`.
   - **Tạo AI Context:** Thu thập toàn bộ ký hiệu kèm chữ ký phương thức đã định dạng, docstring, chú thích, nội dung các phần chuyên đề và các bản tóm tắt phân cấp, đóng gói và ghi ra `wiki/wiki_context.json`.
6. **[Wiki Renderer]** Hoàn tất toàn bộ gói tài liệu tĩnh trong thư mục `wiki/`. **(Điểm kết thúc thành công)**.

### 6.4. Quy tắc nghiệp vụ chi phối
- Nhánh A và Nhánh B độc lập về mặt dữ liệu khuôn mẫu nên có thể xử lý song song.
- Quá trình sinh `search_index.json` và `wiki_context.json` bắt buộc phải diễn ra sau khi đã xác định đầy đủ danh mục ký hiệu và các trang đã render.
- Fork/Join thể hiện hai nhánh độc lập về dữ liệu (có thể song song về logic). Mã hiện tại **chưa xác nhận** chạy song song thật. Người vẽ vẫn vẽ Fork/Join theo kịch bản.

### 6.5. Căn cứ phân tích
- Code: `backend/src/wiki_generation/renderer.py:20-83`, `renderer.py:84-182`, `backend/src/cli.py:101-125`.
- Tài liệu: `docs/designs/html-wiki-storage.md`, `docs/user-stories.md` US-4.1 - US-4.6.

---

## 7. QUY TRÌNH 7 (AD-07): ĐIỀU HƯỚNG VÀ TÌM KIẾM NGOẠI TUYẾN PHÍA TRÌNH DUYỆT

### 7.1. Tên quy trình và mục tiêu
- **Tên quy trình:** Duyệt Cây Tài liệu và Tìm kiếm Trực tiếp Ngoại tuyến trên Giao diện Wiki.
- **Mục tiêu nghiệp vụ:** Cho phép người đọc wiki duyệt các trang chuyên đề qua thanh bên hoặc gõ từ khóa tìm kiếm trực tiếp với tốc độ phản hồi tức thì hoàn toàn phía trình duyệt.

### 7.2. Phân chia Swimlane
1. `Wiki User`: Người đọc tài liệu thao tác nhấp chuột hoặc gõ từ khóa.
2. `Browser UI & DOM`: Giao diện web hiển thị, bắt sự kiện và cập nhật giao diện.
3. `Client Search Engine (JS)`: Mã JavaScript nội bộ xử lý nạp chỉ mục và lọc từ khóa.

### 7.3. Trình tự hành động chi tiết
1. **[Browser UI & DOM]** Người dùng mở trang wiki (ví dụ `wiki/index.html`).
2. **[Client Search Engine (JS)]** Bắt sự kiện `DOMContentLoaded`:
   - Gửi yêu cầu `fetch('search_index.json')` để nạp toàn bộ danh mục tìm kiếm vào biến bộ nhớ `searchIndex`. Nếu `fetch('search_index.json')` thất bại: ghi lỗi Console, tìm kiếm không khả dụng, vẫn cho phép duyệt thanh bên.
   - Phân tích đường dẫn `window.location.pathname`, tìm phần tử thanh bên tương ứng và gắn lớp CSS làm nổi bật mục hiện tại (`active sidebar state`).
3. **[Wiki User]** **Điểm quyết định 1 (Lựa chọn thao tác của người dùng):**
   - **Nhánh 1 (Điều hướng qua Thanh bên Sidebar):**
     - Người dùng nhấp chuột vào một mục chuyên đề trên thanh bên (ví dụ "Architecture").
     - **[Browser UI & DOM]** Trình duyệt chuyển hướng ngay sang trang `wiki/architecture.html`.
     - Mã JavaScript trên trang mới tự động cập nhật trạng thái nổi bật cho mục thanh bên mới. **(Điểm kết thúc nhánh 1)**.
   - **Nhánh 2 (Tìm kiếm trực tiếp Live Search):**
     - Người dùng nhấp chuột vào ô tìm kiếm trên thanh tiêu đề và gõ ký tự.
     - **[Browser UI & DOM]** Bắt sự kiện `input` trên ô tìm kiếm.
     - **[Client Search Engine (JS)]** Lấy chuỗi tìm kiếm, chuyển thành chữ thường và cắt bỏ khoảng trắng.
     - **Điểm quyết định 2:** Chuỗi tìm kiếm có rỗng không?
       - *Rỗng:* Thêm lớp `hidden` vào phần tử kết quả `searchResults` để ẩn danh sách.
       - *Không rỗng:* Tiếp tục lọc.
     - **[Client Search Engine (JS)]** Duyệt mảng `searchIndex`, lọc các phần tử có tên chứa chuỗi từ khóa tìm kiếm và lấy tối đa 15 kết quả hàng đầu (`.slice(0, 15)`).
     - **[Browser UI & DOM]** **Điểm quyết định 3:** Có tìm thấy kết quả phù hợp không?
       - *Có:* Tạo các phần tử liên kết thẻ `<a>` cho từng kết quả và gỡ bỏ lớp `hidden` để hiển thị danh sách thả xuống. Nếu người dùng nhấp chuột ra ngoài ô tìm kiếm thì thêm lớp `hidden` để ẩn danh sách.
       - *Không:* Hiển thị thông báo `No results found`.
     - **[Wiki User]** Người dùng quan sát danh sách thả xuống và nhấp chuột vào một kết quả mong muốn.
     - **[Browser UI & DOM]** Trình duyệt chuyển hướng ngay đến trang tài liệu của ký hiệu hoặc chuyên đề tương ứng (`relPrefix + item.url`). **(Điểm kết thúc nhánh 2)**.

> **Ghi chú vẽ:** "Điểm kết thúc nhánh 1/2" vẽ là **Flow Final** (hoặc quay về chờ thao tác tiếp), không phải Activity Final.

### 7.4. Quy tắc nghiệp vụ chi phối
- Toàn bộ việc tìm kiếm phải diễn ra 100% trong bộ nhớ RAM của trình duyệt, không gửi bất kỳ yêu cầu mạng nào ra ngoài máy cục bộ.
- Nhấp chuột ra ngoài ô tìm kiếm phải tự động đóng danh sách kết quả thả xuống.

### 7.5. Căn cứ phân tích
- Code: `backend/src/wiki_generation/templates/base.html:232-304`.
- Tài liệu: `docs/user-stories.md` US-4.5.

---

## 8. QUY TRÌNH 8 (AD-08): TƯƠNG TÁC HỎI ĐÁP VÀ TRUYỀN LUỒNG THỜI GIAN THỰC VỚI TRỢ LÝ AI

### 8.1. Tên quy trình và mục tiêu
- **Tên quy trình:** Tương tác Hỏi đáp Codebase và Truyền luồng Phản hồi với Trợ lý AI Cục bộ.
- **Mục tiêu nghiệp vụ:** Phân tích câu hỏi tự nhiên của người dùng, trích xuất ngữ cảnh liên quan nhất từ kho tri thức nội bộ, gửi yêu cầu suy luận đến Ollama và truyền luồng câu trả lời về giao diện hoặc tự động chuyển tiếp sang chế độ dự phòng thông minh nếu Ollama ngoại tuyến.

### 8.2. Phân chia Swimlane
1. `Wiki User`: Người dùng nhập câu hỏi và đọc câu trả lời.
2. `AI Chat Widget (JS)`: Mã JavaScript quản lý giao diện chat, phân tích ý định, xếp hạng ngữ cảnh và dự phòng.
3. `Local Ollama Server`: Dịch vụ máy chủ suy luận mô hình ngôn ngữ cục bộ.

### 8.3. Trình tự hành động chi tiết
1. **[Wiki User]** Nhấp vào nút nổi (Floating Button) mở bảng chat Trợ lý AI ở góc màn hình.
2. **[AI Chat Widget (JS)]** Bắt sự kiện, hiển thị khung chat và gửi yêu cầu ngầm kiểm tra sức khỏe dịch vụ: `fetch("http://localhost:11434/api/tags")`.
   - Nếu phản hồi có mô hình `qwen2.5-coder:3b`: Cập nhật chấm trạng thái màu xanh ("Ollama online").
   - Nếu server có nhưng **thiếu model** `qwen2.5-coder:3b`: Cập nhật chấm đỏ, như không kết nối.
   - Nếu không kết nối được: Cập nhật chấm trạng thái màu đỏ ("Ollama offline · dùng tìm kiếm nội bộ").
   > **Lưu ý:** Sau lần kiểm tra đầu, widget kiểm tra lại mỗi 30 giây (chưa xác nhận trong mã).
3. **[Wiki User]** Gõ câu hỏi tự nhiên vào ô nhập liệu và bấm nút Gửi (hoặc nhấn Enter).
4. **[AI Chat Widget (JS)]** Hiển thị câu hỏi của người dùng vào khung chat và tạo một bong bóng thông báo "Đang suy nghĩ...".
5. **[AI Chat Widget (JS)]** Phân tích câu hỏi:
   - Phát hiện ý định (Intent Detection): kiểm tra xem câu hỏi có thuộc dạng đếm số lượng, hỏi vị trí, hỏi kiểm thử hay hỏi kiến trúc không.
   - Tách từ khóa (Keyword Extraction): chuẩn hóa bỏ dấu tiếng Việt, tách các từ có độ dài trên 2 ký tự và loại bỏ các từ dừng thông dụng (`STOP_WORDS`).
6. **[AI Chat Widget (JS)]** Tính điểm liên quan (Scoring):
   - Duyệt mảng ký hiệu trong `wiki_context.json`: cộng điểm tương ứng nếu tên ký hiệu, FQN, đường dẫn tệp hoặc docstring chứa từ khóa; lấy 12 ký hiệu có điểm cao nhất.
   - Duyệt các phần chuyên đề wiki: cộng điểm cho tiêu đề và nội dung; lấy 3 chuyên đề có điểm cao nhất.
7. **[AI Chat Widget (JS)]** Đóng gói chuỗi ngữ cảnh tri thức và câu lệnh nhắc yêu cầu AI trả lời trung thực, không bịa đặt.
8. **[AI Chat Widget (JS)]** Gửi yêu cầu HTTP POST đến `http://localhost:11434/api/generate` kèm cờ `stream: true`.
9. **[AI Chat Widget (JS)]** **Điểm quyết định 1: Yêu cầu kết nối đến Ollama có thành công không?**
   - **Nhánh Thành công (Ollama phản hồi HTTP 200):**
     - Đọc luồng dữ liệu trả về qua `response.body.getReader()`.
     - Xóa dòng chữ "Đang suy nghĩ...".
     - **Vòng lặp đọc gói dữ liệu (Stream Loop):** Nhận từng đoạn dữ liệu (chunks), giải mã UTF-8, phân tích dòng JSON và gắn trực tiếp từ ngữ phản hồi vào khung chat theo thời gian thực cho đến khi kết thúc luồng. (Lưu ý: Lỗi giữa chừng khi đang stream: chưa xác nhận; nếu `fetch` ném ngoại lệ hoặc `response.ok = false` thì chuyển sang nhánh dự phòng).
     - Tự động cuộn khung chat xuống dưới cùng. **(Điểm kết thúc nhánh AI)**.
   - **Nhánh Thất bại (Lỗi mạng hoặc CORS):**
     - Kích hoạt cơ chế Chuyển đổi Dự phòng Thông minh (Intelligent Fallback):
       - **Điểm quyết định 2:** Ý định câu hỏi là gì?
         - *Nếu là câu hỏi thống kê/đếm:* Hiển thị tổng số lớp, số hàm, ngôn ngữ và danh sách 30 ký hiệu tiêu biểu kèm liên kết.
         - *Nếu có ký hiệu liên quan theo từ khóa:* Hiển thị thẻ tóm tắt chi tiết của từng ký hiệu khớp (chữ ký, đường dẫn tệp, docstring) kèm siêu liên kết mở trang ký hiệu.
         - *Nếu không có ký hiệu khớp:* Hiển thị bản tóm tắt tổng quan kiến trúc codebase.
       - Hiển thị hộp chỉ dẫn lệnh PowerShell để người dùng khởi động Ollama khi cần thiết.
       - Cập nhật nội dung dự phòng vào khung chat. **(Điểm kết thúc nhánh Dự phòng)**.
10. **[Wiki User]** Người dùng đọc câu trả lời và nhấp vào các liên kết ký hiệu mã nguồn để xem chi tiết.

### 8.4. Quy tắc nghiệp vụ chi phối
- Trợ lý AI tuyệt đối không được bịa đặt thông tin; mọi câu trả lời đều phải gắn liền với ngữ cảnh trích xuất từ `wiki_context.json`.
- Khi máy chủ Ollama ngoại tuyến, tiện ích không được hiển thị màn hình trắng hay báo lỗi vô nghĩa mà phải cung cấp kết quả từ bộ tìm kiếm nội bộ.

### 8.5. Căn cứ phân tích
- Code: `backend/src/wiki_generation/templates/base.html:305-604`.
- Tài liệu: `docs/user-stories.md` US-4.6, `README.md:Line 14`.

---

## 9. QUY TRÌNH 9 (AD-09): THĂM DÒ SỨC KHỎE OLLAMA VÀ HẠ CẤP DỰ PHÒNG

### 9.1. Tên quy trình và mục tiêu
- **Tên quy trình:** Thăm dò Sức khỏe Máy chủ Ollama và Hạ cấp An toàn sang Chế độ Cấu trúc (Graceful Degradation).
- **Mục tiêu nghiệp vụ:** Tự động phát hiện trạng thái máy chủ AI trong quá trình chạy phân tích CLI; nếu dịch vụ gặp sự cố, tự động chuyển đổi sang bộ tóm tắt cấu trúc để đảm bảo tiến trình tạo tài liệu không bao giờ bị dừng giữa chừng.

### 9.2. Phân chia Swimlane
1. `CLI / Pipeline Coordinator`: Tiếp nhận cấu hình và kích hoạt phân hệ AI.
2. `AI Health Monitor`: Gửi yêu cầu thăm dò mạng và kiểm tra mô hình.
3. `Local Ollama Daemon`: Máy chủ dịch vụ AI cục bộ.

### 9.3. Trình tự hành động chi tiết
1. **[CLI / Pipeline Coordinator]** Đọc tham số `args.no_llm`.
2. **[CLI / Pipeline Coordinator]** **Điểm quyết định 1:** Người dùng có chỉ định cờ `--no-llm` không?
   - *Có (`args.no_llm = True`):* Ghi log "Running without an LLM; documentation will be structural only", khởi tạo ngay `NullLLMClient` và bỏ qua việc thăm dò mạng. **(Điểm kết thúc nhánh Tắt AI)**.
   - *Không (`use_llm = True`):* Tiếp tục bước thăm dò sức khỏe.
3. **[AI Health Monitor]** Khởi tạo đối tượng `OllamaClient(model, endpoint)`.
4. **[AI Health Monitor]** Gửi yêu cầu HTTP GET thăm dò đến `http://localhost:11434/api/tags` với thời gian chờ (timeout) quy định.
5. **[Local Ollama Daemon]** Xử lý yêu cầu thăm dò.
6. **[AI Health Monitor]** **Điểm quyết định 2: Kết quả thăm dò có phản hồi thành công không?**
   - *Không kết nối được hoặc hết thời gian chờ:*
     - Ghi nhật ký cảnh báo: `WARNING: Ollama is not usable at ... falling back to structural mode`.
     - Đóng kết nối máy khách (`client.close()`).
     - Khởi tạo và trả về đối tượng `NullLLMClient`. **(Điểm kết thúc nhánh Hạ cấp 1)**.
   - *Phản hồi thành công (HTTP 200):*
     - Đọc danh sách các mô hình hiện có trên máy chủ Ollama.
     - **Điểm quyết định 3:** Mô hình chỉ định (`qwen2.5-coder:3b`) có tồn tại trong danh sách không?
       - *Không tồn tại:* Ghi nhật ký cảnh báo thiếu mô hình, đóng kết nối và trả về `NullLLMClient`. **(Điểm kết thúc nhánh Hạ cấp 2)**.
       - *Tồn tại:* Ghi nhật ký xác nhận `Using Ollama model ... at ...`, trả về đối tượng `OllamaClient` hoạt động hoàn chỉnh. **(Điểm kết thúc nhánh Sẵn sàng AI)**.

### 9.4. Quy tắc nghiệp vụ chi phối
- Nguyên tắc suy giảm an toàn (Graceful Degradation): Sự cố của dịch vụ AI bên ngoài không bao giờ được phép làm hỏng mục tiêu cốt lõi là sinh bộ tài liệu kỹ thuật của dự án.

### 9.5. Căn cứ phân tích
- Code: `backend/src/ai_analysis/__main__.py:93-114` (hàm `build_llm`), `backend/src/ai_analysis/llm/ollama.py:40-75` (hàm `health_check`).
- Tài liệu: `docs/adrs.md` ADR-006, `docs/product.md` FR-9.

---

## 10. QUY TRÌNH 10 (AD-10): THU HỒI TÀI NGUYÊN TẠM THỜI VÀ XỬ LÝ LỖI TOÀN CỤC

### 10.1. Tên quy trình và mục tiêu
- **Tên quy trình:** Thu Hồi Tài Nguyên Tạm Thời và Dọn Dẹp An Toàn Khi Xảy Ra Sự Cố.
- **Mục tiêu nghiệp vụ:** Đảm bảo toàn bộ các thư mục làm việc tạm thời được giải phóng hoàn toàn khỏi ổ đĩa máy tính trong mọi tình huống kết thúc của pipeline (hoàn thành, gặp lỗi ngoại lệ hoặc người dùng bấm Ctrl+C).

### 10.2. Phân chia Swimlane
1. `CLI Orchestrator`: Quản lý khối bảo vệ `try...finally` toàn cục.
2. `Scanner / Workspace Manager`: Lưu trữ tham chiếu đường dẫn tạm và thực thi giải phóng.
3. `Host File System`: Xóa thư mục vật lý.

### 10.3. Trình tự hành động chi tiết
1. **[CLI Orchestrator]** Mở khối `try` bao bọc 4 giai đoạn pipeline.
2. **[CLI Orchestrator]** Pipeline kết thúc theo **một trong ba cách** (không vẽ Decision Node, cả ba cùng nối vào `finally`):
   - Hoàn thành bình thường;
   - Ngoại lệ chưa xử lý (lỗi đọc tệp, thẩm định đồ thị…);
   - Người dùng nhấn Ctrl+C (`KeyboardInterrupt`).
3. **[CLI Orchestrator]** Luồng điều khiển luôn đi vào khối `finally`.
4. **[Scanner / Workspace Manager]** Kiểm tra `self._temp_dir`.
5. **[Scanner / Workspace Manager]** **Quyết định:** `_temp_dir` có tồn tại không?
   - *Không (phân tích thư mục cục bộ):* bỏ qua việc xóa.
   - *Có (phân tích từ Git):* tiếp tục.
6. **[Host File System]** Gọi `shutil.rmtree(self._temp_dir, ignore_errors=True)`.
7. **[Scanner / Workspace Manager]** Đặt `self._temp_dir = None`.
8. **[CLI Orchestrator]** Giải phóng xong, thoát tiến trình.

> **Chưa xác nhận (không vẽ, hoặc vẽ nét đứt):** việc tự gỡ cờ chỉ đọc của tệp trong `.git` trên Windows rồi xóa lại. Vì `ignore_errors=True` nuốt lỗi nên mô tả "bắt lỗi quyền rồi xóa lại" chỉ đúng nếu mã có xử lý `onerror` riêng.

### 10.4. Quy tắc nghiệp vụ chi phối
- Đảm bảo tính nguyên vẹn và sạch sẽ của môi trường máy trạm: không bao giờ để rò rỉ các thư mục tạm sau khi ứng dụng kết thúc.

### 10.5. Căn cứ phân tích
- Code: `backend/src/cli.py:57-145`, `backend/src/core_indexing/scanner.py:221-226` (hàm `cleanup`).
- Tài liệu: `docs/designs/ast-parser-design.md`, `docs/adrs.md`.
