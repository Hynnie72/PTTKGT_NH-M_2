from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
# CHỈNH SỬA TẠI ĐÂY: Import views từ app 'delivery' thay vì dùng dấu chấm '.'
from delivery import views 

urlpatterns = [
    # Quản trị hệ thống (Mặc định của Django)
    path('admin/', admin.site.urls),

    # Trang chính Dashboard (Nơi chứa Bản đồ)
    path('', views.index, name='index'),
    
    # Quản lý đơn hàng
    path('tao-don/', views.tao_don, name='tao_don'),
    path('don-hang/', views.danh_sach_don_hang, name='danh_sach_don_hang'),
    
    # Xuất dữ liệu
    path('xuat-excel/', views.xuat_excel, name='xuat_excel'),
    
    # Tài khoản
    path('dang-ky/', views.dang_ky, name='register'),
    # Lưu ý: template_name trỏ vào thư mục delivery/login.html
    path('login/', auth_views.LoginView.as_view(template_name='delivery/login.html'), name='login'),
    path('logout/', views.dang_xuat, name='logout'),
]