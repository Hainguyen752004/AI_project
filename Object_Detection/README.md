# Chú thích về code

**Code chạy trên mô hình YOLOv8**

Do chạy trên YOLOv8 nên sẽ tiến hành phân tích theo từng Frame nên nếu muốn cho ra kết quả nhanh nhất thì có thể lựa chọn video_input có fps từ 25-30fps sẽ tiết kiệm được thời gian rất nhiều.

**Về file Code**
Trong file code có 1 dòng sửa tất cả các xe như: xe tải, xe máy,... về chung là xe (car) có thể mở tùy nhu cầu (Mặc định là đang tắt).
Hiện tại các lớp ID vật thể đang để tiếng Anh do còn bị lỗi Font tiếng Việt (Car 1, Person 1).

**Về file Json**
File Json đã sửa thành các giá trị thành tiếng Việt, giá trị Box không được sửa thành tiếng Việt do cảm thấy không cần thiết.
