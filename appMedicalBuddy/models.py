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
    chucVu = Column(String(50))
    soNamLamViec = Column(Integer)
    noiCongTac = Column(String(50), default = "TPHCM")


class YTa(TaiKhoan):
    id = Column(Integer, ForeignKey(TaiKhoan.id), primary_key=True)
    chucVu = Column(String(50),default = "Sơ Cấp" )
    soNamLamViec = Column(Integer)


class NhanVienThuNgan(TaiKhoan):
    id = Column(Integer, ForeignKey(TaiKhoan.id), primary_key=True)
    hesoLuong = Column(Float)


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
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenThuoc = Column(String(50), nullable=False)
    soLuong = Column(Integer, default=0)
    HSD = Column(DateTime, nullable=False)
    ngayNhap = Column(DateTime, nullable=False)
    gia = Column(Float, nullable=False)
    cachDung = Column(String(200), nullable=False)
    ghiChu = Column(String(100))
    id_DVT = Column(Integer, ForeignKey(DonViThuoc.id_DVT), nullable=False)
    CTHD = relationship('ChiTietHoaDon', backref='thuoc', lazy=True)
    CTPK = relationship('ChiTietPhieuKham', backref='thuoc', lazy=True)




class CapNhatDonViThuoc(db.Model):
    id_CapNhatDonViThuoc = Column(Integer, primary_key=True, autoincrement=True)
    id_QuanTri = Column(Integer, ForeignKey(QuanTri.id), nullable=False)
    id_DVT = Column(Integer, ForeignKey(DonViThuoc.id_DVT), nullable=False)
    ngayThayDoi = Column(DateTime, nullable=False)


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())


class PhieuKham(BaseModel):
    id_BacSi = Column(Integer, ForeignKey(BacSi.id), nullable=False)
    id_BenhNhan = Column(Integer, ForeignKey(BenhNhan.id), nullable=False)
    id_Thuoc = Column(Integer, ForeignKey(Thuoc.id))
    ngayKham = Column(DateTime, nullable=False)
    trieuChung = Column(String(200), nullable=False)
    chungDoan = Column(String(100), nullable=False)
    CTPK = relationship('ChiTietPhieuKham', backref='phieukham', lazy=True)


class ChiTietPhieuKham(BaseModel):
    id_Thuoc = Column(Integer, ForeignKey(Thuoc.id), nullable=False)
    soLuongKham = Column(Integer,default=5 )
    giaThuoc = Column(Float, default=0)
    id_PK=Column(Integer, ForeignKey(PhieuKham.id), nullable=False)
    id_DonVi=Column(Integer, ForeignKey(DonViThuoc.id_DVT))

class QuyDinh(db.Model):
    id_QuyDinh = Column(Integer, primary_key=True, autoincrement=True)
    noiDungQuyDinh = Column(String(200), nullable=False)
    tienKham = Column(Float, nullable=False)


class CapNhatQuyDinh(db.Model):
    id_CapNhatQD = Column(Integer, primary_key=True, autoincrement=True)
    id_QuanTri = Column(Integer, ForeignKey(QuanTri.id), nullable=False)
    id_QuyDinh = Column(Integer, ForeignKey(QuyDinh.id_QuyDinh), nullable=False)
    ngayThayDoi = Column(DateTime, nullable=False)


class HoaDon(BaseModel):
    id_NhanVienThuNgan = Column(Integer, ForeignKey(NhanVienThuNgan.id))
    id_BenhNhan = Column(Integer, ForeignKey(BenhNhan.id), nullable=False)
    trangThai = Column(String(100))
    ngayThanhToan = Column(DateTime)
    tienKham = Column(Float)
    tienThuoc = Column(Float)
    tongTien = Column(Float)
    receipt_details = relationship('ChiTietHoaDon', backref='hoadon', lazy=True)


