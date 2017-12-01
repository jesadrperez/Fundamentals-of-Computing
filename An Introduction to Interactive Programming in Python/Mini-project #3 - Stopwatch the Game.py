# "Stopwatch: The Game"
# http://www.codeskulptor.org/#user42_v6YWA8YXcT_10.py

import simplegui

# define global variables
count = 0
sucess = 0
attempts = 0
running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(count):    
    deci_second = str(count % 10)
    second = str((count // 10) % 10)
    tenths_second = str((count // 100) % 6)
    minute = str(count // 600)
    return minute+':'+tenths_second+second+':'+deci_second   
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button():
    global running
    
    running = True
    timer.start()
    
def stop_button():
    global sucess
    global attempts
    global running
    
    timer.stop()
    if (count % 10 == 0) and (running):
        sucess += 1
    if running:        
        attempts += 1
    running = False
    
def reset_button():
    global sucess
    global attempts
    global count
    global running
    
    count = 0
    sucess = 0
    attempts = 0
    running = False

# define event handler for timer with 0.1 sec interval
def tick():
    global count
    count += 1

# define draw handler
def display(canvas):
    disp = format(count)
    canvas.draw_text(disp, (10, 90), 72, 'White')
    score = str(sucess)+"/"+str(attempts)
    canvas.draw_text(score, (150, 25), 24, 'Green')
    
# create frame
frame = simplegui.create_frame('Stopwatch', 200, 110)

# register event handlers
frame.set_draw_handler(display)
frame.add_button('Start', start_button)
frame.add_button('Stop', stop_button)
frame.add_button('Reset', reset_button)
timer = simplegui.create_timer(100, tick)

# start frame
frame.start()

# Please remember to review the grading rubric