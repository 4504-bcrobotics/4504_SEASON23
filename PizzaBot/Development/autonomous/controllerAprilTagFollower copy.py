from magicbot import AutonomousStateMachine, state, timed_state
from wpimath.controller import PIDController

from componentsVision import VisionModule
from componentsDrive import DriveTrainModule

from math import sqrt

# THIS IS CODED TO WORK WITH THE PHOTONVISION MODULE, NOT THE LIMELIGHT
class AprilTagController(AutonomousStateMachine):

    MODE_NAME = "AprilTagPhotonvision"
    DEFAULT = False

    drivetrain : DriveTrainModule
    vision : VisionModule

    kP_linear = 1
    kI_linear = .01
    kD_linear = .2

    kP_angle = 1
    kI_angle = .01
    kD_angle = .2
    
    anglePID = None
    distPID = None
    goalRange = 0

    def setup(self, tagID=3, goalRange=1):
        self.linearPID = PIDController(self.kP_linear, self.kI_linear, self.kD_linear)
        self.anglePID = PIDController(self.kP_angle, self.kI_angle, self.kD_angle)
        self.goalRange = goalRange
        self.tagID = tagID

    @state(first=True)
    def follow(self):
        print("Running controllerAprilTagFollower.py")
        if self.vision.hasTargets():
            target_range = self.vision.getRange()
            forward_speed = self.linearPID.calculate(target_range, self.goalRange)

            yaw = self.vision.getYaw()
            rotation_speed = self.anglePID.calculate(yaw, 0)

        else:
            forward_speed = 0
            rotation_speed = 0
        
        vL = (-forward_speed + rotation_speed)
        vR = (-forward_speed - rotation_speed)

        self.drivetrain.setInput((vL, vR))

    @state()
    def stop(self):
        self.drivetrain.setInput((0, 0))
        return False

    def clamp(self, num, min_value, max_value):
        return max(min(num, max_value), min_value)