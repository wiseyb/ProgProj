from tkinter import *
from tkinter import font as tkFont
import sys
import os

#Add local path /py to modules
sys.path.append('./py')

destination_path  = str(os.path.dirname(os.path.abspath(__file__)))
clone_command = "git clone https://github.com/wiseyb/ProgProj.git" 

clone_with_path = clone_command  +" "+ destination_path
os.system(clone_with_path)

### Setup and creation of missing files
##dta='./DTA'
##config='./DTA/conf'
##camp='./DTA/camp'
##defconf='./DTA/conf/config.conf'
##defcamp='./DTA/camp/game.gmdta'
##cdata='''__map__
##1,1,1,1,1,1,1 1,0,0,0,0,0,1 1,0,0,0,0,0,1 1,0,0,0,0,0,1 1,0,0,0,0,0,1 1,0,0,0,0,0,1 1,1,1,1,1,1,1
##__enemy__
##Drakuseth 2500 50 75
##Hellkite 1250 25 37
##Dragon 750 20 30
##Mage 600 11 40
##Whelp 500 15 25
##Hatchling 400 12 20
##Dragonrider 300 10 17
##Egg 200 7 15
##Shaman 100 5 10
##Goblin 50 5 10
##__level__
##5 Goblin
##3 Shaman
##1 Egg
##1 Goblin'''
##
##if not os.path.exists(dta):
##    os.mkdir(dta)
##if not os.path.exists(config):
##    os.mkdir(config)
##if not os.path.exists(camp):
##    os.mkdir(camp)
##
##if not os.path.exists(defconf):
##    with open(defconf,'w')as f:
##        data='''campaign:
##[DATA]
##speed:
##[DATA]'''
##        f.write(data)
##if not os.path.exists(defcamp):
##    with open(defcamp,'w')as f:
##        f.write(cdata)
##else:
##    f=open(defcamp,'r')
##    c=f.read()
##    f.close()
##    if c != cdata:
##        f=open(defcamp,'w')
##        f.write(cdata)
##        f.close()

        
#Init window
root=Tk()
root.title('GAME')
bgr=PhotoImage(file='./ATT/LOGO.png')
w=bgr.width()
h=bgr.height()
ws=root.winfo_screenwidth()
hs=root.winfo_screenheight()
x=int((ws/2)-(w/2))
y=int((hs/2)-(h/2))
dim=f'{w}x{h}+{x}+{y}'
root.geometry(dim)
l1=Label(root,image=bgr)
l1.place(x=-2,y=-2)


def hover(e):
    e.widget['background']='#B10606'
    e.widget['height']=3

def un_hover(e):
    e.widget['background']='#8A0303'
    e.widget['height']=2


def close():
    root.destroy
    import os
    os._exit(0)
def play():
    print('Play')

def camp():
    print('Campaign Editor')
bwid=18
wid=w
gap=(wid-(3*bwid))/10
fx=gap/2
bx=gap/2


cls = Button(root, text = 'Close',bg='#8A0303',fg='#F5F2E7',height=2,width=bwid,command = close,font=('BankGothic Lt BT', 12))
ply= Button(root, text = 'Play Game',bg='#8A0303',fg='#F5F2E7',height=2,width=bwid,command=play,font=('BankGothic Lt BT', 12))
lm= Button(root, text = 'Campaign Editor',bg='#8A0303',fg='#F5F2E7',height=2,width=bwid,command=camp,font=('BankGothic Lt BT', 12))
py=(600,0)
px=(fx,bx)
cls.pack(side = 'left',pady=py,padx=px)
ply.pack(side = 'left',pady=py,padx=px)
lm.pack(side = 'left',pady=py,padx=px)
cls.bind("<Enter>", hover)
cls.bind("<Leave>", un_hover)
ply.bind("<Enter>", hover)
ply.bind("<Leave>", un_hover)
lm.bind("<Enter>", hover)
lm.bind("<Leave>", un_hover)
root.mainloop()

