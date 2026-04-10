from django.contrib import admin
from .models import DonHang, CaiDatHeThong

@admin.register(DonHang)
class DonHangAdmin(admin.ModelAdmin):
    list_display = (
        'ma_don', 
        'ten_khach', 
        'so_dien_thoai', 
        'trang_thai'
    )
    search_fields = ('ma_don', 'ten_khach', 'so_dien_thoai')
    list_filter = ('trang_thai',)


# ========== THÊM MỚI: Admin cho Cài đặt hệ thống ==========
@admin.register(CaiDatHeThong)
class CaiDatHeThongAdmin(admin.ModelAdmin):
    list_display = ('gia_cuoc_km', 'gio_bat_dau', 'gio_ket_thuc', 'so_xe_toi_da', 'thuat_toan_mac_dinh')
    fieldsets = (
        ('💰 Giá cước vận chuyển', {
            'fields': ('gia_cuoc_km',)
        }),
        ('⏰ Thời gian làm việc', {
            'fields': ('gio_bat_dau', 'gio_ket_thuc')
        }),
        ('🚚 Quản lý đội xe', {
            'fields': ('so_xe_toi_da', 'tai_trong_toi_da')
        }),
        ('🤖 Thuật toán & Tự động hóa', {
            'fields': ('thuat_toan_mac_dinh', 'tu_dong_toi_uu')
        }),
    )
    
    def has_add_permission(self, request):
        # Chỉ cho phép có 1 bản ghi duy nhất
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)