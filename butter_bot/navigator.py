from threading import Lock
import threading
import time

import lcm
from butterbotlcm import state_t
from butterbotlcm import tagpos_t
from butterbotlcm import motor_t
from butterbotlcm import navstate_t

from find_butter import Tagpos

from pid import PID

mutex = Lock()
lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=1")


"""
possible states:
idle
startsearch
search
move
grab
return
existential
"""

state = "idle"
lastTag = Tagpos()
pd = PID(1.0, 0, 0.5)

def tag_handler(channel, data):
    msg = tagpos_t.decode(data)
    with mutex:
        lastTag.timestamp = msg.timestamp
        lastTag.dist      = msg.dist
        lastTag.x         = msg.x
        lastTag.y         = msg.y
        lastTag.z         = msg.z
    

def state_handler(channel, data):
    msg = state_t.decode(data)
    global state
    with mutex:
        state_in = msg.state
        if state_in == "get_butter":
            state = "startsearch"
        elif state == "idle":
            state = "idle"
    
def update_state(newState):
    global state
    state = newState
    msg = navstate_t()
    msg.timestamp = int(time.time())
    msg.state = newState
    lc.publish("BUTTERBOT_NAVSTATE", msg.encode())

def set_motors(left, right):
    msg = motor_t()
    msg.timestamp = int(time.time())
    msg.leftmotor = left
    msg.rightmotor = right
    lc.publish("BUTTERBOT_MOTOR", msg.encode())

def start_search_mode():
    set_motors(-20.0, 20.0)

def stop_motors():
    set_motors(0.0, 0.0)

def panic():
    set_motors(50.0, 50.0)

def navigate_to_tag():
    newval = pd.update(lastTag.x, 0)
    spd = 20.0
    left = spd + newval
    right = spd - newval
    set_motors(left, right)

returnStart = 0.0

def handle_states():
    global state
    with mutex:
        if state == "idle":
            stop_motors()
            pass
        elif state == "startsearch":
            start_search_mode()
            state = "search"
            print("state now", state)
        elif state == "search":
            curtime = int(time.time())
            if curtime - lastTag.timestamp < 3:
                stop_motors()
                state = "move"
                print("state now", state)
        elif state == "move":
            navigate_to_tag()
            if lastTag.dist < .10:
                state = "grab"
                print("state now", state)
            if (time.time() - lastTag.timestamp) > 5:
                start_search_mode()
        elif state == "grab":
            state = "return"
            print("state now", state)
            global returnStart 
            returnStart = time.time()
        elif state == "return":
            set_motors(-20, -20)
            if (time.time() - returnStart) > 8:
                state = "idle"
                print("state now", state)
            
        elif state == "existential":
            panic()
            pass

def main():
    subscription = lc.subscribe("BUTTERBOT_TAG", tag_handler)
    subscription = lc.subscribe("BUTTERBOT_STATE", state_handler)
    print("navigator starting")
    try:
        while True:
            lc.handle_timeout(100)
            handle_states()

    except KeyboardInterrupt:
        pass



if __name__ == "__main__":
    main()