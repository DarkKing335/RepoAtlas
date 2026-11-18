# KỊCH BẢN DEMO SẢN PHẨM — RepoAtlas

Xin chào mọi người. Trước khi bắt đầu, hãy thử đặt mình vào tình huống: chúng ta vừa nhận một project Java vài trăm file, nhưng gần như không có document.

Muốn hiểu project này có những module nào, class nào làm nhiệm vụ gì, các thành phần liên kết với nhau ra sao, chúng ta thường phải đọc source code thủ công. Và khi code thay đổi, document cũng rất dễ trở nên lỗi thời.

Đó chính là vấn đề mà RepoAtlas muốn giải quyết.

**RepoAtlas** là một CLI tool có thể tự động phân tích một repository, hiểu cấu trúc source code, sử dụng AI để tổng hợp thông tin và cuối cùng tạo ra một Wiki để developer có thể đọc và tra cứu project.

Trong phần demo hôm nay, chúng tôi sẽ sử dụng một project Spring Boot thực tế — Spring Petclinic — để đi qua toàn bộ quy trình đó.
**Bối cảnh:** giới thiệu sản phẩm cho khách hàng với tiêu chí "document về project".
**Demo repo:** `spring-petclinic` (Java Spring)
**Vai:** Người dẫn = Member 1 & Member 3 (trình bày phần đầu + Epic 1 + Epic 3). Member 2 & 4 trình bày phần của mình theo tiến trình liền mạch.

---

## PHẦN 1 — SPRINT GOAL (Người dẫn, ~1.5 phút)

**Mục tiêu sprint:**

> "Hoàn thiện phiên bản 1.0 của RepoAtlas — công cụ CLI tự động sinh tài liệu wiki cho một kho mã nguồn. Từ một đường dẫn local hoặc Git URL, hệ thống trích xuất cấu trúc bằng AST (Java/C#), tóm tắt bằng AI cục bộ, xây đồ thị tri thức và xuất bản website wiki tĩnh 4 nội dung (Tech, Tests, Architecture, Modules) — tất cả bằng **một lệnh duy nhất**, 289+ tests đạt."

**Thông điệp giá trị cho khách hàng:**

- Tiết kiệm thời gian onboarding repo (từ nhiều ngày → vài phút)
- Mã nguồn **luôn ở local**, không rò rỉ ra ngoài (local SLM mặc định)
- Không cần hosting/DB — sản phẩm chạy offline, output là trang HTML tĩnh mở được bằng `file://`

---

## PHẦN 2 — EPIC & USER STORY PO GIAO (Người dẫn, ~3 phút)

> Dùng bảng này lần lượt như một "ngân sách tính năng", nói đúng câu: **PO giao epic nào → giải quyết vấn đề gì → PR gồm những user story nào.** Chốt bằng câu phụ đề: "Các epic được thiết kế chạy đúng theo thứ tự pipeline, đầu ra của epic trước là đầu vào của epic sau."

| Epic                         | Trách nhiệm                    | US đã giao   | Giải quyết vấn đề                                             |
| ---------------------------- | ------------------------------ | ------------ | ------------------------------------------------------------- |
| **E1 — Repository Indexing** | Bằng (Core Indexing)           | US-1.1 → 1.4 | Hiểu repo khi chưa có bất kỳ tài liệu nào                     |
| **E2 — Knowledge Graph**     | Hoàng (Graph + Query)          | US-2.1 → 2.3 | Truy vấn quan hệ kế thừa/gọi/hợp thành mà không phân tích lại |
| **E3 — AI Analysis**         | Mẫn (Chunking + Summarization) | US-3.1 → 3.5 | AI tóm tắt chạy local + hoạt động được cả khi không có LLM    |
| **E4 — Wiki Generation**     | Duy (Rendering)                | US-4.1 → 4.5 | Chuyển kết quả thành tài liệu dễ đọc, tra cứu                 |
| **E5 — CLI Orchestration**   | Duy (Release/integration)      | US-5.1, 5.2  | Gói toàn bộ pipeline vào một lệnh duy nhất                    |

_Lưu ý: US-4.6 (AI Assistant widget) là "tính năng bổ sung trong E4/E3"._

---

## PHẦN 3 — KIẾN TRÚC BUSINESS MODULES (Người dẫn, ~2.5 phút)

> Nhấn mạnh: đây là **module nghiệp vụ** (giá trị khách hàng nhận được), không phải module kỹ thuật. Mô tả như một dây chuyền 5 công đoạn:

```
① Nạp kho  →  ② Thấu hiểu mã  →  ③ Tổng hợp AI  →  ④ Đồ thị tri thức  →  ⑤ Xuất bản Wiki
(Intake)    (AST Comprehension)  (AI Summarization)(Knowledge Graph)   (Wiki + AI Assistant)
```

