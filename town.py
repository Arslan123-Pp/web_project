import random
import requests


def get_spn(json_response):
    try:
        crds = \
            json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        lc = crds['boundedBy']['Envelope']['lowerCorner'].split()
        uc = crds['boundedBy']['Envelope']['upperCorner'].split()
        x = str(abs(float(uc[0]) - float(lc[0])) / 100)
        y = str(abs(float(uc[1]) - float(lc[1])) / 100)
        return [x, y]
    except Exception:
        return ['1', '1']


def get_response(town):
    toponym_to_find = town
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        pass
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
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


def do_map_file(town):
    response = get_response(town)
    map_file = "static/img/map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


def get_random_town(last_town):
    with open('towns.txt', 'r', encoding='utf-8') as f:
        lst_towns = [town.strip() for town in f.readlines()]
        town = random.choice(lst_towns)
        while True:
            if last_town != town:
                break
            town = random.choice(lst_towns)
        return town