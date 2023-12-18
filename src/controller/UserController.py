from src.config import *
from src.models.Character import Character
import sys
import time

lista_ataques = ["fisico","magico"]
lista_nome_ataques = []


class UserController:
    def __init__(self):
        self.nick = None
        self.race = None
        self.hp = None
        self.atk = None
        self.magic = None
        self.armor = None
        self.magic_def = None
        self.agility = None
        self.typeatack = None

    def styled_print(self,mensagem):
        for char in mensagem:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.01)  # Ajuste este valor para controlar a velocidade de exibição
        print()

    def get_player(self):
        player = Character(self.race,self.hp,self.atk,self.magic,self.armor,self.magic_def,self.agility)
        return player

    def aux_input(self):
        while True:
            aux = input()
            if aux.isdigit():
                aux = int(aux)
                if aux == 0:
                    self.styled_print("{}, O valor precisa ser mairo que ZERO".format(self.nick))
                    continue
                else:
                    return aux

            else:
                self.styled_print("{}, Digite um numero valido".format(self.nick))
                continue

    def create(self):
        flag = 0

        #PEGANDO NICK DO USUARIO
        self.styled_print("Bem vindo ao X, Digite seu nick para comecarmos")
        self.nick = input()

        #PEGANDO RACA DO USUARIO
        self.styled_print("{}, vamos agora montar seu heroi para enfrentar uma dura jornada".format(self.nick))
        self.styled_print("Digite a raca do seu heroi, ele pode ser [human,elf,dwarf,orc,vamp]")
        self.race = input().lower()

        while (flag == 0):
            i = 0

            if i == 5 :
                print("Deixa de ser burro mlk!")
                exit()

            if self.race not in list(RACES.keys()):
                self.styled_print("{}, A raca do do seu heroi precisa ser uma dessas: human,elf,dwarf,orc,vamp".format(self.nick))
                self.race = input().lower()
                i += 1

            else:
                flag = 1

        #PEGANDO STATS DO USUARIO
        self.styled_print("Digite a quantidade de HP que seu heroi tera")
        self.hp = self.aux_input()

        self.styled_print("Agora digite o valor do Dano do seu heroi")
        self.atk = self.aux_input()

        if int(self.atk) > 30:
            print("Vem Tranquilo {} Vem tranquilo".format(self.nick))
            print()

        if int(self.atk) < 5:
            print("Assim nao mata nem mosca, Melho ja quitar {}".format(self.nick))
            print()

        self.styled_print("Digite agora a quantidade de Armadura que seu heroi tera")
        self.armor = self.aux_input()

        self.styled_print("Digite a quantidade de mana para seu heroi")
        self.magic = self.aux_input()

        self.styled_print("Agora digite o valor da defesa magica do seu heroi")
        self.magic_def = self.aux_input()

        self.styled_print(" {}, qual o valor de agilidade quer para seu heroi".format(self.nick))
        self.agility = self.aux_input()

        self.styled_print("Seu heroi parece bom {} \n\r Sera que ele esta pronto para essa jornada?".format(self.nick))


