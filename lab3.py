import random

class StoreSimulation:
    def __init__(self):
        # Начальные параметры моделирования
        self.VAT_rate = 0.2            # ставка НДС, 20%
        self.account = 20000.0         # расчетный счет
        self.shop_inventory = 0        # товары на складе магазина
        self.basic_inventory = 500     # товары на основном складе
        self.in_transit = 0            # товары на промежуточном складе (in_transit)
        self.daily_spending = 1000.0   # ежедневные расходы
        
        # Параметры оптового предложения
        self.wholesale_offer_volume = 30    # объем партии
        self.wholesale_offer_price = 2000.0   # цена партии
        self.unit_price_wholesale = 50.0      # цена за единицу товара в оптовом предложении
        
        # Параметры розничной торговли
        self.retail_price = 100.0             # розничная цена товара
        self.current_demand = 20              # текущий спрос (единиц товара)
        
        # Временные параметры
        self.model_time = 0
        self.max_time = 100  # можно задать максимальное время моделирования

    def print_status(self):
        print("=" * 50)
        print(f"Время моделирования: {self.model_time}")
        print(f"Расчетный счет: {self.account}")
        print(f"Склад магазина: {self.shop_inventory}")
        print(f"Основной склад: {self.basic_inventory}")
        print(f"Промежуточный склад (in_transit): {self.in_transit}")
        print("Параметры оптового предложения:")
        print(f"  Объем партии: {self.wholesale_offer_volume}")
        print(f"  Цена партии: {self.wholesale_offer_price}")
        print(f"  Цена за единицу: {self.unit_price_wholesale}")
        print("Параметры розничной торговли:")
        print(f"  Розничная цена: {self.retail_price}")
        print(f"  Текущий спрос: {self.current_demand}")
        print("=" * 50)

    def update_parameters(self):
        # Перед каждым шагом моделирования предлагаем пользователю ввести данные,
        # предварительно показывая текущие параметры.
        print("Введите новые параметры для следующего шага моделирования (оставьте пустым для сохранения текущего значения):")
        try:
            new_account = input(f"Расчетный счет [{self.account}]: ")
            if new_account.strip() != "":
                self.account = float(new_account)
        except Exception:
            print("Неверный ввод, используется предыдущее значение.")
        
        try:
            new_shop_inventory = input(f"Склад магазина [{self.shop_inventory}]: ")
            if new_shop_inventory.strip() != "":
                self.shop_inventory = int(new_shop_inventory)
        except Exception:
            print("Неверный ввод, используется предыдущее значение.")
        
        try:
            new_basic_inventory = input(f"Основной склад [{self.basic_inventory}]: ")
            if new_basic_inventory.strip() != "":
                self.basic_inventory = int(new_basic_inventory)
        except Exception:
            print("Неверный ввод, используется предыдущее значение.")
        
        try:
            new_wholesale_volume = input(f"Оптовое предложение, объем [{self.wholesale_offer_volume}]: ")
            if new_wholesale_volume.strip() != "":
                self.wholesale_offer_volume = int(new_wholesale_volume)
        except Exception:
            print("Неверный ввод, используется предыдущее значение.")
        
        try:
            new_wholesale_price = input(f"Оптовое предложение, цена партии [{self.wholesale_offer_price}]: ")
            if new_wholesale_price.strip() != "":
                self.wholesale_offer_price = float(new_wholesale_price)
        except Exception:
            print("Неверный ввод, используется предыдущее значение.")
        
        try:
            new_unit_price = input(f"Оптовое предложение, цена за единицу [{self.unit_price_wholesale}]: ")
            if new_unit_price.strip() != "":
                self.unit_price_wholesale = float(new_unit_price)
        except Exception:
            print("Неверный ввод, используется предыдущее значение.")
        
        try:
            new_retail_price = input(f"Розничная цена [{self.retail_price}]: ")
            if new_retail_price.strip() != "":
                self.retail_price = float(new_retail_price)
        except Exception:
            print("Неверный ввод, используется предыдущее значение.")
        
        try:
            new_demand = input(f"Текущий спрос [{self.current_demand}]: ")
            if new_demand.strip() != "":
                self.current_demand = int(new_demand)
        except Exception:
            print("Неверный ввод, используется предыдущее значение.")

    def simulate_step(self):
        # 1. Оптовое предложение: магазин принимает или отклоняет предложение
        print("\nЭтап 1: Оптовое предложение")
        decision = input("Принять оптовое предложение? (да/нет): ").lower()
        if decision == "да":
            cost = self.wholesale_offer_price
            if self.account >= cost:
                self.account -= cost
                # При покупке товары направляются сразу на промежуточный склад
                self.in_transit += self.wholesale_offer_volume
                # Если на основном складе есть достаточное количество товара для комплектации закупки,
                # уменьшаем его. Иначе выводим предупреждение.
                if self.basic_inventory >= self.wholesale_offer_volume:
                    self.basic_inventory -= self.wholesale_offer_volume
                else:
                    print("Внимание: недостаточно товара на основном складе для формирования оптового предложения!")
                print("Оптовое предложение принято. Товары направлены на промежуточный склад (in_transit).")
            else:
                print("Недостаточно средств для закупки товара.")
        else:
            print("Оптовое предложение отклонено.")

        # 2. Логистика: Перевод товаров с основного склада в промежуточный склад (in_transit)
        print("\nЭтап 2: Логистика (перемещение товаров в in_transit)")
        transfer_input = input("Введите количество товаров для перевода с основного склада на in_transit (0 для пропуска): ")
        try:
            transfer_qty = int(transfer_input)
        except ValueError:
            transfer_qty = 0
        if transfer_qty > 0:
            if self.basic_inventory >= transfer_qty:
                self.basic_inventory -= transfer_qty
                self.in_transit += transfer_qty
                print(f"Перемещено {transfer_qty} единиц товара на промежуточный склад (in_transit).")
            else:
                print("Недостаточно товара на основном складе для перевода.")
        else:
            print("Перемещение не осуществлено.")

        # 3. Прием товара из промежуточного склада (in_transit) на склад магазина
        print("\nЭтап 3: Прием товара из in_transit")
        receive_input = input("Введите количество товаров для поступления из in_transit на склад магазина (0 для пропуска): ")
        try:
            receive_qty = int(receive_input)
        except ValueError:
            receive_qty = 0
        if receive_qty > 0:
            if self.in_transit >= receive_qty:
                self.in_transit -= receive_qty
                self.shop_inventory += receive_qty
                print(f"Принято {receive_qty} единиц товара на склад магазина.")
            else:
                print("Недостаточно товара на промежуточном складе для приема.")
        else:
            print("Прием товара не осуществлен.")

        # 4. Розничная торговля: продажи магазина
        print("\nЭтап 4: Розничная торговля")
        sold_units = min(self.shop_inventory, self.current_demand)
        revenue = sold_units * self.retail_price
        self.account += revenue
        self.shop_inventory -= sold_units
        print(f"Продано {sold_units} единиц по цене {self.retail_price} за единицу. Доход: {revenue}.")

        # 5. Случайные изменения: симуляция колебаний спроса
        print("\nЭтап 5: Случайные события")
        random_change = random.uniform(-5, 5)
        self.current_demand = max(0, int(self.current_demand + random_change))
        print(f"Спрос изменился на {random_change:.2f}. Новый спрос: {self.current_demand}.")

        # Увеличиваем модельное время
        self.model_time += 1
        print("\nШаг моделирования завершён.\n")

def main():
    simulation = StoreSimulation()
    try:
        total_steps = int(input("Введите количество шагов моделирования: "))
    except ValueError:
        total_steps = 10  # значение по умолчанию
    for step in range(total_steps):
        print(f"\n=== Шаг {step + 1} из {total_steps} ===")
        simulation.print_status()
        simulation.update_parameters()
        simulation.simulate_step()
    print("Моделирование завершено.")

if __name__ == "__main__":
    main()
