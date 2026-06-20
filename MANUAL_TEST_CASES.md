# Tài liệu Kiểm thử Thủ công (Manual Test Cases) - TerraAlert

Tài liệu này bao gồm các Test Case để kiểm tra toàn bộ chức năng giao diện và logic của hệ thống TerraAlert.

---

## 1. Module TerraBot Chat (Agentic RAG)

### 1.1. Tính năng Thời tiết (Weather Agent)
| Test Case ID | Mục tiêu kiểm thử | Các bước thực hiện | Kết quả mong đợi |
| --- | --- | --- | --- |
| TC_CHAT_01 | Lấy thông tin thời tiết hợp lệ | 1. Mở cửa sổ TerraBot.<br>2. Nhập: *"Thời tiết Đà Nẵng hôm nay thế nào?"*<br>3. Bấm Gửi. | Bot trả về thông tin thời tiết (nhiệt độ, mưa, gió, độ ẩm). Dưới cùng có link nguồn `📚 Dịch vụ Thời tiết Thực tế (wttr.in)` có thể click vào được. |
| TC_CHAT_02 | Truy vấn thời tiết không nêu rõ địa điểm | 1. Nhập: *"Thời tiết hôm nay ra sao?"*<br>2. Bấm Gửi. | Bot tự động mặc định lấy thời tiết tại "Hà Nội" và trả về kết quả tương ứng. |
| TC_CHAT_03 | Click vào Link Nguồn thời tiết | 1. Click vào text link `📚 Dịch vụ Thời tiết Thực tế (wttr.in)` ở dưới câu trả lời. | Mở tab mới dẫn đến trang `https://wttr.in`. |

### 1.2. Tính năng Cảnh báo rủi ro địa lý (Geo Agent)
| Test Case ID | Mục tiêu kiểm thử | Các bước thực hiện | Kết quả mong đợi |
| --- | --- | --- | --- |
| TC_CHAT_04 | Truy vấn vùng rủi ro cụ thể | 1. Nhập: *"Tình hình sạt lở ở Mộc Châu đang ra sao?"*<br>2. Bấm Gửi. | Bot phân tích đây là câu hỏi Geo và trả về các chỉ số cảnh báo rủi ro về độ dốc, địa chất tại Mộc Châu. |

### 1.3. Tính năng Kiến thức chuyên sâu (Knowledge Base - RAG)
| Test Case ID | Mục tiêu kiểm thử | Các bước thực hiện | Kết quả mong đợi |
| --- | --- | --- | --- |
| TC_CHAT_05 | Truy vấn cách sơ cứu | 1. Nhập: *"Làm thế nào để sơ cứu người bị đuối nước do ngập lụt?"*<br>2. Bấm Gửi. | Bot truy xuất dữ liệu từ ChromaDB và hướng dẫn từng bước sơ cứu. Dưới cùng hiển thị link nguồn các tài liệu hướng dẫn sơ cứu. |
| TC_CHAT_06 | Xử lý truy vấn không liên quan | 1. Nhập: *"Hướng dẫn cách nấu món bún chả."*<br>2. Bấm Gửi. | Bot từ chối trả lời lịch sự vì ngoài phạm vi hiểu biết (Thiên tai & Sơ cứu). |

### 1.4. Giao diện Chat Window
| Test Case ID | Mục tiêu kiểm thử | Các bước thực hiện | Kết quả mong đợi |
| --- | --- | --- | --- |
| TC_UI_01 | Giao diện thanh nhập liệu (Input) | 1. Nhìn vào thanh nhập liệu của Chat. | Nền ô nhập liệu màu trắng, chữ gõ vào là màu đen (`text-gray-900`), hiển thị rõ nét không bị chìm màu. |
| TC_UI_02 | Ngăn gửi tin nhắn rỗng | 1. Để trống ô nhập liệu hoặc gõ toàn dấu cách.<br>2. Bấm nút Gửi (hoặc Enter). | Nút Gửi bị vô hiệu hóa (màu xám), không gửi được tin nhắn rỗng đi. |

---

## 2. Module Tổng quan (Dashboard)

