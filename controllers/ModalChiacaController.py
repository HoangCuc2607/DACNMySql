from models.ChiaCa import ChiaCa
from models.ChiaCaNhanVien import ChiaCaNhanVien
from flask import Blueprint, render_template, flash, request, jsonify

chia_ca_bp = Blueprint("chiaca", __name__)

def format_time(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}"

@chia_ca_bp.route("/lay_chia_ca/<ngay>", methods = ['GET'])
def lay_danh_sach_chia_ca(ngay):
    #lay thoi gian tung ca va lay ten nhan vien
    chiaca = ChiaCa.lay_ca_theo_ngay(ngay)
    print(type(chiaca.gio_bat_dau_ca_sang))

    if not chiaca:
        return jsonify({'error': 'Chưa có ca cho ngày này!'})
    else:
        data = {
            'ca_sang':
            {
                'bat_dau': format_time(chiaca.gio_bat_dau_ca_sang),
                'ket_thuc': format_time(chiaca.gio_ket_thuc_ca_sang),
                'nhanvien_ids': ChiaCaNhanVien.GetNhanVienTheoCa(chiaca.id, 'Sáng')
            },
            'ca_chieu':
            {
                'bat_dau': format_time(chiaca.gio_bat_dau_ca_chieu),
                'ket_thuc': format_time(chiaca.gio_ket_thuc_ca_chieu),
                'nhanvien_ids': ChiaCaNhanVien.GetNhanVienTheoCa(chiaca.id, 'Chiều')
            },  
            'ca_toi':
            {
                'bat_dau': format_time(chiaca.gio_bat_dau_ca_toi),
                'ket_thuc': format_time(chiaca.gio_ket_thuc_ca_toi),
                'nhanvien_ids': ChiaCaNhanVien.GetNhanVienTheoCa(chiaca.id, 'Tối')
            }

              }
        return jsonify(data)

@chia_ca_bp.route("/luu_chia_ca", methods = ['POST'])
def luu_chia_ca():
    #lay thong tin tu form
    data = request.json
    ngay = data.get('ngay')
    ca_sang = data.get('ca_sang') #{'bat_dau': , 'ket_thuc': , 'nhan_vien_ids': }
    ca_chieu = data.get('ca_chieu')
    ca_toi = data.get('ca_toi')

    #cap nhat ca hoac them moi neu chua tao ca
    ca_hien_tai = ChiaCa.lay_ca_theo_ngay(ngay)
    #neu da co thi cap nhat
    if ca_hien_tai:
        ca_hien_tai.gio_bat_dau_ca_sang = ca_sang['bat_dau']
        ca_hien_tai.gio_ket_thuc_ca_sang = ca_sang['ket_thuc']

        ca_hien_tai.gio_bat_dau_ca_chieu = ca_chieu['bat_dau']
        ca_hien_tai.gio_ket_thuc_ca_chieu = ca_chieu['ket_thuc']

        ca_hien_tai.gio_bat_dau_ca_toi = ca_toi['bat_dau']
        ca_hien_tai.gio_ket_thuc_ca_toi = ca_toi['ket_thuc']

        ChiaCa.cap_nhat_ca(ca_hien_tai)
        chia_ca_id = ca_hien_tai.id

    else:
    #chua co thi them moi
        ca_moi = ChiaCa(
        ngay=ngay,
        gio_bat_dau_ca_sang=ca_sang['bat_dau'],
        gio_ket_thuc_ca_sang=ca_sang['ket_thuc'],
        gio_bat_dau_ca_chieu=ca_chieu['bat_dau'],
        gio_ket_thuc_ca_chieu=ca_chieu['ket_thuc'],
        gio_bat_dau_ca_toi=ca_toi['bat_dau'],
        gio_ket_thuc_ca_toi=ca_toi['ket_thuc']
        )

        ca_moi.them_ca()
        chia_ca_id = ca_moi.id 

        # 2. Lưu nhân viên cho từng ca
    if chia_ca_id: 
        try:
            ChiaCaNhanVien.UpdateNhanVienTrongCa(chia_ca_id, 'Sáng', ca_sang['nhanvien_ids'])
            ChiaCaNhanVien.UpdateNhanVienTrongCa(chia_ca_id, 'Chiều', ca_chieu['nhanvien_ids'])
            ChiaCaNhanVien.UpdateNhanVienTrongCa(chia_ca_id, 'Tối', ca_toi['nhanvien_ids'])
            return jsonify({'message': 'Lưu ca thành công!'})
        except:
            return jsonify({'error': 'Lưu ca không thành công!'})
    else:
        return jsonify({'error': 'Lưu ca không thành công!'})
