from django.urls import path
from django.contrib.auth import views as auth_views
from delivery import views
from django.contrib import admin

urlpatterns = [
    # Quản trị hệ thống
    path('admin/', admin.site.urls),

    # Trang chính Dashboard
    path('', views.index, name='index'),
    path('dashboard/', views.index, name='dashboard'),
    
    # Quản lý đơn hàng
    path('tao-don/', views.tao_don, name='tao_don'),
    path('tao-don-moi/', views.tao_don_moi, name='tao_don_moi'),
    path('don-hang/', views.danh_sach_don_hang, name='danh_sach_don_hang'),
    path('thong-tin-don-hang/', views.danh_sach_don_hang, name='thong_tin_don_hang'),
    
    # Xóa và sửa đơn hàng (dùng JSON cho modal)
    path('xoa-don/<int:order_id>/', views.xoa_don, name='xoa_don'),
    path('sua-don/<int:order_id>/', views.sua_don, name='sua_don'),
    
    # Cài đặt hệ thống
    path('cai-dat/', views.cai_dat, name='cai_dat'),
    path('settings/', views.cai_dat, name='settings'),
    
    # Xuất dữ liệu
    path('xuat-excel/', views.xuat_excel, name='xuat_excel'),
    path('export-excel/', views.xuat_excel, name='export_excel'),
    
    # Bản đồ
    path('map/', views.ban_do_giao_hang, name='view_map'),
    path('ban-do/', views.ban_do_giao_hang, name='ban_do'),
    
    # Lịch sử giao hàng
    path('lich-su/', views.lich_su_giao_hang, name='lich_su'),
    
    # Tài khoản
    path('dang-ky/', views.dang_ky, name='register'),
    path('dang-ky-tai-khoan/', views.dang_ky, name='dang_ky'),
    path('login/', auth_views.LoginView.as_view(template_name='delivery/login.html'), name='login'),
    path('dang-nhap/', auth_views.LoginView.as_view(template_name='delivery/login.html'), name='dang_nhap'),
    path('logout/', views.dang_xuat, name='logout'),
    path('dang-xuat/', views.dang_xuat, name='dang_xuat'),
]