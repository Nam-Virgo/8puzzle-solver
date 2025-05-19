# 8puzzle-solver
# 8puzzle-solver
1. Mục tiêu
Xây dựng một công cụ trực quan giúp người dùng giải bài toán 8-Puzzle bằng nhiều thuật toán tìm kiếm khác nhau, trong cả môi trường có thể quan sát và môi trường không có quan sát (sử dụng trạng thái niềm tin – Belief States).

2. Nội dung

2.1. Các thuật toán Tìm kiếm không có thông tin (BFS, DFS, IDS, UCS)

2.1.1. Các thành phần chính của bài toán tìm kiếm
Trong bài toán 8-Puzzle, khi áp dụng các thuật toán tìm kiếm không có thông tin, các thành phần chính được xác định như sau:
Trạng thái (State) là một bảng 3x3 đại diện cho vị trí các ô số từ 1–8 và một ô trống (0).
Trạng thái ban đầu (Initial state):	Trạng thái đầu vào mà người chơi cung cấp.
Trạng thái đích (Goal state): Trạng thái mong muốn, thường là: [[1,2,3],[4,5,6],[7,8,0]]
Tập hành động (Actions): Các thao tác di chuyển ô trống: lên (↑), xuống (↓), trái (←), phải (→)
Hàm kế tiếp (Successor function):	Cho biết trạng thái mới sau khi thực hiện một hành động hợp lệ.
Kiểm tra mục tiêu (Goal test):	Kiểm tra xem trạng thái hiện tại có khớp với trạng thái đích không.
Chi phí bước đi (Path cost):	Mỗi bước đi có thể có chi phí bằng 1 (Uniform) hoặc tính riêng.

2.1.2. Giải pháp (Solution) là gì?
Giải pháp là một chuỗi hành động (move sequence) từ trạng thái ban đầu đến trạng thái đích.
Ví dụ: [↓, →, ↓, ←, ...]
Trong giao diện chương trình, mỗi hành động được áp dụng và hiển thị kèm trạng thái tương ứng.
Một giải pháp tốt nên có ít bước và chi phí nhỏ nhất (nếu xét chi phí).

2.1.3. Nhận xét về hiệu suất các thuật toán trong nhóm này
| Thuật toán | Ưu điểm                                                    | Nhược điểm                               | Quan sát thực tế                         |
| ---------- | ---------------------------------------------------------- | ---------------------------------------- | ---------------------------------------- |
| **BFS**    | Luôn tìm lời giải ngắn nhất (nếu chi phí bằng nhau)        | Tốn bộ nhớ nhiều                         | Mất \~0.73s, 23 bước                     |
| **DFS**    | Bộ nhớ thấp                                                | Dễ đi lạc, không đảm bảo lời giải tối ưu | Chậm hơn, mất \~5.35s                    |
| **UCS**    | Tìm được lời giải tối ưu nếu chi phí không bằng nhau       | Cần hàng đợi ưu tiên, bộ nhớ cao         | \~1.27s, giải đúng                       |
| **IDS**    | Kết hợp ưu điểm của DFS và BFS (ít bộ nhớ, đảm bảo tối ưu) | Tốn thời gian do lặp lại nhiều lần       | Nhanh (\~0.39s), nhưng dài hơn (27 bước) |
✅ Nhận xét tổng quan:
Với 8-Puzzle, do không gian trạng thái không quá lớn, BFS hoặc IDS thường là lựa chọn tốt.
DFS ít hiệu quả vì dễ đi sai hướng và tốn thời gian.
UCS hữu ích nếu bài toán có chi phí bước đi khác nhau.
IDS là lựa chọn hợp lý nếu muốn giảm bộ nhớ mà vẫn tìm được lời giải ngắn.

