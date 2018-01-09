import math
import logging
from random import sample

logging.basicConfig(level=logging.INFO)


class MyCube:
    def __init__(self, length=5):
        self.logger = logging.getLogger(__name__)
        self.origin = [0, 0, 0]
        self.length = length
        self.size= math.pow(length, 3)
        self.no_gaps = self.size
        self._occupied_locations = []
        self._shape_orientations_rot = []
        self._shape_orientations_points = []
        self.no_solutions = 0
        self.solutions = []
        self.no_placed_shapes = 0
        self.place_attempt = 0

    def solve(self, shape):
        """
        Try to combine the shape to form the cube
        :param shape:
        :return:
        """
        if math.fmod(self.size, shape.no_points):
            self.logger.info("Can not fit shape with {} number of points in a cube with size {}".format(shape.no_points, self.length))
            return [0, []]
        else:
            self.no_solutions = 0
            self.solutions = []
            self.no_placed_shapes = 0
            self.place_attempt = 0
            self._generate_shape_orientations(shape)
            self._fill_cube()

            return self.no_solutions, self.solutions

    def _generate_shape_orientations(self, shape):
        """
        Generate the 24 possible shape orientations
        :return:
        """
        for rot_x in Space.ROTATIONS:
            for rot_y in Space.ROTATIONS:
                for rot_z in Space.ROTATIONS:
                    shape_points = Space.rotate_points_x_axis(shape.points, rot_x, reset_origin=True)
                    shape_points = Space.rotate_points_y_axis(shape_points, rot_y, reset_origin=True)
                    shape_points = Space.rotate_points_z_axis(shape_points, rot_z, reset_origin=True)
                    orientation_considered = False
                    for existing_orientation in self._shape_orientations_points:
                        if all(point in existing_orientation for point in shape_points):
                            orientation_considered = True
                    if not orientation_considered:
                        self._shape_orientations_points.append(shape_points)
                        self._shape_orientations_rot.append([rot_x, rot_y, rot_z])

    def _fill_cube(self, current_gape=[0, 0, 0], occupied_locations=[], shapes_locations=[]):
        """
        """
        solution_found = False

        no_orientations = len(self._shape_orientations_points)
        for index in sample(range(no_orientations), no_orientations):
            shape_points = self._shape_orientations_points[index]

            self.place_attempt += 1
            if self.place_attempt % 100000 == 0:
                self.logger.info("Attempt [{}]: No of placed shapes {}".format(self.place_attempt, self.no_placed_shapes))

            for shift_x in range(self.length):
                origin_offset_x = current_gape[0] - shift_x
                if origin_offset_x < 0:
                    break
                origin_offset = [origin_offset_x, current_gape[1], current_gape[2]]
                # Get the positions that should be occupied by the shape
                shape_points_shifted = Space.reset_origin(shape_points, offset=origin_offset)
                shape_can_be_placed = True
                # Check if it possible to place the shape in current position and orientation
                for point in shape_points_shifted:
                    if point in occupied_locations:
                        shape_can_be_placed = False
                        break
                    if point[0] >= self.length or point[1] >= self.length or point[2] >= self.length:
                        shape_can_be_placed = False
                        break

                if shape_can_be_placed:
                    self.no_placed_shapes += 1
                    # Mark the positions as occupied and save shape position and orientation
                    no_points_added = len(shape_points_shifted)
                    occupied_locations = occupied_locations + shape_points_shifted
                    rot_x, rot_y, rot_z = self._shape_orientations_rot[index]
                    shapes_locations.append([current_gape, rot_x, rot_y, rot_z])

                    self.logger.debug("Place shape at (x,y,z): {}".format(current_gape))
                    self.logger.debug("Rotation on X,Y,Z axis: {} {} {}".format(rot_x, rot_y, rot_z))

                    # Check if the cube is full
                    if len(occupied_locations) == self.size:
                        self.solutions = shapes_locations
                        self.no_solutions += 1
                        return True

                    # Go to the next gape
                    next_gape = current_gape
                    while next_gape in occupied_locations:
                        next_gape = self._get_next_location(next_gape)
                    # Recurse to place more shapes
                    solution_found = self._fill_cube(next_gape, occupied_locations, shapes_locations)

                    if solution_found:
                        return True

                    # Remove the currently added shape and try another rotation
                    for i in range(no_points_added):
                        del occupied_locations[-1]
                    del shapes_locations[-1]
                    self.no_placed_shapes -= 1

        return solution_found

    def _get_next_location(self, current_location):

        index = current_location[0] +\
                current_location[1] * self.length +\
                current_location[2] * math.pow(self.length, 2)
        index += 2

        if index == 1:
            return [1, 0, 0]

        l2 = math.pow(self.length, 2)

        tmp_z_inc = 1 if index % l2 else 0
        z = index//l2 + tmp_z_inc
        z = z - 1 if z else 0
        tmp_y = index - z * l2
        tmp_y_inc = 1 if tmp_y % self.length else 0
        y = tmp_y//self.length + tmp_y_inc
        y = y - 1 if y else 0
        x = tmp_y - y * self.length
        x = x - 1 if x else 0

        return [x, y, z]


