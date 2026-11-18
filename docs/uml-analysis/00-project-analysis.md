# 00 — Phân tích Tổng quan Dự án: RepoAtlas

> **Môn học:** Phân tích và Thiết kế Hướng đối tượng (OOAD)
> **Vai trò phân tích:** Business Analyst, Software Architect
> **Ngày phân tích:** 2026-10-19

---

## 1. Giới thiệu Dự án

**RepoAtlas** là một công cụ CLI (Command-Line Interface) tự host (self-hostable), có khả năng phân tích mã nguồn phần mềm và tự động tạo ra một website tài liệu kỹ thuật tĩnh dạng HTML (interactive multi-page static HTML wiki). Hệ thống được xây dựng hoàn toàn bằng Python, không có backend server, không có cơ sở dữ liệu độc lập, và được thiết kế để chạy cục bộ trên máy người dùng.

**Nguồn bằng chứng:** `README.md`, `docs/architecture.md`, `backend/src/cli.py`

---

## 2. Phạm vi Khảo sát

| Thành phần | File nguồn | Trạng thái |
|---|---|---|
| CLI Orchestrator | `backend/src/cli.py` | **Đã xác nhận** |
| Core Indexing Engine | `backend/src/core_indexing/` | **Đã xác nhận** |
| Repository Scanner | `backend/src/core_indexing/scanner.py` | **Đã xác nhận** |
| IR Models (Pydantic) | `backend/src/core_indexing/models.py` | **Đã xác nhận** |
| Java Parser | `backend/src/core_indexing/parsers/java_parser.py` | **Đã xác nhận** (import trong scanner.py) |
| C# Parser | `backend/src/core_indexing/parsers/csharp_parser.py` | **Đã xác nhận** (import trong scanner.py) |
| AI Analysis Engine | `backend/src/ai_analysis/` | **Đã xác nhận** |
| Hierarchical Chunker | `backend/src/ai_analysis/chunker.py` | **Đã xác nhận** |
| Summarizer | `backend/src/ai_analysis/summarizer.py` | **Đã xác nhận** |
| LLM Client (Ollama) | `backend/src/ai_analysis/llm/ollama.py` | **Đã xác nhận** |
| LLM Client (Null) | `backend/src/ai_analysis/llm/null.py` | **Đã xác nhận** |
| Knowledge Graph Builder | `backend/src/knowledge_graph/builder.py` | **Đã xác nhận** |
| Knowledge Graph Models | `backend/src/knowledge_graph/models.py` | **Đã xác nhận** |
| Wiki Renderer | `backend/src/wiki_generation/renderer.py` | **Đã xác nhận** |
| Jinja2 HTML Templates | `backend/src/wiki_generation/templates/` | **Đã xác nhận** (referenced in renderer.py) |
| Test Suite (289 tests) | `backend/tests/` | **Đã xác nhận** |

---

## 3. Kiến trúc Tổng quan

Hệ thống hoạt động theo mô hình **pipeline một chiều (one-directional pipeline)** gồm 5 giai đoạn được điều phối bởi một lệnh CLI duy nhất:

```
[Người dùng nhập lệnh CLI]
         │
         ▼
[Epic 1: Core Indexing Engine]
   - RepositoryScanner: Quét cấu trúc thư mục, nhận diện file .java/.cs
   - JavaParser / CSharpParser: Phân tích AST, trích xuất ký hiệu
   - RepositoryIndexer: Xây dựng bảng ký hiệu và đồ thị phụ thuộc
   - IRGenerator: Xuất ra indexes/repository_index.json
         │
         ▼
[Epic 3: AI Analysis Engine]
   - Chunker: Chia nhỏ AST theo 6 tầng taxonomy
   - Summarizer: Tóm tắt bottom-up qua Ollama LLM (hoặc NullLLMClient)
   - ContentGenerator: Tạo nội dung wiki (tech, tests, arch, modules)
   - Xuất ra analysis/summaries.json
         │
         ▼
[Epic 2: Knowledge Graph]
   - GraphBuilder: Kết hợp IR + summaries -> graph.json
   - Xuất ra graphs/graph.json
         │
         ▼
[Epic 4: Wiki Generation]
   - renderer.py: Jinja2 render HTML pages từ graph + IR
   - Xuất ra wiki/ (index.html, tech.html, architecture.html, modules.html,
                      tests.html, symbols/*.html, search_index.json,
                      wiki_context.json)
         │
         ▼
[Kết quả: Trình duyệt tự động mở wiki/index.html]
```

**Nguồn bằng chứng:** `backend/src/cli.py` hàm `run_analysis_pipeline()`, `docs/architecture.md` mục 6.

---

## 4. Các Module Chính

| Module | Thư mục | Epic | Trách nhiệm |
|---|---|---|---|
| **Core Indexing** | `core_indexing/` | Epic 1 | Quét repo, phân tích AST Java/C#, xuất IR |
| **AI Analysis** | `ai_analysis/` | Epic 3 | Chunking phân cấp, tóm tắt LLM, tạo nội dung wiki |
| **Knowledge Graph** | `knowledge_graph/` | Epic 2 | Xây dựng đồ thị tri thức graph.json |
| **Wiki Generation** | `wiki_generation/` | Epic 4 | Render HTML tĩnh từ template Jinja2 |
| **CLI Orchestrator** | `cli.py` | Epic 5 | Điều phối toàn bộ pipeline qua một lệnh duy nhất |

