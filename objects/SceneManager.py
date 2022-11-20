from importlib import import_module


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
        self.go_to("StartScene")
        self.graphs = dict()
        self.previous = list()

    def go_to(self, scene, args=None):
        """Changes to scene

        Parameters
        ----------
        scene: Scene
            scene that it will change to
        """
        module = import_module("scenes." + scene)
        if args is None:
            scene = getattr(module, scene)()
        else:
            scene = getattr(module, scene)(args)
        try:
            self.previous.append(self.scene)
        except AttributeError:
            pass
        self.scene = scene
        self.scene.manager = self

    def go_back(self):
        """Changes to previous scene"""
        self.scene = self.previous.pop(-1)
        self.scene.manager = self
