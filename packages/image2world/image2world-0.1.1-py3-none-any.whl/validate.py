from interface import *
import numpy as np
from sensor_msgs.msg import CameraInfo

class Validate:
    def __init__(self):
        pass

    def _validateCenter(self, center: Center):
        if not isinstance(center.x, (int, float)) or not isinstance(center.y, (int, float)):
            raise Exception("Center values must be numbers")
        
    def _validateCenter3D(self, center: Center3D):
        if not isinstance(center.x, (int, float)) or not isinstance(center.y, (int, float)) or not isinstance(center.z, (int, float)):
            raise Exception("Center values must be numbers")

    def _validateSize(self, size: Size):
        if not isinstance(size.width, (int, float)) or not isinstance(size.height, (int, float)):
            raise Exception("Size values must be numbers")
    
    def _validateCenterDepth(self, centerDepth):
        if centerDepth <= 0:
            raise Exception("Center depth is not valid")
        
    def _validateCompareCameraInfo(self, currentCameraInfo: CameraInfo, cameraInfo: CameraInfo):
        equal = True
        equal = equal and (cameraInfo.width == currentCameraInfo.width)
        equal = equal and (cameraInfo.height == currentCameraInfo.height)
        equal = equal and np.all(np.isclose(np.asarray(cameraInfo.k),
                                            np.asarray(currentCameraInfo.k)))
        return equal
    
    def _validateBoundingBox3D(self, bbox: BoundingBox3D): 
        self._validateCenter3D(bbox.box.center)
        self._validateSize(bbox.box.size)
        #FINISH THIS VALIDATE METHOD
    
    def _validatePolygonVertices(self, vertices):
        if not isinstance(vertices, list):
            raise Exception("Vertices must be a list")
        for vertex in vertices:
            if not isinstance(vertex, Center):
                raise Exception("Vertices must be Center objects")