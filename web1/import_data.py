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
    """Nhập 20 đơn hàng với địa chỉ rõ ràng, chi tiết"""
    
    print("="*80)
    print("   NHẬP DỮ LIỆU 20 ĐƠN HÀNG - GIAO HÀNG TP.HCM")
    print("="*80)
    
    print("\n--- Đang xóa dữ liệu cũ... ---")
    DonHang.objects.all().delete()
    print("✅ Đã xóa dữ liệu cũ")
    
    # Dữ liệu 20 đơn hàng (5 Đã giao, 5 Đang giao, 10 Chưa giao)
    orders_data = [
        # ========== 5 đơn ĐÃ GIAO (DH016 - DH020) ==========
        ("DH016", "Trần Quốc Khánh", "0956667788", "Số 16, Đường P, Phường Linh Tây, Thành phố Thủ Đức", 10.87000, 106.76000, "DA_GIAO"),
        ("DH017", "Nguyễn Thị Hạnh", "0967778899", "Số 17, Đường Q, Xã Phú Xuân, Huyện Nhà Bè", 10.69000, 106.73000, "DA_GIAO"),
        ("DH018", "Lý Công Minh", "0978889900", "Số 18, Đường R, Xã Tân An Hội, Huyện Củ Chi", 11.00000, 106.50000, "DA_GIAO"),
        ("DH019", "Phạm Văn Long", "0989990011", "Số 19, Đường S, Xã Tân Hiệp, Huyện Hóc Môn", 10.88000, 106.60000, "DA_GIAO"),
        ("DH020", "Đỗ Thị Yến", "0991112233", "Số 20, Đường T, Phường 11, Quận 6", 10.75000, 106.64000, "DA_GIAO"),
        
        # ========== 5 đơn ĐANG GIAO (DH011 - DH015) ==========
        ("DH011", "Nguyễn Quốc Bảo", "0901112233", "Số 11, Đường K, Phường 27, Quận Bình Thạnh", 10.81000, 106.71000, "DANG_GIAO"),
        ("DH012", "Lê Thị Hồng", "0912223344", "Số 12, Đường L, Phường 15, Quận Phú Nhuận", 10.80000, 106.68000, "DANG_GIAO"),
        ("DH013", "Phan Văn Dũng", "0923334455", "Số 13, Đường M, Phường 8, Quận Tân Bình", 10.79000, 106.66000, "DANG_GIAO"),
        ("DH014", "Đặng Thị Hoa", "0934445566", "Số 14, Đường N, Phường Tân Quý, Quận Tân Phú", 10.78000, 106.64000, "DANG_GIAO"),
        ("DH015", "Huỳnh Văn Sơn", "0945556677", "Số 15, Đường O, Phường An Lạc, Quận Bình Tân", 10.76000, 106.60000, "DANG_GIAO"),
        
        # ========== 10 đơn CHƯA GIAO (DH001 - DH010) ==========
        ("DH001", "Nguyễn Văn An", "0901234567", "Số 123, Đường Lê Lợi, Phường Bến Nghé, Quận 1", 10.77400, 106.69900, "CHUA_GIAO"),
        ("DH002", "Trần Thị Bình", "0912345678", "Số 456, Đường Nguyễn Huệ, Phường Bến Nghé, Quận 1", 10.77500, 106.70300, "CHUA_GIAO"),
        ("DH003", "Lê Minh Tâm", "0987654321", "Số 15, Đường Cách Mạng Tháng 8, Phường Bến Thành, Quận 3", 10.77700, 106.68800, "CHUA_GIAO"),
        ("DH004", "Phạm Thanh Hà", "0933445566", "Số 202, Đường Võ Văn Tần, Phường 5, Quận 3", 10.78000, 106.69000, "CHUA_GIAO"),
        ("DH005", "Hoàng Anh Tú", "0944556677", "Số 88, Đường Đoàn Văn Bơ, Phường 16, Quận 4", 10.76200, 106.70500, "CHUA_GIAO"),
        ("DH006", "Nguyễn Thị Lan", "0955667788", "Số 6, Đường F, Phường 12, Quận 4", 10.76000, 106.70200, "CHUA_GIAO"),
        ("DH007", "Đỗ Văn Nam", "0966778899", "Số 7, Đường G, Phường An Phú, Quận 2", 10.79000, 106.72000, "CHUA_GIAO"),
        ("DH008", "Bùi Thị Mai", "0977889900", "Số 8, Đường H, Phường Long Trường, Quận 9", 10.82000, 106.75000, "CHUA_GIAO"),
        ("DH009", "Võ Hoàng Phúc", "0988990011", "Số 9, Đường I, Phường Tân Chánh Hiệp, Quận 12", 10.85000, 106.65000, "CHUA_GIAO"),
        ("DH010", "Trương Mỹ Linh", "0999001122", "Số 10, Đường J, Phường 8, Quận Gò Vấp", 10.83000, 106.67000, "CHUA_GIAO"),
    ]
    
    print("\n--- Đang tạo 20 đơn hàng... ---")
    print("-"*80)
    
    for ma_don, ten_khach, sdt, dia_chi, lat, lng, trang_thai in orders_data:
        DonHang.objects.create(
            ma_don=ma_don,
            ten_khach=ten_khach,
            so_dien_thoai=sdt,
            dia_chi=dia_chi,
            lat=lat,
            lng=lng,
            trang_thai=trang_thai
        )
        
        # Hiển thị trạng thái
        if trang_thai == "CHUA_GIAO":
            icon = "🟡"
            text = "Chưa giao"
        elif trang_thai == "DANG_GIAO":
            icon = "🔵"
            text = "Đang giao"
        else:
            icon = "🟢"
            text = "Đã giao"
            
        print(f"  {icon} {ma_don} - {ten_khach:<22} - {text} - {dia_chi[:50]}...")
    
    # Thống kê
    print("-"*80)
    print("\n📊 KẾT QUẢ NHẬP DỮ LIỆU")
    print("="*80)
    print(f"✅ Tổng số đơn hàng: {DonHang.objects.count()} đơn")
    print(f"🟢 Đã giao        : {DonHang.objects.filter(trang_thai='DA_GIAO').count()} đơn")
    print(f"🔵 Đang giao      : {DonHang.objects.filter(trang_thai='DANG_GIAO').count()} đơn")
    print(f"🟡 Chưa giao      : {DonHang.objects.filter(trang_thai='CHUA_GIAO').count()} đơn")
    print("="*80)
    
    # In chi tiết địa chỉ
    print("\n📍 DANH SÁCH ĐỊA CHỈ CHI TIẾT:")
    print("-"*80)
    for order in DonHang.objects.all().order_by('ma_don'):
        print(f"  {order.ma_don} | {order.ten_khach:<22} | {order.dia_chi}")
    
    print("\n🎉 HOÀN THÀNH! Chạy lại server: python manage.py runserver")

if __name__ == "__main__":
    import_data()