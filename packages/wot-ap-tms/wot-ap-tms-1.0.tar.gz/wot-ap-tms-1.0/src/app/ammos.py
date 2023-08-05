from lesson_9.app.guns import Gun


class Ammo:
    """Создаёт снаряды для пушки танка.
    Принимает 2 аргумента: объект класса Gun и тип снаряда.
    Имеет 2 метода: get_damage (расчёт урона от попадания)
    и get_penetration (возвращает силу пробития брони).
    """

    def __init__(self, gun: Gun, type: str):
        """
        Устанавливает необходимые атрибуты для объекта ammo.
        ______________________
        Принимаемые атрибуты:
        gun (объект пушки): Gun
        type (тип снаряда): str
        """

        self.gun = gun
        self.type = type
        self.penetration_power = 0

    def get_damage(self, gun: Gun):
        """
        Рассчитывает урон, наносимый вражескому танку.
        ______________________
        Принимаемые атрибуты:
        caliber (калибр): int
        """

        return gun.caliber * 3

    def get_penetration(self):
        """Возвращает силу пробития брони, равную
        калибру пушки танка."""

        return self.gun.caliber


class HECartridge(Ammo):
    """Создаёт фугасный снаряд."""

    def __init__(self, gun: Gun):
        super().__init__(gun, type='фугасный')


class HEATCartridge(Ammo):
    """Создаёт кумулятивный снаряд."""

    def __init__(self, gun: Gun):
        super().__init__(gun, type='кумулятивный')

    def get_damage(self, gun: Gun):
        """Переопределяет метод родительского класса Ammo,
        умножая урон на коэффициент 0.6."""

        return super().get_damage(gun) * 0.6


class APCartridge(Ammo):
    """Создаёт подкалиберный снаряд."""

    def __init__(self, gun):
        super().__init__(gun, type='подкалиберный')

    def get_damage(self, gun: Gun):
        """Переопределяет метод родительского класса Ammo,
        умножая урон на коэффициент 0.3."""

        return super().get_damage(gun) * 0.3
