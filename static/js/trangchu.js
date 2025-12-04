document.addEventListener('DOMContentLoaded', function() {
    // ==================== Điểm danh ====================
    const checkInMenu = document.getElementById('checkInMenu');
    const checkInBtn = document.getElementById('checkInBtn');

    if(checkInMenu){
        checkInMenu.addEventListener('click', function(){
            const modal = new bootstrap.Modal(document.getElementById('checkInModal'));
            modal.show();
        });
    }

    if(checkInBtn){
        checkInBtn.addEventListener('click', function(){
            const email = document.getElementById('employeeEmail').value.trim();
            if(email){
                // Gửi dữ liệu về server nếu cần
                alert("Điểm danh thành công: " + email);
                bootstrap.Modal.getInstance(document.getElementById('checkInModal')).hide();
            } else {
                alert("Vui lòng nhập email!");
            }
        });
    }

    // ==================== Sửa nhân viên ====================
    const editModal = new bootstrap.Modal(document.getElementById('editModal'));
    document.querySelectorAll('.btn-edit').forEach(function(btn){
        btn.addEventListener('click', function(){
            const currentRow = btn.closest('tr');
            const nhanvienid = currentRow.dataset.id;

            fetch(`/trangchu/sua_nhan_vien?id=${nhanvienid}`) //gửi yêu cầu get đến flask
            .then(res => res.json())
            .then(data => {
                if(data.error){
                    alert(data.error);
                    return;
                }
                document.getElementById('editName').value = data.ho_ten;
                document.getElementById('editPhone').value = data.so_dien_thoai;
                document.getElementById('editEmail').value = data.email;
                document.getElementById('editAddress').value = data.dia_chi;
                document.getElementById('editGender').value = data.gioi_tinh;
                document.getElementById('editBirthDate').value = data.ngay_sinh;
                console.log(data.ngay_sinh)
                document.getElementById('editModal').dataset.id = nhanvienid;

                editModal.show();
            })
            .catch(err => console.error(err));
        });
    });

    document.getElementById('saveEditBtn').addEventListener('click', function(){
        const ma_nv = document.getElementById('editModal').dataset.id;
        const payload = {
            ma_nhan_vien: ma_nv,
            ho_ten: document.getElementById('editName').value,
            so_dien_thoai: document.getElementById('editPhone').value,
            email: document.getElementById('editEmail').value,
            dia_chi: document.getElementById('editAddress').value,
            gioi_tinh: document.getElementById('editGender').value,
            ngay_sinh: document.getElementById('editBirthDate').value
        };

        fetch('/trangchu/sua_nhan_vien', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            if(data.message){
                alert(data.message);
                location.reload();
            } else {
                alert(data.error);
            }
        });
    });

    // ==================== Xóa nhân viên ====================
    document.querySelectorAll('.btn-delete').forEach(function(btn){
        btn.addEventListener('click', function(){
            const currentRow = btn.closest('tr');
            const ma_nv = currentRow.dataset.id;

            if(confirm("Bạn có chắc muốn xóa nhân viên này không?")){
                fetch('/trangchu/xoa_nhan_vien', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ma_nhan_vien: ma_nv})
                })
                .then(res => res.json())
                .then(data => {
                    if(data.message){
                        alert(data.message);
                        currentRow.remove();
                    } else {
                        alert(data.error);
                    }
                });
            }
        });
    });

    
   // ==================== Tìm kiếm, filter, thống kê ====================
const searchInput = document.querySelector('input[placeholder="Tìm kiếm nhân viên"]');
const filterDropdown = document.querySelectorAll('.dropdown-menu a');
const refreshBtn = document.querySelector('.btn-secondary');
const tbody = document.querySelector('table tbody');

const counts = {
    present: document.getElementById('count-present'),
    pending: document.getElementById('count-pending'),
    late: document.getElementById('count-late')
};

function updateTable(search = '', filter = '') {
    let present = 0, pending = 0, late = 0;

    Array.from(tbody.rows).forEach(row => {
        const name = row.cells[0].textContent.toLowerCase();
        const caSang = row.cells[3].textContent.trim();
        const caChieu = row.cells[4].textContent.trim();
        const caToi = row.cells[5].textContent.trim();

        const matchSearch = name.includes(search.toLowerCase());
        const matchFilter = !filter || caSang === filter || caChieu === filter || caToi === filter;

        row.style.display = (matchSearch && matchFilter) ? '' : 'none';

        if (matchSearch && matchFilter) {
            if (caSang === 'Đã điểm danh' || caChieu === 'Đã điểm danh' || caToi === 'Đã điểm danh') present++;
            if (caSang === 'Chưa điểm danh' || caChieu === 'Chưa điểm danh' || caToi === 'Chưa điểm danh') pending++;
            if (caSang === 'Đến muộn' || caChieu === 'Đến muộn' || caToi === 'Đến muộn') late++;
        }
    });

    counts.present.textContent = `${present} nhân viên`;
    counts.pending.textContent = `${pending} nhân viên`;
    counts.late.textContent = `${late} nhân viên`;
}

// Sự kiện tìm kiếm
if (searchInput) {
    searchInput.addEventListener('input', e => updateTable(e.target.value, ''));
}

// Sự kiện filter
filterDropdown.forEach(a => {
    a.addEventListener('click', e => {
        // e.preventDefault();
        const filter = a.textContent.trim();
        updateTable(searchInput.value, filter);
    });
});

// Refresh bảng
if (refreshBtn) {
    refreshBtn.addEventListener('click', () => {
        searchInput.value = '';
        updateTable();
    });
}

// Load mặc định
updateTable();



});
