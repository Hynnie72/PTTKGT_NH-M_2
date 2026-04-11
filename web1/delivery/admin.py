from django.contrib import admin
from .models import DonHang

@admin.register(DonHang)
class DonHangAdmin(admin.ModelAdmin):
    # Sửa lại danh sách hiển thị ở đây
    list_display = (
        'ma_don', 
        'ten_khach', 
        'so_dien_thoai', 
        'khung_gio_som',   # Thay cho bat_dau
        'khung_gio_muon',  # Thay cho ket_thuc
        'trang_thai'
    )
    search_fields = ('ma_don', 'ten_khach', 'so_dien_thoai')
    list_filter = ('trang_thai',)