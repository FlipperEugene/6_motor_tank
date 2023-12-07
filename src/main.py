# Library imports
from vex import *
import math
# Brain should be defined by default
brain=Brain()

mode = 3
log_directory = "/logs/"
"""drive Motors + Remote"""
motor_11 = Motor(Ports.PORT11, GearSetting.RATIO_6_1, True)
motor_12 = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False)
motor_13 = Motor(Ports.PORT13, GearSetting.RATIO_6_1, False)
controller_1 = Controller(PRIMARY)
motor_18 = Motor(Ports.PORT18, GearSetting.RATIO_6_1, False)
motor_19 = Motor(Ports.PORT19, GearSetting.RATIO_6_1, True)
motor_20 = Motor(Ports.PORT20, GearSetting.RATIO_6_1, True)
right_side = MotorGroup(motor_11, motor_12, motor_13)
left_side = MotorGroup(motor_18, motor_19, motor_20)
compMode = True
#nerd
"""Extra Motors"""
motor_15 = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)
motor_16 = Motor(Ports.PORT6, GearSetting.RATIO_6_1, True)
intake = MotorGroup(motor_15, motor_16)
wings = DigitalOut(brain.three_wire_port.a)
climb_motor = Motor(Ports.PORT17, GearSetting.RATIO_36_1, False)
gyro = Inertial(Ports.PORT8)

"""init"""
intake.set_velocity(100, PERCENT)
right_side.set_velocity(100, PERCENT)
left_side.set_velocity(100, PERCENT)
climb_motor.set_velocity(100, PERCENT)
climb_motor.set_stopping(HOLD)

"""Wheel Base"""
wheelDiameterCM = 8.255
wheelTravel = 275
trackWidth = 370
wheelBase = 330
gearRatio = 1.667
drivetrain = SmartDrive(left_side, right_side, gyro, wheelTravel, trackWidth, wheelBase, MM, gearRatio)



# Begin project code
# Create callback functions for each controller button event


def onevent_controller_1buttonL1_pressed_0():
   
    climb_motor.spin(FORWARD)

def onevent_controller_1buttonL1_released_0():
   
    climb_motor.stop()

def onevent_controller_1buttonL2_pressed_0():
   
    climb_motor.spin(REVERSE)

def onevent_controller_1buttonL2_released_0():
   
    climb_motor.stop()


def forward(distance, speed):
    # brain.screen.print("forward Start" + str(brain.timer.time(SECONDS)))
    # brain.screen.new_line
    drivetrain.set_stopping(BRAKE)
    drivetrain.set_drive_velocity(speed, PERCENT)
    drivetrain.set_turn_velocity(speed, PERCENT)
    drivetrain.drive_for(FORWARD, distance, MM)
    drivetrain.stop()
    # brain.screen.print("forward End" + str(brain.timer.time(SECONDS)))
    # brain.screen.new_line()
    # drivetrain.set_stopping(COAST)

def turnToHeading(heading, speed):
    # brain.screen.print("turn start" + str(brain.timer.time(SECONDS)))
    # brain.screen.new_line()
    drivetrain.set_stopping(BRAKE)
    drivetrain.set_drive_velocity(speed, PERCENT)
    drivetrain.set_turn_velocity(speed, PERCENT)
    # brain.screen.new_line()
    # brain.screen.print("Velocity done"+ str(brain.timer.time(SECONDS)))
    # brain.screen.new_line()
     # Adjust the wait time as needed

    drivetrain.turn_to_heading(heading, DEGREES)
    drivetrain.stop()
    # brain.screen.print("turn stop" + str(brain.timer.time(SECONDS)))
    # drivetrain.set_stopping(COAST)



# Create Controller  events - 15 msec delay to ensure events get registered

wait(10, MSEC)

# Configure Arm and Claw motor hold settings and velocity