class ChiTietHoaDon(BaseModel):
    id_HoaDon = Column(Integer, ForeignKey(HoaDon.id), nullable=False)
    id_Thuoc = Column(Integer, ForeignKey(Thuoc.id), nullable=False)
    soLuongThuoc = Column(Integer,default=5)
    gia = Column(Float, default=0)


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
      #    import hashlib
      #    p1 = QuanTri(username="admin", email="nghia@ou.edu.vn" ,tenNguoiDung="QT. Huu Nghia",password=str(
      #    hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.QUANTRI)
      #    p2 = BenhNhan(username="bn1",email="2151050277nghia@ou.edu.vn" ,tenNguoiDung="BN.Nguyen Huu Nghia",password=str(
      #    hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.BENHNHAN)
      #    p3=BacSi(username="bsdung", email="dung1965@ou.edu.vn" ,tenNguoiDung="Bs.Nguyễn Trường Dũng",
      #    password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.BACSI)
      #    p4 = BacSi(username="bsthao", email="Thao1986@ou.edu.vn", tenNguoiDung="BS.Trần Phương Thảo", password=str(
      #    hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.BACSI)
      #    p5 = BacSi(username="bshien", email="myHien@ou.edu.vn", tenNguoiDung="BS.Trương Mỹ Hiền", password=str(hashlib.md5(
      #    '123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.BACSI)
      #    p6 = BacSi(username="bstri", email="tritri@ou.edu.vn", tenNguoiDung="BS.Đặng Lê Minh Trí",
      #             password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.BACSI)
      #    p7 = YTa(username="ytavu", email="thienvu@ou.edu.vn", tenNguoiDung="YT.Lê Trần Thiên Vũ",
      #         password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.YTA)
      #
      #    p8 = BenhNhan(username="bn2", email="linh123@gmail.com", tenNguoiDung="BN.Võ Thùy Linh",
      #                  password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.BENHNHAN)
      #    p9 = BenhNhan(username="bn3", email="ngan123@gmail.com", tenNguoiDung="BN.Nguyễn Ngọc Ngân",
      #                  password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.BENHNHAN)
      #    p10 = BenhNhan(username="bn4", email="baobao3094@gmail.com", tenNguoiDung="BN.Trần Quốc Bảo",
      #                  password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.BENHNHAN)
      #    p11 = BenhNhan(username="bn5", email="thaoloveyou@gmail.com", tenNguoiDung="BN.Lê Trần Thảo",
      #                  password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.BENHNHAN)
      #    p12 = NhanVienThuNgan(username="tnvu", email="thienvu45@ou.edu.vn", tenNguoiDung="TN.Lê Trần Vũ",
      #             password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.THUNGAN)
      #
      #    db.session.add_all([p1,p2,p3, p4, p5, p6,p7,p8,p9,p10,p11,p12])
      #    db.session.commit()

         # t = DonViThuoc(tenDVT='Viên')
         # t1 = DonViThuoc(tenDVT='Chai')
         # t2 = DonViThuoc(tenDVT='Gói')
         # t3 = DonViThuoc(tenDVT='Vỉ')
         # t4 = DonViThuoc(tenDVT='Hộp')
         # db.session.add_all([t, t1, t2, t3, t4])
         # db.session.commit()
         # b = Thuoc(tenThuoc='Ticagrelor', soLuong=400, HSD='2026-12-24', ngayNhap='2023-2-15',
         #           cachDung='Nhồi máu cơ tim', id_DVT=1, gia=800000)
         # b1 = Thuoc(tenThuoc='Esomeprazole', soLuong=830, HSD='2026-12-6', ngayNhap='2023-7-18',
         #            cachDung='Chống trào ngược dạ dày thực quản', id_DVT=2, gia=1200000)
         # b2 = Thuoc(tenThuoc='Ranitidine', soLuong=50, HSD='2026-8-2', ngayNhap='2023-3-12',
         #            cachDung='Chống trào ngược dạ dày thực quản', id_DVT=1, gia=720000)
         # b3 = Thuoc(tenThuoc='Sumatriptan', soLuong=960, HSD='2026-3-16', ngayNhap='2023-8-19',
         #            cachDung='Đau nửa đầu', id_DVT=1, gia=360000)
         # b4 = Thuoc(tenThuoc='Diltiazem', soLuong=370, HSD='2026-5-13', ngayNhap='2023-10-25',
         #            cachDung='Điều trị tăng huyết áp', id_DVT=1, gia=3220000)
         # b5 = Thuoc(tenThuoc='Oxycodone', soLuong=400, HSD='2026-8-8', ngayNhap='2023-9-23',
         #            cachDung='Giảm đau', id_DVT=3, gia=980000)
         # b6 = Thuoc(tenThuoc='Nitroglycerine', soLuong=670, HSD='2026-9-28', ngayNhap='2023-11-21',
         #            cachDung='Đau thắt ngực', id_DVT=3, gia=5720000)
         # b7 = Thuoc(tenThuoc='Carisoprodol', soLuong=920, HSD='2026-9-16', ngayNhap='2023-3-15',
         #            cachDung='Giản cơ', id_DVT=4, gia=880000)
         # b8 = Thuoc(tenThuoc='Clindamycin', soLuong=360, HSD='2026-3-13', ngayNhap='2023-6-26',
         #            cachDung='Kháng sinh', id_DVT=1, gia=7200000)
         # b9 = Thuoc(tenThuoc='Omeprazol', soLuong=450, HSD='2025-12-02', ngayNhap='2024-1-09',
         #           cachDung='Điều trị loét dạ dày', id_DVT=1, gia=400000)
         # b10 = Thuoc(tenThuoc='Efferagan', soLuong=200, HSD='2026-1-09', ngayNhap='2024-1-18',
         #            cachDung='Hạ sốt', id_DVT=3, gia=450000)
         # b11 = Thuoc(tenThuoc='Madopar', soLuong=35, HSD='2026-03-03', ngayNhap='2025-04-12',
         #            cachDung='Điều trị bệnh Parkinston', id_DVT=1, gia=600000)
         # b12 = Thuoc(tenThuoc='Medol', soLuong=15, HSD='2025-02-18', ngayNhap='2024-8-21',
         #            cachDung='Chống đau nhức', id_DVT=3, gia=500000)
         # b13 = Thuoc(tenThuoc='Tylenol', soLuong=70, HSD='2028-10-04', ngayNhap='2025-12-30',
         #            cachDung='Giảm đau, hạ sốt', id_DVT=4, gia=150000)
         # b14 = Thuoc(tenThuoc='Acyclovir', soLuong=330, HSD='2025-12-12', ngayNhap='2023-11-25',
         #            cachDung='Điều trị các bệnh do nhiễm virus', id_DVT=3, gia=780000)
         # b15 = Thuoc(tenThuoc='Pepto bismol', soLuong=30, HSD='2024-09-22', ngayNhap='2023-10-07',
         #            cachDung='Điều trị các bệnh về tiêu hóa', id_DVT=2, gia=240000)
         # b16 = Thuoc(tenThuoc='Mysobenal', soLuong=20, HSD='2024-07-18', ngayNhap='2023-03-11',
         #            cachDung='Chống đau thắt lưng', id_DVT=3, gia=600000)
         # b17 = Thuoc(tenThuoc='Venrutine', soLuong=320, HSD='2025-02-02', ngayNhap='2024-01-11',
         #            cachDung='Chống tăng huyết áp', id_DVT=3, gia=300000)
         # b21 = Thuoc(tenThuoc='Arcoxia 60mg MSD', soLuong=250, HSD='2026-12-6', ngayNhap='2023-7-18',
         #            cachDung='điều trị thoái hoá khớp, viêm khớp dạng thấp ', id_DVT=4, gia=350000)
         # b22 = Thuoc(tenThuoc='Anaferon For Children Materia ', soLuong=450, HSD='2026-8-2', ngayNhap='2023-3-12',
         #            cachDung=' điều trị và dự phòng nhiễm virus', id_DVT=1, gia=250000)
         # b23 = Thuoc(tenThuoc='Siro Ambroxol Danapha', soLuong=200, HSD='2026-3-16', ngayNhap='2023-8-19',
         #            cachDung='Điều trị viêm phế quản, hen phế quản', id_DVT=2, gia=120000)
         # b24 = Thuoc(tenThuoc='Amitriptylin 25mg Danapha', soLuong=370, HSD='2026-5-13', ngayNhap='2023-10-25',
         #            cachDung='điều trị trầm cảm', id_DVT=1, gia=380000)
         # b25 = Thuoc(tenThuoc='Allopurinol Stella 300mg', soLuong=400, HSD='2026-8-8', ngayNhap='2023-9-23',
         #            cachDung='điều trị tăng acid uric máu, sỏi thận', id_DVT=4, gia=980000)
         # b26 = Thuoc(tenThuoc='Alaxan United ', soLuong=670, HSD='2026-9-28', ngayNhap='2023-11-21',
         #            cachDung='  giảm các cơn đau cơ xương, nhức đầu, đau bụng kinh, nhức răng ', id_DVT=3, gia=550000)
         # b27 = Thuoc(tenThuoc=' Siro Aerius MSD  ', soLuong=920, HSD='2026-10-16', ngayNhap='2023-3-15',
         #            cachDung=' giảm nhanh các triệu chứng viêm mũi dị ứng, mày đay', id_DVT=1, gia=880000)
         # b28 = Thuoc(tenThuoc='Acemol 325mg Nadyphar', soLuong=360, HSD='2026-3-13', ngayNhap='2023-6-24',
         #            cachDung='hạ sốt và giảm đau', id_DVT=1, gia=800000)
         # b29 = Thuoc(tenThuoc='xịt mũi Aladka', soLuong=250, HSD='2026-12-6', ngayNhap='2023-7-18',
         #            cachDung='điều trị viêm mũi, viêm xoang, viêm mũi dị ứng ', id_DVT=2, gia=180000)
         # b30 = Thuoc(tenThuoc=' Alpha Chymotrypsine Choay Sanofi ', soLuong=580, HSD='2026-8-2', ngayNhap='2023-3-12',
         #            cachDung='điều trị phù nề sau chấn thương, phẩu thuật, bỏng', id_DVT=4, gia=100000)
         # db.session.add_all(
         #    [b, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b12, b11, b13, b14, b15, b16, b17, b21, b22, b23, b24, b25, b26,
         #     b27, b28, b29, b30])
         # db.session.commit()
        #
        #  d1 = PhieuKham(id_BenhNhan=8, id_BacSi=4,id_Thuoc =6, trieuChung='Khó thở', ngayKham='2023-05-13',
        #  chungDoan = "Nhồi máu cơ tim")
        #  d2 = PhieuKham(id_BenhNhan=9, id_BacSi=5, id_Thuoc =6, trieuChung='Thường xuyên nhức đầu', ngayKham='2023-08-28',
        #  chungDoan = "Đau nửa đầu")
        #  d3 = PhieuKham(id_BenhNhan=10, id_BacSi=6,id_Thuoc =6, trieuChung='Mệt mỏi', ngayKham='2023-02-13',
        #  chungDoan = "Bổ sung kháng sinh")
        #  d4 = PhieuKham(id_BenhNhan=11, id_BacSi=4,id_Thuoc =6, trieuChung='Cảm giác tức ngực', ngayKham='2023-06-1',
        #  chungDoan = "Đau thắt cơ ngực")
        #  d5 = PhieuKham(id_BenhNhan=2, id_BacSi=5,id_Thuoc =6, trieuChung='Chóng mặt', ngayKham='2023-09-09',
        #  chungDoan = "Tăng huyết áp")
        #  d6 = PhieuKham(id_BenhNhan=11, id_BacSi=6,id_Thuoc =6, trieuChung='Đau tay', ngayKham='2023-10-10',
        # chungDoan = "Đau cơ do vận động mạnh")
        #  db.session.add_all([d1, d2, d3, d4, d5, d6])
        #  db.session.commit()

         # c = HoaDon( id_BenhNhan=10, id_NhanVienThuNgan=12,  ngayThanhToan='2023-5-13', tienKham=100.000, tienThuoc=730.000,
         #            tongTien=HoaDon.tienKham + HoaDon.tienThuoc)
         # c1 = HoaDon( id_BenhNhan=11, id_NhanVienThuNgan=12,  ngayThanhToan='2023-8-28', tienKham=100.000,
         #             tienThuoc=480.000,
         #             tongTien=HoaDon.tienKham + HoaDon.tienThuoc)
         # c2 = HoaDon( id_BenhNhan=9, id_NhanVienThuNgan=12,  ngayThanhToan='2023-02-13', tienKham=100.000,
         #             tienThuoc=560.000,
         #             tongTien=HoaDon.tienKham + HoaDon.tienThuoc)
         # c3 = HoaDon( id_BenhNhan=8, id_NhanVienThuNgan=12,  ngayThanhToan='2023-6-01', tienKham=100.000,
         #             tienThuoc=260.000,
         #             tongTien=HoaDon.tienKham + HoaDon.tienThuoc)
         # c4 = HoaDon(id_BenhNhan=8, id_NhanVienThuNgan=12,  ngayThanhToan='2023-9-9', tienKham=100.000, tienThuoc=540.000,
         #             tongTien=HoaDon.tienKham + HoaDon.tienThuoc)
         # c5 = HoaDon( id_BenhNhan=9, id_NhanVienThuNgan=12,  ngayThanhToan='2023-10-10', tienKham=100.000,
         #             tienThuoc=840.000,
         #             tongTien=HoaDon.tienKham + HoaDon.tienThuoc)
         # db.session.add_all([c, c1, c2, c3, c4, c5])
         # db.session.commit()
         #   h1 = ChiTietPhieuKham(id_PK=1, id_Thuoc=7,giaThuoc=5720000, soLuongKham=28, id_DonVi=1)
         #   h2 = ChiTietPhieuKham(id_PK=1, id_Thuoc=6,giaThuoc=980000, soLuongKham=28, id_DonVi=2)
         #   h3 = ChiTietPhieuKham(id_PK=1, id_Thuoc=9,giaThuoc=7200000,  soLuongKham=14, id_DonVi=3)
         #   h4 = ChiTietPhieuKham(id_PK=2, id_Thuoc=7,giaThuoc=5720000,  soLuongKham=28, id_DonVi=2)
         #   h5 = ChiTietPhieuKham(id_PK=2, id_Thuoc=6,giaThuoc=980000, soLuongKham=28, id_DonVi=1)
         #   h6 = ChiTietPhieuKham(id_PK=3, id_Thuoc=9,giaThuoc=7200000, soLuongKham=7, id_DonVi=4)
         #   h7 = ChiTietPhieuKham(id_PK=3, id_Thuoc=9,giaThuoc=7200000, soLuongKham=28, id_DonVi=2)
         #   h8 = ChiTietPhieuKham(id_PK=4, id_Thuoc=7,giaThuoc=5720000, soLuongKham=28, id_DonVi=4)
         #   h9 = ChiTietPhieuKham(id_PK=4, id_Thuoc=6,giaThuoc=980000, soLuongKham=14, id_DonVi=4)
         #   h10 = ChiTietPhieuKham(id_PK=4, id_Thuoc=9,giaThuoc=7200000, soLuongKham=14, id_DonVi=4)
         #   h11 = ChiTietPhieuKham(id_PK=5, id_Thuoc=9,giaThuoc=7200000, soLuongKham=7, id_DonVi=2)
         #   h12 = ChiTietPhieuKham(id_PK=6, id_Thuoc=9,giaThuoc=7200000, soLuongKham=14, id_DonVi=3)
         #   db.session.add_all([h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12])
         #   db.session.commit()