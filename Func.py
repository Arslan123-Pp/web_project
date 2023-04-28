import random


def func(a):
    t = random.choice([1, 2])
    if t == 1:
        f = open("Town.txt", encoding='utf-8')
    elif t == 2:
        f = open("Town_2.txt", encoding='utf-8')
    s = f.readlines()
    s = [x.strip() for x in s]
    dic = []
    for i in s:
        if i.lower()[0] == a:
            dic.append(i)
    return random.choice(dic)

# while True:
#     # print(func(input()))
#     v = func('б')
#     print(v)
#     if v == 'Бугульма':
#         break
#     v = func('а')
#     print(v)
#     if v == 'Азнакаево':
#         break
