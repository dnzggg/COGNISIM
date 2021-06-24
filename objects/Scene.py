import pygame

from .QuitException import QuitException


class Scene(object):
    """Scene superclass where every scene is created using this class.

    Attributes
    ----------
    clock: pygame.time.Clock()
        Clock in the pygame screen to be controlled
    manager: SceneManager
        Its manager

    Methods
    -------
    render(screen)
        Fills the screen with a certain color
    update()
        Updates the screen
    handle_events()
        Controls if the user wants to exit and if they want to then exits the program
    """
    def __init__(self):
        self.clock = pygame.time.Clock()

    def render(self, screen):
        """Fills the screen with a certain color

        Parameters
        ----------
        screen: pygame.Surface
            pygame screen
        """
        screen.fill((30, 30, 30))

    def update(self):
        """Updates the screen

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError

    def handle_events(self, events):
        """Controls if the user wants to exit and if they want to then exits the program

        Parameters
        ----------
        events: list [pygame.event.Event]
            pygame events
        """
        for e in events:
            if (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE) or e.type == pygame.QUIT:
                raise QuitException
