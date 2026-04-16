from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import DonHang, CaiDatHeThong
from .solver import solve_greedy
import csv
import time
import json
import math

# Hàm bổ trợ: Tính khoảng cách giữa 2 tọa độ (Haversine)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return round(R * c, 2)


@login_required
def index(request):
    """Dashboard - Trang chính với công cụ tối ưu lộ trình"""
    
    settings = CaiDatHeThong.get_settings()
    query = request.GET.get('q', '')
    
    # Lấy danh sách đơn hàng chưa giao
    if query:
        pending_orders = DonHang.objects.filter(
            Q(ma_don__icontains=query) | Q(ten_khach__icontains=query),
            trang_thai='CHUA_GIAO'
        ).order_by('-ngay_tao')
    else:
        pending_orders = DonHang.objects.filter(trang_thai='CHUA_GIAO').order_by('-ngay_tao')
    
    # ========== THỐNG KÊ CHÍNH XÁC TỪ DATABASE ==========
    total = DonHang.objects.count()
    chua_giao = DonHang.objects.filter(trang_thai='CHUA_GIAO').count()
    dang_giao = DonHang.objects.filter(trang_thai='DANG_GIAO').count()
    da_giao = DonHang.objects.filter(trang_thai='DA_GIAO').count()
    
    # Tính tỷ lệ hoàn thành
    ty_le_hoan_thanh = round((da_giao / total * 100) if total > 0 else 0, 1)
    
    # ========== DOANH THU DỰ KIẾN ==========
    KM_TRUNG_BINH_MOI_DON = 10  # Trung bình mỗi đơn 10km
    doanh_thu_du_kien = chua_giao * KM_TRUNG_BINH_MOI_DON * settings.gia_cuoc_km
    # ========== TÍNH CHI PHÍ VẬN CHUYỂN ==========
    UOC_LUONG_KM_MOI_DON = 8
    
    tong_km_co_ban = chua_giao * UOC_LUONG_KM_MOI_DON
    tong_km_chua_toi_uu = tong_km_co_ban * 1.3
    tong_km_da_toi_uu = tong_km_co_ban
    
    tong_chua_toi_uu = tong_km_chua_toi_uu * settings.gia_cuoc_km
    tong_da_toi_uu = tong_km_da_toi_uu * settings.gia_cuoc_km
    tong_tiet_kiem = tong_chua_toi_uu - tong_da_toi_uu
    ty_le_tiet_kiem = (tong_tiet_kiem / tong_chua_toi_uu * 100) if tong_chua_toi_uu > 0 else 0
    
    # Khởi tạo biến với giá trị mặc định
    route_result = None
    route_json = "null"
    total_dist = 0
    total_cost = 0
    optimized_cost = 0
    saved_cost = 0
    saved_percent = 0
    total_time = None
    runtime = None
    error = None

    KHO_LAT = 10.802
    KHO_LNG = 106.713
    
    # Xử lý chạy tối ưu lộ trình
    if request.GET.get('optimize'):
        pending = list(DonHang.objects.filter(trang_thai='CHUA_GIAO'))
        
        if pending:
            start_t = time.time()
            route, dist = solve_greedy(pending)
            runtime = round(time.time() - start_t, 5)
            
            route_result = []
            route_for_map = []
            route_for_map.append({'ten': 'KHO TRUNG TÂM', 'lat': KHO_LAT, 'lng': KHO_LNG})
            
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

            if route:
                dist_back = haversine(prev_lat, prev_lng, KHO_LAT, KHO_LNG)
                total_dist = round(total_dist + dist_back, 2)
                total_time = round(total_dist * 5, 1)
                
                random_dist = round(total_dist * 1.3, 2)
                total_cost = random_dist * settings.gia_cuoc_km
                optimized_cost = total_dist * settings.gia_cuoc_km
                saved_cost = total_cost - optimized_cost
                saved_percent = round((saved_cost / total_cost * 100) if total_cost > 0 else 0, 1)
                route_json = json.dumps(route_for_map, ensure_ascii=False)
        else:
            error = "Không có đơn hàng nào chờ giao!"

    # Lấy thông tin thuật toán hiển thị
    thuat_toan_display = dict(CaiDatHeThong.THUAT_TOAN_CHOICES).get(settings.thuat_toan_mac_dinh, "Nearest Neighbor")

    context = {
        'query': query,
        'pending_orders': pending_orders,
        'pending_count': chua_giao,
        'thong_ke': {
            'tong': total,
            'chua_giao': chua_giao,
            'dang_giao': dang_giao,
            'da_giao': da_giao,
            'ty_le_hoan_thanh': ty_le_hoan_thanh,
        },
        'route_result': route_result,
        'route_json': route_json,
        'total_dist': total_dist,
        'total_cost': total_cost,
        'optimized_cost': optimized_cost,
        'saved_cost': saved_cost,
        'saved_percent': saved_percent,
        'total_time': total_time,
        'runtime': runtime,
        'error': error,
        'chua_giao_count': chua_giao,
        'gia_cuoc': settings.gia_cuoc_km,
        'settings': settings,
        'doanh_thu_du_kien': doanh_thu_du_kien,
        'revenue_estimate': doanh_thu_du_kien,
        'tong_chua_toi_uu': tong_chua_toi_uu,
        'tong_da_toi_uu': tong_da_toi_uu,
        'tong_tiet_kiem': tong_tiet_kiem,
        'ty_le_tiet_kiem': ty_le_tiet_kiem,
        'tong_km_chua_toi_uu': tong_km_chua_toi_uu,
        'tong_km_da_toi_uu': tong_km_da_toi_uu,
        # ========== THÔNG TIN VẬN HÀNH ==========
        'tai_trong': settings.tai_trong_toi_da,
        'so_xe': settings.so_xe_toi_da,
        'gio_bat_dau': settings.gio_bat_dau,
        'gio_ket_thuc': settings.gio_ket_thuc,
        'thuat_toan': thuat_toan_display,
        'now': datetime.now(),
    }
    
    return render(request, 'delivery/index.html', context)


