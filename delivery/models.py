from django.db import models

class DonHang(models.Model):
    # Lựa chọn trạng thái đơn hàng
    TRANG_THAI_CHOICES = [
        ('CHUA_GIAO', 'Chưa giao'),
        ('DANG_GIAO', 'Đang giao'),
        ('DA_GIAO', 'Đã giao'),
    ]
    
    # 1. Thông tin cơ bản
    ma_don = models.CharField(
        "Mã đơn hàng", 
        max_length=20, 
        unique=True, 
        null=True, 
        blank=True
    )
    ten_khach = models.CharField("Tên khách hàng", max_length=100)
    so_dien_thoai = models.CharField(
        "Số điện thoại", 
        max_length=15, 
        null=True, 
        blank=True
    )
    dia_chi = models.TextField("Địa chỉ giao hàng", null=True, blank=True)
    
    # 2. Thông tin vị trí (Dùng cho thuật toán TSP)
    toa_do_x = models.FloatField("Tọa độ X (Kinh độ)", default=0.0)
    toa_do_y = models.FloatField("Tọa độ Y (Vĩ độ)", default=0.0)
    
    # 3. Thông tin khung giờ & Phục vụ 
    khung_gio_som = models.IntegerField("Giờ sớm nhất (0-24)", null=True, blank=True, default=8)
    khung_gio_muon = models.IntegerField("Giờ muộn nhất (0-24)", null=True, blank=True, default=18)
    thoi_gian_phuc_vu = models.IntegerField("TG phục vụ (phút)", null=True, blank=True, default=10)
    
    lat = models.FloatField(default=0.0)  # Vĩ độ
    lng = models.FloatField(default=0.0)  # Kinh độ
    
    # 4. Quản lý trạng thái và thời gian hệ thống
    trang_thai = models.CharField(
        "Trạng thái", 
        max_length=20, 
        choices=TRANG_THAI_CHOICES, 
        default='CHUA_GIAO'
    )
    ngay_tao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Danh sách Đơn hàng"
        ordering = ['-ngay_tao']

    def __str__(self):
        return f"{self.ma_don if self.ma_don else 'No ID'} - {self.ten_khach}"


# ========== THÊM MỚI: Model Cài đặt hệ thống ==========
class CaiDatHeThong(models.Model):
    """Lưu cài đặt hệ thống"""
    
    THUAT_TOAN_CHOICES = [
        ('greedy', 'Nearest Neighbor (Tham lam)'),
        ('clarke_wright', 'Clarke-Wright (Tiết kiệm)'),
        ('genetic', 'Genetic Algorithm (Di truyền)'),
    ]
    
    # Giá cước
    gia_cuoc_km = models.IntegerField("Giá cước (VNĐ/km)", default=5000)
    
    # Thời gian làm việc
    gio_bat_dau = models.IntegerField("Giờ bắt đầu làm việc", default=8)
    gio_ket_thuc = models.IntegerField("Giờ kết thúc làm việc", default=17)
    
    # Quản lý xe
    so_xe_toi_da = models.IntegerField("Số xe tối đa", default=3)
    tai_trong_toi_da = models.IntegerField("Tải trọng tối đa/xe (kg)", default=500)
    
    # Thuật toán
    thuat_toan_mac_dinh = models.CharField(
        "Thuật toán mặc định", 
        max_length=50, 
        choices=THUAT_TOAN_CHOICES, 
        default='greedy'
    )
    
    # Chế độ tự động
    tu_dong_toi_uu = models.BooleanField("Tự động tối ưu lộ trình", default=False)
    
    # Thời gian cập nhật
    cap_nhat_luc = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Cài đặt hệ thống"
        verbose_name_plural = "Cài đặt hệ thống"
    
    def __str__(self):
        return f"Cài đặt hệ thống (cập nhật: {self.cap_nhat_luc.strftime('%d/%m/%Y %H:%M')})"
    
    @classmethod
    def get_settings(cls):
        """Lấy cài đặt (chỉ có 1 bản ghi duy nhất)"""
        settings = cls.objects.first()
        if not settings:
            settings = cls.objects.create()
        return settings