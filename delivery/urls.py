from django.urls import path
from django.contrib.auth import views as auth_views
from delivery import views
from django.contrib import admin

urlpatterns = [
    # Quản trị hệ thống
    path('admin/', admin.site.urls),  # nếu thiếu thì thêm dòng: from django.contrib import admin

    # Trang chính Dashboard
    path('', views.index, name='index'),
    
    # Quản lý đơn hàng
    path('tao-don/', views.tao_don, name='tao_don'),
    path('tao-don-moi/', views.tao_don_moi, name='tao_don_moi'),
    path('don-hang/', views.danh_sach_don_hang, name='danh_sach_don_hang'),
    
    # Xóa và sửa đơn hàng
    path('xoa-don/<int:order_id>/', views.xoa_don, name='xoa_don'),
    path('sua-don/<int:order_id>/', views.sua_don, name='sua_don'),
    
    # Cài đặt hệ thống
    path('cai-dat/', views.cai_dat, name='cai_dat'),
    
    # Xuất dữ liệu
    path('xuat-excel/', views.xuat_excel, name='xuat_excel'),
    
    # Bản đồ
    path('map/', views.ban_do_giao_hang, name='view_map'),
    
    # Tài khoản
    path('dang-ky/', views.dang_ky, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='delivery/login.html'), name='login'),
    path('logout/', views.dang_xuat, name='logout'),
]