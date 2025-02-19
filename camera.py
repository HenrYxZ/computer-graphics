import numpy as np
import utils
# Local Modules
from object import Sphere


class LensParams:
    """
    Parameters for the lens. This will be used to create depth of field effect.

    f(float): focal length for depth of field effect (distance from view window
        to the focal plane)
    ap_sx(float): horizontal aperture size of the lens (in view window
        coordinates)
    ap_sy(float): vertical aperture size of the lens (in view window
        coordinates)
    """
    def __init__(self, f=28, ap_sx=1.8, ap_sy=1.8):
        self.f = f
        self.ap_sx = ap_sx
        self.ap_sy = ap_sy


class Camera:
    """
    Camera object.

    position(array): position in world coordinates
    v_view(array): unit vector pointing to the view window
    v_up(array): unit vector pointing to the upside of the camera
    d(float): distance from the camera position to the view window
    scale_x(float): horizontal size of the view window in world coordinates
    scale_y(float): vertical size of the view window in world coordinates
    n0(array): unit vector for local coordinate
    n1(array): unit vector for local coordinate
    n2(array): unit vector for local coordinate
    p00(array): position of the origin of the view window in world coordinates
    lens_params(LensParams): the lens parameters for depth of field
    """

    def __init__(
        # self, position, v_view, v_up, d=18, scale_x=32, scale_y=16,
            # lens_params
        self, position, v_view, v_up, d=26, scale_x=35, scale_y=24,
            lens_params=None
    ):
        self.position = position
        self.v_view = v_view
        self.v_up = v_up
        self.d = float(d)
        self.scale_x = float(scale_x)
        self.scale_y = float(scale_y)
        self.n0 = utils.normalize(np.cross(self.v_up, self.v_view))
        self.n1 = utils.normalize(np.cross(self.v_view, self.n0))
        self.n2 = utils.normalize(self.v_view)
        # Point in the center of the screen of the camera window
        pc = self.position + self.d * self.n2
        self.p00 = (
            pc - (self.scale_x / 2) * self.n0 - (self.scale_y / 2) * self.n1
        )
        self.lens_params = lens_params

    def set_view_coord(self):
        """
        This are the unit vectors that form the view coordinates of the camera.
        Including the starting point of the view window on world coordinates.
        This information allows for projecting a point in the camera window
        into the world coordinates.
        """
        self.n0 = utils.normalize(np.cross(self.v_up, self.v_view))
        self.n1 = utils.normalize(np.cross(self.v_view, self.n0))
        self.n2 = utils.normalize(self.v_view)
        # Point in the center of the screen of the camera window
        pc = self.position + self.d * self.n2
        self.p00 = (
            pc - (self.scale_x / 2) * self.n0 - (self.scale_y / 2) * self.n1
        )

    def spin(self, degrees):
        pass

    def pan(self, degrees):
        pass

    def tilt(self, degrees):
        pass

    def inside(self, objects):
        """
        Returns true if the camera position is inside any of the objects.
        """
        for obj in objects:
            if isinstance(obj, Sphere):
                dif = self.position - obj.position
                return np.dot(dif, dif) < (obj.radius ** 2)
        return False
