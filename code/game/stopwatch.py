# "Stopwatch: The Game"
import simplegui
# define global variables
milis = 0
minutes = 0
seconds = 0
attempts = 0
success = 0
time = 0
run_timer = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def change_format(value):
    value_string = str(value)
    if value < 10:
        return "0" + value_string
    else:
        return value_string

def format(time):
    global milis,seconds,minutes
    milis = time % 10
    time = time / 10
    seconds = time % 60
    minutes = time / 60
    milis_string = str(milis)
    minutes_string = str(minutes)
    seconds_string = change_format(seconds)
    return minutes_string + ":" + seconds_string + "." + milis_string
    


# define event handlers for buttons; "Start", "Stop", "Reset"

def start1():
    global run_timer 
    if not run_timer:
        run_timer = 1
        timer.start()
	
def stop1():
    global run_timer,attempts,success
    if run_timer:
        run_timer = 0
        timer.stop()
        if not time % 10:
            success += 1
        attempts +=1
    
def reset1():
    global run_timer, time,attempts,success
    time = 0
    run_timer = 0
    attempts = 0
    success = 0
    
# define event handler for timer with 0.1 sec interval

def timer1():
    global time,run_timer
    if run_timer:
        time = time + 1
    if time == 5999:
        timer.stop()
    if time > 5999:
        reset1()
		
# define draw handler
        
def result():
    global attempts,success
    return str(success) + "/" + str(attempts)

def draw(canvas):
    global time
    canvas.draw_text(format(time),[150,200],50,"Red")
    canvas.draw_text("success/attempts" + "    " + result(),[90,50],22,"Yellow")
    
# create frame
frame=simplegui.create_frame("StopWatch",450,250)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button("Start",start1,100)
frame.add_button("Stop",stop1,100)
frame.add_button("Reset",reset1,100)
timer = simplegui.create_timer(100,timer1)
# start frame
frame.start()
