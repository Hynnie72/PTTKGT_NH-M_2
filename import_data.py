import os
import django
import sys

# 1. Thiết lập môi trường Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web1.settings')
django.setup()

# 2. Import Model sau khi đã setup django
from delivery.models import DonHang

def import_data():
    """Nhập 20 đơn hàng với trạng thái: 10 Chưa giao, 5 Đang giao, 5 Đã giao"""
    
    print("--- Đang xóa dữ liệu cũ... ---")
    DonHang.objects.all().delete()
    
    # Dữ liệu 20 đơn hàng
    orders_data = [
        # 10 đơn CHƯA GIAO (1-10)
        ("DH001", "Nguyễn Văn An", "0901234567", "Số 1, Đường A, Quận 1", 10.774, 106.699, "CHUA_GIAO"),
        ("DH002", "Trần Thị Bình", "0912345678", "Số 2, Đường B, Quận 3", 10.775, 106.703, "CHUA_GIAO"),
        ("DH003", "Lê Minh Tâm", "0987654321", "Số 3, Đường C, Quận 5", 10.777, 106.688, "CHUA_GIAO"),
        ("DH004", "Phạm Thanh Hà", "0933445566", "Số 4, Đường D, Quận 10", 10.780, 106.690, "CHUA_GIAO"),
        ("DH005", "Hoàng Anh Tú", "0944556677", "Số 5, Đường E, Quận 7", 10.762, 106.705, "CHUA_GIAO"),
        ("DH006", "Nguyễn Thị Lan", "0955667788", "Số 6, Đường F, Quận 4", 10.760, 106.702, "CHUA_GIAO"),
        ("DH007", "Đỗ Văn Nam", "0966778899", "Số 7, Đường G, Quận 2", 10.790, 106.720, "CHUA_GIAO"),
        ("DH008", "Bùi Thị Mai", "0977889900", "Số 8, Đường H, Quận 9", 10.820, 106.750, "CHUA_GIAO"),
        ("DH009", "Võ Hoàng Phúc", "0988990011", "Số 9, Đường I, Quận 12", 10.850, 106.650, "CHUA_GIAO"),
        ("DH010", "Trương Mỹ Linh", "0999001122", "Số 10, Đường J, Gò Vấp", 10.830, 106.670, "CHUA_GIAO"),
        
        # 5 đơn ĐANG GIAO (11-15)
        ("DH011", "Nguyễn Quốc Bảo", "0901112233", "Số 11, Đường K, Bình Thạnh", 10.810, 106.710, "DANG_GIAO"),
        ("DH012", "Lê Thị Hồng", "0912223344", "Số 12, Đường L, Phú Nhuận", 10.800, 106.680, "DANG_GIAO"),
        ("DH013", "Phan Văn Dũng", "0923334455", "Số 13, Đường M, Tân Bình", 10.790, 106.660, "DANG_GIAO"),
        ("DH014", "Đặng Thị Hoa", "0934445566", "Số 14, Đường N, Tân Phú", 10.780, 106.640, "DANG_GIAO"),
        ("DH015", "Huỳnh Văn Sơn", "0945556677", "Số 15, Đường O, Bình Tân", 10.760, 106.600, "DANG_GIAO"),
        
        # 5 đơn ĐÃ GIAO (16-20)
        ("DH016", "Trần Quốc Khánh", "0956667788", "Số 16, Đường P, Thủ Đức", 10.870, 106.760, "DA_GIAO"),
        ("DH017", "Nguyễn Thị Hạnh", "0967778899", "Số 17, Đường Q, Nhà Bè", 10.690, 106.730, "DA_GIAO"),
        ("DH018", "Lý Công Minh", "0978889900", "Số 18, Đường R, Củ Chi", 11.000, 106.500, "DA_GIAO"),
        ("DH019", "Phạm Văn Long", "0989990011", "Số 19, Đường S, Hóc Môn", 10.880, 106.600, "DA_GIAO"),
        ("DH020", "Đỗ Thị Yến", "0991112233", "Số 20, Đường T, Quận 6", 10.750, 106.640, "DA_GIAO"),
    ]
    
    print("--- Đang tạo 20 đơn hàng... ---")
    
    for ma_don, ten_khach, sdt, dia_chi, lat, lng, trang_thai in orders_data:
        order = DonHang.objects.create(
            ma_don=ma_don,
            ten_khach=ten_khach,
            so_dien_thoai=sdt,
            dia_chi=dia_chi,
            lat=lat,
            lng=lng,
            trang_thai=trang_thai
        )
        
        # Hiển thị trạng thái bằng icon
        if trang_thai == "CHUA_GIAO":
            icon = "🟡"
            text = "Chưa giao"
        elif trang_thai == "DANG_GIAO":
            icon = "🔵"
            text = "Đang giao"
        else:
            icon = "🟢"
            text = "Đã giao"
            
        print(f"  {icon} {ma_don} - {ten_khach} - {text}")
    
    # Thống kê kết quả
    print("\n" + "="*50)
    print("📊 KẾT QUẢ NHẬP DỮ LIỆU")
    print("="*50)
    print(f"✅ Tổng số đơn hàng: {DonHang.objects.count()}")
    print(f"🟡 Chưa giao: {DonHang.objects.filter(trang_thai='CHUA_GIAO').count()} đơn")
    print(f"🔵 Đang giao: {DonHang.objects.filter(trang_thai='DANG_GIAO').count()} đơn")
    print(f"🟢 Đã giao: {DonHang.objects.filter(trang_thai='DA_GIAO').count()} đơn")
    print("="*50)
    print("--- HOÀN THÀNH! ---")

if __name__ == "__main__":
    import_data()