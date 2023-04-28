from flask_login import LoginManager, login_user
from flask import Flask, render_template, redirect
from data import db_session
from town import get_random_town, do_map_file
from data.get_object import GetTownForm
from users import User, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
town = None
bot_town = 'Москва'


@login_manager.user_loader
def load_user():
    pass


# создание обработчика меню, там находится информация об игре, регистарация, таблица лидеров и сам запуск игры
@app.route('/')
@app.route('/menu')
def menu():
    param = {}
    param['title'] = 'Towns game'
    param['in_game'] = 0
    return render_template('menu.html', **param)


# создание обработчика игры, там находится сама игра в города
@app.route('/game_town', methods=['GET', 'POST'])
def game_town():
    global town, bot_town
    form = GetTownForm()
    param = {}
    param['title'] = 'Towns game'
    param['town'] = bot_town
    param['in_game'] = 1
    if town is None:
        town = get_random_town(town)
    do_map_file(bot_town)
    if form.validate_on_submit():
        # если пользователь нажал кнопку 'подтвердить', то обработчик проверяет, проходит ли под условие игры
        if bot_town[-1] != form.town.data.strip()[0].lower():
            return render_template('map.html', **param,
                                   form=form,
                                   message="Название города не подходит условию")
        town = form.town.data
        form.town.data = ''
        bot_town = 'Омск'
        param['town'] = bot_town
        do_map_file(bot_town)
        return render_template('map.html', **param, form=form)
    return render_template('map.html', **param, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')