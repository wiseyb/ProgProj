from tkinter import *
from tkinter import font as tkFont, filedialog, messagebox, simpledialog
from collections import Counter
from random import randint as ri
import os, shutil, filecmp, ctypes, winreg, hashlib
try:
    import winsound
except:
    pass
# Project settings and configuration
with open('./DTA/conf/config.conf','r') as f:
    confFile=f.read().split('\n')
conf={}
for line in confFile:
    data=line.split(' ')
    conf[data[0].strip(':')]=float(data[1])

# General helpers for images and theme colors
def passf():
    pass

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def get_image_color(img, step=10, least_common=False):
    pixels = []
    for x in range(0, img.width(), step):
        for y in range(0, img.height(), step):
            pixels.append(img.get(x, y))
    colors = Counter(pixels).most_common()
    return rgb_to_hex(colors[-1 if least_common else 0][0])


def get_bg_color(img, step=10):
    return get_image_color(img, step)


def get_fg_color(img, step=10):
    return get_image_color(img, step, least_common=True)

# Keep widget colors synchronized when the background theme changes
def update_theme():
    for widget in [root, bf, cewf, inter, textf]:
        widget.configure(bg=bbg)
    for widget in [
        t1, t2, fileText, enNamLab, enHelLab, enAttLab, enSpeLab,
        cBoxLab, cQuantLab,
    ]:
        widget.configure(bg=bbg, fg=bfg)
    for widget in [enNam, enHel, enAtt, enSpe, cBox, cQuant, filep]:
        widget.configure(bg=bbg, fg=bfg, insertbackground=bfg)
    for widget in [b1, b2, b3, b8, enAdd, caAdd, Commit]:
        widget.configure(
            bg=bbg, fg=bfg, activebackground=bab, activeforeground=baf
        )


def apply_background(path, resize=False):
    global bgimagepath, bgimagename, bgr, bbg, bfg, bab, hoverc, ho
    bgimagepath, bgimagename = path, os.path.basename(path)
    bgr = PhotoImage(file=bgimagepath)
    bp.configure(image=bgr)
    bp.image = bgr
    bbg = get_bg_color(bgr)
    bfg = get_fg_color(bgr)
    bab = bfg
    ho, hoverc = get_hover_colors(bab, bbg)
    update_theme()
    if resize:
        width, height = bgr.width() + 400, bgr.height() + 50
        x = int((root.winfo_screenwidth() - width) / 2)
        y = int((root.winfo_screenheight() - height) / 2)
        root.geometry(f"{width}x{height}+{x}+{y}")
    root.update_idletasks()


def set_colour(col, event=None):
    apply_background(os.path.join(script_dir, "ATT", f"LOGO-NEW-{col}.png"), resize=True)


def random_col_path():
    bgcol = ('R', 'B', 'G', 'M', 'C')[ri(0, 4)]
    fbgimagename=f'LOGO-NEW-{bgcol}.png'
    return f'./ATT/{fbgimagename}',fbgimagename

def rand_col(event=None):
    _, bgimagename = random_col_path()
    apply_background(os.path.join(script_dir, "ATT", bgimagename))

# Use the app's folder as the base for its assets and data files
script_dir = os.path.abspath(os.path.dirname(__file__))
os.chdir(script_dir)
_, bgimagename = random_col_path()
bgimagepath = os.path.join(script_dir, 'ATT', bgimagename)

# Create the main window and prepare the bundled font for Tk

name='POLYMORPHISM'

root=Tk()
root.title(name)