| Test Case ID | Mục tiêu kiểm thử | Các bước thực hiện | Kết quả mong đợi |
| --- | --- | --- | --- |
| TC_DASH_01 | Hiển thị thẻ Tóm tắt (Summary Cards) | 1. Vào trang chủ Dashboard. | Hiển thị đầy đủ số liệu: Số khu vực nguy hiểm, số cảnh báo mới, tình trạng cứu hộ, thời tiết. |
| TC_DASH_02 | Hiển thị Biểu đồ (Charts) | 1. Cuộn đến khu vực Biểu đồ lượng mưa/Mực nước. | Biểu đồ render đầy đủ nhãn trục X/Y, tooltip hiện ra khi hover chuột vào biểu đồ. |
| TC_DASH_03 | Hiển thị danh sách Cảnh báo (Alert List) | 1. Xem danh sách Cảnh báo Mới nhất. | Các dòng cảnh báo hiện thị icon mức độ nghiêm trọng (Đỏ/Vàng/Xanh). |

---

## 3. Module Bản đồ Cảnh báo (Map View)

| Test Case ID | Mục tiêu kiểm thử | Các bước thực hiện | Kết quả mong đợi |
| --- | --- | --- | --- |
| TC_MAP_01 | Render Bản đồ | 1. Mở component Bản đồ Cảnh báo. | Map load thành công (có thể dùng Leaflet/Mapbox). Có các điểm đánh dấu (Markers) tương ứng vùng thiên tai. |
| TC_MAP_02 | Xem chi tiết điểm đánh dấu | 1. Click vào một Marker (điểm màu đỏ/cam). | Hiển thị Popup (Tooltip) mô tả: Tên khu vực, Tình trạng, Mức độ cảnh báo. |

---

## 4. Các Trang Chuyên biệt (Pages)

### 4.1. Trang Nghiên cứu (Research Page)
| Test Case ID | Mục tiêu kiểm thử | Các bước thực hiện | Kết quả mong đợi |
| --- | --- | --- | --- |
| TC_RES_01 | Tra cứu tài liệu nghiên cứu | 1. Chuyển sang Tab Research.<br>2. Xem danh sách tài liệu. | Hiển thị Grid/List các tài liệu phân tích rủi ro, cho phép lọc hoặc tìm kiếm. |

### 4.2. Trang Kỹ năng Sinh tồn (Survival Page)
| Test Case ID | Mục tiêu kiểm thử | Các bước thực hiện | Kết quả mong đợi |
| --- | --- | --- | --- |
| TC_SURV_01 | Đọc cẩm nang sinh tồn | 1. Chuyển sang Tab Survival.<br>2. Mở một bài viết (VD: Phòng chống sạt lở). | Hiển thị nội dung chi tiết rõ ràng, hình ảnh minh họa đầy đủ, có nút quay lại (Back). |

---

## 5. Responsive Design (Hiển thị trên Mobile)

| Test Case ID | Mục tiêu kiểm thử | Các bước thực hiện | Kết quả mong đợi |
| --- | --- | --- | --- |
| TC_RES_01 | Giao diện trên Màn hình nhỏ (Mobile) | 1. Mở F12 -> Bật chế độ Responsive (Kích thước iPhone 14/15).<br>2. Điều hướng các trang. | Sidebar menu thu gọn thành Hamburger menu. Các Card hiển thị dạng cột (Column). Thanh chat Input không bị che lấp bởi bàn phím ảo. |

---

## 6. Module Quản trị (Admin)

### 6.1. Knowledge Base (Nạp Dữ liệu RAG)
| Test Case ID | Mục tiêu kiểm thử | Các bước thực hiện | Kết quả mong đợi |
| --- | --- | --- | --- |
| TC_ADMIN_KB_01 | Upload file hợp lệ (Dry Run) | 1. Vào `/admin/kb`.<br>2. Chọn file `.pdf`, `.md` hoặc `.txt`.<br>3. Bấm "Phân tích thử". | Chờ xử lý xong, hệ thống hiển thị danh sách các Chunk (đoạn text được cắt) kèm theo ước tính Token. |
| TC_ADMIN_KB_02 | Lưu Chunks vào Vector DB (Commit) | 1. Sau khi Dry Run thành công, hiển thị danh sách Chunk.<br>2. Bấm "Phê duyệt & Nạp". | Chunks được lưu vào ChromaDB, hiển thị thông báo thành công màu xanh lá và xóa danh sách đang preview. |
| TC_ADMIN_KB_03 | Upload file không hợp lệ | 1. Vào `/admin/kb`.<br>2. Bấm "Phân tích thử" khi chưa chọn file. | Nút phân tích bị khóa (disabled) hoặc hệ thống cảnh báo yêu cầu chọn file. |
