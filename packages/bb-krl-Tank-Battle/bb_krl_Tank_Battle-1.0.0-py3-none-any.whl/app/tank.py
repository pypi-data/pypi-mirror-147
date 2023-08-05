from copy import copy
from typing import List, Optional

import copy
from app.gun import Gun
from app.armor import Armor, HArmour, SArmour
from app.ammo import (
    Ammo, HEATCartridge,
    HECartridge, APCartridge)


class Tank:
    def __init__(
            self, model: str, gun: Gun, health: int,
            armors: List[Armor] = None, ammos: List[Ammo] = None,
    ) -> None:
        self.model = model
        self.gun = gun
        self.armors = armors if armors else self._init_armours(30)
        self.ammos = ammos if ammos else self._init_ammos(10)
        self.health = health
        self._selected_armour = armors[0]
        self._loaded_ammo = None

    def _init_armours(self, armour_width: int):
        self.armors = [cls(armour_width) for cls in [HArmour, SArmour]]

    def _init_ammos(self, ammos_count=10):
        for cls in [HEATCartridge, HECartridge, APCartridge]:
            for _ in range(ammos_count):
                self.ammos.append(cls(self.gun))

    def select_armour(self, armour_type: str):
        self._selected_armour = list(
            filter(lambda x: x.armour_type == armour_type, self.armors)
        )[0]

    def load_gun(self, ammo_type: str):
        """заряжает пушку снарядом выбранного типа и уменьшает общее количество снарядов этого типа в боеукладке"""

        searched_ammos = list(
            filter(lambda x: x.ammo_type == ammo_type, self.ammos)
        )

        if searched_ammos:
            self._loaded_ammo = searched_ammos[0]
        else:
            raise Exception(f'{ammo_type} not exist')

    def _remove_loaded_ammo(self):
        self.ammos.remove(self._loaded_ammo)
        self._loaded_ammo = None

    def shoot(self) -> Optional[Ammo]:
        if not self._loaded_ammo:
            raise Exception(f'Gun {self.gun} must be loaded!')

        fired_ammo = copy(self._loaded_ammo)
        self._remove_loaded_ammo()

        is_on_target = self.gun.is_on_target()

        if is_on_target:
            print('Попадание')
            return fired_ammo

    def handle_hit(self, ammo: Ammo):
        if self._selected_armour.is_penetrated(ammo):
            self.health -= ammo.get_demage()
        else:
            print('Броня не пробита!')
