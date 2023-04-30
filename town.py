import random
import requests


# функция отвечает за получение координат определенного города
def get_spn(json_response):
    try:
        crds = \
            json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        lc = crds['boundedBy']['Envelope']['lowerCorner'].split()
        uc = crds['boundedBy']['Envelope']['upperCorner'].split()
        x = str(abs(float(uc[0]) - float(lc[0])) / 30)
        y = str(abs(float(uc[1]) - float(lc[1])) / 30)
        return [x, y]
    except Exception:
        return ['1', '1']


# функция отвечает за создание request города
def get_response(town):
    try:
        toponym_to_find = town
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)

        if not response:
            return None
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        spn = get_spn(json_response)
        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join(spn),
            "l": "map"
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        return requests.get(map_api_server, params=map_params)
    except Exception:
        return None


# функция отвечает за создание png файла определенного города
def do_map_file(town):
    response = get_response(town)
    map_file = "static/img/map.png"
    if response is not None:
        with open(map_file, "wb") as file:
            file.write(response.content)
    return map_file


# функция отвечает за получение случайного города из списка
def get_random_town(last_town):
    with open('Town.txt', 'r', encoding='utf-8') as f:
        lst_towns = [town.strip() for town in f.readlines()]
        town = random.choice(lst_towns)
        while True:
            if last_town != town:
                break
            town = random.choice(lst_towns)
        return town


# функция отвечает за получение города, подходящего под условие
def get_town_usl_word(a):
    f = open("Town.txt", encoding='utf-8')
    s = [x.strip() for x in f.readlines()]
    d = []
    for i in s:
        if i.lower()[0] == a:
            d.append(i)
    return random.choice(d)


# функция проверяет наличие определенного города в списке
def check_town_in_list(town):
    f1 = open("Town.txt", encoding='utf-8')
    s1 = [x.strip() for x in f1.readlines()]
    if town.strip().capitalize() in s1:
        return True
    return False


# функция проверяет наличие определенного города в списке
def check_town_in_selected_list(town):
    f1 = open("selected_towns.txt", encoding='utf-8')
    s1 = [x.strip() for x in f1.readlines()]
    if town.strip().capitalize() not in s1:
        return True
    return False


# функция убирает все выбранные города в списке
def clear_selected_towns():
    with open('selected_towns.txt', 'w') as f:
        pass


# функция кладет выбранные города в список
def put_in_file_town(town):
    f1 = open("selected_towns.txt", encoding='utf-8')
    s1 = [x.strip() for x in f1.readlines()]
    with open('selected_towns.txt', 'w') as f:
        for i in s1:
            f.write(f'{i}\n')
        f.write(f'{town}\n')


# функция возвращает последнюю букву города
def get_last_letter(town):
    if town[-1] in 'ьйъы' and town[-2] in 'ьйъы':
        return town[-3]
    elif town[-1] in 'ьйъы':
        return town[-2]
    return town[-1]