2.2. Các thuật toán Tìm kiếm có thông tin (A* Search, IDA*, Greedy Best-First Search)
| Thuật toán                   | Ưu điểm nổi bật                                               | Nhược điểm                                              | Quan sát thực tế                                      |
| ---------------------------- | ------------------------------------------------------------- | ------------------------------------------------------- | ----------------------------------------------------- |
| **Greedy Best-First Search** | Nhanh, thường tìm lời giải sớm nhờ heuristic (hàm đánh giá)   | Không đảm bảo tìm lời giải tối ưu (chọn ngắn nhưng sai) | Thời gian thấp (\~0.23s), nhưng dài tới 79 bước       |
| **A\***                      | Tìm lời giải ngắn nhất nếu heuristic tốt (tối ưu, hoàn chỉnh) | Cần nhiều bộ nhớ để lưu tất cả trạng thái duyệt qua     | Cân bằng giữa tốc độ và chất lượng (\~0.47s, 23 bước) |
| **IDA\***                    | Kết hợp độ sâu và heuristic → giảm bộ nhớ so với A\*          | Có thể chạy lại nhiều lần → tốn thời gian hơn A\*       | Kết quả đúng (24 bước), thời gian \~0.70s             |

✅ Tổng kết:
Greedy tuy nhanh nhất nhưng tạo ra lời giải kém chất lượng nhất (nhiều bước) do chỉ quan tâm đến heuristic mà bỏ qua chi phí thực.
A* là lựa chọn tối ưu nhất trong trường hợp này: vừa nhanh, vừa tìm lời giải ngắn.
IDA* là một thay thế cho A* khi bộ nhớ hạn chế, chấp nhận thời gian lâu hơn một chút.

🧠 Ghi chú:
Tất cả các thuật toán này dùng heuristic, phổ biến nhất là:
h(n) = tổng khoảng cách Manhattan từ mỗi ô về đúng vị trí trong goal.
A*, IDA* dùng f(n) = g(n) + h(n)
Greedy chỉ dùng f(n) = h(n)

2.3. Các thuật toán Tìm kiếm cục bộ
(Simple Hill Climbing, Steepest Ascent Hill Climbing, Stochastic Hill Climbing, Simulated Annealing, Local Beam Search, Genetic Algorithm)

📌 Nhận xét về hiệu suất khi áp dụng vào trò chơi 8 ô chữ:

| Thuật toán                        | Ưu điểm                                             | Nhược điểm                                                         | Quan sát thực tế                              |
| --------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------ | --------------------------------------------- |
| **Simple Hill Climbing**          | Cách cài đặt đơn giản, chạy nhanh                   | Dễ kẹt ở local maxima, không đảm bảo tìm được lời giải             | Nhanh (\~0.05s), giải không tối ưu (114 bước) |
| **Steepest Ascent Hill Climbing** | Cải tiến hơn: chọn nước đi tốt nhất trong hàng xóm  | Vẫn có thể kẹt nếu tất cả hàng xóm kém hơn                         | Thường giải được, bước dao động (50–96 bước)  |
| **Stochastic Hill Climbing**      | Chọn ngẫu nhiên hàng xóm tốt hơn → giảm nguy cơ kẹt | Không đảm bảo tối ưu, kết quả không ổn định giữa các lần chạy      | Đa số giải được, bước dao động (64–82 bước)   |
| **Beam Search**                   | Duy trì nhiều trạng thái tốt nhất → giảm kẹt local  | Cần chọn `k` hợp lý, vẫn có thể lặp và sai hướng                   | Chạy được, nhưng giải kém (154 bước)          |
| **Simulated Annealing**           | Cho phép "nhảy có kiểm soát" ra khỏi local minima   | Phụ thuộc nhiều vào tham số nhiệt độ, dễ sai nếu cấu hình chưa tốt | Hiếm khi giải được nếu không tối ưu tham số   |
| **Genetic Algorithm**             | Khám phá mạnh nhờ đột biến và lai ghép              | Ngẫu nhiên cao, không đảm bảo tìm ra lời giải, cần thử nhiều lần   | Rất hiếm khi giải ra, kết quả không ổn định   |

✅ Tổng kết:
Các thuật toán cục bộ rất phù hợp để chạy nhanh trên không gian lớn, nhưng không đảm bảo luôn tìm được lời giải, nhất là khi:

Không có cơ chế thoát khỏi local minima

Hoặc khi heuristic không đủ dẫn hướng

Steepest Ascent HC và Stochastic HC là những lựa chọn khá hiệu quả, nhưng vẫn phụ thuộc vào may rủi và cấu hình. Steepest HC bị kẹt nếu không có hàng xóm nào tốt hơn. Stochastic HC ngẫu nhiên nên có thể không chọn đúng hướng tốt nhất.

Simulated Annealing và Genetic Algorithm cần tối ưu tham số, chạy nhiều lần, và vẫn không đảm bảo thành công.