@login_required
def danh_sach_don_hang(request):
    """Trang thông tin đơn hàng - Danh sách tất cả đơn hàng"""
    
    query = request.GET.get('q', '')
    trang_thai_filter = request.GET.get('trang_thai', '')
    
    orders = DonHang.objects.all()
    
    if query:
        orders = orders.filter(
            Q(ma_don__icontains=query) | 
            Q(ten_khach__icontains=query) |
            Q(so_dien_thoai__icontains=query)
        )
    
    if trang_thai_filter and trang_thai_filter != 'TAT_CA':
        orders = orders.filter(trang_thai=trang_thai_filter)
    
    orders = orders.order_by('-ngay_tao')
    
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
def xoa_don(request, order_id):
    """Xóa đơn hàng theo ID"""
    if request.method == 'POST':
        order = get_object_or_404(DonHang, id=order_id)
        order.delete()
        return redirect('danh_sach_don_hang')
    
    return redirect('danh_sach_don_hang')


@login_required
def sua_don(request, order_id):
    """Sửa đơn hàng - Nhận POST từ modal, trả về JSON cho AJAX"""
    order = get_object_or_404(DonHang, id=order_id)
    
    if request.method == 'POST':
        # Cập nhật đơn hàng
        order.ten_khach = request.POST.get('ten_khach', order.ten_khach)
        order.so_dien_thoai = request.POST.get('so_dien_thoai', order.so_dien_thoai)
        order.dia_chi = request.POST.get('dia_chi', order.dia_chi)
        order.lat = float(request.POST.get('lat', order.lat))
        order.lng = float(request.POST.get('lng', order.lng))
        order.trang_thai = request.POST.get('trang_thai', order.trang_thai)
        order.save()
        
        # Nếu là AJAX request, trả về JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Đã cập nhật đơn hàng!'})
        
        return redirect('danh_sach_don_hang')
    
    # GET request: trả về dữ liệu dạng JSON cho modal
    data = {
        'id': order.id,
        'ma_don': order.ma_don,
        'ten_khach': order.ten_khach,
        'so_dien_thoai': order.so_dien_thoai or '',
        'dia_chi': order.dia_chi or '',
        'lat': float(order.lat),
        'lng': float(order.lng),
        'trang_thai': order.trang_thai,
    }
    return JsonResponse(data)


@login_required
def tao_don_moi(request):
    """Tạo đơn hàng mới"""
    
    if request.method == 'POST':
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
        
        order = DonHang.objects.create(
            ma_don=ma_don_moi,
            ten_khach=request.POST.get('ten_khach'),
            so_dien_thoai=request.POST.get('so_dien_thoai', ''),
            dia_chi=request.POST.get('dia_chi', ''),
            lat=float(request.POST.get('lat', 0)),
            lng=float(request.POST.get('lng', 0)),
            trang_thai='CHUA_GIAO'
        )
        
        return redirect('danh_sach_don_hang')
    
    return render(request, 'delivery/tao_don.html')


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
        settings.save()
        
        return redirect('cai_dat')
    
    context = {
        'settings': settings,
    }
    return render(request, 'delivery/cai_dat.html', context)


@login_required
def xuat_excel(request):
    """Xuất danh sách đơn hàng ra file CSV"""
    
    loai = request.GET.get('loai', '')
    if loai == 'da_giao':
        orders = DonHang.objects.filter(trang_thai='DA_GIAO').order_by('-ngay_tao')
    else:
        orders = DonHang.objects.all().order_by('-ngay_tao')
    
    response = HttpResponse(content_type='text/csv')
    filename = f'don_hang_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    
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


@login_required
def lich_su_giao_hang(request):
    """Lịch sử các đơn hàng đã giao"""
    
    query = request.GET.get('q', '')
    tu_ngay = request.GET.get('tu_ngay', '')
    den_ngay = request.GET.get('den_ngay', '')
    
    orders = DonHang.objects.filter(trang_thai='DA_GIAO')
    
    if query:
        orders = orders.filter(
            Q(ma_don__icontains=query) | 
            Q(ten_khach__icontains=query) |
            Q(so_dien_thoai__icontains=query)
        )
    
    if tu_ngay:
        orders = orders.filter(ngay_tao__date__gte=tu_ngay)
    if den_ngay:
        orders = orders.filter(ngay_tao__date__lte=den_ngay)
    
    orders = orders.order_by('-ngay_tao')
    
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    context = {
        'orders': orders,
        'query': query,
        'tu_ngay': tu_ngay,
        'den_ngay': den_ngay,
        'thong_ke': {
            'tong_da_giao': DonHang.objects.filter(trang_thai='DA_GIAO').count(),
            'hom_nay': DonHang.objects.filter(
                trang_thai='DA_GIAO', 
                ngay_tao__date=today
            ).count(),
            '7_ngay_qua': DonHang.objects.filter(
                trang_thai='DA_GIAO', 
                ngay_tao__date__gte=week_ago
            ).count(),
            '30_ngay_qua': DonHang.objects.filter(
                trang_thai='DA_GIAO', 
                ngay_tao__date__gte=month_ago
            ).count(),
        }
    }
    return render(request, 'delivery/lich_su.html', context)


# ========== ĐĂNG KÝ / ĐĂNG NHẬP ==========
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
    return redirect('tao_don_moi')


def ban_do_giao_hang(request):
    return render(request, 'delivery/index.html')