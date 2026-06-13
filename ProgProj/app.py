from tkinter import *
from tkinter import font as tkFont
import sys
import os
import shutil
import ssl
import urllib.request
import zipfile
import tempfile
import filecmp


class RequirementsError(Exception):
    '''Missing required contents'''




syncerror=False
missingReq=False

required=['./py','./py/camp_edit.py','./py/game.py','./ATT/BACK.png']

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
    if str(e) == "<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Basic Constraints of CA cert not marked critical (_ssl.c:1032)>":
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
root=Tk()
root.title('POLYMORPHISM')
bgr=PhotoImage(file='./ATT/BACK.png')
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

hexv=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

def ls(a,f):
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

bbg='#0a0b0a'

bfg='#ff0000'

hoverc='#'
for c in range(len(bbg)):
    if bbg[c]=='#':
        pass
    else:
        nvi=ls(hexv,bbg[c])+int(ho[c])
        nv=hexv[nvi]
        hoverc+=nv

def deny(e):
    print('Nuh-uh')


def hover(e):
    e.widget['background']=hoverc
    e.widget['height']=2

def un_hover(e):
    e.widget['background']=bbg
    e.widget['height']=1


def close():
    root.destroy()
    import os
    os._exit(0)
def game():
    print('Play')
def camp():
    print('Campaign Editor')


def trigger_button_press(btn):
    btn.event_generate("<Enter>")
    btn.event_generate("<ButtonPress-1>")

def trigger_button_release(btn):
    btn.event_generate("<ButtonRelease-1>")
    btn.event_generate("<Leave>")


    
bwid=13
wid=w
gap=(wid-(3*bwid))/10
fx=gap/2
bx=gap/2

#Define Buttons

b1 = Button(root, text = 'Close',bd=0,activebackground=bab,activeforeground=baf,bg=bbg,fg=bfg,height=1,width=bwid,command = close,font=('BankGothic Lt BT', 12))
b2= Button(root, text = 'Play Game',bd=0,activebackground=bab,activeforeground=baf,bg=bbg,fg=bfg,height=1,width=bwid,command=game,font=('BankGothic Lt BT', 12))
b3= Button(root, text = 'Campaign Editor',activebackground=bab,activeforeground=baf,bd=0,bg=bbg,fg=bfg,height=1,width=bwid,command=camp,font=('BankGothic Lt BT', 12))
py=(300,0)
px=(fx,bx)

#Render Homescreeen

b1.pack(side = 'left',pady=py,padx=px)
b2.pack(side = 'left',pady=py,padx=px)
b3.pack(side = 'left',pady=py,padx=px)

# Custom Keyboard Shortcuts


# Play Game (key 1)
root.bind("<KeyPress-space>", lambda e: trigger_button_press(b2))
root.bind("<KeyRelease-space>", lambda e: trigger_button_release(b2))

# Close (key 2)
root.bind("<KeyPress-q>", lambda e: trigger_button_press(b1))
root.bind("<KeyRelease-q>", lambda e: trigger_button_release(b1))

# Campaign (key 3)
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

