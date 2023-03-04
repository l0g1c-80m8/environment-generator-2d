import math


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
