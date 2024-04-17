from cube import Cube
from cube_controller import CubeController
from cube_view import TkCubeView

# Model
model = Cube(3)

# View
view = TkCubeView()

# Controller
controller = CubeController(model, view)
controller.start()

# TODO: add server-client API functionality to allow for external control