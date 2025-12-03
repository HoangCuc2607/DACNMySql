from flask import Blueprint, render_template, flash, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv  
from controllers.TrangchuController import trang_chu_bp

load_dotenv()

PASSWORD_HASH = os.getenv("PASSWORD_HASH")
dang_nhap_bp = Blueprint("dangnhap", __name__)
@dang_nhap_bp.route("/", methods = ['GET', 'POST'])
def dangnhap():
    if request.method == 'GET':
        return render_template("dangnhap.html")
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        if email == "admin@gmail.com" and check_password_hash(PASSWORD_HASH, password):
            session['login'] = True
            return redirect(url_for("trangchu.GetNhanVienDiemDanh"))

        else:
            return render_template("dangnhap.html", error = 'Email hoặc mật khẩu sai!')
