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
rightside = MotorGroup(motor_11, motor_12, motor_13)
leftside = MotorGroup(motor_18, motor_19, motor_20)
#nerd
"""Extra Motors"""
motor_15 = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)
motor_16 = Motor(Ports.PORT6, GearSetting.RATIO_6_1, True)
intake = MotorGroup(motor_15, motor_16)
wings = DigitalOut(brain.three_wire_port.a)
climbmotor = Motor(Ports.PORT17, GearSetting.RATIO_36_1, False)
gyro = Inertial(Ports.PORT8)

"""init"""
intake.set_velocity(100, PERCENT)
rightside.set_velocity(100, PERCENT)
leftside.set_velocity(100, PERCENT)
climbmotor.set_velocity(100, PERCENT)
climbmotor.set_stopping(BRAKE)

"""Wheel Base"""
wheelDiameterCM = 8.255
wheelTravel = 275
trackWidth = 370
wheelBase = 330
gearRatio = .4
drivetrain = SmartDrive(leftside, rightside, gyro, wheelTravel, trackWidth, wheelBase, MM, gearRatio)
drivetrain
gyro.calibrate
wait(1, SECONDS)
# Begin project code
# Create callback functions for each controller button event


def onevent_controller_1buttonL1_pressed_0():
   
    climbmotor.spin(FORWARD)

def onevent_controller_1buttonL1_released_0():
   
    climbmotor.stop()

def onevent_controller_1buttonL2_pressed_0():
   
    climbmotor.spin(REVERSE)

def onevent_controller_1buttonL2_released_0():
   
    climbmotor.stop()


def forward_time(time, speed):
    leftside.set_stopping(BRAKE)
    rightside.set_stopping(BRAKE)
    leftside.set_velocity(speed, PERCENT)
    rightside.set_velocity(speed, PERCENT)

    start_time = brain.timer.time(SECONDS)

    while brain.timer.time(SECONDS) - start_time < time:
        wait(5, MSEC)
    
    leftside.set_velocity(0, PERCENT)
    rightside.set_velocity(0, PERCENT)
    leftside.set_stopping(COAST)
    rightside.set_stopping(COAST)

def forward(distance, speed):
    if speed == 100:
        speed = 100 * 2
    drivetrain.set_stopping(BRAKE)
    drivetrain.set_drive_velocity(speed)
    drivetrain.set_turn_velocity(speed)
    drivetrain.drive_for(FORWARD, distance, MM)
    drivetrain.stop()
    drivetrain.set_stopping(BRAKE)
    drivetrain.set_stopping(COAST)

def turnToHeading(heading, speed):
    drivetrain.set_stopping(BRAKE)
    drivetrain.set_drive_velocity(speed)
    drivetrain.set_turn_velocity(speed)
     # Adjust the wait time as needed

    drivetrain.turn_to_heading(heading)
    drivetrain.stop()
    drivetrain.set_stopping(BRAKE)
    drivetrain.set_stopping(COAST)


# Create Controller  events - 15 msec delay to ensure events get registered

wait(15, MSEC)

# Configure Arm and Claw motor hold settings and velocity

def pre_autonomous():
    global mode
    mode = 3
    controller_1.screen.print("Carter Mode?")
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
    if not brain.sdcard.is_inserted():
        brain.screen.print("No Sd card not logging")
    autonomous()


def autonomous():
    # forward(100, 50)
    turnToHeading(-90, 100)
    # forward(300, 100)
    # wait(30,MSEC)
    # turnToHeading(90, 60)
    # wait(30,MSEC)
    # forward(300, 200)

    climbmotor.spin_for(FORWARD, 86, DEGREES)
    climbmotor.stop
    # brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here



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
        else:
            wings.set(False)
        if controller_1.buttonL1.pressing():
            intake.spin(FORWARD)
        else:
            intake.stop()

        

        
        if mode == 2:
            rightside.spin(FORWARD)
            leftside.spin(FORWARD)
            rightside.set_velocity(controller_1.axis2.position(), PERCENT)
            leftside.set_velocity(controller_1.axis3.position(), PERCENT)
        elif mode == 1:
            rightside.spin(FORWARD)
            leftside.spin(FORWARD)
            rightside.set_velocity((controller_1.axis3.position() - controller_1.axis4.position()), PERCENT)
            leftside.set_velocity((controller_1.axis3.position() + controller_1.axis4.position()), PERCENT)

# class Logging(object):
    """
    A class that can run multiple logs for different events and store their outputs to the SD card
    """

    def __init__(self, log_name, flush_interval=1, terminal=None):
        """
        Create a new instance of the class
        :param log_name: The name to use for the log, a number preceded by a hyphen "-" will be appended to this name to avoid overwriting old logs
        :type log_name: str
        """
        self.terminal = terminal
        

        self.file_name = log_directory + str(log_name) + ".log"
        self.file_object = open(self.file_name, "w", )
        self.write_queue = []
        self.log("Starting log at " + self.file_name)

        Thread(self.auto_flush_logs, [flush_interval])

    def log(self, string: str):
        """
        Send a string to the file, using the log format
        :param string:
        """
        try:
            self.write_queue.append(string)
        except MemoryError:
            self.write_queue.clear()
            self.log("Ran out of memory while writing logs, some messages may be omitted\n")

    def exit(self):
        """
        Close the log object
        """
        self.log("Ending log at " + self.file_name)
        self.flush_file_contents()
        self.file_object.close()

    def flush_file_contents(self):
        try:
            with open(self.file_name, "a") as self.file_object:
                for _ in range(len(self.write_queue)):
                    self.file_object.write(self.write_queue.pop(0))
                self.file_object.flush()
        except OSError:
            brain.screen.print("Failed to flush log write queue (Was the SD card removed?)")

    def auto_flush_logs(self, interval_sec):
        while True:
            wait(interval_sec, SECONDS)
            self.flush_file_contents()

# create competition instance
comp = Competition(user_control, autonomous)
pre_autonomous()
# Main Controller loop to set motors to controller axis postiions

        
