from tkinter import *
from random import randint as ri


hs=Tk()
sides=['top','left','bottom','right']
dim='400x400+0+0'
hs.geometry(dim)

def change():
    s=ri(0,3)
    b.pack(side=sides[s],pady=(25,25),padx=(25,25))


b=Button(hs,text='Button',bg='red',command=change,width=27,height=12)
b.pack(side='top',pady=(25,25),padx=(25,25))

hs.mainloop()
