from models.db import get_conn
from models.ChiaCa import ChiaCa

class ChiaCaNhanVien:
    def __init__(self, id=None, chia_ca_id=None, nhanvien_id=None, ca=""):
        self.id = id
        self.chia_ca_id = chia_ca_id
        self.nhanvien_id = nhanvien_id
        self.ca = ca  # Sáng / Chiều / Tối

    # --------------------------------------------------------
    # Thêm 1 nhân viên vào ca
    # --------------------------------------------------------
    def AddNhanVienVaoCa(self):
        try:
            conn = get_conn()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO ChiaCaNhanVien (chia_ca_id, nhanvien_id, ca)
                VALUES (%s, %s, %s)
            """, (self.chia_ca_id, self.nhanvien_id, self.ca))

            conn.commit()
            self.id = cursor.lastrowid

            return self.id

        except Exception as e:
            print("Lỗi AddNhanVienVaoCa:", e)
            return None

        finally:
            conn.close()

    # --------------------------------------------------------
    # Cập nhật danh sách nhân viên của 1 ca (xóa hết -> thêm mới)
    # --------------------------------------------------------
    @staticmethod
    def UpdateNhanVienTrongCa(chia_ca_id, ca, danh_sach_nhan_vien_ids):
        try:
            # Xóa cũ
            ChiaCaNhanVien.DeleteNhanVienTheoCa(chia_ca_id, ca)

            # Thêm mới
            for nv_id in danh_sach_nhan_vien_ids:
                obj = ChiaCaNhanVien(chia_ca_id=chia_ca_id, nhanvien_id=nv_id, ca=ca)
                obj.AddNhanVienVaoCa()

            return True

        except Exception as e:
            print("Lỗi UpdateNhanVienTrongCa:", e)
            return False

    # --------------------------------------------------------
    # Lấy danh sách ID nhân viên theo ca
    # --------------------------------------------------------
    @staticmethod
    def GetNhanVienTheoCa(chia_ca_id, ca):
        try:
            conn = get_conn()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT nhanvien_id
                FROM ChiaCaNhanVien
                WHERE chia_ca_id = %s AND ca = %s
            """, (chia_ca_id, ca))

            rows = cursor.fetchall()
            return [r[0] for r in rows]

        except Exception as e:
            print("Lỗi GetNhanVienTheoCa:", e)
            return []

        finally:
            conn.close()

    # --------------------------------------------------------
    # Xóa tất cả nhân viên thuộc 1 ca
    # --------------------------------------------------------
    @staticmethod
    def DeleteNhanVienTheoCa(chia_ca_id, ca):
        try:
            conn = get_conn()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM ChiaCaNhanVien
                WHERE chia_ca_id = %s AND ca = %s
            """, (chia_ca_id, ca))

            conn.commit()
            return True

        except Exception as e:
            print("Lỗi DeleteNhanVienTheoCa:", e)
            return False

        finally:
            conn.close()

