document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');

    // Xử lý khi bấm nút Đăng ký
    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Ngăn form submit mặc định

        // Lấy dữ liệu từ form
        const ho_ten = form.querySelector('input[placeholder="Nguyễn Văn A"]').value;
        const so_dien_thoai = form.querySelector('input[placeholder="0123456789"]').value;
        const dia_chi = form.querySelector('input[placeholder^="Số nhà"]').value;
        const ngay_sinh = form.querySelector('input[type="date"]').value;
        const email = form.querySelector('input[placeholder="example@company.com"]').value;
        const gioi_tinh = form.querySelector('select[name = "gioi_tinh"]').value;

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
            if (data.message) {
                alert(data.message);
                LoadForm();
                // window.location.href = "/trangchu";
            } else if (data.error) {
                alert("Lỗi: " + data.error);
            }
        })
        .catch(err => console.error(err));
    });

    // Xử lý khi bấm nút Hủy
    const cancelButton = document.querySelector('.btn-cancel');
    if (cancelButton) {
        cancelButton.addEventListener('click', function(e) {
            e.preventDefault(); // Ngăn form reset mặc định
            if (confirm("Bạn có chắc muốn hủy đăng ký không?")) {
                window.location.href = "/trangchu"; // Quay về trang chủ
            }
        });
    }
});

function LoadForm() {
    const form = document.getElementById('registrationForm');

    form.querySelector('input[placeholder="Nguyễn Văn A"]').value = "";
    form.querySelector('input[placeholder="0123456789"]').value = "";
    form.querySelector('input[placeholder^="Số nhà"]').value = "";
    form.querySelector('input[type="date"]').value = "";
    form.querySelector('input[placeholder="example@company.com"]').value = "";
    form.querySelector('select[name="gioi_tinh"]').value = "";
}
