from magicbot import AutonomousStateMachine, state, timed_state
from wpimath.controller import PIDController

from componentsIMU import IMUModule
from componentsDrive import DriveTrainModule

from math import sqrt

class AutoDriveController(AutonomousStateMachine):

    MODE_NAME = "Auto Driver"
    DEFAULT = False

    drivetrain: DriveTrainModule
    imu: IMUModule

    leftSpeed = 0
    rightSpeed = 0

    kP_dist = 10
    kI_dist = 0
    kD_dist = 0

    kP_angle = 10
    kI_angle = 0
    kD_angle = 0
    
    anglePID = None
    distPID = None

    def setup(self, target_heading=120, target_distance=10):
        '''This function is called from teleop or autonomous to cause the
           shooter to fire'''
        
        self.distPID = PIDController(self.kP_dist, self.kI_dist, self.kD_dist)
        self.distPID.setTolerance(0.05, 0.1)
        self.distPID.setSetpoint(target_distance)

        self.anglePID = PIDController(self.kP_angle, self.kI_angle, self.kD_angle)
        self.anglePID.enableContinuousInput(0, 360)
        self.anglePID.setTolerance(1, 1)
        self.anglePID.setSetpoint(target_heading)



    # Arcade drive code from https://xiaoxiae.github.io/Robotics-Simplified-Website/drivetrain-control/arcade-drive/
    def arcade_drive(self, drive, rotate):
        """Drives the robot using arcade drive."""
        # variables to determine the quadrants
        maximum = max(abs(drive), abs(rotate))
        total, difference = drive + rotate, drive - rotate

        # set speed according to the quadrant that the values are in
        if drive >= 0:
            if rotate >= 0:  # I quadrant
                return (maximum, difference)
            else:            # II quadrant
                return (total, maximum)
        else:
            if rotate >= 0:  # IV quadrant
                return (total, -maximum)
            else:            # III quadrant
                return (-maximum, difference)


    @timed_state(duration=10, first=True, must_finish=True, next_state='stop')
    def update(self):
        # Update PID controller for error
        dist_current = self.drivetrain.getDistance()
        print(dist_current)
        dist_current = sqrt(sum([i**2 for i in dist_current]))
        dist_out = self.clamp(self.distPID.calculate(dist_current), -0.5, 0.5) 

        #TODO: Find out what the maximum Yaw value is. It may be returning something greater than 180 for some reason, resulting in the code bugging out.
        angle_current = self.imu.getYPR()[0] % 360
        angle_out = self.clamp(self.anglePID.calculate(angle_current)/360, -0.5, 0.5)
        dist_out = self.clamp(self.distPID.calculate(dist_current), -0.5, 0.5)


        self.drivetrain.setInput(self.arcade_drive(dist_out, angle_out)) # Fill in arguments to this function
        print(dist_out, angle_out)

        # Go to move state
        if self.is_atTargetHeading():
            self.next_state_now('stop')

    @state()
    def stop(self):
        self.drivetrain.setInput((0, 0))
        return False

    def is_atTargetHeading(self):
        if self.anglePID.atSetpoint() and self.distPID.atSetpoint():
            return True
        return False

    def clamp(self, num, min_value, max_value):
        return max(min(num, max_value), min_value)