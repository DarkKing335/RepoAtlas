# 03 — Kịch bản Activity Diagram: RepoAtlas

> **Môn học:** Phân tích và Thiết kế Hướng đối tượng (OOAD)

---

## AD-01: Luồng Pipeline Phân tích Đầy đủ (UC-18)

**Tên biểu đồ:** Activity Diagram — Toàn bộ Pipeline `repoatlas analyze`
**Use Case tương ứng:** UC-18
**Mục đích:** Mô tả toàn bộ luồng điều phối từ khi người dùng nhập lệnh đến khi wiki được mở trong trình duyệt.
**Swimlane:**
- **Software Engineer:** Nhập lệnh và xem kết quả
- **CLI Orchestrator:** Điều phối pipeline
- **Core Indexing Engine:** Quét và phân tích AST
- **AI Analysis Engine:** Chunking và tóm tắt
- **Knowledge Graph Builder:** Xây dựng đồ thị
- **Wiki Generator:** Render HTML

### Kịch bản:

1. **Bắt đầu.**
2. **[Software Engineer]** Nhập lệnh `repoatlas analyze <path|url> [--no-llm]`.
3. **[CLI Orchestrator]** Parse đối số (`path`, `use_llm`).
4. **[CLI Orchestrator]** Quyết định: `path` có phải Git URL không?
   - **Nếu có (Git URL):** Chuyển sang AD-02 (luồng clone repo) rồi quay lại.
   - **Nếu không (local path):** Kiểm tra đường dẫn có tồn tại không?
     - **Nếu không tồn tại:** In lỗi "Khong tim thay duong dan", `sys.exit(1)`. → **Kết thúc (thất bại).**
     - **Nếu tồn tại:** Tiếp tục.
5. **[Core Indexing Engine]** Quét cấu trúc thư mục (duyệt đệ quy, tôn trọng .gitignore).
6. **[Core Indexing Engine]** Ghi `indexes/structure.json`.
7. **[Core Indexing Engine]** Duyệt file và phân tích AST từng file:
   - Với mỗi file `.java`: Gọi `JavaParser.parse()` → `FileIndex`.
   - Với mỗi file `.cs`: Gọi `CSharpParser.parse()` → `FileIndex`.
   - File parse lỗi: Log cảnh báo, bỏ qua, tiếp tục.
8. **[Core Indexing Engine]** Build `RepositoryIndex` từ tất cả `FileIndex`.
9. **[Core Indexing Engine]** Ghi `indexes/repository_index.json` và `indexes/structure_overview.json`.
10. **[AI Analysis Engine]** Nạp `repository_index.json`.
11. **[AI Analysis Engine]** Xây dựng `TaxonomyTree` 6 tầng.
12. **[CLI Orchestrator]** Quyết định: `use_llm = True`?
    - **Nếu có:** Kiểm tra Ollama health.
      - **Ollama khả dụng:** Dùng `OllamaClient`.
      - **Ollama không khả dụng:** Log cảnh báo, chuyển sang dùng `NullLLMClient`.
    - **Nếu không (`--no-llm`):** Dùng `NullLLMClient`.
13. **[AI Analysis Engine]** Duyệt tất cả nút taxonomy theo thứ tự bottom-up.
14. **[AI Analysis Engine]** Với mỗi nút:
    - Tạo chunk (AST skeleton hoặc child summaries digest).
    - Quyết định: LLM enabled?
      - **Có:** Gửi prompt đến LLM, nhận summary.
      - **Không:** Tạo structural summary từ metadata.
