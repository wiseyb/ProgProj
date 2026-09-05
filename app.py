from tkinter import *
from tkinter import font as tkFont
from tkinter import filedialog,messagebox
from collections import Counter
import sys
import os
import shutil
import ssl
import urllib.request
import zipfile
import tempfile
import filecmp

PROTECTED_PATHS = {".git", ".github", "__pycache__", ".venv"}

DEV_MODE = False  # Set True to prevent git syncing

def is_protected_path(path):
    normalized = os.path.normcase(os.path.normpath(path))
    parts = [part for part in normalized.split(os.sep) if part and part not in {".", ".."}]
    return any(part in PROTECTED_PATHS for part in parts)


def passf():
    pass

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def get_bg_color(img, step=10):
    pixels = []

    width = img.width()
    height = img.height()

    for x in range(0, width, step):
        for y in range(0, height, step):
            pixels.append(img.get(x, y))  # returns (r, g, b)

    most_common = Counter(pixels).most_common(1)[0][0]
    return rgb_to_hex(most_common)



class RequirementsError(Exception):
    '''Missing required contents'''


bgimagepath='./ATT/LOGO-NEW.png'

syncerror=False
missingReq=False

required=[bgimagepath]

#Add local path /py to modules

# Setup and creation of missing files
def drz(rurl,dzip):
    urllib.request.urlretrieve(rurl,dzip)

def extract(zpath,to):
    with zipfile.ZipFile(zpath,'r') as z:
        z.extractall(to)

def sync(local, repo, delete_ext=False):
    local = os.path.abspath(local)
    repo = os.path.abspath(repo)

    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if not is_protected_path(os.path.join(root, d))]
        rel = os.path.relpath(root, repo)
        local_eqv = os.path.join(local, rel)
        os.makedirs(local_eqv, exist_ok=True)

        for f in files:
            repof = os.path.join(root, f)
            if is_protected_path(repof):
                continue
            localf = os.path.join(local_eqv, f)
            if not os.path.exists(localf) or not filecmp.cmp(repof, localf, shallow=False):
                shutil.copy2(repof, localf)
                print("Updated:", os.path.relpath(localf, local))

        if delete_ext:
            for current_root, current_dirs, current_files in os.walk(local, topdown=False):
                current_dirs[:] = [d for d in current_dirs if not is_protected_path(os.path.join(current_root, d))]
                rel = os.path.relpath(current_root, local)
                repo_eqv = os.path.join(repo, rel)
                if is_protected_path(current_root):
                    continue
                if not os.path.exists(repo_eqv):
                    if os.path.isdir(current_root) and not os.path.islink(current_root):
                        shutil.rmtree(current_root)
                    else:
                        os.remove(current_root)
                    continue
                repofs = set(os.listdir(repo_eqv))
                localfs = set(os.listdir(current_root))
                for i in localfs - repofs:
                    p = os.path.join(current_root, i)
                    if is_protected_path(p):
                        continue
                    if os.path.isdir(p):
                        shutil.rmtree(p)
                    else:
                        os.remove(p)
                    print("Deleted:", os.path.relpath(p, local))


script_dir = os.path.abspath(os.path.dirname(__file__))
os.chdir(script_dir)
local_dir = script_dir
bgimagepath = os.path.join(script_dir, 'ATT', 'LOGO-NEW.png')
required = [bgimagepath]
gzip = ("https://github.com/wiseyb/ProgProj/archive/refs/heads/main.zip")
if not DEV_MODE:
    try:
        with tempfile.TemporaryDirectory() as tmp:
            zpath = os.path.join(tmp, 'repo.zip')
            print("Downloading GitHub repo…")
            drz(gzip, zpath)
            print("Extracting…")
            extract(zpath, tmp)

            repo_candidates = [
                os.path.join(tmp, d)
                for d in os.listdir(tmp)
                if os.path.isdir(os.path.join(tmp, d))
            ]
            repo_root = next((p for p in repo_candidates if os.path.isdir(os.path.join(p, '.git'))), repo_candidates[0] if repo_candidates else None)
            if repo_root is None:
                raise FileNotFoundError("Downloaded repo contents were not found")

            print("Syncing...")
            sync(local_dir, repo_root, delete_ext=True)
    except Exception as e:
        syncerror = True
        if "<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Basic Constraints of CA cert not marked critical (_ssl.c:" in str(e):
            exp = 'SSL certificate verification failed'
        else:
            exp = e
        print(f'''Error syncing project:  {exp}''')
