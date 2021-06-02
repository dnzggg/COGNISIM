from scenes import StartScene


class SceneManager(object):
    """SceneManager that takes control of switching scenes.

    Attributes
    ----------
    graphs: dict
        Stores the matplotlib graphs to be displayed
    scene: Scene
        Current scene
    tk: tkinter.Tk
        tk object of tkinter

    Methods
    -------
    go_to(scene)
        Changes to scene
    """
    def __init__(self):
        self.go_to(StartScene())
        self.graphs = dict()

    def go_to(self, scene):
        """Changes to scene

        Parameters
        ----------
        scene: Scene
            scene that it will change to
        """
        try:
            self.previous = self.scene
        except AttributeError:
            pass
        self.scene = scene
        self.scene.manager = self
