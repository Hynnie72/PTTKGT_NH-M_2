from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import DonHang, CaiDatHeThong
from .solver import solve_greedy
import csv
import time
import json
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
    
    # Lấy cài đặt hệ thống
    settings = CaiDatHeThong.get_settings()
    
    # Lấy tham số tìm kiếm nhanh
    query = request.GET.get('q', '')
    
    # Lấy danh sách đơn hàng chưa giao (thay vì đơn hàng gần đây)
    if query:
        pending_orders = DonHang.objects.filter(
            Q(ma_don__icontains=query) | 
            Q(ten_khach__icontains=query),
            trang_thai='CHUA_GIAO'
        ).order_by('-ngay_tao')
    else:
        pending_orders = DonHang.objects.filter(trang_thai='CHUA_GIAO').order_by('-ngay_tao')
    
    # Thống kê số lượng theo trạng thái
    total = DonHang.objects.count()
    chua_giao = DonHang.objects.filter(trang_thai='CHUA_GIAO').count()
    da_giao = DonHang.objects.filter(trang_thai='DA_GIAO').count()
    
    # Tính tỷ lệ hoàn thành
    ty_le_hoan_thanh = round((da_giao / total * 100) if total > 0 else 0, 1)
    
    # Khởi tạo biến kết quả tối ưu
    route_result = None
    route_json = None
    total_dist = 0
    total_cost = 0
    optimized_cost = 0
    saved_cost = 0
    total_time = None
    runtime = None
    error = None

    # Tọa độ Kho thực tế (Võ Oanh, Bình Thạnh)
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
            
            # Tạo danh sách lộ trình chi tiết kèm khoảng cách
            route_result = []
            route_for_map = []
            
            # Điểm xuất phát là Kho
            route_for_map.append({'ten': 'KHO TRUNG TÂM', 'lat': KHO_LAT, 'lng': KHO_LNG})
            
            # Điểm hiện tại bắt đầu từ Kho
            prev_lat, prev_lng = KHO_LAT, KHO_LNG

            for i, point in enumerate(route):
                dist_from_prev = haversine(prev_lat, prev_lng, point.lat, point.lng)
                
                total_dist += dist_from_prev
                route_result.append({
                    'ten_khach': point.ten_khach,
                    'ma_don': point.ma_don,
                    'dia_chi': point.dia_chi,
                    'distance': round(dist_from_prev, 2)
                })
            
                route_for_map.append({
                    'ten': point.ten_khach,
                    'lat': point.lat,
                    'lng': point.lng
                })

                prev_lat, prev_lng = point.lat, point.lng

            # Thêm khoảng cách từ điểm cuối về kho
            if route:
                dist_back = haversine(prev_lat, prev_lng, KHO_LAT, KHO_LNG)
                total_dist = round(total_dist + dist_back, 2)
                total_time = round(total_dist * 5, 1)  # Giả sử 5 phút/km
                
                # ========== TÍNH CHI PHÍ ==========
                # Chi phí thực tế (nếu chạy theo thứ tự ngẫu nhiên)
                # Giả sử chi phí chưa tối ưu cao hơn 30%
                random_dist = round(total_dist * 1.3, 2)
                total_cost = random_dist * settings.gia_cuoc_km
                optimized_cost = total_dist * settings.gia_cuoc_km
                saved_cost = total_cost - optimized_cost
                
                route_json = json.dumps(route_for_map)
        else:
            error = "Không có đơn hàng nào chờ giao!"

    context = {
        'query': query,
        'pending_orders': pending_orders,  # Đơn hàng chưa giao thay vì gần đây
        'thong_ke': {
            'tong': total,
            'chua_giao': chua_giao,
            'da_giao': da_giao,
            'ty_le_hoan_thanh': ty_le_hoan_thanh,
        },
        'route_result': route_result,
        'route_json': route_json,
        'total_dist': total_dist,
        'total_cost': total_cost,
        'optimized_cost': optimized_cost,
        'saved_cost': saved_cost,
        'total_time': total_time,
        'runtime': runtime,
        'error': error,
        'chua_giao_count': chua_giao,
        'gia_cuoc': settings.gia_cuoc_km,  # Truyền giá cước sang template
    }
    
    return render(request, 'delivery/index.html', context)


@login_required
def danh_sach_don_hang(request):
    """Trang thông tin đơn hàng - Danh sách tất cả đơn hàng (có xóa và sửa)"""
    
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


# ========== THÊM MỚI: Xóa đơn hàng ==========
@login_required
def xoa_don(request, order_id):
    """Xóa đơn hàng theo ID"""
    if request.method == 'POST':
        order = get_object_or_404(DonHang, id=order_id)
        order.delete()
        
        # Nếu là AJAX request, trả về JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Đã xóa đơn hàng!'})
        
        return redirect('danh_sach_don_hang')
    
    return redirect('danh_sach_don_hang')


