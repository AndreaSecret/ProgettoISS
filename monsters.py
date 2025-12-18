from abc import ABC, abstractmethod
import pygame
from game_assets import *
serpe_front_img =  pygame.transform.scale(pygame.image.load('monster_sprites/Serpe/Serpe_front.png'), monster_size)
serpe_back_img =  pygame.transform.scale(pygame.image.load('monster_sprites/Serpe/Serpe_back.png'), monster_size)
drago_front_img =  pygame.transform.scale(pygame.Surface(monster_size), monster_size)
drago_front_img.fill("#FFA601")
drago_back_img =  pygame.transform.scale(pygame.Surface(monster_size), monster_size)
drago_back_img.fill("#895900")

# monster actions
class MonsterAction(ABC):
    def __init__(self, name, power):
        self.name = name
        self.power = power

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
        return AttackAction(name, power)

    @staticmethod
    def create_heal(name, power):
        return HealAction(name, power)

DEFAULT_MOVES = {
    'attack': MonsterActionFactory.create_attack("Graffio", 15),
    'heal': MonsterActionFactory.create_heal("Rigenerazione", 15),
}


# monsters

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


# monster factory
class MonsterFactory:
    def __init__(self, move_factory):
        self.move_factory = move_factory

    def create_dragon(self, team):
        return Monster(
            name="Drago",
            hp=150,
            attack=20,
            defense=50,
            moves=[
                self.move_factory.create_attack("Palla di fuoco", 25),
                self.move_factory.create_heal("Assorbi magma", 20),
                DEFAULT_MOVES['attack'],
                DEFAULT_MOVES['heal']],
            front_image=drago_front_img,
            back_image=drago_back_img,
            team=team
        )

    def create_snake(self, team):
        return Monster(
            name="Serpe",
            hp=100,
            attack=50,
            defense=15,
            moves=[
                self.move_factory.create_attack("Morso", 30),
                self.move_factory.create_heal("Cambio muta", 15),
                DEFAULT_MOVES['attack'],
                DEFAULT_MOVES['heal']],
            front_image=serpe_front_img,
            back_image=serpe_back_img,
            team=team
        )


move_factory = MonsterActionFactory()
monster_factory = MonsterFactory(move_factory)

#esempio di test


drago = monster_factory.create_dragon(0)
serpe = monster_factory.create_snake(1)