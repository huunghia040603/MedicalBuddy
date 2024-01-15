import hashlib

from flask_login import current_user

from appMedicalBuddy import db
from appMedicalBuddy.dao import ma_hoa
from appMedicalBuddy.models import TaiKhoan


def hien_phieu_tam_thoi(phieuKham):
    tenBenhNhan, trieuChung, duDoanBenh, id = "", "", "", []
    if phieuKham:
        tenBenhNhan = phieuKham["thongTinKhamBenh"]["tenBenhNhan"]
        trieuChung = phieuKham["thongTinKhamBenh"]["trieuChung"]
        duDoanBenh = phieuKham["thongTinKhamBenh"]["duDoanBenh"]
        id = [int(i) for i in phieuKham["cacLoaiThuoc"]]

    return {
        "tenBenhNhan": tenBenhNhan,
        "trieuChung": trieuChung,
        "duDoanBenh": duDoanBenh,
        "id": id
    }


def chi_tiet_phieu_kham(phieuKham):
    id_Thuoc = []
    if phieuKham:
        id_Thuoc = [id for id in phieuKham["cacLoaiThuoc"].values()]
        total_amount, total_quantity = 0, 0

        # if phieuKham:
        #     for c in phieuKham.values():
        #         total_quantity += c['quantity']
        #         total_amount += c['quantity'] * c['price']
        #
        # return {
        #     "total_amount": total_amount,
        #     "total_quantity": total_quantity,

    return {
        "id_Thuoc": id_Thuoc
    }


def count_price(phieuKham):
    total_price = 0

    if phieuKham:
        for pk in phieuKham["cacLoaiThuoc"].values():
            total_price += int(pk["giaThuoc"]) * int(pk["soLuong"])

    return total_price


