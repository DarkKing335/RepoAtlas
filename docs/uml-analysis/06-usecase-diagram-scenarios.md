# Kịch bản cho Biểu đồ Use Case — RepoAtlas

> **Môn học:** Phân tích và Thiết kế Hướng đối tượng (OOAD)
> Tài liệu này mô tả ngữ cảnh và lý do tồn tại của từng nhóm biểu đồ Use Case, viết theo dạng văn xuôi để người đọc nắm bắt bài toán trước khi xem biểu đồ.

---

## UC-00: Tổng quan hệ thống

Để hiểu tổng thể cách hệ thống RepoAtlas vận hành, cần xem xét toàn bộ các tác nhân và chức năng từ góc độ bao quát nhất. Hệ thống chỉ có hai loại người dùng trực tiếp: **kỹ sư phần mềm** — người khởi động quá trình phân tích thông qua dòng lệnh — và **người đọc wiki** — người sử dụng kết quả tài liệu đã sinh ra. Ngoài ra, hệ thống còn phụ thuộc vào ba hệ thống bên ngoài: máy chủ Git để clone repository từ xa, máy chủ Ollama để cung cấp khả năng tóm tắt bằng AI, và trình duyệt web để hiển thị tài liệu HTML. Đáng chú ý là quan hệ generalization giữa hai actor: kỹ sư phần mềm là trường hợp đặc biệt của người đọc wiki, vì sau khi phân tích xong họ cũng chính là người xem lại tài liệu vừa tạo ra. Biểu đồ tổng quan (uc-00-overview.puml) thể hiện toàn bộ mối quan hệ này, đồng thời làm rõ các chuỗi `<<include>>` giữa lệnh phân tích đầy đủ và từng bước con trong pipeline, cũng như quan hệ `<<extend>>` khi Ollama không khả dụng và hệ thống tự động chuyển sang chế độ cấu trúc thuần túy.

---

## UC-01: Nhóm chức năng Quét và Phân tích Mã nguồn (Epic 1)

Chức năng cốt lõi đầu tiên mà hệ thống cung cấp là khả năng đọc và hiểu mã nguồn Java hoặc C# mà không cần biên dịch hay chạy project đó. Kỹ sư phần mềm có thể cung cấp đường dẫn đến một thư mục dự án đang có sẵn trên máy, hoặc một URL Git trỏ đến repository từ xa — hệ thống sẽ tự xử lý việc clone về và dọn dẹp sau khi xong. Điều quan trọng là dù nguồn đầu vào là gì, toàn bộ việc phân tích cú pháp đều được thực hiện tại tầng AST (Abstract Syntax Tree), không phải đọc text thô hay regex. Với Java, parser nhận diện các class, interface, enum, record, annotation cùng toàn bộ thành viên của chúng — bao gồm Javadoc, annotation như `@Service` hay `@RestController`, kiểu dữ liệu của field và tham số của method. Với C#, logic tương tự áp dụng cho namespace, class, struct, interface, record, thuộc tính `[ApiController]` hay `[HttpGet]`, các property với accessor `{ get; set; }`, method bất đồng bộ và XML doc comment. Kết quả là một bảng chỉ mục ký hiệu thống nhất, ngôn ngữ bất khả tri, được lưu lại để tái sử dụng ở mọi bước tiếp theo trong pipeline mà không cần quét lại. Biểu đồ (uc-01-epic1-indexing.puml) mô tả rõ chuỗi `<<include>>` từ lệnh phân tích cục bộ và từ Git URL đến các bước quét thư mục, lưu cấu trúc, gọi từng parser, xây dựng chỉ mục và xuất file kết quả.

---

## UC-02: Nhóm chức năng AI Analysis, Knowledge Graph và Wiki Generation (Epic 2, 3, 4)

Sau khi có chỉ mục ký hiệu, hệ thống tiến vào ba nhóm chức năng tiếp theo có mối liên hệ chặt chẽ với nhau. **Nhóm AI Analysis** chịu trách nhiệm tổ chức các ký hiệu đã phân tích thành một cây phân cấp sáu tầng và lần lượt tóm tắt từng tầng theo chiều từ dưới lên, sử dụng một mô hình ngôn ngữ cục bộ (Ollama) hoặc thuần túy từ dữ liệu cấu trúc nếu không có LLM. Chức năng quan trọng nhất ở nhóm này là việc phân khúc code theo ranh giới AST — thay vì cắt theo số dòng, mỗi đoạn ngữ cảnh gửi cho LLM tương ứng đúng với một node trong cây AST, đảm bảo không bao giờ cắt ngang một method hay một class. **Nhóm Knowledge Graph** nhận kết quả từ hai nhóm trước và tổng hợp thành một đồ thị JSON duy nhất biểu diễn toàn bộ cấu trúc, quan hệ và tóm tắt của dự án. **Nhóm Wiki Generation** sử dụng đồ thị đó để render ra website HTML tĩnh với đầy đủ các trang: tổng quan, công nghệ, kiến trúc, modules, kiểm thử, và hàng trăm trang chi tiết cho từng class và method. Biểu đồ (uc-02-epics-ai-graph-wiki.puml) thể hiện đặc biệt rõ quan hệ `<<extend>>` giữa chế độ có LLM và không có LLM, vì đây là điểm phân kỳ nghiệp vụ quan trọng nhất trong toàn bộ pipeline.

---

## UC-03: Nhóm chức năng CLI Orchestration và Sử dụng Wiki (Epic 5 + Wiki Usage)

Toàn bộ chuỗi chức năng từ Epic 1 đến Epic 4 được bao bọc trong một lệnh duy nhất: `repoatlas analyze`. Kỹ sư phần mềm không cần biết pipeline gồm bao nhiêu bước hay thứ tự thực hiện — họ chỉ cần cung cấp đường dẫn và tùy chọn `--no-llm` nếu muốn chạy nhanh mà không dùng AI. Sau khi pipeline hoàn tất, trình duyệt tự động mở trang wiki để người dùng xem kết quả ngay lập tức. Ở phía người đọc wiki, hệ thống cung cấp ba cách tương tác chính: điều hướng qua cây sidebar để khám phá cấu trúc dự án, tìm kiếm ký hiệu cụ thể bằng thanh tìm kiếm hoạt động hoàn toàn phía client (không cần gọi server), và đặt câu hỏi trực tiếp trong giao diện chat AI được nhúng sẵn trong mọi trang wiki. Widget chat này kết hợp hai nguồn thông tin: tìm kiếm cục bộ từ `search_index.json` để xác định symbols liên quan, và gọi Ollama để sinh câu trả lời tự nhiên có kèm liên kết đến trang chi tiết tương ứng. Biểu đồ (uc-03-cli-wiki-usage.puml) làm nổi bật quan hệ generalization giữa hai actor và quan hệ `<<extend>>` trong luồng sử dụng widget AI.
