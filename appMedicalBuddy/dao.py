import hmac
from datetime import datetime

from appMedicalBuddy.models import TaiKhoan, CauHoi, BenhNhan, ThongTinNguoiDung, DatLichKham
import hashlib
from appMedicalBuddy import app, db
import cloudinary.uploader
from sqlalchemy import func
from flask_login import current_user


def add_user(username, password, email, tenNguoiDung):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = BenhNhan(username=username, password=password, email=email, tenNguoiDung=tenNguoiDung)
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
    q = CauHoi(id_BenhNhan = current_user.id, chuDe=topic, noiDung=message, ngayGui=datetime.now())
    db.session.add(q)
    db.session.commit()

    return q


def add_booking(name=None,email=None, ngayKham=None):
    if name and email:
      taiKhoan= TaiKhoan.query.filter(TaiKhoan.email.__eq__(email)).first()
      if taiKhoan:
          q=DatLichKham(id_BenhNhan=taiKhoan.id,ngayKham=ngayKham)
      else:
          BN=BenhNhan(username=email, tenNguoiDung=name, password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), email=email)
          db.session.add(BN)
          q= DatLichKham(benhnhan=BN, ngayKham=ngayKham)
    else:
        q = DatLichKham(id_BenhNhan = current_user.id, ngayKham=ngayKham)
    db.session.add(q)
    db.session.commit()

    return q

def check_MK(matkhau):
    #tk = TaiKhoan.query.filter(TaiKhoan.username == current_user.username).first()
    return current_user.password==(str(hashlib.md5(matkhau.strip().encode('utf-8')).hexdigest()))

def get_BenhNhan():
    return BenhNhan.query.all()
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
