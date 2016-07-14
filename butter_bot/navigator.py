import lcm
from threading import Lock
from butterbotlcm import state_t
from butterbotlcm import tagpos_t
from butterbotlcm import motor_t

mutex = Lock()
lc = lcm.LCM()

def tag_handler(channel, data):
    msg = tagpos_t.decode(data)
    

def state_handler(channel, data):
    msg = state_t.decode(data)
    

def set_motors(left, right):
    msg = motor_t()
    msg.timestamp = int(time.time())
    msg.leftmotor = leftMotor
    msg.rightmotor = rightMotor
    lc.publish("BUTTERBOT_MOTOR", msg.encode())

def search_mode():
    set_motors(-40.0, 40.0)

def main():
    subscription = lc.subscribe("BUTTERBOT_TAG", tag_handler)
    subscription = lc.subscribe("BUTTERBOT_STATE", state_handler)
    try:
        while True:
            lc.handle()
    except KeyboardInterrupt:
        pass



if __name__ == "__main__":
    main()