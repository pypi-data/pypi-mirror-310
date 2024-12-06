from irsim.world import ObjectBase
from math import sin, cos, tan, pi
import numpy as np
from irsim.util.util import WrapToPi, diff_to_omni
from irsim.global_param import world_param
from matplotlib import image
import matplotlib.transforms as mtransforms
from irsim.util.util import WrapToRegion, get_transform, get_affine_transform
import matplotlib as mpl
from irsim.global_param.path_param import path_manager
from irsim.lib import kinematics_factory


class RobotAcker(ObjectBase):
    def __init__(
        self, shape="rectangle", shape_tuple=None, color="y", state_dim=4, **kwargs
    ):
        super(RobotAcker, self).__init__(
            shape=shape,
            shape_tuple=shape_tuple,
            kinematics="acker",
            role="robot",
            color=color,
            state_dim=state_dim,
            **kwargs,
        )

        assert (
            state_dim >= 4
        ), "for differential robot, the state dimension should be greater than 4"

        self.wheelbase = kwargs["wheelbase"]
        self.info.add_property("wheelbase", self.wheelbase)

    def plot_object(self, ax, **kwargs):

        # x = self.vertices[0, 0]
        # y = self.vertices[1, 0]

        start_x = self.vertices[0, 0]
        start_y = self.vertices[1, 0]
        r_phi = self._state[2, 0]
        r_phi_ang = 180 * r_phi / pi

        # car_image_path = Path(current_file_frame).parent / 'car0.png'
        car_image_path = path_manager.root_path + "/world/description/car_green.png"
        car_img_read = image.imread(car_image_path)

        car_img = ax.imshow(
            car_img_read,
            extent=[start_x, start_x + self.length, start_y, start_y + self.width],
        )
        trans_data = (
            mtransforms.Affine2D().rotate_deg_around(start_x, start_y, r_phi_ang)
            + ax.transData
        )
        car_img.set_transform(trans_data)

        self.plot_patch_list.append(car_img)

    def plot_goal(
        self, ax, goal_color="r", buffer_length=0.0, buffer_width=0.1, **kwargs
    ):

        goal_x = self._goal[0, 0]
        goal_y = self._goal[1, 0]
        theta = self._goal[2, 0]

        l = buffer_length + self.length
        w = buffer_width + self.width

        arrow = mpl.patches.Arrow(
            goal_x, goal_y, l * cos(theta), l * sin(theta), width=w, color=goal_color
        )
        arrow.set_zorder(3)
        ax.add_patch(arrow)

        self.plot_patch_list.append(arrow)

    @property
    def velocity_xy(self):
        return diff_to_omni(self.state[2, 0], self._velocity)
