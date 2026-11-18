# 03 — KỊCH BẢN BIỂU ĐỒ TRẠNG THÁI (STATE MACHINE DIAGRAM SCENARIOS)

> **Tài liệu:** Kịch bản Vòng đời và Chuyển trạng thái Đối tượng (State Machine Scenarios Specification)  
> **Chuyên môn:** Phân tích và Thiết kế Hướng đối tượng (OOAD) & Kiến trúc Phần mềm  
> **Dự án đối chiếu:** RepoAtlas (Automated AST-Grounded Repository Documentation Generator)  
> **Mục tiêu:** Nhận diện và đặc tả chính xác các đối tượng nghiệp vụ có vòng đời thực sự trong hệ thống, phân tích các sự kiện kích hoạt, điều kiện bảo vệ (guard conditions), hành động và bảng chuyển trạng thái làm căn cứ trực tiếp để vẽ State Machine Diagram.

---

## I. NGUYÊN TẮC XÁC ĐỊNH ĐỐI TƯỢNG CÓ TRẠNG THÁI

Trong phân tích hướng đối tượng (OOAD), không phải mọi thực thể dữ liệu (Entity) đều cần biểu diễn bằng biểu đồ trạng thái. Các đối tượng chỉ mang tính chất cấu trúc tĩnh hoặc dữ liệu chuyển giao (DTO/Value Object) như `DirectoryNode`, `SourceRange`, hay `ImportInfo` chỉ được khởi tạo và đọc giá trị mà không trải qua các giai đoạn biến đổi hành vi.

Dựa trên việc rà soát toàn bộ source code của dự án RepoAtlas, chúng tôi xác định được **5 đối tượng nghiệp vụ cốt lõi** có vòng đời đầy đủ, có các trạng thái phân biệt rõ ràng và có sự kiện chuyển tiếp được bảo chứng bởi mã nguồn:
1. **`AnalysisSession` (Phiên làm việc Phân tích Repository):** Quản lý toàn bộ tiến trình thực thi của một lần chạy lệnh `repoatlas analyze`.
2. **`GitCloneWorkspace` (Không gian Làm việc Git Tạm thời):** Quản lý vòng đời tài nguyên đĩa từ cấp phát, được sử dụng, đến thu hồi an toàn.
3. **`ASTSymbolNode` (Ký hiệu Cú pháp Mã nguồn):** Quản lý vòng đời của một thành phần mã nguồn từ trích xuất thô trong AST đến khi thành trang tài liệu web tĩnh.
4. **`KnowledgeGraph` (Đồ thị Tri thức Dự án):** Quản lý quá trình tích lũy thực thể, gắn kết tóm tắt, thẩm định toàn vẹn và ghi đĩa nguyên tử.
5. **`AskAIWidgetSession` (Phiên Tương tác Trợ lý AI trên Wiki):** Quản lý chu trình hội thoại thời gian thực, xếp hạng ngữ cảnh và cơ chế chuyển đổi dự phòng phía trình duyệt.

---

## II. ĐẶC TẢ CHI TIẾT VÒNG ĐỜI VÀ TRẠNG THÁI TỪNG ĐỐI TƯỢNG

---

### ĐỐI TƯỢNG 1: PHIÊN LÀM VIỆC PHÂN TÍCH (`AnalysisSession`)

#### 1. Tên đối tượng và mục đích quản lý
- **Tên đối tượng:** `AnalysisSession` (Phiên phân tích Repository).
- **Mục đích quản lý:** Đại diện cho một lần thực thi trọn vẹn của đường ống phân tích từ khi nhận lệnh từ người dùng tại giao diện dòng lệnh cho đến khi hoàn tất hoặc gặp sự cố dừng lại. Quản lý trạng thái chuyển giao giữa 4 phân hệ lớn và bảo đảm thu hồi tài nguyên tạm thời.

#### 2. Vòng đời tổng quát và cách tạo ra
Phiên làm việc được tạo ra ngay khi hàm `run_analysis_pipeline(target_path, use_llm)` trong `cli.py` được triệu gọi. Nó bắt đầu ở trạng thái chờ lệnh, chuyển sang xác thực tham số, qua các pha quét mã nguồn, phân tích AI, xây dựng đồ thị, sinh wiki và kết thúc bằng việc mở trình duyệt hiển thị kết quả. Dù thành công hay thất bại, phiên luôn kết thúc sau khi đã thực hiện dọn dẹp tài nguyên.

