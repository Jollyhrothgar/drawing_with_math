"""
Defines the Walker module which splits the task of taking a random walk from
keeping to a grid. A grid object can be written to define the rules for
walkers.
"""

import numpy as np

DEG_TO_RAD = np.pi / 180.

class Walker():
    """Defines a random walker which can be configured to step in any direction
    on 2D plane. Steps are taken according to magnetude and direction, for
    increased computational cost to achieve configurability.
    """

    def __init__(
            self,
            dir_picker,
            len_picker,
            start_pos=(0, 0),
            keep_history=True,
            transform_x=None,
            transform_y=None,
            transform_length=None,
            transform_angle=None,

    ):
        """
        Args:
            dir_picker (function pointer): provide a function which
                returns the direction measured as an angle relative to the
                x-axis.
            len_picker (function pointer): provide a function that returns
                the length of the step to take.
            start_pos (Tuple x, y): choose the starting x, y location for the
                walker.
            keep_history (bool): keep a record of past steps if True, else
                don't
            transform_x (function pointer): transformation to apply to x step
            transform_y (function pointer): transformation to apply to y step
            transform_length (function pointer): transformation to apply to the
                step length.
            transform_angle (function pointer): transformation to apply to the
                step angle.
        """
        self.pos = start_pos
        self.keep_history = keep_history
        if self.keep_history:
            self.history = [start_pos]
        self.ang = dir_picker
        self.len = len_picker
        self.ang_trans = transform_angle
        self.len_trans = transform_length
        self.x_trans = transform_x
        self.y_trans = transform_y


    def get_step(self):
        """Generates a step for the walker to take using the transformation
        rules, returning the step as an x,y tuple. Uses polar coordinates to
        allow for stepping in any direction, but this introduces floating point
        error which can be corrected for by rounding the x,y coordinate via
        transformation functions at the cost of performance.

        Returns:
            Tuple(x,y) the x,y vector representing the next step to take.
        """
        angle = self.ang() * DEG_TO_RAD
        length = self.len()

        angle = angle if self.ang_trans is None else self.ang_trans(angle)
        length = length if self.len_trans is None else self.len_trans(length)
        step_x = np.cos(angle)*length
        step_y = np.sin(angle)*length

        step_x = step_x if self.x_trans is None else self.x_trans(step_x)
        step_y = step_y if self.x_trans is None else self.x_trans(step_y)

        return step_x, step_y


    def take_step(self, step):
        """Given a step x,y vector, add in cartesian vector form to the current
        walker position and save this new position in the step history.
        """
        x = self.pos[0] + step[0]
        y = self.pos[1] + step[1]
        self.pos = (x, y)
        if self.keep_history:
            self.history.append((x, y))
        return x, y
