import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi

from typing import Callable

# Визначення функції


def f(x):
    return x ** 2

# Метод Монте-Карло


def monte_carlo_integration(func: Callable[[np.ndarray], np.ndarray],
                            a: float,
                            b: float,
                            num_samples: int) -> float:
    """
    Обчислює значення інтеграла функції методом Монте-Карло.

    Параметри:
    - func: Функція, яку потрібно інтегрувати. Має приймати NumPy масив і повертати NumPy масив.
    - a: Нижня межа інтегрування (тип float).
    - b: Верхня межа інтегрування (тип float).
    - num_samples: Кількість випадкових зразків для оцінки площі під кривою (тип int).

    Повертає:
    - Площа під кривою (тип float), що є оцінкою інтеграла функції на заданому інтервалі.
    """
    # Генерація випадкових x та y координат
    x_random = np.random.uniform(a, b, num_samples)
    y_random = np.random.uniform(
        0, max(func(np.linspace(a, b, 1000))), num_samples)

    # Обчислення площі під кривою
    area_under_curve = np.mean(y_random < func(
        x_random)) * (b - a) * max(func(np.linspace(a, b, 1000)))

    return area_under_curve

# Візуалізація


def plot_integration(func, a, b, num_samples=1000):
    # Графік функції
    x = np.linspace(-0.5, 2.5, 400)
    y = func(x)

    fig, ax = plt.subplots()

    # Малювання функції
    ax.plot(x, y, 'r', linewidth=2)

    # Заповнення області під кривою
    ix = np.linspace(a, b, 100)
    iy = func(ix)
    ax.fill_between(ix, iy, color='gray', alpha=0.3)

    # Метод Монте-Карло
    area_monte_carlo = monte_carlo_integration(func, a, b, num_samples)

    # Метод Монте-Карло з меншою кількістю точок
    area_monte_carlo_less_samples = monte_carlo_integration(
        func, a, b, int(num_samples / 100))

    # Обчислення інтеграла за допомогою quad
    area_quad, _ = spi.quad(func, a, b)

    # Налаштування графіка
    ax.set_xlim([x[0], x[-1]])
    ax.set_ylim([0, max(y) + 0.1])
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')

    # Додавання меж інтегрування
    ax.axvline(x=a, color='gray', linestyle='--', label='Lower Bound (a)')
    ax.axvline(x=b, color='gray', linestyle='--', label='Upper Bound (b)')

    # Додавання легенди
    ax.legend()
    ax.set_title(label=f"Графік інтегрування f(x) = x^2 від {
                 str(a)} до {str(b)}")
    # Додавання тексту з результатами розрахунків
    textstr = f'Monte Carlo Area: {
        area_monte_carlo:.4f}\nMonte Carlo Area less samples: {
            area_monte_carlo_less_samples} \nQuad Area: {area_quad:.4f}'
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

    plt.grid()
    plt.show()


# Виклик функції
a = 0  # Нижня межа
b = 2  # Верхня межа
num_samples = 100000  # Кількість випадкових точок

plot_integration(f, a, b, num_samples)
