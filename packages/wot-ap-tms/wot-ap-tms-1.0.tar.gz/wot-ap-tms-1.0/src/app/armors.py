from lesson_9.app.ammos import Ammo


class Armor:
    """Создаёт броню для танка.
     Принимает 2 аргумента: толщину брони и её тип.
     Имеет 1 метод is_penetrated (возвращает bool значение (пробита ли броня)
     по условию: {пробивная способность снаряда} > {толщина брони}.)
     """

    def __init__(self, thickness: int, type: str):
        """
        Устанавливает необходимые атрибуты для объекта armor.
        ______________________
        Принимаемые атрибуты:
        thickness (толщина брони): int
        type (тип брони): str
        """

        if thickness < 0:
            raise Exception('armor thickness can\'t be less than 0!')

        self.thickness = thickness
        self.type = type

    def is_penetrated(self, ammo: Ammo):
        """Возвращает bool значение (пробита ли броня) по условию:
        {пробивная способность снаряда} > {толщина брони}."""

        return ammo.get_penetration() > self.thickness


class HArmor(Armor):
    """Создаёт гомогенную броню."""

    def __init__(self, thickness):
        super().__init__(thickness, type='гомогенная')

    def is_penetrated(self, ammo: Ammo):
        """Возвращает bool значение (пробита ли броня) по условию:
        {пробивная способность снаряда} > {толщина брони} * коэффициент."""

        factors = {'фугасный': 1.2,
                   'кумулятивный': 1.0,
                   'подкалиберный': 0.7}

        return ammo.gun.caliber > self.thickness * factors.get(ammo.type)


class SArmor(Armor):
    """Создаёт стальную броню."""

    def __init__(self, thickness):
        super().__init__(thickness, type='стальная')

    def is_penetrated(self, ammo: Ammo):
        """Возвращает bool значение (пробита ли броня) по условию:
        {пробивная способность снаряда} > {толщина брони} * коэффициент."""

        factors = {'фугасный': 1.0,
                   'кумулятивный': 0.8,
                   'подкалиберный': 0.5}

        return ammo.gun.caliber > self.thickness * factors.get(ammo.type)


class CArmor(Armor):
    """Создаёт керамическую броню."""

    def __init__(self, thickness):
        super().__init__(thickness, type='керамическая')

    def is_penetrated(self, ammo: Ammo):
        """Возвращает bool значение (пробита ли броня) по условию:
        {пробивная способность снаряда} > {толщина брони} * коэффициент."""

        factors = {'фугасный': 0.6,
                   'кумулятивный': 0.5,
                   'подкалиберный': 0.4}

        return ammo.gun.caliber > self.thickness * factors.get(ammo.type)
