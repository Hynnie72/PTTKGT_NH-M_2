-- Xóa bảng nếu đã tồn tại
DROP TABLE IF EXISTS orders;

-- Tạo bảng
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    ma_don TEXT,
    ten_khach TEXT,
    sdt TEXT,
    dia_chi TEXT,
    quan TEXT,
    thanh_pho TEXT,
    gia_tri INTEGER,
    khoang_cach REAL,
    lat REAL,
    lng REAL
);

-- Insert data
INSERT INTO orders 
(ma_don, ten_khach, sdt, dia_chi, quan, thanh_pho, gia_tri, khoang_cach, lat, lng)
VALUES
('ORD01','Nguyễn Văn An','0901234567','Q1','Quận 1','HCM',500000,2.5,10.774,106.699),
('ORD02','Trần Thị Bình','0912345678','Q3','Quận 3','HCM',300000,3.2,10.775,106.703),
('ORD03','Lê Minh Tâm','0987654321','Q5','Quận 5','HCM',450000,4.1,10.777,106.688),
('ORD04','Phạm Thanh Hà','0933445566','Q10','Quận 10','HCM',600000,5.0,10.780,106.690),
('ORD05','Hoàng Anh Tú','0944556677','Q7','Quận 7','HCM',200000,6.3,10.762,106.705),
('ORD06','Nguyễn Thị Lan','0955667788','Q4','Quận 4','HCM',350000,2.9,10.760,106.702),
('ORD07','Đỗ Văn Nam','0966778899','Q2','Quận 2','HCM',700000,7.5,10.790,106.720),
('ORD08','Bùi Thị Mai','0977889900','Q9','Quận 9','HCM',150000,8.2,10.820,106.750),
('ORD09','Võ Hoàng Phúc','0988990011','Q12','Quận 12','HCM',400000,9.1,10.850,106.650),
('ORD10','Trương Mỹ Linh','0999001122','Gò Vấp','Gò Vấp','HCM',250000,6.8,10.830,106.670),

('ORD11','Nguyễn Quốc Bảo','0901112233','Bình Thạnh','Bình Thạnh','HCM',520000,3.7,10.810,106.710),
('ORD12','Lê Thị Hồng','0912223344','Phú Nhuận','Phú Nhuận','HCM',310000,4.0,10.800,106.680),
('ORD13','Phan Văn Dũng','0923334455','Tân Bình','Tân Bình','HCM',280000,5.6,10.790,106.660),
('ORD14','Đặng Thị Hoa','0934445566','Tân Phú','Tân Phú','HCM',330000,6.2,10.780,106.640),
('ORD15','Huỳnh Văn Sơn','0945556677','Bình Tân','Bình Tân','HCM',410000,7.9,10.760,106.600),
('ORD16','Trần Quốc Khánh','0956667788','Thủ Đức','Thủ Đức','HCM',620000,8.5,10.870,106.760),
('ORD17','Nguyễn Thị Hạnh','0967778899','Nhà Bè','Nhà Bè','HCM',270000,9.0,10.690,106.730),
('ORD18','Lý Công Minh','0978889900','Củ Chi','Củ Chi','HCM',360000,15.0,11.000,106.500),
('ORD19','Phạm Văn Long','0989990011','Hóc Môn','Hóc Môn','HCM',290000,12.0,10.880,106.600),
('ORD20','Đỗ Thị Yến','0991112233','Quận 6','Quận 6','HCM',330000,5.5,10.750,106.640);