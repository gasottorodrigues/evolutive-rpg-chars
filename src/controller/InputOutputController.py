from src.config import *
from src.models.Character import Character
import sys
import json

class InputOutputController:
    @staticmethod
    def get_input(players_file,rooms_file):
        with open(players_file) as pf:
            players_data = json.load(pf)
            attrs = SIMULATION_PARAMS['attrs'].copy()

            race = players_data['party'][0]['race']

            attrs['hp'] = sum([ind['hp'] for ind in players_data['party']])/len(players_data['party'])
            attrs['atk'] = sum([ind['atk'] for ind in players_data['party']])/len(players_data['party'])
            attrs['magic'] = sum([ind['magic'] for ind in players_data['party']])/len(players_data['party'])
            attrs['armor'] = sum([ind['armor'] for ind in players_data['party']])/len(players_data['party'])
            attrs['magic_def'] = sum([ind['magic_def'] for ind in players_data['party']])/len(players_data['party'])
            attrs['agility'] = sum([ind['agility'] for ind in players_data['party']])/len(players_data['party'])

            n_players = len(players_data['party'])
            ref_player = Character(race,attrs['hp'],attrs['atk'],attrs['magic'],attrs['armor'],attrs['magic_def'],attrs['agility'])


        total_mobs = [0,0,0]
        with open(rooms_file) as rf:
            rooms_data = json.load(rf)

            for room in rooms_data['config']:
                if room['diff'] == 1:
                    total_mobs[0] += 3
                    total_mobs[1] += 1
                elif room['diff'] ==  2:
                    total_mobs[0] += 1
                    total_mobs[1] += 2
                    total_mobs[2] += 1
                elif room['diff'] ==  3:
                    total_mobs[2] += 3
                    total_mobs[1] += 1

        return ref_player, total_mobs, rooms_data, n_players
    
    @staticmethod
    def generate_output(rooms_data,mobs_arr,n_players):
        output_dict = {
            'rooms':[]
        }         
        for room in rooms_data['config']:
            new_room = {
                "x":room["x"],
                "y":room["y"],
                "diff":room["diff"],
                "mobs":[]
            }
            if room['diff'] == 1:
                easy = 3
                medium = 1
                hard = 0
            elif room['diff'] ==  2:
                easy = 1
                medium = 2
                hard = 1
            elif room['diff'] ==  3:
                easy = 0
                medium = 1
                hard = 3

            for i in range(0,easy):
                new_room['mobs'].append((mobs_arr[0].pop()).json())
            for i in range(0,medium):
                new_room['mobs'].append((mobs_arr[1].pop()).json())
            for i in range(0,hard):
                new_room['mobs'].append((mobs_arr[2].pop()).json())

            output_dict['rooms'].append(new_room)

        return output_dict