else:
    print("DEV MODE enabled. Skipping Git sync.")
for el in required:
    if not os.path.exists(el):
        missingReq=True
        break


if syncerror and missingReq:
    raise RequirementsError("Program is missing required data and cannot sync with remote storage")

if syncerror:
    for p in required:
        if not os.path.exists(p):
            fpath=os.path.abspath(p)
            print(f'''Required data is not present.
Path: {fpath}
Quitting...''')
            import os
            os._exit(0)
        
#Init window

name='POLYMORPHISM'

root=Tk()
root.title(name)
bgr=PhotoImage(file=bgimagepath)
w=bgr.width()+400
h=bgr.height()+50
ws=root.winfo_screenwidth()
hs=root.winfo_screenheight()
x=int((ws/2)-(w/2))
y=int((hs/2)-(h/2))
dim=f'{w}x{h}+{x}+{y}'
root.geometry(dim)
root.configure(bg=get_bg_color(bgr))
bp=Label(root,image=bgr,bd=0)
screen=0


#determine hover colours for buttons

hexv=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

def ls(a,f): # Linear search algorithm
    found=False
    for i in range(len(a)):
        if a[i]==f:
            found=True
            break
    if found:
        return i
    else:
        return 0
    
bab='#990000'

baf='#000'

ho='#350000'

bbg=get_bg_color(bgr)

bfg='#ff0000'

hoverc='#'
for c in range(len(bbg)):
    if bbg[c]=='#':
        pass
    else:
        nvi=ls(hexv,bbg[c])+int(ho[c])
        nv=hexv[nvi]
        hoverc+=nv


# Functions requrired for buttons and keybinds
global campDTA
global fn
fn=''
campDTA=''
global ciV
ciV=''
global eiV
eiV=''
global file
global filesv
filesv=StringVar()
with open('./DTA/camp/TMPLT/blank.gmdta','r') as f:
    t=str(f.read())
    filesv.set(t)
    file=t
def commit():
    global campDTA
    campDTA=file.format(eny=eiV,camp=ciV)
    fn=filep.get()
    path=f'./DTA/camp/{fn}.gmdta'
    with open(path,'w') as f:
        f.write(campDTA)
        print('Write')
        filep.delete(0, END)
    with open(path,'r') as r:
        print(r.read())
    
def eAdd():
    global ciV
    global eiV
    global file
    name=True
    nm=enNam.get()
    if nm=='':
        enNam.delete(0,END)
        enNam.insert(0,'Enter a name')
        nm=enNam.get()
        name=False
    try:
        hl=int(enHel.get())
        health=True
    except:
        enHel.delete(0,END)
        enHel.insert(0,'Enter a number')
        health=False
    try:
        at=int(enAtt.get())
        attack=True
    except:
        enAtt.delete(0,END)
        enAtt.insert(0,'Enter a number')
        attack=False
    try:
        sp=int(enSpe.get())
        spell=True
    except:
        enSpe.delete(0,END)
        enSpe.insert(0,'Enter a number')
        spell=False
    if name and health and attack and spell:
        dta=f'''{nm} {hl} {at} {sp}
'''
        eiV+=dta
        fileText.configure(text=file.format(eny=eiV,camp=ciV))
        campDTA=file.format(eny=eiV,camp=ciV)       
        enNam.delete(0, END)
        enHel.delete(0, END)
        enAtt.delete(0, END)
        enSpe.delete(0, END)

        print(campDTA)

