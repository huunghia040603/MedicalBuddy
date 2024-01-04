from pymysql import Date
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from appMedicalBuddy import db, app
from flask_login import UserMixin
import enum
from datetime import datetime


class UserRoleEnum(enum.Enum):
    QUANTRI = 1
    BACSI = 2
    YTA = 3
    THUNGAN = 4
    BENHNHAN = 5


class TaiKhoan(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.BENHNHAN)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name


class ThongTinNguoiDung(db.Model):
    id_ThongTinNguoiDung = Column(Integer, primary_key=True, autoincrement=True)
    id_TaiKhoan = Column(Integer, ForeignKey(TaiKhoan.id), autoincrement=True)
    tenNguoiDung = Column(String(50), nullable=False)
    soDTNguoiDung = Column(String(100), nullable=False,unique=True)
    email = Column(String(200), nullable=False,unique=True)
    diaChi = Column(String(50), nullable=False)
    namSinh = Column(Integer, nullable=False)
    gioiTinh = Column(Boolean, nullable=False)

class BacSi(TaiKhoan):
    id = Column(Integer, ForeignKey(TaiKhoan.id), primary_key=True, autoincrement=True)
    chucVu = Column(String(50), nullable=False)
    soNamLamViec = Column(Integer, nullable=False)
    noiCongTac = Column(String(50), default = "TPHCM")


class YTa(TaiKhoan):
    id = Column(Integer, ForeignKey(TaiKhoan.id), primary_key=True, autoincrement=True)
    chucVu = Column(String(50),default = "Sơ Cấp" )
    soNamLamViec = Column(Integer, nullable=False)


class NhanVienThuNgan(TaiKhoan):
    id = Column(Integer, ForeignKey(TaiKhoan.id), primary_key=True, autoincrement=True)
    heSoLuong = Column(Float, nullable=False)

class QuanTri(TaiKhoan):
    id = Column(Integer, ForeignKey(TaiKhoan.id), primary_key=True, autoincrement=True)
    chucVu = Column(String(50))


class BenhNhan(TaiKhoan):
    id = Column(Integer, ForeignKey(TaiKhoan.id), primary_key=True, autoincrement=True)


class DanhSachPhieuKham(db.Model):
    id_DanhSachPhieuKham = Column(Integer, primary_key=True, autoincrement=True)
    id_YTa = Column(Integer, ForeignKey(YTa.id), autoincrement=True)
    id_BenhNhan= Column(Integer, ForeignKey(BenhNhan.id), autoincrement=True)


class Thuoc(db.Model):
    id_Thuoc = Column(Integer, primary_key=True, autoincrement=True)
    tenThuoc = Column(String(50), nullable=False)
    hanSuDung = Column(DateTime, nullable=False)
    ngayNhap = Column(DateTime, nullable=False)
    gia = Column(Float, nullable=False)
    cachDung = Column(String(200), nullable=False)
    ghiChu = Column(String(100))


class DonViThuoc(db.Model):
    id_DVT = Column(Integer, primary_key=True, autoincrement=True)
    id_Thuoc = Column(Integer, ForeignKey(Thuoc.id_Thuoc), autoincrement=True)
    tenDVT = Column(String(10), default="Viên")


class CapNhatDonViThuoc(db.Model):
    id_CapNhatDonViThuoc = Column(Integer, primary_key=True, autoincrement=True)
    id_QuanTri = Column(Integer, ForeignKey(QuanTri.id), autoincrement=True)
    id_DVT = Column(Integer, ForeignKey(DonViThuoc.id_DVT), autoincrement=True)
    ngayThayDoi = Column(DateTime, nullable=False)

class PhieuKham(db.Model):
    id_PhieuKham = Column(Integer, primary_key=True, autoincrement=True)
    id_BacSi = Column(Integer, ForeignKey(BacSi.id), autoincrement=True)
    id_BenhNhan = Column(Integer, ForeignKey(BenhNhan.id), autoincrement=True)
    id_Thuoc = Column(Integer, ForeignKey(Thuoc.id_Thuoc), autoincrement=True)
    ngayKham = Column(DateTime, nullable=False)
    trieuChung = Column(String(200), nullable=False)
    chungDoan = Column(String(100), nullable=False)


class ChiTietPhieuKham(db.Model):
    id_ChiTietPhieuKham =  Column(Integer, primary_key=True, autoincrement=True)
    id_Thuoc = Column(Integer, ForeignKey(Thuoc.id_Thuoc), autoincrement=True)
    soLuong = Column(Integer, nullable=False)


