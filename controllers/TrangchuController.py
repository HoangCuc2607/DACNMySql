from flask import Blueprint, render_template, flash, request, jsonify ,url_for, session, redirect
from models.NhanVien import NhanVien
from models.DiemDanh import DiemDanh
from datetime import date

trang_chu_bp = Blueprint("trangchu", __name__)

@trang_chu_bp.route("/")
def GetNhanVienDiemDanh():
    if 'login' not in session:
        return redirect(url_for('dangnhap.dangnhap'))

    ngay_hien_tai = date.today().strftime('%Y-%m-%d')
    try:
        danh_sach_nv = NhanVien.GetAllNhanVien()
    except Exception as e:
        print("Lỗi lấy danh sách nhân viên:", e)
        flash("Không thể tải danh sách nhân viên!", "danger")
        danh_sach_nv = []
    
    #lay trang thai diem danh theo ngay
    danh_sach_diemdanh = DiemDanh.GetDiemDanhByDate(ngay_hien_tai)
    #ghep nhan vien voi bang diem danh
    diem_danh_dict = {dd.nhanvien_id : dd for dd in danh_sach_diemdanh}
    for nv in danh_sach_nv:
        dd = diem_danh_dict.get(nv.ma_nhan_vien)
        if dd:
            nv.ca_sang = dd.ca_sang or "Chưa điểm danh"
            nv.ca_chieu = dd.ca_chieu or "Chưa điểm danh"
            nv.ca_toi= dd.ca_toi or "Chưa điểm danh"
        
        else:
            nv.ca_sang =  nv.ca_chieu = nv.ca_toi = "Chưa điểm danh"
    return render_template("trangchu.html", danh_sach = danh_sach_nv)

@trang_chu_bp.route("/sua_nhan_vien", methods = ['GET', 'POST'])
def UpdateNhanVien():
    #lay thong tin tra len modal
    if request.method == 'GET':
        ma_nv = request.args.get('id')
        if not ma_nv:
            return jsonify({'error': 'Không có id nhân viên'}), 400
        
        nv = NhanVien.GetNhanVienById(ma_nv)
        if nv:
            return jsonify({
                'ma_nhan_vien': nv.ma_nhan_vien,
                'ho_ten': nv.ho_ten,
                'so_dien_thoai': nv.so_dien_thoai,
                'dia_chi': nv.dia_chi,
                'gioi_tinh': nv.gioi_tinh,
                'email': nv.email,
                'ngay_sinh': nv.ngay_sinh.strftime("%Y-%m-%d") if nv.ngay_sinh else ""
                })
        else:
            return jsonify({'error': 'Khong co du lieu nhan vien'}), 404
        
    #nhan thong tin tu modal, lay thong tin tu json
    elif request.method == 'POST':
        data = request.json
        ma_nhan_vien = data.get('ma_nhan_vien')
        ho_ten = data.get('ho_ten')
        so_dien_thoai = data.get('so_dien_thoai')
        dia_chi = data.get('dia_chi')
        gioi_tinh = data.get('gioi_tinh')
        email = data.get('email')
        ngay_sinh = data.get('ngay_sinh')

        nv = NhanVien(ma_nhan_vien, ho_ten, so_dien_thoai, dia_chi, gioi_tinh, email, ngay_sinh)
        result = NhanVien.UpdateNhanVien(nv)
        if result:
            return jsonify({'message': 'Cap nhat nhan vien thanh cong'})
        else:
            return jsonify({'error': 'Cap nhat nhan vien that bai'}), 400

@trang_chu_bp.route("/xoa_nhan_vien", methods = ['POST'])
def DeleteNhanVien():
    data = request.json
    ma_nv = data['ma_nhan_vien']
    if not ma_nv:
        return jsonify({'Error': 'Thieu ma nhan vien'})
    else:
        try:
            NhanVien.DeleteNhanVien(ma_nv)
            return jsonify({'message': 'Xoa nhan vien thanh cong'})
        except Exception as e:
            return jsonify({'error': f'Xoa nhan vien khong thanh cong {e}!'}), 500
        
@trang_chu_bp.route("/dangxuat")
def dangxuat():
    session.clear()
    return redirect(url_for("dangnhap.dangnhap"))






        

        
