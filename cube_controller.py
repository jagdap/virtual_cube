from cube import Cube
from cube_view import TkCubeView

class CubeController():
    drag_sensitivity = 100

    def __init__(self, model: Cube, view: TkCubeView):
        self.model = model
        assert model.width == 3, "CubeController can only handle 3x3 cubes."

        self.view = view

        self.bind()

    def bind(self):
        self.model.add_event_listener("cube_updated", self.update_view)
        self.view.bind_click_handler(self.handle_click_drag)

    def handle_click_drag(self, event):
        if "reset" in event:
            self.model.reset()
            return
        
        if "shuffle" in event:
            self.model.shuffle()
            return

        face, row, col, action = event
        
        command = self._process_action(action)
        if command is None:
            return
        
        if "x" in command:
            if face in [0,1,2,3]:
                self.model.rotate(1, row, 1 if "+" in command else -1)
            elif face == 4:
                self.model.rotate(2, 2-row, 1 if "+" in command else -1)
            elif face == 5:
                self.model.rotate(2, row, -1 if "+" in command else 1)

        if "y" in command:
            if face in [0,4,5]:
                self.model.rotate(0, col, -1 if "+" in command else 1)
            elif face == 1:
                self.model.rotate(2, col, 1 if "+" in command else -1)
            elif face == 2:
                self.model.rotate(0, 2-col, 1 if "+" in command else -1)
            elif face == 3:
                self.model.rotate(2, 2-col, -1 if "+" in command else 1)
    
    def _process_action(self, action) -> str:
        if abs(action.x) > self.drag_sensitivity:
            return "+x" if action.x > 0 else "-x"
        
        if abs(action.y) > self.drag_sensitivity:
            return "+y" if action.y > 0 else "-y"

        return None

    def update_view(self, *args):
        self.view.update_view(self.model.state.reshape((6,9)))
    
    def start(self):
        self.view.mainloop()