import base64
from flask import render_template, request, redirect, jsonify, session, json
from flask_login import login_user, logout_user, current_user, login_required
import utils
from appMedicalBuddy import app, dao, login, admin


@app.route("/")
def index():
    if session.get("phieuKham"):
        del session["phieuKham"]
    return render_template('index.html')


@app.route('/sign-in', methods=['get', 'post'])
def process_user_login():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('pass')

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            next = request.args.get('next')
            return redirect('/' if next is None else next)

    return render_template('dangnhap.html')


@app.route('/sign-up', methods=['get', 'post'])
def dangky():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('pass')
        confirm = request.form.get('passa')

        if password.__eq__(confirm):
            try:
                dao.add_user(
                    username=request.form.get('username'),
                    password=password,
                    email=request.form.get('email'),
                    tenNguoiDung=request.form.get('name'))
            except Exception as ex:
                print(ex)
                err_msg = str(ex)
            else:
                return redirect('/sign-in')
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('dangky.html', err_msg=err_msg)


@app.route("/log-out")
def process_logout_user():
    logout_user()
    return redirect("/")


@app.route("/question")
def datcauhoi():
    return render_template('cauhoi.html')


@app.route("/schedule")
def lich():
    return render_template('schedule.html')


@app.route("/lapphieukham")
def lapphieukham():
    kw = request.args.get('kw')
    return render_template('doctor/lapphieukham.html',
                           ds_BenhNhan=dao.get_BenhNhan(), ds_Thuoc=dao.get_Thuoc(kw),
                           ds_DVT=dao.get_DVT(), phieuKham=utils.hien_phieu_tam_thoi(session.get("phieuKham")))


@app.route("/modal-booking")
def modal_booking1():
    return render_template('modal-booking.html')


@app.route("/hoadon")
def hoadon():
    return render_template('hoadon.html', ds_chitiet=utils.chi_tiet_phieu_kham(session.get("phieuKham")),
                           total=utils.count_price(session.get("phieuKham")))


@app.route("/api/thanhtoan/<id_thuoc>", methods=["put"])
def update_quantity(id_thuoc):
    phieuKham = session.get("phieuKham")

    soLuong = request.json.get("soLuong")

    if phieuKham and id_thuoc in phieuKham["cacLoaiThuoc"]:
        phieuKham["cacLoaiThuoc"][str(id_thuoc)]["soLuong"] = soLuong

    session["phieuKham"] = phieuKham

    return jsonify(utils.count_price(phieuKham))


@app.route("/contact")
def ketnoi():
    return render_template('contacts.html')


@app.route("/profile")
def user_profile():
    return render_template('profile.html')


@app.route("/about")
def about_us():
    return render_template('about-us.html')


@app.route("/blog")
def mau_blog():
    return render_template('blog.html')


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/api/capnhatthuoc', methods=["post"])
@login_required
def capNhatThuoc():
    tenThuoc = request.json.get("tenThuoc")

    try:
        return dao.get_Thuoc(tenThuoc)
    except Exception as ex:
        return jsonify({"message": str(ex), 'status': 500})


@app.route('/api/ngaykham', methods=["post"])
@login_required
def add_ngayKham():
    ngayKham = request.json.get("ngayKham")
    tenBN = request.json.get("tenBN")
    emailBN = request.json.get("emailBN")

    try:
        dao.add_booking(name=tenBN, email=emailBN, ngayKham=ngayKham)
    except Exception as ex:
        return jsonify({"message": str(ex), 'status': 500}), 404
    else:
        return jsonify({"message": "Lịch khám đã được đặt thành công! Vui lòng đến đúng giờ", 'status': 200}), 200


@app.route('/api/luutamthoi', methods=["post"])
def luutamthoi():
            data = request.json

            phieuKham = session.get("phieuKham")

            if phieuKham is None:
                phieuKham = {}

            tenBenhNhan = data.get("tenBenhNhan")
            trieuChung = data.get("trieuChung")
            duDoanBenh = data.get("duDoanLoaiBenh")

            id = data.get("id")

            phieuKham['thongTinKhamBenh'] = {
                'tenBenhNhan': tenBenhNhan,
                'trieuChung': trieuChung,
                'duDoanBenh': duDoanBenh
            }

            phieuKham["cacLoaiThuoc"] = {}

            for i in id:
                phieuKham["cacLoaiThuoc"][str(i)] = {
                    "id": i,
                    "tenThuoc": dao.get_Thuoc(id=int(i))[0][0].tenThuoc,
                    "giaThuoc": dao.get_Thuoc(id=int(i))[0][0].gia,
                    "soLuong": 5
                }
            session["phieuKham"] = phieuKham

            return utils.hien_phieu_tam_thoi(phieuKham)


@app.route('/api/lapphieukham', methods=['post'])
def lpk():
    luutamthoi()
    return redirect("/hoadon")


@app.route('/api/thanhtoan', methods=['post'])
def pay():
    id = request.json.get("id")
    soLuong = request.json.get("soLuong")

    phieuKham = session.get("phieuKham")

    if phieuKham:
        for i in range(len(id)):
            phieuKham["cacLoaiThuoc"][str(id[i])]["soLuong"] = soLuong[i]

    session["phieuKham"] = phieuKham

    try:
        pass
    except Exception as ex:
        return jsonify({"message": str(ex), "status": 500})


@app.route('/api/check', methods=["post"])
@login_required
def CheckMK():
    matkhau = request.json.get("matkhau")

    try:
        if dao.check_MK(matkhau):
            return jsonify({"message": "Xác Minh Thành Công", 'status': 200})
        else:
            return jsonify({"message": "Xác Minh Thất Bại", 'status': 400})
    except Exception as ex:
        return jsonify({"message": str(ex), 'status': 500})


@app.route('/api/cauhoi', methods=["post"])
@login_required
def add_question():
    topic = request.json.get("topic")
    message = request.json.get("message")
    try:
        dao.add_question(topic, message)
    except Exception as ex:
        return jsonify({"message": "Không thể gửi câu hỏi lúc này!"}), 404
    else:
        return jsonify({"message": "Câu hỏi được gửi thành công!"}), 200


@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route("/api/change-password", methods=["post"])
def change_password():
    old = request.json.get("matkhaucu")
    new = request.json.get("matkhaumoi")

    if dao.change_password(current_user.username, old, new):
        return jsonify({"message": "Change Successful!"}), 200

    return jsonify({"message": "ERROR: Incorrect password!"}), 405


if __name__ == '__main__':
    app.run(debug=True, port=10000)
