import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import tkinter

import pygame

from components.SceneManager import SceneManager

os.environ['SDL_VIDEO_WINDOW_POS'] = "250,200"


class Screen:
    """This is the controller of the view

    Attributes
    ----------
    __w: int
        width of the screen
    __h: int
        height of the screen
    __screen: pygame.display
        A pygame display where objects are going to be rendered on
    __cont: bool
        This is to control if the pygame display should still be shown or not
    manager: SceneManager
        This controls the scenes (the set of objects) to be displayed

    Methods
    -------
    start()
        Start the tkinter window to display graphs and control both tkinter and pygame.
    """
    def __init__(self, width, height):
        """
        Parameters
        ----------
        width:
        height:
        """
        self.__w = width
        self.__h = height
        self.__screen = pygame.display.set_mode((width, height))
        self.__cont = True
        self.manager = SceneManager()

        icon = pygame.image.load("Images/logo.png")
        pygame.display.set_icon(icon)

    def start(self):
        """Start the tkinter window to display graphs and control both tkinter and pygame"""
        tk = tkinter.Tk()
        tk.withdraw()
        main_dialog = tkinter.Frame(tk)
        main_dialog.pack()
        self.manager.tk = tk

        while self.__cont:
            main_dialog.update()
            temp = self.manager.graphs.copy()
            for graph in self.manager.graphs:
                if not self.manager.graphs[graph].running:
                    temp.pop(graph)
                self.manager.graphs[graph].update()
            self.manager.graphs = temp
            self.manager.scene.handle_events(pygame.event.get())
            self.manager.scene.update()
            self.manager.scene.render(self.__screen)
            self.manager.scene.clock.tick(144)
            pygame.display.flip()

        main_dialog.destroy()


if __name__ == "__main__":
    pygame.init()
    screen = Screen(950, 550)
    screen.start()
