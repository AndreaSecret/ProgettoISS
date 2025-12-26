from abc import ABC, abstractmethod
import pygame
from game_assets import monster_size, game

# caricamente immagini dei mostri
serpe_front_img =  pygame.transform.scale(pygame.image.load('monster_sprites/Serpe/Serpe_front.png'), monster_size)
serpe_back_img =  pygame.transform.scale(pygame.image.load('monster_sprites/Serpe/Serpe_back.png'), monster_size)
drago_front_img =  pygame.transform.scale(pygame.image.load('monster_sprites/Drago/drago_front.png'), monster_size)
drago_back_img =  pygame.transform.scale(pygame.image.load('monster_sprites/Drago/drago_back.png'), monster_size)

MONSTERS = {
    'Serpe': {'front': serpe_front_img,
              'back': serpe_back_img},
    'Drago': {'front': drago_front_img,
              'back': drago_back_img}
}

# monster actions

class MonsterAction(ABC):
    def __init__(self, name, power, target):
        self.name = name
        self.power = power
        self.target = target

    @abstractmethod
    def execute(self, attacker, target):
        pass


class AttackAction(MonsterAction):
    def execute(self, attacker, target):
        damage = max(1, attacker.attack + self.power - target.defense) # max perchè se la difesa è troppo alta allora la mossa cura
        target.hp -= damage

class HealAction(MonsterAction):
    def execute(self, attacker, target=None):
        attacker.hp += self.power
        if attacker.hp > attacker.max_hp: attacker.hp = attacker.max_hp

class MonsterActionFactory:     
    @staticmethod
    def create_attack(name, power):
        return AttackAction(name, power, target = 'to_other')

    @staticmethod
    def create_heal(name, power):
        return HealAction(name, power, target = 'to_self')

DEFAULT_MOVES = {
    'attack': MonsterActionFactory.create_attack("Graffio", 15),
    'heal': MonsterActionFactory.create_heal("Rigenerazione", 15),
}


class Monster:
    def __init__(self, name, moves, hp, attack, defense, front_image, back_image, team):
        super().__init__()
        self.name = name
        self.moves = moves
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.front_image = front_image
        self.back_image = back_image
        self.team = team
        self.alive = True

    def die(self):
        self.hp = 0
        self.alive = False
        game.remove_monster_from_team(self)

class MonsterFactory:
    def __init__(self, move_factory):
        self.move_factory = move_factory

    def create_dragon(self, team):
        name = 'Drago'
        return Monster(
            name=name,
            hp=150,
            attack=20,
            defense=35,
            moves=[
                self.move_factory.create_attack("Palla di fuoco", 30),
                self.move_factory.create_heal("Assorbi magma", 20),
                DEFAULT_MOVES['attack'],
                DEFAULT_MOVES['heal']],
            front_image=MONSTERS[name]['front'].copy(),
            back_image=MONSTERS[name]['back'].copy(),
            team=team
        )

    def create_snake(self, team):
        name = 'Serpe'
        return Monster(
            name=name,
            hp=100,
            attack=50,
            defense=15,
            moves=[
                self.move_factory.create_attack("Morso", 40),
                self.move_factory.create_heal("Cambio muta", 15),
                DEFAULT_MOVES['attack'],
                DEFAULT_MOVES['heal']],
            front_image=MONSTERS[name]['front'].copy(),
            back_image=MONSTERS[name]['back'].copy(),
            team=team
        )

    def create_monster(self, monster_name, team):
        if monster_name in list(MONSTERS.keys()):
            match monster_name:
                case 'Serpe':
                    return self.create_snake(team)
                case 'Drago':
                    return self.create_dragon(team)
        else:
            raise ValueError("Questo mostro non esiste")

move_factory = MonsterActionFactory()
monster_factory = MonsterFactory(move_factory)