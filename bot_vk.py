import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
from town import get_random_town, get_town_usl_word, clear_selected_towns, check_town_in_selected_list
from town import check_town_in_list, put_in_file_town, get_last_letter


# функция отправляет сообщения в вк от лица бота
def send_message(user_id, message):
    vk.messages.send(user_id=user_id,
                     message=message,
                     random_id=random.randint(0, 2 ** 64))


# функция отправляет кнопки в вк
def send_button(user_id, message, keyboard):
    vk.messages.send(user_id=user_id,
                     message=message,
                     random_id=random.randint(0, 2 ** 64),
                     keyboard=keyboard.get_keyboard())


# функция добавляет кнопки окончания игры и напоминания буквы
def add_buttons_end_and_hint(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(label='Напомнить букву', color=VkKeyboardColor.POSITIVE)
    send_button(user_id, '-' * 20, keyboard)
    keyboard.add_line()
    keyboard.add_button(label='Закончить игру', color=VkKeyboardColor.NEGATIVE)
    send_button(user_id, '-' * 20, keyboard)


# функция добавляет кнопку играть в города и кнопку правил
def add_buttons_play_and_rules(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(label='Играть в города', color=VkKeyboardColor.POSITIVE)
    send_button(user_id, '-' * 20, keyboard)
    keyboard.add_button(label='Правила игры', color=VkKeyboardColor.POSITIVE)
    send_button(user_id, '-' * 20, keyboard)


def main():
    longpoll = VkLongPoll(vk_session, 220304282)
    last_letter_bot = None
    game_started = False
    counter_towns = 0
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            # в цикле код прослушивает сообщения и выполняет команды
            if event.to_me:
                text = event.text.lower()
                if '[club220304282|@club220304282]' in text:
                    text = text[text.find(' '):]
                user_id = event.user_id
                # если пользователь написал help или помощь, то отправляются сами команды
                if text == 'help' or text == 'помощь':
                    send_message(user_id,
                                 '''Начать игру: start (играть)\n
Закончить игру: end (закончить игру)\n
Напомнить букву: hint (напомнить букву)
                    ''')
                if 'rules' in text or 'правила' in text:
                    send_message(user_id, '''Предлагаем сыграть в нашу игру под названием «Угадай город».
Суть игры проста, вы пишите город, который совпадает с условиями:
Первая буква вашего названного города должна совпадать с конечной
(если конечно он не заканчивается на й, или ы, или ь), который написал bot.
Вы не можете писать города, которые уже раннее были назаваны.''')
                # если пользователь написал end или закончить игру, то игра в города заканчивается
                if 'end' in text or 'закончить игру' in text:
                    send_message(user_id, f'Количество названных вами городов: {counter_towns}')
                    game_started = False
                # выполняется проверка условий игры в город, и если все подходит - бот называет другой город
                if game_started and 'hint' not in text and \
                        'напомнить букву' not in text and 'help' not in text \
                        and 'помощь' not in text and 'правила' not in text and 'rules' not in text:
                    town = text.lower().strip().capitalize()
                    first_letter_your = town[0].lower()
                    if not check_town_in_selected_list(town):
                        send_message(user_id, 'Такой город уже был >:(')
                        send_message(user_id, f'Назовите город на букву "{last_letter_bot}"')
                    elif not check_town_in_list(town):
                        send_message(user_id, 'Такого города не существует >:(')
                        send_message(user_id, f'Назовите город на букву "{last_letter_bot}"')
                    elif last_letter_bot == first_letter_your:
                        town_bot = get_town_usl_word(get_last_letter(town))
                        put_in_file_town(town_bot)
                        put_in_file_town(town)
                        last_letter_bot = get_last_letter(town_bot)
                        send_message(user_id, town_bot)
                        counter_towns += 1
                    else:
                        send_message(user_id, 'Город не подходит условию')
                        send_message(user_id, f'Назовите город на букву "{last_letter_bot}"')
                # если пользователь написал hint или напомнить букву, то бот напоминает на какую букву вы должны
                # написать город
                if 'hint' in text or 'напомнить букву' in text:
                    send_message(user_id, f'Вы должны назвать город на букву "{last_letter_bot}"')
                # если пользователь написал start или играть, то бот начинает игру в города
                if ('start' in text or 'играть' in text) and not game_started:
                    clear_selected_towns()
                    send_message(user_id, 'Я начну')
                    town_bot = get_random_town('Москва')
                    send_message(user_id, town_bot)
                    last_letter_bot = get_last_letter(town_bot)
                    game_started = True
                    counter_towns = 0
                    put_in_file_town(town_bot)
                # если игра уже началась, то у пользователся появляются кнопки заканчивания игры и напоминания буквы
                if game_started:
                    add_buttons_end_and_hint(user_id)
                # иначе бот отправляет саму кнопку игры и как в нее играть
                else:
                    add_buttons_play_and_rules(user_id)


if __name__ == '__main__':
    # токен и вк сессия
    TOKEN = 'vk1.a.i2zBg-uq1E2rDk2acvVSejttCWal4Q_DHewLVYwRV64NK11O2O8U76MTXTVA5yybRRoCLw8FSf4NeN37r3UfFP73cwuX_0biGdiIQNOlJfpcFO-CQxXAR_RSR9CzrC6wgBnsykXuKqfaA0B4WqzheEyJEVHQ-XX_YrXTOjoj4Cuu43QbwioMQccSoTwLWoLAb0MYwzUbI0m3uRfl0FRSAA'
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
    main()