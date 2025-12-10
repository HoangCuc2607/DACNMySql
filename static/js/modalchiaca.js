document.addEventListener('DOMContentLoaded', () => {
    const shiftModalEl = document.getElementById('shiftModal');
    const saveBtn = document.getElementById('saveShiftBtn');
    const nextDateSpan = document.getElementById('nextDate');
    const shiftModal = new bootstrap.Modal(shiftModalEl);

    // Hàm load dữ liệu ca theo ngày
    function loadShiftData(ngay) {
        nextDateSpan.textContent = ngay;
        fetch(`/trangchu/lay_chia_ca/${ngay}`)
            .then(res => {
                if (!res.ok) throw new Error('Chưa có dữ liệu cho ngày này');
                return res.json();
            })
            .then(data => {
                if(data.error)
                {
                    alert(data.error)
                }else{

                ['ca_sang', 'ca_chieu', 'ca_toi'].forEach((caKey, index) => {
                    const i = index + 1;
                    // set giờ bắt đầu/kết thúc
                    document.querySelector(`input[name="ca${i}_start"]`).value = data[caKey].bat_dau || '';
                    document.querySelector(`input[name="ca${i}_end"]`).value = data[caKey].ket_thuc || '';

                    // tick checkbox nhân viên
                    data[caKey].nhanvien_ids.forEach(nv_id => {
                        const checkbox = document.getElementById(`ca${i}_nv${nv_id}`);
                        if (checkbox) checkbox.checked = true;
                    
                    });
                
                })
                ;}

            })
            .catch(err => {
                console.log(err);
                // Nếu chưa có dữ liệu, reset form
                shiftModalEl.querySelectorAll('input[type="time"]').forEach(input => input.value = '');
                shiftModalEl.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
            });
    }

    // Mở modal cho ngày hôm nay (có thể thay đổi theo yêu cầu)
   shiftModalEl.addEventListener('show.bs.modal', () => {
    // Lấy ngày hôm sau
    const tomorrow = new Date();
    console.log("aaaaaaaaaa"+ Date());
    tomorrow.setDate(tomorrow.getDate() + 1);

    const yyyy = tomorrow.getFullYear();
    const mm = String(tomorrow.getMonth() + 1).padStart(2, '0');
    const dd = String(tomorrow.getDate()).padStart(2, '0');

    const tomorrowStr = `${yyyy}-${mm}-${dd}`;
    console.log("mai: "+ tomorrowStr);
    // Load dữ liệu ca của ngày hôm sau
    loadShiftData(tomorrowStr);
});


    // Lưu dữ liệu khi bấm nút
    saveBtn.addEventListener('click', () => {
        const ngay = nextDateSpan.textContent;
        const getCheckedEmployees = i => Array.from(
            document.querySelectorAll(`input[name="ca${i}_employees"]:checked`)
        ).map(cb => cb.value);

        const payload = {
            ngay,
            ca_sang: {
                bat_dau: document.querySelector('input[name="ca1_start"]').value,
                ket_thuc: document.querySelector('input[name="ca1_end"]').value,
                nhanvien_ids: getCheckedEmployees(1)
            },
            ca_chieu: {
                bat_dau: document.querySelector('input[name="ca2_start"]').value,
                ket_thuc: document.querySelector('input[name="ca2_end"]').value,
                nhanvien_ids: getCheckedEmployees(2)
            },
            ca_toi: {
                bat_dau: document.querySelector('input[name="ca3_start"]').value,
                ket_thuc: document.querySelector('input[name="ca3_end"]').value,
                nhanvien_ids: getCheckedEmployees(3)
            }
        };

        fetch('/trangchu/luu_chia_ca', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            alert(data.message || 'Đã lưu thành công!');
            shiftModal.hide();
        })
        .catch(err => {
            console.error(err);
            alert('Lưu thất bại, thử lại sau.');
        });
    });
});

document.getElementById("shiftMenu").addEventListener("click", () => {
    const shiftModal = new bootstrap.Modal(document.getElementById("shiftModal"));
    shiftModal.show();
});
