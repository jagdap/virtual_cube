import tkinter as tk
import numpy as np

class TkCubeView(tk.Tk):

    _click_handler_fn = None
    
    def __init__(self):
        super().__init__()
        self.faces = {}
        self._initializeCubeView()
    
    def _initializeCubeView(self):
        """Builds out the cube and buttons."""

        self.geometry("600x600") 

        # create the three "rows" for displaying the faces
        row0, row1, row2 = tk.Frame(self), tk.Frame(self), tk.Frame(self)
        row0.pack(expand=True, fill="both", side="top")
        row1.pack(expand=True, fill="both", side="top")
        row2.pack(expand=True, fill="both", side="top")

        # 6 cube faces and spacers
        face0 = TkCubeFace(row1)
        face1 = TkCubeFace(row1)
        face2 = TkCubeFace(row1)
        face3 = TkCubeFace(row1)
        face4 = TkCubeFace(row0)
        face5 = TkCubeFace(row2)
        self.faces = {0:face0, 1:face1, 2:face2, 3:face3, 4:face4, 5:face5}

        spacer00, spacer01, spacer02 = tk.Frame(row0), tk.Frame(row0), tk.Frame(row0)
        spacer00.pack(expand=True, fill="both", side="left")
        self.faces[4].pack(expand=True, fill="both", side="left")
        spacer01.pack(expand=True, fill="both", side="left")
        spacer02.pack(expand=True, fill="both", side="left")

        self.faces[3].pack(expand=True, fill="both", side="left")
        self.faces[0].pack(expand=True, fill="both", side="left")
        self.faces[1].pack(expand=True, fill="both", side="left")
        self.faces[2].pack(expand=True, fill="both", side="left")

        spacer20, spacer21, spacer22 = tk.Frame(row2), tk.Frame(row2), tk.Frame(row2)
        spacer20.pack(expand=True, fill="both", side="left")
        self.faces[5].pack(expand=True, fill="both", side="left")
        spacer21.pack(expand=True, fill="both", side="left")
        spacer22.pack(expand=True, fill="both", side="left")

        for face_id in range(6):
            self.faces[face_id].update_face(9 * [face_id])
        
        self.faces[0].bind_mouse_drag(lambda x: self._click_handler((0, x[0], x[1], x[2])))
        self.faces[1].bind_mouse_drag(lambda x: self._click_handler((1, x[0], x[1], x[2])))
        self.faces[2].bind_mouse_drag(lambda x: self._click_handler((2, x[0], x[1], x[2])))
        self.faces[3].bind_mouse_drag(lambda x: self._click_handler((3, x[0], x[1], x[2])))
        self.faces[4].bind_mouse_drag(lambda x: self._click_handler((4, x[0], x[1], x[2])))
        self.faces[5].bind_mouse_drag(lambda x: self._click_handler((5, x[0], x[1], x[2])))

        # add buttons to reset and shuffle cube
        reset_button = tk.Button(spacer00, text="RESET")
        shuffle_button = tk.Button(spacer00, text="SHUFFLE")
        reset_button.pack()
        shuffle_button.pack()

        reset_button.bind("<ButtonRelease-1>", lambda x: self._click_handler_fn("reset"))
        shuffle_button.bind("<ButtonRelease-1>", lambda x: self._click_handler_fn("shuffle"))


    def _click_handler(self, *args):
        if self._click_handler_fn is None:
            print(*args)
            return

        self._click_handler_fn(*args)

    def bind_click_handler(self, fn):
        self._click_handler_fn = fn
    
    def update_view(self, state):
        for face_idx in range(6):
            for block_idx in range(9):
                self.faces[face_idx].blocks[block_idx].configure(bg=TkCubeFace.colors[state[face_idx, block_idx]])

class TkCubeFace(tk.Frame):

    colors = {
        0: "white",
        1: "green",
        2: "yellow",
        3: "blue",
        4: "red",
        5: "orange"
        }
    
    mouse_drag_fn = None

    def __init__(self, master, init_color = 0):
        super().__init__(master)
        self.blocks = {}
        self._initialize_face()

    def _initialize_face(self):
        row0 = tk.Frame(self)
        row0.pack(expand=True, fill="both", side="top")

        row1 = tk.Frame(self)
        row1.pack(expand=True, fill="both", side="top")

        row2 = tk.Frame(self)
        row2.pack(expand=True, fill="both", side="top")

        b0, b1, b2 = tk.Label(row0), tk.Label(row0), tk.Label(row0)
        b3, b4, b5 = tk.Label(row1), tk.Label(row1), tk.Label(row1)
        b6, b7, b8 = tk.Label(row2), tk.Label(row2), tk.Label(row2)

        self.blocks = {0:b0, 1:b1, 2:b2, 3:b3, 4:b4, 5:b5, 6:b6, 7:b7, 8:b8}

        for block_idx in range(9):
            self.blocks[block_idx].pack(expand=True, fill="both", side="left")
            self.blocks[block_idx].configure(borderwidth=2, relief="groove")
        
        # event = "<B1-Motion>"
        event = "<ButtonRelease-1>"
        self.blocks[0].bind(event, lambda x: self._process_mouse_drag((0,0,x)))
        self.blocks[1].bind(event, lambda x: self._process_mouse_drag((0,1,x)))
        self.blocks[2].bind(event, lambda x: self._process_mouse_drag((0,2,x)))
        self.blocks[3].bind(event, lambda x: self._process_mouse_drag((1,0,x)))
        self.blocks[4].bind(event, lambda x: self._process_mouse_drag((1,1,x)))
        self.blocks[5].bind(event, lambda x: self._process_mouse_drag((1,2,x)))
        self.blocks[6].bind(event, lambda x: self._process_mouse_drag((2,0,x)))
        self.blocks[7].bind(event, lambda x: self._process_mouse_drag((2,1,x)))
        self.blocks[8].bind(event, lambda x: self._process_mouse_drag((2,2,x)))

    def update_face(self, face_state):
        assert len(face_state) == 9
        for block_idx in range(9):
            self.blocks[block_idx].configure(bg=self.colors[face_state[block_idx]])
        return
    
    def _process_mouse_drag(self, event):
        if self.mouse_drag_fn is None:
            print(event)
            return

        self.mouse_drag_fn(event)

    def bind_mouse_drag(self, fn):
        self.mouse_drag_fn = fn


if __name__ == "__main__":

    vu = TkCubeView()
    vu.mainloop()