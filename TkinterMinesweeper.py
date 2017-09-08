import tkinter as tk
import random

"""
=--Python Tkinter Minesweeper--=

-A janky beginner project by Matt Hansen-
July 2017
  The dream has always been to create Minesweeper.
    This is my first attempt at it, and it works sorta.
    The main issue, if there still aren't restart/flag buttons,
    is that when revealing large fields of safe tiles
        (eg 20x40 map with only 10 bombs)
    causes recursion errors and ends up doing some weird stuff.
    Got a few ideas on fixing that but nothing solid yet.

"""

root = tk.Tk()
root.wm_title("Minesweeper")
root.resizable(width=False, height=False)

main_frame = tk.Frame()
main_frame.pack(side=tk.BOTTOM)

frame = tk.Frame(main_frame)
frame.pack(side=tk.BOTTOM)
frame.grid(row=0,column=0)


global counter
global grid_height
global grid_width
global bombs
global flags_placed

counter = 0
grid_height = 20
grid_width = 20
bombs = 50
flags_placed=0

b = [] # b is the array of buttons, which will display their relational location in b_grid
b_grid = [] # b_grid is the array of tile values
bomb_locations = [] # holds bomb locations for quick finding
checked_tiles = [] # holds checked tiles
unchecked_tiles = []
debug_mode=True
global flag_mode
flag_mode =False

def debug(*args):
    if debug_mode==True:
        for i in args: print(i)

def init_values():
    global bombs
    global grid_height
    global grid_width
    global flags_placed
    
    flags_placed = 0
    flag_button.configure(text='Flag: {}'.format(flags_placed))
                            
    a = bomb_entry.get()
    b = height_entry.get()
    c = width_entry.get()
    try:
        a = int(a)
    except ValueError:
        a = 50
    try:
        b = int(b)
    except ValueError:
        b = 20
    try:
        c = int(c)
    except ValueError:
        c = 20
    grid_height = b
    grid_width = c
    if a < b*c:
        bombs = a
    else:
        bombs=int((b*c)/4)

def init_grid():
    # initialize array and fill with 0
    debug(' init_grid')
    del b_grid[:]
    del checked_tiles[:]
    for i in range(grid_height):
        b_grid.append([])
        for j in range(grid_width):
            b_grid[i].append(0)
    debug('  grid successfully initialized',
          '  height {}  width {}'.format(grid_height, grid_width), '  {} parent lists'.format(len(b_grid)))
          

def init_unchecked_tiles():
    debug(' init_unchecked_tiles')
    del unchecked_tiles[:]
    for i in range(grid_height):
        for j in range(grid_width):
            unchecked_tiles.append('{},{}'.format(i,j))
    debug('  unchecked array initialized', '  size: {}'.format(len(unchecked_tiles)))
        
def init_bombs(num):
    # place bombs into b_grid
    debug(' init_bombs({})'.format(num))
    del bomb_locations[:]
    b = num
    while b != 0:
        ranY = random.randint(0, grid_height-1)
        ranX = random.randint(0, grid_width-1)
##        print(ranY)
##        print(ranX)
        if b_grid[ranY][ranX]!=9:
            b_grid[ranY][ranX] = 9
            bomb_locations.append('{},{}'.format(ranY, ranX))
            b -= 1

def checkbomb(locY, locX):
    # used by count_near_bombs
    # checks for bomb in tile [locY][locX] and returns 1 to be counted into the parent tile
    return 1*(b_grid[locY][locX]==9)


def do_thing_nearby(thing, locY, locX):
##    debug('doing {} at {},{}'.format(thing, locY, locX))
    if locY > 0:
        thing(locY-1, locX)
        if locX > 0:
            thing(locY-1, locX-1)       
        if locX < grid_width-1:
            thing(locY-1, locX+1)                
    if locY < grid_height-1:
        thing(locY+1, locX)
        if locX > 0:
            thing(locY+1, locX-1)
        if locX < grid_width-1:
            thing(locY+1, locX+1)               
    if locX > 0:
        thing(locY, locX-1)
    if locX < grid_width-1:
        thing(locY, locX+1) 

def count_near_bombs(locY, locX):
    if b_grid[locY][locX]==0:
        count = 0
        if locY > 0:
            count+=checkbomb(locY-1, locX)
            if locX > 0:
                count+=checkbomb(locY-1, locX-1)       
            if locX < grid_width-1:
                count+=checkbomb(locY-1, locX+1)                
        if locY < grid_height-1:
            count+=checkbomb(locY+1, locX)
            if locX > 0:
                count+=checkbomb(locY+1, locX-1)
            if locX < grid_width-1:
                count+=checkbomb(locY+1, locX+1)               
        if locX > 0:
            count+=checkbomb(locY, locX-1)
        if locX < grid_width-1:
            count+=checkbomb(locY, locX+1)   
        b_grid[locY][locX] = count
        
def init_near_bombs():
    for i in bomb_locations:
        locY = int(i.split(',')[0])
        locX = int(i.split(',')[1])
        do_thing_nearby(count_near_bombs, locY, locX)

