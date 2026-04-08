"""
URL configuration for web1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from delivery import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    # 1. Trang quản trị admin
    path('admin/', admin.site.urls),

    # 2. Trang chủ Dashboard (Hàm index trong views.py)
    path('', views.index, name='index'),

    # 3. Các chức năng quản lý đơn hàng
    path('tao-don/', views.tao_don, name='tao_don'),
    path('don-hang/', views.danh_sach_don_hang, name='danh_sach_don_hang'),
    
    # 4. Xuất dữ liệu Excel
    path('xuat-excel/', views.xuat_excel, name='xuat_excel'),
    
    # 5. Bản đồ (Nếu Thịnh muốn dùng đường dẫn /map/)
    path('map/', views.ban_do_giao_hang, name='view_map'),

    # 6. Tài khoản (Đăng nhập/Đăng xuất)
    # Lưu ý: template_name phải khớp với thư mục trong templates của bạn
    path('login/', auth_views.LoginView.as_view(template_name='delivery/login.html'), name='login'),
    path('logout/', views.dang_xuat, name='logout'),
    path('dang-ky/', views.dang_ky, name='register'),
]