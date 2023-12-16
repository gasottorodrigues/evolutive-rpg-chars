from src.models.Character import Character
from src.config import *

import random

class CharacterManipulator:
    @staticmethod
    def generateChar(race,points):
        genetics = RACES[race]['genes']
        attrs = SIMULATION_PARAMS['attrs'].copy()

        keys = list(genetics.keys())
        prob = list(genetics.values())
        points_dist = random.choices(keys,weights=prob,k=points)

        for p in points_dist:
            attrs[p] += 1
        
        char  = Character(race,
                          attrs['hp'],
                          attrs['atk'],
                          attrs['magic'],
                          attrs['armor'],
                          attrs['magic_def'],
                          attrs['agility'])
        return char

    @staticmethod
    def simulate_attack(attacker:Character,defender:Character):
        if(attacker.attack.nature == 'physical'):
            return attacker.atk - ((defender.armor)/(defender.armor + 100))*attacker.atk
        
        return attacker.magic - ((defender.magic_def)/(defender.magic_def + 100))*attacker.magic
    
    @staticmethod
    def reproduce(mother,father,points):
        race = random.choice([mother.race,father.race])
        attrs = SIMULATION_PARAMS['attrs'].copy()
        attrs['hp'] = int((mother.hp+father.hp)/2)
        attrs['atk'] = int((mother.atk+father.atk)/2)
        attrs['magic'] = int((mother.magic+father.magic)/2)
        attrs['armor'] = int((mother.armor+father.armor)/2)
        attrs['magic_def'] = int((mother.magic_def+father.magic_def)/2)
        attrs['agility'] = int((mother.agility+father.agility)/2)

        extra_points = max(points - sum(list(attrs.values())),0)

        if(extra_points > 0):
            genetics = RACES[race]['genes']
            keys = list(genetics.keys())
            prob = list(genetics.values())
            points_dist = random.choices(keys,weights=prob,k=extra_points)

            for p in points_dist:
                attrs[p] += 1

        son = Character(race,attrs['hp'],attrs['atk'],attrs['magic'],attrs['armor'],attrs['magic_def'],attrs['agility'])
        return son
    
    @staticmethod
    def mutate(ind):
        mutations = SIMULATION_PARAMS['mutation']['mutation_per_ind']
        agressiveness = SIMULATION_PARAMS['mutation']['mutation_aggr']
        attrs = ind.attrs()
        attrs_list = list(attrs.keys())

        while(mutations > 0):
            receiver = random.choice(attrs_list)
            donor = random.choice(attrs_list)

            if(attrs[donor] > agressiveness+1) and (attrs[receiver] + agressiveness <= 100):
                attrs[donor] = attrs[donor] - agressiveness
                attrs[receiver] = attrs[receiver] + agressiveness
                mutations -= 1

        ind.set_attrs(attrs)
        return ind
        