def read_font_family(font_path):
    with open(font_path, "rb") as font_file:
        data = font_file.read()

    if len(data) < 12:
        raise ValueError("The font file is too small to contain a TrueType header.")

    table_count = int.from_bytes(data[4:6], "big")
    name_table = None
    for index in range(table_count):
        record_offset = 12 + index * 16
        if record_offset + 16 > len(data):
            raise ValueError("The font table directory is incomplete.")
        record = data[record_offset:record_offset + 16]
        if record[:4] == b"name":
            table_offset = int.from_bytes(record[8:12], "big")
            table_length = int.from_bytes(record[12:16], "big")
            if table_offset + table_length > len(data):
                raise ValueError("The font name table is incomplete.")
            name_table = data[table_offset:table_offset + table_length]
            break

    if name_table is None or len(name_table) < 6:
        raise ValueError("The font does not contain a valid name table.")

    record_count = int.from_bytes(name_table[2:4], "big")
    strings_offset = int.from_bytes(name_table[4:6], "big")
    candidates = []
    for index in range(record_count):
        record_offset = 6 + index * 12
        if record_offset + 12 > len(name_table):
            raise ValueError("The font name records are incomplete.")
        record = name_table[record_offset:record_offset + 12]
        platform_id = int.from_bytes(record[0:2], "big")
        language_id = int.from_bytes(record[4:6], "big")
        name_id = int.from_bytes(record[6:8], "big")
        value_length = int.from_bytes(record[8:10], "big")
        value_offset = int.from_bytes(record[10:12], "big")
        if name_id not in (1, 16):
            continue

        start = strings_offset + value_offset
        end = start + value_length
        if end > len(name_table):
            raise ValueError("A font family name extends beyond the name table.")
        if platform_id in (0, 3):
            value = name_table[start:end].decode("utf-16-be").strip("\0 ")
            platform_priority = 0 if platform_id == 3 else 1
        elif platform_id == 1:
            value = name_table[start:end].decode("mac_roman").strip("\0 ")
            platform_priority = 2
        else:
            continue

        if value:
            candidates.append((
                0 if name_id == 1 else 1,
                platform_priority,
                0 if language_id in (0, 0x0409) else 1,
                value,
            ))

    if not candidates:
        raise ValueError("The font does not declare a readable family name.")
    return min(candidates)[3]


def install_bundled_font():
    font_path = os.path.join(script_dir, "ATT", "font.ttf")
    if not os.path.isfile(font_path):
        print(f"Font file not found at {font_path}; using the fallback font.")
        return False

    try:
        fonts_dir = os.path.join(
            os.environ["LOCALAPPDATA"], "Microsoft", "Windows", "Fonts"
        )
        with open(font_path, "rb") as font_file:
            font_digest = hashlib.sha256(font_file.read()).hexdigest()[:16]
        font_basename, font_extension = os.path.splitext(os.path.basename(font_path))
        installed_path = os.path.join(
            fonts_dir, f"{font_basename}-{font_digest}{font_extension}"
        )
        font_family = read_font_family(font_path)
        registry_name = f"{font_family} (TrueType)"
        os.makedirs(fonts_dir, exist_ok=True)
        font_updated = not os.path.exists(installed_path)
        if font_updated:
            shutil.copy2(font_path, installed_path)
        elif not filecmp.cmp(font_path, installed_path, shallow=False):
            raise OSError(f"The installed font file is corrupted: {installed_path}")

        if not ctypes.windll.gdi32.AddFontResourceW(installed_path):
            raise OSError(f"Windows could not load the font at {installed_path}")

        with winreg.CreateKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows NT\CurrentVersion\Fonts",
        ) as fonts_key:
            winreg.SetValueEx(
                fonts_key, registry_name, 0, winreg.REG_SZ, installed_path
            )

        ctypes.windll.user32.SendMessageTimeoutW(
            0xFFFF, 0x001D, 0, 0, 0x0002, 5000, None
        )
        return font_family
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Could not install the bundled font; using the fallback font: {error}")
        return None


# Load the initial logo and create the app's shared font styles
fontname = install_bundled_font() or "Candara"
bgr=PhotoImage(file=bgimagepath)
ico=PhotoImage(file='./ATT/icon.png')
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
root.iconphoto(False, ico)
root.iconphoto(True, ico)
screen=0

standard_size=12
t1size=50
font=tkFont.Font(family=fontname, size=standard_size)
tfont=tkFont.Font(family=fontname, size=t1size)
t2font=tkFont.Font(family=fontname, size=int(t1size/2))

# Convert the logo's palette into base and hover colors
hexv=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
hchexv=['2','3','4','5','6','7','8','9','a','b','c','d','e','f']

def ls(a,f):
    return a.index(f) if f in a else 0
    

def get_hover_colors(foreground, background):
    modifier = '#'
    for color in foreground:
        if color == '#':
            continue
        index = ls(hchexv, color) - 10
        if index == -10:
            modifier += '0'
        else:
            modifier += hchexv[max(0, min(index, len(hchexv) - 1))]

    hover = '#'
    for index, color in enumerate(background):
        if color == '#':
            continue
        value = min(ls(hexv, color) + int(modifier[index]), 15)
        hover += hexv[value]
    return modifier, hover


