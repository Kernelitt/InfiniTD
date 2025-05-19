

def get_info(self):
    return ("Hard Mode", 
            "Increase Difficulty")

def run(game):
    game.economy -= 20


def update(game):
    current_enemy = game.wave % 3
    
    for enemy in game.enemies:
        if current_enemy == 0:
            if enemy.health <= game.max_health:       #Basic
                enemy.health += game.max_health / 500
        if current_enemy == 1:
            if enemy.health <= game.max_health / 1.8: #Fast
                enemy.health += game.max_health / 500
        if current_enemy == 2:
            if enemy.health <= game.max_health * 1.5: #Strong
                enemy.health += game.max_health / 500

def wave_cleared(game):
    pass