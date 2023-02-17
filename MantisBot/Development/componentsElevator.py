import rev 
import math

ElevatorLevelDict_m = {
    0: 0,
    1: 0.35,
    2: 0.65,
    3: 1.0,
}

def positionToNextLevel(current_level, next_level):
    assert current_level in ElevatorLevelDict_m.keys(), '[+] ERROR: current level argument not a valid level'
    assert next_level in ElevatorLevelDict_m.keys(), '[+] ERROR: next level argument not a valid level'
    return ElevatorLevelDict_m[next_level] - ElevatorLevelDict_m[current_level]

class ElevatorSparkMax:
    def __init__(self, canID_leader, canID_followers, motorType='brushless', inverted=False,
                wheel_diameter_in=6.5, ticks_per_rotation=42):
        self.canID_leader = canID_leader
        self.canID_followers = canID_followers
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

        followerMotors = []
        for canID in self.canID_followers:
            follower = rev.CANSparkMax(canID, mtype)
            follower.setInverted(not inverted)
            follower.follow(self.mainMotor)                              
            followerMotors.append(follower)

        self.followerMotors = followerMotors

    def getPosition(self):
        enc = self.mainEncoder.getPosition()
        return enc

    def getContoller(self):
        con = self.mainMotor.getPIDController()
        return con 

    def resetEncoder(self):
        self.mainEncoder.setPosition(0)
        return False

class ElevatorModule:
    '''
    REFERENCE: https://github.com/REVrobotics/SPARK-MAX-Examples/blob/master/Java/Position%20Closed%20Loop%20Control/src/main/java/frc/robot/Robot.java
    '''

    elevator_motor: ElevatorSparkMax

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
        self.stateChanged = False

    def __setupController__(self):
        controller = self.elevator_motor.getController()
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

    def goToNextLevel(self, next_level):
        position = positionToNextLevel(self.currentLevel, self.nextLevel)
        self.nextElevatorPosition = position
        self.__setPosition__(position)
        return False

    def getPosition(self):
        self.currentElevatorPosition = self.elevator_motor.getPosition()
        return False

    def isAtLevel(self):
        if abs(self.currentPosition - self.nextPosition) < self.tol:
            self.currentLevel = self.nextLevel
            return True

        return False

    def setNextLevel(self, next_level):
        if next_level not in ElevatorLevelDict_m.keys():
            return True
        self.stateChanged = True
        self.nextElevatorLevel = next_level

    def execute(self):
        # Update elevator position
        self.getPosition()

        # Move level if needed
        if self.stateChanged:
            self.goToNextLevel()
            self.stateChanged = False

        pass



        


        

