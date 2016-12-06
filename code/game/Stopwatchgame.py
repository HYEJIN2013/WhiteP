#Stopwatch game for coursera project
#If you find this through a google search. Please don't just copy and paste. Get the logic and try to do it yourself. 

import simplegui
# global variables

ticks = 0
points = 0
tries = 0
display = "0:00.0"

# helper functions
def format(t):
    global display
    D = t % 10
    BC = int(t / 10) % 60
    A = int(t / 600)
    if (BC < 10):
        BC="0"+str(BC)
    display =  str(str(A) + ":" + str(BC) + "." + str(D))
    return display
    
# event handlers for buttons; "Start", "Stop", "Reset"
def start():    
    timer.is_running()
    timer.stop()
    timer.start()
                
def stop():
    global ticks, points, tries 
    if timer.is_running():
        timer.stop()
        if ticks % 10 == 0:
            points += 1
        else:
            tries += 1
def reset():
    global ticks, tries, points, display
    ticks = 0    
    points = 0
    tries = 0
    timer.stop()
    format(ticks)

# event handler for timer
def timer():
    global ticks
    ticks += 1
    format(ticks)
    
# draw handler
def draw_handler(canvas):
    global message, point, t
    canvas.draw_text(display, [10, 90], 80, "ff69b4", "sans-serif")    
    canvas.draw_text(str(points)+"/"+str(tries), [250,80], 40, "41A317", "sans-serif")
    canvas.draw_text("Points   Tries", [245, 42], 10, "white", "sans-serif")
    
# frame
frame = simplegui.create_frame("home", 330, 130)
frame.set_canvas_background("black")

# event handlers
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)
 
frame.set_draw_handler(draw_handler)
timer = simplegui.create_timer(100, timer)

frame.start()