#### 3. Danh sách tất cả trạng thái nghiệp vụ đã xác nhận
| Tên trạng thái | Phân loại | Ý nghĩa nghiệp vụ | Bằng chứng mã nguồn |
|---|:---:|---|---|
| `Idle` | Khởi tạo | Hệ thống đang chờ người dùng kích hoạt lệnh phân tích | Trước khi gọi `run_analysis_pipeline` |
| `Validating` | Trung gian | Đang thẩm định đường dẫn cục bộ hoặc nhận diện định dạng URL Git | `cli.py:44-52` |
| `CloningRepository` | Trung gian | Đang tải bản sao nông của repository từ máy chủ Git từ xa vào thư mục tạm | `scanner.py:89-111` |
| `Scanning` | Trung gian | Đang quét thư mục, lọc bỏ tệp rác và phân tích AST các ngôn ngữ Java/C# | `cli.py:62-76` (Epic 1) |
| `Analyzing` | Trung gian | Đang phân khúc 6 tầng và sinh tóm tắt thông qua Ollama hoặc chế độ cấu trúc | `cli.py:82-88` (Epic 3) |
| `BuildingGraph` | Trung gian | Đang hợp nhất tri thức, bù trừ nút ngoại vi và thẩm định toàn vẹn đồ thị | `cli.py:93-96` (Epic 2) |
| `GeneratingWiki` | Trung gian | Đang kết xuất các trang chuyên đề HTML, trang ký hiệu, chỉ mục tìm kiếm và ngữ cảnh AI | `cli.py:101-125` (Epic 4) |
| `CleaningUp` | Trung gian | Khối kết thúc bắt buộc (`finally`) đang thực thi thu hồi tài nguyên tạm | `cli.py:141-144` |
| `Completed` | Kết thúc (Success) | Phân tích hoàn tất thành công, trình duyệt web mặc định đã mở trang Dashboard | `cli.py:127-139` |
| `Failed` | Kết thúc (Failure) | Phân tích thất bại tại một khâu nào đó, lỗi đã được thông báo ra terminal | `cli.py:48-49`, `finally block` |

#### 4. Câu chuyện vòng đời (Lifecycle Narrative)
Khi kỹ sư phần mềm gõ lệnh phân tích, một `AnalysisSession` thức dậy từ trạng thái `Idle` và bước vào `Validating`. Hệ thống kiểm tra xem địa chỉ là đường dẫn máy tính hay kho Git từ xa. Nếu là đường dẫn cục bộ không tồn tại, phiên chuyển thẳng sang `Failed`. Nếu là địa chỉ Git hợp lệ, phiên chuyển sang `CloningRepository` để tải mã nguồn về đĩa; nếu mất mạng hoặc sai địa chỉ, phiên chuyển sang `CleaningUp` rồi kết thúc ở `Failed`. Khi đã có mã nguồn sẵn sàng trên đĩa, phiên chuyển qua tuần tự 4 pha: `Scanning` (quét AST), `Analyzing` (tóm tắt AI), `BuildingGraph` (dựng đồ thị) và `GeneratingWiki` (sinh HTML). Nếu bất kỳ giai đoạn nào phát sinh ngoại lệ không thể xử lý, phiên lập tức bị kéo vào trạng thái `CleaningUp` để dọn dẹp trước khi chuyển sang `Failed`. Khi toàn bộ các trang HTML được ghi thành công, hệ thống tự động kích hoạt trình duyệt và phiên đạt trạng thái `Completed`. Khối dọn dẹp `CleaningUp` luôn được thực thi trước khi phiên kết thúc hoàn toàn.

#### 5. Bảng chuyển trạng thái (State Transition Table)
Quy ước: `hasError` = đã có lỗi ở giai đoạn trước.

| Trạng thái hiện tại | Sự kiện kích hoạt | Điều kiện bảo vệ [guard] | Trạng thái tiếp theo | Hành động /action |
|---|---|---|---|---|
| Initial | Khởi tạo phiên | — | `Idle` | — |
| `Idle` | Nhập lệnh `repoatlas analyze` | Tham số được tiếp nhận | `Validating` | Phân tích đối số CLI |
| `Validating` | Thẩm định địa chỉ | `_is_git_url(target) == True` | `CloningRepository` | Tạo thư mục tạm, chuẩn bị clone |
| `Validating` | Thẩm định địa chỉ | thư mục cục bộ tồn tại | `Scanning` | Khởi tạo `RepositoryScanner` |
| `Validating` | Thẩm định địa chỉ | thư mục cục bộ không tồn tại | `Failed` | In `Khong tim thay duong dan`, `sys.exit(1)` |
| `CloningRepository` | Tải Git hoàn tất | exit code = 0 | `Scanning` | Gán `repo_path` trỏ về thư mục tạm |
| `CloningRepository` | Tải Git thất bại | `CalledProcessError` | `CleaningUp` | Bắt lỗi, `hasError = true` |
| `Scanning` | Quét & parse xong | Tạo xong `RepositoryIndex` | `Analyzing` | Ghi `indexes/` |
| `Scanning` | Lỗi nghiêm trọng | Ngoại lệ chưa bắt | `CleaningUp` | Ghi log, `hasError = true` |
| `Analyzing` | Tóm tắt xong | Tạo xong `AnalysisResult` | `BuildingGraph` | Ghi `analysis/summaries.json` |
| `Analyzing` | Lỗi | `FileNotFoundError` hoặc ngoại lệ khác | `CleaningUp` | Báo lỗi, `hasError = true` |
| `BuildingGraph` | Đồ thị hợp lệ & đã ghi | Thẩm định đạt | `GeneratingWiki` | Ghi nguyên tử `graphs/graph.json` |
| `BuildingGraph` | Thẩm định / ghi đĩa lỗi | Trùng ID, cạnh mồ côi hoặc I/O lỗi | `CleaningUp` | Ném `ValueError`, `hasError = true` |
| `GeneratingWiki` | Render xong tất cả tệp | 5 trang + symbols + 2 JSON đã ghi | `CleaningUp` | In SUCCESS, mở trình duyệt |
| `GeneratingWiki` | Lỗi ghi đĩa / template | Ngoại lệ I/O hoặc Jinja2 | `CleaningUp` | Ghi lỗi, `hasError = true` |
| `CloningRepository`, `Scanning`, `Analyzing`, `BuildingGraph`, `GeneratingWiki` | Ctrl+C | `KeyboardInterrupt` | `CleaningUp` | `hasError = true` |
| `CleaningUp` | Dọn dẹp xong | `hasError == false` | `Completed` | Dashboard đã mở |
| `CleaningUp` | Dọn dẹp xong | `hasError == true` | `Failed` | In thông báo thất bại |
| `Completed` | — | — | Final | (không nhãn) |
| `Failed` | — | — | Final | (không nhãn) |

