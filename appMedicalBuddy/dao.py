import hmac
from datetime import datetime

from appMedicalBuddy.models import TaiKhoan, CauHoi, BenhNhan, ThongTinNguoiDung
import hashlib
from appMedicalBuddy import app, db
import cloudinary.uploader
from sqlalchemy import func
from flask_login import current_user


def add_user(username, password, email, tenNguoiDung):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = TaiKhoan(username=username, password=password, email=email, tenNguoiDung=tenNguoiDung)
    db.session.add(u)
    db.session.commit()

    # if avatar:
    #     res = cloudinary.uploader.upload(avatar)
    #     print(res)
    #     u.avatar = res['secure_url']



def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return TaiKhoan.query.filter(TaiKhoan.username.__eq__(username.strip()),
                                 TaiKhoan.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return TaiKhoan.query.get(user_id)


def ma_hoa(data):
    return hmac.new(app.secret_key.encode('utf-8'),
                    data.encode('utf-8'),
                    hashlib.sha256).hexdigest()

def add_question(topic, message):
    q = CauHoi(id_TaiKhoan=current_user.id, chuDe=topic, noiDung=message, ngayGui=datetime.now())
    db.session.add(q)
    db.session.commit()

    return q

def change_password(email, old_password, new_password):
    account_patient = TaiKhoan.query.filter(TaiKhoan.email == email).first()

    old_password = ma_hoa(old_password)
    new_password = ma_hoa(new_password)

    if old_password == account_patient.password:
        account_patient.password = new_password
        db.session.add(account_patient)
        db.session.commit()
        return True

    return False
