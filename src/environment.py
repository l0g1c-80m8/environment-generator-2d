import numpy as np
import matplotlib.pyplot as plt

from enum import Enum
from obstacle import ObstacleDescriptor


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
            eta: float,
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
        plt.imshow(
            self.occ_grid,
            extent=[
                self.environment_range[0],
                self.environment_range[1],
                self.environment_range[0],
                self.environment_range[1]
            ],
            origin='lower',
            cmap='gray_r'
        )

    def save_env_img(self, out_path="../out/img.png") -> None:
        """
        A function to save the environment to an image
        """

        self.plot_environment()
        plt.savefig(out_path)
