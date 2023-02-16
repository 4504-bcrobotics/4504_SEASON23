from rev import ColorSensorV3

class ColorModule:
    colorSensor : ColorSensorV3

    def __init__(self):
        self.currentColor = None
        self.colorChanged = False
        self.proximity = 0

    def is_colorChanged(self):
        return self.colorChanged
    
    def getColor(self):
        color = self.colorSensor.getColor()
        return color

    def getIR(self):
        ir = self.colorSensor.getIR()
        return ir

    def getProximity(self):
        prox = self.colorSensor.getProximity()
        return prox

    def execute(self):
        pass