def cAdd():
    global ciV
    global eiV
    global file
    q=cQuant.get()
    nm=cBox.get()
    dta=f'''{q} {nm}
'''
    ciV+=dta
    fileText.configure(text=file.format(eny=eiV,camp=ciV))
    campDTA=file.format(eny=eiV,camp=ciV)    
    cQuant.delete(0, END)
    cBox.delete(0, END)
    print(campDTA)

def deny(e):
    print('Nuh-uh')


def hover(e):
    e.widget['background']=hoverc

def un_hover(e):
    e.widget['background']=bbg



#Class system imported from class

from class_sys import *

g=game_sys()

#Window configs

def home():
    global screen
    screen = 0
    root.bind("<KeyPress-space>", lambda e: trigger_button_press(b2))
    root.bind("<KeyRelease-space>", lambda e: trigger_button_release(b2))
    root.bind("<KeyPress-q>", lambda e: trigger_button_press(b1))
    root.bind("<KeyRelease-q>", lambda e: trigger_button_release(b1))
    root.bind("<KeyPress-e>", lambda e: trigger_button_press(b3))
    root.bind("<KeyRelease-e>", lambda e: trigger_button_release(b3))
    root.title(name)
    cewf.place_forget()
    t1.configure(text=name)
    t2.configure(text='Shape your own reality')
    b1.configure(text = '''Close
[Q]''',bd=0,activebackground=bab,activeforeground=baf,bg=bbg,fg=bfg,height=2,width=bwid,command = close,font=('BankGothic Lt BT', 12))
    b2.configure(text = '''Play Game
[SPACE]''',bd=0,activebackground=bab,activeforeground=baf,bg=bbg,fg=bfg,height=2,width=bwid,command=game_home,font=('BankGothic Lt BT', 12))
    b3.configure(text = '''Campaign Editor
[E]''',activebackground=bab,activeforeground=baf,bd=0,bg=bbg,fg=bfg,height=2,width=bwid,command=camp,font=('BankGothic Lt BT', 12))
    bp.place(relx=0.5, rely=0.5, anchor='center')
    t1.place(relx=0.5, rely=0.5, anchor='center')
    t2.place(relx=0.5, rely=0.6, anchor='center')
    bf.place(relx=0.5, rely=0.75, anchor='center')
    b1.pack(side='left', padx=30)
    b2.pack(side='left', padx=30)
    b3.pack(side='left', padx=30)
def close():
    print('''


------------------------------------
------------------------------------
          WINDOW CLOSED
------------------------------------
------------------------------------


''')
    root.destroy()
    import os
    os._exit(0)

camp_type=''

def player_select():
    global screen
    screen = 3
    t1.configure(text=camp_type)
    t2.configure(text='Choose your Player')
    t2.place(relx=0.5, rely=0.5, anchor='center')
    b3.pack_forget()
    b1.configure(text='''Home
    [Q]''', command=home)
    b2.configure(text='''New Player
    [SPACE]''',width=bwid+5,command=newp)
    bf.place(relx=0.5, rely=0.7, anchor='center')
    b1.pack(side='left', padx=40)
    b2.pack(side='left', padx=40)

def start_encounter():
    global screen
    screen = 4
    t1.configure(text=f'{p.name} vs {g.current_enemy.name}')
    t2.configure(text=f'{g.current_enemy.name}: {g.current_enemy.health} health | {p.name}: {p.health}')
    b1.configure(text='''Home
    [Q]''', command=home)
    b2.configure(text='''Melee Attack
    [SPACE]''',width=bwid+5,command=Mattack)
    b3.configure(text='''Spell Attack
    [E]''',width=bwid+5,command=Sattack)
    bf.place(relx=0.5, rely=0.7, anchor='center')
    b1.pack(side='left', padx=40)
    b2.pack(side='left', padx=40)
    b3.pack(side='left', padx=40)