15. **[AI Analysis Engine]** Tạo wiki content sections (tech, tests, architecture, modules).
16. **[AI Analysis Engine]** Ghi `analysis/summaries.json`.
17. **[Knowledge Graph Builder]** Nạp `repository_index.json` và `summaries.json`.
18. **[Knowledge Graph Builder]** Tạo GraphNode cho repository, files, symbols, taxonomy.
19. **[Knowledge Graph Builder]** Tạo GraphEdge cho các quan hệ.
20. **[Knowledge Graph Builder]** Ghi `graphs/graph.json` (atomic write).
21. **[Wiki Generator]** Với mỗi content section (`tech`, `tests`, `architecture`, `modules`): Render HTML page bằng Jinja2 template.
22. **[Wiki Generator]** Render `wiki/index.html` (Dashboard).
23. **[Wiki Generator]** Render `wiki/symbols/*.html` cho mỗi symbol.
24. **[Wiki Generator]** Sinh `wiki/search_index.json`.
25. **[Wiki Generator]** Sinh `wiki/wiki_context.json`.
26. **[CLI Orchestrator]** In "SUCCESS: Phan tich hoan tat!".
27. **[CLI Orchestrator]** Quyết định: Hệ điều hành là Windows?
    - **Có:** Gọi `os.startfile(wiki/index.html)`.
    - **Không:** Gọi `webbrowser.open(uri)`.
    - **Mở thất bại:** Log cảnh báo, gợi ý mở thủ công.
28. **[CLI Orchestrator]** Gọi `scanner.cleanup()` (trong finally — luôn chạy).
29. **Kết thúc.**

---

## AD-02: Luồng Clone Repository từ Git URL (UC-02)

**Tên biểu đồ:** Activity Diagram — Clone Git Repository
**Use Case tương ứng:** UC-02
**Mục đích:** Mô tả chi tiết quá trình nhận diện URL, clone repo, và dọn dẹp.
**Swimlane:**
- **CLI/Scanner:** Điều khiển quá trình
- **Git Remote Server:** Cung cấp dữ liệu repo

### Kịch bản:

1. **Bắt đầu.**
2. **[CLI/Scanner]** Nhận `target` string từ người dùng.
3. **[CLI/Scanner]** Gọi `_is_git_url(target)` để nhận diện loại URL:
   - Khớp pattern `^https?://.*\.git$` hoặc `^git@.*:.*\.git$`: → **Git URL đầy đủ.**
   - Khớp pattern `^https?://github\.com/.*`: → **GitHub URL.**
   - Khớp pattern `^[\w\.-]+/[\w\.-]+$` và path không tồn tại locally: → **GitHub shorthand.**
   - Bắt đầu bằng `.`, `/`, `\` hoặc là absolute path: → **Đường dẫn cục bộ** (kết thúc luồng này).
4. **[CLI/Scanner]** Xây dựng URL đầy đủ:
   - Nếu shorthand (`owner/repo`): Ghép thành `https://github.com/owner/repo.git`.
   - Nếu đã là URL đầy đủ: Giữ nguyên.
5. **[CLI/Scanner]** Tạo thư mục tạm `tempfile.mkdtemp(prefix="repoatlas_repo_")`.
6. **[CLI/Scanner]** In thông báo "Dang clone git repository tu: <url>...".
7. **[CLI/Scanner]** Chạy `git clone --depth 1 <url> <temp_dir>`.
8. **[Git Remote Server]** Xử lý yêu cầu clone:
   - **Thành công:** Trả về dữ liệu repo.
   - **Thất bại (repo không tồn tại, mất mạng, không có quyền):** Trả về lỗi.
9. **[CLI/Scanner]** Quyết định: `git clone` thành công không?
   - **Có:** Đặt `self.repo_path = temp_dir`, tiếp tục pipeline.
   - **Không:** Gọi `cleanup()`, ném `ValueError("Failed to clone...")`. → **Kết thúc (thất bại).**
10. **[CLI/Scanner]** (Sau khi pipeline hoàn tất — trong `finally`) Gọi `cleanup()` xóa temp_dir.
11. **Kết thúc.**

---

## AD-03: Luồng Phân tích AST File Java (UC-03)

**Tên biểu đồ:** Activity Diagram — Parse Java Source File
**Use Case tương ứng:** UC-03
**Mục đích:** Mô tả quá trình đọc file .java và trích xuất ký hiệu AST.
**Swimlane:**
- **Scanner:** Quản lý vòng lặp file
- **JavaParser:** Phân tích AST

