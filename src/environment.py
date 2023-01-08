import math
import numpy as np
import random
from enum import Enum
import matplotlib.pyplot as plt


class RBFKernel:
    """
    A class to represent an instance of an RBF function kernel

    Attributes
    ----------
    gamma: float
        A float to set the gamma parameter for the RBF function
    origin: tuple
        A 2-tuple to hold the origin coordinates in a 2D plane

    Methods
    -------
    value(point: tuple)
        Gives the value at the point corresponding to the given RBF instance (origin and gamma)
    """

    def __init__(self, gamma: float, origin: tuple) -> None:
        """
        Parameters
        ----------
        :param gamma: float
            The distance parameter gamma
        :param origin: tuple
            The coordinates for the origin in 2D
        """

        self.gamma = gamma
        self.origin = origin

    def __str__(self):
        """
        Returns
        ----------
        :returns
            String representation for the object
        """
        return "RBFKernel(gamma=" + str(self.gamma) + ", origin=" + str(self.origin) + ")"

    def value(self, point: tuple) -> float:
        """
        Parameters
        ----------
        :param point: tuple
            The point for which the value of the function is required

        Returns
        ----------
        :returns
            Value of the RBF function at the point
        """

        return math.exp(-self.gamma * math.pow(math.dist(self.origin, point), 2))


class ObstacleDescriptor:
    """
    A class to represent an instance of an RBF function kernel

    Attributes
    ----------
    obstacle_pts: int
        The number of obstacle points to be generated
    obstacle_range: tuple
        A range for min and max x and y values in a grid to center obstacle points around
    obstacle_descriptors: list
        A list of RBFKernel objects centered around random points in the obstacle_range
    gamma: int
        The distance parameter for the RBFKernels

    Methods
    -------
    generate_obstacle_descriptor() -> RBFKernel
        Returns a RBFKernel

    get_point_value(point: tuple) -> float
        Returns the collective sum of values from each RBFKernel centered at the obstacle descriptors
    """

    def __init__(self, obstacle_pts: int, obstacle_range: tuple, seed: int, gamma: int) -> None:
        """
        Parameters
        ----------
        :param obstacle_pts: int
            The number obstacle descriptors
        :param obstacle_range: tuple
            Range for the RBFKernel points as a 2-tuple
        :param seed: int
            Seed for the random number generator
        :param gamma: int
            The distance parameter to be used in the obstacle descriptors
        """

        self.obstacle_pts = obstacle_pts
        self.obstacle_range = obstacle_range
        self.gamma = gamma

        if seed is not None:
            random.seed(seed)
        self.obstacle_descriptors = [self.generate_obstacle_descriptor() for _ in range(obstacle_pts)]

    def generate_obstacle_descriptor(self) -> RBFKernel:
        """
        Returns
        ----------
        :returns
            An RBFKernel object initialized with the given gamma param and random origin in the range
        """

        return RBFKernel(self.gamma, (
            random.uniform(self.obstacle_range[0], self.obstacle_range[1]),
            random.uniform(self.obstacle_range[0], self.obstacle_range[1]),
        ))

    def get_point_value(self, point: tuple) -> float:
        """
        Parameters
        ----------
        :param point: tuple
            The point for which the value of the function is required

        Returns
        ----------
        :returns
            The collective sum of values from each RBFKernel centered at the obstacle descriptors
        """

        return sum([kernel.value(point) for kernel in self.obstacle_descriptors])


