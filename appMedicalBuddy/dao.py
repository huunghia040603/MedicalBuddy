import hmac
from datetime import datetime

from appMedicalBuddy.models import TaiKhoan, CauHoi, BenhNhan, ThongTinNguoiDung, DatLichKham, Thuoc, DonViThuoc, \
    ChiTietPhieuKham, PhieuKham, HoaDon
import hashlib
from appMedicalBuddy import app, db
import cloudinary.uploader
from sqlalchemy import func, DateTime
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

def addPhieuKham(name=None,trieuChung=None,chungDoan=None,phieuKham=None):
    if name:
        taiKhoan = TaiKhoan.query.filter(TaiKhoan.tenNguoiDung.__eq__(name)).first()
        if taiKhoan:
            lk=PhieuKham(id_BenhNhan=taiKhoan.id,id_BacSi=current_user.id ,ngayKham=datetime.now(),trieuChung=trieuChung,chungDoan=chungDoan)
            db.session.add(lk)
    if phieuKham:
        for c in phieuKham.values():
            d = ChiTietPhieuKham(giaThuoc=c['price'], quantity=c['quantity'], receipt=r, product_id=c['id'])
            db.session.add(d)

    db.session.commit()

    return lk


def check_MK(matkhau):
    #tk = TaiKhoan.query.filter(TaiKhoan.username == current_user.username).first()
    return current_user.password==(str(hashlib.md5(matkhau.strip().encode('utf-8')).hexdigest()))


def get_BenhNhan():
    return BenhNhan.query.all()


def get_Thuoc(kw=None, id=None):
    thuoc = db.session.query(Thuoc, DonViThuoc.tenDVT).join(DonViThuoc, DonViThuoc.id_DVT.__eq__(Thuoc.id_DVT))

    if kw:
        thuoc = thuoc.filter(Thuoc.tenThuoc.contains(kw))

    if id:
        thuoc = thuoc.filter(Thuoc.id_Thuoc.__eq__(id))

    return thuoc.all()


# def get_Thuoc():
#     thuoc = Thuoc.query.filter(Thuoc.tenThuoc.__eq__(name)).first()
#
#     return {
#         "tenThuoc": thuoc.tenThuoc if thuoc else "",
#         "gia": thuoc.gia if thuoc else "",
#         "cachDung": thuoc.cachDung if thuoc else "",
#         "soLuong": soLuong,
#         "donVi": donVi
#     }


def change_password(username, old_password, new_password):
    account_patient = TaiKhoan.query.filter(TaiKhoan.username == username).first()

    if current_user.password==(str(hashlib.md5(old_password.strip().encode('utf-8')).hexdigest())):
        account_patient.password = (str(hashlib.md5(new_password.strip().encode('utf-8')).hexdigest()))
        db.session.add(account_patient)
        db.session.commit()
        return True

    return False

def doanhthu_thongke(month=6):
    query = (db.session.query(func.extract('day', HoaDon.ngayThanhToan),
                              func.count(HoaDon.id_BenhNhan), func.sum(HoaDon.tongTien),
                              func.sum(HoaDon.tongTien) / TongDT(month)[0] * 100)
             .join(BenhNhan, BenhNhan.id.__eq__(HoaDon.id_BenhNhan))
             .filter(func.extract('month', HoaDon.ngayThanhToan).__eq__(month))
             .group_by(func.extract('day', HoaDon.ngayThanhToan))
             .order_by(func.extract('day', HoaDon.ngayThanhToan)))

    return query.all()


def thuoc_thongke(month=9):
    query = (db.session.query(Thuoc.tenThuoc, DonViThuoc.tenDVT, func.sum(ChiTietPhieuKham.soLuongKham),
                              func.count(ChiTietPhieuKham.id_Thuoc))
             .join(DonViThuoc, Thuoc.id_DVT.__eq__(DonViThuoc.id_DVT))
             .join(ChiTietPhieuKham, ChiTietPhieuKham.id_Thuoc.__eq__(Thuoc.id_Thuoc))
             .filter(func.extract("month",PhieuKham.ngayKham).__eq__(month))
             .group_by(Thuoc.tenThuoc, DonViThuoc.tenDVT)
             .order_by(func.count(ChiTietPhieuKham.id_Thuoc),func.sum(ChiTietPhieuKham.soLuongKham)))

    return query.all()

def TongDT(month=6):
    return (db.session.query(func.sum(HoaDon.tongTien))
            .filter(func.extract('month', HoaDon.ngayThanhToan).__eq__(month))).first()

def get_DVT():
    return DonViThuoc.query.all()
    return thuoc.all()


def layThuoc(name="Diltiazem"):
    thuoc = Thuoc.query.filter(Thuoc.tenThuoc.__eq__(name)).first()
    return thuoc.gia


