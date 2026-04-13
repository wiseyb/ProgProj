from tkinter import *
from tkinter import font as tkFont
import sys
import os
import shutil
import urllib.request
import zipfile
import tempfile
import filecmp

####TESTING TESTING 123


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

