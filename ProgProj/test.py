import sys
sys.path.append('./py')
from window_build import App

def hi():
    print('hi')
def hi2():
    print('hi2')

app=App('Hi',bgimage='./ATT/baa.png')

app.addButton(hi,'Button1',100,300,w=20,h=2)
app.addButton(hi2,'Button2',300,300,w=20,h=2)
app.addButton(app.stop,'Button3',500,300,w=20,h=2)
app.addLabel('Label 1',100,100)
print(app.buttons)

app.addEntry(90,90)
print(app.widgets)