# ========== THÊM MỚI: Sửa đơn hàng ==========
@login_required
def sua_don(request, order_id):
    """Sửa đơn hàng"""
    order = get_object_or_404(DonHang, id=order_id)
    
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        order.ten_khach = request.POST.get('ten_khach', order.ten_khach)
        order.so_dien_thoai = request.POST.get('so_dien_thoai', order.so_dien_thoai)
        order.dia_chi = request.POST.get('dia_chi', order.dia_chi)
        order.lat = float(request.POST.get('lat', order.lat))
        order.lng = float(request.POST.get('lng', order.lng))
        order.toa_do_x = order.lng  # Đồng bộ
        order.toa_do_y = order.lat  # Đồng bộ
        order.trang_thai = request.POST.get('trang_thai', order.trang_thai)
        
        order.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Đã cập nhật đơn hàng!'})
        
        return redirect('danh_sach_don_hang')
    
    return render(request, 'delivery/sua_don_modal.html', {'order': order})


# ========== THÊM MỚI: Tạo đơn hàng mới (bỏ 3 trường thời gian) ==========
@login_required
def tao_don_moi(request):
    """Tạo đơn hàng mới - KHÔNG có khung giờ và thời gian phục vụ"""
    
    if request.method == 'POST':
        # Tạo mã đơn tự động
        last_order = DonHang.objects.order_by('-id').first()
        if last_order and last_order.ma_don:
            try:
                last_num = int(last_order.ma_don.replace('DH', ''))
                new_num = last_num + 1
            except:
                new_num = 1
        else:
            new_num = 1
        
        ma_don_moi = f"DH{new_num:03d}"
        
        # Tạo đơn hàng mới (bỏ qua khung_gio_som, khung_gio_muon, thoi_gian_phuc_vu)
        order = DonHang.objects.create(
            ma_don=ma_don_moi,
            ten_khach=request.POST.get('ten_khach'),
            so_dien_thoai=request.POST.get('so_dien_thoai', ''),
            dia_chi=request.POST.get('dia_chi', ''),
            lat=float(request.POST.get('lat', 0)),
            lng=float(request.POST.get('lng', 0)),
            toa_do_x=float(request.POST.get('lng', 0)),
            toa_do_y=float(request.POST.get('lat', 0)),
            trang_thai='CHUA_GIAO'
        )
        
        return redirect('danh_sach_don_hang')
    
    return render(request, 'delivery/tao_don.html')


# ========== THÊM MỚI: Cài đặt hệ thống ==========
@login_required
def cai_dat(request):
    """Trang cài đặt hệ thống"""
    settings = CaiDatHeThong.get_settings()
    
    if request.method == 'POST':
        settings.gia_cuoc_km = int(request.POST.get('gia_cuoc_km', 5000))
        settings.gio_bat_dau = int(request.POST.get('gio_bat_dau', 8))
        settings.gio_ket_thuc = int(request.POST.get('gio_ket_thuc', 17))
        settings.so_xe_toi_da = int(request.POST.get('so_xe_toi_da', 3))
        settings.tai_trong_toi_da = int(request.POST.get('tai_trong_toi_da', 500))
        settings.thuat_toan_mac_dinh = request.POST.get('thuat_toan_mac_dinh', 'greedy')
        settings.tu_dong_toi_uu = request.POST.get('tu_dong_toi_uu') == 'on'
        settings.save()
        
        return redirect('cai_dat')
    
    context = {
        'settings': settings,
    }
    return render(request, 'delivery/cai_dat.html', context)


@login_required
def xuat_excel(request):
    """Xuất danh sách đơn hàng ra file CSV"""
    
    # Lọc theo loại nếu có
    loai = request.GET.get('loai', '')
    if loai == 'da_giao':
        orders = DonHang.objects.filter(trang_thai='DA_GIAO').order_by('-ngay_tao')
    else:
        orders = DonHang.objects.all().order_by('-ngay_tao')
    
    response = HttpResponse(content_type='text/csv')
    filename = f'don_hang_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    
    # Ghi header
    writer.writerow([
        'STT', 'Mã đơn hàng', 'Tên khách hàng', 'Số điện thoại',
        'Địa chỉ', 'Tọa độ Lat', 'Tọa độ Lng', 'Trạng thái', 'Ngày tạo'
    ])
    
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
            order.lat,
            order.lng,
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
    """Chuyển hướng đến trang tạo đơn mới"""
    return redirect('tao_don_moi')


def ban_do_giao_hang(request):
    return render(request, 'delivery/index.html')