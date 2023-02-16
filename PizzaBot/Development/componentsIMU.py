import wpilib
import ctre


class IMUModule:

    imuSensor: ctre.Pigeon2

    def __init__(self):
        self.YPR = (0, 0, 0)

    def getYPR(self):
        return self.YPR

    def execute(self):
        self.YPR = self.imuSensor.getYawPitchRoll()
        pass 
