class DepositCalculator:
    """Расчёт итоговой суммы вклада с учётом сложных процентов."""

    def __init__(self, first=1000.0, second=5.0, years=1):
        self.first = first
        self.second = second
        self.years = years

    @property
    def first(self):
        """Начальная сумма вклада."""
        return self.__first

    @first.setter
    def first(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Начальная сумма вклада должна быть положительной.")
        self.__first = value

    @property
    def second(self):
        """Годовая процентная ставка в процентах."""
        return self.__second

    @second.setter
    def second(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Процентная ставка должна быть положительной.")
        self.__second = value

    @property
    def years(self):
        """Срок вклада в годах."""
        return self.__years

    @years.setter
    def years(self, value):
        value = int(value)
        if value <= 0:
            raise ValueError("Срок вклада должен быть положительным целым числом.")
        self.__years = value

    def read(self):
        """Ввод данных с клавиатуры с обработкой ошибок."""
        while True:
            try:
                self.first = float(input("Введите начальную сумму вклада: "))
                self.second = float(input("Введите годовую процентную ставку (%): "))
                self.years = int(input("Введите срок вклада в полных годах: "))
                break
            except ValueError as error:
                print(f"Ошибка ввода: {error}")
                print("Повторите ввод всех значений.")

    def display(self):
        """Вывод введённых данных."""
        print(f"Начальная сумма вклада: {self.first:.2f}")
        print(f"Годовая процентная ставка: {self.second:.2f}%")
        print(f"Срок вклада: {self.years} год(лет)")

    def final_amount(self):
        """Итоговая сумма при ежегодной капитализации процентов."""
        return self.first * (1 + self.second / 100) ** self.years

    def profit(self):
        """Чистая прибыль без учёта налогов и комиссий."""
        return self.final_amount() - self.first


def main():
    calculator = DepositCalculator()
    calculator.read()
    calculator.display()

    try:
        print(f"Итоговая сумма вклада: {calculator.final_amount():.2f}")
        print(f"Прибыль: {calculator.profit():.2f}")
    except (ValueError, ZeroDivisionError) as error:
        print(f"Не удалось выполнить расчёт: {error}")


if __name__ == "__main__":
    main()
