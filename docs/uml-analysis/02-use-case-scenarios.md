# 02 — Đặc tả Chi tiết Use Case: RepoAtlas

> **Môn học:** Phân tích và Thiết kế Hướng đối tượng (OOAD)

---

## UC-01: Phân tích Repository Cục bộ

- **Mục tiêu:** Quét cấu trúc thư mục, nhận diện và phân tích AST tất cả file Java/C# trong một repository cục bộ, sau đó lưu kết quả vào `indexes/`.
- **Actor chính:** Software Engineer (A1)
- **Actor phụ:** Không có
- **Mô tả:** Software Engineer cung cấp đường dẫn cục bộ đến một project Java hoặc C#. Hệ thống quét thư mục, nhận diện file nguồn, phân tích AST từng file, và xuất kết quả ra `indexes/repository_index.json`.
- **Tiền điều kiện:**
  - Đường dẫn local tồn tại và là thư mục hợp lệ.
  - Có ít nhất một file `.java` hoặc `.cs` trong project.
- **Kích hoạt:** Software Engineer chạy lệnh `repoatlas analyze <local_path>`.
- **Luồng chính (Main Flow):**
  1. CLI nhận đối số `path` và xác định đây là đường dẫn cục bộ (không phải Git URL).
  2. Hệ thống tạo `RepositoryScanner` với `target=local_path`.
  3. `RepositoryScanner.prepare_repository()` xác nhận đường dẫn tồn tại và là thư mục hợp lệ.
  4. `RepositoryScanner.scan_structure()` duyệt đệ quy thư mục, tạo `DirectoryNode` tree, tôn trọng `.gitignore` và `DEFAULT_EXCLUDES`.
  5. `RepositoryScanner.save_structure()` ghi `DirectoryNode` tree ra `indexes/structure.json`.
  6. `RepositoryScanner.scan_and_parse()` duyệt lại thư mục, với mỗi file `.java` gọi `JavaParser.parse()`, với mỗi file `.cs` gọi `CSharpParser.parse()`.
  7. Mỗi parser trả về `FileIndex` chứa danh sách `ASTSymbolNode`.
  8. `RepositoryIndexer.build_index()` tổng hợp tất cả `FileIndex` thành `RepositoryIndex`.
  9. `IRGenerator.generate_all()` ghi `repository_index.json` và `structure_overview.json` ra `indexes/`.
  10. Hệ thống trả về `RepositoryIndex` và danh sách `FileIndex` cho pipeline tiếp theo.
- **Luồng thay thế (Alternative Flow):**
  - **Alt 1a - Repo không có file nguồn được hỗ trợ:** Scan hoàn tất nhưng `file_indexes` rỗng. `RepositoryIndex` được tạo với danh sách symbols trống.
  - **Alt 1b - Một số file parse bị lỗi:** `scanner.py:217` bắt exception, log lỗi, bỏ qua file đó và tiếp tục với các file còn lại.
- **Luồng ngoại lệ (Exception Flow):**
  - **Exc 1a - Đường dẫn không tồn tại:** `scanner.py:114-115` ném `ValueError`, CLI in thông báo lỗi và thoát.
  - **Exc 1b - Lỗi đọc .gitignore:** `scanner.py:128` log cảnh báo và tiếp tục không có filter.
- **Hậu điều kiện thành công:** `indexes/repository_index.json` và `indexes/structure.json` được tạo, chứa toàn bộ ký hiệu AST đã được nhận diện.
- **Hậu điều kiện thất bại:** Pipeline dừng với thông báo lỗi, không có artifact nào được ghi.
- **Quy tắc nghiệp vụ liên quan:**
  - Chỉ nhận diện file `.java` và `.cs` — quy tắc trong `scanner.py:59-62`.
  - Bỏ qua các thư mục trong `DEFAULT_EXCLUDES` (`.git`, `node_modules`, `bin`, v.v.) — `scanner.py:33-36`.
  - Tôn trọng các luật trong `.gitignore` nếu file tồn tại — `scanner.py:120-129`.
- **Bằng chứng:** `backend/src/core_indexing/scanner.py`, `backend/src/cli.py:58-76`, `docs/user-stories.md` US-1.1, US-1.2.

---

## UC-02: Phân tích Repository từ Git URL