class Shape:
    """
    Abstract function to define a shape
    """
    def __init__(self, points=[]):
        self.length_x = 0
        self.length_y = 0
        self.length_z = 0
        self.points = points

        if points:
            [min_x, max_x, min_y, max_y, min_z, max_z] = Space.min_max(points)
            self.length_x = max_x - min_x + 1
            self.length_y = max_y - min_y + 1
            self.length_z = max_z - min_z + 1

        self.no_points = len(self.points)

    @classmethod
    def from_size(cls, length_x, length_y, length_z):
        """ This method imports the interfaces from an pdo_xml file using
        a dedicated interface loader.
        In case of success the interfaces are parsed in order to determine
        the manipulation type.
        The interface supporting the special "signal manipulation" in software
        will be marked with "manipulation:full|basic|none"

        This method creates an instance (with the interface dictionary
        as argument).

        In case of parsing error it will raise an ValueError exception

        """
        points = []
        for x in range(length_x):
            for y in range(length_y):
                for z in range(length_z):
                    points.append([x, y, z])

        return cls(points)

    def get_occupied_position(self, origin, direction, rotation):
        """
        Gets the origin, direction and rotation and generates a list
        with all positions in space occupied by the piece.
        :return:
        """
        points_ret = []

        return points_ret



class MyPiece:

    def __init__(self):
        self.points = [[0, 0, 0],
                       [1, 0, 0],
                       [2, 0, 0],
                       [3, 0, 0],
                       [1, 0, 1]]

    def get_occupied_position(self, origin, direction, rotation):
        """
        Gets the origin, direction and rotation and generates a list
        with all positions in space occupied by the piece.
        :return:
        """
        points_ret = []

        return points_ret