class EnvironmentDescriptor:
    """
    A class to represent an instance of the environment

    Attributes
    ----------
    __occ_grid: int
        The grid image as a numpy array
    environment_range: tuple
        A range for min and max x and y values for the grid
    obstacle_point_range: tuple
        A range for min and max x and y values in a grid to center obstacle points around
    start_point: tuple
        Start point on the grid
    end_point: tuple
        End point on the grid
    obstacle_points: int
        Number of obstacle points for the RBFKernels
    eta: int
        A parameter to determine the classification of a point in the grid as an obstacle
    grid_resolution: int
        Number of parts to discretize the grid in along each axis

    Methods
    -------
    classify_point(point: tuple) -> PointClass
        Classify a point into one of the categories in PointClass
    occ_grid() -> np.array
        Generate the grid image
    plot_environment() -> None
        Plot the environment as a grid
    """

    """ An enum holding the classifications for the points on the environment grid """
    PointClass = Enum("PointClass", ["FREE", "OBSTACLE", "START", "END", "OUT_OF_RANGE"])

    def __init__(
            self,
            environment_range: tuple,
            obstacle_point_range: tuple,
            start_point: tuple,
            end_point: tuple,
            obstacle_points: int,
            eta: int,
            grid_resolution: int,
            seed: int,
            gamma: int
    ) -> None:
        """
        Parameters
        ----------
        environment_range: tuple
            A range for min and max x and y values for the grid
        obstacle_point_range: tuple
            A range for min and max x and y values in a grid to center obstacle points around
        start_point: tuple
            Start point on the grid
        end_point: tuple
            End point on the grid
        obstacle_points: int
            Number of obstacle points for the RBFKernels
        eta: int
            A parameter to determine the classification of a point in the grid as an obstacle
        grid_resolution: int
            Number of parts to discretize the grid in along each axis
        seed: int
            The seed for the random number generator
        gamma: int
            The distance parameter to be used in the obstacle descriptors (RBFKernel)
        """

        self.__occ_grid = None
        self.environment_range = environment_range
        self.obstacle_point_range = obstacle_point_range
        self.start_point = start_point
        self.end_point = end_point
        self.obstacle_points = obstacle_points
        self.eta = eta
        self.grid_resolution = grid_resolution

        self.obstacle_descriptor = ObstacleDescriptor(self.obstacle_points, self.obstacle_point_range, seed, gamma)

    def classify_point(self, point: tuple) -> PointClass:
        """
        Parameters
        ----------
        :param point: tuple
            The point to be classified

        Returns
        ----------
        :returns
            The classification of the point as one of PointClass
        """

        if point == self.start_point:
            return self.PointClass["START"]
        elif point == self.end_point:
            return self.PointClass["END"]
        elif point[0] < self.environment_range[0] \
                or point[0] > self.environment_range[1] \
                or point[1] < self.environment_range[0] \
                or point[1] > self.environment_range[1]:
            return self.PointClass["OUT_OF_RANGE"]
        elif self.obstacle_descriptor.get_point_value(point) > self.eta:
            return self.PointClass["OBSTACLE"]
        else:
            return self.PointClass["FREE"]

    @property
    def occ_grid(self) -> np.array:
        """
        Returns
        ----------
        :returns
            The grid image as a numpy array
        """

        if not self.__occ_grid:
            xs = np.linspace(self.environment_range[0], self.environment_range[1], self.grid_resolution)
            ys = np.linspace(self.environment_range[0], self.environment_range[1], self.grid_resolution)
            xy_grid = np.stack([_.flatten() for _ in np.meshgrid(xs, ys)], axis=1)
            self.__occ_grid = np.array([1 if point == self.PointClass["OBSTACLE"] else 0 for point in
                                        [self.classify_point((point[0], point[1])) for point in xy_grid]]) \
                .reshape(self.grid_resolution, self.grid_resolution)
        return self.__occ_grid

    def plot_environment(self) -> None:
        """
        A function to plot the grid
        """

        plt.plot(self.start_point[0], self.start_point[1], marker='o', markerfacecolor="green", markersize=10)
        plt.plot(self.end_point[0], self.end_point[1], marker='*', markerfacecolor="red", markersize=10)
        plt.imshow(self.occ_grid, extent=[-1.2, 1.2, -1.2, 1.2], origin='lower', cmap='gray_r')