bab=get_fg_color(bgr)

baf='#000'

bbg=get_bg_color(bgr)
bfg=get_fg_color(bgr)
ho, hoverc = get_hover_colors(bab, bbg)

# Campaign editor state and actions
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
    nm=enNam.get()
    name_valid = bool(nm)
    if nm=='':
        enNam.delete(0,END)
        enNam.insert(0,'Enter a name')
        nm=enNam.get()
    stats = [read_integer(entry) for entry in (enHel, enAtt, enSpe)]
    if name_valid and all(value is not None for value in stats):
        hl, at, sp = stats
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


def read_integer(entry):
    try:
        return int(entry.get())
    except ValueError:
        entry.delete(0, END)
        entry.insert(0, 'Enter a number')
        return None


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


# Game model and screen navigation
from class_sys import *

g=game_sys(conf)

def home():
    global screen
    screen = 0
    bind_button_key("space", b2)
    bind_button_key("q", b1)
    bind_button_key("e", b3)
    root.title(name)
    cewf.place_forget()
    t1.configure(text=name)
    t2.configure(text='Shape your own reality')
    bp.place(relx=0.5, rely=0.5, anchor='center')
    t1.place(relx=0.5, rely=0.5, anchor='center')
    t2.place(relx=0.5, rely=0.6, anchor='center')
    show_menu([
        (b1, {"text": "Close\n[Q]", "command": close}),
        (b2, {"text": "Play Game\n[SPACE]", "command": game_home}),
        (b3, {"text": "Campaign Editor\n[E]", "command": camp}),
    ], y=0.75, padx=30, reset_style=True)


def show_menu(buttons, y=0.7, padx=40, reset_style=False):
    for button, options in buttons:
        if reset_style:
            options.update(
                activebackground=bab, activeforeground=baf, bg=bbg, fg=bfg,
                height=2, width=bwid, font=font,
            )
        button.configure(**options)
        button.pack(side='left', padx=padx)
    bf.place(relx=0.5, rely=y, anchor='center')


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
player_file=''

def player_select():
    global screen
    screen = 3
    t1.configure(text=camp_type)
    t2.configure(text='Choose your Player')
    t2.place(relx=0.5, rely=0.5, anchor='center')
    show_menu([
        (b1, {"text": "Home\n[Q]", "command": home}),
        (b2, {"text": "New Player\n[SPACE]", "width": bwid + 5, "command": newp}),
        (b3, {"text": "Load Player\n[E]", "width": bwid + 5, "command": exip}),
    ])

def start_encounter():
    global screen
    screen = 4
    bind_button_key("e", b3)
    t1.configure(text=f'{p.name} vs {g.current_enemy.name}')
    t2.configure(text=f'{g.current_enemy.name}: {g.current_enemy.health} health | {p.name}: {p.health}')
    show_menu([
        (b1, {"text": "Home\n[Q]", "command": home}),
        (b2, {"text": "Melee Attack\n[SPACE]", "width": bwid + 5, "command": Mattack}),
        (b3, {"text": "Spell Attack\n[E]", "width": bwid + 5, "command": Sattack}),
    ])

def encounter_result(result):
    global screen
    screen = 5
    b3.pack_forget()
    if result == 'victory' and g.level_index < len(g.level):
        button_text, result_title, result_text, result_command = (
            "Continue\n[SPACE]", "Encounter Victory",
            f'{p.name} defeated {g.current_enemy.name}', continue_campaign,
        )
    elif result == 'victory':
        button_text, result_title, result_text, result_command = (
            "Play Again\n[SPACE]", "Campaign Complete",
            f'{p.name} defeated every enemy', game_home,
        )
    else:
        button_text, result_title, result_text, result_command = (
            "Try Again\n[SPACE]", "Encounter Defeat",
            f'{p.name} was defeated by {g.current_enemy.name}', game_home,
        )
        g.remove_player(player_file)
    t1.configure(text=result_title)
    t2.configure(text=result_text)
    show_menu([
        (b1, {"text": "Home\n[Q]", "command": home}),
        (b2, {"text": button_text, "width": bwid + 5, "command": result_command}),
    ])
    bind_button_key("space", b2)
    bind_button_key("e")

