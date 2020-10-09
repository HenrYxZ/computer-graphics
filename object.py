import numpy as np
# Local modules
from constants import NO_INTERSECTION


class Object:
    """
    Represent a generic object inside the scene that has a specific position,
    material and intersect function.

    Attributes:
        position(numpy.array): A 3D point that represents the position
        material(Material): The material to be rendered for this object
        ID(int): The index inside the scene
    """

    def __init__(self, position, material):
        self.position = position
        self.material = material
        self.ID = None
        self.normal_map = None

    def set_id(self, idx):
        self.ID = idx

    def normal_at(self, p):
        """
        Get the normal at point p.
        """
        pass


class Sphere(Object):
    """
    Represent a Sphere object to be used in a scene.

    Attributes:
        position(numpy.array): A 3D point inside the plane
        material(Material): The material to be rendered for this object
        radius(float): The radius of this sphere
    """

    def __init__(
            self, position, material, radius
    ):
        Object.__init__(self, position, material)
        self.radius = radius

    def __str__(self):
        return "r: {}, pc: {}".format(
            self.radius, self.position
        )

    def normal_at(self, p):
        return (p - self.position) / float(self.radius)

    def intersect_sphere_np(self, pr, nr):
        # Intersect the sphere using numpy array approach (don't know how to
        # do it)
        pc = self.position
        dif = pr - pc
        b = np.dot(nr, dif)
        c = np.dot(dif, dif) - self.radius ** 2
        discriminant = b ** 2 - c
        t = -1 * b - np.sqrt(discriminant)
        return np.where(b > 0 or discriminant < 0, NO_INTERSECTION, t)