def encounter_result(result):
    global screen
    screen = 5
    b3.pack_forget()
    b1.configure(text='''Home
    [Q]''', command=home)
    if result == 'victory' and g.level_index < len(g.level):
        b2.configure(text='''Continue
    [SPACE]''', width=bwid+5, command=continue_campaign)
        t1.configure(text='Encounter Victory')
        t2.configure(text=f'{p.name} defeated {g.current_enemy.name}')
    elif result == 'victory':
        b2.configure(text='''Play Again
    [SPACE]''', width=bwid+5, command=game_home)
        t1.configure(text='Campaign Complete')
        t2.configure(text=f'{p.name} defeated every enemy')
    else:
        b2.configure(text='''Try Again
    [SPACE]''', width=bwid+5, command=game_home)
        t1.configure(text='Encounter Defeat')
        t2.configure(text=f'{p.name} was defeated by {g.current_enemy.name}')
    root.bind("<KeyPress-space>", lambda e: trigger_button_press(b2))
    root.bind("<KeyRelease-space>", lambda e: trigger_button_release(b2))
    root.bind("<KeyPress-e>", lambda e: passf())
    root.bind("<KeyRelease-e>", lambda e: passf())
    bf.place(relx=0.5, rely=0.7, anchor='center')
    b1.pack(side='left', padx=40)
    b2.pack(side='left', padx=40)

def continue_campaign():
    if g.next_encounter():
        start_encounter()

def combat_action(action):
    result=g.take_turn(action)
    if result == 'continue':
        t1.configure(text=f'{p.name} vs {g.current_enemy.name}')
        t2.configure(text=f'{g.current_enemy.name}: {g.current_enemy.health} health | {p.name}: {p.health} health')
    elif result == 'victory':
        encounter_result(result)
    elif result == 'defeat':
        encounter_result(result)

def Mattack():
    combat_action(1)

def Sattack():
    combat_action(2)

def play_game():
    print('Game Start')
    g.begin(p)
    start_encounter()
    


def default_camp():
    global camp_type
    camp_type='Default Campaign'
    g.load('camp/game')
    g.prep()
    player_select()


def custom_camp():
    global camp_type
    camp_type='Custom Campaign'
    file_path = filedialog.askopenfilename(initialdir="./DTA/camp", title="Select Campaign File", filetypes=(("Game Data Files", "*.gmdta"), ("All Files", "*.*")))
    while file_path and not file_path.lower().endswith('.gmdta'):
        messagebox.showerror("Invalid File", "Please select a valid .gmdta file.")
        file_path = filedialog.askopenfilename(initialdir="./DTA/camp", title="Select Campaign File", filetypes=(("Game Data Files", "*.gmdta"), ("All Files", "*.*")))
    if not file_path:
        return
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    g.load(f'camp/{file_name}')
    g.prep()
    player_select()


def newp():
    global p
    p=player('Player')
    play_game()


def game_home():
    global screen
    screen = 1
    bp.place_forget()
    t1.configure(text='Select Campaign')
    t1.place(relx=0.5, rely=0.4, anchor='center')
    t2.place_forget()
    b1.configure(text='''Home
[Q]''', command=home)
    b2.configure(text='''Play Default Campaign
[SPACE]''',width=bwid+5,command=default_camp)
    b3.configure(text='''Play Custom Campaign
[E]''',width=bwid+5,command=custom_camp)
    bf.place(relx=0.5, rely=0.7, anchor='center')
    b1.pack(side='left', padx=40)
    b2.pack(side='left', padx=40)
    b3.pack(side='left', padx=40)

