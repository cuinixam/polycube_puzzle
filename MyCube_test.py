import unittest
from MyCube import *


MY_SHAPE_001 = [[0, 0, 0],
                [1, 0, 0],
                [2, 0, 0],
                [3, 0, 0],
                [1, 0, 1]]


class MyCubeTestCase(unittest.TestCase):
    def test_class_exists(self):
        my_cube = MyCube()
        self.assertTrue(my_cube)
        self.assertEqual(my_cube.origin, [0, 0, 0])
        self.assertEqual(my_cube.length, 5)
        self.assertEqual(my_cube.no_gaps, 125)

    def test_get_next_location(self):
        my_cube = MyCube(length=3)
        my_loc = [0, 0, 0]
        my_loc = my_cube._get_next_location(my_loc)
        self.assertEqual(my_loc, [1, 0, 0])
        my_loc = my_cube._get_next_location(my_loc)
        self.assertEqual(my_loc, [2, 0, 0])
        my_loc = my_cube._get_next_location(my_loc)
        self.assertEqual(my_loc, [0, 1, 0])
        my_loc = my_cube._get_next_location(my_loc)
        self.assertEqual(my_loc, [1, 1, 0])
        my_loc = my_cube._get_next_location(my_loc)
        self.assertEqual(my_loc, [2, 1, 0])
        for index in range(5):
            my_loc = my_cube._get_next_location(my_loc)
        self.assertEqual(my_loc, [1, 0, 1])
        for index in range(10):
            my_loc = my_cube._get_next_location(my_loc)
        self.assertEqual(my_loc, [2, 0, 2])
        for index in range(6):
            my_loc = my_cube._get_next_location(my_loc)
        self.assertEqual(my_loc, [2, 2, 2])

    def test_generate_shape_orientations(self):
        my_cube = MyCube(length=3)
        my_shape = Shape(MY_SHAPE_001)
        my_cube._generate_shape_orientations(my_shape)

        self.assertEqual(len(my_cube._shape_orientations_points), 24, "There should be 24 possible orientations")
        self.assertEqual(len(my_cube._shape_orientations_rot), 24, "There should be 24 possible orientations")

    def test_generate_shape_orientations_symmetric_shape(self):
        my_cube = MyCube(length=2)
        my_cube._generate_shape_orientations(Shape.from_size(1, 1, 2))
        self.assertEqual(len(my_cube._shape_orientations_points), 3, "There should be 3 possible orientations")
        self.assertEqual(len(my_cube._shape_orientations_rot), 3, "There should be 3 possible orientations")

    def test_solve_shape_size_doesnt_fit(self):
        my_cube = MyCube(length=5)
        my_shape = Shape.from_size(1, 1, 2)
        number_solutions, _ = my_cube.solve(my_shape)
        self.assertEqual(number_solutions, 0, "No solutions can be found")

    def test_solve_2by2_cube(self):
        my_cube = MyCube(length=2)
        my_shape = Shape.from_size(1, 1, 2)
        number_solutions, solutions = my_cube.solve(my_shape)
        self.assertEqual(number_solutions, 1, "Solution found")

    def test_solve_4by4_cube(self):
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
        my_shape = Shape(my_points)
        number_solutions, solutions = my_cube.solve(my_shape)
        print("Total attempts: {}".format(my_cube.place_attempt))
        self.assertEqual(number_solutions, 1, "Solution found")

    @unittest.skip("takes too much time!")
    def test_solve_5by5_cube(self):
        my_cube = MyCube(length=5)
        my_shape = Shape(MY_SHAPE_001)
        number_solutions, solutions = my_cube.solve(my_shape)
        self.assertEqual(number_solutions, 1, "Solution found")


class MyPieceTestCase(unittest.TestCase):
    def test_class_exists(self):
        my_piece = MyPiece()
        self.assertTrue(my_piece)


class ShapeTestCase(unittest.TestCase):
    def test_class_exists(self):
        my_shape = Shape()
        self.assertTrue(my_shape)

    def test_from_size(self):
        my_shape = Shape.from_size(2, 2, 2)
        self.assertEqual(my_shape.length_x, 2)
        self.assertEqual(my_shape.length_y, 2)
        self.assertEqual(my_shape.length_z, 2)
        self.assertEqual(my_shape.no_points, 8)

    def test_from_points(self):
        my_points = [[0, 0, 0], [1, 0, 0],
                     [0, 1, 0], [1, 1, 0],
                     [0, 0, 1], [1, 0, 1],
                     [0, 1, 1], [1, 1, 1]
                     ]
        my_shape = Shape(my_points)
        self.assertEqual(my_shape.length_x, 2)
        self.assertEqual(my_shape.length_y, 2)
        self.assertEqual(my_shape.length_z, 2)
        self.assertEqual(my_shape.no_points, 8)


class MathTestCase(unittest.TestCase):
    def test_trig_func(self):
        self.assertEqual(math.sin(math.pi/2), 1)
        x = 2
        y = 3
        (x, y) = (-y, -x)
        self.assertEqual(x, -3)
        self.assertEqual(y, -2)


class SpaceTestCase(unittest.TestCase):
    def test_rotate_point_x_axis(self):
        self.assertEqual(Space.rotate_point_x_axis([0, 0, 0], Space.ROT_90), [0, 0, 0])
        self.assertEqual(Space.rotate_point_x_axis([1, 0, 0], Space.ROT_90), [1, 0, 0])
        self.assertEqual(Space.rotate_point_x_axis([1, 1, 0], Space.ROT_90), [1, 0, 1])
        self.assertEqual(Space.rotate_point_x_axis([1, 1, 0], Space.ROT_180), [1, -1, 0])
        self.assertEqual(Space.rotate_point_x_axis([1, 0, 1], Space.ROT_180), [1, 0, -1])
        self.assertEqual(Space.rotate_point_x_axis([1, 0, 1], Space.ROT_270), [1, 1, 0])

    def test_reset_origin(self):
        my_points = [[0, 0, 0],
                     [-1, 0, 0]]
        my_new_points = [[1, 0, 0],
                         [0, 0, 0]]
        self.assertEqual(Space.reset_origin(my_points), my_new_points)
        self.assertEqual(my_points, [[0, 0, 0], [-1, 0, 0]])

    def test_rotate_points_x_axis(self):
        my_exp_points = [[0, 0, 1],
                         [1, 0, 1],
                         [2, 0, 1],
                         [3, 0, 1],
                         [1, 0, 0]]

        my_new_points = Space.rotate_points_x_axis(points=MY_SHAPE_001,
                                                   rotation=Space.ROT_180,
                                                   reset_origin=True)
        for point in my_exp_points:
            self.assertTrue(point in my_new_points)

        my_new_points = Space.rotate_points_x_axis(points=my_exp_points,
                                                   rotation=Space.ROT_180,
                                                   reset_origin=True)
        for point in MY_SHAPE_001:
            self.assertTrue(point in my_new_points)


if __name__ == '__main__':
    unittest.main()