> **Mẹo cho người vẽ SD-01:** Gộp 5 trạng thái `CloningRepository`…`GeneratingWiki` vào một composite state, rồi vẽ một mũi tên `KeyboardInterrupt` từ composite sang `CleaningUp`.

#### 6. Chuyển trạng thái không hợp lệ / bị cấm
- Không nhảy từ `Scanning` thẳng sang `GeneratingWiki` (bỏ qua `Analyzing` và `BuildingGraph`).
- Không quay lại `Idle`/khởi động lại phiên từ `Failed` trong cùng một lần chạy.
- Không chuyển sang `Failed` hoặc `Completed` mà không qua `CleaningUp`, **trừ** `Validating → Failed` (chưa có tài nguyên tạm cần dọn).

#### 7. Căn cứ phân tích
- Code: `backend/src/cli.py:43-145` (hàm `run_analysis_pipeline`), `scanner.py:89-118`.
- Trạng thái xác minh: **Đã xác nhận đầy đủ trong mã nguồn**.

---

### ĐỐI TƯỢNG 2: KHÔNG GIAN LÀM VIỆC GIT TẠM THỜI (`GitCloneWorkspace`)

#### 1. Tên đối tượng và mục đích quản lý
- **Tên đối tượng:** `GitCloneWorkspace` (Không gian Làm việc Tạm thời cho Kho Git).
- **Mục đích quản lý:** Quản lý vòng đời của thư mục làm việc tạm thời trên ổ đĩa máy trạm khi người dùng yêu cầu phân tích một repository từ xa qua mạng.

#### 2. Vòng đời tổng quát và cách tạo ra
Được tạo ra bởi `RepositoryScanner.prepare_repository()` thông qua hàm `tempfile.mkdtemp(prefix="repoatlas_repo_")`. Đối tượng trải qua quá trình cấp phát, nhận dữ liệu clone, được sử dụng để các bộ phân tích AST đọc mã nguồn, và cuối cùng được giải phóng sạch sẽ qua lệnh xóa đệ quy `shutil.rmtree`.

#### 3. Danh sách trạng thái nghiệp vụ đã xác nhận
| Tên trạng thái | Phân loại | Ý nghĩa nghiệp vụ | Bằng chứng mã nguồn |
|---|:---:|---|---|
| `Unallocated` | Khởi tạo | Thư mục tạm chưa được cấp phát trên ổ đĩa (`_temp_dir is None`) | `scanner.py:65` |
| `Allocating` | Trung gian | Đang yêu cầu hệ điều hành cấp phát định danh thư mục tạm | `scanner.py:100` |
| `Cloning` | Trung gian | Thư mục đã tạo, đang tiếp nhận luồng tải dữ liệu từ lệnh `git clone` | `scanner.py:102-107` |
| `InUse` | Trung gian | Tải xong, thư mục đang được sử dụng bởi các bộ đọc AST | `scanner.py:108`, `cli.py:64` |
| `Releasing` | Trung gian | Tiến trình phân tích hoàn tất hoặc bị lỗi, bắt đầu quy trình dọn dẹp | `scanner.py:221-225` |
| `Purged` | Kết thúc (Success) | Toàn bộ thư mục và tệp con đã bị xóa sạch khỏi đĩa cứng | `scanner.py:224-225` |
| `FailedAllocation`| Kết thúc (Failure) | Cấp phát hoặc clone thất bại, tài nguyên tạm đã được thu hồi ngay lập tức | `scanner.py:110` |