def camp():
    global screen
    screen = 2
    root.bind("<KeyPress-space>", lambda e: passf())
    root.bind("<KeyRelease-space>", lambda e:  passf())
    root.bind("<KeyPress-q>", lambda e: trigger_button_press(b8))
    root.bind("<KeyRelease-q>", lambda e: trigger_button_release(b8))
    root.bind("<KeyPress-e>", lambda e: passf())
    root.bind("<KeyRelease-e>", lambda e: passf())
    root.title('Campaign Editor')
    bp.place_forget()
    t1.place_forget()
    t2.place_forget()
    bf.place_forget()
    b1.pack_forget()
    b2.pack_forget()
    b3.pack_forget()

    cewf.place(relx=0.5, rely=0.5, anchor='center')
    
def esc():
    global screen
    if screen == 0:
        close()
    else:
        home()

def trigger_button_press(btn):
    btn.event_generate("<Enter>")
    btn.event_generate("<ButtonPress-1>")

def trigger_button_release(btn):
    btn.event_generate("<ButtonRelease-1>")
    btn.event_generate("<Leave>")



#Define Labels
t1=Label(root,text=name,fg=bfg,bg=bbg,font=('BankGothic Lt BT', 40))
t2=Label(root,text='Shape your own reality',fg=bfg,bg=bbg,font=('BankGothic Lt BT', 20))


#Determine button widths and padding
    
bwid=13
wid=w
gap=(wid-(3*bwid))/10
fx=gap/2
bx=gap/2


bf=Frame(root,bg=bbg)
cewf=Frame(root,bg=bbg)

#Define Elements and set initial appearance

b1 = Button(bf, text = '''Close
[Q]''',bd=0,activebackground=bab,activeforeground=baf,bg=bbg,fg=bfg,height=2,width=bwid,command = close,font=('BankGothic Lt BT', 12))

b2= Button(bf, text = '''Play Game
[SPACE]''',bd=0,activebackground=bab,activeforeground=baf,bg=bbg,fg=bfg,height=2,width=bwid,command=game_home,font=('BankGothic Lt BT', 12))

b3= Button(bf, text = '''Campaign Editor
[E]''',activebackground=bab,activeforeground=baf,bd=0,bg=bbg,fg=bfg,height=2,width=bwid,command=camp,font=('BankGothic Lt BT', 12))

