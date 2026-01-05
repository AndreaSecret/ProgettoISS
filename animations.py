from game_assets import attacking_monster_pos, defending_monster_pos, screen_x, game

animation_types = ['attacking', 'returning_to_place', 'switching_sides', 'dying']

# singleton managing all the animations

class AnimationManager:
    def __init__(self):
        self.current = None
        self.animations_queue = []

    def add_animations(self, type, animations):
        assert type in animation_types
        assert all(anim.duration == animations[0].duration for anim in animations), "Le animazioni simultanee devono avere la stessa durata"
        self.animations_queue.append((type, animations))

    def update(self):
        '''
        La classe lavora sul primo elemento della coda,
        ogni elemento della coda è formato da una tupla ('nome_animazione', [animazioni])
        animazioni è una lista, ma può essere anche di un solo elemento.
        Questo perchè se più elementi sono presenti in [animazioni], verranno eseguiti in simultanea.
        Lavorando su una coda, passa alla seconda animazione in coda solo dopo aver terminato la prima.
        '''
        if self.animations_queue:
            self.current, anims = self.animations_queue[0]
            for anim in anims:
                is_finished = anim.update()
            if is_finished: #in questo caso ho fatto finire tutte le animazioni
                self.animations_queue.pop(0)
            return is_finished
        else:
            self.current = None
    
    def add_switching_sides_anim(self, monster1, monster2, game_switch):
        anims = switch_animation(monster1, monster2, game_switch)
        self.add_animations('switching_sides', anims)
    
    def add_attack_anim(self, monster_sprite, target, move):
        atk_anim, return_anim = attack_animations(monster_sprite, target, move)
        self.add_animations('attacking', [atk_anim])
        self.add_animations('returning_to_place', [return_anim])

    def add_death_anim(self, monster_sprite):
        self.animations_queue.insert(1, ('dying', [death_animation(monster_sprite)]))

animation_manager = AnimationManager() #singleton

class Animation:
    def __init__(self, obj, start_pos, end_pos, motion_func, parameters, duration, on_finish = None, fade_out = None):
        self.obj = obj  # oggetto da muovere
        self.start_pos = start_pos # posizione di partenza
        self.end_pos = end_pos # posizione di arrivo a fine animazione
        self.motion_func = motion_func # funzione di moto parametrica 
        self.parameters = parameters # parametri per la funzione sopracitata
        self.duration = duration # numero frame di durata animazione
        self.frame = 0 
        self.finished = False
        self.on_finish = on_finish # funzione da applicare una volta finita l'animazione
        self.fade_out = fade_out # valore di alpha che vuoi che raggiunga l'oggetto a fine animazione (dissolvenza graduale)
        self.alpha = 255

    def update(self):
        if self.finished:
            return self.finished

        t = self.frame / self.duration
        if t >= 1:
            t = 1
            self.finished = True
            self.obj.pos = self.end_pos
            if self.fade_out:
                self.obj.image.set_alpha(self.fade_out)
            if self.on_finish:
                self.on_finish() 
            return self.finished

        if self.fade_out:
            self.alpha = int(255 + (self.fade_out - 255) * t)
            self.obj.image.set_alpha(self.alpha)
            self.obj.front_image.set_alpha(self.alpha)
            self.obj.back_image.set_alpha(self.alpha)
        x, y = self.motion_func(t, self.parameters)
        self.obj.pos = (x, y)

        self.frame += 1

 # Geometric calculations and animations functions

import math

def compute_ellipse(start, end, a):  # calcola funzione ellisse passante per start e end con data a (mezza larghezza ellisse)
    x1, y1 = start
    x2, y2 = end

    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2

    dx = x1 - cx
    dy = y1 - cy

    denom = 1 - (dx*dx) / (a*a)
    if denom <= 0:
        raise ValueError("Ellisse impossibile con questo valore di a")

    b = abs(dy) / math.sqrt(denom)
    return (cx, cy, a, b)

