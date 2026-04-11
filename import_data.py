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

def import_from_file(file_path):
    ten_cac_diem = ["Kho (Bình Thạnh)", "Quận 1", "Quận 3", "Quận 4", "Quận 5", "Quận 6", "Quận 8", "Quận 10"]

    if not os.path.exists(file_path):
        print(f"Không tìm thấy file tại: {file_path}")
        return

    print("--- Đang làm sạch dữ liệu cũ... ---")
    DonHang.objects.all().delete()

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            data_lines = lines[1:] 

            for index, line in enumerate(data_lines):
                parts = line.split()
                if len(parts) >= 2:
                    lat_val = float(parts[0])
                    lng_val = float(parts[1])
                    ten_diem = ten_cac_diem[index] if index < len(ten_cac_diem) else f"Điểm {index+1}"

                    # SỬA LỖI TẠI ĐÂY: Dùng update_or_create hoặc tạo mới cẩn thận
                    obj = DonHang(
                        ma_don=f"DH{index+1:03d}",
                        ten_khach=ten_diem,
                        dia_chi=f"Khu vực {ten_diem}",
                        lat=lat_val,
                        lng=lng_val,
                        trang_thai='CHUA_GIAO'
                    )
                    obj.save() # Lưu trực tiếp để đảm bảo nhận field mới
                    
                    print(f"Đã nạp: {ten_diem} | Tọa độ: {lat_val}, {lng_val}")

        print("--- HOÀN THÀNH: Đã nạp xong 8 quận! ---")
    
    except Exception as e:
        print(f" Có lỗi xảy ra: {e}")
        print("💡 Mẹo: Hãy chạy 'python manage.py migrate' trước khi chạy file này!")

if __name__ == "__main__":
    PATH_TO_DATA = os.path.join(BASE_DIR, 'data.txt')
    import_from_file(PATH_TO_DATA)