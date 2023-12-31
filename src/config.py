# Parameters for the simulation

SIMULATION_PARAMS={
    "population_size":500,
    "max_generations":100,
    "breeders":100,
    "target_arr": [2,0,-2],
    "limiter":0.5,
    "player_base_points":100,
    "player_base_race":'elf',
    "attrs":{
        "hp":0,
        "atk":0,
        "magic":0,
        "armor":0,
        "magic_def":0,
        "agility":0,
    },
    "eval_coefs":{
        "hp":1,
        "dmg":0.8,
        "def":0.9,
        "agility":0.9,
    },
    "mutation":{
        "mutation_aggr":1,
        "mutation_per_ind":5
    }
}


OUTPUT_INFOS=[3,5,2]

# Genes of each race
RACES={
    'human':{
        "genes":{
            "hp":21,
            "atk":20,
            "magic":12,
            "armor":18,
            "magic_def":13,
            "agility":17
        },
        "attack":{
            "name":"Simple Atack",
            "nature":"physical"
        }
    },
    'elf':{
        "genes":{
        "hp":15,
        "atk":5,
        "magic":25,
        "armor":15,
        "magic_def":15,
        "agility":25
        },
        "attack":{
            "name":"Dark Arrow",
            "nature":"magic"
        }
        
    },
    'dwarf':{
        "genes":{
            "hp":25,
            "atk":20,
            "magic":3,
            "armor":20,
            "magic_def":17,
            "agility":15
        },
        "attack":{
            "name":"Forge Hammer",
            "nature":"magical"
        }
    },
    'orc':{
        "genes":{
            "hp":25,
            "atk":17,
            "magic":10,
            "armor":20,
            "magic_def":17,
            "agility":10
        },
        "attack":{
            "name":"Brutal Assault",
            "nature":"physical"
        }
    },
    'vamp':{
        "genes":{
            "hp":19,
            "atk":1,
            "magic":25,
            "armor":15,
            "magic_def":15,
            "agility":25
        },
         "attack":{
            "name":"Bloody Bite",
            "nature":"magical"
        }
    }
}
