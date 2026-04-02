from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Q, Count
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import DonHang
from .solver import solve_greedy
import csv
import time
import json # #### THÊM MỚI: Để truyền dữ liệu tọa độ sang JavaScript của Map ####
import math
# --- HÀM BỔ TRỢ: Tính khoảng cách giữa 2 tọa độ (Haversine) ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Bán kính Trái Đất tính bằng km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return round(R * c, 2)


@login_required
def index(request):
    """Dashboard - Trang chính với công cụ tối ưu lộ trình"""
    
    # Lấy tham số tìm kiếm nhanh
    query = request.GET.get('q', '')
    
    # Lấy danh sách đơn hàng gần đây (10 đơn mới nhất)
    if query:
        recent_orders = DonHang.objects.filter(
            Q(ma_don__icontains=query) | 
            Q(ten_khach__icontains=query)
        ).order_by('-ngay_tao')[:10]
    else:
        recent_orders = DonHang.objects.all().order_by('-ngay_tao')[:10]
    
    # Thống kê số lượng theo trạng thái
    total = DonHang.objects.count()
    chua_giao = DonHang.objects.filter(trang_thai='CHUA_GIAO').count()
    da_giao = DonHang.objects.filter(trang_thai='DA_GIAO').count()
    
    # Tính tỷ lệ hoàn thành
    ty_le_hoan_thanh = round((da_giao / total * 100) if total > 0 else 0, 1)
    
    # Khởi tạo biến kết quả tối ưu
    route_result = None
    route_json = None # #### THÊM MỚI: Biến lưu danh sách tọa độ để vẽ đường màu xanh ####
    total_dist = 0 # #### CHỈNH SỬA: Gán mặc định là 0 để tránh lỗi cộng dồn ####
    total_time = None
    runtime = None
    error = None

    # #### THÊM MỚI: Tọa độ Kho thực tế (Võ Oanh, Bình Thạnh) thay vì 0,0 ####
    KHO_LAT = 10.802
    KHO_LNG = 106.713
    
    # Xử lý chạy tối ưu lộ trình
    if request.GET.get('optimize'):
        pending = list(DonHang.objects.filter(trang_thai='CHUA_GIAO'))
        
        if pending:
            start_t = time.time()
            # Sử dụng thuật toán tham lam (Nearest Neighbor)
            route, dist = solve_greedy(pending)
            runtime = round(time.time() - start_t, 5)
            total_dist = round(dist, 2)
            total_time = round(dist * 5, 1)  # Giả sử tốc độ trung bình 12km/h (5 phút/km)
            
            # Tạo danh sách lộ trình chi tiết kèm khoảng cách
            route_result = []
            route_for_map = [] # #### THÊM MỚI: Danh sách để vẽ lên Leaflet ####
            # #### THÊM MỚI: Điểm xuất phát là Kho thực tế vào danh sách Map ####
            route_for_map.append({'ten': 'KHO TRUNG TÂM', 'lat': KHO_LAT, 'lng': KHO_LNG})
            
            # Điểm hiện tại bắt đầu từ Kho
            prev_lat, prev_lng = KHO_LAT, KHO_LNG

            for i, point in enumerate(route):
                # Tính khoảng cách từ điểm trước đến điểm hiện tại
                #if i == 0:
                    # Khoảng cách từ kho đến điểm đầu tiên
                    #dist_from_prev = round(((point.toa_do_x ** 2 + point.toa_do_y ** 2) ** 0.5), 1)
                #else:
                    # Khoảng cách từ điểm trước đến điểm hiện tại
                   #dist_from_prev = round(((point.toa_do_x - prev.toa_do_x) ** 2 + (point.toa_do_y - prev.toa_do_y) ** 2) ** 0.5, 1)

                # #### CHỈNH SỬA: Tính khoảng cách dựa trên tọa độ thực GPS ####
                # Công thức: d = sqrt((y2-y1)^2 + (x2-x1)^2) * 111 (quy đổi độ sang km)
                d = ((point.toa_do_y - prev_lat)**2 + (point.toa_do_x - prev_lng)**2)**0.5
                dist_from_prev = round(d * 111, 2) # 111 là hệ số km/độ xấp xỉ
                
                total_dist += dist_from_prev
                route_result.append({
                    'ten_khach': point.ten_khach,
                    'ma_don': point.ma_don,
                    'dia_chi': point.dia_chi,
                    'distance': dist_from_prev
                })
            
              # #### THÊM MỚI: Đưa điểm vào danh sách vẽ Map ####
                route_for_map.append({
                    'ten': point.ten_khach,
                    'lat': point.toa_do_y,
                    'lng': point.toa_do_x
                })

                # Cập nhật điểm trước đó cho lần lặp sau
                prev_lat, prev_lng = point.toa_do_y, point.toa_do_x

            # Thêm khoảng cách từ điểm cuối về kho
            #if route:
                #last_point = route[-1]
               # dist_back = round(((last_point.toa_do_x ** 2 + last_point.toa_do_y ** 2) ** 0.5), 1)
                #total_dist += dist_back
                #total_time = round(total_dist * 5, 1)
        #else:
           # error = "Không có đơn hàng nào chờ giao!"
            
             # Thêm khoảng cách từ điểm cuối về kho
            if route:
                dist_back = round((((KHO_LAT - prev_lat)**2 + (KHO_LNG - prev_lng)**2)**0.5) * 111, 2)
                total_dist = round(total_dist + dist_back, 2)
                total_time = round(total_dist * 5, 1) # Giả sử 5 phút/km
                
                # #### THÊM MỚI: Chuyển dữ liệu sang JSON để JavaScript sử dụng ####
                route_json = json.dumps(route_for_map)
        else:
            error = "Không có đơn hàng nào chờ giao!"

    context = {
        'query': query,
        'recent_orders': recent_orders,
        'thong_ke': {
            'tong': total,
            'chua_giao': chua_giao,
            'da_giao': da_giao,
            'ty_le_hoan_thanh': ty_le_hoan_thanh,
        },
        'route_result': route_result,
        'total_dist': total_dist,
        'total_time': total_time,
        'runtime': runtime,
        'error': error,
        'chua_giao_count': chua_giao,
    }
    
    return render(request, 'delivery/index.html', context)


