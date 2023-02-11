from networktables import NetworkTables
from photonvision import PhotonCamera, PhotonUtils

class LimelightModule:

    camera: PhotonCamera

    def __init__(self, camera_height_m=.3, target_height_m=.3, camera_pitch_rad=0, goal_range_m=0):
        self.camera_height = camera_height_m
        self.target_height = target_height_m
        self.camera_pitch = camera_pitch_rad
        self.goal_range = goal_range_m
        self.result = None

        self.table = NetworkTables.getTable("limelight")
        self.hasTargets = bool(self.table.getNumber('tv',None))
        self.targetX = self.table.getNumber('tx',None)
        self.targetY = self.table.getNumber('ty',None)
        self.targetArea = self.table.getNumber('ta',None)
        # targetSkew = table.getNumber('ts',None)

    def getRange(self):
        if self.hasTargets:
            target_pitch = self.targetX
            target_range = PhotonUtils.calculateDistanceToTarget(self.camera_height, 
                                                                self.target_height, 
                                                                self.camera_pitch,
                                                                target_pitch)
            return target_range
        else:
            return None

    def getX(self):
        if self.hasTargets:
            return self.targetX
        else:
            return None

    def getY(self):
        if self.hasTargets:
            return self.targetY
        else:
            return None  

    #TODO: find out how to get target ID via networktables
    # def getID(self):
    #     if self.result is not None:
    #         if self.hasTargets():
    #             id = self.result.getBestTarget().getFiducialId()
    #             return id
    #         else:
    #             return None

    def hasTargets(self):
        return self.hasTargets

    def execute(self):
        self.hasTargets = bool(self.table.getNumber('tv',None))
        self.targetX = self.table.getNumber('tx',None)
        self.targetY = self.table.getNumber('ty',None)
        self.targetArea = self.table.getNumber('ta',None)
        pass