#### 4. Câu chuyện vòng đời
Khi người dùng cung cấp một URL Git, không gian làm việc xuất phát từ `Unallocated`. Hệ thống chuyển sang `Allocating` để xin hệ điều hành một thư mục rỗng với tiền tố `repoatlas_repo_`. Sau khi có thư mục, nó chuyển sang `Cloning` để tiếp nhận dữ liệu từ lệnh `git clone --depth 1`. Nếu lệnh clone bị lỗi (ví dụ mất kết nối mạng), không gian làm việc chuyển ngay sang `Releasing` để xóa thư mục vừa tạo và kết thúc ở `FailedAllocation`. Nếu clone thành công, đối tượng chuyển sang `InUse` — trong suốt giai đoạn này, các bộ parser AST và scanner liên tục đọc các tệp tin bên trong thư mục. Khi toàn bộ đường ống kết thúc (hoặc xảy ra ngoại lệ tại các khâu sau), khối `finally` triệu gọi hàm `cleanup()`, đưa không gian làm việc vào `Releasing` để thực thi xóa đệ quy toàn bộ dữ liệu, và kết thúc ở trạng thái `Purged`.

#### 5. Bảng chuyển trạng thái
Quy ước: `cloneFailed` = lệnh clone đã thất bại.

| Trạng thái hiện tại | Sự kiện kích hoạt | Điều kiện bảo vệ | Trạng thái tiếp theo | Hành động |
|---|---|---|---|---|
| Initial | Khởi tạo | — | `Unallocated` | — |
| `Unallocated` | Phát hiện URL Git | `is_remote == True` | `Allocating` | Gọi `tempfile.mkdtemp` |
| `Allocating` | Cấp phát thành công | Thư mục vật lý được tạo | `Cloning` | `git clone --depth 1` |
| `Allocating` | Cấp phát thất bại | `mkdtemp` ném lỗi | `FailedAllocation` | Báo lỗi (chưa có gì để xóa) |
| `Cloning` | Clone thành công | Exit code = 0 | `InUse` | `self.repo_path = temp_dir` |
| `Cloning` | Clone thất bại hoặc Ctrl+C | `CalledProcessError` / `KeyboardInterrupt` | `Releasing` | `cloneFailed = true` (nếu lỗi clone) |
| `InUse` | Pipeline kết thúc hoặc lỗi | gọi `scanner.cleanup()` | `Releasing` | Xóa đệ quy |
| `Releasing` | Xóa xong | `cloneFailed == false` | `Purged` | `_temp_dir = None` |
| `Releasing` | Xóa xong | `cloneFailed == true` | `FailedAllocation` | Ném `ValueError` báo lỗi clone ra CLI |
| `Purged` | — | — | Final | (không nhãn) |
| `FailedAllocation` | — | — | Final | (không nhãn) |

> **Ghi chú cho người vẽ:** Với đường dẫn cục bộ, đối tượng này không được tạo, không vẽ.

#### 6. Chuyển trạng thái không hợp lệ / bị cấm
- Không xóa thư mục tạm khi tiến trình `git clone` còn đang ghi dữ liệu (chỉ xóa sau khi lệnh Git đã kết thúc/ngắt).
- Không chuyển sang `InUse` khi clone trả mã lỗi khác 0.
- Không tái sử dụng workspace đã `Purged`.

#### 7. Căn cứ phân tích
- Code: `backend/src/core_indexing/scanner.py:100-111`, `scanner.py:221-226`.
- Trạng thái xác minh: **Đã xác nhận đầy đủ trong mã nguồn**.

---

### ĐỐI TƯỢNG 3: KÝ HIỆU CÚ PHÁP MÃ NGUỒN (`ASTSymbolNode`)

#### 1. Tên đối tượng và mục đích quản lý
- **Tên đối tượng:** `ASTSymbolNode` (Ký hiệu cú pháp trích xuất từ cây AST).
- **Mục đích quản lý:** Đại diện cho một đơn vị mã nguồn độc lập (Lớp, Giao diện, Hàm, Trường dữ liệu, Thuộc tính). Quản lý chu trình chuyển hóa từ lúc được parser phát hiện trong AST đến khi trở thành trang tài liệu HTML hiển thị trước người dùng.

#### 2. Vòng đời tổng quát và cách tạo ra
Được sinh ra bởi các parser ngôn ngữ (`JavaParser` hoặc `CSharpParser`) khi duyệt qua các nút định nghĩa kiểu dữ liệu và thành viên trong cây cú pháp AST. Nó trải qua việc định danh, lập chỉ mục toàn cục, trích xuất khung xương, gắn tóm tắt, tích hợp vào đồ thị và kết xuất ra tệp HTML độc lập.

