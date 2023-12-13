from src.config import *

class Attack:
    def __init__(self,race:str):
        self.name = RACES[race]['attack']['name']
        self.nature = RACES[race]['attack']['nature']
        pass