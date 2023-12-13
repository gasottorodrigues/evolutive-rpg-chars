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
        hp = int((mother.hp+father.hp)/2)
        atk = int((mother.atk+father.atk)/2)
        magic = int((mother.magic+father.magic)/2)
        armor = int((mother.armor+father.armor)/2)
        magic_def = int((mother.magic_def+father.magic_def)/2)
        agility = int((mother.agility+father.agility)/2)

        son = Character(race,hp,atk,magic,armor,magic_def,agility)
        extra_points = points - son.get_total_points() 

        genetics = RACES[son.race]['genes']
        attrs = son.attrs()

        keys = list(genetics.keys())
        prob = list(genetics.values())
        points_dist = random.choices(keys,weights=prob,k=extra_points)

        for p in points_dist:
            attrs[p] += 1

        son.set_attrs(attrs)
        return son
    
    @staticmethod
    def mutate(ind):
        mutations = SIMULATION_PARAMS['mutation']['mutation_per_ind']
        agressiveness = SIMULATION_PARAMS['mutation']['mutation_aggr']
        attrs = ind.attrs()
        attrs_list = list(attrs.keys())

        for i in range(0,mutations):
            receiver = random.choices(attrs_list,weights=list(map(lambda x: 100/(1+attrs[x]),attrs_list)),k=1)[0]
            donor = random.choices(attrs_list,weights=list(map(lambda x: attrs[x],attrs_list)),k=1)[0]

            if (attrs[donor] - agressiveness >= 1):
                attrs[donor] -= agressiveness
                attrs[receiver] += agressiveness
            else:
                attrs[receiver] += attrs[donor]
                attrs[donor] = 1

        ind.set_attrs(attrs)
        return ind

    @staticmethod
    def balance(ind):
        attr_dist = list(ind.attrs().values())

        return 1/(max(attr_dist) - min(attr_dist))
        