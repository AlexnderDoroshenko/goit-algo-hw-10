from pulp import LpProblem, LpVariable, LpMaximize, value, LpInteger


def get_arguments(*args, **kwargs):
    expected_arg_count = 4  # Очікується 4 обов'язкових аргументів
    # Створюємо словник ресурсів
    resources = {
        'water':  None,
        'sugar': None,
        'lemon_juice': None,
        'fruit_puree': None,
        0: 'water',
        1: 'sugar',
        2: 'lemon_juice',
        3: 'fruit_puree'
    }

    # Призначення значень з args
    for i in range(len(args)):
        if i < expected_arg_count:  # Обираємо тільки перші 4 ресурси
            resource_name = resources[i]  # Отримуємо ім'я ресурсу за індексом
            resources[resource_name] = args[i]

        # Виходимо з циклу, якщо обробили 3-й індекс
        if i == 3:
            break

    # Додаємо значення з kwargs
    resources.update(kwargs)

    # Перевірка на None значення
    if any(res is None for res in resources.values()):
        not_defined = [{key: value}
                       for key, value in resources.items() if value is None]
        raise ValueError(f"Очікується 4 аргументи, передано {
                         4 - len(not_defined)}.")

    return resources


def optimize_production(*args, **kwargs) -> int:
    """
    Функція для оптимізації виробництва напоїв "Лимонад" та "Фруктовий сік".

    Args:
        *args: Обмеження на ресурси (вода, цукор, лимонний сік, фруктове пюре).
        **kwargs: Додаткові ресурси, які можуть бути передані як (цукор, лимонний сік, фруктове пюре).

    Returns:
        int: Максимальна кількість вироблених напоїв.

    Except:
        ValueError: Якщо кількість переданих аргументів не співпадає з очікуваною або ресурси неповні.
    """

    resources = get_arguments(*args, **kwargs)

    # Задаємо обмеження
    water_limit = resources['water']
    sugar_limit = resources['sugar']
    lemon_juice_limit = resources['lemon_juice']
    fruit_puree_limit = resources['fruit_puree']

    # Ініціалізація проблеми
    problem = LpProblem("Maximize_Production", LpMaximize)

    # Змінні для виробництва напоїв
    lemonade = LpVariable("Lemonade", lowBound=0, cat=LpInteger)
    juice = LpVariable("Juice", lowBound=0, cat=LpInteger)

    # Обмеження ресурсів
    problem += 2 * lemonade + juice <= water_limit, "Water_Constraint"
    problem += lemonade <= sugar_limit, "Sugar_Constraint"
    problem += lemonade <= lemon_juice_limit, "Lemon_Juice_Constraint"
    problem += 2 * juice <= fruit_puree_limit, "Fruit_Puree_Constraint"

    # Функція мети: максимізувати виробництво
    problem += lemonade + juice, "Total_Production"

    # Розв'язання задачі
    problem.solve()

    # Повернення результату
    return int(value(problem.objective))

# Тестування функції з новими обмеженнями


def run_tests():
    # Тест 1: Основний тест
    expected_max_production = 50  # Згідно з розрахунками
    result = optimize_production(100, 50, 30, 40)
    assert result == expected_max_production, (
        f"Тест 1: Очікуваний результат {expected_max_production}, "
        f"отримано {result}"
    )

    # Тест 2: Нульові ресурси
    assert optimize_production(0, 0, 0, 0) == 0, (
        "Тест 2: Очікуваний результат 0, "
        f"отримано {optimize_production(0, 0, 0, 0)}"
    )

    # Тест 3: Обмеження води
    expected_production_water = optimize_production(10, 50, 30, 40)
    assert expected_production_water < expected_max_production, (
        "Тест 3: Обмеження води вплинуло на виробництво."
    )

    # Тест 4: Обмеження цукру
    expected_production_sugar = optimize_production(100, 1, 30, 40)
    assert expected_production_sugar < expected_max_production, (
        "Тест 4: Обмеження цукру вплинуло на виробництво."
    )

    # Тест 5: Обмеження лимонного соку
    expected_production_lemon = optimize_production(100, 50, 0, 40)
    assert expected_production_lemon < expected_max_production, (
        "Тест 5: Обмеження лимонного соку вплинуло на виробництво."
    )

    # Тест 6: Обмеження фруктового пюре
    expected_production_puree = optimize_production(100, 50, 30, 1)
    assert expected_production_puree < expected_max_production, (
        "Тест 6: Обмеження фруктового пюре вплинуло на виробництво."
    )

    # Тест 7: Перевірка на неправильну кількість аргументів
    try:
        optimize_production(100, 50)
    except ValueError as e:
        assert str(e) == "Очікується 4 аргументи, передано 2."

    # Тест 8: Перевірка з одним аргументом в args та трьома в kwargs
    result = optimize_production(
        100, sugar=50, fruit_puree=40, lemon_juice=30)
    assert result == expected_max_production, (
        f"Тест 8: Очікуваний результат {expected_max_production}, "
        f"отримано {result}"
    )

    print("Всі тести пройдені!")


# Виклик функцій та тестів
max_production = optimize_production(100, 50, 30, 40)
print(f"Максимальна кількість вироблених продуктів: {max_production}")
run_tests()
