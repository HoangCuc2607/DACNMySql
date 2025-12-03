import mysql.connector
import random
from datetime import datetime, timedelta

# -----------------------------
# 1. KẾT NỐI DATABASE
# -----------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="mydatabase"
)
cursor = db.cursor()

# -----------------------------
# 2. FAKE DANH SÁCH NHÂN VIÊN
# -----------------------------
nhanvien_list = [
    ("Nguyễn Văn A", "1995-03-12", "Nam", "Hà Nội", "0901111111", "nguyenvana@example.com"),
    ("Trần Thị B", "1998-07-21", "Nữ", "Đà Nẵng", "0902222222", "tranthib@example.com"),
    ("Lê Văn C", "1992-01-05", "Nam", "TP.HCM", "0903333333", "levanc@example.com"),
    ("Phạm Thị D", "2000-10-10", "Nữ", "Hải Phòng", "0904444444", "phamthid@example.com"),
    ("Đỗ Minh E", "1997-12-30", "Khác", "Cần Thơ", "0905555555", "dominhe@example.com")
]

# Insert nhân viên nếu bảng đang trống
cursor.execute("SELECT COUNT(*) FROM NhanVien")
if cursor.fetchone()[0] == 0:
    cursor.executemany("""
        INSERT INTO NhanVien (ho_ten, ngay_sinh, gioi_tinh, dia_chi, so_dien_thoai, email)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, nhanvien_list)
    db.commit()
    print("✔ Đã thêm 5 nhân viên")

# Lấy lại ID nhân viên
cursor.execute("SELECT ma_nhan_vien FROM NhanVien")
nhanvien_ids = [row[0] for row in cursor.fetchall()]

# -----------------------------
# 3. FAKE 5 NGÀY CHIA CA
# -----------------------------
start_date = datetime(2025, 11, 27)
days = 5

chia_ca_ids = []

for i in range(days):
    day = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
    cursor.execute("""
        INSERT INTO ChiaCa (
            ngay,
            gio_bat_dau_ca_sang, gio_ket_thuc_ca_sang,
            gio_bat_dau_ca_chieu, gio_ket_thuc_ca_chieu,
            gio_bat_dau_ca_toi, gio_ket_thuc_ca_toi
        )
        VALUES (%s, '07:00:00','11:00:00','13:00:00','17:00:00','18:00:00','22:00:00')
    """, (day,))
    db.commit()

    chia_ca_ids.append(cursor.lastrowid)

print("✔ Đã tạo 5 ngày ChiaCa")

# -----------------------------
# 4. FAKE PHÂN CA (ChiaCaNhanVien)
# -----------------------------
ca_values = ["Sáng", "Chiều", "Tối"]

for cc_id in chia_ca_ids:
    for nv in nhanvien_ids:
        ca = random.choice(ca_values)
        cursor.execute("""
            INSERT INTO ChiaCaNhanVien (chia_ca_id, nhanvien_id, ca)
            VALUES (%s, %s, %s)
        """, (cc_id, nv, ca))

db.commit()
print("✔ Đã phân ca cho nhân viên")

# -----------------------------
# 5. FAKE ĐIỂM DANH
# -----------------------------
diemdanh_status = ["Đã điểm danh", "Đến muộn", "Chưa điểm danh"]

for idx, cc_id in enumerate(chia_ca_ids):
    ngay = (start_date + timedelta(days=idx)).strftime("%Y-%m-%d")

    for nv in nhanvien_ids:
        # random điểm danh cho từng ca
        ca_sang = random.choice(diemdanh_status)
        ca_chieu = random.choice(diemdanh_status)
        ca_toi = random.choice(diemdanh_status)

        cursor.execute("""
            INSERT INTO DiemDanh (nhanvien_id, ngay_diem_danh, ca_sang, ca_chieu, ca_toi)
            VALUES (%s, %s, %s, %s, %s)
        """, (nv, ngay, ca_sang, ca_chieu, ca_toi))

db.commit()
print("✔ Đã thêm dữ liệu điểm danh")

# -----------------------------
# HOÀN THÀNH
# -----------------------------
print("\n🎉 Fake data thành công cho 5 ngày!")
