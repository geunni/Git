from flask import Blueprint , render_template , request , url_for , flash , session
from AI.forms import UserCreateForm , UserLoginForm
from .. import db
from AI.models import User
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash , check_password_hash
from datetime import datetime

bp =Blueprint('auth' , __name__ , url_prefix='/auth')

# 회원가입
@bp.route('/signup' , methods = ('GET' , 'POST'))
def signup():
    form = UserCreateForm()
    print("-"*10)
    if request.method == 'POST' and form.validate_on_submit():
        print('-'*10)
        user = User.query.filter_by(username = form.username.data).first()
        if not user:
            user = User(username = form.username.data , password = generate_password_hash(form.password1.data) ,
                        name = form.name.data , birthday = form.birthday.data , gender = form.gender.data , address1 = form.address1.data ,
                        address2 = form.address2.data , email = form.email.data , phone = form.phone.data , reg_date = datetime.now())
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("main.index"))
        else:
            flash("이미 존재하는 유저입니다.")
    return render_template('auth/signup.html' , form=form)

# 로그인
@bp.route('/signin/', methods=('GET', 'POST'))
def signin():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/sign.html', form=form)