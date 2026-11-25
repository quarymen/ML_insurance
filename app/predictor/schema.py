INPUT_SCHEMA = {
    'Gender': {'type': 'choice', 'choices': [('Male', 'Мужской'), ('Female', 'Женский')], 'label': 'Пол'},
    'Age': {'type': 'int', 'min': 18, 'max': 100, 'label': 'Возраст'},
    'Driving_License': {'type': 'choice', 'choices': [(1, 'Есть'), (0, 'Нет')], 'label': 'Водительские права'},
    'Region_Code': {'type': 'float', 'label': 'Код региона'},
    'Previously_Insured': {'type': 'choice', 'choices': [(1, 'Да'), (0, 'Нет')], 'label': 'Ранее был застрахован'},
    'Vehicle_Age': {'type': 'choice', 'choices': [('< 1 Year', '< 1 года'), ('1-2 Year', '1-2 года'), ('> 2 Years', '> 2 лет')], 'label': 'Возраст автомобиля'},
    'Vehicle_Damage': {'type': 'choice', 'choices': [('Yes', 'Да'), ('No', 'Нет')], 'label': 'Были повреждения авто'},
    'Annual_Premium': {'type': 'float', 'min': 0, 'label': 'Годовая страховая премия'},
    'Policy_Sales_Channel': {'type': 'float', 'label': 'Канал продаж'},
    'Vintage': {'type': 'int', 'label': 'Стаж клиента (дней)'},
}