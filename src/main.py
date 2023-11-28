# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()
global mode
mode = 10
"""drive Motors + Remote"""
motor_11 = Motor(Ports.PORT11, GearSetting.RATIO_6_1, True)
motor_12 = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False)
motor_13 = Motor(Ports.PORT13, GearSetting.RATIO_6_1, False)
controller_1 = Controller(PRIMARY)
motor_18 = Motor(Ports.PORT18, GearSetting.RATIO_6_1, False)
motor_19 = Motor(Ports.PORT19, GearSetting.RATIO_6_1, True)
motor_20 = Motor(Ports.PORT20, GearSetting.RATIO_6_1, True)

rightside = MotorGroup(motor_11, motor_12, motor_13)
leftside = MotorGroup(motor_18, motor_19, motor_20)

"""Extra Motors"""
motor_15 = Motor(Ports.PORT15, GearSetting.RATIO_6_1, True)
motor_16 = Motor(Ports.PORT16, GearSetting.RATIO_6_1, False)
intake = MotorGroup(motor_15, motor_16)
wings = DigitalOut(brain.three_wire_port.a)

"""init"""
intake.set_velocity(100, PERCENT)
rightside.set_velocity(100, PERCENT)
leftside.set_velocity(100, PERCENT)

# Begin project code
# Create callback functions for each controller button event
def onStart():
    controller_1.screen.print("Carter Mode?")
    if controller_1.buttonA.pressing():
         mode = 1
    if controller_1.buttonB.pressing():
        mode = 2
def controller_L1_Pressed():
    pass

def controller_L2_Pressed():
    pass


def controller_R1_Pressed():
    pass

def controller_R2_Pressed():
    pass

# Create Controller callback events - 15 msec delay to ensure events get registered
controller_1.buttonL1.pressed(controller_L1_Pressed)
controller_1.buttonL2.pressed(controller_L2_Pressed)
controller_1.buttonR1.pressed(controller_R1_Pressed)
controller_1.buttonR2.pressed(controller_R2_Pressed)
wait(15, MSEC)
onStart()
# Configure Arm and Claw motor hold settings and velocity


# Main Controller loop to set motors to controller axis postiions
while True:
    if controller_1.buttonL2.pressing():
        wings.set(True)
    else:
        wings.set(False)
    if controller_1.buttonL1.pressing():
        intake.spin(FORWARD)
    else:
        intake.stop()

    rightside.spin(FORWARD)
    leftside.spin(FORWARD)
    if mode == 2:
        rightside.set_velocity(controller_1.axis2.position(), PERCENT)
        leftside.set_velocity(controller_1.axis3.position(), PERCENT)
    if mode == 1:
        rightside.set_velocity((controller_1.axis3.position() - controller_1.axis4.position()), PERCENT)
        leftside.set_velocity((controller_1.axis3.position() + controller_1.axis4.position()), PERCENT)


        