- **Mục tiêu:** Clone một remote Git repository vào thư mục tạm, phân tích, và dọn dẹp sau khi hoàn tất.
- **Actor chính:** Software Engineer (A1)
- **Actor phụ:** Git Remote Server (EX1)
- **Mô tả:** Khi người dùng cung cấp một URL Git (https, git@) hoặc GitHub shorthand (`owner/repo`), hệ thống tự động clone vào thư mục tạm, thực hiện phân tích như UC-01, rồi xóa thư mục tạm.
- **Tiền điều kiện:**
  - URL Git hợp lệ và repository công khai (hoặc người dùng có quyền truy cập).
  - Máy có kết nối internet và git được cài đặt.
- **Kích hoạt:** Software Engineer chạy `repoatlas analyze <git_url>` hoặc `repoatlas analyze owner/repo`.
- **Luồng chính (Main Flow):**
  1. CLI nhận đối số và gọi `RepositoryScanner._is_git_url()` để nhận diện đây là Git URL.
  2. `prepare_repository()` xây dựng URL đầy đủ (thêm `https://github.com/` nếu là shorthand).
  3. Hệ thống tạo thư mục tạm bằng `tempfile.mkdtemp(prefix="repoatlas_repo_")`.
  4. Chạy lệnh `git clone --depth 1 <url> <temp_dir>` để clone nhanh (chỉ 1 commit gần nhất).
  5. Đặt `self.repo_path = <temp_dir>` và tiến hành quét như UC-01 (bước 4-10).
  6. Sau khi toàn bộ pipeline hoàn tất, `scanner.cleanup()` xóa thư mục tạm.
- **Luồng thay thế:**
  - **Alt 2a - Owner/repo shorthand:** Hệ thống tự động ghép thành `https://github.com/<owner>/<repo>.git` trước khi clone.
- **Luồng ngoại lệ:**
  - **Exc 2a - Git clone thất bại:** `scanner.py:109-111` bắt `CalledProcessError`, gọi `cleanup()` và ném `ValueError` với thông báo lỗi từ git.
  - **Exc 2b - Mất kết nối mạng:** Được bắt qua `CalledProcessError` của subprocess git.
  - **Exc 2c - URL không hợp lệ hoặc repo private:** Git clone thất bại, hệ thống dọn temp dir và báo lỗi.
- **Hậu điều kiện thành công:** Phân tích hoàn tất, thư mục tạm đã được xóa, `indexes/` chứa đầy đủ artifact.
- **Hậu điều kiện thất bại:** Thư mục tạm được xóa (đảm bảo trong khối `finally`), không có artifact.
- **Quy tắc nghiệp vụ liên quan:**
  - Clone chỉ một commit (depth=1) để tiết kiệm băng thông và không gian.
  - Cleanup đảm bảo trong khối `finally` trong `cli.py:141-144`.
- **Bằng chứng:** `backend/src/core_indexing/scanner.py:89-118`, `backend/src/cli.py:43-44`, `docs/user-stories.md` US-1.1.

---

## UC-05: Tóm tắt Code bằng LLM Cục bộ (Ollama)

- **Mục tiêu:** Sử dụng Ollama LLM Server để tóm tắt từng ký hiệu AST theo phương pháp bottom-up hierarchical.
- **Actor chính:** Software Engineer (A1)
- **Actor phụ:** Ollama LLM Server (EX2)
- **Mô tả:** Hệ thống đọc `repository_index.json`, xây dựng cây taxonomy 6 tầng, chia mỗi nút thành chunk AST, gửi đến Ollama để tóm tắt theo thứ tự bottom-up (Method → Class → Component → Container → Module → Repository), và lưu kết quả vào `analysis/summaries.json`.
- **Tiền điều kiện:**
  - `indexes/repository_index.json` đã tồn tại.
  - Ollama server đang chạy tại `http://localhost:11434`.
  - Model `qwen2.5-coder:3b` (hoặc model được cấu hình) đã được pull vào Ollama.
- **Kích hoạt:** Bước 2 trong `run_analysis_pipeline()` với `use_llm=True`.
- **Luồng chính (Main Flow):**
  1. `build_llm()` tạo `OllamaClient` và gọi `health_check()` để xác nhận Ollama khả dụng.
  2. `load_repository_index()` nạp `repository_index.json`.
  3. `resolve_provider()` chọn taxonomy provider phù hợp (auto, index, hoặc heuristic).
  4. Provider xây dựng `TaxonomyTree` 6 tầng từ dữ liệu IR.
  5. `Chunker` được khởi tạo với `index` và `tree`.
  6. `Summarizer.run()` duyệt tất cả nút theo thứ tự `bottom_up()`.
  7. Với mỗi nút tầng METHOD hoặc CLASS: `Chunker.chunk_for()` tạo chunk từ AST skeleton.
  8. `Summarizer` xây dựng prompt với hệ thống context (tier, tên, skeleton).
  9. Nếu method có >= 5 dòng: đính kèm tool `read_source_range` để LLM có thể xem source đầy đủ.
  10. `OllamaClient.generate()` gọi Ollama API và nhận tóm tắt (có streaming).
  11. Summary được ghi nhận vào `SummaryNode` với `referenced_symbols` được grounded.
  12. Các tầng cao hơn (COMPONENT, CONTAINER, MODULE, REPOSITORY) nhận digest của child summaries.
  13. `ContentGenerator.generate_all()` tạo `content` (tech, tests, architecture, modules sections).
  14. `write_result()` ghi `AnalysisResult` ra `analysis/summaries.json`.
