
from tkinter import *

class App(Tk):
    def __init__(s,name,height=800,width=600,bgimage='./path/to/image.png'):
        from tkinter import PhotoImage
        image=False
        super().__init__()
        s.title(name)
        s.configure(background='black')
        s.widgets=[]
        s.buttons=0
        if bgimage != './path/to/image.png':
            image=True
            s.bgr=PhotoImage(file=bgimage)
            w=s.bgr.width()
            h=s.bgr.height()
        else:
            w=width
            h=height
        ws=s.winfo_screenwidth()
        hs=s.winfo_screenheight()
        x=int((ws/2)-(w/2))
        y=int((hs/2)-(h/2))
        s.dim=f'{w}x{h}+{x}+{y}'
        s.geometry(s.dim)
        if image:
            l1=Label(s,image=s.bgr)
            l1.place(x=-2,y=-2)
            s.widgets.append(l1)
    def addButton(s,command,text,x,y,w=-1,h=-1):
        if w==-1 and h==-1:
            temp=Button(s,text=text,command=command)
        elif w==-1:
            temp=Button(s,text=text,command=command,height=h)
        elif h==-1:
            temp=Button(s,text=text,command=command,width=w)
        else:
            temp=Button(s,text=text,command=command,height=h,width=w)
        temp.place(x=x,y=y)
        s.buttons+=1
        s.widgets.append(temp)
    def stop(s):
        s.destroy
        import os
        os._exit(0)
    def clear(s,e):
        e.widget.delete(0,END)
    def addLabel(s,text,x,y):
        temp=Label(s,text=text)
        temp.place(x=x,y=y)
        s.widgets.append(temp)
    def addEntry(s,x,y,DefText='Enter Text'):
        temp=Entry(s)
        temp.place(x=x,y=y)
        temp.insert(10,DefText)
        temp.bind('<FocusIn>',s.clear)
        s.widgets.append(temp)
    def addMessage(s,text,x,y):
        temp=Message(s,text=text)
        temp.place(x=x,y=y)
        s.widgets.append(temp)
    def addCheck(s):
        pass
    def addRadio(s,options,x,y):
        pass
    def addMenu(s):
        pass
    def addCombo(s):
        pass
    def addList(s):
        pass
    def addMenuButton(s):
        pass
    def addCanvas(s):
        pass
    def addScale(s):
        pass
   
    def duplicate(s, widgetList):
        # Create new window with same geometry
        new = App(
            name=s.title(),
            width=s.winfo_width(),
            height=s.winfo_height()
        )

        for w in widgetList:
            info = w.place_info()  # x, y, width, height
            x = int(info.get("x", 0))
            y = int(info.get("y", 0))
            width = int(info.get("width", -1)) if info.get("width") else -1
            height = int(info.get("height", -1)) if info.get("height") else -1

            if isinstance(w, Label):
                new_label = Label(
                    new,
                    text=w.cget("text"),
                    bg=w.cget("bg"),
                    fg=w.cget("fg"),
                    font=w.cget("font"),
                    image=w.cget("image")
                )
                new_label.place(x=x, y=y)

                new.widgets.append(new_label)

            elif isinstance(w, Button):
                new_button = Button(
                    new,
                    text=w.cget("text"),
                    command=w.cget("command"),
                    width=w.cget("width"),
                    height=w.cget("height")
                )
                new_button.place(x=x, y=y)

                new.widgets.append(new_button)

            elif isinstance(w, Entry):
                new_entry = Entry(
                    new,
                    width=w.cget("width"),
                    font=w.cget("font")
                )
                new_entry.place(x=x, y=y)
                new_entry.insert(0, w.get())
                new_entry.bind("<FocusIn>", new.clear)

                new.widgets.append(new_entry)

        return new

        
        
            
