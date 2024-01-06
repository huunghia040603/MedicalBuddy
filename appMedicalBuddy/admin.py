from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView, Admin
from flask_login import current_user, logout_user
from flask import redirect, request

from appMedicalBuddy.models import LichKham, Thuoc, BenhNhan, YTa, DatLichKham, LichSuBenh, HoaDon, ChiTietHoaDon, \
    CauHoi, TraLoi, QuyDinh, Benh, UserRoleEnum
from appMedicalBuddy import db, app

import utils

class MyAdmin(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(app=app, name='QUẢN TRỊ MEDICAL BUDDY', template_mode='bootstrap4', index_view=MyAdmin())

class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.QUANTRI


class PolyModel(AuthenticatedAdmin):
    excluded_form_columns = ('type',)

    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedView(AuthenticatedAdmin):
    def is_accessible(self):
        return current_user.is_authenticated


class DoctorModelView(AuthenticatedAdmin):
    can_export = True


class YTaModelView(AuthenticatedAdmin):
    can_export = True


class CauHoiModelView(AuthenticatedAdmin):
    can_export = True


class TraLoiModelView(AuthenticatedAdmin):
    can_export = True


class QuyDinhModelView(AuthenticatedAdmin):
    can_export = True


class ThuocModelView(AuthenticatedAdmin):
    can_export = True


class BenhNhanModelView(AuthenticatedAdmin):
    can_export = True


class LichKhamModelView(AuthenticatedAdmin):
    can_export = True


class LichSuBenhModelView(AuthenticatedAdmin):
    can_export = True


class ChiTietHoaDonModelView(AuthenticatedAdmin):
    can_export = True


class HoaDonModelView(AuthenticatedAdmin):
    can_export = True


class BookModelView(AuthenticatedAdmin):
    can_export = True


class BenhModelView(AuthenticatedAdmin):
    can_export = True


class OderView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/HoaDon-list.html")

    def is_accessible(self):
        return current_user.is_authenticated


class ProfilePatinetView(BaseView):
    @expose("/")
    def index(self):
        name_BenhNhan = request.args.get("nameBenhNhan")
        getBenhNhan = utils.get_profile_customer(name_BenhNhan= name_BenhNhan)
        if getBenhNhan:
            mes = "co du lieu"
            return self.render("admin/search-BenhNhan.html", getBenhNhan=getBenhNhan, mes=mes)
        else:
            mes = "chua co du lieu"
            return self.render("admin/search-BenhNhan.html", getBenhNhan=getBenhNhan, mes=mes)

    def is_accessible(self):
        return current_user.is_authenticated


class MenuView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/stats.html")

    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class AllDetailsModelView(BaseView):
    @expose("/")
    def index(self):
        detail = utils.get_all_HoaDons()
        return self.render("admin/HoaDon-list.html", detail=detail)

    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(BaseView):
    @expose("/")
    def index(self):
        date_start = request.args.get("date_start")
        date_end = request.args.get("date_end")
        stats = utils.get_stats_by_date(date_start=date_start, date_end=date_end)
        if stats:
            mes = "Valid data!"
            return self.render("admin/stats.html", stats=stats, mes=mes)
        else:
            mes = "Invalid data!"
            return self.render("admin/stats.html", stats=stats, mes=mes)

    def is_accessible(self):
        return current_user.is_authenticated


class GetDetailView(BaseView):
    @expose("/")
    def index(self):
        name = request.args.get("nameBenhNhan")
        getDetail = utils.get_name_HoaDon_detail(name)
        if getDetail:
            mes = "Valid data!"
            return self.render("admin/HoaDon-details.html", getDetail=getDetail, mes=mes)
        else:
            mes = "Invalid data!"
            return self.render("admin/HoaDon-details.html", getDetail=getDetail, mes=mes)

    def is_accessible(self):
        return current_user.is_authenticated


class DetailByDateView(BaseView):
    @expose("/")
    def index(self):
        date1 = request.args.get("date_start")
        date2 = request.args.get("date_end")
        detail_date = utils.get_all_detail_by_date(date1=date1, date2=date2)
        totaldetail_date = utils.get_totaldetail_by_date(date1=date1, date2=date2)
        if detail_date and totaldetail_date:
            mes = "co du lieu"
            return self.render("admin/detail-date.html", detail_date=detail_date, totaldetail_date=totaldetail_date, mes=mes)
        else:
            mes = "chua co du lieu"
            return self.render("admin/detail-date.html", detail_date=detail_date, totaldetail_date=totaldetail_date, mes=mes)

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(LichKhamModelView(LichKham, db.session, name="LichKham"))

admin.add_view(ThuocModelView(Thuoc, db.session, name="Thuocs", category='Lists'))
admin.add_view(BenhNhanModelView(BenhNhan, db.session, name="BenhNhans", category='Lists'))
admin.add_view(YTaModelView(YTa, db.session, name="YTas", category='Lists'))
admin.add_view(BookModelView(DatLichKham, db.session, name="DatLichKham", endpoint='book-lists', category='Lists'))
admin.add_view(ProfilePatinetView(name="Information BenhNhan", category='Lists'))

admin.add_view(LichSuBenhModelView(LichSuBenh, db.session, name="Type Info Checking", endpoint="Record", category='Medical Examination'))
admin.add_view(HoaDonModelView(HoaDon, db.session, name="Choose Doctor", category='Medical Examination'))
admin.add_view(ChiTietHoaDonModelView(ChiTietHoaDon, db.session, name="Get Thuocs", category='Medical Examination'))
admin.add_view(AllDetailsModelView(name="HoaDon", category="Medical Examination"))
admin.add_view(GetDetailView(name="HoaDon Details", category="Medical Examination"))

admin.add_view(CauHoiModelView(CauHoi, db.session, name="CauHoi", category="Q&A"))
admin.add_view(TraLoiModelView(TraLoi, db.session, name="TraLoi", category="Q&A"))

admin.add_view(QuyDinhModelView(QuyDinh, db.session, name="Rules"))

admin.add_view(BenhModelView(Benh, db.session, name="Benh"))

admin.add_view(StatsView(name="Monthly Report", category="Statistics"))
admin.add_view(DetailByDateView(name="Stats", category="Statistics"))

admin.add_view(MenuView(name="My Profile", endpoint="profile", category="menu"))
admin.add_view(LogoutView(name="Logout", endpoint="logout", category="menu"))
