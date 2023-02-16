from photonvision import PhotonCamera, PhotonUtils

class VisionModule:

    camera: PhotonCamera

    def __init__(self, camera_height_m=.3, target_height_m=.3, camera_pitch_rad=0, goal_range_m=0):
        self.camera_height = camera_height_m
        self.target_height = target_height_m
        self.camera_pitch = camera_pitch_rad
        self.goal_range = goal_range_m
        self.result = None

    def getRange(self):
        if self.result.hasTargets():
            target_pitch = self.result.getBestTarget().getPitch()
            target_range = PhotonUtils.calculateDistanceToTarget(self.camera_height, 
                                                                self.target_height, 
                                                                self.camera_pitch,
                                                                target_pitch)
            return target_range
        else:
            return None

    def getYaw(self):
        if self.result.hasTargets():
            yaw = self.result.getBestTarget().getYaw()
            return yaw
        else:
            return None

    def getPitch(self):
        if self.result.hasTargets():
            yaw = self.result.getBestTarget().getPitch()
            return yaw
        else:
            return None    
    def getID(self):
        if self.result is not None:
            if self.result.hasTargets():
                id = self.result.getBestTarget().getFiducialId()
                return id
            else:
                return None

    def hasTargets(self):
        if self.result == None:
            return False
        return self.result.hasTargets()

    def execute(self):
        result = self.camera.getLatestResult()
        self.result = result
        pass