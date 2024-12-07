from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import Vector3, Quaternion
from cv_bridge import CvBridge
from typing import Union
import numpy as np

bridge = CvBridge()

class Center():
  def __init__(self, x: float = 0, y: float = 0):
    self.x: float = x
    self.y: float = y

class Center3D():
  def __init__(self, x: float = 0, y: float = 0, z: float = 0):
    self.x: float = x
    self.y: float = y
    self.z: float = z

class Size:
  def __init__(self, width: float = 0, height: float = 0, depth: float = 0):
    self.width = width
    self.height = height
    self.depth = depth

class Color:
  def __init__(self, r: float = 0, g: float = 0, b: float = 0):
    self.r = r
    self.g = g
    self.b = b

class Sensor:
  def __init__(self):
    self.imageDepth: np.ndarray  = np.array([])
    self.cameraInfo: CameraInfo = CameraInfo()
  
  def setSensorData(self, imageDepth: Union[Image, np.ndarray], cameraInfo: CameraInfo):
    if isinstance(imageDepth, (Image)):
      self.imageDepth = bridge.imgmsg_to_cv2(imageDepth, desired_encoding='passthrough')
    else:
      self.imageDepth = imageDepth
    self.cameraInfo = cameraInfo
class BoundingBox2D:
  def __init__(self, 
               center: Center = Center(), 
               size: Size = Size(), 
               maxSize: Vector3 = Vector3()):
    self.center: Center = center
    self.size: Size = size
    self.maxSize: Vector3 = maxSize

  def setBoundingBox2D(self, center: Center, size: Size, maxSize: Vector3):
    self.center = center
    self.size = size
    self.maxSize = maxSize

class Box:
  def __init__(self, 
               center: Center3D = Center3D(), 
               orientation: Quaternion = Quaternion(), 
               size: Size = Size()):
    self.center: Center3D = center
    self.orientation: Quaternion = orientation
    self.size: Size = size

class BoundingBox3D:
  def __init__(self, 
               boundingBox2D: BoundingBox2D = BoundingBox2D(), 
               box: Box = Box()):
    self.boundingBox2D: BoundingBox2D = boundingBox2D
    self.box: Box = box

  def _setData(self,
                boundingBox2D: BoundingBox2D, 
                box: Box):
    self.boundingBox2D = boundingBox2D
    self.box = box
  
class Data:
  def __init__(self, 
               sensor: Sensor = Sensor(), 
               boundingBox2D: BoundingBox2D = BoundingBox2D()):
    self.sensor: Sensor = sensor
    self.boundingBox2D: BoundingBox2D = boundingBox2D

  def __setData(self, boundingBox2D: BoundingBox2D, image: Union[Image, np.ndarray], cameraInfo: CameraInfo):
        self.boundingBox2D = boundingBox2D
        self.sensor.setSensorData(image, cameraInfo)
