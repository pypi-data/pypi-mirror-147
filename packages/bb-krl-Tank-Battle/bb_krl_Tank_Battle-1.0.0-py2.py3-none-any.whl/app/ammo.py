import gun


class Ammo(object):
    """class Ammo - материнский класс для классов-наследников снарядов
    Класс Ammo имеет следующие поля:
        -gun(каждый снаряд делается под конкретную пушку,
    так что здесь стоит применить агрегацию)
        -type (фугасный, кумулятивный, подкалиберный)
    """

    def __init__(self, gun: gun, shell_type: str):
        self.gun = gun
        self.shell_type = shell_type

    def get_damage(self):
        """метод возвращает калибр пушки, умноженный на 3"""

        return self.gun.caliber * 3

    def get_penetration(self):
        """снаряд может пробить броню, равную по толщине своему калибру
        метод возвращает калибр пушки"""
        return self.gun.caliber


class HECartridge(Ammo):
    """класс фугасных снарядов.
    метод get_damage никак не изменяется"""

    def __init__(self, gun: gun.Gun):
        super().__init__(gun, 'фугасный')


class HEATCartridge(Ammo):
    """класс кумулятивный снаряд"""

    def __init__(self, gun: gun.Gun):
        super().__init__(gun, 'кумулятивный')

    def get_damage(self):
        return super().get_damage() * 0.6


class APCartridge(Ammo):
    """класс подкалиберного снаряда"""

    def __init__(self, gun: gun.Gun):
        super().__init__(gun, 'подкалиберный')

    def get_damage(self):
        return super().get_damage() * 0.3
