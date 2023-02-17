import ctre

class ComboTalonSRX:
    def __init__(self, canID_leader, canID_followers, inverted=False):
        self.canID_leader = canID_leader
        self.canID_followers = canID_followers
        self.inverted = inverted
        self.mainMotor = None
        self.followerMotors = None

        self.mainMotor = ctre.TalonSRX(self.canID_leader)
        self.mainMotor.setInverted(self.inverted)

        if not isinstance(self.canID_followers, list):
            self.canID_followers = [self.canID_followers]

        followerMotors = []
        for canID in self.canID_followers:
            follower = ctre.TalonSRX(canID)
            follower.setInverted(self.inverted)
            follower.follow(self.mainMotor)                              
            followerMotors.append(follower)

        self.followerMotors = followerMotors

    def setPercent(self, value):
        self.mainMotor.set(ctre._ctre.TalonSRXControlMode.PercentOutput, value)
        return False
        

class DriveTrainModule:
    mainLeft_motor: ComboTalonSRX
    mainRight_motor: ComboTalonSRX

    def __init__(self):
        self.leftSpeed = 0
        self.leftSpeedChanged = False
        
        self.rightSpeed = 0
        self.rightSpeedChanged = False           

    def setLeft(self, value):
        self.leftSpeed = value*.4           #TODO: Remove .4 when used with comp bot
        self.leftSpeedChanged = True
        
    def setRight(self, value):
        self.rightSpeed = value
        self.rightSpeedChanged = True
        
    def is_leftChanged(self):
        return self.leftSpeedChanged
    
    def is_rightChanged(self):
        return self.rightSpeedChanged

    # Arcade drive code from https://xiaoxiae.github.io/Robotics-Simplified-Website/drivetrain-control/arcade-drive/
    def setArcade(self, drive, rotate):
        """Drives the robot using arcade drive."""
        # variables to determine the quadrants
        maximum = max(abs(drive), abs(rotate))
        total, difference = drive + rotate, drive - rotate

        # set speed according to the quadrant that the values are in
        if drive >= 0:
            if rotate >= 0:  # I quadrant
                self.setLeft(maximum)
                self.setRight(difference)
            else:            # II quadrant
                self.setLeft(total)
                self.setRight(maximum)
        else:
            if rotate >= 0:  # IV quadrant
                self.setLeft(total)
                self.setRight(-maximum)
            else:            # III quadrant
                self.setLeft(-maximum)
                self.setRight(difference)


    def execute(self):
        '''This gets called at the end of the control loop'''
        if self.is_leftChanged():
            self.mainLeft_motor.setPercent(self.leftSpeed)
            self.leftSpeedChanged = False

        if self.is_rightChanged():
            self.mainRight_motor.setPercent(self.rightSpeed)
            self.rightSpeedChanged = False