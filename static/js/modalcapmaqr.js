document.addEventListener("DOMContentLoaded", () => {
    const menuItem = document.getElementById("capLaiQR");
    const qrModal = new bootstrap.Modal(document.getElementById("qrRegenerateModal"));
    const generateBtn = document.getElementById("generateQRBtn");
    const emailInput = document.getElementById("emailInput");
    const qrResult = document.getElementById("qrResult");

    // Khi mở menu "Cấp lại QR"
    menuItem.addEventListener("click", () => {
        emailInput.value = "";
        qrResult.innerHTML = "";
        qrModal.show();
    });

    // Tạo lại mã QR
    generateBtn.addEventListener("click", async () => {
        const email = emailInput.value.trim();

        if (!email) {
            alert("Vui lòng nhập email!");
            return;
        }

        qrResult.innerHTML = `
            <span style="color:#00ffaa; font-weight:bold;">Đang tạo QR...</span>
        `;

        try {
            const res = await fetch("/trangchu/cap_lai_qr", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: email })
            });

            const data = await res.json();

            if (data.error) {
                qrResult.innerHTML = `
                    <span style="color:#ff7777; font-weight:bold;">${data.error}</span>
                `;
            } else {
                qrResult.innerHTML = `
                    <span style="color:#00ffaa; font-weight:bold;">Tạo QR thành công!</span><br>
                    <img src="${data.qr_url}" alt="QR Code"><br>
                    <a id="downloadQR" href="${data.qr_url}" download="QR_k.png">Tải QR về</a>
                `;
            }
        } catch (err) {
            qrResult.innerHTML = `
                <span style="color:#ff7777; font-weight:bold;">Lỗi kết nối server!</span>
            `;
        }
    });
});
