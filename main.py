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
        self.__w = width
        self.__h = height
        self.__screen = pygame.display.set_mode((width, height))
        self.__cont = True
        self.manager = SceneManager()

        icon = pygame.image.load("Images/logo.png")
        pygame.display.set_icon(icon)

    def on_closing(self):
        self.manager.tk.withdraw()

    def start(self):
        """Start the tkinter window to display graphs and control both tkinter and pygame"""
        tk = tkinter.Tk()
        tk.withdraw()
        main_dialog = tkinter.Frame(tk)
        main_dialog.pack_forget()
        tk.geometry("250x250+0+0")
        tk.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.manager.tk = tk

        while self.__cont:
            try:
                main_dialog.update()
            except:
                print("tkinter window closed")
            try:
                self.manager.scene.handle_events(pygame.event.get())
            except QuitException:
                self.__cont = False
                continue
            self.manager.scene.update()
            self.manager.scene.render(self.__screen)
            self.manager.scene.clock.tick(144)
            pygame.display.update()

        main_dialog.destroy()


if __name__ == "__main__":
    pygame.init()
    pygame.display.init()
    screen = Screen(950, 550)
    screen.start()
    pygame.display.quit()
    pygame.quit()
