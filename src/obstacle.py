import random

from kernel import RBFKernel


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
