import unittest
from abc import ABC, abstractmethod
import pygame
from game_assets import *


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

class MonsterActionFactory:
    @staticmethod
    def create_attack(name, power):
        return AttackAction(name, power)

    @staticmethod
    def create_heal(name, power):
        return HealAction(name, power)


# monsters

class Monster(pygame.sprite.Sprite):
    def __init__(self, name, moves, hp, attack, defense, image, team):
        super().__init__()
        self.name = name
        self.moves = moves
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.image = image
        self.team = team

    def check_is_alive(self):
        if self.hp<=0:
            #self.kill()
            print(f'{self.name} dead')
        else:
            print(f'{self.name}\'s hp: {self.hp}')
    
    def print_stats(self):
        print(f'{self.name} stats:')
        print(f'atk: {self.attack}')
        print(f'hp: {self.hp}')
        print(f'def: {self.defense}')

    def use_move(self, move_index, target=None):
        if target == None: target = self
        self.moves[move_index].execute(self, target)
    

# monster factory
class MonsterFactory:
    def __init__(self, move_factory):
        self.move_factory = move_factory

    def create_dragon(self, team):
        return Monster(
            name="Dragonazzo",
            hp=150,
            attack=20,
            defense=50,
            moves=[
                self.move_factory.create_attack("Palla di fuoco", 25),
                self.move_factory.create_heal("Rigenerazione", 20)],
            image=None,
            team=team
        )

    def create_snake(self, team):
        return Monster(
            name="Pitone Programmatore",
            hp=100,
            attack=50,
            defense=15,
            moves=[
                self.move_factory.create_attack("Morso", 30),
                self.move_factory.create_heal("Cambio muta", 15)],
            image=None,
            team=team
        )


move_factory = MonsterActionFactory()
monster_factory = MonsterFactory(move_factory)

#esempio di test


drago = monster_factory.create_dragon(0)
serpe = monster_factory.create_snake(1)

print('stats prima della interazione:\n')
drago.print_stats()
serpe.print_stats()

drago.use_move(0, serpe)

print('\ndrago attacca serpe\n')
serpe.print_stats()

serpe.use_move(1)
print('\nserpe si cura\n')
serpe.print_stats()
