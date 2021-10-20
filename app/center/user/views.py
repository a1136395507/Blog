from . import bp
from flask_login import login_user
from flask import flash, request,redirect, render_template
from app.form.user_form import LoginForm, RegisterForm


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        try:

            user = User.query.filter(User.username == form.username.data,
                                     User.password == form.password.data,
                                     User.roles == "admin").first()
            if user:
                login_user(user)
                flash(message="登录成功")
                return redirect("home")
            else:
                flash(message="密码不正确", category="error")
                return render_template('login.html', form=form)
        except Exception as e:
            print(e)
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)
