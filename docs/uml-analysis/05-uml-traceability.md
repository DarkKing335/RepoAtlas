# 05 — Bảng Liên kết (Traceability Matrix): RepoAtlas

> **Môn học:** Phân tích và Thiết kế Hướng đối tượng (OOAD)

---

## 1. Bảng Liên kết Use Case — Activity Diagram — State Diagram — File nguồn

| Use Case | Kịch bản Activity Diagram | Đối tượng State Diagram | File nguồn liên quan |
|---|---|---|---|
| UC-01 (Phân tích Repo Cục bộ) | AD-01 (Pipeline Đầy đủ), AD-03 (Parse Java) | SD-01 (AnalysisSession: Validating → Scanning), SD-02 (ASTSymbolNode: Discovered) | `scanner.py`, `cli.py` |
| UC-02 (Phân tích Repo Git URL) | AD-02 (Clone Git Repo) | SD-01 (AnalysisSession: Validating → CloningRepository → Scanning) | `scanner.py:89-118`, `cli.py:43-44` |
| UC-03 (Parse Java AST) | AD-03 (Parse Java Source File) | SD-02 (ASTSymbolNode: Discovered → Indexed) | `core_indexing/parsers/java_parser.py`, `scanner.py` |
| UC-04 (Parse C# AST) | AD-03 (thay thế cho C#) | SD-02 (ASTSymbolNode: Discovered → Indexed) | `core_indexing/parsers/csharp_parser.py`, `scanner.py` |
| UC-05 (Tóm tắt với LLM) | AD-04 (Bottom-Up AI Summarization) | SD-01 (AnalysisSession: Analyzing), SD-02 (ASTSymbolNode: Chunked → Summarized) | `ai_analysis/summarizer.py`, `ai_analysis/chunker.py`, `ai_analysis/llm/ollama.py` |
| UC-06 (Tóm tắt không LLM) | AD-04 (Bottom-Up, nhánh NullLLM) | SD-01 (AnalysisSession: Analyzing), SD-02 (ASTSymbolNode: Chunked → Summarized) | `ai_analysis/llm/null.py`, `ai_analysis/__main__.py:99-110` |
| UC-07 (AST Chunking 6 tầng) | AD-04 (bước 2-3: xây dựng taxonomy và chunk) | SD-02 (ASTSymbolNode: Indexed → Chunked) | `ai_analysis/chunker.py`, `ai_analysis/models.py` |
| UC-08 (Tạo Knowledge Graph) | AD-05 (Build Knowledge Graph) | SD-03 (KnowledgeGraph: Building → Persisted) | `knowledge_graph/builder.py`, `knowledge_graph/models.py` |
| UC-09 (Truy vấn Graph) | — (không có AD riêng) | SD-03 (KnowledgeGraph: Persisted) | `knowledge_graph/query.py` |
| UC-10 (Render Dashboard) | AD-06 (Render Wiki HTML, bước 4) | SD-01 (AnalysisSession: GeneratingWiki) | `wiki_generation/renderer.py:64-82`, `wiki_generation/templates/index.html` |
| UC-11 (Render Tech) | AD-06 (bước 3, key=tech) | SD-01 (AnalysisSession: GeneratingWiki) | `wiki_generation/renderer.py:20-36`, `wiki_generation/templates/tech.html` |
| UC-12 (Render Architecture) | AD-06 (bước 3, key=architecture) | SD-01 (AnalysisSession: GeneratingWiki) | `wiki_generation/renderer.py:20-36`, `wiki_generation/templates/architecture.html` |
| UC-13 (Render Modules) | AD-06 (bước 3, key=modules) | SD-01 (AnalysisSession: GeneratingWiki) | `wiki_generation/renderer.py:20-36`, `wiki_generation/templates/modules.html` |
| UC-14 (Render Tests) | AD-06 (bước 3, key=tests) | SD-01 (AnalysisSession: GeneratingWiki) | `wiki_generation/renderer.py:20-36`, `wiki_generation/templates/tests.html` |
| UC-15 (Render Symbol Pages) | AD-06 (bước 5) | SD-01 (AnalysisSession: GeneratingWiki), SD-02 (ASTSymbolNode: Graphed → Rendered) | `wiki_generation/renderer.py:38-62`, `wiki_generation/templates/symbol.html` |
| UC-16 (Tạo Search Index) | AD-06 (bước 6) | SD-01 (AnalysisSession: GeneratingWiki) | `wiki_generation/renderer.py:84-106` |
| UC-17 (Tạo AI Context) | AD-06 (bước 7) | SD-01 (AnalysisSession: GeneratingWiki) | `wiki_generation/renderer.py:122-182` |
| UC-18 (Pipeline Đầy đủ) | AD-01 (Toàn bộ Pipeline) | SD-01 (AnalysisSession: Idle → Completed/Failed) | `cli.py:43-144` |
| UC-19 (Cấu hình LLM) | AD-01 (bước 12: quyết định LLM mode) | SD-01 (AnalysisSession: Validating) | `cli.py:159-177`, `ai_analysis/__main__.py:93-113` |
| UC-20 (Điều hướng Sidebar) | AD-07 (Wiki Navigation, nhánh Sidebar) | — | `wiki_generation/templates/base.html` (JS sidebar) |
| UC-21 (Tìm kiếm Wiki) | AD-07 (Wiki Navigation, nhánh Search) | — | `wiki/search_index.json`, `wiki_generation/renderer.py:84-106` |
| UC-22 (Hỏi AI Widget) | — (AD riêng cần bổ sung) | — | `wiki_generation/renderer.py:122-182`, Ollama |
| UC-23 (Xem Chi tiết Symbol) | AD-07 (bước 5) | SD-02 (ASTSymbolNode: Rendered) | `wiki/symbols/<fqn>.html` |

---

## 2. Bảng Liên kết Use Case — User Story

| Use Case | User Story | Epic |
|---|---|---|
| UC-01, UC-02 | US-1.1 (Analyze a Repository) | Epic 1 |
| UC-01, UC-02 | US-1.2 (Save Repository Structure) | Epic 1 |
| UC-03 | US-1.3 (Java AST Parsing) | Epic 1 |
| UC-04 | US-1.4 (C# AST Parsing) | Epic 1 |
| UC-08 | US-2.1 (Generate a Knowledge Graph) | Epic 2 |
| UC-09 | US-2.2 (Query the Knowledge Graph) | Epic 2 |
| UC-08 | US-2.3 (Regenerate After Repository Changes) | Epic 2 |
| UC-05 | US-3.1 (Configure a Local LLM) | Epic 3 |
| UC-06 | US-3.2 (Run Without an LLM) | Epic 3 |
| UC-05 | US-3.3 (Generate Architecture Summaries) | Epic 3 |
| UC-05 | US-3.4 (Generate Module Summaries) | Epic 3 |
| UC-07 | US-3.5 (Hierarchical AST Chunking) | Epic 3 |
| UC-11 | US-4.1 (Generate Tech Documentation) | Epic 4 |
| UC-14 | US-4.2 (Generate Tests Documentation) | Epic 4 |
| UC-12 | US-4.3 (Generate Architecture Documentation) | Epic 4 |
| UC-13, UC-15 | US-4.4 (Generate Modules Documentation) | Epic 4 |
| UC-10, UC-16, UC-20, UC-21, UC-23 | US-4.5 (Render Interactive Static HTML Wiki) | Epic 4 |
| UC-22 | US-4.6 (Interactive Embedded Local AI Assistant Widget) | Epic 4 |
| UC-18 | US-5.1 (Execute the Complete Workflow) | Epic 5 |
| UC-19 | US-5.2 (Configure the LLM) | Epic 5 |

---

## 3. Bảng Liên kết Biểu đồ — File PlantUML

| Loại biểu đồ | Tên file PlantUML | Use Case | Activity/State |
|---|---|---|---|
| Use Case Diagram | `diagrams/uc-00-overview.puml` | Tất cả UC | — |
| Use Case Diagram | `diagrams/uc-01-epic1-indexing.puml` | UC-01, UC-02, UC-03, UC-04 | — |
| Use Case Diagram | `diagrams/uc-02-epic3-ai.puml` | UC-05, UC-06, UC-07 | — |
| Use Case Diagram | `diagrams/uc-03-epic2-graph.puml` | UC-08, UC-09 | — |
| Use Case Diagram | `diagrams/uc-04-epic4-wiki.puml` | UC-10, UC-11, UC-12, UC-13, UC-14, UC-15, UC-16, UC-17 | — |
| Use Case Diagram | `diagrams/uc-05-wiki-usage.puml` | UC-18, UC-19, UC-20, UC-21, UC-22, UC-23 | — |
| Activity Diagram | `diagrams/ad-01-full-pipeline.puml` | UC-18 | AD-01 |
| Activity Diagram | `diagrams/ad-02-git-clone.puml` | UC-02 | AD-02 |
| Activity Diagram | `diagrams/ad-03-java-parse.puml` | UC-03 | AD-03 |
| Activity Diagram | `diagrams/ad-04-ai-summarization.puml` | UC-05, UC-06 | AD-04 |
| Activity Diagram | `diagrams/ad-05-knowledge-graph.puml` | UC-08 | AD-05 |
| Activity Diagram | `diagrams/ad-06-wiki-render.puml` | UC-10 to UC-17 | AD-06 |
| Activity Diagram | `diagrams/ad-07-wiki-usage.puml` | UC-20, UC-21, UC-23 | AD-07 |
| State Diagram | `diagrams/sd-01-analysis-session.puml` | UC-18 | SD-01 |
| State Diagram | `diagrams/sd-02-ast-symbol-node.puml` | UC-03, UC-04, UC-05, UC-15 | SD-02 |
| State Diagram | `diagrams/sd-03-knowledge-graph.puml` | UC-08 | SD-03 |

---

## 4. Kiểm tra Tính nhất quán

### Checklist

- [x] Tất cả Use Case có actor và mục tiêu rõ ràng (xem `01-use-case-catalog.md`).
- [x] Tất cả Activity Diagram tương ứng với luồng chính hoặc thay thế của Use Case (xem `03-activity-scenarios.md`).
- [x] State Diagrams phản ánh vòng đời của đối tượng nghiệp vụ thực tế (xem `04-state-scenarios.md`).
- [x] Các trạng thái trong State Diagram có sự kiện chuyển trạng thái hợp lý.
- [x] Không có hai biểu đồ mô tả cùng một nghiệp vụ theo cách mâu thuẫn.
- [x] Không bỏ qua các chức năng quan trọng được xác nhận trong code (cleanup, fallback LLM, atomic write).
- [x] Không khẳng định dự án triển khai chức năng chưa xác nhận.

### Vấn đề đã phát hiện và ghi nhận

| Vấn đề | Loại | Mô tả |
|---|---|---|
| `knowledge_graph/query.py` | **Chưa xác định** | File tồn tại nhưng chưa được phân tích chi tiết trong tài liệu này. UC-09 được đặt ưu tiên thấp. |
| LLM timeout handling | **Suy luận** | OllamaClient có thể có timeout nhưng chưa tìm thấy bằng chứng cụ thể trong code đã đọc. |
| Widget AI offline capability | **Đã xác nhận** | Cần Ollama. Client-side chỉ là search_index.json, không phải fully offline AI. |
| Cache/incremental update | **Chưa xác định** | Không tìm thấy cơ chế cache. Mỗi lần chạy đều phân tích lại từ đầu. |
