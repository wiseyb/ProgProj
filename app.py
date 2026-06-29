from tkinter import *
from tkinter import font as tkFont
from collections import Counter
import sys
import os
import shutil
import ssl
import urllib.request
import zipfile
import tempfile
import filecmp


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

required=['./py','./py/camp_edit.py','./py/game.py',bgimagepath]

#Add local path /py to modules
sys.path.append('./py')

# Setup and creation of missing files
def drz(rurl,dzip):
    urllib.request.urlretrieve(rurl,dzip)

def extract(zpath,to):
    with zipfile.ZipFile(zpath,'r') as z:
        z.extractall(to)

def sync(local,repo,delete_ext=False):
    for root, dirs, files in os.walk(repo):
        rel=os.path.relpath(root,repo)
        local_eqv=os.path.join(local,rel)
        if not os.path.exists(local_eqv):
            os.makedirs(local_eqv)
        for f in files:
            repof=os.path.join(root,f)
            localf=os.path.join(local_eqv,f)
            if not os.path.exists(localf) or not filecmp.cmp(repof, localf, shallow=False):
                shutil.copy2(repof,localf)
                print("Updated:", os.path.relpath(localf, local))
        
        if delete_ext:
            for root, dirs, files in os.walk(local, topdown=False):
                rel = os.path.relpath(root, local)
                repo_eqv = os.path.join(repo, rel)
                if not os.path.exists(repo_eqv):
                    shutil.rmtree(root)
                    continue
                repofs=set(os.listdir(repo_eqv))
                localfs=set(os.listdir(root))
                for i in localfs-repofs:
                    p=os.path.join(root,i)
                    if os.path.isdir(p):
                        shutil.rmtree(p)
                    else:
                        os.remove(p)
                    print("Deleted:", os.path.relpath(p, local))
                    

local_dir='./'
gzip=("https://github.com/wiseyb/ProgProj/archive/refs/heads/main.zip")
try:
    with tempfile.TemporaryDirectory() as tmp:
        zpath=os.path.join(tmp,'repo.zip')
        print("Downloading GitHub repo…")
        drz(gzip,zpath)
        print("Extracting…")
        extract(zpath,tmp)
        

        repo_root = next(
                os.path.join(tmp, d)
                for d in os.listdir(tmp)
                if os.path.isdir(os.path.join(tmp, d))
            )

        print("Syncing...")
        sync(local_dir,repo_root,delete_ext=True)
except Exception as e:
    syncerror=True
    if "<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Basic Constraints of CA cert not marked critical (_ssl.c:" in str(e):
        exp='SSL certificate verification failed'
    else:
        exp=e
    print(f'''Error syncing project:  {exp}''')

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
def deny(e):
    print('Nuh-uh')


def hover(e):
    e.widget['background']=hoverc

def un_hover(e):
    e.widget['background']=bbg

def home():
    b1.configure(text = '''Close
[Q]''',bd=0,activebackground=bab,activeforeground=baf,bg=bbg,fg=bfg,height=2,width=bwid,command = close,font=('BankGothic Lt BT', 12))
    b2.configure(text = '''Play Game
[SPACE]''',bd=0,activebackground=bab,activeforeground=baf,bg=bbg,fg=bfg,height=2,width=bwid,command=game,font=('BankGothic Lt BT', 12))
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
    root.destroy()
    import os
    os._exit(0)
def game():
    bp.place_forget()
    t1.place_forget()
    t2.place_forget()
    b1.configure(text='''Home
[Q]''', command=home)
    b2.configure(text='''Attack
[SPACE]''')
    b3.configure(text='''Spell
[E]''')
    bf.place(relx=0.5, rely=0.7, anchor='center')
    b1.pack(side='left', padx=40)
    b2.pack(side='left', padx=40)
    b3.pack(side='left', padx=40)
def camp():
    print('Campaign Editor')


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

#Define Buttons

b1 = Button(bf, text = '''Close
[Q]''',bd=0,activebackground=bab,activeforeground=baf,bg=bbg,fg=bfg,height=2,width=bwid,command = close,font=('BankGothic Lt BT', 12))
b2= Button(bf, text = '''Play Game
[SPACE]''',bd=0,activebackground=bab,activeforeground=baf,bg=bbg,fg=bfg,height=2,width=bwid,command=game,font=('BankGothic Lt BT', 12))
b3= Button(bf, text = '''Campaign Editor
[E]''',activebackground=bab,activeforeground=baf,bd=0,bg=bbg,fg=bfg,height=2,width=bwid,command=camp,font=('BankGothic Lt BT', 12))
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


#Hover Bindings

b1.bind("<Enter>", hover)
b1.bind("<Leave>", un_hover)
b2.bind("<Enter>", hover)
b2.bind("<Leave>", un_hover)
b3.bind("<Enter>", hover)
b3.bind("<Leave>", un_hover)

#Render Window

root.mainloop()

