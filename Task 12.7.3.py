per_cent = {'ТКБ': 5.6, 'СКБ': 5.9, 'ВТБ': 4.28, 'СБЕР': 4.0}

money = int(input('money = '))
lst = list(map(lambda num: int(money / 100 * num), per_cent.values()))

print('deposit =', lst)
print('Максимальная сумма, которую вы можете заработать —', max(lst))
