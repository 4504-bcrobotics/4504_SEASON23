import ctre
import wpilib
import rev
from componentsDrive import ComboSparkMax, DriveTrainModule

class IntakeModule:
    top_motor: ComboSparkMax
    bottom_motor: ComboSparkMax
    pneumaticHub: wpilib.PneumaticHub

    def __init__(self):
        self.topSpeed = 0
        self.topSpeedChanged = False

        self.bottomSpeed = 0
        self.bottomSpeedChanged = False

        self.doubleSolenoid = None
        self.isOpen = False
        self.stateChanged = False


    def setup(self):
        self.__setUpPneumaticHub__()
        self.doubleSolenoid = self.__setUpDoubleSolenoid__()
        pass

    def __setUpPneumaticHub__(self):
        self.pneumaticHub.clearStickyFaults()
        return False
    
    def __setUpDoubleSolenoid__(self):
        doubleSolenoid = self.pneumaticHub.makeDoubleSolenoid(self.PNEUMATIC_FORWARD_CHANNEL, 
                                                              self.PNEUMATIC_REVERSE_CHANNEL)
        return doubleSolenoid

    def setTop(self, value):
        self.topSpeed = value
        self.topSpeedChanged = True
        
    def setBottom(self, value):
        self.bottomSpeed = value
        self.bottomSpeedChanged = True

    def is_topChanged(self):
        return self.topSpeedChanged
    
    def is_bottomChanged(self):
        return self.bottomSpeedChanged

    def execute(self):
        '''This gets called at the end of the control loop'''
        if self.is_topChanged():
            self.top_motor.set(self.topSpeed)
            self.topSpeedChanged = False
        else:
            pass

        if self.is_bottomChanged():
            self.bottom_motor.set(self.bottomSpeed)
            self.bottomSpeedChanged = False
        else:
            pass

        if self.stateChanged:
            if self.isOpen:
                self.closeIntake()
            else:
                self.openIntake()
            self.stateChanged = False
        else:
            pass
#TODO: Configure the motors for Spark Max motor controllers
    def __activateMotors__(self):
        self.bottom_motor.set(rev.CANSparkMax.ControlType.kPercentOutput, self.MAX_SPEED_BOTTOM)
        self.top_motor.set(rev.CANSparkMax.ControlType.kPercentOutput, self.MAX_SPEED_TOP)
        return False
    
    def __deactivateMotors__(self):
        self.bottom_motor.set(ctre._ctre.TalonSRXControlMode.PercentOutput, 0)
        self.top_motor.set(ctre._ctre.TalonSRXControlMode.PercentOutput, 0)
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

    def openIntake(self):
        self.doubleSolenoid.set(wpilib.DoubleSolenoid.Value.kForward) #forward = 1, reverse = 2, off = 0
        self.__activateMotors__()
        return False
        
    def closeIntake(self):
        self.doubleSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
        self.__deactivateMotors__()
        return False