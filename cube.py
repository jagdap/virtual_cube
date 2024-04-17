import numpy as np

class ObservableModel():
    def __init__(self):
        self._event_listeners = {}

    def add_event_listener(self, event, fn):
        try:
            self._event_listeners[event].append(fn)
        except KeyError:
            self._event_listeners[event] = [fn]

        return lambda: self._event_listeners[event].remove(fn)

    def trigger_event(self, event, *args):
        if event not in self._event_listeners.keys():
            return

        for func in self._event_listeners[event]:
            func(self)

class Cube(ObservableModel):
    """A generic NxN Rubik's cube model.

    This model is observable. Available events include: cube_updated,

    """

    def __init__(self, width: int):
        super().__init__()

        assert isinstance(width, int), "width must be an integer"
        assert width >= 2 and width, "width parameter must be at least 2"
        self.width = width
        self.state = None
        self.reset()

    def reset(self,) -> None:
        """
            Resets cube to initial (solved) state.
        """
        self.state = np.array([self.width * [self.width * [face]] for face in range(6)])
        self.trigger_event("cube_updated")

    def shuffle(self, iterations: int = 37) -> None:
        """
            Shuffles cube by randomly shifting columns.
        """
        assert iterations >= 0, "assertions must be non-negative."
        for i in range(iterations):
            axis = np.random.randint(0, 3)
            index = np.random.randint(0, self.width-1)
            direction = 1 if np.random.rand() > 0.5 else -1

            self.rotate(axis,index,direction)
            

    def rotate(self, axis: int, index: int, direction: int) -> None:
        """
            Rotates a column on the cube.
        """
        assert axis in [0,1,2], "axis may only be 0 (x-axis), 1 (y-axis), or 2 (z-axis)"
        assert index >= 0 and index < self.width, "index must be in [0 : width-1]"
        assert direction in [-1, 1], "direction must be either 1 (clockwise) or -1 (counter-clockwise)"

        # x-axis
        self._flip_cube(axis)
        if axis == 2: 
            index = -1 - index
        self._shift_column(index, direction)
        self._unflip_cube(axis)

        self.trigger_event("cube_updated")

    def _flip_cube(self, axis: int) -> None:
        """
            Flips cube such that desired work axis is on front face.
        """
        # y-axis
        previous_state = self.state.copy()
        if axis == 1:
            self.state[0] = np.rot90(previous_state[0], 1)
            self.state[1] = np.rot90(previous_state[5], 1)
            self.state[2] = np.rot90(previous_state[2], 3)
            self.state[3] = np.rot90(previous_state[4], 1)
            self.state[4] = np.rot90(previous_state[1], 1)
            self.state[5] = np.rot90(previous_state[3], 1)
        # z-axis
        elif axis == 2:
            self.state[0] = previous_state[3]
            self.state[1] = previous_state[0]
            self.state[2] = previous_state[1]
            self.state[3] = previous_state[2]
            self.state[4] = np.rot90(previous_state[4], 1)
            self.state[5] = np.rot90(previous_state[5], 3)

    def _unflip_cube(self, axis: int) -> None:
        """
            Unflips cube such that desired front face is returned to original axis.
        """
        # y-axis
        previous_state = self.state.copy()
        if axis == 1:
            self.state[0] = np.rot90(previous_state[0], 3)
            self.state[1] = np.rot90(previous_state[4], 3)
            self.state[2] = np.rot90(previous_state[2], 1)
            self.state[3] = np.rot90(previous_state[5], 3)
            self.state[4] = np.rot90(previous_state[3], 3)
            self.state[5] = np.rot90(previous_state[1], 3)
        # z-axis
        elif axis == 2:
            self.state[0] = previous_state[1]
            self.state[1] = previous_state[2]
            self.state[2] = previous_state[3]
            self.state[3] = previous_state[0]
            self.state[4] = np.rot90(previous_state[4], 3)
            self.state[5] = np.rot90(previous_state[5], 1)

    def _shift_column(self, index, direction: int) -> None:
        """
            Shifts columns up/down on the current front face.
        """
        previous_state = self.state.copy()
        previous_state[2] = np.rot90(previous_state[2], 2)
        self.state[0,:,index] = previous_state[5 if direction == 1 else 4,:,index]
        self.state[4,:,index] = previous_state[0 if direction == 1 else 2,:,index]
        self.state[2,:,-1 - index] = previous_state[4 if direction == 1 else 5,::-1,index]
        self.state[5,:,index] = previous_state[2 if direction == 1 else 0,:,index]

        if index == 0:
            self.state[3] = np.rot90(previous_state[3], 1 if direction == 1 else 3)
        if index == self.width - 1:
            self.state[1] = np.rot90(previous_state[1], 3 if direction == 1 else 1)

        
    def __str__(self):
        """
            Default cube display as string.
        """
        cube_display = ""
        # top display row
        for row in range(self.width):
            cube_display += "".join(self.width * "  ")
            cube_display += "".join(["{} ".format(i) for i in self.state[4][row]])
            cube_display += "\n"
        # center display row
        for row in range(self.width):
            cube_display += "".join(["{} ".format(i) for i in self.state[3][row]])
            cube_display += "".join(["{} ".format(i) for i in self.state[0][row]])
            cube_display += "".join(["{} ".format(i) for i in self.state[1][row]])
            cube_display += "".join(["{} ".format(i) for i in self.state[2][row]])
            cube_display += "\n"
        # bottom display row
        for row in range(self.width):
            cube_display += "".join(self.width * "  ")
            cube_display += "".join(["{} ".format(i)for i in self.state[5][row]])
            cube_display += "\n"        
        return cube_display
        
if __name__ == "__main__":
    qb = Cube(3)
    qb.shuffle()
    print(qb)