def continue_campaign():
    if g.next_encounter():
        start_encounter()

def combat_action(action):
    result=g.take_turn(action)
    if player_file:
        g.save_player(player_file)
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
    g.begin(p)
    start_encounter()
    


def default_camp():
    global camp_type
    camp_type='Default Campaign'
    g.load('camp/DEFAULT/game')
    g.prep()
    player_select()


def choose_data_file(initialdir, title, filetypes, extension, blocked=()):
    while True:
        path = filedialog.askopenfilename(
            initialdir=initialdir, title=title, filetypes=filetypes
        )
        if not path:
            return ""
        if not path.lower().endswith(extension):
            messagebox.showerror("Invalid File", f"Please select a valid {extension} file.")
            continue
        if any(path.find(token) > 0 for token in blocked):
            messagebox.showerror(
                "Invalid File Location",
                f"Please select a file from the /{os.path.basename(initialdir)} location only.",
            )
            continue
        return path


def custom_camp():
    global camp_type
    camp_type='Custom Campaign'
    file_path = choose_data_file(
        "./DTA/camp", "Select Campaign File",
        (("Game Data Files", "*.gmdta"), ("All Files", "*.*")),
        ".gmdta", ("TMPLT", "DEFAULT"),
    )
    if not file_path:
        return
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    g.load(f'camp/{file_name}')
    g.prep()
    player_select()

def newp():
    global p
    global player_file
    name = simpledialog.askstring("New Player", "Enter your player's name:")
    p=player(name,conf=conf)
    player_file=f'chr/{name}'
    play_game()

def exip():
    global p
    global player_file
    file_path = choose_data_file(
        "./DTA/chr", "Select Player File",
        (("Player Data Files", "*.chrdta"), ("All Files", "*.*")),
        ".chrdta", ("TMPLT",),
    )
    if not file_path:
        return
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    g.load_player(f'chr/{file_name}')
    p=g.player
    player_file=f'chr/{file_name}'
    play_game()

def game_home():
    global screen
    screen = 1
    bp.place_forget()
    t1.configure(text='Select Campaign')
    t1.place(relx=0.5, rely=0.4, anchor='center')
    t2.place_forget()
    show_menu([
        (b1, {"text": "Home\n[Q]", "command": home}),
        (b2, {"text": "Play Default Campaign\n[SPACE]", "width": bwid + 5, "command": default_camp}),
        (b3, {"text": "Play Custom Campaign\n[E]", "width": bwid + 5, "command": custom_camp}),
    ])

def camp():
    global screen
    screen = 2
    bind_button_key("space")
    bind_button_key("q", b8)
    bind_button_key("e")
    root.title('Campaign Editor')

    for w in [bp, t1, t2, bf, b1, b2, b3]:
        w.place_forget()
        w.pack_forget()

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


def make_button(parent, text, command, **options):
    return Button(
        parent, text=text, command=command, activebackground=bab,
        activeforeground=baf, bg=bbg, fg=bfg, font=font, **options,
    )


def bind_button_key(key, button=None):
    if button is None:
        press = release = lambda event: passf()
    else:
        press = lambda event: trigger_button_press(button)
        release = lambda event: trigger_button_release(button)
    root.bind(f"<KeyPress-{key}>", press)
    root.bind(f"<KeyRelease-{key}>", release)


# Build the shared title labels, screen frames, and campaign editor controls
t1=Label(root,text=name,fg=bfg,bg=bbg,font=tfont)
t2=Label(root,text='Shape your own reality',fg=bfg,bg=bbg,font=t2font)


# Size the menu buttons using the current window width
bwid=20
wid=w
gap=(wid-(3*bwid))/10
fx=gap/2
bx=gap/2


bf=Frame(root,bg=bbg)
cewf=Frame(root,bg=bbg)

# Create common menu buttons and campaign editor widgets
b1 = make_button(bf, "Close\n[Q]", close, height=2, width=bwid)
b2 = make_button(bf, "Play Game\n[SPACE]", game_home, height=2, width=bwid)
b3 = make_button(bf, "Campaign Editor\n[E]", camp, height=2, width=bwid)

inter=Frame(cewf,bg=bbg)
inter.pack(side='left', padx=100)
textf=Frame(cewf,bg=bbg)
textf.pack(side='right')
fileText=Label(textf,width=50,text=file,bg=bbg,fg=bfg,font=font)
fileText.pack(padx=10, pady=10)
eBox=Frame(inter,bg=bbg)
eBox.pack(padx=10, pady=10)

