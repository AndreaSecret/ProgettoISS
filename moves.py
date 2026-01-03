from abc import ABC, abstractmethod
from game_assets import game

class MonsterAction(ABC):
    def __init__(self, name, power, target, type, choose_target=False, xp_gain=1):
        self.name = name
        self.type = type
        assert type in ['attack', 'heal', 'buff', 'debuff']
        self.power = power
        assert target in ['to_other', 'to_self']
        self.target = target
        self.choose_target = choose_target # applicabile solo ai buff!!!
        self.xp_gain = xp_gain # xp che dà la mossa quando utilizzata
        self.is_plus = False

    def execute(self, attacker, target):
        
        self.activate(attacker, target) # eseguo la mossa

        if game.teams_xp[attacker.team] < game.max_xp: # se non è attivo il plus
            game.teams_xp[attacker.team] += self.xp_gain # aggiungo l'esperienza alla barra
        if game.teams_xp[attacker.team] >= game.max_xp: #se è attivo o deve attivarsi il plus
            if game.active_plus_durations[attacker.team] > 0: # il plus è stato attivato turni scorsi
                game.active_plus_durations[attacker.team]-=1
                if game.active_plus_durations[attacker.team] == 0: game.teams_xp[attacker.team] = 0 # rimuovo il plus
            else: # attivo il plus
                game.active_plus_durations[attacker.team] = game.plus_moves_duration

    @abstractmethod
    def activate(self, attacker, target):
        pass

class AttackAction(MonsterAction):
    def activate(self, attacker, target):
        damage = max(1, attacker.attack + self.power - target.defense) # max perchè se la difesa è troppo alta allora la mossa cura
        target.hp -= damage

class HealAction(MonsterAction):
    def activate(self, attacker, target):
        if self.choose_target:
            target.hp += self.power
            if target.hp > target.max_hp: target.hp = target.max_hp
        else:
            attacker.hp = min(attacker.hp+self.power, attacker.max_hp)

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
        if self.effective_duration > 0:
            return (self.targeted_stat, self.power/100)
        else:
            self.active = False
            return None, None
    
    def copy(self):
        return Status_effect(self.targeted_stat, self.power, self.duration)

class Apply_Buff_Action(MonsterAction):
    def __init__(self, name, power, target, status_effect, type, choose_target=False):
        super().__init__(name, power, target, type, choose_target)
        self.status_effect = status_effect

    def activate(self, attacker, target):
        if self.choose_target:
            target.add_status_effect(self.status_effect)
        else:
            attacker.add_status_effect(self.status_effect)

class Apply_Debuff_Action(MonsterAction):
    def __init__(self, name, power, target, status_effect, type):
        super().__init__(name, power, target, type)
        self.status_effect = status_effect

    def activate(self, attacker, target):
        target.add_status_effect(self.status_effect)

class PlusAction(MonsterAction): # decorator pattern
    def __init__(self, base_move: MonsterAction, plus_type):
        super().__init__(
            name=base_move.name + '+',
            power=base_move.power,
            target=base_move.target,
            type=base_move.type,
            choose_target=base_move.choose_target,
            xp_gain=base_move.xp_gain
        )
        self.base_move = base_move
        self.is_plus = True
        assert plus_type in ['heal', 'damage', 'debuff', 'buff', 'remove_debuffs']
        self.plus_type = plus_type

    @abstractmethod
    def activate(self, attacker, target):
        self.base_move.activate(attacker=attacker, target=target)
        pass

class PlusHeal(PlusAction):
    def __init__(self, base_move, heal_amount):
        super().__init__(base_move, plus_type='heal')
        self.heal_amount = heal_amount

    def activate(self, attacker, target):
        self.base_move.activate(attacker, target)
        attacker.hp = min(attacker.hp + self.heal_amount, attacker.max_hp)

class PlusDamage(PlusAction):
    def __init__(self, base_move, dmg_amount):
        super().__init__(base_move, plus_type='damage')
        self.dmg_amount = dmg_amount

    def activate(self, attacker, target):
        self.base_move.activate(attacker, target)
        damage = max(1, attacker.attack + self.dmg_amount - target.defense)
        target.hp -= damage

class PlusDebuff(PlusAction):
    def __init__(self, base_move, plus_status_effect):
        super().__init__(base_move, plus_type='debuff')
        self.status_effect = base_move.status_effect
        self.plus_status_effect = plus_status_effect

    def activate(self, attacker, target):
        self.base_move.activate(attacker, target)
        target.add_status_effect(self.plus_status_effect)

class PlusRemoveDebuffs(PlusAction):
    def __init__(self, base_move):
        super().__init__(base_move, plus_type='remove_debuffs')

    def activate(self, attacker, target):
        self.base_move.activate(attacker, target)
        for se in attacker.status_effects.copy():
            if se.power < 0: attacker.status_effects.remove(se)

class MonsterActionFactory:     
    @staticmethod
    def create_attack(name, power):
        return AttackAction(name, power, type='attack', target = 'to_other')

    @staticmethod
    def create_heal(name, power, choose_target=False):
        return HealAction(name, power, type='heal', target = 'to_self', choose_target=choose_target)
    
    @staticmethod
    def create_debuff(name, power, targeted_stat, duration):
        return Apply_Debuff_Action(name, power, type='debuff', target = 'to_other', status_effect=Status_effect(targeted_stat, -power, duration))
    
    @staticmethod
    def create_buff(name, power, targeted_stat, duration, choose_target=False):
        return Apply_Buff_Action(name, power, type='buff', target = 'to_self', status_effect=Status_effect(targeted_stat, power, duration), choose_target=choose_target)

    @staticmethod
    def create_plus_damage(base, power):
        return PlusDamage(base, power)

    @staticmethod
    def create_plus_heal(base, power):
        return PlusHeal(base, power)
    
    @staticmethod
    def create_plus_debuff(base, power, targeted_stat, duration):
        return PlusDebuff(base, plus_status_effect=Status_effect(targeted_stat, -power, duration))
    
    @staticmethod
    def create_plus_remove_debuffs(base):
        return PlusRemoveDebuffs(base)
    
move_factory = MonsterActionFactory()

DEFAULT_MOVES = {
    'attack': move_factory.create_attack("Graffio", 15), # danno al nemico
    'heal': move_factory.create_heal("Rigenerazione", 15), #cura a se stesso
    'heal_any': move_factory.create_heal("Aiuto a casa", 40, choose_target=True), # cura a chiunque nel team
    'buff_any': move_factory.create_buff('Rinforzo', 30, 'attack', 3, choose_target=True) # buff di 40% a chiunque nel team per 3 turni
}
