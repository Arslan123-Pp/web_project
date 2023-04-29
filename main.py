from flask import Flask, render_template, redirect, abort
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from town import get_random_town, do_map_file, get_town_usl_word, clear_selected_towns, check_town_in_selected_list
from town import check_town_in_list, put_in_file_town, get_last_letter
from forms.get_object import GetTownForm
from data import db_session
from forms.user import RegisterForm
from data.users import User, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
town = None
bot_town = get_random_town('Москва')
# первые буквы, на которые должны начинаться города
first_word_town = get_last_letter(bot_town)
first_word_bot_town = ''
# счетчик названных городов
counter_town = 0


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# создание обработчика меню, там находится информация об игре, регистарация, таблица лидеров и сам запуск игры
@app.route('/')
@app.route('/menu')
def menu():
    global town, bot_town, first_word_bot_town, first_word_town, counter_town
    if counter_town != 0 and current_user.is_authenticated:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if not user.record:
            user.record = counter_town
        elif user.record < counter_town:
            user.record = counter_town
        db_sess.commit()
    param = {}
    param['title'] = 'Towns game'
    param['in_game'] = 0
    town = None
    bot_town = get_random_town('Москва')
    first_word_town = get_last_letter(bot_town)
    first_word_bot_town = ''
    counter_town = 0
    return render_template('menu.html', **param)


# создание обработчика игры, там находится сама игра в города
@app.route('/game_town', methods=['GET', 'POST'])
def game_town():
    global town, bot_town, first_word_bot_town, first_word_town, counter_town
    form = GetTownForm()
    if town is None:
        clear_selected_towns()
        town = get_random_town(town)
    param = {}
    param['title'] = 'Towns game'
    param['town'] = bot_town
    param['in_game'] = 1
    do_map_file(get_town_usl_word(first_word_town))
    if form.validate_on_submit():
        town = form.town.data.strip().capitalize()
        # если пользователь нажал кнопку 'подтвердить', то обработчик проверяет, проходит ли под условие игры
        # если пользователь нажал кнопку 'подтвердить', то обработчик проверяет, проходит ли под условие игры
        if first_word_town != form.town.data.strip()[0].lower():
            return render_template('map.html', **param,
                                   form=form,
                                   message="Название города не подходит условию")
        elif not check_town_in_list(town):
            return render_template('map.html', **param,
                                   form=form,
                                   message="Нет такого города")
        elif not check_town_in_selected_list(town):
            return render_template('map.html', **param,
                                   form=form,
                                   message="Такой город уже был")
        form.town.data = ''
        first_word_bot_town = get_last_letter(town)
        bot_town = get_town_usl_word(first_word_bot_town)
        first_word_town = get_last_letter(bot_town)
        put_in_file_town(town)
        put_in_file_town(bot_town)
        do_map_file(get_town_usl_word(first_word_town))
        counter_town += 1
        param['town'] = bot_town
        return render_template('map.html', **param, form=form)
    return render_template('map.html', **param, form=form)


# регистрация пользователя
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            nickname=form.nickname.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# войти в аккаун пользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.nickname == form.nickname.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# таблица рекордов
@app.route("/table_records")
def table_records():
    db_sess = db_session.create_session()
    user_record = -1
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user_record = user.record
    users = db_sess.query(User).all()
    users = sorted([[user.nickname, user.record] for user in users], key=lambda x: x[1], reverse=True)[:10]
    users = [{'record': i[1], 'nickname': i[0]} for i in users]
    return render_template("table_records.html", users=users, record=user_record, in_game=2)


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    app.run(port=8000, host='127.0.0.1')