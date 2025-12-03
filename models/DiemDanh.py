from models.db import get_conn
from datetime import date

class DiemDanh:
    def __init__(self, id=None, nhanvien_id=None, ngay_diem_danh=None,
                 ca_sang=None, ca_chieu=None, ca_toi=None):
        self.id = id
        self.nhanvien_id = nhanvien_id
        self.ngay_diem_danh = ngay_diem_danh or date.today()
        self.ca_sang = ca_sang
        self.ca_chieu = ca_chieu
        self.ca_toi = ca_toi

    # ---------------------------
    # Thêm mới điểm danh
    # ---------------------------
    def AddDiemDanh(self):
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO DiemDanh (nhanvien_id, ngay_diem_danh, ca_sang, ca_chieu, ca_toi)
            VALUES (%s, %s, %s, %s, %s)
        """, (self.nhanvien_id, self.ngay_diem_danh, self.ca_sang, self.ca_chieu, self.ca_toi))

        conn.commit()
        conn.close()

    # ---------------------------
    # Cập nhật trạng thái 1 ca
    # ---------------------------
    @staticmethod
    def UpdateDiemDanh(nhanvien_id, ngay_diem_danh, ca, trang_thai):
        col = f"ca_{ca.lower()}"  # ca_sang, ca_chieu, ca_toi
        print("ten ca: ", col)
        print("ngay diem danh: ", ngay_diem_danh)
        print("nhan vien id", nhanvien_id)
        print("trang thai: ", trang_thai)
        conn = get_conn()
        cursor = conn.cursor()
        try: 
            cursor.execute(f"""
                UPDATE DiemDanh
                SET {col} = %s
                WHERE nhanvien_id = %s AND ngay_diem_danh = %s
            """, (trang_thai, nhanvien_id, ngay_diem_danh))

            conn.commit()
        except Exception as e:
            print("loi la: ", e)
        conn.close()

    # ---------------------------
    # Lấy điểm danh theo ngày
    # ---------------------------
    @staticmethod
    def GetDiemDanhByDate(ngay_diem_danh):
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nhanvien_id, ngay_diem_danh, ca_sang, ca_chieu, ca_toi
            FROM DiemDanh
            WHERE ngay_diem_danh = %s
        """, (ngay_diem_danh,))

        records = cursor.fetchall()
        conn.close()

        return [DiemDanh(*r) for r in records]

    # ---------------------------
    # Lấy điểm danh theo nhân viên
    # ---------------------------
    @staticmethod
    def GetDiemDanhByNhanVienId(nhanvien_id):
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nhanvien_id, ngay_diem_danh, ca_sang, ca_chieu, ca_toi
            FROM DiemDanh
            WHERE nhanvien_id = %s
            ORDER BY ngay_diem_danh DESC
        """, (nhanvien_id,))

        records = cursor.fetchall()
        conn.close()

        return [DiemDanh(*r) for r in records]

    # ---------------------------
    # Lấy trạng thái 1 ca
    # ---------------------------
    @staticmethod
    def GetTrangThaiCa(nhanvien_id, ngay_diem_danh, ca):
        col = f"ca_{ca.lower()}"

        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT {col}
            FROM DiemDanh
            WHERE nhanvien_id = %s AND ngay_diem_danh = %s
        """, (nhanvien_id, ngay_diem_danh))

        result = cursor.fetchone()
        conn.close()

        return result[0] if result else None

    # ---------------------------
    # Xóa điểm danh
    # ---------------------------
    @staticmethod
    def DeleteDiemDanhById(id):
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM DiemDanh WHERE id = %s
        """, (id,))

        conn.commit()
        conn.close()

    @staticmethod
    def GetDiemDanhByDateAndId(nhanvien_id, ngay_diem_danh):
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
                        select * from DiemDanh
                       where ngay_diem_danh = %s and nhanvien_id = %s
        """, (ngay_diem_danh, nhanvien_id))

        records = cursor.fetchall()
        conn.commit()
        conn.close()

        return [DiemDanh(*r) for r in records]
