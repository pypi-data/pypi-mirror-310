from math import inf, pi
from irsim.world import ObjectBase
from irsim.world.robots.robot_omni import RobotOmni
from irsim.util.util import diff_to_omni


class ObstacleOmni(RobotOmni):
    def __init__(
        self, shape: str = "circle", shape_tuple=(0, 0, 0.2), color="k", **kwargs
    ):
        super(RobotOmni, self).__init__(
            shape=shape, shape_tuple=shape_tuple, color=color, **kwargs
        )

        self.role = "obstacle"

    def plot(self, ax, **kwargs):
        super().plot(ax, **kwargs)

    @property
    def velocity_xy(self):
        return self._velocity
