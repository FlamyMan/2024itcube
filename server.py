from flask import Flask, render_template, redirect, request, abort, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from generatemath import generate_equation


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = "my_secret_key"

HARDNESS_TO_VAL = {"low": 0, "mid": 1, "high": 2}
EXAMPLE_TYPE_TO_VAL = {"calc": 0, "equation": 1, "inequality": 2}
STATUS_TO_VAL = {"not_finished": 0, "ok": 1, "filed": 2}


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

def generate_problem_by_settings(problem_type: int, hardness:int, additional: str, user_name: str=None) -> int:
    eq, right = generate_equation(3, 3) # temporarily 
    db_sess = db_session.create_session()
    if user_name:
        userid = db_sess.query(User).filter(User.name == user_name).first().id
    else:
        userid = None
    ex = Example(
        user_id = userid,
        example = eq,
        example_type = problem_type,
        hardness = hardness,
        status = STATUS_TO_VAL["not_finished"],
        right = right
    )
    db_sess.add(ex)
    db_sess.commit()
    id_sess = db_sess.query(Example).filter(Example.user_id == userid).filter(Example.example == eq).filter(Example.status == STATUS_TO_VAL["not_finished"]).first().id
    return id_sess
    
def getExample(id: int, db_sess=None) -> Example:
    if not db_sess:
        db_sess = db_session.create_session()
    return db_sess.query(Example).filter(Example.id == id).first()

def user_to_null_or_name(user):
    if user.is_authenticated:
        return user.name
    else:
        return None
    
@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    example_id: int
    example: Example
    answer_form = ProblemForm()
    pr_type = int(request.cookies.get("P_TYPE", EXAMPLE_TYPE_TO_VAL["calc"]))
    hardness = int(request.cookies.get("HARDNESS", HARDNESS_TO_VAL["mid"]))
    additional = request.cookies.get("ADDITIONAL", "no")
    last_ex_id = int(request.cookies.get("LAST_EXAMPLE_ID", 0))
    last_answer = request.cookies.get("LAST_ANS", 0)
    if request.method == "POST":
        form = request.form.to_dict()
        print(form)
        if "problem_type" in form.keys(): # generate
            pr_type = EXAMPLE_TYPE_TO_VAL[form["problem_type"]]
            hardness = HARDNESS_TO_VAL[form["hardness"]]
            additional = form["additional"]
        elif "example_id" in form.keys(): # test problem
            db_sess = db_session.create_session()
            example_id = form["example_id"]
            last_ex_id = example_id
            example = getExample(example_id, db_sess=db_sess)
            ans = form["answer"]
            last_answer = ans
            if example.right == ans:
                example.status = STATUS_TO_VAL["ok"]
            else:
                example.status = STATUS_TO_VAL["filed"]
            db_sess.commit()

    example_id = generate_problem_by_settings(pr_type, hardness, additional, user_name=user_to_null_or_name(current_user))
    example = getExample(example_id)
    
    kwargs = {"title":"Math website", "example_id": example_id, "example": example.example, "problem_form": answer_form}
    res = make_response(render_template("index.html", **kwargs))
    res.set_cookie('P_TYPE', str(pr_type))
    res.set_cookie('HARDNESS', str(hardness))
    res.set_cookie('ADDITIONAL', str(additional))
    res.set_cookie('LAST_EXAMPLE_ID', str(last_ex_id))
    return res

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