class QuyDinh(db.Model):
    id_QuyDinh = Column(Integer, primary_key=True, autoincrement=True)
    noiDungQuyDinh = Column(String(200), nullable=False)
    tienKham = Column(Float, nullable=False)


class CapNhatQuyDinh(db.Model):
    id_CapNhatQD = Column(Integer, primary_key=True, autoincrement=True)
    id_QuanTri = Column(Integer, ForeignKey(QuanTri.id), autoincrement=True)
    id_QuyDinh = Column(Integer, ForeignKey(QuyDinh.id_QuyDinh), autoincrement=True)
    ngayThayDoi = Column(DateTime, nullable=False)


class HoaDon(db.Model):
    id_HoaDon = Column(Integer, primary_key=True, autoincrement=True)
    id_NhanVienThuNgan = Column(Integer, ForeignKey(NhanVienThuNgan.id), autoincrement=True)
    id_BenhNhan = Column(Integer, ForeignKey(BenhNhan.id), autoincrement=True)
    trangThai = Column(String(100), nullable=False)
    tienKham = Column(Float, nullable=False)
    tienThuoc = Column(Float, nullable=False)
    tongTien = Column(Float, nullable=False)


class ChiTietHoaDon(db.Model):
    id_ChiTietHoaDon = Column(Integer, primary_key=True, autoincrement=True)
    id_HoaDon = Column(Integer, ForeignKey(HoaDon.id_HoaDon), autoincrement=True)
    id_Thuoc = Column(Integer, ForeignKey(Thuoc.id_Thuoc), autoincrement=True)
    soLuongThuoc =  Column(Integer, nullable=False)
    donGia = Column(Float, nullable=False)


class LichKham(db.Model):
    id_LichKham = Column(Integer, primary_key=True, autoincrement=True)
    trangThai = Column(String(20), nullable=False)


class DatLichKham(db.Model):
    id_DatLichKham = Column(Integer, primary_key=True, autoincrement=True)
    id_LichKham = Column(Integer, ForeignKey(LichKham.id_LichKham), autoincrement=True)
    id_BenhNhan = Column(Integer, ForeignKey(BenhNhan.id), autoincrement=True)
    ngayKham = Column(DateTime, nullable=False)
    caKham =  Column(String(10), nullable=False)


class Benh(db.Model):
    id_Benh = Column(Integer, primary_key=True, autoincrement=True)
    tenBenh = Column(String(50), nullable=False)
    trieuChung = Column(String(100), nullable=False)
    capDoNguyHiem = Column(Integer)


class LichSuBenh(db.Model):
    id_LichSuBenh = Column(Integer, primary_key=True, autoincrement=True)
    id_Benh = Column(Integer, ForeignKey(Benh.id_Benh), autoincrement=True)
    id_BenhNhan = Column(Integer, ForeignKey(BenhNhan.id), autoincrement=True)
    ngayKham = Column(DateTime, nullable=False)


class CauHoi(db.Model):
    id_CauHoi = Column(Integer, primary_key=True, autoincrement=True)
    id_BenhNhan = Column(Integer, ForeignKey(BenhNhan.id), autoincrement=True)
    ngayGui = Column(DateTime, nullable=False)
    chuDe = Column(String(50), nullable=False)
    noiDung = Column(String(200), nullable=False)

class TraLoi(db.Model):
    id_TraLoi = Column(Integer, primary_key=True, autoincrement=True)
    id_BacSi = Column(Integer, ForeignKey(BacSi.id), autoincrement=True)
    id_CauHoi = Column(Integer, ForeignKey(CauHoi.id_CauHoi), autoincrement=True)
    ngayTraLoi = Column(DateTime, nullable=False)
    noiDungTraLoi = Column(String(500), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()



        # p1 = Product(name='iPhone 13', price=20000000, category_id=1,
        #              image="https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg")
        # p2 = Product(name='Galaxy S23', price=21000000, category_id=1,
        #              image="https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg")
        # p3 = Product(name='iPad Pro 2023', price=22000000, category_id=2,
        #              image="https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg")
        # p4 = Product(name='Galaxy Tab S9', price=28000000, category_id=2,
        #              image="https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg")
        # p5 = Product(name='Note 13', price=20000000, category_id=1,
        #              image="https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg")
        #
        # db.session.add_all([p1, p2, p3, p4, p5])
        # db.session.commit()