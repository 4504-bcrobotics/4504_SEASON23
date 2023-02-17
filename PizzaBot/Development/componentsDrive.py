import ctre
import rev 

import math

from componentsHMI import FlightStickHMI

class ComboTalonSRX:
    def __init__(self, canID_leader, canID_followers, inverted=False,
                ticks_per_rotation=4096, wheel_diameter_in=6.25):
        self.canID_leader = canID_leader
        self.canID_followers = canID_followers
        self.inverted = inverted
        self.mainMotor = None
        self.followerMotors = None
        self.coefficient = 2*math.pi*wheel_diameter_in*0.0254/ticks_per_rotation

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

    def getVelocity(self):
        vel = self.mainMotor.getSelectedSensorVelocity(0)
        return vel

    def __getRawSensorPosition__(self):
        pos = self.mainMotor.getSelectedSensorPosition(0)
        return pos

    def getDistance(self):
        pos = self.__getRawSensorPosition__()*self.coefficient
        return pos
    

class ComboSparkMax:
    def __init__(self, canID_leader, canID_followers, motorType='brushless', inverted=False):
        self.canID_leader = canID_leader
        self.canID_followers = canID_followers
        self.inverted = inverted
        self.mainMotor = None
        self.followerMotors = None

        if motorType == 'brushless':
            mtype = rev.CANSparkMaxLowLevel.MotorType.kBrushless
        else:
            mtype = rev.CANSparkMaxLowLevel.MotorType.kBrushed # FIXME!: Is this right? 

        self.mainMotor = rev.CANSparkMax(canID_leader, mtype)
        self.mainMotor.setInverted(self.inverted)
        self.mainEncoder = self.mainMotor.getEncoder(rev.SparkMaxRelativeEncoder.Type.kQuadrature, 4096)

        followerMotors = []
        for canID in self.canID_followers:
            follower = rev.CANSparkMax(canID, mtype)
            follower.setInverted(self.inverted)
            follower.follow(self.mainMotor)                              
            followerMotors.append(follower)

        self.followerMotors = followerMotors

    def setPercent(self, value):
        self.mainMotor.set(value)
        return False

    def getVelocity(self):
        vel = self.mainEncoder.getVelocity() #rpm
        return vel

class DriveTrainModule:
    mainLeft_motor: ComboSparkMax
    mainRight_motor: ComboSparkMax
    # mainLeft_motor: ComboTalonSRX
    # mainRight_motor: ComboTalonSRX
    hmi_interface: FlightStickHMI

    def __init__(self):
        self.fsR = 0
        self.fsL = 0
        self.changed = False
        self.autoLockout = True

    def setInput(self, fsTuple): # fsTuple = (fsL, fsR)
        self.fsL = fsTuple[0]
        self.fsR = fsTuple[1]
        self.changed = True
        return False

    def getHMIInput(self):
        (self.fsL, self.fsR) = self.hmi_interface.getInput()
        return None

    def getVelocity(self):
        vL = self.mainLeft_motor.getVelocity()
        vR = self.mainRight_motor.getVelocity()
        return (vL, vR)

    def getDistance(self):
        dL = self.mainLeft_motor.getDistance()
        dR = self.mainRight_motor.getDistance()
        return (dR, dL)
        

    def enable_autoLockout(self):
        self.autoLockout = True

    def disable_autoLockout(self):
        self.autoLockout = False

    def is_autoLockoutActive(self):
        return self.autoLockout

    def is_changed(self):
        return self.changed

    def setMotors(self):
        self.mainLeft_motor.setPercent(self.fsL)
        self.mainRight_motor.setPercent(self.fsR)
        self.changed = False
        return False

    def execute(self):
        '''This gets called at the end of the control loop'''
        if not self.is_autoLockoutActive():
            self.getHMIInput()
            self.setMotors()
        
        else: 
            """Note: An external function needs to call setMotors() function before this will do anything useful"""
            if self.is_changed():
                self.setMotors()


        