#### 3. Danh sách trạng thái nghiệp vụ đã xác nhận
| Tên trạng thái | Phân loại | Ý nghĩa nghiệp vụ | Bằng chứng mã nguồn |
|---|:---:|---|---|
| `Discovered` | Khởi tạo | Vừa được parser trích xuất từ cây cú pháp AST, chứa thông tin kỹ thuật thô | `scanner.py:210-215` |
| `Indexed` | Trung gian | Đã được chuẩn hóa FQN và đưa vào danh sách chỉ mục toàn dự án `RepositoryIndex.symbols` | `indexer.py:20-50` |
| `Chunked` | Trung gian | Đã được trích xuất khung xương cú pháp AST (loại bỏ thân hàm) để làm prompt AI | `chunker.py:80-96` |
| `Summarized` | Trung gian | Đã được gắn kèm đoạn văn bản tóm tắt chức năng (do AI sinh hoặc cấu trúc tạo) | `summarizer.py:120-150` |
| `Graphed` | Trung gian | Đã trở thành một nút `GraphNode` liên kết mạng lưới quan hệ trong Knowledge Graph | `builder.py:156-168` |
| `Rendered` | Kết thúc (Success) | Đã được Jinja2 biên dịch thành trang tài liệu `wiki/symbols/<safe_filename>.html` | `renderer.py:38-63` |
| `Discarded` | Kết thúc (Failure) | Bị loại bỏ do thiếu hoặc không hợp lệ tên định danh (FQN) | `scanner.py:217`, `renderer.py:52` |

#### 4. Câu chuyện vòng đời
Khi bộ phân tích AST đọc một tệp .java/.cs, mỗi ký hiệu trích xuất được ra đời ở Discovered. Khi tổng hợp chỉ mục, nếu tên định danh (FQN) hợp lệ thì ký hiệu sang Indexed; nếu FQN thiếu hoặc không hợp lệ thì sang Discarded. (Lỗi parse một tệp xảy ra trước khi ký hiệu được tạo, nên tệp đó trả chỉ mục rỗng và không có ký hiệu nào để loại.) Tại đây, nếu ký hiệu là kiểu dữ liệu hoặc hàm quan trọng (CLASS hoặc METHOD), phân hệ AI chọn nó để chuyển sang Chunked, trích xuất khung xương chữ ký và gửi đến Ollama để nhận lại đoạn tóm tắt, đưa ký hiệu sang Summarized, rồi nạp vào Knowledge Graph ở trạng thái Graphed. Các ký hiệu còn lại (không phải CLASS/METHOD như FIELD, thuộc tính...) đi thẳng từ Indexed sang Graphed. Cuối cùng, phân hệ Wiki Renderer duyệt qua ký hiệu, kiểm tra tính hợp lệ của tên định danh, chuẩn hóa tên tệp an toàn và kết xuất thành một trang HTML độc lập, đưa ký hiệu đạt trạng thái kết thúc hoàn mỹ `Rendered`.

#### 5. Bảng chuyển trạng thái
| Trạng thái hiện tại | Sự kiện kích hoạt | Điều kiện bảo vệ | Trạng thái tiếp theo | Hành động |
|---|---|---|---|---|
| Initial | Parser trích xuất ký hiệu | — | `Discovered` | — |
| `Discovered` | Tổng hợp chỉ mục | FQN hợp lệ | `Indexed` | Thêm vào `RepositoryIndex.symbols` |
| `Discovered` | Tổng hợp chỉ mục | FQN thiếu/không hợp lệ | `Discarded` | Bỏ qua, ghi log cảnh báo |
| `Indexed` | Phân đoạn theo taxonomy | Thuộc tầng `CLASS` hoặc `METHOD` | `Chunked` | Trích xuất khung xương AST |
| `Indexed` | Không có tóm tắt riêng | [còn lại: không phải CLASS/METHOD] | `Graphed` | Nạp thẳng vào đồ thị |
| `Chunked` | Sinh tóm tắt xong | Nhận phản hồi LLM hoặc cấu trúc | `Summarized` | Tạo `SummaryNode` |
| `Summarized` | Nạp vào Knowledge Graph | Tạo nút đồ thị | `Graphed` | `GraphNode(id="symbol:<fqn>")` |
| `Graphed` | Kết xuất trang | Có `fully_qualified_name` | `Rendered` | Ghi `wiki/symbols/<safe_filename>.html` |
| `Rendered` | — | — | Final | (không nhãn) |
| `Discarded` | — | — | Final | (không nhãn) |

> **Ghi chú:** lỗi parse một tệp xảy ra **trước** khi ký hiệu được tạo (tệp đó trả chỉ mục rỗng), nên không vẽ chuyển tiếp "lỗi parse → Discarded" cho ký hiệu. Việc renderer kiểm tra lại FQN (`renderer.py:52`) chỉ là phòng vệ bổ sung, không vẽ.

