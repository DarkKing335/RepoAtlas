# 04 — Kịch bản State Diagram: RepoAtlas

> **Môn học:** Phân tích và Thiết kế Hướng đối tượng (OOAD)

---

## Xác định Đối tượng có Vòng đời rõ ràng

Sau khi phân tích source code, các đối tượng nghiệp vụ sau có trạng thái và vòng đời rõ ràng:

| Đối tượng | Lý do chọn | File nguồn |
|---|---|---|
| **AnalysisSession** | Mỗi lần chạy `repoatlas analyze` là một phiên làm việc hoàn chỉnh với các trạng thái rõ ràng | `cli.py:run_analysis_pipeline()` |
| **ASTSymbolNode** | Ký hiệu AST được tạo, gắn parent, trở thành một phần của index, và được tóm tắt | `core_indexing/models.py:121` |
| **KnowledgeGraph** | Đồ thị tri thức có vòng đời từ khởi tạo → xây dựng → hợp lệ → ghi ra disk | `knowledge_graph/builder.py`, `knowledge_graph/models.py:74` |

---

## SD-01: Vòng đời của AnalysisSession

### Thông tin đối tượng

- **Tên đối tượng:** `AnalysisSession` (đại diện cho một lần thực thi `repoatlas analyze`)
- **Lý do chọn:** Mỗi lần gọi `run_analysis_pipeline()` là một phiên phân tích độc lập với các trạng thái rõ ràng từ khởi tạo đến hoàn tất. Các trạng thái này phản ánh trực tiếp các giai đoạn trong `cli.py:43-144`.
- **Trạng thái ban đầu:** `Idle` (trước khi nhập lệnh)
- **Trạng thái kết thúc:** `Completed` (thành công) hoặc `Failed` (thất bại)

### Danh sách trạng thái

| Trạng thái | Mô tả | Bằng chứng |
|---|---|---|
| `Idle` | Hệ thống chờ lệnh từ người dùng | Trạng thái ban đầu |
| `Validating` | Đang xác nhận đường dẫn/URL đầu vào | `cli.py:45-52` |
| `CloningRepository` | Đang clone repo từ Git URL (chỉ khi remote) | `scanner.py:89-111` |
| `Scanning` | Đang quét cấu trúc thư mục và parse AST | `cli.py:62-76` — Epic 1 |
| `Analyzing` | Đang thực hiện AI Analysis (chunking + summarization) | `cli.py:82-88` — Epic 3 |
| `BuildingGraph` | Đang xây dựng Knowledge Graph | `cli.py:93-96` — Epic 2 |
| `GeneratingWiki` | Đang render HTML pages | `cli.py:101-124` — Epic 4 |
| `Completed` | Pipeline hoàn tất thành công, wiki đã mở | `cli.py:127-139` |
| `Failed` | Pipeline thất bại tại một giai đoạn nào đó | `cli.py:141-144` |
| `CleaningUp` | Đang dọn dẹp tài nguyên tạm (temp dir) | `cli.py:141-144` (finally) |

### Bảng chuyển trạng thái

| Trạng thái hiện tại | Sự kiện | Điều kiện | Trạng thái tiếp theo | Hành động |
|---|---|---|---|---|
| `Idle` | `repoatlas analyze <args>` | Lệnh được nhận | `Validating` | Parse đối số |
| `Validating` | Xác nhận đầu vào | `_is_git_url()` = True | `CloningRepository` | Tạo temp dir |
| `Validating` | Xác nhận đầu vào | Path tồn tại và hợp lệ | `Scanning` | Khởi tạo RepositoryScanner |
| `Validating` | Đường dẫn không tồn tại | `not local_path.exists()` | `Failed` | In lỗi, sys.exit(1) |
| `CloningRepository` | Clone thành công | `git clone` exit code 0 | `Scanning` | Thiết lập repo_path |
| `CloningRepository` | Clone thất bại | `git clone` raise CalledProcessError | `CleaningUp` | Cleanup temp dir, báo lỗi |
| `Scanning` | Quét và parse hoàn tất | Không có exception | `Analyzing` | Ghi indexes/ artifacts |
| `Scanning` | Lỗi nghiêm trọng | Unhandled exception | `CleaningUp` | Cleanup, báo lỗi |
| `Analyzing` | AI Analysis hoàn tất | Không có exception | `BuildingGraph` | Ghi analysis/summaries.json |
| `Analyzing` | FileNotFoundError | `repository_index.json` thiếu | `CleaningUp` | Báo lỗi |
| `BuildingGraph` | Graph xây dựng hoàn tất | Validation thành công | `GeneratingWiki` | Ghi graphs/graph.json |
| `BuildingGraph` | Validation thất bại | Node IDs trùng hoặc edge thiếu | `CleaningUp` | Báo lỗi |
| `GeneratingWiki` | Wiki render hoàn tất | Tất cả file được ghi | `Completed` | Mở trình duyệt |
| `GeneratingWiki` | Lỗi IO | Không ghi được file | `CleaningUp` | Báo lỗi |
| `Completed` | Người dùng xem wiki | — | (Terminal) | Wiki hiển thị trong browser |
| `Failed` | Cleanup hoàn tất | — | (Terminal) | Thông báo thất bại |
| `CleaningUp` | Cleanup hoàn tất | — | `Failed` | Xóa temp dir |