class Space:
    DIR_Xp = [1, 0, 0]
    DIR_Xn = [-1, 0, 0]
    DIR_Yp = [0, 1, 0]
    DIR_Yn = [0, -1, 0]
    DIR_Zp = [0, 0, 1]
    DIR_Zn = [0, 0, -1]

    [ROT_0, ROT_90, ROT_180, ROT_270] = range(0, 360, 90)

    ROTATIONS = [ROT_0, ROT_90, ROT_180, ROT_270]
    DIRECTIONS = [DIR_Xp, DIR_Yp, DIR_Zp]

    @staticmethod
    def rotate_points_axis(axis, points, rotation, reset_origin=False):
        if axis == Space.DIR_Xn:
            points = Space.rotate_points_x_axis(points, rotation, reset_origin)
        elif axis == Space.DIR_Yn:
            points = Space.rotate_points_y_axis(points, rotation, reset_origin)
        elif axis == Space.DIR_Zn:
            points = Space.rotate_points_z_axis(points, rotation, reset_origin)

        return points

    @staticmethod
    def rotate_point_x_axis(point, rotation):
        """
        X-Axis rotation
        y' = y*cos q - z*sin q
        z' = y*sin q + z*cos q
        x' = x
        """
        (x, y, z) = point

        if rotation == Space.ROT_90:
            (y, z) = (-z, y)
        elif rotation == Space.ROT_180:
            (y, z) = (-y, -z)
        elif rotation == Space.ROT_270:
            (y, z) = (z, -y)

        return [x, y, z]

    @staticmethod
    def rotate_points_x_axis(points, rotation, reset_origin=False):
        """
        X-Axis rotation
        """
        new_points = []

        for point in points:
            new_points.append(Space.rotate_point_x_axis(point, rotation))
        if reset_origin:
            new_points = Space.reset_origin(new_points)

        return new_points

    @staticmethod
    def rotate_points_y_axis(points, rotation, reset_origin=False):
        """
        Y-Axis rotation
        """
        new_points = []

        for point in points:
            new_points.append(Space.rotate_point_y_axis(point, rotation))
        if reset_origin:
            new_points = Space.reset_origin(new_points)

        return new_points

    @staticmethod
    def rotate_points_z_axis(points, rotation, reset_origin=False):
        """
        Y-Axis rotation
        """
        new_points = []

        for point in points:
            new_points.append(Space.rotate_point_z_axis(point, rotation))
        if reset_origin:
            new_points = Space.reset_origin(new_points)

        return new_points

    @staticmethod
    def rotate_point_y_axis(point, rotation):
        """
        Y-Axis rotation
        z' = z*cos q - x*sin q
        x' = z*sin q + x*cos q
        y' = y
        """
        (x, y, z) = point

        if rotation == Space.ROT_90:
            (z, x) = (-x, z)
        elif rotation == Space.ROT_180:
            (z, x) = (-z, -x)
        elif rotation == Space.ROT_270:
            (z, x) = (x, -z)

        return [x, y, z]

    @staticmethod
    def rotate_point_z_axis(point, rotation):
        """
        Z-Axis rotation
        x' = x*cos q - y*sin q
        y' = x*sin q + y*cos q
        z' = z
        """
        (x, y, z) = point

        if rotation == Space.ROT_90:
            (x, y) = (-y, x)
        elif rotation == Space.ROT_180:
            (x, y) = (-x, -y)
        elif rotation == Space.ROT_270:
            (x, y) = (y, -x)

        return [x, y, z]

    @staticmethod
    def reset_origin(points, offset=[]):
        """
        Shift all the points such that the most "negative point" becomes the origin (0,0,0)
        :param points:
        :param offset: shift all points with this offset
        :return: new points shifted
        """
        if not points:
            return []
        else:
            if offset:
                min_x = -offset[0]
                min_y = -offset[1]
                min_z = -offset[2]
            else:
                [min_x, _, min_y, _, min_z, _] = Space.min_max(points)
            new_points = []
            for point in points:
                new_x = point[0] - min_x
                new_y = point[1] - min_y
                new_z = point[2] - min_z
                new_points.append([new_x, new_y, new_z])
            return new_points

    @staticmethod
    def min_max(points):
        """
        Gets the min and max for all coordinates (x,y,z) from a list of points
        :param points:
        :return: [min_x, max_x, min_y, max_y, min_z, max_z]
        """
        min_x = None
        max_x = None
        min_y = None
        max_y = None
        min_z = None
        max_z = None

        if points:
            min_x = max_x = points[0][0]
            min_y = max_y = points[0][1]
            min_z = max_z = points[0][2]
            for point in points:
                min_x = min(min_x, point[0])
                max_x = max(max_x, point[0])
                min_y = min(min_y, point[1])
                max_y = max(max_y, point[1])
                min_z = min(min_z, point[2])
                max_z = max(max_z, point[2])

        return [min_x, max_x, min_y, max_y, min_z, max_z]

    @staticmethod
    def size(points):
        [min_x, max_x, min_y, max_y, min_z, max_z] = Space.min_max(points)
        length_x = max_x - min_x
        length_y = max_y - min_y
        length_z = max_z - min_z

        return [length_x, length_y, length_z]


if __name__ == '__main__':

    if 0:
        my_cube = MyCube(length=4)
        my_points = [
            [0, 0, 0],
            [1, 0, 0],
            [2, 0, 0],
            [0, 0, 1],
            [1, 0, 1],
            [2, 0, 1],
            [0, 0, 2],
            [0, 0, 3]
        ]
    else:
        my_cube = MyCube(length=5)
        my_points = [
            [0, 0, 0],
            [1, 0, 0],
            [2, 0, 0],
            [3, 0, 0],
            [1, 0, 1]
        ]

    my_shape = Shape(my_points)
    number_solutions, solutions = my_cube.solve(my_shape)
    if number_solutions:
        index = 1
        for solution in solutions:
            print("[{}] ---------------- ".format(index))
            index += 1
            print("Position (x,y,z): {}".format(solution[0]))
            print("Rotation X axis: {}".format(solution[1]))
            print("Rotation Y axis: {}".format(solution[2]))
            print("Rotation Z axis: {}".format(solution[3]))
            print("")
    else:
        print("Cube could not be solved!")
