import random
from copy import copy


class Gun:
    def __init__(self, calibеr: int, barrel_lenght: int, dice: int) -> None:
        self.caliber = calibеr
        self.barrel_lenght = barrel_lenght
        self.dice = dice
    
    def is_on_target(self) -> bool:
        self.dice = random.randint(1, 6)
        return self.dice * self.barrel_lenght > 100


class Ammo:
    def __init__(self, gun: Gun, ammo_type: str) -> None:
        self.gun = gun
        self.ammo_type = ammo_type

    def get_damage(self):
        return self.gun.caliber * 3

    def get_penetration(self):
        return self.gun.caliber


class HECartidge(Ammo):
    def __init__(self, gun: Gun) -> None:
        super().__init__(gun, 'фугасный')
    

class HEATCartridge(Ammo):
    def __init__(self, gun: Gun) -> None:
        super().__init__(gun, 'кумулятивный')

    def get_damage(self):
        return super().get_damage() * 0.6


class APCartridge(Ammo):
    def __init__(self, gun: Gun) -> None:
        super().__init__(gun, 'подкалиберный')
        
    def get_damage(self):
        return super().get_damage() * 0.3


class Armour:
    def __init__(self, thickness: int, armour_type: str) -> None:
        self.thickness = thickness
        self.armour_type = armour_type

    def is_penetrated(self, ammo: Ammo) -> bool:
        return ammo.get_penetration() > self.thickness


class HArmour(Armour):
    def __init__(self, thickness: int) -> None:
        super().__init__(thickness, 'гомогенная')

    def is_penetrated(self, ammo: Ammo) -> bool:
        if ammo is HECartidge:
            ammo_fact = 1.2
        elif ammo is HEATCartridge:
            ammo_fact = 1
        else:
            ammo_fact = 0.7

        return ammo.get_penetration() > self.thickness * ammo_fact


class SArmour(Armour):
    def __init__(self, thickness: int) -> None:
        super().__init__(thickness, 'стальная')

    def is_penetrated(self, ammo: Ammo) -> bool:
        if ammo is HECartidge:
            ammo_fact = 1.1
        elif ammo is HEATCartridge:
            ammo_fact = 0.9
        else:
            ammo_fact = 0.5

        return ammo.get_penetration() > self.thickness * ammo_fact
        

class CArmour(Armour):
    def __init__(self, thickness: int) -> None:
        super().__init__(thickness, 'керамическая')

    def is_penetrated(self, ammo: Ammo) -> bool:
        if ammo is HECartidge:
            ammo_fact = 1.4
        elif ammo is HEATCartridge:
            ammo_fact = 1.2
        else:
            ammo_fact = 0.8

        return ammo.get_penetration() > self.thickness * ammo_fact


class Tank:
    def __init__(
        self, model: str, gun: Gun, armours: list[Armour], ammos: list[Ammo], 
        health: int, _is_gun_loaded: bool = False
        ) -> None:
        self.model = model
        self.gun = gun
        self.armours = armours
        self.ammos = ammos
        self.health = health
        self._is_gun_loaded = _is_gun_loaded

    def _add_armours(self, width: int):
        self.width = width
        self.armours = ['гомогенная', 'стальная', 'керамическая']

    def _load_ammos(self):
        self.ammos = [
            'фугасный', 'фугасный', 'фугасный', 'фугасный', 'фугасный', 
            'фугасный', 'фугасный', 'фугасный', 'фугасный', 'фугасный', 
            'кумулятивный', 'кумулятивный', 'кумулятивный', 'кумулятивный', 'кумулятивный', 
            'кумулятивный', 'кумулятивный', 'кумулятивный', 'кумулятивный', 'кумулятивный', 
            'подкалиберный', 'подкалиберный', 'подкалиберный', 'подкалиберный', 'подкалиберный', 
            'подкалиберный', 'подкалиберный', 'подкалиберный', 'подкалиберный', 'подкалиберный'
            ]

    def select_armour(self, armour_type: str):
        self.armour_type = armour_type

    def load_gun(self, ammo_type: str):
        self.ammo_type = ammo_type
        self.ammos.remove(self.ammo_type)
        self._is_gun_loaded = True
        
    def shoot(self):
        if self._is_gun_loaded:
            fired_ammo = copy(self.ammo_type)
            self._is_gun_loaded = False
            if self.gun.is_on_target():
                print('Попадание')
                return fired_ammo
            else:
                print('Промах')
                return None
        else:
            print('Не заряжено')
            return None


    def handle_hit(self, fired_ammo):
        if self.armour_type.is_penetrated(fired_ammo):
            self.health -= fired_ammo.get_damage()
        else:
            print('Броня не пробита')
