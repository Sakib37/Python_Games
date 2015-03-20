# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global memory_deck, exposed, clicked_index, turn_counter, state
    state = 0
    memory_deck = range(0, 8) * 2
    random.shuffle(memory_deck)
    turn_counter = 0
    COUNTER_LABEL = "Turns =" + str(turn_counter)
    exposed = [False] * 16
    clicked_index = []
     
# define event handlers
def mouseclick(pos):
    global state, clicked_index, exposed, turn_counter
    mouse_position = list (pos)
    exposed[mouse_position[0] // 50] = True
    clicked_index.append(mouse_position[0] // 50)
    if state == 0:
        state = 1 
        turn_counter += 1
    elif state == 1:
        state =2
        
    else:
        state = 1
        turn_counter += 1
        if (memory_deck[clicked_index[-2]]) != (memory_deck[clicked_index[-3]]):
            exposed[clicked_index[-2]] = False
            exposed[clicked_index[-3]] = False
            clicked_index = [clicked_index[-1]]           
                    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    NUM_POSITION = [5, 60]
    RECTANGLE_POINT1 = [0, 0]
    RECTANGLE_POINT2 = [(RECTANGLE_POINT1[0] + 50), 0]
    RECTANGLE_POINT3 = [(RECTANGLE_POINT1[0] + 50), 100]
    RECTANGLE_POINT4 = [RECTANGLE_POINT1[0], 100]
    label.set_text('Turns = '+ str(turn_counter))
    
# print mouse_position
    for idx, num in enumerate(memory_deck):
        if exposed[idx] == False:
            canvas.draw_polygon([RECTANGLE_POINT1, RECTANGLE_POINT2, RECTANGLE_POINT3, RECTANGLE_POINT4], 2, 'red', 'Green')
            NUM_POSITION[0] += 50
            RECTANGLE_POINT1[0] += 50 
            RECTANGLE_POINT2[0] = RECTANGLE_POINT1[0] + 50 
            RECTANGLE_POINT3[0] = RECTANGLE_POINT2[0] 
            RECTANGLE_POINT4[0] = RECTANGLE_POINT1[0]
        elif exposed[idx] == True:
            canvas.draw_text(str(num), NUM_POSITION, 50, 'Gray')
            NUM_POSITION[0] += 50
            RECTANGLE_POINT1[0] += 50 
            RECTANGLE_POINT2[0] = RECTANGLE_POINT1[0] + 50 
            RECTANGLE_POINT3[0] = RECTANGLE_POINT2[0] 
            RECTANGLE_POINT4[0] = RECTANGLE_POINT1[0]


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")



# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric