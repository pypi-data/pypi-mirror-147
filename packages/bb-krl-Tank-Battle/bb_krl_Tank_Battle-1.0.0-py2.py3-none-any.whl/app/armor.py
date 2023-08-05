import ammo


class Armor:
    """thickness (толщина брони)
     type(тип брони)
     """

    def __init__(self, thickness: int, thickness_type: str):
        self.thickness = thickness
        self.type = thickness_type

    def is_penetrated(self, ammo: ammo):
        return True if getattr(ammo.gun, 'caliber') > self.thickness else False


class HArmour(Armor):
    ammo_type_coeff = {
        'фугасный': 1.2,
        'подкалиберный': 1,
        'кумулятивный': 0.7
    }

    def __init__(self, thickness: int):
        super().__init__(thickness, 'гомогенная')

    def is_penetrated(self, ammo: ammo):
        return True if getattr(ammo.gun, 'caliber') > self.thickness * \
                       self.ammo_type_coeff[getattr(ammo, 'shell_type')] else False


class SArmour(Armor):
    """ стальная"""

    ammo_type_coeff = {
        'фугасный': 0.6,
        'подкалиберный': 1.2,
        'кумулятивный': 1.5
    }

    def __init__(self, thickness: int):
        super().__init__(thickness, 'стальная')

    def is_penetrated(self, ammo: ammo):
        return True if getattr(ammo.gun, 'caliber') > self.thickness * \
                       self.ammo_type_coeff[getattr(ammo, 'shell_type')] else False


class CArmour(Armor):
    """керамическая"""

    ammo_type_coeff = {
        'фугасный': 0.6,
        'подкалиберный': 1.2,
        'кумулятивный': 1.5
    }

    def __init__(self, thickness: int):
        super().__init__(thickness, 'керамическая')

    def is_penetrated(self, ammo: ammo):
        return True if getattr(ammo.gun, 'caliber') > self.thickness * \
                       self.ammo_type_coeff[getattr(ammo, 'shell_type')] else False