#### 6. Chuyển trạng thái không hợp lệ / bị cấm
- Không render trực tiếp từ `Discovered`/`Chunked`/`Summarized` mà chưa qua `Graphed`.
- `FIELD` không bao giờ vào `Chunked`.

#### 7. Căn cứ phân tích
- Code: `backend/src/core_indexing/models.py:121-160`, `backend/src/ai_analysis/chunker.py:80-96`, `backend/src/wiki_generation/renderer.py:38-63`.
- Trạng thái xác minh: **Đã xác nhận đầy đủ trong mã nguồn**.

---

### ĐỐI TƯỢNG 4: ĐỒ THỊ TRI THỨC DỰ ÁN (`KnowledgeGraph`)

#### 1. Tên đối tượng và mục đích quản lý
- **Tên đối tượng:** `KnowledgeGraph` (Kho Đồ thị Tri thức Đa thực thể).
- **Mục đích quản lý:** Đóng vai trò kho dữ liệu trung gian chuẩn hóa duy nhất của hệ thống, hội tụ toàn bộ thông tin cấu trúc, mạng lưới quan hệ đa chiều và văn bản tóm tắt phân cấp trước khi chuyển hóa thành website.

#### 2. Vòng đời tổng quát và cách tạo ra
Được khởi tạo bởi lớp `GraphBuilder` trong `knowledge_graph/builder.py`. Đối tượng bắt đầu rỗng, lần lượt tiếp nhận các nút lõi, các cạnh phụ thuộc, gắn nội dung tóm tắt, trải qua quy trình thẩm định tính toàn vẹn đa thực thể nghiêm ngặt và lưu trữ nguyên tử ra tệp `graphs/graph.json`.

#### 3. Danh sách trạng thái nghiệp vụ đã xác nhận
| Tên trạng thái | Phân loại | Ý nghĩa nghiệp vụ | Bằng chứng mã nguồn |
|---|:---:|---|---|
| `Initialized` | Khởi tạo | Đối tượng đồ thị rỗng vừa được tạo trong bộ nhớ | `builder.py:67-87` |
| `PopulatingCore` | Trung gian | Đang thêm các nút đại diện cho repository, tệp tin và ký hiệu cú pháp | `builder.py:93-94` |
| `LinkingEdges` | Trung gian | Đang nạp các quan hệ phụ thuộc, nối cạnh và bù trừ nút ngoại vi `EXTERNAL` | `builder.py:95`, `builder.py:270-320` |
| `AttachingSummaries` | Trung gian | Đang gắn kết các văn bản tóm tắt phân cấp vào metadata của từng nút | `builder.py:97-100` |
| `ValidatingIntegrity`| Trung gian | Đang chạy hàm kiểm tra toàn vẹn (trùng ID nút, cạnh mồ côi) | `models.py:83-95` |
| `PersistingAtomic` | Trung gian | Thẩm định đạt chuẩn, đang ghi dữ liệu vào tệp tạm `.graph.tmp` | `builder.py:344-355` |
| `Committed` | Kết thúc (Success) | Tệp tạm đã được hoán đổi nguyên tử thành `graphs/graph.json` | `builder.py:356` |
| `ValidationFailed`| Kết thúc (Failure) | Thẩm định thất bại (trùng ID hoặc cạnh mồ côi), ném ngoại lệ, dừng pipeline | `models.py:87, 91` |
| `WriteFailed` | Kết thúc (Failure) | Lỗi I/O khi đang ghi tệp tạm, xóa tệp tạm trong finally | `builder.py:358-359` |

#### 4. Câu chuyện vòng đời
Khi phân hệ Knowledge Graph khởi động, một `KnowledgeGraph` mới được sinh ra ở trạng thái `Initialized`. Hệ thống bắt đầu chuyển nó sang `PopulatingCore` để nạp các thực thể vật lý (kho lưu trữ, tệp nguồn, ký hiệu cú pháp, phân cấp taxonomy). Tiếp đó, đồ thị chuyển sang `LinkingEdges` để quét qua toàn bộ quan hệ (kế thừa, gọi hàm, cài đặt). Nếu phát hiện quan hệ trỏ đến một lớp ngoài dự án, đồ thị tự động tạo nút `EXTERNAL` để bảo đảm mọi cạnh đều có hai đầu mút hợp lệ. Sau đó, nó chuyển sang `AttachingSummaries` để nạp các khối văn bản tóm tắt từ AI. Khi dữ liệu đã đầy đủ, đồ thị bước vào cửa ải khắt khe nhất: `ValidatingIntegrity`. Nếu có hai nút trùng mã định danh hoặc có cạnh trỏ vào hư vô, đồ thị lập tức chuyển sang `ValidationFailed`, ném ngoại lệ và dừng pipeline (lúc này chưa tạo tệp tạm nào). Nếu vượt qua kiểm tra, đồ thị chuyển sang `PersistingAtomic`, mở tệp tạm `.graph.tmp` và ghi toàn bộ dữ liệu JSON; nếu xảy ra lỗi I/O đĩa thì chuyển sang `WriteFailed` và xóa tệp tạm trong `finally`. Nếu ghi thành công, hệ thống thực thi lệnh hoán đổi tệp nguyên tử `os.replace` để đạt trạng thái bền vững `Committed`.