elip = compute_ellipse(attacking_monster_pos, defending_monster_pos, a=screen_x*2/3)

def ellipse_start_angle(start, elip): # calcolo punto di start dall'ellisse 
    cx, cy, a, b = elip
    return math.atan2(
        (start[1] - cy) / b,
        (start[0] - cx) / a
    )
theta_attacking = ellipse_start_angle(attacking_monster_pos, elip)
theta_defending = ellipse_start_angle(defending_monster_pos, elip)

def ellipse_motion(t, parameters):  # funzione effettiva ellissa (sign cambia il senso)
    theta_start, elip, sign = parameters
    cx, cy, a, b = elip
    theta = theta_start + sign * math.pi * t
    x = cx + a * math.cos(theta)
    y = cy + b * math.sin(theta)
    return x, y

switch_duration = 50 
def switch_animation(monster1, monster2, game_switch):
    anim_atk = Animation(
        obj=monster1,
        start_pos=monster1.pos,
        end_pos=monster2.pos,
        motion_func=ellipse_motion,
        parameters=(theta_attacking, elip, -1),
        duration=switch_duration,
        on_finish=game_switch
    )
    anim_def = Animation(
        obj=monster2,
        start_pos=monster2.pos,
        end_pos=monster1.pos,
        motion_func=ellipse_motion,
        parameters=(theta_defending, elip, -1),
        duration=switch_duration 
    )
    return (anim_atk, anim_def)


def compute_line(start, end):
    x1, y1 = start
    x2, y2 = end
    return (x1, y1, x2, y2)

# per mosse con target il nemico (attacco e debuff)
stop_atk = (attacking_monster_pos[0]+abs(attacking_monster_pos[0]-defending_monster_pos[0])/5,attacking_monster_pos[1]-abs(attacking_monster_pos[1]-defending_monster_pos[1])/5)
atk_line = compute_line(attacking_monster_pos, stop_atk)

# per mosse con target se stesso (cura e buff)
stop_heal = (attacking_monster_pos[0],attacking_monster_pos[1]-abs(attacking_monster_pos[1]-defending_monster_pos[1])/5)
heal_line = compute_line(attacking_monster_pos, stop_heal)

def line_motion(t, parameters):
    x1, y1, x2, y2, reverse = parameters

    if reverse:
        t = 1 - t
    x = x1 + (x2 - x1) * t
    y = y1 + (y2 - y1) * t

    return x, y

atk_duration = 10
def attack_animations(monster_sprite, target, move):
    if move.target == 'to_self':
        end_pos = stop_heal
        line = heal_line
    elif move.target == 'to_other':
        end_pos = stop_atk
        line = atk_line
    else:
        raise ValueError('Move target not identified')

    def apply_effect():
        move_xp = move.execute(attacker=monster_sprite.monster, target=target)
        game.update_xp(move_xp)

    attack_anim = Animation(
        obj=monster_sprite,
        start_pos=monster_sprite.pos,
        end_pos=end_pos,
        motion_func=line_motion,
        parameters=line+tuple([False]),
        duration=atk_duration,
        on_finish=apply_effect)
    return_anim = Animation(
        obj=monster_sprite,
        start_pos=end_pos,
        end_pos=attacking_monster_pos,
        motion_func=line_motion,
        parameters=line+tuple([True]),
        duration=atk_duration)
    return (attack_anim, return_anim)

# può morire solo il mostro attaccato
stop_death = (defending_monster_pos[0],defending_monster_pos[1]+abs(attacking_monster_pos[1]-defending_monster_pos[1])/5)
death_line = compute_line(defending_monster_pos, stop_death)
death_anim_duration = 60
def death_animation(monster_sprite):
    death_anim = Animation(
        obj=monster_sprite,
        start_pos=monster_sprite.pos,
        end_pos=stop_death,
        motion_func=line_motion,
        parameters=death_line+tuple([False]),
        duration=death_anim_duration,
        fade_out=1)
    return death_anim