from models.db import get_conn

class NhanVien:
    def __init__(self, ma_nhan_vien=None, ho_ten="", so_dien_thoai="", dia_chi="", gioi_tinh="", email="", ngay_sinh="", ma_qr = None):
        self.ma_nhan_vien = ma_nhan_vien
        self.ho_ten = ho_ten
        self.so_dien_thoai = so_dien_thoai
        self.dia_chi = dia_chi
        self.gioi_tinh = gioi_tinh
        self.email = email
        self.ngay_sinh = ngay_sinh
        self.ma_qr = ma_qr



    def AddNhanVien(self):
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO NhanVien (ho_ten, so_dien_thoai, dia_chi, gioi_tinh, email, ngay_sinh, ma_qr)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (self.ho_ten, self.so_dien_thoai, self.dia_chi, self.gioi_tinh, self.email, self.ngay_sinh, self.ma_qr))

        conn.commit()
        self.ma_nhan_vien = cur.lastrowid
        conn.close()
        return self.ma_nhan_vien

    @staticmethod
    def GetAllNhanVien():
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT ma_nhan_vien, ho_ten, so_dien_thoai, dia_chi, gioi_tinh, email, ngay_sinh
            FROM NhanVien
        """)

        records = cursor.fetchall()
        conn.close()

        return [NhanVien(*r) for r in records]
    
    @staticmethod    
    def GetNhanVienById(ma_nhan_vien):
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT ma_nhan_vien, ho_ten, so_dien_thoai, dia_chi, gioi_tinh, email, ngay_sinh, ma_qr
            FROM NhanVien
            WHERE ma_nhan_vien = %s
        """, (ma_nhan_vien,))

        record = cursor.fetchone()
        conn.close()

        if record:
            return NhanVien(*record)
        return None
        
    @staticmethod
    def GetNhanVienByQR(ma_qr):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("select * from NhanVien where ma_qr = %s", (ma_qr, ))
        record = cur.fetchone()
        conn.close()
        if record:
            return NhanVien(*record)
        return None
    
    @staticmethod
    def UpdateNhanVien(nv):
        try:
            conn = get_conn()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE NhanVien
                SET ho_ten=%s, so_dien_thoai=%s, dia_chi=%s, gioi_tinh=%s, email=%s, ngay_sinh=%s
                WHERE ma_nhan_vien=%s
            """, (nv.ho_ten, nv.so_dien_thoai, nv.dia_chi, nv.gioi_tinh, nv.email, nv.ngay_sinh, nv.ma_nhan_vien))

            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    @staticmethod
    def DeleteNhanVien(ma_nhan_vien):
        try: 
            conn = get_conn()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM NhanVien WHERE ma_nhan_vien = %s", (ma_nhan_vien,))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    @staticmethod
    def GetNhanVienByEmail(email):
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT ma_nhan_vien, ho_ten, so_dien_thoai, dia_chi, gioi_tinh, email, ngay_sinh
            FROM NhanVien
            WHERE email = %s
        """, (email,))

        record = cursor.fetchone()
        conn.close()

        if record:
            return NhanVien(*record)
        return None

    def UpdateMaQRById(ma_qr, id):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("""update NhanVien
                            set ma_qr = %s
                            where ma_nhan_vien = %s""", (ma_qr, id))
            conn.commit()
            conn.close()
            return True
        except:
            return False
        
    
