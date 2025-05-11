

def get_info(self):
    return ("Hard Mode", 
            "Decrease Intervals")

def run(game):
    game.enemy_spawn_intervals = [100]


def update(game):
    pass

def wave_cleared(game):
    print(f"Mod: Wave Cleared")