def add_entry(parent, label, width=10, row=False):
    container = Frame(parent, bg=bbg) if row else parent
    if row:
        container.pack()
    label_widget = Label(container, text=label, bg=bbg, fg=bfg, font=font)
    entry_widget = Entry(
        container, width=width, bg=bbg, fg=bfg, font=font, insertbackground=bfg
    )
    label_widget.pack(side='left', padx=2, pady=2 if row else 0)
    entry_widget.pack(
        side='right' if row else 'left', padx=2, pady=2 if row else 10
    )
    return label_widget, entry_widget


enNamLab, enNam = add_entry(eBox, "Name:", row=True)
enHelLab, enHel = add_entry(eBox, "Health:", row=True)
enAttLab, enAtt = add_entry(eBox, "Attack:", row=True)
enSpeLab, enSpe = add_entry(eBox, "Spell Attack:", row=True)

enAdd=make_button(eBox, "Add", eAdd, bd=0)
enAdd.pack(padx=2, pady=2)
cBoxCont=Frame(inter,bg=bbg)
cBoxCont.pack()

cQuantLab, cQuant = add_entry(cBoxCont, "Quantity:", 2)
cBoxLab, cBox = add_entry(cBoxCont, "Name:")
caAdd=make_button(inter, "Add", cAdd, bd=0)
caAdd.pack(padx=2, pady=2)
filep=Entry(inter,bg=bbg,fg=bfg,font=font,insertbackground=bfg)
filep.pack(pady=10)
Commit=make_button(inter, "Commit to file", lambda: commit(), bd=0)
Commit.pack(padx=10, pady=10)
b8=make_button(inter, "Home\n[Q]", home, bd=0, height=2, width=bwid)
b8.pack(side='top', pady=40)




py=(0,40)
px=(fx,bx)

# Show the initial home screen and apply its default palette
home()
set_colour("D")

# Keyboard shortcuts for navigation, palette selection, and fullscreen
# Escape (esc key)
root.bind('<Escape>', lambda e: esc())

#Change Colour
root.bind('<Control-Shift-Return>',rand_col)
for color in "RGBCMD":
    root.bind(f"<Control-Shift-{color}>", lambda event, color=color: set_colour(color))

# Fullscreen indicator border
border_size = 5

border_top = Frame(root, bd=0, highlightthickness=0)
border_bottom = Frame(root, bd=0, highlightthickness=0)
border_left = Frame(root, bd=0, highlightthickness=0)
border_right = Frame(root, bd=0, highlightthickness=0)

def show_fullscreen_border(event=None):
    border_top.configure(bg=bfg)
    border_bottom.configure(bg=bfg)
    border_left.configure(bg=bfg)
    border_right.configure(bg=bfg)

    border_top.place(x=0, y=0, relwidth=1, height=border_size)
    border_bottom.place(relx=0, rely=1, anchor="sw",
                        relwidth=1, height=border_size)
    border_left.place(x=0, y=0, width=border_size, relheight=1)
    border_right.place(relx=1, y=0, anchor="ne",
                       width=border_size, relheight=1)


def hide_fullscreen_border_and_toggle(event=None):
    for b in (border_top, border_bottom, border_left, border_right):
        b.place_forget()

    current = root.attributes("-fullscreen")
    root.attributes("-fullscreen", not current)
    
# F11
root.bind("<KeyPress-F11>", show_fullscreen_border)
root.bind("<KeyRelease-F11>", hide_fullscreen_border_and_toggle)

# Ctrl+Alt+Enter
root.bind("<Control-KeyPress-Return>", show_fullscreen_border)
root.bind("<Control-Alt-KeyRelease-Return>", hide_fullscreen_border_and_toggle)

# Add hover feedback to clickable controls, then start the Tk event loop
for widget in [b1, b2, b3, Commit, caAdd, enAdd, b8]:
    widget.bind("<Enter>", hover)
    widget.bind("<Leave>", un_hover)

#Render Window
root.attributes("-fullscreen", True)
try:
    winsound.PlaySound('./ATT/intro2.wav', winsound.SND_FILENAME)
except:
    pass
root.mainloop()
