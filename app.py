from flask import Flask, render_template, redirect, url_for, request, session
from controllers.TrangchuController import trang_chu_bp
from controllers.DangnhapController import dang_nhap_bp
from controllers.ModalChiacaController import chia_ca_bp
from controllers.DangkyController import dang_ky_bp
from controllers.ModalDiemdanhController import diem_danh_bp


app = Flask(__name__)
app.secret_key = "abc123"

# Đăng ký các route (blueprint)
app.register_blueprint(trang_chu_bp, url_prefix = "/trangchu")
app.register_blueprint(dang_nhap_bp)
app.register_blueprint(chia_ca_bp, url_prefix = "/trangchu")
app.register_blueprint(dang_ky_bp, url_prefix = "/trangchu")
app.register_blueprint(diem_danh_bp, url_prefix = "/trangchu")



if __name__ == "__main__":
    app.run(debug=True)
