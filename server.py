from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from generatemath import generate_equation
app = Flask(__name__)
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = "my_secret_key"

HARDNESS_TO_VAL = {"low": 0, "mid": 1, "high": 2}

from forms.user import LoginForm, RegisterForm
from forms.example import ProblemForm
from data import db_session
from data.users import User
from data.examples import Example

import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logging.getLogger("werkzeug").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).filter(User.id == user_id).first()

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('signup.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == form.email.data.lower()).first() or db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('signup.html', title='Регистрация', form=form,
                                   message="Пользователь с такой почтой или именем уже существует")
        user = User(
            name=form.name.data,
            email=form.email.data.lower()
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('signup.html', title='Регистрация', form=form)

@app.route("/rating")
def rating():
    db_sess = db_session.create_session()
    users = db_sess.query(User.name, User.rating).all()
    users.sort(key=lambda x: x[1], reverse=True)
    final = []
    curr = None
    for i, user in enumerate(users, start=1):
        final.append([i] + list(user))
        if current_user.is_authenticated and user[0] == current_user.name:
            curr = [i] + list(user)
            
    return render_template("rating.html", title="Рейтинг", rate=final, curr=curr)

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
        return render_template('login.html', message="Не правильный логин или пароль.", form=form)
    return render_template('login.html', title='Вход', form=form)

def generate_problem_by_settings(problem_type, hardness, additional, user_name: str=""):
    eq, right = generate_equation(3, 3) # temporarily 
    db_sess = db_session.create_session()
    if user_name:
        user = db_sess.query(User).filter(User.name == user_name).first()
    Example(
        user_id = user.id,
        example = eq,
        hardness = hardness,
        right = right
    )

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    example_id = ""
    answer_form = ProblemForm()
    if request.method == "POST":
        form = request.form.to_dict()
        print(form)
        if "problem_type" in form.keys(): # generate
            if current_user.is_authenticated:
                example, right = generate_problem_by_settings(form["problem_type"], HARDNESS_TO_VAL[form["hardness"]], form["additional"], user=current_user.name)
        elif "example_id" in form.keys(): # test problem
            example = ""
    else:
        example, right = generate_equation(3, 3)
    return render_template("index.html", title="Math website", example=example, problem_form=answer_form)

@app.route('/delete')
@login_required
def delete():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == current_user.name).first()
    examples = db_sess.query(Example).filter(Example.user_id == user.id)
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

@app.route("/profile/<string:name>")
def profile(name: str):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == name).first()
    if not user:
        abort(404)
    examples = db_sess.query(Example).filter(Example.user_id == user.id).all()
    examples.sort(key=lambda x: x.date, reverse=True)
    return render_template("profile.html", title=user.name, profile=user, examples=examples[:20])

def main():
    db_session.global_init("db/dataBase.db")
    app.run()

if __name__ == "__main__":
    main()