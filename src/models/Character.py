import logging
from src.config import *
from src.models.Attack import Attack

class Character:
    def __init__(self,race:str,base_hp:int,base_atk:int,base_magic:int,base_armor:int,base_mg_def:int,base_spd:int):
            self.race = race.lower()
            self.hp = base_hp 
            self.curr_hp = base_hp
            self.atk = base_atk
            self.magic = base_magic
            self.armor = base_armor
            self.magic_def = base_mg_def
            self.agility = base_spd
            self.eval = -1

            self.attack = Attack(self.race)

            self.logger = logging.getLogger(__name__)  # Inicializa o logger
            self.logger.setLevel(logging.INFO)  # Define o nível do logger

            return
    def attrs(self):
         return {
            "hp":self.hp,
            "atk":self.atk,
            "magic":self.magic,
            "armor":self.armor,
            "magic_def":self.magic_def,
            "agility":self.agility,
         }
    
    def json(self):
         return {
            "race":self.race,
            "hp":self.hp,
            "atk":self.atk,
            "magic":self.magic,
            "armor":self.armor,
            "magic_def":self.magic_def,
            "agility":self.agility,
         }
    
    def set_attrs(self,attrs:dict):
         self.hp = attrs['hp']
         self.atk= attrs['atk']
         self.magic = attrs['magic']
         self.armor = attrs['armor']
         self.magic_def = attrs['magic_def']
         self.agility = attrs['agility']
         return 

    def get_total_points(self):
        return self.hp + self.atk + self.magic + self.armor + self.magic_def + self.agility

    def log(self):
        self.logger.info(f"RACE:{self.race} (POINTS:{self.get_total_points()})")
        self.logger.info(f"HP:{self.hp} | ATK:{self.atk}")
        self.logger.info(f"MAG:{self.magic} | ARMOR:{self.armor}") 
        self.logger.info(f"MDEF:{self.magic_def} | AGI: {self.agility} \n")