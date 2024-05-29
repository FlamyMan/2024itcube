from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from generatemath import generate_example
app = Flask(__name__)
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = "my_secret_key"

from forms.user import LoginForm, RegisterForm
from forms.example import ExampleForm
from data import db_session
from data.users import User
from data.examples import Examples

import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logging.getLogger("werkzeug").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('signup.html', title='Signing Up', form=form,
                                   message="Passwords are not the same.")
        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == form.email.data.lower()).first() or db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('signup.html', title='Signing Up', form=form,
                                   message="The User with this email already exist.")
        user = User(
            name=form.name.data,
            email=form.email.data.lower()
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('signup.html', title='Signing Up', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.enter.data).first()
        if not user:
            user = db_sess.query(User).filter(User.name == form.enter.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Wrong login or password.", form=form)
    return render_template('login.html', title='Authorisation', form=form)


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    example = generate_example(2)
    form = ExampleForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

    return render_template("index.html", title="Math website", example=example, form=form)

@app.route('/delete')
def delete():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == current_user.name).first()
    examples = db_sess.query(Examples).filter(Examples.user_id == user.id)
    for ex in examples:
        db_sess.delete(ex)
    db_sess.delete(user)
    db_sess.commit()
    logout_user()
    return redirect("/")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/profile/<string:name>", methods=['GET', 'POST'])
def profile(name):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == name).first()
    examples = db_sess.query(Examples).filter(Examples.user_id == user.id).all()
    logger.debug(examples)
    return render_template("profile.html", title=user.name, profile=user, examples=examples)

def main():
    db_session.global_init("db/dataBase.db")
    app.run()

if __name__ == "__main__":
    main()