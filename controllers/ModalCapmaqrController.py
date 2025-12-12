from models.DiemDanh import DiemDanh
from models.ChiaCa import ChiaCa
from models.ChiaCaNhanVien import ChiaCaNhanVien
from models.NhanVien import NhanVien
from flask import Blueprint, render_template, flash, request, jsonify, send_file, url_for
from datetime import datetime
from .DangkyController import tao_qr, tao_token


cap_lai_qr_bp = Blueprint("caplaiqr", __name__)
@cap_lai_qr_bp.route("/cap_lai_qr", methods = ['POST'])
def caplaiqr():
    data = request.json
    email = data['email']

    nv = NhanVien.GetNhanVienByEmail(email)
    if not nv:
        return jsonify({'error':'Loi khong tim duoc nhan vien!'})
        
    tokenqr = tao_token()
    nv.ma_qr = tokenqr
    print("ma qr", nv.ma_qr)
    img_qr = tao_qr(tokenqr)

    #cap nhat lai khi tao xong
    try:
        if NhanVien.UpdateMaQRById(nv.ma_qr, nv.ma_nhan_vien):
            qr_url =  url_for("dangky.qr_image", id = nv.ma_nhan_vien)

            return jsonify({'message': 'Cap nhat ma QR thanh cong!!', 'qr_url': qr_url })
        else: return jsonify({'error': 'Cap nhat ktc'})
    except Exception as e:
        return jsonify({'error': str(e)})