### Chuyển trạng thái không hợp lệ / bị cấm

- Không thể chuyển từ `Scanning` trực tiếp sang `GeneratingWiki` (phải qua `Analyzing` và `BuildingGraph`).
- Không thể quay lại `Idle` sau khi đã bắt đầu (không có cơ chế restart trong session hiện tại).
- Không thể chuyển từ `Completed` sang bất kỳ trạng thái nào khác trong cùng một phiên.

---

## SD-02: Vòng đời của ASTSymbolNode

### Thông tin đối tượng

- **Tên đối tượng:** `ASTSymbolNode` (`core_indexing/models.py:121`)
- **Lý do chọn:** Đây là đơn vị cốt lõi của hệ thống — mỗi class, method, field được trích xuất từ AST. ASTSymbolNode trải qua các giai đoạn từ được phát hiện (raw parse) → được index → được tóm tắt → được render vào wiki.
- **Trạng thái ban đầu:** `Discovered` (khi parser tạo ra object từ AST node)
- **Trạng thái kết thúc:** `Rendered` (đã được render thành trang HTML)

### Danh sách trạng thái

| Trạng thái | Mô tả | Bằng chứng |
|---|---|---|
| `Discovered` | Parser vừa tạo `ASTSymbolNode` từ tree-sitter AST node | `scanner.py:206-215` — parser.parse() trả về |
| `Indexed` | Symbol đã được đưa vào `RepositoryIndex.symbols` | `indexer.py` — build_index() |
| `Chunked` | Đã được `Chunker` tạo `Chunk` (AST skeleton) cho prompt | `chunker.py:80-96` |
| `Summarized` | Đã có `SummaryNode` gắn với symbol này (via taxonomy) | `summarizer.py` — SummaryNode tạo |
| `Graphed` | Đã trở thành `GraphNode` trong KnowledgeGraph | `builder.py:156-168` |
| `Rendered` | Đã được render thành trang `symbols/<fqn>.html` | `renderer.py:38-62` |

### Bảng chuyển trạng thái

| Trạng thái hiện tại | Sự kiện | Điều kiện | Trạng thái tiếp theo | Hành động |
|---|---|---|---|---|
| `Discovered` | `RepositoryIndexer.build_index()` | Symbol hợp lệ với FQN | `Indexed` | Thêm vào index.symbols list |
| `Discovered` | Parse thất bại | Exception trong parser | (Bị loại bỏ) | Log lỗi, không tiến xa hơn |
| `Indexed` | `Chunker.chunk_for(node)` | Symbol nằm trong TaxonomyTree tại tier CLASS hoặc METHOD | `Chunked` | Tạo Chunk với AST skeleton |
| `Indexed` | `GraphBuilder._add_files_and_symbols()` | Symbol được thêm vào graph | `Graphed` | Tạo GraphNode |
| `Chunked` | `Summarizer.run()` hoàn tất cho nút này | LLM enabled hoặc null | `Summarized` | Tạo SummaryNode với summary text |
| `Summarized` | `GraphBuilder._attach_summaries()` | Summary được gán vào GraphNode.metadata | `Graphed` | GraphNode.metadata.summary được set |
| `Graphed` | `render_symbol_pages()` | Symbol có fully_qualified_name hợp lệ | `Rendered` | Ghi `symbols/<fqn>.html` |
| `Graphed` | `render_symbol_pages()` | Symbol không có FQN | (Bị bỏ qua) | `continue` trong `renderer.py:53` |