| #                             | Business Module                                                                                                                                                                         | Khách hàng nhận được gì |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| ① **Nạp kho mã nguồn**        | Chấp nhận local path, Git URL, GitHub shorthand (`owner/repo`); tự clone repo về workspace tạm và dọn dẹp sạch sau phân tích                                                            |
| ② **Thấu hiểu mã nguồn**      | Đọc Java/C# bằng **AST parser** (tree-sitter) thay vì regex → trích xuất chính xác class, interface, method, annotation (`@RestController`, `[ApiController]`), Javadoc, call-graph     |
| ③ **Tổng hợp AI**             | Chunk code theo **6 tầng AST** (Repository → Module → Container → Component → Class → Method), local SLM (`qwen2.5-coder:3b`) tóm tắt từ dưới lên; **vẫn chạy được khi không có model** |
| ④ **Đồ thị tri thức**         | Lưu thực thể + quan hệ thành `graph.json` → truy vấn dependency khi repo thay đổi hoặc khi cần                                                                                          |
| ⑤ **Xuất bản & Tra cứu Wiki** | Sinh website tĩnh tương tác (Tech, Tests, Architecture, Modules, symbol detail) + tìm kiếm nhanh + AI chat widget — mở offline không cần server                                         |

**Câu chốt:** "Toàn bộ dây chuyền này khách hàng chỉ cần 1 lệnh; các bạn sẽ thấy trực tiếp ở cuối buổi."

---

## PHẦN 4 — DEMO TUẦN TỰ TỪNG EPIC

> **Chiến thuật demo:** Chạy **một lần `repoatlas analyze` thật** ở đầu (Epic 1), rồi mỗi epic sau trình bày bằng artifact tương ứng. Đảm bảo máy demo đã cài Python 3.10+, Ollama đang chạy model `qwen2.5-coder:3b`, và chạy thử full flow ít nhất 2 lần trước giờ demo (có sẵn `backend/wiki/` làm bản dự phòng để trình bày bằng file nếu Ollama lỗi).

---

### EPIC 1 — REPOSITORY INDEXING (MEMBER 1 — TRÌNH BÀY) — ~5 phút

**Lời giới thiệu:**

> "Epic đầu tiên giải quyết câu hỏi: _làm sao biết trong repo này có gì_ mà không cần đọc từng file. Tôi sẽ phân tích `spring-petclinic` — một repo Spring Boot thực tế nằm ngay trên máy demo."

**Demo — từng user story:**

| US                     | Thao tác trên màn hình                                                                                          | Điểm nhấn nói với khách                                                          |
| ---------------------- | --------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **US-1.1**             | Gõ `repoatlas analyze ./spring-petclinic` → show console log nhận dạng local repo, đếm file Java                | "Chấp nhận cả local path lẫn Git URL; nếu đưa remote nó tự clone và tự dọn dẹp"  |
| **US-1.2**             | Trỏ vào `indexes/structure.json` + `structure_overview.json`                                                    | "Cấu trúc repo được lưu lại để các giai đoạn sau dùng lại, không phải scan lại"  |
| **US-1.3**             | Mở `indexes/repository_index.json`, lọc ra `@RestController`, `@Service` trong petclinic                        | "Parser AST bắt đúng class, method, annotation, Javadoc — không phải quét regex" |
| **US-1.4**             | Nêu nhanh: cùng pipeline, thêm parser C# (`tree-sitter-c-sharp`) nắm namespace, property, `[HttpPost]`, XML doc | "Hỗ trợ song song Java và C# — mở rộng sang repo .NET"                           |
| **Bonus (call graph)** | Trỏ vào phần dependency/call-graph trong index                                                                  | "Kèm call-graph để biết file nào gọi file nào"                                   |

**Câu hỏi tiềm năng — chuẩn bị sẵn:**

- _"Parser hỗ trợ ngôn ngữ nào?"_ → Java & C# hiện tại; kiến trúc tree-sitter cho phép thêm ngôn ngữ mới.
- _"Repo rất lớn thì sao?"_ → Chunk theo tầng AST giữ token ≤ 2k/prompt (sẽ thấy ở Epic 3).

**Chuyển giao:** "Epic 1 giúp chúng ta biết repository có những gì. Nhưng biết từng entity riêng lẻ vẫn chưa đủ — chúng ta cần biết chúng liên kết với nhau như thế nào. Đây là phần Member 2 sẽ trình bày qua Knowledge Graph."

---

### EPIC 2 — KNOWLEDGE GRAPH (Member 2) — ~3.5 phút

**Bài trình bày (soạn sẵn cho member 2, đã chuẩn bị đầu vào):**

- **US-2.1:** Mở `graphs/graph.json` → show nodes (thực thể) + edges (kế thừa, gọi, hợp thành). Giới thiệu schema.
- **US-2.2:** Ví dụ truy vấn: _"class nào implement `Pet` / controller nào gọi `ClinicService`"_ → trả về dependency.
- **US-2.3:** Sửa 1 class → chạy lại phân tích → `graph.json` được tạo lại hoàn toàn, không lỗi thời.

**Câu chuyện giá trị:** "Không cần đọc cả repo, chỉ cần hỏi đồ thị là biết ai phụ thuộc ai — phục vụ review code, refactor, tác động thay đổi."

