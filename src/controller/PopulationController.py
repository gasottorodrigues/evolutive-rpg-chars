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

            avg_dmg_caused = CharacterManipulator.simulate_attack(ind,player)
            avg_dmg_suffered = CharacterManipulator.simulate_attack(player,ind)
            attr_balance = CharacterManipulator.balance(ind)

            coefs = list(SIMULATION_PARAMS["eval_coefs"].values())
            ind.eval = (coefs[0]*avg_dmg_caused + coefs[1]*(100-avg_dmg_suffered) + coefs[2]*ind.hp + coefs[3]*ind.agility + coefs[4]*attr_balance)/((sum(coefs)))
            self.population[idx].eval = ind.eval

            self.logger.debug(f'Evaluating character {idx + 1} - Race:{ind.race}, Eval: {ind.eval}')
        
        self.logger.info(f'Ordenating evaluation')
        self.population = sorted(self.population, key=lambda ind: ind.eval)

        for ind in self.population:
             self.logger.debug(f'character - Race:{ind.race}, Eval: {ind.eval}')
        return
    
    def new_generation(self,n_breeders):
        breeders = self.population[len(self.population)-n_breeders-1:len(self.population)]
        self.population = [self.population[-1]]
        
        for i in range(1,self.pop_size):
            self.logger.debug(f'Reproduction {i}')
            mother = random.choice(breeders)
            father = random.choice(breeders)
            self.logger.debug(f'Mother: {mother.race} - {mother.eval}')
            self.logger.debug(f'Father: {father.race} - {father.eval}')
            son = CharacterManipulator.reproduce(mother,father,self.base_points)
            son = CharacterManipulator.mutate(son)
            self.logger.debug(f'Generated character {i + 1} - Race: {son.race}, Points: {son.get_total_points()}')
            self.population.append(son)
        
        self.logger.info(f'Population Size: {len(self.population)}.')
        return


    def get_max_eval(self):
        return self.population[-1].eval
    
    def get_avg_eval(self):
        acc = 0
        for ind in self.population:
            acc += ind.eval

        return acc/len(self.population)
    
    