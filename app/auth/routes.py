from . import auth_bp
from .models import User
from.forms import LoginForm, SignupForm
import logging
from werkzeug.urls import url_parse
from flask_login import login_user, log_out
from flask import current_user, redirect, request, url_for, render_template


logger = logging.getLogger(__name__)

@auth_bp.route('/login/', methods= ['GET', 'POST'])
def go_login():
    if current_user.is_authenticated:
        return redirect('index')

    form = LoginForm()
    if form.validate_on_submit():
        user=User.get_by_email(form.email.data)

        if user is None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page= request.args.get(url_for('public.index'))
#Como funciona el next page?! Se que es para darle seguridad a la pagina pe
            if not next_page or url_parse(next_page).netlog !='':
                return redirect('index')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/signup/', methods=['GET','POST'])
def go_signup():
    form=SignupForm()
    if form.validate_on_submit():
        name=form.name.data
        email=form.email.data
        password=form.password.data

        user=User.get_by_email(email)
        error=None
        if user is not None:
            error=f'La cuenta {email} ya existe.'
        else:
            user=User(name=name, email=email)
            user.set_password(password)
            user.save()

            login_user(user, remember=True)
            next_page= request.args.get(url_for('index'))
#Como funciona el next page?! Se que es para darle seguridad a la pagina pe
            if not next_page or url_parse(next_page).netlog !='':
                return redirect('index')
    return render_template('auth/signup', form=form, error=error)
        