#### 5. Bảng chuyển trạng thái
| Trạng thái hiện tại | Sự kiện | Guard | Tiếp theo | Hành động |
|---|---|---|---|---|
| Initial | Khởi tạo | — | `Initialized` | — |
| `Initialized` | Bắt đầu xây dựng | Có `RepositoryIndex` hợp lệ | `PopulatingCore` | Tạo nút repository, file, symbol, taxonomy |
| `PopulatingCore` | Nạp xong nút lõi | — | `LinkingEdges` | Duyệt quan hệ |
| `LinkingEdges` | Gặp đích ngoài dự án | đích không có trong đồ thị | `LinkingEdges` | Tạo nút `EXTERNAL` |
| `LinkingEdges` | Nối xong cạnh | tất cả cạnh đã thêm | `AttachingSummaries` | Nạp `summaries.json` |
| `AttachingSummaries` | Gắn xong | — | `ValidatingIntegrity` | `validate_graph_integrity()` |
| `ValidatingIntegrity` | Thẩm định đạt | ID duy nhất VÀ mọi cạnh có 2 đầu mút | `PersistingAtomic` | Mở `NamedTemporaryFile` |
| `ValidatingIntegrity` | Trùng ID | có ≥ 2 nút trùng `id` | `ValidationFailed` | Ném `ValueError("Graph node IDs must be unique")` |
| `ValidatingIntegrity` | Cạnh mồ côi | đỉnh nguồn/đích không tồn tại | `ValidationFailed` | Ném `ValueError("Edge endpoint is missing")` |
| `PersistingAtomic` | Ghi đệm thành công | ghi trọn vẹn | `Committed` | `os.replace` |
| `PersistingAtomic` | Lỗi I/O | không ghi được | `WriteFailed` | Xóa tệp tạm trong `finally` |
| `Committed`, `ValidationFailed`, `WriteFailed` | — | — | Final | (không nhãn) |

#### 6. Chuyển trạng thái không hợp lệ / bị cấm
- Không vào `PersistingAtomic` khi chưa qua `ValidatingIntegrity`.
- Không ghi đè trực tiếp `graph.json` mà không qua tệp tạm `.graph.tmp`.
- Khi `ValidationFailed` **chưa có tệp tạm** nào được tạo.

#### 7. Căn cứ phân tích
- Code: `backend/src/knowledge_graph/builder.py:64-322`, `builder.py:334-360`, `backend/src/knowledge_graph/models.py:74-95`.
- Trạng thái xác minh: **Đã xác nhận đầy đủ trong mã nguồn**.

---

### ĐỐI TƯỢNG 5: PHIÊN TƯƠNG TÁC TRỢ LÝ AI TRÊN WIKI (`AskAIWidgetSession`)

#### 1. Tên đối tượng và mục đích quản lý
- **Tên đối tượng:** `AskAIWidgetSession` (Phiên Tương tác Hỏi đáp của Trợ lý AI trên Giao diện Wiki).
- **Mục đích quản lý:** Quản lý chu trình tiếp nhận câu hỏi tự nhiên của người đọc trên trình duyệt, xếp hạng ngữ cảnh tri thức, duy trì kết nối truyền luồng với Ollama và thực thi cơ chế hạ cấp dự phòng nội bộ khi mất kết nối.

#### 2. Vòng đời tổng quát và cách tạo ra
Được khởi tạo bởi mã JavaScript trên trang `base.html` khi người dùng mở trang wiki và nhấp mở bảng chat. Nó trải qua việc thăm dò kết nối dịch vụ, chờ câu hỏi, phân tích từ khóa, xếp hạng ngữ cảnh, truyền luồng câu trả lời hoặc kích hoạt cơ chế dự phòng thông minh khi Ollama ngoại tuyến.

#### 3. Danh sách trạng thái nghiệp vụ đã xác nhận
| Tên trạng thái | Phân loại | Ý nghĩa nghiệp vụ | Bằng chứng mã nguồn |
|---|:---:|---|---|
| `Idle` | Khởi tạo | Widget đang mở ở trạng thái chờ người dùng nhập câu hỏi | `base.html:327-330` |
| `ProbingService` | Trung gian | Đang gửi yêu cầu ngầm kiểm tra sức khỏe dịch vụ Ollama cục bộ | `base.html:332-356` |
| `ProcessingIntent` | Trung gian | Đã nhận câu hỏi, đang phân tích ý định (đếm/tìm kiếm/kiểm thử) và lọc từ khóa | `base.html:392-402, 450-452` |
| `RankingContext` | Trung gian | Đang tính điểm và trích xuất tối đa 12 ký hiệu và 3 chuyên đề khớp nhất | `base.html:454-486` |
| `StreamingAI` | Trung gian | Đang truyền luồng suy luận thời gian thực từ API Ollama về giao diện chat | `base.html:491-522` |
| `FallbackLocal` | Trung gian | Kết nối Ollama thất bại, đang tổng hợp câu trả lời từ tri thức nội bộ | `base.html:528-595` |
| `Answered` | Trung gian (Ổn định) | Câu trả lời đã hiển thị trọn vẹn kèm siêu liên kết, sẵn sàng cho câu hỏi tiếp theo | `base.html:521, 594` |

