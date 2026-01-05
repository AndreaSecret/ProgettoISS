from pygame import Surface, font
from pygame.sprite import Sprite, GroupSingle
from game_assets import game, screen_x, screen_y, bar_h, monster_size, attacking_monster_pos, defending_monster_pos, game_font
font.init()

# semplicemente il rettangolo in basso con le mosse ecc.
class MatchBar(Sprite):
    def __init__(self):
        super().__init__()
        self.state = None
        size = (screen_x, bar_h)
        self.image = Surface(size)
        self.image.fill("#FFFFFF")
        self.pos = (0, screen_y-bar_h)
        self.rect = self.image.get_rect(topleft = self.pos)

bar = GroupSingle(MatchBar())

# barra vita, nome, exp
class BattleBox(Sprite):
    def __init__(self, pos):
        super().__init__()
        self.monster = None
        size_x, size_y = (monster_size[0], monster_size[1]/4)
        self.image = Surface((size_x, size_y))
        self.image.fill("#FFFFFF")
        self.pos = pos
        self.rect = self.image.get_rect(topleft = self.pos)

        self.bars_size_x = size_x*29/30
        self.hp_bar_size_y = size_y/5
        self.xp_bar_size_y = size_y/10

        self.spacing = (size_x - self.bars_size_x)/2
        self.bars_x = size_x-self.bars_size_x-self.spacing
        self.hp_bar_y = self.spacing
        self.xp_bar_y = self.hp_bar_y+self.hp_bar_size_y

        self.hp_bar = Surface((self.bars_size_x, self.hp_bar_size_y))
        self.hp_bar_pos = (self.bars_x, self.hp_bar_y)

        self.xp_bar = Surface((self.bars_size_x, self.xp_bar_size_y))
        self.xp_bar_pos = (self.bars_x, self.xp_bar_y)

        text_size = round((size_y-self.xp_bar_y)/2)
        self.text_font = font.Font(game_font, text_size)
        self.text_pos = (self.spacing,self.xp_bar_y+self.xp_bar_size_y+self.spacing)

        hp_text_size = round(self.hp_bar_size_y)-2
        self.hp_text_font = font.Font(game_font, hp_text_size)
        self.hp_text_pos = (self.spacing,1)
    
    def set_monster(self, monster):
        self.monster = monster

    def draw_background(self):
        self.image.fill('#FFFFFF')
        monster_name = self.monster.name
        name_surface = self.text_font.render(monster_name, True, (0, 0, 0))
        self.image.blit(name_surface, self.text_pos)

    def draw_hp_bar(self):
        hp_ratio = self.monster.hp/self.monster.max_hp
        self.hp_bar.fill("#FC2C2C")
        green_portion = self.bars_size_x*hp_ratio
        if green_portion>0:
            green_hp = Surface((green_portion,self.hp_bar_size_y))
            green_hp.fill("#2CF150")
            self.hp_bar.blit(green_hp, (0,0))
        hp_text = str(self.monster.hp)+'/'+str(self.monster.max_hp)
        hp_text_surface = self.hp_text_font.render(hp_text, True, (0, 0, 0))
        self.hp_bar.blit(hp_text_surface, self.hp_text_pos)

        self.image.blit(self.hp_bar, self.hp_bar_pos)
    
    def draw_xp_bar(self):
        team = self.monster.team
        xp_ratio = game.teams_xp[team]/game.max_xp
        self.xp_bar.fill("#7AA5EF")
        filled_portion = self.bars_size_x*xp_ratio
        if game.active_plus_durations[team] > 0:
            self.xp_bar.fill("#FFE520")
        elif filled_portion>0:
            filled_xp = Surface((filled_portion,self.xp_bar_size_y))
            filled_xp.fill("#064CC5")
            self.xp_bar.blit(filled_xp, (0,0))
        self.image.blit(self.xp_bar, self.xp_bar_pos)

    def update(self):
        self.draw_background()
        self.draw_hp_bar()
        self.draw_xp_bar()

attacking_monster_box_pos = (attacking_monster_pos[0]+monster_size[0]*1.2, attacking_monster_pos[1]+monster_size[1]*0.2)
attacking_monster_box = BattleBox(attacking_monster_box_pos)

defending_monster_box_pos = (defending_monster_pos[0]-monster_size[0]*0.2-attacking_monster_box.rect.w, defending_monster_pos[1]+monster_size[1]*0.2)
defending_monster_box = BattleBox(defending_monster_box_pos)

# attacco e difesa
class InfoBox(Sprite):
    def __init__(self, pos):
        super().__init__()
        self.monster = None
        self.size_x, self.size_y = (monster_size[0]*0.5, monster_size[1]*0.3)
        self.image = Surface((self.size_x, self.size_y))
        self.image.fill("#FFFFFF")
        self.pos = pos
        self.rect = self.image.get_rect(topleft = self.pos)

        self.spacing_y = self.size_y/20
        text_size = round(self.size_y/3-self.spacing_y)
        self.text_font = font.Font(game_font, text_size)

    def set_monster(self, monster):
        self.monster = monster
        self.image.fill("#FFFFFF")

        atk_text = 'ATK: '+str(self.monster.attack)
        if self.monster.attack > self.monster.base_attack: atk_color = (0,0,200)
        elif self.monster.attack < self.monster.base_attack: atk_color = (200,0,0)
        else: atk_color = (0,0,0)
        atk_text_surface = self.text_font.render(atk_text, True, atk_color)
        atk_pos = ((self.size_x-atk_text_surface.get_width())/2, self.size_y/2-self.spacing_y-atk_text_surface.get_height())
        self.image.blit(atk_text_surface, atk_pos)

        def_text = 'DEF: '+str(self.monster.defense)
        if self.monster.defense > self.monster.base_defense: def_color = (0,0,200)
        elif self.monster.defense < self.monster.base_defense: def_color = (200,0,0)
        else: def_color = (0,0,0)
        def_text_surface = self.text_font.render(def_text, True, def_color)
        def_pos = ((self.size_x-def_text_surface.get_width())/2, self.size_y/2+self.spacing_y)
        self.image.blit(def_text_surface, def_pos)

defending_monster_infobox_pos = (defending_monster_pos[0]+monster_size[0], defending_monster_pos[1]-monster_size[1]*0.1)
defending_monster_infobox = InfoBox(defending_monster_infobox_pos)

attacking_monster_infobox_pos = (attacking_monster_pos[0]-defending_monster_infobox.rect.w*0.8, attacking_monster_pos[1]-monster_size[1]*0.1)
attacking_monster_infobox = InfoBox(attacking_monster_infobox_pos)