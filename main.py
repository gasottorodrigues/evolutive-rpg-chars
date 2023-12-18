import logging
from src.config import *
from src.controller.CharacterManipulator import CharacterManipulator
from src.controller.PopulationController import PopulationController
from src.controller.InputOutputController import InputOutputController
import matplotlib.pyplot as plt


import random
import json 

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
    plt.text(len(evaluation) -1, min(avg_values), f"Player ( {player.race} ) \n HP: {attrs['hp']} | ATK: {attrs['atk']}\n MGC: {attrs['magic']} | ARM: {attrs['armor']}\n MR: {attrs['magic_def']} | SPD: {attrs['agility']}\n", fontsize=10, ha='center', va='bottom')

    # Plotagem dos dados
    plt.plot(range(len(evaluation)), max_values, label='Melhor de Todos')
    plt.plot(range(len(evaluation)), avg_values, label='Média da Geração')

    # Adicionando rótulos e título ao gráfico
    plt.xlabel('Geração')
    plt.ylabel('Avaliação')
    plt.title('Resultados por Gerações')

    for i, attrs in enumerate(breeders_attributes):
        plt.text(i, max_values[i], f"{attrs['race']}\n HP: {attrs['hp']} | ATK: {attrs['atk']}\n MGC: {attrs['magic']} | ARM: {attrs['armor']}\n MGC_DEF: {attrs['magic_def']} | SPD: {attrs['agility']}\n", fontsize=8, ha='center', va='bottom')

    
    # Configurando a legenda e exibindo o gráfico
    plt.legend()
    plt.tight_layout()
    plt.show()
def plot_gen(ind_list):
    eixo_x = list(range(len(ind_list)))  # Números de 0 a 100 com um intervalo de 5


    # Plotando os pontos
    plt.figure(figsize=(8, 6))
    plt.scatter(eixo_x, ind_list, color='blue')  # Pode personalizar cor, tamanho do ponto, etc.

    # Configurações do gráfico
    plt.title('Avaliação da Geração')
    plt.xlabel('Individuo')
    plt.ylabel('Resultado')

    plt.grid(True)  # Adiciona grade ao gráfico

    plt.show()

if __name__ == "__main__":
    logging.basicConfig(format='[%(name)s - %(levelname)s]: %(message)s', level=logging.INFO)

    # Sets up the simulation parameters based on config.py parameters
    pop_size = SIMULATION_PARAMS['population_size']
    max_gen = SIMULATION_PARAMS['max_generations']
    num_breeders = SIMULATION_PARAMS['breeders']
    limiter = SIMULATION_PARAMS['limiter']

    inout_ctrl = InputOutputController()

    player, total_mobs, rooms_data, n_players = inout_ctrl.get_input(SIMULATION_PARAMS["player_file"],SIMULATION_PARAMS["rooms_file"])

    logging.info(f'Start Evolutional Char Generation.')
    logging.info(f'Population Size: {pop_size}')
    logging.info(f'Max Generations: {max_gen}\n')

    # logging.info(f'Player Inital Points: {player_points}\n')
    # logging.info(f'Player Race: {player_race}\n')
    # logging.info(f'Generating Player...')

    # player = CharacterManipulator.generateChar(player_race,player_points)
    # player.log()

    logging.info(f'Generating First Population...')
    

# Evaluating and generating populations according to preset difficulty
#
# Three groups are generated: an easy, a medium, and a hard ones, from which are selected the individuals

    evaluation = []
    curr_avg = 10
    mobs_arr = []

    # Runs a 3-time loop for each difficulty
    for idx,n_mobs in enumerate(total_mobs):

        # Target parameter is chose por each difficulty
        target = SIMULATION_PARAMS['target_arr'][idx]

        # Number of points for each enemy is chosen based on the difficulty
        # Individuals per popullation is based on the number of mobs to be generated
        pop_ctrl = PopulationController(n_mobs*50,int(player.get_total_points()*(1-(0.1*target))))

        # Number of breeders is based in the number of mobs to be generated
        num_breeders = n_mobs*10

        pop_ctrl.reset()
        gen_id = 1

        # Generates populations until the average is close to the desired value
        #

        # Here is where the evolution occurs
        while (curr_avg >= limiter) &  (gen_id <= max_gen):             # abs(avg - target value) < limiter break condition
            logging.info(f'Generation {gen_id}:')

            logging.info(f'Evaluating Population...')

            # Here is where the population is evaluated, the breeders are chosen and the reproduction occurs
            pop_ctrl.evaluate_population(player,target)

            logging.info(f'Max evaluation: {pop_ctrl.get_max_eval()}') 
            logging.info(f'AVG: {pop_ctrl.get_avg_eval()}')

            # Gets the average evaluation of the generation
            curr_avg = pop_ctrl.get_avg_eval()
            evaluation.append({
                "max":pop_ctrl.get_max_eval(),
                "avg":pop_ctrl.get_avg_eval(),
                "breeders":pop_ctrl.population[-3:-1]
                })
            # plot_gen(pop_ctrl.get_eval_list())
            print(pop_ctrl.get_races_count())
            if curr_avg >= limiter:
                pop_ctrl.new_generation(num_breeders)
                gen_id+=1
            
            # Checks if generation convergency is impossible and resets the evolution process
            if(gen_id == max_gen) & (curr_avg > limiter):
                logging.info(f'Bad Generations. Reseting')
                pop_ctrl.reset()
                gen_id=1

        # Adds the mobs generated for this difficulty, chosen by random
        mobs_arr.append(random.choices(pop_ctrl.population,k=n_mobs))
    
    # Output dictionary to be converted into a json and read by the graphical engine
    # Mobs separeted by room
    output_dict = inout_ctrl.generate_output(rooms_data,mobs_arr,n_players)

    with open(SIMULATION_PARAMS['output_file'],'w') as outfile:
        json.dump(output_dict,outfile)

    print(pop_ctrl.get_races_count())
    plot(evaluation,player)
        