### Kịch bản:

1. **Bắt đầu.**
2. **[Scanner]** Duyệt thư mục, phát hiện file với extension `.java`.
3. **[Scanner]** Đọc nội dung file bằng `file_path.read_text(encoding="utf-8")`.
4. **[Scanner]** Gọi `JavaParser.parse(file_path, content, repo_path)`.
5. **[JavaParser]** Sử dụng `tree-sitter` để parse cú pháp Java thành AST.
6. **[JavaParser]** Trích xuất `package_or_namespace` từ package declaration.
7. **[JavaParser]** Trích xuất `imports` (import statements).
8. **[JavaParser]** Duyệt tất cả type declarations trong file:
   - Với mỗi class/interface/enum/record/annotation:
     a. Tạo `ASTSymbolNode` với `kind = CLASS/INTERFACE/ENUM/RECORD/ANNOTATION`.
     b. Trích xuất: `name`, `fully_qualified_name`, `modifiers`, `annotations`, `docstring` (Javadoc), `extends`, `implements`.
     c. Đặt `range = SourceRange(start_line, end_line)`.
     d. Duyệt members:
        - Field: Tạo `ASTSymbolNode` với `kind = FIELD`, trích xuất `field_type`.
        - Method/Constructor: Tạo `ASTSymbolNode` với `kind = METHOD/CONSTRUCTOR`, trích xuất `MethodSignature` (return_type, parameters, thrown_exceptions).
9. **[JavaParser]** Trả về `FileIndex` với danh sách symbols.
10. **[Scanner]** Quyết định: Parse thành công không?
    - **Có:** Thêm `FileIndex` vào `file_indexes`.
    - **Không:** Log lỗi `"Error parsing file '<path>': <error>"`, bỏ qua file.
11. **Kết thúc.**

---

## AD-04: Luồng Tóm tắt AI Bottom-Up (UC-05)

**Tên biểu đồ:** Activity Diagram — Hierarchical Bottom-Up AI Summarization
**Use Case tương ứng:** UC-05
**Mục đích:** Mô tả chi tiết quá trình tóm tắt bottom-up từ Method đến Repository.
**Swimlane:**
- **Summarizer:** Điều khiển luồng tóm tắt
- **Chunker:** Tạo context
- **Ollama LLM:** Sinh text summary

### Kịch bản:

1. **Bắt đầu.**
2. **[Summarizer]** Xây dựng thứ tự `bottom_up()` từ TaxonomyTree (từ lá đến gốc).
3. **[Summarizer]** Với mỗi nút `node` trong thứ tự bottom-up:
   a. **[Chunker]** Gọi `chunk_for(node, child_summaries)`:
      - Nếu `node.tier == METHOD`: Render AST skeleton của method (signature + docstring).
      - Nếu `node.tier == CLASS`: Render AST skeleton của class (fields + method signatures).
      - Nếu tier cao hơn (COMPONENT, CONTAINER, MODULE, REPOSITORY): Render digest của child summaries.
   b. **[Summarizer]** Xây dựng prompt với: tier context + skeleton/digest.
   c. **[Summarizer]** Tính token count của prompt.
   d. **[Summarizer]** Quyết định: Token count > budget (2000)?
      - **Có:** Cắt bớt context bằng `enforce_budget()`.
      - **Không:** Tiếp tục.
   e. **[Summarizer]** Quyết định: LLM enabled?
      - **Có (OllamaClient):**
        - Quyết định: Node là METHOD có >= 5 dòng code?
          - **Có:** Đính kèm tool `read_source_range` vào prompt.
        - Gửi prompt đến **[Ollama LLM]**.
        - **[Ollama LLM]** Sinh summary (streaming).
        - **[Summarizer]** Nhận và xử lý response.
      - **Không (NullLLMClient):** Tạo structural summary từ metadata AST.
   f. **[Summarizer]** Ground symbols: Kiểm tra mỗi identifier trong summary có tồn tại trong registry không.
   g. **[Summarizer]** Tạo `SummaryNode` với `summary`, `referenced_symbols`, `generated_by`.
   h. **[Summarizer]** Ghi nhận `TokenReport` cho nút này.