#### 4. Câu chuyện vòng đời
Khi người đọc nhấp vào nút nổi ở góc màn hình, một `AskAIWidgetSession` mở ra ở trạng thái `Idle`. Ngay lập tức, một tiến trình ngầm chuyển sang `ProbingService` để kiểm tra cổng `11434`. Dựa trên kết quả, chấm trạng thái đổi sang màu xanh ("Ollama online") hoặc màu đỏ ("Ollama offline"). Khi người dùng gõ câu hỏi và nhấn gửi, phiên chuyển sang `ProcessingIntent` để phân tích ngữ nghĩa và tách từ khóa bỏ qua từ dừng. Tiếp theo, phiên chuyển sang `RankingContext` để rà soát toàn bộ tệp `wiki_context.json`, chọn ra những thành phần mã nguồn có điểm liên quan cao nhất. Sau khi đóng gói câu lệnh nhắc, hệ thống gửi yêu cầu đến Ollama: nếu kết nối thông suốt, phiên chuyển sang `StreamingAI`, từng từ ngữ tuôn trào theo thời gian thực vào khung chat; nếu kết nối thất bại (do tắt server hoặc lỗi CORS), phiên chuyển sang `FallbackLocal`, tự động hiển thị thẻ tóm tắt ký hiệu hoặc thống kê codebase nội bộ. Cuối cùng, phiên đạt trạng thái `Answered`, cuộn khung chat xuống dưới cùng và sẵn sàng tiếp nhận câu hỏi mới. Trạng thái kết thúc (Final State) chỉ đạt được khi người dùng đóng widget hoặc rời trang web.

#### 5. Bảng chuyển trạng thái
| Trạng thái hiện tại | Sự kiện | Guard | Tiếp theo | Hành động |
|---|---|---|---|---|
| Initial | Mở widget | Đã nạp trang | `Idle` | Hiển thị khung chat |
| `Idle` | Tự động ngay sau khi mở, hoặc timer 30 giây | Đã nạp trang | `ProbingService` | `fetch(http://localhost:11434/api/tags)` |
| `ProbingService` | Có phản hồi | có model `qwen2.5-coder:3b` | `Idle` | Chấm xanh "Ollama online" |
| `ProbingService` | Có phản hồi | thiếu model | `Idle` | Chấm đỏ "Ollama offline" |
| `ProbingService` | Không kết nối | lỗi mạng / server tắt | `Idle` | Chấm đỏ "Ollama offline" |
| `Idle` | Bấm Gửi / Enter | `text.trim() != ""` | `ProcessingIntent` | Hiển thị câu hỏi, "Đang suy nghĩ..." |
| `ProcessingIntent` | Tách từ khóa xong | có mảng `words` | `RankingContext` | Tính điểm ký hiệu + chuyên đề |
| `RankingContext` | Đóng gói prompt xong | ngữ cảnh sẵn sàng | `StreamingAI` | POST tới `/api/generate` (`stream: true`) |
| `StreamingAI` | Nhận gói stream | `response.ok == true` | `StreamingAI` | Gắn từ vào khung chat |
| `StreamingAI` | Luồng kết thúc | `done == true` | `Answered` | Hoàn tất câu trả lời AI |
| `StreamingAI` | Lỗi kết nối / CORS | `fetch` ném lỗi hoặc không 200 | `FallbackLocal` | Kích hoạt dự phòng thông minh |
| `FallbackLocal` | Tổng hợp xong | dữ liệu nội bộ đã định dạng | `Answered` | Hiển thị ký hiệu + hướng dẫn lệnh |
| `Answered` | Nhập câu hỏi mới | `text.trim() != ""` | `ProcessingIntent` | Lượt hỏi đáp tiếp theo |
| `Idle` / `Answered` | Đóng widget / rời trang | — | Final | (không nhãn) |

#### 6. Chuyển trạng thái không hợp lệ / bị cấm
- Không gửi câu hỏi rỗng.
- Không để widget treo khi Ollama ngoại tuyến (phải đi qua `FallbackLocal`).

#### 7. Căn cứ phân tích
- Code: `backend/src/wiki_generation/templates/base.html:305-604`.
- Trạng thái xác minh: **Đã xác nhận đầy đủ trong mã nguồn**.
