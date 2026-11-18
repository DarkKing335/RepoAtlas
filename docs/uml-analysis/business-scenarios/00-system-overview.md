# 00 — TỔNG QUAN HỆ THỐNG VÀ BÀI TOÁN NGHIỆP VỤ: REPOATLAS

> **Tài liệu:** Kịch bản Nghiệp vụ Tổng quan Hệ thống (System Business Overview Scenario)  
> **Chuyên môn:** Phân tích và Thiết kế Hướng đối tượng (OOAD) & Kiến trúc Phần mềm  
> **Dự án đối chiếu:** RepoAtlas (Automated AST-Grounded Repository Documentation Generator)  
> **Mục đích:** Cung cấp văn cảnh bài toán bằng văn xuôi sư phạm làm cơ sở đầu vào để xây dựng các mô hình UML (Use Case, Activity, State Machine Diagram).

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

## 1. Kịch bản Bài toán Tổng quan (Văn phong Đề bài OOAD)

Trong các tổ chức công nghệ và doanh nghiệp phát triển phần mềm quy mô lớn, kỹ sư phần mềm thường xuyên phải tiếp nhận, bảo trì hoặc tích hợp các kho mã nguồn (repository) khổng lồ được xây dựng qua nhiều thế hệ lập trình viên. Thực tế cho thấy, tài liệu kỹ thuật của hầu hết các dự án thường rơi vào tình trạng thiếu thốn, chắp vá hoặc nhanh chóng trở nên lỗi thời so với mã nguồn thực tế. Việc thiếu vắng tài liệu kiến trúc chuẩn xác khiến các kỹ sư mới mất hàng tuần, thậm chí hàng tháng chỉ để đọc từng dòng mã, tự vẽ sơ đồ tương tác và phỏng đoán cấu trúc hệ thống. Các công cụ tạo tài liệu truyền thống chỉ dừng lại ở việc trích xuất văn bản ghi chú thủ công gắn liền với hàm hoặc lớp (như Javadoc hay XML Comments), hoàn toàn bất lực trong việc tổng hợp bức tranh toàn cảnh về kiến trúc đa tầng, mối quan hệ phụ thuộc giữa các thành phần và luồng dữ liệu cốt lõi của toàn bộ giải pháp phần mềm.

Nhằm giải quyết triệt để rào cản trên, một nhóm kỹ sư kiến trúc quyết định xây dựng **RepoAtlas** — một hệ thống tự động phân tích mã nguồn phần mềm chuyên sâu và sinh bộ tài liệu kỹ thuật tương tác đa trang dưới dạng trang thông tin điện tử tĩnh (Static Wiki). Hệ thống hướng đến phục vụ hai nhóm đối tượng người dùng chính: **Kỹ sư vận hành hệ thống** (Software Engineer) — người trực tiếp ra lệnh phân tích dự án thông qua giao diện dòng lệnh, và **Người đọc tài liệu kỹ thuật** (Wiki User / Solution Architect / QA Engineer) — những người khai thác, tra cứu và nghiên cứu kho tri thức dự án thông qua giao diện trình duyệt trực quan. Do chính kỹ sư vận hành sau khi tạo xong tài liệu cũng sẽ trở thành người đọc tài liệu, giữa hai vai trò này tồn tại mối quan hệ kế thừa và mở rộng quyền năng tự nhiên trong mô hình người dùng.

Để khởi động quá trình lập tài liệu, kỹ sư vận hành chỉ cần cung cấp địa chỉ của kho mã nguồn mục tiêu. Hệ thống hỗ trợ xử lý linh hoạt cả các thư mục dự án đang lưu trữ cục bộ trên máy tính lẫn các kho mã nguồn từ xa lưu trữ trên máy chủ Git thông qua giao thức truyền tải trực tuyến hoặc định danh rút gọn. Nếu đầu vào là một kho mã nguồn từ xa, hệ thống sẽ tự động khởi tạo một không gian làm việc an toàn, tiến hành tải bản sao tinh gọn của mã nguồn về đĩa cục bộ, thực hiện phân tích và cam kết dọn dẹp triệt để dữ liệu tạm thời ngay khi phiên làm việc kết thúc, bảo đảm không làm rò rỉ dữ liệu hoặc chiếm dụng bộ nhớ của máy trạm.