def write_location(y, x):
    if b_grid[y][x] == 9:
        return 'X'
    elif b_grid[y][x] == 0:
        return ' '
    else:
        return b_grid[y][x]


def check_pressed(y,x):
    tile_coord = '{},{}'.format(y,x)
    if tile_coord not in checked_tiles or tile_coord in unchecked_tiles:
        return True

##def number_colorizer(location, ground):
    # colorize foreground/disabledforeground
    

def tile_wizard(y, x):
    global counter
    global flags_placed
    tile_coord = '{},{}'.format(y,x)
##    b[y][x].config(text=str(counter))
    counter = counter + 1
    if tile_coord not in checked_tiles:
        if flag_mode==False:
            checked_tiles.append(tile_coord)
            unchecked_tiles.remove(tile_coord)
            b[y][x].configure(state='disabled')
            if b_grid[y][x]==9:
                print("GAME OVER")
                b[y][x].config(bg='red', text='x', fg='black', disabledforeground='black')
                big_button.config(text='RIP', bg='orange')
    ##            for i in range(grid_height):  UNCOMMENT THIS TO DISPLAY ALL MAP WHEN TILE IS HIT
    ##                for j in range(grid_width):
    ##                    tile_wizard(i,j)
            elif b_grid[y][x]<9 and b_grid[y][x]!=0:
                b[y][x].config(text='{}'.format(write_location(y,x)))
                b[y][x].config(relief='sunken')
                b[y][x].config(bg='light grey')
                if b_grid[y][x]==1:
                    b[y][x].config(fg='blue', disabledforeground='blue')
                elif b_grid[y][x]==2:
                    b[y][x].config(fg='green', disabledforeground='green')
                elif b_grid[y][x]==3:
                    b[y][x].config(fg='red', disabledforeground='red')
                elif b_grid[y][x]==4:
                    b[y][x].config(fg='purple', disabledforeground='purple')
                elif b_grid[y][x]==5:
                    b[y][x].config(fg='black', disabledforeground='black')
                elif b_grid[y][x]==6:
                    b[y][x].config(fg='cyan', disabledforeground='cyan')
                elif b_grid[y][x]==7:
                    b[y][x].config(fg='yellow', disabledforeground='yellow')
                elif b_grid[y][x]==8:
                    b[y][x].config(fg='orange', disabledforeground='orange')               
            elif b_grid[y][x]==0:
                b[y][x].config(relief='sunken')
                b[y][x].config(bg='light grey')
                do_thing_nearby(tile_wizard, y, x)
                
        else:
            if b[y][x].cget('text')=='':
                b[y][x].configure(bg='paleturquoise1', text='?', fg='black')
                flags_placed+=1
                flag_button.configure(text='Flag: {}'.format(flags_placed))
            else:
                b[y][x].configure(bg='white smoke', text='')
                flags_placed-=1
                flag_button.configure(text='Flag: {}'.format(flags_placed))
def display_grid():
    del b[:]
    for x in frame.grid_slaves():
        x.destroy()
    for i in range(grid_height):
        b.append([])
        for j in range(grid_width):
            b[i].append(tk.Button(frame, text='', font='fixedsys', bd=1, width=2, height=1, command=lambda y=i, x=j: tile_wizard(y,x))) # font=("Courier", 12)
            b[i][j].grid(column=j,row=i+10)
    

def update_map():
    for i in range(grid_height):
        for j in range(grid_width):
            b[i][j].config(text='{}'.format(write_location(i,j)))

def main():
    debug('main')
    big_button.configure(state='disabled')
    init_values()
    init_grid()
    init_unchecked_tiles()
    init_bombs(bombs)
    display_grid()
    init_near_bombs()
    big_button.config(text=': )', bg='yellow', state='normal')

def toggle_flag():
    global flag_mode
    flag_mode = not flag_mode
    if flag_mode==True:
        flag_button.config(bg='paleturquoise1')
    else:
        flag_button.config(bg='white smoke')

big_button = tk.Button(text=": )", width=4, height=2, command=main)
big_button.pack(side='right')

restart_label = tk.Label(text='NEW->')
restart_label.pack(side='right')

flag_button = tk.Button(text='Flag: {} '.format(flags_placed), width=5, height=2, command=toggle_flag)
flag_button.pack(side='left')

bomb_label = tk.Label(text='Bombs')
bomb_label.pack(side='left')

bomb_entry = tk.Entry(width=3)
bomb_entry.pack(side='left')
bomb_entry.insert(0, '50')

height_label = tk.Label(text='Height')
height_label.pack(side='left')

height_entry = tk.Entry(width=2)
height_entry.pack(side='left')
height_entry.insert(0, '20')

width_label = tk.Label(text='Width')
width_label.pack(side='left')

width_entry = tk.Entry(width=2)
width_entry.pack(side='left')
width_entry.insert(0, '20')

##init_grid()
##init_bombs(bombs)
##display_grid()  
##init_near_bombs()
##init_unchecked_tiles()
main()
root.mainloop()
