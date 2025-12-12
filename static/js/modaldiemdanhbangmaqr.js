document.addEventListener("DOMContentLoaded", () => {
    const qrModal = document.getElementById("qrCheckInModal");
    const scanResult = document.getElementById("scanResult");
    const selectShift = document.getElementById("selectShift");
    let qrScanner = null;

    qrModal.addEventListener("shown.bs.modal", () => {
            const today = new Date();
            const yyyy = today.getFullYear();
            const mm = String(today.getMonth() + 1).padStart(2, '0'); 
            const dd = String(today.getDate()).padStart(2, '0');     

            const ngay = `${yyyy}-${mm}-${dd}`;

        scanResult.innerHTML = "";

        qrScanner = new Html5Qrcode("qr-reader");

        qrScanner.start(
            { facingMode: "environment" },
            { fps: 10, qrbox: 250 },

            // Khi đọc được QR
            qrCodeMessage => {
                scanResult.innerHTML = "Đang xử lý...";
                const ca = parseInt(document.getElementById('selectShift').value);

                fetch("/trangchu/diemdanhbangqr", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        tokenqr: qrCodeMessage,
                        ca: ca,
                        ngay: ngay
                    })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.error) {
                        alert(`${data.error}`);
                        scanResult.innerHTML =
                            `<span style="color:#ff7777">${data.error}</span>`;
                    } else {
                            alert(`${data.message}: ${data.trang_thai}`);
                        scanResult.innerHTML =
                            `<span style="color:#00ffaa">${data.message}</span>`;
                    }
                })
                .catch(err => {
                    scanResult.innerHTML =
                        `<span style="color:#ff7777">Lỗi kết nối server</span>`;
                });

                // qrScanner.stop(); // Dừng quét sau khi đã quét xong
            },

            // lỗi khi quét
            errorMessage => {}
        )
        .catch(err => {
            console.error("Không thể mở camera:", err);
            scanResult.innerHTML =
                "Không thể mở camera. Vui lòng kiểm tra quyền truy cập.";
        });
    });

    qrModal.addEventListener("hidden.bs.modal", () => {
        if (qrScanner) qrScanner.stop().catch(() => {});
        scanResult.innerHTML = "";
        document.getElementById("qr-reader").innerHTML = "";
    });
});