Quy trình phân tích mã nguồn được tổ chức theo đường ống xử lý một chiều tuần tự, phân tách nghiêm ngặt thành các giai đoạn nghiệp vụ độc lập nhưng kết nối chặt chẽ. Đầu tiên, hệ thống duyệt quét toàn bộ cấu trúc thư mục của dự án, tự động loại trừ các tệp tin rác, thư mục thư viện phụ thuộc và áp dụng triệt để các quy tắc bỏ qua đặc thù của dự án. Tiếp theo, thay vì đọc chuỗi ký tự thô hay sử dụng các mẫu tìm kiếm biểu thức chính quy dễ sai sót, hệ thống sử dụng các bộ phân tích cú pháp chuyên biệt theo từng ngôn ngữ lập trình (hỗ trợ nền tảng Java và C#) để mổ xẻ cây cú pháp trừu tượng (Abstract Syntax Tree - AST). Quá trình này giúp nhận diện chính xác từng thực thể trong mã nguồn như gói không gian tên, lớp, giao diện, bảng liệt kê, cấu trúc dữ liệu, hàm xử lý, thuộc tính, trường dữ liệu, chú thích định danh kiến trúc đặc thù, cùng mạng lưới quan hệ đa chiều như kế thừa, cài đặt giao diện, lời gọi hàm và truy cập trường dữ liệu.

Sau khi đã hoàn tất lập chỉ mục ký hiệu cú pháp, dữ liệu được chuyển giao cho phân hệ phân tích phân cấp và tóm tắt thông minh. Hệ thống tự động phân loại cấu trúc mã nguồn theo một cây phân cấp sáu tầng chặt chẽ — từ cấp độ toàn bộ kho mã nguồn, xuống các phân hệ lớn, đơn vị triển khai phần mềm độc lập, nhóm thành phần chức năng, lớp cụ thể, và kết thúc ở từng phương thức chi tiết. Tại đây, hệ thống cho phép kỹ sư vận hành linh hoạt lựa chọn: kích hoạt trợ lý trí tuệ nhân tạo cục bộ để sinh tóm tắt ngôn ngữ tự nhiên từ dưới lên theo từng tầng phân cấp với sự quản lý nghiêm ngặt về giới hạn dung lượng từ ngữ (ngân sách token), hoặc tự động hạ cấp an toàn sang chế độ tóm tắt cấu trúc xác định nếu máy chủ mô hình ngôn ngữ không khả dụng. Toàn bộ thông tin cấu trúc, mạng lưới phụ thuộc và nội dung tóm tắt sau đó được hội tụ vào một **Đồ thị Tri thức** (Knowledge Graph) duy nhất, được thẩm định tính toàn vẹn đa thực thể và lưu trữ nguyên tử xuống ổ đĩa.

Tại giai đoạn hoàn tất, hệ thống chuyển hóa đồ thị tri thức và chỉ mục cú pháp thành một bộ trang web tài liệu tĩnh đa trang hoàn chỉnh và chuyên nghiệp. Bộ tài liệu bao gồm: Bảng điều khiển trung tâm hiển thị các chỉ số định lượng của dự án, Trang thông tin ngăn xếp công nghệ, Trang kiến trúc đa tầng, Trang phân rã các phân hệ và đơn vị triển khai, Trang hướng dẫn kiểm thử tự động, cùng hàng loạt trang hồ sơ chi tiết cho từng lớp và hàm nghiệp vụ. Đồng thời, hệ thống tự động khởi tạo một chỉ mục tìm kiếm ngoại tuyến siêu tốc và một tệp ngữ cảnh mở rộng, phục vụ tiện ích Trợ lý AI Cục bộ nhúng trực tiếp trên giao diện wiki. Tiện ích này cho phép người đọc đặt câu hỏi tự nhiên về dự án, tra cứu vị trí mã nguồn, nhận câu trả lời kèm siêu liên kết chính xác đến trang hồ sơ của ký hiệu mà không đòi hỏi bất kỳ dịch vụ máy chủ đám mây hay kết nối Internet nào.

Toàn bộ giải pháp hoạt động theo nguyên lý tự vận hành cục bộ (local-first, self-contained), bảo mật tuyệt đối mã nguồn độc quyền của doanh nghiệp, loại bỏ hoàn toàn chi phí bản quyền điện toán đám mây và mang lại tốc độ phản hồi tức thì cho người dùng.

---

## 2. Các Thành phần Nghiệp vụ Trọng tâm Suy luận cho Thiết kế Hướng đối tượng

Dựa trên kịch bản bài toán tổng quan, các chuyên gia phân tích và thiết kế hướng đối tượng (OOAD) có thể xác định ngay các trục kiến trúc nền tảng:

1. **Ranh giới Hệ thống (System Boundary):**  
   Hệ thống ứng dụng máy trạm tự trị không máy chủ web nền (Serverless / Daemonless CLI tool), nhận đầu vào là mã nguồn dự án và sản sinh đầu ra là gói tài liệu HTML tĩnh chạy trực tiếp trên trình duyệt máy trạm.
2. **Các Tác nhân Hệ thống (Actors):**  
   - *Tác nhân người dùng:* Kỹ sư phần mềm (Software Engineer - điều phối CLI), Người đọc Wiki (Wiki User - tra cứu web). Kỹ sư phần mềm kế thừa toàn bộ hành vi của Người đọc Wiki.  
   - *Tác nhân hệ thống ngoài:* Máy chủ kho Git từ xa (Git Remote Server), Máy chủ suy luận AI cục bộ (Ollama LLM Server), Trình duyệt Web và Hệ điều hành máy trạm (Web Browser / Host OS).
3. **Các Luồng Xử lý Chính (Business Workflows):**  
   - Quét mã nguồn và lập chỉ mục cú pháp AST (Core Indexing).  
   - Phân khúc và tóm tắt đa tầng từ dưới lên có kiểm soát ngân sách (Hierarchical Summarization).  
   - Xây dựng, thẩm định và lưu trữ Đồ thị Tri thức nguyên tử (Knowledge Graph Construction).  
   - Biên dịch gói giao diện tĩnh và phục vụ tra cứu ngoại tuyến (Static Wiki Generation & Client Search).
4. **Các Thực thể có Trạng thái Nghiệp vụ Rõ rệt (Stateful Business Entities):**  
   - Phiên phân tích dự án (`AnalysisSession`).  
   - Không gian làm việc Git tạm thời (`GitCloneWorkspace`).  
   - Ký hiệu cú pháp mã nguồn (`ASTSymbolNode`).  
   - Đồ thị tri thức dự án (`KnowledgeGraph`).  
   - Phiên tương tác hỏi đáp của Trợ lý AI trên Wiki (`AskAIWidgetSession`).

---

## 3. Căn cứ Phân tích từ Dự án Thực tế

| Yếu tố nghiệp vụ trong kịch bản | Bằng chứng source code / tài liệu dự án | Trạng thái xác minh |
|---|---|---|
| Mô hình CLI tự trị, không máy chủ backend | `backend/src/cli.py:43-145`, `docs/architecture.md:Section 5` | **Đã xác nhận** |
| Hỗ trợ 2 ngôn ngữ Java và C# qua parser AST | `backend/src/core_indexing/scanner.py:59-62`, `backend/src/core_indexing/parsers/` | **Đã xác nhận** |
| Nhận diện đường dẫn cục bộ hoặc URL Git từ xa | `backend/src/core_indexing/scanner.py:70-87`, `backend/src/core_indexing/scanner.py:89-118` | **Đã xác nhận** |
| Phân cấp 6 tầng (`Repository` -> `Method`) | `backend/src/ai_analysis/models.py:25-53`, `docs/designs/hierarchical-prompting-chunking.md` | **Đã xác nhận** |
| Cơ chế chuyển đổi dự phòng sang cấu trúc khi mất Ollama | `backend/src/ai_analysis/__main__.py:93-113`, `backend/src/ai_analysis/llm/null.py` | **Đã xác nhận** |
| Đồ thị tri thức lưu trữ nguyên tử qua file tạm | `backend/src/knowledge_graph/builder.py:334-360` | **Đã xác nhận** |
| Sinh 5 trang chuyên đề + hàng trăm trang symbol | `backend/src/wiki_generation/renderer.py:20-83`, `backend/src/cli.py:104-124` | **Đã xác nhận** |
| Widget AI nhúng streaming + tìm kiếm fallback | `backend/src/wiki_generation/templates/base.html:310-604` | **Đã xác nhận** |