---

## 5. Các Đối tượng Nghiệp vụ Quan trọng

| Đối tượng | Class/Model | Mô tả |
|---|---|---|
| `RepositoryIndex` | `core_indexing/models.py:288` | IR cấp cao nhất — bảng ký hiệu toàn bộ repo |
| `ASTSymbolNode` | `core_indexing/models.py:121` | Đơn vị ký hiệu AST (class, method, field...) |
| `FileIndex` | `core_indexing/models.py:234` | Metadata của một file nguồn |
| `TaxonomyTree` | `ai_analysis/models.py` | Cây phân loại 6 tầng AST |
| `SummaryNode` | `ai_analysis/models.py` | Kết quả tóm tắt của một nút trong taxonomy |
| `AnalysisResult` | `ai_analysis/models.py` | Kết quả tổng hợp của toàn bộ AI Analysis |
| `KnowledgeGraph` | `knowledge_graph/models.py:74` | Đồ thị tri thức với nodes + edges |
| `GraphNode` | `knowledge_graph/models.py:39` | Một nút trong knowledge graph |
| `GraphEdge` | `knowledge_graph/models.py:49` | Một cạnh (quan hệ) trong knowledge graph |

---

## 6. Các Actor trong Hệ thống

### Actor Nội bộ

| Actor | Mô tả | Nguồn bằng chứng |
|---|---|---|
| **Software Engineer / Developer** | Người dùng chính — chạy CLI để phân tích repo và xem tài liệu wiki | `docs/user-stories.md` (tất cả US) |
| **Wiki User** (đọc tài liệu) | Người dùng trang wiki tĩnh — sử dụng tìm kiếm, điều hướng, và hỏi AI Widget | `docs/user-stories.md` US-4.5, US-4.6 |

### Hệ thống Bên ngoài (External Systems)

| Hệ thống | Mô tả | Nguồn bằng chứng |
|---|---|---|
| **Git Remote Repository** | Nguồn repo được clone khi người dùng cung cấp URL | `core_indexing/scanner.py:89-111` |
| **Ollama LLM Server** | Máy chủ LLM cục bộ cung cấp tóm tắt AI | `ai_analysis/llm/ollama.py`, `ai_analysis/__main__.py:103` |
| **Target Repository** | Repository được phân tích (file .java, .cs cục bộ) | `core_indexing/scanner.py` |
| **Web Browser** | Trình duyệt mở file wiki/index.html sau khi tạo xong | `cli.py:133-137` |

---

## 7. Các File Artifact Được Sinh Ra

| Artifact | Vị trí | Mô tả |
|---|---|---|
| `structure.json` | `indexes/structure.json` | Cây thư mục repo |
| `repository_index.json` | `indexes/repository_index.json` | IR toàn bộ ký hiệu AST |
| `structure_overview.json` | `indexes/structure_overview.json` | Tổng quan cấu trúc 6 tầng |
| `summaries.json` | `analysis/summaries.json` | Kết quả AI tóm tắt theo taxonomy |
| `graph.json` | `graphs/graph.json` | Knowledge graph dạng JSON |
| `wiki/index.html` | `wiki/index.html` | Dashboard chính |
| `wiki/tech.html` | `wiki/tech.html` | Tài liệu technology stack |
| `wiki/architecture.html` | `wiki/architecture.html` | Tài liệu kiến trúc |
| `wiki/modules.html` | `wiki/modules.html` | Tài liệu modules |
| `wiki/tests.html` | `wiki/tests.html` | Tài liệu test suite |
| `wiki/symbols/*.html` | `wiki/symbols/` | Trang chi tiết từng ký hiệu AST |
| `wiki/search_index.json` | `wiki/search_index.json` | Index tìm kiếm phía client |
| `wiki/wiki_context.json` | `wiki/wiki_context.json` | Ngữ cảnh cho AI Widget |

---

## 8. Giới hạn và Giả định

### Giới hạn đã xác nhận
- Chỉ hỗ trợ Java (`.java`) và C# (`.cs`) — bằng chứng: `scanner.py:59-62` (parsers dict chỉ có `.java` và `.cs`).
- Không có web server, không có REST API, không có cơ sở dữ liệu — bằng chứng: `docs/architecture.md` mục 5.
- Không có giao diện người dùng tương tác trong quá trình phân tích (chỉ console logs) — bằng chứng: `cli.py`.
- Chỉ có một lệnh CLI duy nhất: `repoatlas analyze <path|url>` — bằng chứng: `cli.py:159`.

### Giới hạn của LLM
- Nếu Ollama không khả dụng, hệ thống tự động chuyển sang `NullLLMClient` — bằng chứng: `ai_analysis/__main__.py:104-110`.
- Token budget mặc định là 2000 tokens mỗi prompt — bằng chứng: `cli.py:37`, `ai_analysis/__main__.py`.

### Câu hỏi cần xác nhận
1. Có cơ chế cache để tránh phân tích lại khi repo không thay đổi không? (Chưa tìm thấy bằng chứng — có thể là **Suy luận**)
2. Widget "Ask Local AI" hoạt động hoàn toàn offline không hay cần kết nối Ollama? (Theo US-4.6, cần Ollama — **Đã xác nhận**)
3. Có hỗ trợ ngôn ngữ lập trình nào khác ngoài Java/C# không? (Chưa có bằng chứng — **Chưa xác định**)