---

### EPIC 3 — AI ANALYSIS (MEMBER 3 — TRÌNH BÀY) — ~5 phút

**Lời giới thiệu:**

> "Epic này là 'bộ não' của sản phẩm: biến index khô khan thành mô tả tự nhiên, lại vẫn giữ mã nguồn ở local."

**Demo — từng user story:**

| US         | Thao tác/demo                                                                                  | Điểm nhấn                                                                                               |
| ---------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **US-3.1** | Điểm config trỏ về Ollama local (`qwen2.5-coder:3b`)                                           | "Model nhỏ 3B chạy ngay trên máy khách — mã nguồn không gửi ra ngoài"                                   |
| **US-3.2** | **Demo xoay:** tắt Ollama → chạy lại analysis → vẫn ra tài liệu (chỉ giảm độ mượt của mô tả)   | "Không phụ thuộc AI — không có LLM vẫn có tài liệu cấu trúc, tiến trình không dừng"                     |
| **US-3.3** | Mở summary của tầng Architecture (petclinic: Controller/Service/Repository/Persistence)        | "Hệ thống tự nhận diện lớp kiến trúc và mô tả"                                                          |
| **US-3.4** | Mở summary từng module (web, system, async...)                                                 | "Mỗi module được tóm tắt trách nhiệm tự động"                                                           |
| **US-3.5** | Nêu kỹ thuật 6 tầng AST: Repository→Module→Container→Component→Class→Method, tóm tắt bottom-up | "Chunk không cắt giữa dòng code, prompt dùng AST skeleton ngắn → ≤ 2.000 token, model 7B/8B xử lý được" |

**Câu hỏi tiềm năng — chuẩn bị:**

- _"Dùng model mạnh hơn được không?"_ → Được, kiến trúc model-agnostic: đổi config là dùng remote LLM.
- _"Chất lượng mô tả có ảo giác (hallucination) không?"_ → AST skeleton giới hạn ngữ cảnh theo đúng cấu trúc code, giảm bịa đặt.

**Chuyển giao:** "Summary này Member 2 dùng làm mô tả trong đồ thị, và Member 4 dùng để đổ vào trang wiki."

---

### EPIC 4 — WIKI GENERATION (Member 4) — ~5 phút

**Demo — mở từng trang trong `backend/wiki/` bằng trình duyệt (`file://`):**

- **US-4.1** `tech.html` → tech stack, cách build/run petclinic.
- **US-4.2** `tests.html` → liệt kê test suites + lệnh chạy.
- **US-4.3** `architecture.html` → các layer + sơ đồ quan hệ.
- **US-4.4** `modules.html` + bấm vào 1 class trong `symbols/` → trang detail có signature syntax-highlight.
- **US-4.5** Demo tương tác: sidebar tree, breadcrumb, live search (gõ `Pet` → kết quả), link chéo giữa symbol. Emphasize load <100ms, FOUT đã loại.
- **US-4.6** _(nếu demo):_ bấm widget "Ask Local AI", hỏi _"class nào xử lý appointment?"_ → streaming + link tới `symbols/`.

---

### EPIC 5 — CLI ORCHESTRATION (Member 4) — ~2.5 phút (khép màn)

- **US-5.1:** Chạy lại từ đầu `repoatlas analyze ./spring-petclinic` → show **toàn bộ pipeline** chạy trong 1 lệnh (scan → parse → chunk → summarize → graph → render). Đây là điểm "wow" để kết bài.
- **US-5.2:** Chốt các chế độ: local SLM (mặc định) / remote LLM / **không LLM** — khách chủ động theo yêu cầu bảo mật & chi phí.

**Kết bài (mọi người):**

> "Tóm lại: một lệnh, vài phút, bạn có một wiki hoàn chỉnh của bất kỳ repo Java/C# nào — chạy offline, mã không rời khỏi máy, và luôn cập nhật được khi code thay đổi. Xin cảm ơn, chúng tôi sẵn sàng nhận câu hỏi."

---

## PHẦN 5 — LEDGER ĐIỀU PHỐI (dành riêng người dẫn)

- **Thời lượng gợi ý:** tổng ~25 phút (P1:1.5 + P2:3 + P3:2.5 + E1:5 + E2:3.5 + E3:5 + E4:5 + E5:2.5) + 5 phút Q&A.
- **Người dẫn trình:** P1, P2, P3, Epic 1, Epic 3.
- **Checklist trước giờ demo:** Py3.10+ cài đặt, Ollama chạy `qwen2.5-coder:3b`, đã chạy thử full flow, backup `backend/wiki/` sẵn, demo chạy bằng repo **petclinic**.
- **Plan B:** Ollama lỗi → chuyển US-3.2 thành demo chính (no-LLM fallback vẫn ra tài liệu) — đây là tính năng, không phải trục trặc.
- **Cần thống nhất nội bộ:** US-4.6 (AI widget) ai trình; phân bổ thời gian Q&A cho từng epic.