- **Luồng thay thế:**
  - **Alt 5a - Prompt vượt token budget:** `enforce_budget()` cắt bớt context trước khi gửi.
  - **Alt 5b - LLM không trả về JSON hợp lệ:** Summarizer fallback sang structural description.
- **Luồng ngoại lệ:**
  - **Exc 5a - Ollama không khả dụng tại thời điểm health_check:** Hệ thống tự động fallback sang UC-06 (NullLLMClient) với log cảnh báo.
  - **Exc 5b - Ollama timeout trong quá trình generate:** Tùy thuộc vào implementation của OllamaClient (cần xác nhận thêm).
- **Hậu điều kiện thành công:** `analysis/summaries.json` với AI-generated summaries cho mọi nút trong taxonomy.
- **Hậu điều kiện thất bại:** Fallback sang UC-06 hoặc pipeline dừng với lỗi IO.
- **Quy tắc nghiệp vụ liên quan:**
  - Token budget tối đa 2000 tokens/prompt — `cli.py:37`, `ai_analysis/__main__.py`.
  - Bottom-up: nút cha chỉ nhận summaries của con, không đọc raw source — `summarizer.py:1-30`.
  - Symbol grounding: chỉ reference FQNs thực sự tồn tại trong registry — `chunker.py:228-244`.
- **Bằng chứng:** `backend/src/ai_analysis/summarizer.py`, `backend/src/ai_analysis/chunker.py`, `backend/src/ai_analysis/__main__.py`, `docs/designs/hierarchical-prompting-chunking.md`.

---

## UC-06: Tóm tắt Code không có LLM (Structural Mode)

- **Mục tiêu:** Tạo tài liệu cấu trúc dựa trên AST metadata mà không cần LLM, đảm bảo pipeline hoàn tất ngay cả khi Ollama không khả dụng.
- **Actor chính:** Software Engineer (A1)
- **Actor phụ:** Không có
- **Mô tả:** Khi người dùng dùng `--no-llm` hoặc khi Ollama không khả dụng, hệ thống dùng `NullLLMClient` — không gọi bất kỳ API AI nào, chỉ tạo tài liệu từ AST metadata (tên, signature, docstring).
- **Tiền điều kiện:** `indexes/repository_index.json` đã tồn tại.
- **Kích hoạt:** Cờ `--no-llm` được đặt, hoặc Ollama health check thất bại.
- **Luồng chính (Main Flow):**
  1. `build_llm()` trả về `NullLLMClient` (do `--no-llm` hoặc Ollama không khả dụng).
  2. `NullLLMClient.enabled == False` — `Summarizer` bỏ qua bước gọi LLM.
  3. Với mỗi nút AST, `Summarizer` tạo structural summary từ metadata có sẵn (tên, tier, docstring).
  4. `ContentGenerator` tạo nội dung wiki từ structural summaries.
  5. `write_result()` ghi `summaries.json`.
- **Luồng thay thế:** Không có.
- **Luồng ngoại lệ:**
  - **Exc 6a - `repository_index.json` không tồn tại:** `load_repository_index()` ném `FileNotFoundError`.
- **Hậu điều kiện thành công:** `summaries.json` với structural-only descriptions.
- **Hậu điều kiện thất bại:** Pipeline dừng với lỗi FileNotFoundError.
- **Quy tắc nghiệp vụ liên quan:**
  - `NullLLMClient.enabled = False` — cờ này kiểm soát toàn bộ pipeline không gọi LLM.
  - Tài liệu structural vẫn đầy đủ cho wiki (không có AI-generated summaries).
- **Bằng chứng:** `backend/src/ai_analysis/llm/null.py`, `backend/src/ai_analysis/__main__.py:99-110`, `docs/user-stories.md` US-3.2.

---

## UC-08: Tạo Knowledge Graph

