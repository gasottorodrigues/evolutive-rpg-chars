import logging
from src.config import *
from src.controller.CharacterManipulator import CharacterManipulator
from src.controller.PopulationController import PopulationController
import matplotlib.pyplot as plt

def plot(evaluation,player):
    # Listas de dados
    xticks = [range(len(evaluation))]
    max_values = []
    avg_values = []

    # Lista para armazenar atributos dos objetos em 'breeders'
    breeders_attributes = []

    for idx, cur in enumerate(evaluation):
        max_values.append(cur['max'])
        avg_values.append(cur['avg'])
        breeders_attributes.append(cur['breeders'][0].attrs())
        breeders_attributes[idx]['race'] = cur['breeders'][0].race

    plt.figure(figsize=(10, 6))

    attrs = player.attrs()
    plt.text(len(evaluation) -1, min(avg_values), f'Player ( {player.race} ) \n HP: {attrs['hp']} | ATK: {attrs['atk']}\n MGC: {attrs['magic']} | ARM: {attrs['armor']}\n MR: {attrs['magic_def']} | SPD: {attrs['agility']}\n', fontsize=10, ha='center', va='bottom')

    # Plotagem dos dados
    plt.plot(range(len(evaluation)), max_values, label='Melhor de Todos')
    plt.plot(range(len(evaluation)), avg_values, label='Média da Geração')

    # Adicionando rótulos e título ao gráfico
    plt.xlabel('Geração')
    plt.ylabel('Avaliação')
    plt.title('Resultados por Gerações')

    for i, attrs in enumerate(breeders_attributes):
        plt.text(i, max_values[i], f'{attrs['race']}\n HP: {attrs['hp']} | ATK: {attrs['atk']}\n MGC: {attrs['magic']} | ARM: {attrs['armor']}\n MGC_DEF: {attrs['magic_def']} | SPD: {attrs['agility']}\n', fontsize=8, ha='center', va='bottom')

    
    # Configurando a legenda e exibindo o gráfico
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    logging.basicConfig(format='[%(name)s - %(levelname)s]: %(message)s', level=logging.INFO)

    pop_size = SIMULATION_PARAMS['population_size']
    max_gen = SIMULATION_PARAMS['max_generations']
    player_points = SIMULATION_PARAMS['player_base_points']
    player_race = SIMULATION_PARAMS['player_base_race']
    num_breeders = SIMULATION_PARAMS['breeders']

    logging.info(f'Start Evolutional Char Generation.')
    logging.info(f'Population Size: {pop_size}')
    logging.info(f'Max Generations: {max_gen}\n')



    logging.info(f'Player Inital Points: {player_points}\n')
    logging.info(f'Player Race: {player_race}\n')
    logging.info(f'Generating Player...')

    player = CharacterManipulator.generateChar(player_race,player_points)
    player.log()

    logging.info(f'Generating First Population...')
    pop_ctrl = PopulationController(pop_size,player_points)
    pop_ctrl.generate_population()

    evaluation = []

    for i in range(1,max_gen+1):
        logging.info(f'Generation {i}:')

        logging.info(f'Evaluating Population...')
        pop_ctrl.evaluate_population(player)
        logging.info(f'Max evaluation: {pop_ctrl.get_max_eval()}')
        evaluation.append({
            "max":pop_ctrl.get_max_eval(),
            "avg":pop_ctrl.get_avg_eval(),
            "breeders":pop_ctrl.population[-3:-1]
            })
        print()
        
        pop_ctrl.new_generation(num_breeders)
    
    plot(evaluation,player)
        