4. **[Summarizer]** Kiểm tra budget violations (summaries vượt 2000 tokens).
5. **[Summarizer]** Trả về danh sách `SummaryNode`.
6. **Kết thúc.**

---

## AD-05: Luồng Xây dựng Knowledge Graph (UC-08)

**Tên biểu đồ:** Activity Diagram — Build Knowledge Graph
**Use Case tương ứng:** UC-08
**Mục đích:** Mô tả quá trình tạo đồ thị tri thức từ IR và summaries.
**Swimlane:**
- **GraphBuilder:** Xây dựng đồ thị
- **File System:** Đọc/ghi artifact

### Kịch bản:

1. **Bắt đầu.**
2. **[GraphBuilder]** Nạp `repository_index.json` → `RepositoryIndex`.
3. **[GraphBuilder]** Nạp `structure_overview.json` → `StructureOverview` (tùy chọn).
4. **[GraphBuilder]** Nạp `analysis/summaries.json` → `AnalysisResult`.
5. **[GraphBuilder]** Xác nhận: `analysis.repository_name == index.repository_name`?
   - **Không khớp:** Ném `ValueError`. → **Kết thúc (thất bại).**
6. **[GraphBuilder]** Thêm node REPOSITORY gốc (`repository:<name>`).
7. **[GraphBuilder]** Với mỗi `FileIndex` trong `index.files`:
   - Tạo `GraphNode(type="FILE", id="file:<path>")`.
   - Thêm edge: `repository → file` (kind="contains").
8. **[GraphBuilder]** Với mỗi `ASTSymbolNode` trong `index.symbols`:
   - Tạo `GraphNode(type=<kind>, id=<symbol_id>)` với metadata đầy đủ.
   - Thêm edge: `file → symbol` (kind="declares").
9. **[GraphBuilder]** Với mỗi `RelationshipEdge` trong `index.relationships`:
   - Gọi `_ensure_endpoint()` cho source và target (tạo EXTERNAL node nếu thiếu).
   - Thêm `GraphEdge` với kind từ relationship (extends, implements, calls, v.v.).
10. **[GraphBuilder]** Nếu `analysis` có taxonomy: Duyệt `TaxonomyTree` đệ quy, tạo taxonomy nodes.
11. **[GraphBuilder]** Gắn AI summaries vào metadata của nodes tương ứng.
12. **[GraphBuilder]** Sắp xếp nodes và edges.
13. **[GraphBuilder]** Tạo `KnowledgeGraph` và validate integrity (unique IDs, edge endpoints).
14. **[GraphBuilder]** Quyết định: Validation thành công?
    - **Không:** Ném `ValueError`. → **Kết thúc (thất bại).**
15. **[File System]** Ghi ra temp file, sau đó `os.replace()` → `graphs/graph.json`.
16. **Kết thúc.**

---

## AD-06: Luồng Render Wiki HTML (UC-10 đến UC-17)

**Tên biểu đồ:** Activity Diagram — Render Static HTML Wiki
**Use Case tương ứng:** UC-10, UC-11, UC-12, UC-13, UC-14, UC-15, UC-16, UC-17
**Mục đích:** Mô tả toàn bộ quá trình sinh trang HTML từ data và templates Jinja2.
**Swimlane:**
- **Wiki Generator (renderer.py):** Điều phối render
- **Jinja2 Template Engine:** Render HTML
- **File System:** Ghi output

### Kịch bản:

