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
    tenNguoiDung = Column(String(50), nullable=False)
    email = Column(String(200), nullable=False,unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.BENHNHAN)
    def __str__(self):
        return self.name


class ThongTinNguoiDung(db.Model):
    id_ThongTinNguoiDung = Column(Integer, primary_key=True, autoincrement=True)
    id_TaiKhoan = Column(Integer, ForeignKey(TaiKhoan.id), nullable=False)
    soDTNguoiDung = Column(String(100), nullable=False,unique=True)
    diaChi = Column(String(50), nullable=False)


class BacSi(TaiKhoan):
    id = Column(Integer, ForeignKey(TaiKhoan.id), primary_key=True)
    chucVu = Column(String(50), nullable=False)
    soNamLamViec = Column(Integer, nullable=False)
    noiCongTac = Column(String(50), default = "TPHCM")


class YTa(TaiKhoan):
    id = Column(Integer, ForeignKey(TaiKhoan.id), primary_key=True)
    chucVu = Column(String(50),default = "Sơ Cấp" )
    soNamLamViec = Column(Integer, nullable=False)


class NhanVienThuNgan(TaiKhoan):
    id = Column(Integer, ForeignKey(TaiKhoan.id), primary_key=True)
    heSoLuong = Column(Float, nullable=False)


class QuanTri(TaiKhoan):
    id = Column(Integer, ForeignKey(TaiKhoan.id), primary_key=True)
    chucVu = Column(String(50))


class BenhNhan(TaiKhoan):
    id = Column(Integer, ForeignKey(TaiKhoan.id), primary_key=True)


class DanhSachPhieuKham(db.Model):
    id_DanhSachPhieuKham = Column(Integer, primary_key=True, autoincrement=True)
    id_YTa = Column(Integer, ForeignKey(YTa.id), nullable=False)
    id_BenhNhan= Column(Integer, ForeignKey(BenhNhan.id), nullable=False)


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
    id_Thuoc = Column(Integer, ForeignKey(Thuoc.id_Thuoc), nullable=False)
    tenDVT = Column(String(10), default="Viên")


class CapNhatDonViThuoc(db.Model):
    id_CapNhatDonViThuoc = Column(Integer, primary_key=True, autoincrement=True)
    id_QuanTri = Column(Integer, ForeignKey(QuanTri.id), nullable=False)
    id_DVT = Column(Integer, ForeignKey(DonViThuoc.id_DVT), nullable=False)
    ngayThayDoi = Column(DateTime, nullable=False)

class PhieuKham(db.Model):
    id_PhieuKham = Column(Integer, primary_key=True, autoincrement=True)
    id_BacSi = Column(Integer, ForeignKey(BacSi.id), nullable=False)
    id_BenhNhan = Column(Integer, ForeignKey(BenhNhan.id), nullable=False)
    id_Thuoc = Column(Integer, ForeignKey(Thuoc.id_Thuoc), nullable=False)
    ngayKham = Column(DateTime, nullable=False)
    trieuChung = Column(String(200), nullable=False)
    chungDoan = Column(String(100), nullable=False)


class ChiTietPhieuKham(db.Model):
    id_ChiTietPhieuKham =  Column(Integer, primary_key=True, autoincrement=True)
    id_Thuoc = Column(Integer, ForeignKey(Thuoc.id_Thuoc), nullable=False)
    soLuong = Column(Integer, nullable=False)


class QuyDinh(db.Model):
    id_QuyDinh = Column(Integer, primary_key=True, autoincrement=True)
    noiDungQuyDinh = Column(String(200), nullable=False)
    tienKham = Column(Float, nullable=False)


class CapNhatQuyDinh(db.Model):
    id_CapNhatQD = Column(Integer, primary_key=True, autoincrement=True)
    id_QuanTri = Column(Integer, ForeignKey(QuanTri.id), nullable=False)
    id_QuyDinh = Column(Integer, ForeignKey(QuyDinh.id_QuyDinh), nullable=False)
    ngayThayDoi = Column(DateTime, nullable=False)


class HoaDon(db.Model):
    id_HoaDon = Column(Integer, primary_key=True, autoincrement=True)
    id_NhanVienThuNgan = Column(Integer, ForeignKey(NhanVienThuNgan.id), nullable=False)
    id_BenhNhan = Column(Integer, ForeignKey(BenhNhan.id), nullable=False)
    trangThai = Column(String(100), nullable=False)
    tienKham = Column(Float, nullable=False)
    tienThuoc = Column(Float, nullable=False)
    tongTien = Column(Float, nullable=False)


class ChiTietHoaDon(db.Model):
    id_ChiTietHoaDon = Column(Integer, primary_key=True, autoincrement=True)
    id_HoaDon = Column(Integer, ForeignKey(HoaDon.id_HoaDon), nullable=False)
    id_Thuoc = Column(Integer, ForeignKey(Thuoc.id_Thuoc), nullable=False)
    soLuongThuoc =  Column(Integer, nullable=False)
    donGia = Column(Float, nullable=False)


class LichKham(db.Model):
    id_LichKham = Column(Integer, primary_key=True, autoincrement=True)
    trangThai = Column(String(20), nullable=False)


class DatLichKham(db.Model):
    id_DatLichKham = Column(Integer, primary_key=True, autoincrement=True)
    id_LichKham = Column(Integer, ForeignKey(LichKham.id_LichKham), nullable=False)
    id_BenhNhan = Column(Integer, ForeignKey(BenhNhan.id), nullable=False)
    ngayKham = Column(DateTime, nullable=False)
    caKham =  Column(String(10), nullable=False)


class Benh(db.Model):
    id_Benh = Column(Integer, primary_key=True, autoincrement=True)
    tenBenh = Column(String(50), nullable=False)
    trieuChung = Column(String(100), nullable=False)
    capDoNguyHiem = Column(Integer)


class LichSuBenh(db.Model):
    id_LichSuBenh = Column(Integer, primary_key=True, autoincrement=True)
    id_Benh = Column(Integer, ForeignKey(Benh.id_Benh), nullable=False)
    id_BenhNhan = Column(Integer, ForeignKey(BenhNhan.id), nullable=False)
    ngayKham = Column(DateTime, nullable=False)


class CauHoi(db.Model):
    id_CauHoi = Column(Integer, primary_key=True, autoincrement=True)
    id_BenhNhan = Column(Integer, ForeignKey(BenhNhan.id), nullable=False)
    ngayGui = Column(DateTime, default=datetime.now())
    chuDe = Column(String(50), nullable=False)
    noiDung = Column(String(200), nullable=False)

class TraLoi(db.Model):
    id_TraLoi = Column(Integer, primary_key=True, autoincrement=True)
    id_BacSi = Column(Integer, ForeignKey(BacSi.id), nullable=False)
    id_CauHoi = Column(Integer, ForeignKey(CauHoi.id_CauHoi), nullable=False)
    ngayTraLoi = Column(DateTime, default=datetime.now())
    noiDungTraLoi = Column(String(500), nullable=False)


if __name__ == '__main__':
    with app.app_context():
         db.create_all()


       # import hashlib
       # p1 = TaiKhoan(username="admin", password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.QUANTRI)
       # db.session.add(p1)
       # db.session.commit()

