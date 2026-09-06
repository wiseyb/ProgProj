class master():
    def __init__(s):
        s.strmode='n'
    def str_mode(s,mode='n'):
        modes=['n','g']
        if mode in modes:
            s.strmode=str(mode)
        else:
            s.strmode='n'

class char(master):
    def __init__(s):
        super().__init__()
        s.name=''
        s.type=''
        s.health=-1
        s.attackv=-1
        s.spell=-1
    def load_data(s):
        return False
    def damage(s,damag):
        t_health=s.health-damag
        if t_health<=0:
            s.health=0
            return False
        else:
            s.health-=damag
            return True

    def attack(s,t,damag):
        t.damage(damag)
    def __str__(s):
        if s.strmode=='n':
            return f'''---DATA---
Name: {s.name}
Type: {s.type}
Health: {s.health}
Attack: {int(s.attackv)}
Spell: {s.spell}

'''
        elif s.strmode=='g':
            return f'''{s.name} has {s.health} health, an attack strength of {int(s.attackv)} and a Spell damage of {s.spell}.
'''


class player(char):
    def __init__(s,name,health=1000,atta=1000,spell=1000):
        super().__init__()
        s.name=name
        s.type='Player'
        s.health=health
        s.health=health
        s.attackv=atta
        s.spell=spell



class enemy(char):
    def __init__(s,name,health=1000,atta=1000,spell=1000):
        super().__init__()
        s.name=name
        s.type='Enemy'
        s.health=health
        s.attackv=atta
        s.spell=spell

#Class system for game operation

class game_sys():
    def __init__(s):
        s.gdta=[]
        s.map=[]
        s.level=[]
        s.chars={}
        s.player=None
        s.current_enemy=None
        s.level_index=0
        s.level_p=False
        s.char_init=False
        s.prepped=True

    def load(s,file):
        s.prepped=False
        f=open(f'./DTA/{file}.gmdta','r')
        s.gdta=[]
        for l in f:
            ls=l.strip('\n')
            s.gdta.append(ls)
        f.close()

    def load_player(s,file):
        with open(f'./DTA/{file}.chrdta','r') as f:
            data=f.read().split()

        s.player=player(data[0], int(data[1]), int(data[2]), int(data[3]))
        return s.player

    def save_player(s,file):
        with open(f'./DTA/{file}.chrdta','w') as f:
            f.write(f'{s.player.name} {s.player.health} {s.player.attackv} {s.player.spell}\n')

    def prep(s):
        tmg=[]
        for i in range(len(s.gdta)):
            if s.gdta[i]=='__map__':
                pass
            elif s.gdta[i-1] == '__map__' and s.gdta[i] != None:
                mdta=s.gdta[i].split()
                for e in mdta:
                    gr=e.split(',')
                    for t in gr:
                        tmg.append(int(t))
                    s.map.append(tmg)
                    tmg=[]
            elif s.gdta[i]=='__enemy__':
                s.char_init=True
            elif s.gdta[i]=='__level__':
                s.char_init=False
                s.level_p=True
            elif s.char_init:
                s.att=s.gdta[i].split(' ')
                s.chars[f'{s.att[0].lower()}']=enemy(s.att[0],int(s.att[1]),int(s.att[2]),int(s.att[3]))
            elif s.level_p:
                s.levelatt=s.gdta[i].split(' ')
                for j in range(int(s.levelatt[0])):
                    s.level.append(s.levelatt[1])
        s.prepped=True

    def turn(s,en,pl,pa):
        pl.str_mode('g')
        en.str_mode('g')
        if pa==1:
            pl.attack(en,pl.attackv)
        elif pa==2:
            pl.attack(en,pl.spell)
        if en.health > 0:
            en.attack(pl,en.attackv)

    def begin(s,player):
        s.player=player
        s.level_index=0
        s.current_enemy=None
        if s.level:
            enemy_name=s.level[0]
            enemy_data=s.chars[enemy_name.lower()]
            s.current_enemy=enemy(
                enemy_data.name,
                enemy_data.health,
                int(enemy_data.attackv),
                enemy_data.spell,
            )
        return s.current_enemy

    def take_turn(s,pa):
        if s.player is None or s.current_enemy is None:
            return 'complete'

        s.turn(s.current_enemy,s.player,pa)
        if s.player.health <= 0:
            return 'defeat'
        if s.current_enemy.health <= 0:
            s.level_index+=1
            return 'victory'
        return 'continue'

    def next_encounter(s):
        if s.level_index >= len(s.level):
            s.current_enemy=None
            return False

        enemy_name=s.level[s.level_index]
        enemy_data=s.chars[enemy_name.lower()]
        s.current_enemy=enemy(
            enemy_data.name,
            enemy_data.health,
            int(enemy_data.attackv),
            enemy_data.spell,
        )
        return True

    def play(s,player):
        s.begin(player)
        while s.current_enemy is not None and player.health > 0:
            s.take_turn(1)