1. **Bắt đầu.**
2. **[Wiki Generator]** Nhận `analysis_result` (AnalysisResult) và `repo_index` (RepositoryIndex dict).
3. **[Wiki Generator]** Duyệt `analysis_result.content` (danh sách content sections):
   - Với mỗi section (key: tech, tests, architecture, modules):
     a. **[Jinja2]** Load template `<key>.html` từ `wiki_generation/templates/`.
     b. **[Jinja2]** Render HTML với dữ liệu `section.model_dump()`.
     c. **[File System]** Ghi ra `wiki/<key>.html`.
4. **[Wiki Generator]** Gọi `render_index_page(repo_index_dict, analysis_result.model_dump())`:
   - **[Jinja2]** Load template `index.html`.
   - **[Jinja2]** Render với: repo_name, languages, files count, symbols count, relationships count.
   - **[File System]** Ghi ra `wiki/index.html`.
5. **[Wiki Generator]** Gọi `render_symbol_pages(repo_index_dict)`:
   - Với mỗi symbol có `fully_qualified_name` hợp lệ:
     a. Tính `safe_filename = fqn.replace('<','_').replace('>','_') + '.html'`.
     b. **[Jinja2]** Load template `symbol.html`.
     c. **[Jinja2]** Render với dữ liệu symbol (signature, docstring, annotations, modifiers).
     d. **[File System]** Ghi ra `wiki/symbols/<safe_filename>`.
6. **[Wiki Generator]** Gọi `generate_search_index(repo_index_dict)`:
   - Tạo list: các trang cố định (Dashboard, Tech, Architecture, Modules, Tests) + tất cả symbols FQN.
   - **[File System]** Ghi ra `wiki/search_index.json`.
7. **[Wiki Generator]** Gọi `generate_ai_context(repo_index_dict, analysis_result.model_dump())`:
   - Tạo context: repository_name, languages, symbols (với docstring, signature, annotations), sections, summaries.
   - **[File System]** Ghi ra `wiki/wiki_context.json`.
8. **Kết thúc.**

---

## AD-07: Luồng Người dùng Sử dụng Wiki — Tìm kiếm và Xem Symbol (UC-20, UC-21, UC-23)

**Tên biểu đồ:** Activity Diagram — Wiki User Navigation and Search
**Use Case tương ứng:** UC-20, UC-21, UC-23
**Mục đích:** Mô tả hành vi người dùng khi điều hướng, tìm kiếm và xem chi tiết symbol trong wiki.
**Swimlane:**
- **Wiki User:** Tương tác với giao diện
- **Browser (Client-side JS):** Xử lý tìm kiếm cục bộ

### Kịch bản:

1. **Bắt đầu.**
2. **[Wiki User]** Mở `wiki/index.html` trong trình duyệt.
3. **[Browser]** Hiển thị Dashboard với Bento Grid metrics (tổng số files, symbols, relationships).
4. **[Wiki User]** Quyết định: Muốn điều hướng bằng sidebar hay tìm kiếm?
   - **Sidebar:** Wiki User click vào module/container trong sidebar tree.
     - **[Browser]** Điều hướng đến trang tương ứng (`modules.html`, `tech.html`, v.v.).
   - **Tìm kiếm:**
     - **[Wiki User]** Nhập từ khóa vào live search bar.
     - **[Browser]** Nạp `search_index.json` (lần đầu tiên).
     - **[Browser]** Lọc kết quả theo từ khóa (client-side, không cần server).
     - **[Browser]** Hiển thị danh sách kết quả.
     - **[Wiki User]** Click vào kết quả.
     - **[Browser]** Điều hướng đến trang tương ứng (page hoặc `symbols/<fqn>.html`).
5. **[Wiki User]** Đang xem trang symbol detail (`symbols/<fqn>.html`):
   - **[Browser]** Hiển thị: tên symbol, kind, language, file_path, modifiers, annotations, docstring, signature.
6. **[Wiki User]** Quyết định: Muốn hỏi AI Widget?
   - **Có:** Chuyển sang AD-08 (AI Widget flow).
   - **Không:** Tiếp tục điều hướng hoặc kết thúc.
7. **Kết thúc.**