inter=Frame(cewf,bg=bbg)
inter.pack(side='left', padx=100)
textf=Frame(cewf,bg=bbg)
textf.pack(side='right')
fileText=Label(textf,width=50,text=file,bg=bbg,fg=bfg,font=('BankGothic Lt BT', 12))
fileText.pack(padx=10, pady=10)
eBox=Frame(inter,bg=bbg)
eBox.pack(padx=10, pady=10)
enNamCont=Frame(eBox,bg=bbg)
enHelCont=Frame(eBox,bg=bbg)
enAttCont=Frame(eBox,bg=bbg)
enSpeCont=Frame(eBox,bg=bbg)
enNamCont.pack()
enHelCont.pack()
enAttCont.pack()
enSpeCont.pack()
enNamLab=Label(enNamCont,text="Name:",bg=bbg,fg=bfg,font=('BankGothic Lt BT', 12))
enNam=Entry(enNamCont,width=10,bg=bbg,fg=bfg,font=('BankGothic Lt BT', 12),insertbackground=bfg)
enHelLab=Label(enHelCont,text="Health:",bg=bbg,fg=bfg,font=('BankGothic Lt BT', 12))
enHel=Entry(enHelCont,width=10,bg=bbg,fg=bfg,font=('BankGothic Lt BT', 12),insertbackground=bfg)
enAttLab=Label(enAttCont,text="Attack:",bg=bbg,fg=bfg,font=('BankGothic Lt BT', 12))
enAtt=Entry(enAttCont,width=10,bg=bbg,fg=bfg,font=('BankGothic Lt BT', 12),insertbackground=bfg)
enSpeLab=Label(enSpeCont,text="Spell Attack:",bg=bbg,fg=bfg,font=('BankGothic Lt BT', 12))
enSpe=Entry(enSpeCont,width=10,bg=bbg,fg=bfg,font=('BankGothic Lt BT', 12),insertbackground=bfg)
enNamLab.pack(side = 'left',padx=2, pady=2)
enNam.pack(side = 'right',padx=2, pady=2)
enHelLab.pack(side = 'left',padx=2, pady=2)
enHel.pack(side = 'right',padx=2, pady=2)
enAttLab.pack(side = 'left',padx=2, pady=2)
enAtt.pack(side = 'right',padx=2, pady=2)
enSpeLab.pack(side = 'left',padx=2, pady=2)
enSpe.pack(side = 'right',padx=2, pady=2)
enAdd=Button(eBox,text='Add',command=eAdd,bd=0,activebackground=bab,activeforeground=baf,bg=bbg,fg=bfg,font=('BankGothic Lt BT', 12))
enAdd.pack(padx=2, pady=2)
cBoxCont=Frame(inter,bg=bbg)
cBoxCont.pack()
cQuant=Entry(cBoxCont,width=2,bg=bbg,fg=bfg,font=('BankGothic Lt BT', 12),insertbackground=bfg)
cQuantLab=Label(cBoxCont,text='Quantity:',bg=bbg,fg=bfg,font=('BankGothic Lt BT', 12))
cQuantLab.pack(side='left')
cQuant.pack(side='left',padx=2, pady=10)
cBox=Entry(cBoxCont,width=10,bg=bbg,fg=bfg,font=('BankGothic Lt BT', 12),insertbackground=bfg)
cBoxLab=Label(cBoxCont,text='Name:',bg=bbg,fg=bfg,font=('BankGothic Lt BT', 12))
cBoxLab.pack(side='left')
cBox.pack(side='left',padx=2, pady=10)
caAdd=Button(inter,text='Add',command=cAdd,bd=0,activebackground=bab,activeforeground=baf,bg=bbg,fg=bfg,font=('BankGothic Lt BT', 12))
caAdd.pack(padx=2, pady=2)
filep=Entry(inter,bg=bbg,fg=bfg,font=('BankGothic Lt BT', 12),insertbackground=bfg)
filep.pack(pady=10)
Commit=Button(inter,text='Commit to file',command=lambda: commit(),bd=0,activebackground=bab,activeforeground=baf,bg=bbg,fg=bfg,font=('BankGothic Lt BT', 12))
Commit.pack(padx=10, pady=10)
b8= Button(inter,text='''Home
[Q]''', command=home,activebackground=bab,activeforeground=baf,bd=0,bg=bbg,fg=bfg,height=2,width=bwid,font=('BankGothic Lt BT', 12))
b8.pack(side='top', pady=40)




py=(0,40)
px=(fx,bx)

#Render Homescreeen
home()


# Custom Keyboard Shortcuts


# Play Game (space key)
root.bind("<KeyPress-space>", lambda e: trigger_button_press(b2))
root.bind("<KeyRelease-space>", lambda e: trigger_button_release(b2))

# Close (q key)
root.bind("<KeyPress-q>", lambda e: trigger_button_press(b1))
root.bind("<KeyRelease-q>", lambda e: trigger_button_release(b1))

# Campaign (e key)
root.bind("<KeyPress-e>", lambda e: trigger_button_press(b3))
root.bind("<KeyRelease-e>", lambda e: trigger_button_release(b3))

# Escape (esc key)
root.bind('<Escape>', lambda e: esc())


#Hover Bindings

b1.bind("<Enter>", hover)
b1.bind("<Leave>", un_hover)
b2.bind("<Enter>", hover)
b2.bind("<Leave>", un_hover)
b3.bind("<Enter>", hover)
b3.bind("<Leave>", un_hover)
Commit.bind("<Enter>", hover)
Commit.bind("<Leave>", un_hover)
caAdd.bind("<Enter>", hover)
caAdd.bind("<Leave>", un_hover)
enAdd.bind("<Enter>", hover)
enAdd.bind("<Leave>", un_hover)
b8.bind("<Enter>", hover)
b8.bind("<Leave>", un_hover)
#Render Window

root.mainloop()

