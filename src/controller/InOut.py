from src.models.Character import RACES
import sys
import time

lista_races = list(RACES.keys())
lista_ataques = ["fisico","magico"]
lista_nome_ataques = []


class CreateUser:

    def __init__(self):
        self.race = None
        self.hp = None
        self.atk = None
        self.magic = None
        self.armor = None
        self.magic_def = None
        self.agility = None
        self.typeatack = None

    @staticmethod
    def obter_nomes_ataques_por_raca():

        for raca, detalhes in RACES.items():
            if 'attack' in detalhes and 'name' in detalhes['attack']:
                lista_nome_ataques.append(detalhes['attack']['name'])

    def _printComEfeito(self,mensagem):
        for char in mensagem:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.03)  # Ajuste este valor para controlar a velocidade de exibição
        print()

    def _geraJson(self):
        self.obter_nomes_ataques_por_raca()
        if self.race == "human":
            nomeAtaque = lista_nome_ataques[0]
        if self.race == "elf":
            nomeAtaque = lista_nome_ataques[1]
        if self.race == "dwarf":
            nomeAtaque = lista_nome_ataques[2]
        if self.race == "orc":
            nomeAtaque = lista_nome_ataques[3]
        if self.race == "vamp":
            nomeAtaque = lista_nome_ataques[4]

        nova_raca = {
            "genes": {
            "hp": self.hp,
            "atk": self.atk,
            "magic": self.magic,
            "armor": self.armor,
            "magic_def": self.magic_def,
            "agility": self.agility
                },
                    "attack": {
                        "name": nomeAtaque,
                        "nature": self.typeatack
                    }
                }
        RACES["player"] = nova_raca

    def createUser(self):
        flag = 0

        #PEGANDO NICK DO USUARIO
        self._printComEfeito("Bem vindo ao X, Digite seu nick para comecarmos")
        self.nick = input()

        #PEGANDO RACA DO USUARIO
        self._printComEfeito("{}, vamos agora montar seu heroi para enfrentar uma dura jornada".format(self.nick))
        self._printComEfeito("Digite a raca do seu heroi, ele pode ser [human,elf,dwarf,orc,vamp]")
        self.race = input().lower()

        while (flag == 0):
            i = 0

            if i == 5 :
                print("Deixa de ser burro mlk!")
                exit()

            if self.race not in lista_races:
                self._printComEfeito("{}, A raca do do seu heroi precisa ser uma dessas: human,elf,dwarf,orc,vamp".format(self.nick))
                self.race = input().lower()
                i += 1

            else:
                flag = 1

        #PEGANDO STATS DO USUARIO
        self._printComEfeito("Digite a quantidade de HP que seu heroi tera")
        self.hp = input()

        self._printComEfeito("Agora digite o valor do Dano do seu heroi")
        self.atk = input()
        if int(self.atk) > 50:
            print("Vem Tranquilo {} Vem tranquilo".format(self.nick))
            print()

        if int(self.atk) < 20:
            print("Assim nao mata nem mosca, Melho ja quitar {}".format(self.nick))
            print()

        self._printComEfeito("Digite agora a quantidade de Armadura que seu heroi tera")
        self.armor = input()

        self._printComEfeito("Digite a quantidade de mana para seu heroi")
        self.magic = input()

        self._printComEfeito("Agora digite o valor da defesa magica do seu heroi")
        self.magic_def = input()

        self._printComEfeito(" {}, qual o valor de agilidade quer para seu heroi".format(self.nick))
        self.agility = input()

        ##TIPO DE DANO
        self._printComEfeito("Por fim {}, voce quer que seu heori de dano fisico ou magico?".format(self.nick))
        aux = input().lower()
        flag = 0
        while (flag == 0):
            i = 0

            if i == 5 :
                print("Deixa de ser burro mlk!")
                exit()

            if aux not in lista_ataques:
                self._printComEfeito("{}, O tipo de ataque pode ser apenas fisico ou magico".format(self.nick))
                aux = input().lower()
                i += 1

            else:
                flag = 1
                if aux == "fisico":
                    self.typeatack = "physical"
                else:
                    self.typeatack = "magic"


        self._printComEfeito("Seu heroi parece bom {} \n Sera que ele esta pronto para essa jornada?".format(self.nick))

    def printaUser(self):
        entrada = 0
        self._printComEfeito("Caso queira olhar como seu heori ficou {}, digite 1, caso queira comecar sua aventura pressione ENTER".format(self.nick))
        entrada = input()
        if type(entrada) == int and int(entrada) == 1:
            self._printComEfeito("{}, Seu heroi é do tipo {} e possui as seguintes caracteristicas:".format(self.nick,self.race))

            print(f"HP : {self.hp}")
            print(f"DANO : {self.atk}")
            print(f"MANA : {self.magic}")
            print(f"ARMADURA : {self.armor}")
            print(f"DEFESA MAGICA : {self.magic_def}")
            print(f"AGILIDADE : {self.agility}")
            print(f"TIPO DE ATAQUE : {self.typeatack}")





usuario1 = CreateUser()

usuario1.createUser()
usuario1.printaUser()
usuario1._geraJson()

print("A")