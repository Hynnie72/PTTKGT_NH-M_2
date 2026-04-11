THUẬT TOÁN VÉT CẠN (BRUTE FORCE)
1. Ý tưởng
Bài toán được mô hình hóa thành TSP: xuất phát từ kho hàng, đi qua tất cả các điểm giao và quay về kho với tổng quãng đường nhỏ nhất.
Phương pháp vét cạn sẽ thử tất cả các tuyến đường có thể và chọn tuyến tốt nhất.
2. Mô tả
Thuật toán gồm 3 bước:
	Sinh tất cả các tuyến đường (hoán vị các điểm giao): Từ danh sách các địa điểm giao hàng, tiến hành sinh tất cả các hoán vị để tạo ra các tuyến đường khác nhau. Điểm xuất phát (kho hàng) được cố định.
	Tính chi phí cho từng tuyến: Với mỗi tuyến đường, tính tổng quãng đường bằng cách cộng khoảng cách giữa các điểm liên tiếp, bao gồm cả quãng đường quay về kho ban đầu.
	Chọn tuyến có chi phí nhỏ nhất: So sánh chi phí của tất cả các tuyến đường và chọn tuyến có tổng chi phí nhỏ nhất.
3. Tính chi phí
Chi phí là tổng khoảng cách giữa các điểm liên tiếp, bao gồm cả quay về kho:
Cost=d(0,x1)+d(x1,x2)+⋯+d(xn,0)
Trong đó:
	0là kho hàng
	x_1,x_2,...,x_nlà các điểm giao hàng
	d(i,j)là khoảng cách giữa điểm ivà j
4. Độ phức tạp
Độ phức tạp: O(n!)
Số tuyến tăng rất nhanh khi số điểm tăng.
Ví dụ:
	Với 5 điểm → 5! = 120 tuyến
	Với 8 điểm → 8! = 40320 tuyến
	Với 10 điểm → 10! ≈ 3.6 triệu tuyến
Khi số lượng điểm tăng, số lượng tuyến đường tăng rất nhanh, dẫn đến thời gian thực thi lớn. Vì vậy, phương pháp vét cạn chỉ phù hợp với bài toán có quy mô nhỏ.
5. Thời gian chạy
Thời gian chạy của thuật toán phụ thuộc trực tiếp vào số lượng tuyến đường cần xét. Khi số lượng điểm giao hàng tăng lên, số lượng hoán vị tăng theo cấp số giai thừa, khiến chương trình chạy chậm đáng kể.
Trong thực tế, với số lượng đơn hàng lớn (trên 10 điểm), thuật toán vét cạn trở nên không khả thi do tốn quá nhiều thời gian xử lý.
6. Kết quả
Chương trình được chạy thử với dữ liệu mẫu bao gồm các địa điểm giao hàng và ma trận khoảng cách giữa các điểm.
Kết quả đầu ra bao gồm:
	Danh sách tất cả các tuyến đường
	Chi phí tương ứng của từng tuyến
	Tuyến đường có chi phí nhỏ nhất (tuyến tối ưu)
Kết quả được hiển thị trên màn hình và xuất ra file output để tiện theo dõi và đánh giá.
7. Kết luận
Phương pháp vét cạn đảm bảo tìm được lời giải tối ưu tuyệt đối cho bài toán TSP. Tuy nhiên, do độ phức tạp rất lớn O(n!), phương pháp này chỉ phù hợp với các bài toán có số lượng điểm giao hàng nhỏ.
Vét cạn cho kết quả chính xác nhưng không hiệu quả với dữ liệu lớn, cần dùng thuật toán khác trong thực tế.

