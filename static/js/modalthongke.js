// ===============================
// 1. EVENT LISTENERS
// ===============================

// Mở modal thống kê ca
document.getElementById("ThongkeCa").addEventListener("click", () => {
    openModal("thongKeCaModal");
});

// Mở modal thống kê điểm danh
document.getElementById("ThongkeDiemDanh").addEventListener("click", () => {
    openModal("thongKeDiemDanhModal");
});


// ===============================
// 2. HÀM MỞ MODAL
// ===============================
function openModal(modalId) {
    const modal = new bootstrap.Modal(document.getElementById(modalId));
    
    modal.show();
}


// ===============================
// 7. LỌC THỐNG KÊ CA
// ===============================

document.getElementById("btnLocThongKeCa").addEventListener("click", () => {
    const thang = document.getElementById("tkThang").value;
    const nam = document.getElementById("tkNam").value;

    if (!thang || !nam) {
        alert("Vui lòng chọn tháng và năm");
        return;
    }
    fetch("/trangchu/loc_thong_ke_ca", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ thang, nam })
    })
    .then(res => res.json())
    .then(res => {
        if (res.error) {
            alert(res.error);
            return;
        }
        alert("Thành công lấy dữ liệu")
        const tbody = document.querySelector("#thongKeCaModal tbody");
        tbody.innerHTML = ""; 

        res.data.forEach(row => {
            tbody.innerHTML += `
                <tr>
                    <td>${row.ngay}</td>
                    <td>${row.thoi_gian_bat_dau_ca_sang}</td>
                    <td>${row.thoi_gian_ket_thuc_ca_sang}</td>
                    <td>${row.thoi_gian_ca_sang}</td>

                    <td>${row.thoi_gian_bat_dau_ca_chieu}</td>
                    <td>${row.thoi_gian_ket_thuc_ca_chieu}</td>
                    <td>${row.thoi_gian_ca_chieu}</td>

                    <td>${row.thoi_gian_bat_dau_ca_toi}</td>
                    <td>${row.thoi_gian_ket_thuc_ca_toi}</td>
                    <td>${row.thoi_gian_ca_toi}</td>
                </tr>
            `;
        });

    });
});

// ===============================
// LỌC THỐNG KÊ ĐIỂM DANH
// ===============================

document.getElementById("btnLocThongKeDiemdanh").addEventListener("click", () => {
    const thang = document.getElementById("ddThang").value;
    const nam = document.getElementById("ddNam").value;

    if (!thang || !nam) {
        alert("Vui lòng chọn tháng và năm");
        return;
    }

    fetch("/trangchu/loc_thong_ke_diem_danh", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ thang, nam })
    })
    .then(res => res.json())
    .then(res => {
        if (res.error) {
            alert(res.error);
            return;
        }
        alert("thành công lấy dữ liệu!")
        renderThongKeDiemDanh(res.data);
    });
});
function renderThongKeDiemDanh(data) {
    const ketQua = document.getElementById("ddKetQua");
    ketQua.innerHTML = ""; // reset phần kết quả

    // -------------------------------
    // Render từng nhân viên
    // -------------------------------
    for (let id_nv in data) {
        const nv = data[id_nv];

        let html = `
            <h6 class="fw-bold mb-2 tk-label">${nv.ho_ten}</h6>
            <div class="table-responsive mb-4">
                <table class="table table-bordered tk-table align-middle">
                    <thead>
                        <tr>
                            <th>Ngày</th>
                            <th>Ca sáng</th>
                            <th>Ca chiều</th>
                            <th>Ca tối</th>
                            <th>Đi muộn</th>
                            <th>Đã điểm danh</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        // Render từng ngày
        nv.records.forEach(r => {
            html += `
                <tr>
                    <td>${r.ngay}</td>
                    <td>${r.ca_sang}</td>
                    <td>${r.ca_chieu}</td>
                    <td>${r.ca_toi}</td>
                    <td>${r.den_muon}</td>
                    <td>${r.da_diem_danh}</td>
                </tr>
            `;
        });

        // Tổng theo nhân viên
        html += `
                <tr>
                    <td colspan="4" class="fw-bold text-end">Tổng</td>
                    <td>${nv.tong_den_muon}</td>
                    <td>${nv.tong_da_diem_danh}</td>
                </tr>
            </tbody>
            </table>
        </div>
        `;

        ketQua.innerHTML += html; // render kết quả mới

    }
}
//xuatfile
document.getElementById("btnExportThongKeCa").addEventListener("click", () => {
    const thang = document.getElementById("tkThang").value;
    const nam = document.getElementById("tkNam").value;

    if (!thang || !nam) {
        alert("Vui lòng chọn tháng và năm trước khi xuất file");
        return;
    }

    // tải file
    window.location.href = `/trangchu/export_thong_ke_ca?thang=${thang}&nam=${nam}`;
});

//xuatfile thong ke diem danh
document.getElementById("btnExportThongKeDiemdanh").addEventListener("click", () => {
    const thang = document.getElementById("ddThang").value;
    const nam = document.getElementById("ddNam").value;

    if (!thang || !nam) {
        alert("Vui lòng chọn tháng và năm trước khi xuất file");
        return;
    }

    // tải file
    window.location.href = `/trangchu/export_thong_ke_diem_danh?thang=${thang}&nam=${nam}`;
});
