from models.NhanVien import NhanVien

from flask import Blueprint, render_template, flash, request, jsonify

dang_ky_bp = Blueprint("dangky", __name__)

@dang_ky_bp.route("/dangky")
def form_dang_ky():
    return render_template("dangkynhanvien.html")

@dang_ky_bp.route("/dangkynhanvien", methods = ['POST'])
def dangkynhanvien():
    data = request.json
    print("du lieu nhan: ", data)
    nv = NhanVien(ho_ten = data['ho_ten'],
                so_dien_thoai = data['so_dien_thoai'],
                dia_chi = data['dia_chi'], 
                gioi_tinh = data['gioi_tinh'], 
                email = data['email'], 
                ngay_sinh = data['ngay_sinh'])

    #kiem tra nhan vien nay da dang ky chua
    dsnv = NhanVien.GetAllNhanVien()
    dsemail = [i.email for i in dsnv]
    if dsemail:
        if nv.email in dsemail:
            return jsonify({'error': 'Nhân viên đã tồn tại!'})
        else:
            #thêm mới nhân viên
            try:
                NhanVien.AddNhanVien(nv)
                return jsonify({'message':'Thêm nhân viên thành công!'})
            except Exception as e:
                return jsonify({'error': f'{e}, Thêm nhân viên không thành công!'})