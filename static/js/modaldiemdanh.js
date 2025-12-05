// static/js/checkin.js

document.addEventListener('DOMContentLoaded', () => {
  const saveBtn = document.getElementById('checkInBtn');
  if (!saveBtn) return;

  saveBtn.addEventListener('click', () => {
    const email = document.getElementById('employeeEmail').value.trim();
    const ca = parseInt(document.getElementById('shiftSelect').value);
    const ngay = new Date().toISOString().split('T')[0]; // ngày hôm nay

    if (!email) {
      alert('Vui lòng nhập email!');
      return;
    }

    fetch('/trangchu/diemdanh', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, ca, ngay })
    })
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          alert(data.error);
        } else {
          alert(`${data.message}: ${data.trang_thai}`);
          location.reload()
          // Ẩn modal
          const modalEl = document.getElementById('checkInModal');
          bootstrap.Modal.getInstance(modalEl)?.hide();
        }
      })
      .catch(err => {
        console.error(err);
        alert('Điểm danh thất bại, thử lại sau.');
      });
  });
});
