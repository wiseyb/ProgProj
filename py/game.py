from tkinter import *

class char():
    def __init__(s):
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
