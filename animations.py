from game_assets import *
class Animation:
    def __init__(self, obj, start_pos, end_pos, motion_func, parameters, duration):
        self.obj = obj  # oggetto da muovere
        self.start_pos = start_pos # posizione di partenza
        self.end_pos = end_pos # posizione di arrivo a fine animazione
        self.motion_func = motion_func # funzione di moto parametrica 
        self.parameters = parameters # parametri per la funzione sopracitata
        self.duration = duration # numero frame di durata animazione
        self.frame = 0 
        self.finished = False

    def start(self):
        self.frame = 0
        self.finished = False
        self.obj.pos = self.start_pos  # inizializza posizione

    def update(self):
        if self.finished:
            return self.finished

        t = self.frame / self.duration
        if t >= 1:
            t = 1
            self.finished = True
            self.obj.pos = self.end_pos
            return


        x, y = self.motion_func(t, self.parameters)
        self.obj.pos = (x, y)

        self.frame += 1


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
def switch_animation(monster1, monster2):
    anim_atk = Animation(
        obj=monster1,
        start_pos=monster1.pos,
        end_pos=monster2.pos,
        motion_func=ellipse_motion,
        parameters=(theta_attacking, elip, -1),
        duration=switch_duration
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