- **Mục tiêu:** Kết hợp Repository Index (IR) và AI Analysis summaries thành một đồ thị tri thức (Knowledge Graph) dạng JSON với nodes và edges mô tả cấu trúc và quan hệ giữa các thực thể code.
- **Actor chính:** Hệ thống (được gọi từ CLI pipeline)
- **Actor phụ:** Không có
- **Mô tả:** `GraphBuilder` đọc `repository_index.json` và `summaries.json`, tạo node cho mỗi file, ký hiệu và taxonomy entity, tạo edge cho mỗi quan hệ (contains, declares, extends, implements, calls), và ghi ra `graphs/graph.json`.
- **Tiền điều kiện:** `indexes/repository_index.json` và `analysis/summaries.json` đã tồn tại.
- **Kích hoạt:** Bước 3 trong `run_analysis_pipeline()`.
- **Luồng chính (Main Flow):**
  1. `build_from_paths()` nạp `repository_index.json` và `summaries.json`.
  2. `GraphBuilder.__init__()` xác nhận repository_name khớp giữa index và analysis.
  3. `GraphBuilder.build()` thêm node REPOSITORY gốc.
  4. `_add_files_and_symbols()` tạo GraphNode cho mỗi FileIndex và ASTSymbolNode, cùng edges "contains" và "declares".
  5. `_add_index_relationships()` tạo GraphEdge cho mỗi RelationshipEdge trong RepositoryIndex (extends, implements, calls, v.v.).
  6. `_add_analysis_taxonomy()` tạo nodes taxonomy từ TaxonomyTree (MODULE, CONTAINER, COMPONENT, CLASS).
  7. `_attach_summaries()` gán AI-generated summaries vào metadata của các GraphNode tương ứng.
  8. Kết quả được sắp xếp và đóng gói thành `KnowledgeGraph`.
  9. `write_graph()` ghi ra `graphs/graph.json` dùng atomic write (temp file → rename).
- **Luồng thay thế:**
  - **Alt 8a - Không có summaries (no-LLM mode):** `overview` từ `structure_overview.json` được dùng thay thế để xây taxonomy (`_add_overview_taxonomy()`).
  - **Alt 8b - Edge endpoint bị thiếu:** `_ensure_endpoint()` tạo EXTERNAL node giả cho symbol bên ngoài.
- **Luồng ngoại lệ:**
  - **Exc 8a - repository_name không khớp:** `GraphBuilder.__init__()` ném `ValueError`.
  - **Exc 8b - Node ID trùng lặp:** `KnowledgeGraph.validate_graph_integrity()` ném `ValueError`.
- **Hậu điều kiện thành công:** `graphs/graph.json` hợp lệ với unique node IDs và edges hợp lệ.
- **Hậu điều kiện thất bại:** Ghi thất bại, graph.json không được tạo.
- **Quy tắc nghiệp vụ liên quan:**
  - Atomic write: dùng temp file rồi `os.replace()` để tránh corrupt — `builder.py:334-360`.
  - Node ID phải unique — được validate bởi `KnowledgeGraph.validate_graph_integrity()`.
  - Edge endpoints phải tồn tại trong nodes — được validate bởi model_validator.
- **Bằng chứng:** `backend/src/knowledge_graph/builder.py`, `backend/src/knowledge_graph/models.py`.

---

## UC-18: Thực thi Pipeline Phân tích Đầy đủ

- **Mục tiêu:** Chạy toàn bộ workflow từ quét repo đến mở wiki trong trình duyệt chỉ bằng một lệnh CLI.
- **Actor chính:** Software Engineer (A1)
- **Actor phụ:** Git Remote Server (EX1, nếu là URL), Ollama LLM Server (EX2, nếu LLM bật), Web Browser (EX3)
- **Mô tả:** Đây là use case cấp cao nhất — điều phối tất cả các use case khác. Software Engineer chạy `repoatlas analyze <path|url>`, hệ thống lần lượt thực hiện Epic 1 → Epic 3 → Epic 2 → Epic 4, rồi tự động mở trình duyệt để xem kết quả.
- **Tiền điều kiện:**
  - Python 3.10+ được cài đặt.
  - `repoatlas` được cài qua `pip install -e ".[dev]"`.
  - Repo target tồn tại (local) hoặc có kết nối mạng (remote).
