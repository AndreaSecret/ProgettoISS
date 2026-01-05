from pygame import transform, image
from game_assets import monster_size
from moves import move_factory, DEFAULT_MOVES

# caricamente immagini dei mostri
serpe_front_img =  transform.scale(image.load('monster_sprites/Serpe/Serpe_front.png'), monster_size)
serpe_back_img =  transform.scale(image.load('monster_sprites/Serpe/Serpe_back.png'), monster_size)
drago_front_img = transform.scale(image.load('monster_sprites/Drago/drago_front.png'), monster_size)
drago_back_img = transform.scale(image.load('monster_sprites/Drago/drago_back.png'), monster_size)
divoratore_front_img = transform.scale(image.load('monster_sprites/Divoratore/divoratore_front.png'), monster_size)
divoratore_back_img = transform.scale(image.load('monster_sprites/Divoratore/divoratore_back.png'), monster_size)

MONSTERS = {
    'Serpe': {'front': serpe_front_img,
              'back': serpe_back_img},
    'Drago': {'front': drago_front_img,
              'back': drago_back_img},
    'Divoratore': {'front': divoratore_front_img,
              'back': divoratore_back_img}
}

# drago
palla_di_fuoco = move_factory.create_attack("Palla di fuoco", 30)
palla_di_fuoco_plus = move_factory.create_plus_damage(palla_di_fuoco, power=30)

# serpe
cambio_muta = move_factory.create_heal("Cambio muta", 25)
cambio_muta_plus = move_factory.create_plus_heal(cambio_muta, power=50)

# divoratore
leccata = move_factory.create_attack("Leccata", 60)
leccata_plus = move_factory.create_plus_heal(leccata, power=40)
scodinzola = move_factory.create_buff("Scodinzola", 20, 'attack', 2)
scodinzola_plus = move_factory.create_plus_debuff(scodinzola, 50, 'defense', 1)
bagno_di_fango = move_factory.create_heal('Bagno di fango', 20)
bagno_di_fango_plus = move_factory.create_plus_remove_debuffs(bagno_di_fango)

MONSTERS_MOVES = {
    'Drago' : {
                palla_di_fuoco : palla_di_fuoco_plus,
                move_factory.create_heal("Assorbi magma", 20) : None,
                move_factory.create_debuff("Calura", 50, 'defense', 2) : None,
                DEFAULT_MOVES['heal_any'] : None},
    'Serpe' : {
                move_factory.create_attack("Morso", 40) : None,
                cambio_muta : cambio_muta_plus,
                DEFAULT_MOVES['buff_any'] : None,
                DEFAULT_MOVES['heal'] : None
    },
    'Divoratore': {
                leccata : leccata_plus,
                scodinzola : scodinzola_plus,
                bagno_di_fango : bagno_di_fango_plus,
                DEFAULT_MOVES['heal'] : None}
}

class Monster:
    def __init__(self, name, moves, hp, attack, defense, front_image, back_image, team):
        super().__init__()
        self.name = name
        self.moves = moves
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.base_attack = attack
        self.defense = defense
        self.base_defense = defense
        self.status_effects = []
        self.front_image = front_image
        self.back_image = back_image
        self.team = team
        self.alive = True
    
    def add_status_effect(self, se):
        self.status_effects.append(se.copy())

    def update_status_effects(self):
        atk_mult, def_mult = 0.0, 0.0

        for se in self.status_effects.copy():
            stat, value = se.apply()

            if not se.active:
                self.status_effects.remove(se)
                continue

            if stat == 'attack':
                atk_mult += value
            elif stat == 'defense':
                def_mult += value

        atk_mult = max(atk_mult, -1.0)
        def_mult = max(def_mult, -1.0)

        self.attack = int(self.base_attack * (1 + atk_mult))
        self.defense = int(self.base_defense * (1 + def_mult))
    
    def check_death(self):
        if self.hp<=0 and self.alive:
            self.hp = 0
            self.alive = False
            return True
        return False

class MonsterFactory:
    def create_drago(self, team):
        name = 'Drago'
        return Monster(
            name=name,
            hp=150,
            attack=20,
            defense=35,
            moves=MONSTERS_MOVES[name],
            front_image=MONSTERS[name]['front'].copy(),
            back_image=MONSTERS[name]['back'].copy(),
            team=team
        )

    def create_serpe(self, team):
        name = 'Serpe'
        return Monster(
            name=name,
            hp=120,
            attack=50,
            defense=25,
            moves=MONSTERS_MOVES[name],
            front_image=MONSTERS[name]['front'].copy(),
            back_image=MONSTERS[name]['back'].copy(),
            team=team
        )
    
    def create_divoratore(self, team):
        name = 'Divoratore'
        return Monster(
            name=name,
            hp=80,
            attack=100,
            defense=15,
            moves=MONSTERS_MOVES[name],
            front_image=MONSTERS[name]['front'].copy(),
            back_image=MONSTERS[name]['back'].copy(),
            team=team
        )

    def create_monster(self, monster_name, team):
        if monster_name in list(MONSTERS.keys()):
            match monster_name:
                case 'Serpe':
                    return self.create_serpe(team)
                case 'Drago':
                    return self.create_drago(team)
                case 'Divoratore':
                    return self.create_divoratore(team)
        else:
            raise ValueError("Questo mostro non esiste")

monster_factory = MonsterFactory()