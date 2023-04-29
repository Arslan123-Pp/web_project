import random


def func(a):
    f = open("towns.txt.txt", encoding='utf-8')
    s = f.readlines()
    s = [x.strip() for x in s]
    dic = []
    for i in s:
        if i.lower()[0] == a:
            dic.append(i)
    return random.choice(dic)
#
# while True:
#     print(func(input()))
#     v = func('б')
#     print(v)
#     if v == 'Бугульма':
#         break
#     v = func('а')
#     print(v)
#     if v == 'Азнакаево':
#         break
