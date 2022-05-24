def search_salary():
    value = int(input('Минимальная зарплата: '))
    res = vacations.find({'$or':
                              [{'salary_currency': 'руб.',
                                    '$or': [
                                        {'salary_min': {'$gt': value}},
                                        {'salary_max': {'$gt': value}},]
                                }]
                            })

    return list(res)

res = search_by_salary()
pprint(res)