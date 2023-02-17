import rev 
import math
import wpilib

GrabberLevelDict_m = {
    0: 0,
    1: 0.35,
    2: 0.65,
    3: 1.0,
}

def rotationsToNextLevel(current_level, next_level):
    assert current_level in GrabberLevelDict_m.keys(), '[+] ERROR: current level argument not a valid level'
    assert next_level in GrabberLevelDict_m.keys(), '[+] ERROR: next level argument not a valid level'
    return GrabberLevelDict_m[next_level] - GrabberLevelDict_m[current_level]

class GrabberSparkMax:
    def __init__(self, canID_leader, motorType='brushless', inverted=False,
                wheel_diameter_in=6.5, ticks_per_rotation=42):
        self.canID_leader = canID_leader
        self.inverted = inverted
        self.mainMotor = None
        self.followerMotors = None
        self.coefficient = 2*math.pi*wheel_diameter_in*0.0254/ticks_per_rotation

        if motorType == 'brushless':
            mtype = rev.CANSparkMaxLowLevel.MotorType.kBrushless
        else:
            mtype = rev.CANSparkMaxLowLevel.MotorType.kBrushed

        self.mainMotor = rev.CANSparkMax(canID_leader, mtype)
        self.mainMotor.setInverted(inverted)
        self.mainEncoder = self.mainMotor.getEncoder(rev.SparkMaxRelativeEncoder.Type.kHallSensor, 42)

    def getPosition(self):
        enc = self.mainEncoder.getPosition()
        return enc

    def getContoller(self):
        con = self.mainMotor.getPIDController()
        return con 

    def resetEncoder(self):
        self.mainEncoder.setPosition(0)
        return False



class GrabberModule:
    '''
    REFERENCE: https://github.com/REVrobotics/SPARK-MAX-Examples/blob/master/Java/Position%20Closed%20Loop%20Control/src/main/java/frc/robot/Robot.java
    '''

    grabber_motor: GrabberSparkMax
    grabber_pneumatics: wpilib.PneumaticHub

    tol = 0.1
    kP = 0.1
    kI = 1e-4
    kD = 1
    kIz = 0 
    kFF = 0 
    kMaxOutput = 1 
    kMinOutput = -1
    sprocketDiameter_in = 2.5

    def __init__(self):
        self.currentPosition = 0
        self.nextPosition = 0
        self.currentLevel = 0
        self.nextLevel = 0
        self.controller = self.__setupController__()
        self.coefficient = math.pi*self.sprocketDiameter_in/25.3e-3 # m/cycle

        self.solenoid = self.__setUpDoubleSolenoid__()
        self.isOpen = False
        self.stateChanged = False

    def __setUpPneumaticHub__(self):
        self.pneumaticHub.clearStickyFaults()
        return False
    
    def __setUpDoubleSolenoid__(self):
        doubleSolenoid = self.pneumaticHub.makeDoubleSolenoid(self.PNEUMATIC_FORWARD_CHANNEL, 
                                                              self.PNEUMATIC_REVERSE_CHANNEL)
        return doubleSolenoid

    def __setupController__(self):
        controller = self.grabber_motor.getController()
        # set PID coefficients
        controller.setP(self.kP)
        controller.setI(self.kI)
        controller.setD(self.kD)
        controller.setIZone(self.kIz)
        controller.setFF(self.kFF)
        controller.setOutputRange(self.kMinOutput, self.kMaxOutput)
        return controller

    def __setRotations__(self, rotations):
        self.controller.setReference(rotations, rev.CANSparkMax.ControlType.kPosition)
        return False

    def __setPosition__(self, position):
        self.nextElevatorPosition = position
        rotations = position/self.coefficient
        self.__setRotations__(rotations)
        return False

    def setNextLevel(self, next_level):
        if next_level not in GrabberLevelDict_m.keys():
            return True

        self.nextElevatorLevel = next_level
        position = rotationsToNextLevel(self.currentLevel, next_level)

        self.nextElevatorPosition = position
        self.__setPosition__(position)

    def getPosition(self):
        self.currentElevatorPosition = self.grabber_motor.getPosition()
        return False

    def isAtLevel(self):
        if abs(self.currentPosition - self.nextPosition) < self.tol:
            self.currentLevel = self.nextLevel
            return True

        return False

    def __openGrabber__(self):
        self.doubleSolenoid.set(wpilib.DoubleSolenoid.Value.kForward) #forward = 1, reverse = 2, off = 0
        self.isOpen = True
        return False
        
    def __closeGrabber__(self):
        self.doubleSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
        self.isOpen = False
        return False

    def is_stateChanged(self):
        return self.stateChanged

    def is_open(self):
        return self.isOpen

    def setOpen(self):
        self.stateChanged = True
        self.isOpen = True

    def setClosed(self):
        self.stateChanged = True
        self.isOpen = False

    def execute(self):
        # Update grabber position
        self.getPosition()

        # Check if state has changed
        if self.stateChanged:
            if self.isOpen:
                self.__openGrabber__()
            else:
                self.__closeGrabber__()
            self.stateChanged = False
            
        pass