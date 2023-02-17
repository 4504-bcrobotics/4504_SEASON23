# OUTDATED - REPLACED BY drivetrainController.py

import time
from math import sin, cos

from magicbot import StateMachine, state, timed_state

from componentsIMU import IMUModule
from componentsDrive import DriveTrainModule

class DriveController(StateMachine):
    drivetrain: DriveTrainModule
    imuSensor: IMUModule

    target_heading = 0
    target_distance = 0
    target_position = 0

    starting_position = (0, 0)
    starting_distance = 0

    leftSpeed = 0
    rightSpeed = 0

    current_heading = (0, 0, 0)
    current_position = (0, 0)

    TOL = (0.1, 0.1)
    err = (1, 1)

    kP = 1
    kI = 1
    kD = 1
    error = 0

    def go(self, target_heading, target_distance):
        '''This function is called from teleop or autonomous to cause the
           shooter to fire'''
        self.target_heading = target_heading
        self.target_distance = target_distance
        self.target_position = (target_distance*cos(target_heading), target_distance*sin(target_heading))
    
        self.engage()

    @state(first=True)
    def update(self):

        # Calculate current position of the robot
        self.__calculateCurrentPosition__()

        # Update PID controller for error
        self.leftSpeed, self.rightSpeed = self.__PIDIteration__()

        # Go to move state
        if self.is_atTargetHeading():
            self.next_state_now('stop')
        else:
            self.next_state_now('move')

    @state()
    def move(self):

        # Set drivetrain movement speed
        self.starting_time = time.time_ns()
        self.drivetrain.setLeft(self.leftSpeed) # Fill in arguments to this function
        self.drivetrain.setRight(self.rightSpeed) # Fill in arguments to this function

        # Go to update state
        self.next_state_now('update')

    def is_atTargetHeading(self):
        (err_x,err_y) = self.err
        if abs(err_x) < self.TOL[0] and abs(err_y) < self.TOL[1]:
            return True
        else:
            False

    @state()
    def stop(self):
        self.drivetrain.setLeft(0)
        self.drivetrain.setRight(0)
        return False

    def __calculateCurrentPosition__(self):
        # Get current heading information from last iteration
        (prev_yaw, *_) = self.current_heading


        self.current_heading = self.imu.getYPR() # Get yaw, pitch, and roll from the IMUs
        current_speed = self.drivetrain.getSpeed()

        # Calculate the change in the yaw angle
        yaw = self.current_heading[0]
        dTheta = yaw - prev_yaw

        # Calculate the change in the
        
        dt = (time.time_ns() - self.starting_time)*1e-9
        dL = dt*current_speed

        # Calculate the chage (dx,dy)
        dx = dL*cos(dTheta)
        dy = dL*sin(dTheta)

        # Update current (x,y) location of the robot
        new_x = self.current_position[0] + dx
        new_y = self.current_position[1] + dy
        self.current_position = (new_x, new_y)
        return False

    def __PIDIteration__(self):
        (cx, cy) = self.current_position
        (tx, ty) = self.target_position
        (prev_err_x, prev_err_y) = self.err

        err_x = tx - cx
        err_y = ty - cy
        
        # Use PID parameters here with err_x and err_y
        self.kP
        self.kI
        self.kD

        # Figure out how to update PID to output new speed left and right
        new_target_heading = 0 
        new_target_distance = 0
        self.err = (err_x, err_y)
        return new_target_heading, new_target_distance