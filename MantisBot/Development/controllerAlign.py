from math import sin, cos, pi
from magicbot import StateMachine, state

from componentsDrive import DriveTrainModule
from componentsVision import VisionModule
from componentsIMU import IMUModule

class AlignAprilTagController(StateMachine):
    vision : VisionModule
    drivetrain : DriveTrainModule
    imu : IMUModule

    targetAngle_rad = None
    targetDistance_m = None
    targetId = None
    new_target = False
    enagaged = False
    offset = 0

    def align(self, offset_m):
        if self.engaged == False:
            self.enagaged = True
            self.offset_m = offset_m

        self.engage()

    state(first=True, must_finish=True)
    def state_rotateAngle(self):

        # Identify pitch of target apriltag
        if self.new_target == False:
            self.targetAngle_rad = self.vision.getPitch()/360*2*pi
            self.targetDistance_m = self.vision.getRange()
            self.targetId = self.vision.getID()
            self.new_target = True

        # Setup PID controller for IMU pich

        # Turn self.targetAngle

        # If angle is reached
        self.next_state_now('state_moveFirstLeg')

    state(must_finish=True)
    def state_moveFirstLeg(self):
        target_distance = self.targetDistance_m*cos(self.targetAngle_rad)

        # Move target_distance
        self.drivetrain.setDistance(target_distance)

        # If distance is reached
        if self.drivetrain.isAtDistance():
            self.next_state_now('state_moveNeg90')

    state(must_finish=True)
    def state_rotateNeg90(self):
        #set PID controller for motor angle -90 degrees

        # Turn -90 degrees

        # If angle is reached
        self.next_state_now('state_moveSecondLeg')

    state(must_finish=True)
    def state_moveSecondLeg(self):
        target_distance = self.targetDistance_m*sin(self.targetAngle_rad)
        target_distance -= self.offset_m

        # Move target_distance
        self.drivetrain.setDistance(target_distance)

        # If distance is reached
        if self.drivetrain.isAtDistance():            
            self.engaged = False

    def is_engaged(self):
        return self.engaged

    


        
            
        

        

