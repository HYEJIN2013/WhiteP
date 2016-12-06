# template for "Stopwatch: The Game"
import simplegui

# define global variables
time = 0
interval = 100
running = False
stops = 0
stops_on_point = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    tenths = t % 10
    t = t // 20
    seconds = t % 60
    t = t // 60
    minutes = t
    return "%d:%02d.%d" % (minutes, seconds, tenths)

def start():
    if not timer.is_running():
        global running
        timer.start()
        running = True
        print "Timer started!"
    
def stop():
    if timer.is_running():
        global time, running, stops, stops_on_point
        timer.stop()
        running = False
        stops = stops + 1
        
        if format(time)[-1:] == "0":
            print "Stopped on Point!"
            stops_on_point += 1
        
        print "Timer has been stopped."

def reset():
    global time, running, stops, stops_on_point
    time = 0
    stops = 0
    stops_on_point = 0
    timer.stop()
    running = False
    print "Timer has been reset."

# define event handler for timer with 0.1 sec interval
def tick():
    global time
    time = time + 1
    print time

# define draw handler
def draw(canvas):
    global time, stops, stops_on_point
    canvas.draw_text(format(time), [75, 100], 50, "Red")
    canvas.draw_text(str(stops_on_point), [230, 25], 20, "Red")
    canvas.draw_text("/", [255, 25], 20, "Red")
    canvas.draw_text(str(stops), [275, 25], 20, "Red")
    
# create frame
f = simplegui.create_frame("Timer", 300, 250)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
f.add_button("Start", start, 200)
f.add_button("Stop", stop, 200)
f.add_button("Reset", reset, 200)

# register event handlers
f.set_draw_handler(draw)
timer = simplegui.create_timer(interval, tick)

# start frame
f.start()
timer.stop()

# Please remember to review the grading rubric
