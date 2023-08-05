import random


class Dice:
    """Создаёт кубик для игры."""

    def __init__(self):
        self.result = None

    def throw(self):
        """Возвращает случайное int число от 1 до 6."""

        self.result = random.randrange(1, 7)
        return self.result


class Gun:
    """
    Создаёт пушку для танка.
    Принимает 2 аргумента: калибр и длина пушки.
    Имеет 1 метод is_on_target (фиксирует попадание в чужой танк).
    """

    def __init__(self, caliber: int, length: int):
        """
        Устанавливает необходимые атрибуты для объекта gun.
        ______________________
        Принимаемые атрибуты:
        caliber (калибр): int
        gun_length (длина пушки): int
        """

        if caliber < 0 or length < 0:
            raise Exception('gun caliber and length can\'t be less than 0!')

        self.caliber = caliber
        self.length = length

    def is_on_target(self, dice: Dice):
        """
        Вычисляет по формуле, было ли попадание в чужой танк.
        Возвращает значение True или False.
        ______________________
        Принимаемые атрибуты:
        dice (бросок кубика): int
        """

        return self.length * dice.throw() > 100
