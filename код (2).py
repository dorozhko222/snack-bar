# Файлы для хранения данных
PRODUCTS_FILE = "products.txt"
ORDERS_FILE = "orders.txt"
REVENUE_FILE = "revenue.txt"

# Меню (название: цена)
ADULT_MENU = {"пицца": 500, "пельмени": 300, "шаурма": 250}
CHILD_MENU = {"пицца": 300, "пельмени": 180, "шаурма": 150}

# Продукты для блюд (блюдо: {продукт: количество})
PRODUCTS_USAGE = {
    "пицца": {"тесто": 1.0, "сыр": 0.3, "томатный_соус": 0.2, "начинка": 0.4},
    "пельмени": {"тесто": 0.2, "фарш": 0.3},
    "шаурма": {"лаваш": 1.0, "овощи": 0.2, "мясо": 0.3, "соус": 0.1}
}

# Загрузка продуктов
products = {}
try:
    products_file = open(PRODUCTS_FILE, "r", encoding="utf-8")
    for line in products_file:
        if ":" in line:
            name, quantity = line.strip().split(":")
            products[name] = float(quantity)
    products_file.close()
except FileNotFoundError:
    # Начальные продукты
    products = {
        "тесто": 10.0, "сыр": 5.0, "томатный_соус": 3.0,
        "начинка": 4.0, "фарш": 3.0, "лаваш": 8.0,
        "овощи": 2.0, "мясо": 3.0, "соус": 2.0
    }
    products_file = open(PRODUCTS_FILE, "w", encoding="utf-8")
    for name, quantity in products.items():
        products_file.write(f"{name}:{quantity}\n")
    products_file.close()

# Загрузка выручки
total_revenue = 0
try:
    revenue_file = open(REVENUE_FILE, "r", encoding="utf-8")
    total_revenue = float(revenue_file.read().strip())
    revenue_file.close()
except FileNotFoundError:
    revenue_file = open(REVENUE_FILE, "w", encoding="utf-8")
    revenue_file.write("0")
    revenue_file.close()

# Ввод данных клиента
print("=== ЗАКУСОЧНАЯ ===")
user_name = input("Ваше имя: ")
surname = input("Ваша фамилия: ")
age = input("Ваш возраст: ")

# Выбор меню
if age.isdigit() and int(age) < 18:
    menu = CHILD_MENU
    menu_type = "детское"
else:
    menu = ADULT_MENU
    menu_type = "взрослое"

print(f"\n{menu_type.upper()} МЕНЮ:")
for item, price in menu.items():
    print(f"{item}: {price} руб")

# Выбор блюд
order = {}
while True:
    dish = input("\nВыберите блюдо (или 'готово' для завершения): ").lower()
    if dish == "готово":
        break
    if dish in menu:
        try:
            quantity = int(input(f"Количество порций {dish}: "))
            if quantity > 0:
                order[dish] = quantity
            else:
                print("Количество должно быть больше 0")
        except ValueError:
            print("Введите число")
    else:
        print("Такого блюда нет в меню")

if not order:
    print("Заказ пуст. До свидания!")
    exit()

# Расчет суммы
total_cost = 0
for dish, quantity in order.items():
    total_cost += menu[dish] * quantity

print(f"\nОбщая сумма: {total_cost} руб")
# Оплата
payment_method = input("\nСпособ оплаты (нал/карта): ").lower()
change = 0

if payment_method == "нал":
    while True:
        try:
            cash = float(input("Введите сумму: "))
            if cash >= total_cost:
                change = cash - total_cost
                print(f"Сдача: {change:.2f} руб")
                break
            else:
                print(f"Недостаточно средств. Нужно еще {total_cost - cash} руб")
        except ValueError:
            print("Введите число")
elif payment_method == "карта":
    print("Оплата картой прошла успешно")
else:
    print("Неверный способ оплаты")
    exit()

# Обновление продуктов
can_cook = True
for dish, quantity in order.items():
    for product, needed in PRODUCTS_USAGE[dish].items():
        total_needed = needed * quantity
        if products.get(product, 0) < total_needed:
            print(f"Недостаточно {product} для {dish}")
            can_cook = False
            break

if not can_cook:
    print("Не можем выполнить заказ - недостаточно продуктов")
    exit()

# Списание продуктов
for dish, quantity in order.items():
    for product, needed in PRODUCTS_USAGE[dish].items():
        products[product] -= needed * quantity
        # Сохранение продуктов
        products_file = open(PRODUCTS_FILE, "w", encoding="utf-8")
        for name, quantity in products.items():
            products_file.write(f"{name}:{quantity}\n")
        products_file.close()

        # Обновление выручки
        total_revenue += total_cost
        revenue_file = open(REVENUE_FILE, "w", encoding="utf-8")
        revenue_file.write(str(total_revenue))
        revenue_file.close()

        # Сохранение заказа
        orders_file = open(ORDERS_FILE, "a", encoding="utf-8")
        orders_file.write(f"{name} {surname} | {age} лет | ")
        orders_file.write(f"{order} | {total_cost} руб | {payment_method}\n")
        orders_file.close()

        # Чек
        print("\n" + "=" * 40)
        print("             ЧЕК")
        print("=" * 40)
        print(f"Клиент: {user_name} {surname}")
        print(f"Возраст: {age} лет")
        print(f"Тип меню: {menu_type}")
        print("-" * 40)
        for dish, quantity in order.items():
            print(f"{dish:15} x{quantity:2} = {menu[dish] * quantity:5} руб")
        print("-" * 40)
        print(f"ИТОГО: {total_cost:26} руб")
        print(f"Оплата: {payment_method:24}")
        if payment_method == "нал":
            print(f"Сдача: {change:26.2f} руб")
        print("=" * 40)
        print("СПАСИБО ЗА ЗАКАЗ!")