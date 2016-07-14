import pygame
import lcm

import time

from butterbotlcm import motor_t






size = 240, 240

pygame.init()
screen = pygame.display.set_mode(size)

spd = 0.0
direction = 0.0

lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=1")

leftMotor = 0
rightMotor = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); #sys.exit() if sys is imported
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            state = 0
            if event.type == pygame.KEYDOWN: state = 1

            if event.key == pygame.K_UP:
                spd = 70*state
            if event.key == pygame.K_DOWN:
                spd = -70*state
            if event.key == pygame.K_LEFT:
                direction = 50*state
            if event.key == pygame.K_RIGHT:
                direction = -50*state

            leftMotor = spd + direction
            rightMotor = spd - direction
            print("rightmotor: %d,  leftmotor: %d" % (leftMotor, rightMotor))

    msg = motor_t()
    msg.timestamp = int(time.time())
    msg.leftmotor = leftMotor
    msg.rightmotor = rightMotor
    lc.publish("BUTTERBOT", msg.encode())
    time.sleep(.5)
            