### Câu hỏi cần xác nhận

- Không phải mọi symbol đều đi qua `Chunked` → `Summarized`: Chỉ các symbol nằm trong TaxonomyTree (tier CLASS/METHOD) mới được chunk/summarize. Symbol ở tier thấp hơn (FIELD, PROPERTY) không được summarize riêng lẻ.

---

## SD-03: Vòng đời của KnowledgeGraph

### Thông tin đối tượng

- **Tên đối tượng:** `KnowledgeGraph` (`knowledge_graph/models.py:74`)
- **Lý do chọn:** `KnowledgeGraph` là artifact trung gian quan trọng nhất của hệ thống — nó được xây dựng từ từng bước, validated, và sau đó được persist sang disk. Có trạng thái "đang xây dựng" rõ ràng và trạng thái "hợp lệ" trước khi ghi.
- **Trạng thái ban đầu:** `Building` (khi `GraphBuilder.build()` bắt đầu)
- **Trạng thái kết thúc:** `Persisted` hoặc `Invalid`

### Danh sách trạng thái

| Trạng thái | Mô tả | Bằng chứng |
|---|---|---|
| `Building` | `GraphBuilder` đang thêm nodes và edges vào internal dict | `builder.py:92-131` |
| `PartiallyBuilt` | Repository node + file nodes + symbol nodes đã xong; taxonomy/summaries chưa | `builder.py:93-95` |
| `TaxonomyAttached` | Taxonomy nodes và summaries đã được gắn vào | `builder.py:97-99` |
| `ReadyForValidation` | `KnowledgeGraph` object đã được tạo từ sorted nodes/edges | `builder.py:122-130` |
| `Valid` | `model_validator` xác nhận node IDs unique và edge endpoints tồn tại | `models.py:83-94` |
| `Invalid` | Validation thất bại (duplicate IDs hoặc edge thiếu endpoint) | `models.py:86-93` |
| `Persisted` | `graph.json` đã được ghi ra disk thành công | `builder.py:334-360` |

### Bảng chuyển trạng thái

| Trạng thái hiện tại | Sự kiện | Điều kiện | Trạng thái tiếp theo | Hành động |
|---|---|---|---|---|
| `Building` | `_add_repository()` hoàn tất | — | `Building` | Thêm REPOSITORY node |
| `Building` | `_add_files_and_symbols()` hoàn tất | — | `PartiallyBuilt` | Thêm FILE + SYMBOL nodes + edges |
| `PartiallyBuilt` | `_add_analysis_taxonomy()` và `_attach_summaries()` hoàn tất | `analysis` không None | `TaxonomyAttached` | Taxonomy nodes + summaries gắn vào |
| `PartiallyBuilt` | `_add_overview_taxonomy()` hoàn tất | `analysis` là None, `overview` có | `TaxonomyAttached` | Structural taxonomy gắn vào |
| `TaxonomyAttached` | `KnowledgeGraph(...)` được khởi tạo | Pydantic model_validator chạy | `ReadyForValidation` | Tạo immutable KnowledgeGraph |
| `ReadyForValidation` | Validation thành công | Node IDs unique + edges hợp lệ | `Valid` | — |
| `ReadyForValidation` | Validation thất bại | Duplicate IDs hoặc thiếu endpoint | `Invalid` | Ném ValueError |
| `Valid` | `write_graph()` thành công | Temp file ghi OK và os.replace() OK | `Persisted` | `graph.json` trên disk |
| `Valid` | `write_graph()` thất bại | IOError hoặc OS Error | `Valid` (không persist) | Báo lỗi |
| `Invalid` | — | — | (Terminal) | Báo lỗi, pipeline dừng |
| `Persisted` | — | — | (Terminal) | graph.json sẵn sàng cho Wiki Gen |

### Ghi chú
- Trạng thái `Building` và `PartiallyBuilt` là internal state của `GraphBuilder`, không phải của `KnowledgeGraph` object trực tiếp. `KnowledgeGraph` object chỉ được tạo (và validate) một lần trong `builder.py:122`.
- Atomic write (`os.replace`) đảm bảo không bao giờ có `graph.json` corrupt trên disk.
