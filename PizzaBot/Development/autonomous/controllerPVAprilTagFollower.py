from magicbot import AutonomousStateMachine, state, timed_state
from wpimath.controller import PIDController

from componentsVision import VisionModule
from componentsDrive import DriveTrainModule

from math import sqrt

# THIS IS CODED TO WORK WITH THE PHOTONVISION MODULE, NOT THE LIMELIGHT
class AprilTagController(AutonomousStateMachine):

    MODE_NAME = "AprilTagPhotonvision"
    DEFAULT = True

    drivetrain : DriveTrainModule
    vision : VisionModule

    kP_linear = .04
    kI_linear = .01
    kD_linear = .0002

    kP_angle = .035
    kI_angle = .03
    kD_angle = .0002

    
    anglePID = None
    distPID = None
    goalRange = 0

    def setup(self, tagID=3, goalRange=2):
        self.linearPID =  PIDController(self.kP_linear, self.kI_linear, self.kD_linear)
        self.anglePID = PIDController(self.kP_angle, self.kI_angle, self.kD_angle)
        self.goalRange = goalRange
        self.tagID = tagID


    @state(first=True)
    def follow(self):
        if self.vision.hasTargets():
            target_range = self.vision.getRange()
            forward_speed = -(self.linearPID.calculate(target_range, self.goalRange))

            yaw = self.vision.getYaw()
            rotation_speed = self.anglePID.calculate(yaw, 0)

        else:
            forward_speed = 0
            rotation_speed = 0
        
        forward_speed = self.clamp(forward_speed, -1, 1)
        rotation_speed = self.clamp(rotation_speed, -1, 1)

        self.drivetrain.setArcade(forward_speed, rotation_speed)
        if self.drivetrain.leftSpeed != 0 or self.drivetrain.rightSpeed != 0:
            print(self.drivetrain.leftSpeed, self.drivetrain.rightSpeed, rotation_speed)
        
        # vL = (-forward_speed + rotation_speed)
        # vR = (-forward_speed - rotation_speed)

        # self.drivetrain.setLeft(vL)
        # self.drivetrain.setRight(vR)
        # print(self.vision.hasTargets(), vL, vR)



    

    @state()
    def stop(self):
        self.drivetrain.setLeft(0)
        self.drivetrain.setRight(0)
        return False

    def clamp(self, num, min_value, max_value):
        return max(min(num, max_value), min_value)