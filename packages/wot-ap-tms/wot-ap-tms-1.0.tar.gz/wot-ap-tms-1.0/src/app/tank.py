from lesson_9.app.guns import Gun, Dice
from lesson_9.app.ammos import Ammo, HECartridge, HEATCartridge, APCartridge
from lesson_9.app.armors import HArmor, SArmor, CArmor


class Tank:
    """Создаёт танк.
         Принимает 4 аргумента: модель танка, его здоровье, объект класса Gun
         и bool-значение того, заряжена ли пушка снарядом.

         Имеет 5 методов:
         _load_ammos (добавляет танку боезапас в 10 снарядов каждого вида)
         select_armor (меняет броню танку в зависимости от выбора пользователя)
         load_gun (заряжает пушку танка выбранным пользователем снарядом)
         shoot (производит выстрел по вражескому танку и сообщает, попал ли снаряд)
         handle_hit (вычисляет, пробита ли броня вражеским снарядом;
            если пробита - уменьшает здоровье танка)
         """

    def __init__(self, model: str, health: int,
                 gun: Gun = Gun(125, 30),
                 _is_gun_loaded: bool = False):
        """
        Устанавливает необходимые атрибуты для объекта tank.
        ______________________
        Принимаемые атрибуты:
            model (модель танка): str
            health (здоровье): int
            gun (пушка): Gun
            _is_gun_loaded (заряжена ли пушка): bool
        """

        self.model = model
        self.gun = gun
        self.armors = [HArmor(200), SArmor(300), CArmor(400)]
        self.ammos = [HECartridge(gun),
                      HEATCartridge(gun), APCartridge(gun)]
        self.health = health
        self._is_gun_loaded = False

        self.current_armor = None
        self.current_ammo = None
        self.fired_ammo = None

    def _load_ammos(self):
        """Добавляет танку боезапас в 10 снарядов каждого вида."""

        self.hecartridge_list = []
        self.heatcartridge_list = []
        self.apcartridge_list = []

        for ammo in self.ammos:
            if ammo.type == 'фугасный':
                self.hecartridge_list = [ammo for _ in range(10)]
            elif ammo.type == 'кумулятивный':
                self.heatcartridge_list = [ammo for _ in range(10)]
            elif ammo.type == 'подкалиберный':
                self.apcartridge_list = [ammo for _ in range(10)]
            else:
                raise Exception('Проверьте тип снаряда!')

        return self.hecartridge_list, self.heatcartridge_list, self.apcartridge_list

    def select_armor(self, armor_type: str):
        """Устанавливает танку броню, выбранную пользователем."""

        if armor_type.lower() == 'гомогенная':
            self.current_armor = self.armors[0]
        elif armor_type.lower() == 'стальная':
            self.current_armor = self.armors[1]
        elif armor_type.lower() == 'керамическая':
            self.current_armor = self.armors[2]
        else:
            raise Exception('Указан неверный тип брони!')

    def load_gun(self, ammo_type: str):
        """Заряжает пушку танка выбранным пользователем снарядом."""
        try:
            if ammo_type.lower() == 'фугасный':
                self.current_ammo = self.hecartridge_list.pop()
            elif ammo_type.lower() == 'кумулятивный':
                self.current_ammo = self.heatcartridge_list.pop()
            elif ammo_type.lower() == 'подкалиберный':
                self.current_ammo = self.apcartridge_list.pop()
            else:
                raise Exception('Указан неверный тип снаряда!')

            self._is_gun_loaded = True

        except IndexError:
            print(f'{ammo_type} снаряд? Таких больше нет!')

    def shoot(self):
        """Производит выстрел по вражескому танку и сообщает, попал ли снаряд."""

        if self._is_gun_loaded:
            self.fired_ammo = self.current_ammo
            self.current_ammo = None

            dice = Dice()

            if self.gun.is_on_target(dice):
                print('Попадание!')
                return self.fired_ammo
            else:
                print('Промах!')

        else:
            print('не заряжено')

        self._is_gun_loaded = False

    def handle_hit(self, fired_ammo: Ammo):
        """Вычисляет, пробита ли броня вражеским снарядом;
            если пробита - уменьшает здоровье танка."""

        if self.current_armor.is_penetrated(fired_ammo):
            self.health -= fired_ammo.get_damage(fired_ammo.gun)
        else:
            print('Броня не пробита.')
