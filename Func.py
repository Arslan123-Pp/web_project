import random


def func(a):
    f = open("Town.txt", encoding='utf-8')
    s = f.readlines()
    s = [x.strip() for x in s]
    d = []
    for i in s:
        if i.lower()[0] == a:
            d.append(i)
    return random.choice(d)

# while True:
#     print(func(input()))
    # v = func('б')
    # print(v)
    # if v == 'Бугульма':
    #     break
    # v = func('а')
    # if v == 'Азнакаево':
    #     break
