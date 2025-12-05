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
# 2. THÊM NHÂN VIÊN (nếu chưa có)
# -----------------------------
nhanvien_list = [
    ("Nguyễn Văn A", "1995-03-12", "Nam", "Hà Nội", "0901111111", "nguyenvana@example.com"),
    ("Trần Thị B", "1998-07-21", "Nữ", "Đà Nẵng", "0902222222", "tranthib@example.com"),
    ("Lê Văn C", "1992-01-05", "Nam", "TP.HCM", "0903333333", "levanc@example.com"),
    ("Phạm Thị D", "2000-10-10", "Nữ", "Hải Phòng", "0904444444", "phamthid@example.com"),
    ("Đỗ Minh E", "1997-12-30", "Khác", "Cần Thơ", "0905555555", "dominhe@example.com"),
]

cursor.execute("SELECT COUNT(*) FROM NhanVien")
if cursor.fetchone()[0] == 0:
    cursor.executemany("""
        INSERT INTO NhanVien (ho_ten, ngay_sinh, gioi_tinh, dia_chi, so_dien_thoai, email)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, nhanvien_list)
    db.commit()
    print("✔ Đã thêm 5 nhân viên")

cursor.execute("SELECT ma_nhan_vien FROM NhanVien")
nhanvien_ids = [row[0] for row in cursor.fetchall()]

# -----------------------------
# 3. TẠO DANH SÁCH NGÀY CẦN FAKE
# -----------------------------
def date_range(start, end):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)

ngay_fake = []

# Tháng 10
ngay_fake += list(date_range(datetime(2025, 10, 1), datetime(2025, 10, 31)))

# Tháng 11
ngay_fake += list(date_range(datetime(2025, 11, 1), datetime(2025, 11, 30)))

# Tháng 12 đến ngày 3
ngay_fake += list(date_range(datetime(2025, 12, 1), datetime(2025, 12, 3)))

print(f"✔ Tổng số ngày fake: {len(ngay_fake)}")

chia_ca_ids = []

# -----------------------------
# 4. FAKE CHIA CA (giờ random)
# -----------------------------
def random_time(start_hour, end_hour):
    h = random.randint(start_hour, end_hour - 1)
    m = random.choice([0, 15, 30, 45])
    return f"{h:02d}:{m:02d}:00"

for day in ngay_fake:
    ngay_str = day.strftime("%Y-%m-%d")

    # Ca sáng: 6–9h → 10–12h
    start_sang = random_time(6, 9)
    end_sang = random_time(10, 12)

    # Ca chiều: 12–14h → 16–18h
    start_chieu = random_time(12, 14)
    end_chieu = random_time(16, 18)

    # Ca tối: 17–19h → 21–23h
    start_toi = random_time(17, 19)
    end_toi = random_time(21, 23)

    cursor.execute("""
        INSERT INTO ChiaCa (
            ngay,
            gio_bat_dau_ca_sang, gio_ket_thuc_ca_sang,
            gio_bat_dau_ca_chieu, gio_ket_thuc_ca_chieu,
            gio_bat_dau_ca_toi, gio_ket_thuc_ca_toi
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (ngay_str, start_sang, end_sang, start_chieu, end_chieu, start_toi, end_toi))

    db.commit()
    chia_ca_ids.append(cursor.lastrowid)

print("✔ Đã tạo bảng ChiaCa cho tất cả các ngày")

# -----------------------------
# 5. FAKE PHÂN CA NHÂN VIÊN
# -----------------------------
ca_list = ["Sáng", "Chiều", "Tối"]

for cc_id in chia_ca_ids:
    for nv in nhanvien_ids:
        cursor.execute("""
            INSERT INTO ChiaCaNhanVien (chia_ca_id, nhanvien_id, ca)
            VALUES (%s, %s, %s)
        """, (cc_id, nv, random.choice(ca_list)))

db.commit()
print("✔ Đã phân ca nhân viên")

# -----------------------------
# 6. FAKE ĐIỂM DANH
# -----------------------------
diemdanh_status = ["Đã điểm danh", "Đến muộn", "Chưa điểm danh"]

for i, cc_id in enumerate(chia_ca_ids):
    ngay = ngay_fake[i].strftime("%Y-%m-%d")

    for nv in nhanvien_ids:
        cursor.execute("""
            INSERT INTO DiemDanh (nhanvien_id, ngay_diem_danh, ca_sang, ca_chieu, ca_toi)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            nv,
            ngay,
            random.choice(diemdanh_status),
            random.choice(diemdanh_status),
            random.choice(diemdanh_status)
        ))

db.commit()
print("✔ Đã fake bảng ĐiểmDanh")

print("\n🎉 **HOÀN THÀNH FAKE DATA 3 THÁNG!**")
