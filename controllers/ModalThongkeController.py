from flask import Blueprint, render_template, flash, request, jsonify ,url_for, session, redirect, send_file
from models.NhanVien import NhanVien
from models.DiemDanh import DiemDanh
from models.ChiaCa import ChiaCa
from models.ChiaCaNhanVien import ChiaCaNhanVien
from datetime import date
from datetime import datetime, date
from datetime import time, timedelta, datetime, date
import openpyxl
from io import BytesIO

def to_time(value):
    if isinstance(value, time):
        return value
    if isinstance(value, timedelta):
        # Convert timedelta → time (MySQL TIME trả timedelta)
        total_seconds = int(value.total_seconds())
        hour = total_seconds // 3600
        minute = (total_seconds % 3600) // 60
        second = total_seconds % 60
        return time(hour, minute, second)
    if isinstance(value, str):
        # Nếu chuỗi HH:MM:SS
        return datetime.strptime(value, "%H:%M:%S").time()
    return None

def tinh_gio_ca(bat_dau, ket_thuc):
    bat_dau = to_time(bat_dau)
    ket_thuc = to_time(ket_thuc)

    if not bat_dau or not ket_thuc:
        return timedelta()

    bd = datetime.combine(date.today(), bat_dau)
    kt = datetime.combine(date.today(), ket_thuc)

    # Ca qua ngày (vd 22:00 → 06:00)
    if kt < bd:
        kt += timedelta(days=1)
    td = kt-bd
    return int(td.total_seconds() // 3600)  # giờ dạng số nguyên



thong_ke_bp = Blueprint("thongke", __name__)

@thong_ke_bp.route("/loc_thong_ke_ca", methods = ['POST'])
def laythongkeca():
    data = request.json
    thang = data.get('thang')
    nam = data.get('nam')
    try: 
        ds_ca = ChiaCa.GetChiaCaByThangAndNam(thang, nam)
        data = []
        for ca in ds_ca:
            ca.thoi_gian_ca_sang = tinh_gio_ca(ca.gio_bat_dau_ca_sang, ca.gio_ket_thuc_ca_sang)
            ca.thoi_gian_ca_chieu = tinh_gio_ca(ca.gio_bat_dau_ca_chieu, ca.gio_ket_thuc_ca_chieu)
            ca.thoi_gian_ca_toi = tinh_gio_ca(ca.gio_bat_dau_ca_toi, ca.gio_ket_thuc_ca_toi)
            print(ca.gio_ket_thuc_ca_toi, ca.thoi_gian_ca_sang, "aaaa")
            
            data.append({
                "ngay": ca.ngay.strftime("%Y-%m-%d"),

                "thoi_gian_bat_dau_ca_sang": str(ca.gio_bat_dau_ca_sang),
                "thoi_gian_ket_thuc_ca_sang": str(ca.gio_ket_thuc_ca_sang),
                "thoi_gian_ca_sang": ca.thoi_gian_ca_sang,

                "thoi_gian_bat_dau_ca_chieu": str(ca.gio_bat_dau_ca_chieu),
                "thoi_gian_ket_thuc_ca_chieu": str(ca.gio_ket_thuc_ca_chieu),
                "thoi_gian_ca_chieu": ca.thoi_gian_ca_chieu,

                "thoi_gian_bat_dau_ca_toi": str(ca.gio_bat_dau_ca_toi),
                "thoi_gian_ket_thuc_ca_toi": str(ca.gio_ket_thuc_ca_toi),
                "thoi_gian_ca_toi": ca.thoi_gian_ca_toi,
            })

        return jsonify({"data": data})
    except Exception as e:
        print(e)
        return jsonify({'error': 'Không có dữ liệu trùng với lựa chọn!'})

@thong_ke_bp.route("/loc_thong_ke_diem_danh", methods = ['POST'])
def thongkediemdanh():
    data = request.json
    thang = data.get('thang')
    nam = data.get('nam')
    try:
        ds_tk = DiemDanh.GetDiemDanhByThangAndNam(thang, nam)
        ds = {}
        for dd in ds_tk:
            
            if dd[1] not in ds:
                nv = NhanVien.GetNhanVienById(dd[1])
                ds[dd[1]] = {
                    'records' : [],
                    'ho_ten': nv.ho_ten,
                    'tong_da_diem_danh': 0,
                    'tong_den_muon': 0
                }
            
            #them từng ngày vào records
            ds[dd[1]]['records'].append(
                {
                    'ngay': dd[2].strftime("%Y-%m-%d"),
                    'ca_sang': dd[3],
                    'ca_chieu': dd[4],
                    'ca_toi':dd[5],
                    'da_diem_danh':dd[6],
                    'den_muon':dd[7]
                }
            )
            #cộng dồn thống kê:
            ds[dd[1]]['tong_da_diem_danh'] += dd[6]
            ds[dd[1]]['tong_den_muon'] += dd[7]
        return jsonify({'data':ds})
    except Exception as e:
        print(e)
        return jsonify({'error': 'Không có dữ liệu trùng với lựa chọn!'})
    

@thong_ke_bp.route("/export_thong_ke_ca")   
def export_thong_ke_ca():
    thang = request.args.get("thang")
    nam = request.args.get("nam")

    try: 
        ds_ca = ChiaCa.GetChiaCaByThangAndNam(thang, nam)
        data = []
        for ca in ds_ca:
            ca.thoi_gian_ca_sang = tinh_gio_ca(ca.gio_bat_dau_ca_sang, ca.gio_ket_thuc_ca_sang)
            ca.thoi_gian_ca_chieu = tinh_gio_ca(ca.gio_bat_dau_ca_chieu, ca.gio_ket_thuc_ca_chieu)
            ca.thoi_gian_ca_toi = tinh_gio_ca(ca.gio_bat_dau_ca_toi, ca.gio_ket_thuc_ca_toi)
            print(ca.gio_ket_thuc_ca_toi, ca.thoi_gian_ca_sang, "aaaa")
            
            data.append({
                "ngay": ca.ngay.strftime("%Y-%m-%d"),

                "thoi_gian_bat_dau_ca_sang": str(ca.gio_bat_dau_ca_sang),
                "thoi_gian_ket_thuc_ca_sang": str(ca.gio_ket_thuc_ca_sang),
                "thoi_gian_ca_sang": ca.thoi_gian_ca_sang,

                "thoi_gian_bat_dau_ca_chieu": str(ca.gio_bat_dau_ca_chieu),
                "thoi_gian_ket_thuc_ca_chieu": str(ca.gio_ket_thuc_ca_chieu),
                "thoi_gian_ca_chieu": ca.thoi_gian_ca_chieu,

                "thoi_gian_bat_dau_ca_toi": str(ca.gio_bat_dau_ca_toi),
                "thoi_gian_ket_thuc_ca_toi": str(ca.gio_ket_thuc_ca_toi),
                "thoi_gian_ca_toi": ca.thoi_gian_ca_toi,
            })
 
            # Tạo file Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Thống kê ca"

            # Header
        ws.append([
            "Ngày", "BĐ Ca sáng", "KT Ca sáng", "TG ca sáng",
            "BĐ Ca chiều", "KT Ca chiều", "TG ca chiều",
            "BĐ Ca tối", "KT Ca tối", "TG ca tối"
            ])
        if data:
            for row in data:
                    ws.append([
                        row["ngay"],
                        row["thoi_gian_bat_dau_ca_sang"],
                        row["thoi_gian_ket_thuc_ca_sang"],
                        row["thoi_gian_ca_sang"],

                        row["thoi_gian_bat_dau_ca_chieu"],
                        row["thoi_gian_ket_thuc_ca_chieu"],
                        row["thoi_gian_ca_chieu"],

                        row["thoi_gian_bat_dau_ca_toi"],
                        row["thoi_gian_ket_thuc_ca_toi"],
                        row["thoi_gian_ca_toi"],
                    ])

                # Lưu vào bộ nhớ (RAM)
        file_stream = BytesIO()
        wb.save(file_stream)
        file_stream.seek(0)

        filename = f"ThongKeCa_{thang}_{nam}.xlsx"

        return send_file(
                    file_stream,
                    download_name=filename,
                    as_attachment=True,
                    mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:
        print(e)
        

@thong_ke_bp.route("/export_thong_ke_diem_danh")
def export_thong_ke_diem_danh():
    thang = request.args.get("thang")
    nam = request.args.get("nam")

    try:
        ds_tk = DiemDanh.GetDiemDanhByThangAndNam(thang, nam)

        # Gom dữ liệu giống route lọc
        ds = {}
        for dd in ds_tk:
            if dd[1] not in ds:
                nv = NhanVien.GetNhanVienById(dd[1])
                ds[dd[1]] = {
                    'records': [],
                    'ho_ten': nv.ho_ten,
                    'tong_da_diem_danh': 0,
                    'tong_den_muon': 0
                }

            ds[dd[1]]['records'].append({
                'ngay': dd[2],
                'ca_sang': dd[3],
                'ca_chieu': dd[4],
                'ca_toi': dd[5],
                'da_diem_danh': dd[6],
                'den_muon': dd[7]
            })

            ds[dd[1]]['tong_da_diem_danh'] += dd[6]
            ds[dd[1]]['tong_den_muon'] += dd[7]

            # Tạo workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Thống kê điểm danh"

            # Header
        ws.append([
                "ID NV", "Họ tên", "Ngày",
                "Ca sáng", "Ca chiều", "Ca tối",
                "Đã điểm danh", "Đến muộn"
            ])

            # Đổ dữ liệu
        for id_nv, nv in ds.items():
            for r in nv['records']:
                ws.append([
                        id_nv,
                        nv['ho_ten'],
                        r['ngay'],
                        r['ca_sang'],
                        r['ca_chieu'],
                        r['ca_toi'],
                        r['da_diem_danh'],
                        r['den_muon']
                    ])

            # Xuống dòng thêm tổng
        ws.append([])
        ws.append(["TỔNG HỢP"])

        ws.append(["ID NV", "Họ tên", "Tổng đã điểm danh", "Tổng đến muộn"])
        if ds_tk:
            for id_nv, nv in ds.items():
                    ws.append([
                        id_nv,
                        nv['ho_ten'],
                        nv['tong_da_diem_danh'],
                        nv['tong_den_muon']
                    ])

            # Xuất file
        file_stream = BytesIO()
        wb.save(file_stream)
        file_stream.seek(0)

        filename = f"ThongKeDiemDanh_{thang}_{nam}.xlsx"

        return send_file(
                file_stream,
                download_name=filename,
                as_attachment=True,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        print(e)
        return jsonify({"error": "Không thể xuất file!"})
