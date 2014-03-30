import pyglet
import random
from pyglet.gl import *
from pyglet.window import key as keys

WIDTH = 500
HEIGHT = 500

rows = 100
columns = 100

RUNNING = False

cell_width  = float(WIDTH) / rows
cell_height = float(HEIGHT) / columns

INITAL_POPULATION = 10
ACTIVE_TILE_INDEX = 0

STATE = []


win = pyglet.window.Window(width=WIDTH, height=HEIGHT)

# A probably unecessary initial attempt at creating a clean little api for checking keyboard state
class Keyboard:
    def __init__(self):
        self.storage = {
            keys.UP: False,
            keys.DOWN: False,
            keys.LEFT: False,
            keys.RIGHT: False,
            keys.SPACE: False,
            keys.ENTER: False
        }
        
    def up(self):
        if self.storage[keys.UP]:
            return True

    def down(self):
        if self.storage[keys.DOWN]:
            return True
            
    def left(self):
        if self.storage[keys.LEFT]:
            return True

    def right(self):
        if self.storage[keys.RIGHT]:
            return True
            
    def enter(self):
        if self.storage[keys.ENTER]:
            return True

keyboard = Keyboard()

def reset_state():
    global STATE, INITAL_POPULATION
    STATE = []
    last_i = 0
    pop = 0

    for i in range(rows * columns):
        STATE.append(0)
        if random.randint(0, 300) < 50 and pop <= INITAL_POPULATION:
            pop += 1
            STATE.append(1)
        else:
            STATE.append(0)

 
@win.event
def on_draw():
    global ACTIVE_TILE_INDEX

    glClear(GL_COLOR_BUFFER_BIT)
    
    x = (WIDTH / 2) - (cell_width / 2)
    y = (HEIGHT / 2) - (cell_height / 2)

    i = 0
    tau = 0
    
    for j, row in enumerate(STATE):
        if j % rows == 0:
            i += 1
            tau = 0

        if STATE[j] == 1:
            y = cell_height * i
            x = cell_width * tau
            
            verts = (
                x, y,
                x, y + cell_height,
                x + cell_width, y + cell_height,
                x + cell_width, y
            )
            
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', verts))
        
        tau += 1

def neighbor_count(i):
    global STATE
    
    row = (i - (i % rows)) / rows
    
    top_left = (i + rows) - 1
    mid_left = (i + rows)
    top_right = (i + rows) + 1
    left = (i - 1) # + (row * rows)
    right = (i + 1) #+ (row * rows)
    bot_left = (i - rows) - 1
    bot_mid = (i - rows)
    bot_right  = (i - rows) + 1

    to_check = [
     top_left, mid_left, top_right,
     left, right,
     bot_left, bot_mid, bot_right
    ]
 
    alive = STATE[i] == 1
    num_alive = 0

    for cell in to_check:
        try:
            if STATE[cell] == 1: num_alive += 1
        except: pass
            
    return num_alive

@win.event
def on_mouse_motion(x, y, dx, dy):
    global ACTIVE_TILE_INDEX

    row    = int(y / float(cell_height)) - 1 # TODO: Why subtract 1?
    column = int(x / float(cell_width))
    i = (row * rows) + column
    ACTIVE_TILE_INDEX = i
    
    print 'cell %d has %d live neighbors' % (i, neighbor_count(ACTIVE_TILE_INDEX))
    

@win.event
def on_mouse_press(x, y, dx, dy):
    global STATE
    val = STATE[ACTIVE_TILE_INDEX]
    if val == 1:
        new = 0
    else:
        new = 1

    STATE[ACTIVE_TILE_INDEX] = new

@win.event
def on_key_press(sym, mod):
    keyboard.storage[sym] = True
    global RUNNING

    if sym == keys.ENTER and not RUNNING:
        print 'STARTING THE Game'
        RUNNING = True

    elif sym == keys.ENTER and RUNNING:
        print 'STOPPING THE GAME'
        RUNNING = False

    if sym == 111: # r
        print '~~~~~~~~~~~~~~~~~~'
        print 'LOL RESTTING'
        reset_state()
        
    
@win.event
def on_key_release(sym, mod):
    keyboard.storage[sym] = False

gen = 1

def update(dt):
    global gen, RUNNING, STATE
    
    next_generation = list(STATE)
    
    if not RUNNING: return
    
    for i, cell in enumerate(STATE):
        row = (i - (i % rows)) / rows

        alive = cell == 1
        num_alive = neighbor_count(i)
        
        if alive:
            if num_alive < 2:
                next_generation[i] = 0
            if num_alive == 2 or num_alive == 3:
                next_generation[i] = 1
            if num_alive > 3:
                next_generation[i] = 0
        elif num_alive == 3:
            next_generation[i] = 1

    gen += 1
    print 'computed generation %d in %f seconds' % (gen, dt)
    STATE = next_generation

def main():
    glColor3f(1.0, 1.0, 0)

    reset_state()
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()
    

if __name__ == '__main__':
    main()