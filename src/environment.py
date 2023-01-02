import math
import numpy as np
import random
from enum import Enum
import matplotlib.pyplot as plt


class RBFKernel:
    def __init__(self, gamma, origin):
        self.gamma = gamma
        self.origin = origin

    def __str__(self):
        return "RBFKernel(gamma=" + str(self.gamma) + ", origin=" + str(self.origin) + ")"

    def value(self, point):
        return math.exp(-self.gamma * math.pow(math.dist(self.origin, point), 2))


class ObstacleDescriptor:
    def __init__(self, obstacle_pts, obstacle_range, seed):
        self.obstacle_pts = obstacle_pts
        self.obstacle_range = obstacle_range

        random.seed(seed)
        self.obstacle_descriptors = [self.generate_obstacle_descriptor() for _ in range(obstacle_pts)]

    def generate_obstacle_descriptor(self):
        return RBFKernel(25, (
            random.uniform(self.obstacle_range[0], self.obstacle_range[1]),
            random.uniform(self.obstacle_range[0], self.obstacle_range[1]),
        ))

    def get_point_value(self, point):
        return sum([kernel.value(point) for kernel in self.obstacle_descriptors])


class EnvironmentDescriptor:
    def __init__(
            self,
            environment_range,
            obstacle_point_range,
            start_point,
            end_point,
            obstacle_points,
            eta,
            grid_resolution,
            seed
    ):
        self.__occ_grid = None
        self.environment_range = environment_range
        self.obstacle_point_range = obstacle_point_range
        self.start_point = start_point
        self.end_point = end_point
        self.obstacle_points = obstacle_points
        self.eta = eta
        self.grid_resolution = grid_resolution

        self.PointClass = Enum("PointClass", ["FREE", "OBSTACLE", "START", "END", "OUT_OF_RANGE"])
        self.obstacle_descriptor = ObstacleDescriptor(self.obstacle_points, self.obstacle_point_range, seed)

    def classify_point(self, point):
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
    def occ_grid(self):
        if not self.__occ_grid:
            xs = np.linspace(self.environment_range[0], self.environment_range[1], self.grid_resolution)
            ys = np.linspace(self.environment_range[0], self.environment_range[1], self.grid_resolution)
            xy_grid = np.stack([_.flatten() for _ in np.meshgrid(xs, ys)], axis=1)
            self.__occ_grid = [self.classify_point((point[0], point[1])) for point in xy_grid]
        return self.__occ_grid

    def grid_image(self):
        return np.array([1 if point == self.PointClass["OBSTACLE"] else 0 for point in self.occ_grid]) \
            .reshape(self.grid_resolution, self.grid_resolution)

    def plot_environment(self):
        plt.plot(self.start_point[0], self.start_point[1], marker='o', markerfacecolor="green", markersize=10)
        plt.plot(self.end_point[0], self.end_point[1], marker='*', markerfacecolor="red", markersize=10)
        plt.imshow(self.grid_image(), extent=[-1.2, 1.2, -1.2, 1.2], origin='lower', cmap='gray_r')
        return plt





