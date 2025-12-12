document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');

    // Xử lý khi bấm nút Đăng ký
    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Ngăn form submit mặc định

        // Lấy dữ liệu từ form
        const ho_ten = document.getElementById('ho_va_ten').value.trim();
        const so_dien_thoai = document.getElementById('so_dien_thoai').value.trim();
        const dia_chi = document.getElementById('dia_chi').value.trim();
        const ngay_sinh = document.getElementById('ngay_sinh').value;
        const email = document.getElementById('email').value.trim();
        const gioi_tinh = document.getElementById('gioi_tinh').value;

        // Gửi dữ liệu lên server
        fetch('/trangchu/dangkynhanvien', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ho_ten, so_dien_thoai, dia_chi, ngay_sinh, email, gioi_tinh })
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert("Lỗi: " + data.error);
                return;
            }

            if (data.message && data.qr_url) {

                // Reset form
                LoadForm();

                // Gán QR vào modal
                const qrImg = document.getElementById("qrImage");
                const downloadBtn = document.getElementById("downloadQR");

                qrImg.src = data.qr_url;
                downloadBtn.href = data.qr_url;

                // Hiện modal
                document.getElementById("qrModal").style.display = "flex";
            }

        })
        .catch(err => console.error(err));
    });

    // Xử lý khi bấm nút Hủy
    const cancelButton = document.querySelector('.btn-cancel');
    if (cancelButton) {
        cancelButton.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm("Bạn có chắc muốn hủy đăng ký không?")) {
                window.location.href = "/trangchu";
            }
        });
    }

    // Nút đóng modal
    const closeQR = document.getElementById("closeQR");
    if (closeQR) {
        closeQR.addEventListener("click", () => {
            document.getElementById("qrModal").style.display = "none";
        });
    }
});

// Reset form
function LoadForm() {
    const form = document.getElementById('registrationForm');

    form.querySelector('input[placeholder="Nguyễn Văn A"]').value = "";
    form.querySelector('input[placeholder="0123456789"]').value = "";
    form.querySelector('input[placeholder^="Số nhà"]').value = "";
    form.querySelector('input[type="date"]').value = "";
    form.querySelector('input[placeholder="example@company.com"]').value = "";
    form.querySelector('select[name="gioi_tinh"]').value = "";
}