@login_required
def danh_sach_don_hang(request):
    """Trang thông tin đơn hàng - Danh sách tất cả đơn hàng"""
    
    # Lấy tham số tìm kiếm
    query = request.GET.get('q', '')
    # Lấy tham số lọc trạng thái
    trang_thai_filter = request.GET.get('trang_thai', '')
    
    # Lọc đơn hàng
    orders = DonHang.objects.all()
    
    if query:
        orders = orders.filter(
            Q(ma_don__icontains=query) | 
            Q(ten_khach__icontains=query) |
            Q(so_dien_thoai__icontains=query)
        )
    
    if trang_thai_filter and trang_thai_filter != 'TAT_CA':
        orders = orders.filter(trang_thai=trang_thai_filter)
    
    # Sắp xếp theo ngày tạo mới nhất
    orders = orders.order_by('-ngay_tao')
    
    # Thống kê số lượng theo trạng thái
    thong_ke = {
        'tong': DonHang.objects.count(),
        'chua_giao': DonHang.objects.filter(trang_thai='CHUA_GIAO').count(),
        'dang_giao': DonHang.objects.filter(trang_thai='DANG_GIAO').count(),
        'da_giao': DonHang.objects.filter(trang_thai='DA_GIAO').count(),
    }
    
    context = {
        'orders': orders,
        'query': query,
        'trang_thai_filter': trang_thai_filter,
        'thong_ke': thong_ke,
    }
    
    return render(request, 'delivery/don_hang.html', context)


@login_required
def xuat_excel(request):
    """Xuất danh sách đơn hàng ra file CSV"""
    
    orders = DonHang.objects.all().order_by('-ngay_tao')
    
    # Tạo response
    response = HttpResponse(content_type='text/csv')
    filename = f'don_hang_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    
    # Ghi header
    writer.writerow([
        'STT', 'Mã đơn hàng', 'Tên khách hàng', 'Số điện thoại',
        'Địa chỉ', 'Tọa độ X', 'Tọa độ Y', 'Khung giờ sớm',
        'Khung giờ muộn', 'Thời gian phục vụ (phút)', 'Trạng thái', 'Ngày tạo'
    ])
    
    # Ghi dữ liệu
    trang_thai_map = {
        'CHUA_GIAO': 'Chưa giao',
        'DANG_GIAO': 'Đang giao',
        'DA_GIAO': 'Đã giao'
    }
    
    for idx, order in enumerate(orders, 1):
        writer.writerow([
            idx,
            order.ma_don or '',
            order.ten_khach,
            order.so_dien_thoai or '',
            order.dia_chi or '',
            order.toa_do_x,
            order.toa_do_y,
            order.khung_gio_som,
            order.khung_gio_muon,
            order.thoi_gian_phuc_vu,
            trang_thai_map.get(order.trang_thai, order.trang_thai),
            order.ngay_tao.strftime('%d/%m/%Y %H:%M') if order.ngay_tao else ''
        ])
    
    return response


# --- CÁC VIEW XỬ LÝ TÀI KHOẢN ---

def dang_ky(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'delivery/register.html', {'form': form})


def dang_xuat(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('index')


@login_required
def tao_don(request):
    """Admin có thể truy cập thẳng trang thêm đơn"""
    if request.user.is_staff:
        return redirect('/admin/delivery/donhang/add/')
    else:
        return redirect('index')
def ban_do_giao_hang(request):
    # Hàm này chỉ để trả về giao diện bản đồ
    return render(request, 'delivery/index.html')