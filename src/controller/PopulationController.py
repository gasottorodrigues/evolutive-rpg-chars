import logging

from src.config import *
from src.controller.CharacterManipulator import CharacterManipulator

import random 

class PopulationController:
    def __init__(self,pop_size,base_points) -> None:
        self.pop_size = pop_size
        self.base_points = base_points
        self.population = []

        self.logger = logging.getLogger(__name__)  # Inicializa o logger
        return

    def generate_population(self):
        for i in range(0,self.pop_size):
            races = list(RACES.keys())
            selected_race = random.choice(races)
            new_char = CharacterManipulator.generateChar(selected_race,self.base_points)
            
            self.logger.debug(f'Generated character {i + 1} - Race: {new_char.race}, Points: {new_char.get_total_points()}')
            self.population.append(new_char)

        self.logger.info(f'Population Size: {len(self.population)}.')
        return
    
    def evaluate_population(self, player):
        for idx,ind in enumerate(self.population):
            if(ind.eval != -1):
                continue

            genes = RACES[ind.race]['genes']
            k = SIMULATION_PARAMS['eval_coefs']
            hp_diff = abs(player.hp - ind.hp)
            avg_dmg_caused = CharacterManipulator.simulate_attack(ind,player)
            avg_dmg_suffered = CharacterManipulator.simulate_attack(player,ind)
            agility_diff = abs(player.agility - ind.agility)

            hp_param = (hp_diff*genes['hp'])/(ind.hp/player.hp)
            dmg_param = avg_dmg_caused*(genes['atk']+genes['magic'])
            def_param = (100-avg_dmg_suffered)*(genes['armor'] + genes['magic_def'])
            agility_param = (agility_diff*genes['agility'])/(ind.agility/player.agility)

            ind.eval = ((hp_param*k['hp'])+(dmg_param*k['dmg'])+(def_param*k['def'])+(agility_param*k['agility']))/100.0
            self.population[idx].eval = ind.eval
            self.logger.debug(f'Evaluating character {idx + 1} - Race:{ind.race}, Eval: {ind.eval}')
        
        self.logger.info(f'Ordenating evaluation')
        self.population = sorted(self.population, key=lambda ind: ind.eval)

        for ind in self.population:
             self.logger.debug(f'character - Race:{ind.race}, Eval: {ind.eval}')
        return
    
    def new_generation(self,n_breeders):
        breeders = self.population[len(self.population)-n_breeders-1:len(self.population)]
        others = self.population[0:len(self.population)-n_breeders-1]
        new_pop = [self.population[-1]]
        for i in range(1,self.pop_size):
            self.logger.debug(f'Reproduction {i}')
            mother = random.choice(breeders)
            father = random.choice(others)
            self.logger.debug(f'Mother: {mother.race} - {mother.eval}')
            self.logger.debug(f'Father: {father.race} - {father.eval}')
            son = CharacterManipulator.reproduce(mother,father,self.base_points)
            son = CharacterManipulator.mutate(son)
            self.logger.debug(f'Generated character {i + 1} - Race: {son.race}, Points: {son.get_total_points()}')
            new_pop.append(son)
        
        self.logger.info(f'Population Size: {len(new_pop)}.')
        self.population = new_pop.copy()
        return
    
    def get_races_count(self):
        orcs = sum(1 for ind in self.population if ind.race == 'orc')
        elfs = sum(1 for ind in self.population if ind.race == 'elf')
        humans = sum(1 for ind in self.population if ind.race == 'human')
        dwarfs = sum(1 for ind in self.population if ind.race == 'dwarf')
        vamps = sum(1 for ind in self.population if ind.race == 'vamp')
        return orcs, elfs, humans, dwarfs, vamps
    
    def get_eval_list(self):
        return [i.eval for i in self.population]
    def get_max_eval(self):
        return self.population[-1].eval
    
    def get_avg_eval(self):
        acc = 0
        for ind in self.population:
            acc += ind.eval

        return acc/len(self.population)
    
    