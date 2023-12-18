from src.models.Character import Character
from src.config import *

import random

# Character manipulator class operates on characters either by creating, simulating fights, reproducing, and mutating them

class CharacterManipulator:

    # Generates a char based on the genetic charge of the race
    @staticmethod
    def generateChar(race,points):
        # Gets the race genes
        genetics = RACES[race]['genes']
        attrs = SIMULATION_PARAMS['attrs'].copy()

        attrs['hp'] = 1
        attrs['atk'] = 1
        attrs['armor'] = 1
        attrs['magic'] = 1
        attrs['magic_def'] = 1
        attrs['agility'] = 1

        # Distributes the points based on the genetic probability of each attribute
        keys = list(genetics.keys())
        prob = list(genetics.values())
        points_dist = random.choices(keys,weights=prob,k=(points-6))

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

    # Simulates a fight to understand how much damage a char would inflict in another
    @staticmethod
    def simulate_attack(attacker:Character,defender:Character):
        if(attacker.attack.nature == 'physical'):
            return attacker.atk - ((defender.armor)/(defender.armor + 100))*attacker.atk   # damage reduced by armor
        
        return attacker.magic - ((defender.magic_def)/(defender.magic_def + 100))*attacker.magic # damage reducted by magic resistance
    

    # Breeds individuals of a generation
    @staticmethod
    def reproduce(mother,father,points):
        # race is chosen by random from the parents
        race = random.choice([mother.race,father.race])

        # new-born receives the arithmetics average of the parents attributes
        attrs = SIMULATION_PARAMS['attrs'].copy()
        attrs['hp'] = int((mother.hp+father.hp)/2)
        attrs['atk'] = int((mother.atk+father.atk)/2)
        attrs['magic'] = int((mother.magic+father.magic)/2)
        attrs['armor'] = int((mother.armor+father.armor)/2)
        attrs['magic_def'] = int((mother.magic_def+father.magic_def)/2)
        attrs['agility'] = int((mother.agility+father.agility)/2)

        # in case the average float-to-int approximation ends up distributing less points then the difficulty determinates, the diffence is distributed based on the race
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

    # Mutates a individual
    @staticmethod
    def mutate(ind):
        # Each time a mutation occurs, it is based on two parameters
        # Num of mutations
        # Agressiveness -> mutations is based on taking points from a individual (donor) and giving them to another (receiver); agressiveness determinates how many points will be donated
        mutations = SIMULATION_PARAMS['mutation']['mutation_per_ind']
        agressiveness = SIMULATION_PARAMS['mutation']['mutation_aggr']
        attrs = ind.attrs()
        attrs_list = list(attrs.keys())

        # Donates a num of "agressiveness" points to another char, while there are still mutations left
        while(mutations > 0):
            receiver = random.choice(attrs_list)
            donor = random.choice(attrs_list)

            if(attrs[donor] >= agressiveness+1) and (attrs[receiver] + agressiveness <= 100):
                attrs[donor] = attrs[donor] - agressiveness
                attrs[receiver] = attrs[receiver] + agressiveness
                mutations -= 1

        ind.set_attrs(attrs)
        return ind
        
