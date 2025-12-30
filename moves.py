from abc import ABC, abstractmethod

class MonsterAction(ABC):
    def __init__(self, name, power, target):
        self.name = name
        self.power = power
        assert target in ['to_other', 'to_self']
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

class Status_effect(ABC):
    def __init__(self, targeted_stat, power, duration):
        assert targeted_stat in ['attack', 'defense']
        self.targeted_stat = targeted_stat 
        assert -100 <= power <= 100
        self.power = power # power in % da -100 a 100
        self.duration = duration
        self.effective_duration = duration*2+1 # turni di durata dell'effetto
        self.active = True

    def apply(self):
        self.effective_duration-=1
        print(self.effective_duration)
        if self.effective_duration > 0:
            return (self.targeted_stat, self.power/100)
        else:
            self.active = False
            return None, None
    
    def copy(self):
        return Status_effect(self.targeted_stat, self.power, self.duration)

class Apply_Buff_Action(MonsterAction):
    def __init__(self, name, power, target, status_effect):
        super().__init__(name, power, target)
        self.status_effect = status_effect
    def execute(self, attacker, target=None):
        attacker.add_status_effect(self.status_effect)

class Apply_Debuff_Action(MonsterAction):
    def __init__(self, name, power, target, status_effect):
        super().__init__(name, power, target)
        self.status_effect = status_effect
    def execute(self, target, attacker=None):
        target.add_status_effect(self.status_effect)
    


class MonsterActionFactory:     
    @staticmethod
    def create_attack(name, power):
        return AttackAction(name, power, target = 'to_other')

    @staticmethod
    def create_heal(name, power):
        return HealAction(name, power, target = 'to_self')
    
    @staticmethod
    def create_debuff(name, power, targeted_stat, duration):
        return Apply_Debuff_Action(name, power, target = 'to_other', status_effect=Status_effect(targeted_stat, -power, duration))
    
    @staticmethod
    def create_buff(name, power, targeted_stat, duration):
        return Apply_Buff_Action(name, power, target = 'to_self', status_effect=Status_effect(targeted_stat, power, duration))

DEFAULT_MOVES = {
    'attack': MonsterActionFactory.create_attack("Graffio", 15),
    'heal': MonsterActionFactory.create_heal("Rigenerazione", 15),
}

move_factory = MonsterActionFactory()