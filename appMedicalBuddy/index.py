from flask import render_template, request, redirect, jsonify, session
from flask_login import login_user, logout_user, current_user, login_required

from appMedicalBuddy import app, dao, login,admin


@app.route("/")
def index():
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


@app.route("/profile")
def user_profile():
    return render_template('profile.html')


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/api/cauhoi', methods=["post"])
@login_required
def add_question():
    topic = request.json.get("topic")
    message = request.json.get("message")
    try:
        dao.add_question(topic, message)
    except Exception as ex:
        return jsonify({"message": "can't add questions!"}), 404
    else:
        return jsonify({"message": "add questions success!"}), 200



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
    old = request.form.get("oldPassword")
    new = request.form.get("newPassword")

    if dao.change_password(current_user.patient.account.email, old, new):
        return jsonify({"message": "Change Successful!"}), 200

    return jsonify({"message": "ERROR: Incorrect password!"}), 405



if __name__ == '__main__':
    app.run(debug=True, port=10000)
