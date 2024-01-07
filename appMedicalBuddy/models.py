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
    benhNhan = relationship("BenhNhan", backref="taikhoan", lazy=True)

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
    hesoLuong = Column(Float, nullable=False)


class QuanTri(TaiKhoan):
    id = Column(Integer, ForeignKey(TaiKhoan.id), primary_key=True)
    chucVu = Column(String(50))


class BenhNhan(TaiKhoan):
    id = Column(Integer, ForeignKey(TaiKhoan.id), primary_key=True)
    cauHoi = relationship("CauHoi", backref="benhnhan", lazy=True)
    datLichKham = relationship ("DatLichKham", backref="benhnhan",lazy=True)


class DanhSachPhieuKham(db.Model):
    id_DanhSachPhieuKham = Column(Integer, primary_key=True, autoincrement=True)
    id_YTa = Column(Integer, ForeignKey(YTa.id), nullable=False)
    id_BenhNhan= Column(Integer, ForeignKey(BenhNhan.id), nullable=False)


class DonViThuoc(db.Model):
    id_DVT = Column(Integer, primary_key=True, autoincrement=True)
    tenDVT = Column(String(10), nullable=False)

       
class Thuoc(db.Model):
    id_Thuoc = Column(Integer, primary_key=True, autoincrement=True)
    tenThuoc = Column(String(50), nullable=False)
    soLuong = Column(Integer, default=0)
    HSD = Column(DateTime, nullable=False)
    ngayNhap = Column(DateTime, nullable=False)
    gia = Column(Float, nullable=False)
    cachDung = Column(String(200), nullable=False)
    ghiChu = Column(String(100))
    id_DVT = Column(Integer, ForeignKey(DonViThuoc.id_DVT), nullable=False)


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
    soLuongKham = Column(Integer, nullable=False)


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
    gia = Column(Float, nullable=False)





class DatLichKham(db.Model):
    id_DatLichKham = Column(Integer, primary_key=True, autoincrement=True)
    id_BenhNhan = Column(Integer, ForeignKey(BenhNhan.id), nullable=False)
    ngayKham = Column(DateTime, nullable=False)
    caKham =  Column(String(20))


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
         #
         #
         import hashlib
         # p1 = TaiKhoan(username="admin", email="nghia@ou.edu.vn" ,tenNguoiDung="QT. Huu Nghia",password=str(
         # hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.QUANTRI)
         # p2 = BenhNhan(username="bn1",email="2151050277nghia@ou.edu.vn" ,tenNguoiDung="BN.Nguyen Huu Nghia",password=str(
         # hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.BENHNHAN)
         # p3=TaiKhoan(username="bsdung", email="dung1965@ou.edu.vn" ,tenNguoiDung="Bs.Nguyễn Trường Dũng",
         # password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.BACSI)
         # p4 = TaiKhoan(username="bsthao", email="Thao1986@ou.edu.vn", tenNguoiDung="BS.Trần Phương Thảo", password=str(
         # hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.BACSI)
         # p5 = TaiKhoan(username="bshien", email="myHien@ou.edu.vn", tenNguoiDung="BS.Trương Mỹ Hiền", password=str(hashlib.md5(
         # '123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.BACSI)
         # p6 = TaiKhoan(username="bstri", email="tritri@ou.edu.vn", tenNguoiDung="BS.Đặng Lê Minh Trí",
         #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.BACSI)
         # p7 = TaiKhoan(username="ytavu", email="thienvu@ou.edu.vn", tenNguoiDung="YT.Lê Trần Thiên Vũ",
         #      password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.YTA)

         # p8 = BenhNhan(username="bn2", email="linh123@gmail.com", tenNguoiDung="BN.Võ Thùy Linh",
         #               password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.BENHNHAN)
         # p9 = BenhNhan(username="bn3", email="ngan123@gmail.com", tenNguoiDung="BN.Nguyễn Ngọc Ngân",
         #               password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.BENHNHAN)
         # p10 = BenhNhan(username="bn4", email="baobao3094@gmail.com", tenNguoiDung="BN.Trần Quốc Bảo",
         #               password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.BENHNHAN)
         # p11 = BenhNhan(username="bn5", email="thaoloveyou@gmail.com", tenNguoiDung="BN.Lê Trần Thảo",
         #               password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.BENHNHAN)
         # db.session.add_all([p1,p2,p3, p4, p5, p6,p7,p8,p9,p10,p11])
         #
         # t = DonViThuoc(tenDVT='Viên')
         # t1 = DonViThuoc(tenDVT='Chai')
         # t2 = DonViThuoc(tenDVT='Gói')
         # t3 = DonViThuoc(tenDVT='Vỉ')
         # t4 = DonViThuoc(tenDVT='Hộp')
         # db.session.add_all([t, t1, t2, t3, t4])
         # b = Thuoc(tenThuoc='Ticagrelor', soLuong=400, HSD='2026-12-24', ngayNhap='2023-2-15',
         #           cachDung='Nhồi máu cơ tim', id_DVT=2, gia=800000)
         # b1 = Thuoc(tenThuoc='Esomeprazole', soLuong=830, HSD='2026-12-6', ngayNhap='2023-7-18',
         #            cachDung='Chống trào ngược dạ dày thực quản', id_DVT=5, gia=1200000)
         # b2 = Thuoc(tenThuoc='Ranitidine', soLuong=50, HSD='2026-8-2', ngayNhap='2023-3-12',
         #            cachDung='Chống trào ngược dạ dày thực quản', id_DVT=5, gia=720000)
         # b3 = Thuoc(tenThuoc='Sumatriptan', soLuong=960, HSD='2026-3-16', ngayNhap='2023-8-19',
         #            cachDung='Đau nửa đầu', id_DVT=2, gia=360000)
         # b4 = Thuoc(tenThuoc='Diltiazem', soLuong=370, HSD='2026-5-13', ngayNhap='2023-10-25',
         #            cachDung='Điều trị tăng huyết áp', id_DVT=2, gia=3220000)
         # b5 = Thuoc(tenThuoc='Oxycodone', soLuong=400, HSD='2026-8-8', ngayNhap='2023-9-23',
         #            cachDung='Giảm đau', id_DVT=5, gia=980000)
         # b6 = Thuoc(tenThuoc='Nitroglycerine', soLuong=670, HSD='2026-9-28', ngayNhap='2023-11-21',
         #            cachDung='Đau thắt ngực', id_DVT=2, gia=5720000)
         # b7 = Thuoc(tenThuoc='Carisoprodol', soLuong=920, HSD='2026-9-16', ngayNhap='2023-3-15',
         #            cachDung='Giản cơ', id_DVT=5, gia=880000)
         # b8 = Thuoc(tenThuoc='Clindamycin', soLuong=360, HSD='2026-3-13', ngayNhap='2023-6-26',
         #            cachDung='Kháng sinh', id_DVT=5, gia=7200000)
         # db.session.add_all([b, b1, b2, b3, b4, b5, b6, b7, b8])
         # db.session.commit()