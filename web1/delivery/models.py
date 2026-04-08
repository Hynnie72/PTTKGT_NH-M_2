from django.db import models

class DonHang(models.Model):
    # Lựa chọn trạng thái đơn hàng
    TRANG_THAI_CHOICES = [
        ('CHUA_GIAO', 'Chưa giao'),
        ('DANG_GIAO', 'Đang giao'),
        ('DA_GIAO', 'Đã giao'),
    ]
    
    # 1. Thông tin cơ bản (Cho phép null/blank để tránh lỗi migrate dữ liệu cũ)
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
    # Tọa độ X, Y (Kinh độ, Vĩ độ)
    toa_do_x = models.FloatField("Tọa độ X (Kinh độ)", default=0.0)
    toa_do_y = models.FloatField("Tọa độ Y (Vĩ độ)", default=0.0)
    
    # 3. Thông tin khung giờ & Phục vụ (Time Windows)
    khung_gio_som = models.IntegerField("Giờ sớm nhất (0-24)", default=8)
    khung_gio_muon = models.IntegerField("Giờ muộn nhất (0-24)", default=18)
    thoi_gian_phuc_vu = models.IntegerField("TG phục vụ (phút)", default=10)
    
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
        ordering = ['-ngay_tao'] # Đơn mới nhất hiện lên đầu

    def __str__(self):
        return f"{self.ma_don if self.ma_don else 'No ID'} - {self.ten_khach}"