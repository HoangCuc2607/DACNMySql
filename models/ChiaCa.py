from models.db import get_conn

class ChiaCa:
    def __init__(self, id=None, ngay="",
                 gio_bat_dau_ca_sang="", gio_ket_thuc_ca_sang="",
                 gio_bat_dau_ca_chieu="", gio_ket_thuc_ca_chieu="",
                 gio_bat_dau_ca_toi="", gio_ket_thuc_ca_toi=""):

        self.id = id
        self.ngay = ngay
        self.gio_bat_dau_ca_sang = gio_bat_dau_ca_sang
        self.gio_ket_thuc_ca_sang = gio_ket_thuc_ca_sang
        self.gio_bat_dau_ca_chieu = gio_bat_dau_ca_chieu
        self.gio_ket_thuc_ca_chieu = gio_ket_thuc_ca_chieu
        self.gio_bat_dau_ca_toi = gio_bat_dau_ca_toi
        self.gio_ket_thuc_ca_toi = gio_ket_thuc_ca_toi

    # ---------------------------
    # Thêm ca mới
    # ---------------------------
    def them_ca(self):
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO ChiaCa (
                ngay,
                gio_bat_dau_ca_sang, gio_ket_thuc_ca_sang,
                gio_bat_dau_ca_chieu, gio_ket_thuc_ca_chieu,
                gio_bat_dau_ca_toi, gio_ket_thuc_ca_toi
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            self.ngay,
            self.gio_bat_dau_ca_sang, self.gio_ket_thuc_ca_sang,
            self.gio_bat_dau_ca_chieu, self.gio_ket_thuc_ca_chieu,
            self.gio_bat_dau_ca_toi, self.gio_ket_thuc_ca_toi
        ))

        self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self.id

    # ---------------------------
    # Cập nhật ca dựa trên ngày
    # ---------------------------
    def cap_nhat_ca(self):
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE ChiaCa
            SET 
                gio_bat_dau_ca_sang=%s, gio_ket_thuc_ca_sang=%s,
                gio_bat_dau_ca_chieu=%s, gio_ket_thuc_ca_chieu=%s,
                gio_bat_dau_ca_toi=%s, gio_ket_thuc_ca_toi=%s
            WHERE ngay=%s
        """, (
            self.gio_bat_dau_ca_sang, self.gio_ket_thuc_ca_sang,
            self.gio_bat_dau_ca_chieu, self.gio_ket_thuc_ca_chieu,
            self.gio_bat_dau_ca_toi, self.gio_ket_thuc_ca_toi,
            self.ngay
        ))

        conn.commit()
        conn.close()

    # ---------------------------
    # Lấy ca theo ngày
    # ---------------------------
    @staticmethod
    def lay_ca_theo_ngay(ngay):
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                id, ngay,
                gio_bat_dau_ca_sang, gio_ket_thuc_ca_sang,
                gio_bat_dau_ca_chieu, gio_ket_thuc_ca_chieu,
                gio_bat_dau_ca_toi, gio_ket_thuc_ca_toi
            FROM ChiaCa
            WHERE ngay = %s
        """, (ngay,))

        record = cursor.fetchone()
        conn.close()

        if record:
            return ChiaCa(*record)
        return None

    # ---------------------------
    # Lấy ca theo ngày + số ca
    # ---------------------------
    @staticmethod
    def lay_ca_theo_ngay_va_so(ngay, so_ca):
        ca = ChiaCa.lay_ca_theo_ngay(ngay)

        if not ca:
            return None

        if so_ca == 1:
            return {"start": ca.gio_bat_dau_ca_sang, "end": ca.gio_ket_thuc_ca_sang}
        if so_ca == 2:
            return {"start": ca.gio_bat_dau_ca_chieu, "end": ca.gio_ket_thuc_ca_chieu}
        if so_ca == 3:
            return {"start": ca.gio_bat_dau_ca_toi, "end": ca.gio_ket_thuc_ca_toi}

        return None
    @staticmethod
    def GetAllChiaCa():
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            select * from ChiaCa
            """)
        records = cursor.fetchall()
        conn.close()
        return [ChiaCa(*r) for r in records]
    
    @staticmethod
    def GetChiaCaByThangAndNam(thang, nam):

        query = """
            SELECT *
            FROM ChiaCa
            WHERE MONTH(ngay) = %s AND YEAR(ngay) = %s
            ORDER BY ngay ASC
        """

        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute(query, (thang, nam))
        records = cursor.fetchall()

        conn.close()
        return [ChiaCa(*r) for r in records]


