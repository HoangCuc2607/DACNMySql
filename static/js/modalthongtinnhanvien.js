document.addEventListener("DOMContentLoaded", () => {

    const menu = document.getElementById("tatCaNhanVien");
    const tbody = document.getElementById("tbodyNhanVien");

    menu.addEventListener("click", () => {

        fetch("/trangchu/laytatcanhanvien")
            .then(res => res.json())
            .then(data => {
                
                if (data.error) {          
                    alert(data.error);
                    return;
                }

                tbody.innerHTML = "";

                data.forEach(nv => {
                    const row = `
                        <tr>
                            <td>${nv.ma_nhan_vien}</td>
                            <td>${nv.ho_ten}</td>
                            <td>${nv.gioi_tinh}</td>
                            <td>${nv.so_dien_thoai}</td>
                            <td>${nv.email}</td>
                            <td>${nv.ngay_sinh}</td>
                            <td>${nv.dia_chi}</td>
                        </tr>
                    `;
                    tbody.insertAdjacentHTML("beforeend", row);
                });

                new bootstrap.Modal(document.getElementById("dsNhanVienModal")).show();
            })
            .catch(err => console.error(err));

    });

});
