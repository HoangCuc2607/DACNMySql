from models.DiemDanh import DiemDanh
from models.ChiaCa import ChiaCa
from models.ChiaCaNhanVien import ChiaCaNhanVien
from models.NhanVien import NhanVien
from flask import Blueprint, render_template, flash, request, jsonify
from datetime import datetime

diem_danh_bp = Blueprint("diemdanh", __name__)

@diem_danh_bp.route("/diemdanh", methods = ['POST'])
def diemdanh():
    data = request.json
    email = data['email']
    ca = data.get('ca') #1 sang, 2 chieu, 3 toi
    print("ca", ca)
    ngay = data['ngay']

    nv = NhanVien.GetNhanVienByEmail(email)
    return checkdiemdanh(nv, ca, ngay)

@diem_danh_bp.route("/diemdanhbangqr", methods = ['POST'])
def diemdanhbangqr():
    data = request.json
    ma_qr = data['tokenqr']
    ca = data.get('ca')
    ngay = data['ngay']

    nv = NhanVien.GetNhanVienByQR(ma_qr)
    return checkdiemdanh(nv, ca, ngay)


def checkdiemdanh(nv, ca, ngay):
    #truyen vao nv 
    if not nv:
        return jsonify({'error': 'Loi khong tim duoc nhan vien'})
    else:
        #lay thong tin cua ca theo ngay va so ca de so sanh gio vao lam
        ca_infor = ChiaCa.lay_ca_theo_ngay_va_so(ngay, ca)
        obj_ca = ChiaCa.lay_ca_theo_ngay(ngay)
        ca_to_text = {1:"Sáng", 2: "Chiều", 3: "Tối"}

        if not ca_infor:
            return jsonify({'error': 'Chua co ca cho ngay nay'})
        #kiem tra nhan vien có o trong ca khong
        nv_in_ca = ChiaCaNhanVien.GetNhanVienTheoCa(obj_ca.id, ca_to_text[ca])
        if nv.ma_nhan_vien not in nv_in_ca:
            return jsonify({'error': 'Nhân viên không có trong ca!'})

        # Chuyển giờ sang datetime.time
        start_td = ca_infor['start']
        print("start_td", start_td)
        end_td = ca_infor['end']

        start_time = (datetime.min + start_td).time()
        print("start time: ", start_time)
        end_time = (datetime.min + end_td).time()
        now_time = datetime.now().time()
        print("now" , now_time)

        # Xác định trạng thái điểm danh
        if now_time <= start_time:
            trang_thai = "Đã điểm danh"
        elif start_time < now_time <= end_time:
            trang_thai = "Đến muộn"
        else:
            trang_thai = "Chưa điểm danh"

            # Kiểm tra xem đã có bản ghi điểm danh cho ngày này chưa
        dd = DiemDanh.GetDiemDanhByDateAndId(nv.ma_nhan_vien, ngay)
        print("dd: ", dd)
        if not dd:
            # Nếu chưa có, tạo mới
            new_dd = DiemDanh(nhanvien_id=nv.ma_nhan_vien, ngay_diem_danh=ngay)
            new_dd.AddDiemDanh()
            print("newdd: ", new_dd)

        # Cập nhật trạng thái ca
        ca_dict = {1: 'sang', 2: 'chieu', 3: 'toi'}
        try:
            DiemDanh.UpdateDiemDanh(nv.ma_nhan_vien, ngay, ca_dict[ca], trang_thai)
            return jsonify({'message': 'Điểm danh thành công', 'trang_thai': trang_thai})
        except Exception as e:
            return jsonify({'error': f'{e}'})

    

    
