import os
import tkinter

# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
# os.environ['SDL_VIDEO_WINDOW_POS'] = "250,200"

import pygame

from objects import QuitException
from objects.SceneManager import SceneManager


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
        self.manager = SceneManager()
        tk = tkinter.Tk()
        tk.withdraw()
        # self.main_dialog = tkinter.Frame(tk)
        # self.main_dialog.pack_forget()
        tk.geometry("900x300+0+0")
        tk.protocol("WM_DELETE_WINDOW", self.on_closing)
        tk.configure(background='#333')
        self.manager.tk = tk
        # self.manager.main_dialog = self.main_dialog

        pygame.init()
        self.__w = width
        self.__h = height
        self.__screen = pygame.display.set_mode((width, height))
        self.__cont = True

        icon = pygame.image.load("Images/logo.png")
        pygame.display.set_icon(icon)

    def on_closing(self):
        self.manager.tk.withdraw()

    def start(self):
        """Start the tkinter window to display graphs and control both tkinter and pygame"""

        while self.__cont:
            self.manager.tk.update()

            try:
                self.manager.scene.handle_events(pygame.event.get())
            except QuitException:
                self.__cont = False
                continue
            self.manager.scene.update()
            self.manager.scene.render(self.__screen)
            self.manager.scene.clock.tick(144)
            pygame.display.update()

        self.manager.tk.destroy()


if __name__ == "__main__":
    screen = Screen(950, 550)
    screen.start()
    pygame.display.quit()
    pygame.quit()
