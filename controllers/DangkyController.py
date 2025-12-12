from models.NhanVien import NhanVien
import qrcode
from io import BytesIO
from flask import send_file, url_for
import uuid

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
                nv.ma_qr = tao_token()
                id_add = NhanVien.AddNhanVien(nv)
                qr_url = url_for("dangky.qr_image", id=id_add)

                return jsonify({
                            'message': 'Thêm nhân viên thành công!',
                            'qr_url': qr_url
                                })

            except Exception as e:
                return jsonify({'error': f'{e}, Thêm nhân viên không thành công!'})

@dang_ky_bp.route('/nhanvien/<id>/qr')
def qr_image(id):
    try:
        nv = NhanVien.GetNhanVienById(id)
        if nv is None:
            return jsonify({'error': 'Khong tim duoc nhan vien!'})
        img = tao_qr(nv.ma_qr)
        print("dangky: ",img)
        return send_file(img, mimetype='image/png')
    except:
        return jsonify({'error': 'Loi khong lay duoc ma QR!',
                        })
    
def tao_qr(token):
    img = qrcode.make(token)
    buf = BytesIO() 
    img.save(buf, format='png')
    buf.seek(0)
    return buf

def tao_token():
    token = str(uuid.uuid4())
    return token