def pre_autonomous():
    global mode
    gyro.calibrate()
    # if brain.battery.capacity() <= 70 and compMode == True:
    #     brain.screen.set_font(FontType.PROP40)
    #     brain.screen.print("Change Battery")
    
    if brain.sdcard.is_inserted():
        brain.screen.clear_screen()
        global sd
        sd = True
    mode = 3
    brain.screen.draw_image_from_file("boot.png", 0, 0)
    controller_1.screen.print("Carter Mode?")
    global team
    team = 1
    """Team 2 = Red, Team 3 = Blue, Team 4 = Skills"""
    while mode not in (1, 2):
        if controller_1.buttonA.pressing():
            mode = 1
            controller_1.screen.clear_line(1)
            controller_1.screen.set_cursor(1,1)
            controller_1.screen.print("you're just wrong")
        if controller_1.buttonB.pressing():
            mode = 2
            controller_1.screen.clear_line(1)
            controller_1.screen.set_cursor(1,1)
            controller_1.screen.print("Good choice")
    wait(2, SECONDS)
    

    while team not in (2, 3, 4):
        if controller_1.buttonA.pressing():
            team = 2
            controller_1.screen.clear_line(1)
            controller_1.screen.set_cursor(1,1)
            controller_1.screen.print("Red Team")

        if controller_1.buttonB.pressing():
            team = 3
            controller_1.screen.clear_line(1)
            controller_1.screen.set_cursor(1,1)
            controller_1.screen.print("Blue Team")

        if controller_1.buttonX.pressing():
            team = 3
            controller_1.screen.clear_line(1)
            controller_1.screen.set_cursor(1,1)
            controller_1.screen.print("Skills")

        

    if not brain.sdcard.is_inserted():
        brain.screen.print("No Sd card not logging")
    # autonomous()


def autonomous():
    # gyro.calibrate()
    # pass
    # if mode == 1:
    #     forward(2000, 100)
    #     climb_motor.spin_for(FORWARD, 43, DEGREES)
    #     turnToHeading(50, 50)
    #     wings.set(True)
    #     intake.spin(FORWARD)
    #     forward(1450, 200)
    #     turnToHeading(0, 50)
    #     forward(850, 200)
    #     turnToHeading(-90, 80)
    #     wings.set(False)
    #     forward(-600, 200)
    #     forward(2200, 200)
    #     forward(-500, 200)
    #     intake.stop()
    #     brain.screen.print("AUTO END AT" + str(brain.timer.time(SECONDS)))
    
    
        

def user_control():
    # brain.screen.clear_screen()
    controller_1.buttonR1.pressed(onevent_controller_1buttonL1_pressed_0)
    controller_1.buttonR1.released(onevent_controller_1buttonL1_released_0)
    controller_1.buttonR2.pressed(onevent_controller_1buttonL2_pressed_0)
    controller_1.buttonR2.released(onevent_controller_1buttonL2_released_0)
# add 15ms delay to make sure events are registered correctly.
    wait(15, MSEC)
    
    while True:
        

        if controller_1.buttonL2.pressing():
            wings.set(True)
            """Deploy the wings"""
        else:
            wings.set(False)
        if controller_1.buttonL1.pressing():
            intake.spin(FORWARD)
        else:
            intake.stop()
        if controller_1.buttonB.pressing():
            left_side.set_stopping(BRAKE)
            right_side.set_stopping(BRAKE)
        else:
            left_side.set_stopping(COAST)
            right_side.set_stopping(COAST)
        brain.screen.new_line()

        
        if mode == 2:
            """Tank steering"""
            right_side.spin(FORWARD)
            left_side.spin(FORWARD)
            right_side.set_velocity(controller_1.axis2.position(), PERCENT)
            left_side.set_velocity(controller_1.axis3.position(), PERCENT)
        elif mode == 1:
            """Single stick drive"""
            right_side.spin(FORWARD)
            left_side.spin(FORWARD)
            carter = controller_1.axis4.position() / 2 
            carter_2 = controller_1.axis4.position() / 2
            right_side.set_velocity((controller_1.axis3.position() - carter), PERCENT)
            left_side.set_velocity((controller_1.axis3.position() + carter_2), PERCENT)

# create competition instance
comp = Competition(user_control, autonomous)
pre_autonomous()
# Main Controller loop to set motors to controller axis positions

        