- **Kích hoạt:** Người dùng nhập `repoatlas analyze <path|url> [--no-llm]`.
- **Luồng chính (Main Flow):**
  1. `main()` parse đối số, xác định `path` và `use_llm`.
  2. `run_analysis_pipeline(path, use_llm)` được gọi.
  3. **[include UC-01 hoặc UC-02]** — Quét và phân tích repo, xuất `indexes/`.
  4. **[include UC-05 hoặc UC-06]** — AI Analysis, xuất `analysis/summaries.json`.
  5. **[include UC-08]** — Build Knowledge Graph, xuất `graphs/graph.json`.
  6. **[include UC-10 đến UC-17]** — Render toàn bộ trang wiki vào `wiki/`.
  7. Hệ thống xác định đường dẫn `wiki/index.html`.
  8. Trên Windows: `os.startfile(wiki_index_path)` mở file bằng trình duyệt mặc định.
  9. Trên Mac/Linux: `webbrowser.open(uri)`.
  10. `scanner.cleanup()` được gọi trong `finally` để xóa temp dir nếu có.
- **Luồng thay thế:**
  - **Alt 18a - Cờ `--no-llm` được dùng:** Bước 4 dùng UC-06 thay vì UC-05.
  - **Alt 18b - Không mở được trình duyệt:** Log cảnh báo `WARNING: Khong the tu dong bat trinh duyet...`, gợi ý người dùng mở thủ công.
- **Luồng ngoại lệ:**
  - **Exc 18a - Đường dẫn không hợp lệ:** CLI in `ERROR: Khong tim thay duong dan...` và `sys.exit(1)`.
  - **Exc 18b - Git clone thất bại:** Ném ValueError, pipeline dừng, temp dir được dọn.
  - **Exc 18c - Lỗi IO khi ghi file:** Bắt bởi khối try/finally, cleanup đảm bảo.
- **Hậu điều kiện thành công:** `wiki/` đầy đủ, trình duyệt mở `wiki/index.html`.
- **Hậu điều kiện thất bại:** Thông báo lỗi in ra console, temp dir được dọn sạch.
- **Quy tắc nghiệp vụ liên quan:**
  - Epic 3 (AI Analysis) chạy TRƯỚC Epic 2 (Knowledge Graph) vì Graph cần `summaries.json` — comment trong `cli.py:80`.
  - Cleanup luôn chạy trong `finally` bất kể thành công hay thất bại.
- **Bằng chứng:** `backend/src/cli.py:43-144`, `docs/user-stories.md` US-5.1, US-5.2.

---

## UC-22: Hỏi AI Widget về Codebase

- **Mục tiêu:** Người dùng đặt câu hỏi về kiến trúc, class, method của codebase qua chat widget trong wiki và nhận câu trả lời từ AI với symbol links.
- **Actor chính:** Wiki User (A2)
- **Actor phụ:** Ollama LLM Server (EX2)
- **Mô tả:** Widget "Ask Local AI" được nhúng trong mỗi trang HTML của wiki. Khi người dùng nhập câu hỏi, widget phân tích `search_index.json` cục bộ để tìm symbols liên quan, rồi gửi context + câu hỏi đến Ollama với streaming response.
- **Tiền điều kiện:**
  - `wiki/wiki_context.json` và `wiki/search_index.json` đã tồn tại.
  - Ollama đang chạy tại `http://localhost:11434`.
  - Người dùng đang xem wiki trong trình duyệt.
- **Kích hoạt:** Người dùng click vào "Ask Local AI" widget và nhập câu hỏi.
- **Luồng chính (Main Flow):**
  1. Người dùng click mở floating chat panel.
  2. Người dùng nhập câu hỏi (ví dụ: "Where is the UserService class?").
  3. Widget phân tích `search_index.json` cục bộ (client-side) để tìm symbols khớp.
  4. Widget gửi request đến Ollama với: context từ `wiki_context.json` + câu hỏi.
  5. Ollama streaming response được hiển thị real-time trong chat panel.
  6. Widget render symbol links có thể click được trong câu trả lời.
- **Luồng thay thế:**
  - **Alt 22a - Không tìm thấy symbol trong search_index:** Widget gửi câu hỏi không có symbol context.
- **Luồng ngoại lệ:**
  - **Exc 22a - Ollama không khả dụng:** Widget hiển thị thông báo lỗi kết nối.
- **Hậu điều kiện thành công:** Câu trả lời hiển thị trong chat panel với clickable symbol links.
- **Hậu điều kiện thất bại:** Thông báo lỗi trong chat panel.
- **Quy tắc nghiệp vụ liên quan:**
  - Hybrid search: client-side search_index.json + server-side LLM.
  - Real-time streaming response.
- **Bằng chứng:** `backend/src/wiki_generation/renderer.py:122-181`, `docs/user-stories.md` US-4.6, `docs/epics.md` Epic 4.
