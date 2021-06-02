import pygame

from .Button import Button


class ImageButton(Button):
    """ImageButton object for pygame GUI

    Attributes
    ----------
    image: pygame.Surface
        Encoded image that is going to be displayed on the screen

    Methods
    -------
    render(screen, image)
        Renders the button and its image
    """
    def __init__(self, w=30, h=30, pos=(250, 300)):
        """
        w: int
            width of button
        h: int
            height of button
        pos: tuple [int, int]
            position that it is to be drawn
        """
        Button.__init__(self, w, h, pos)
        self.image = None

    def render(self, screen, image):
        """Renders the button and its image

        Parameters
        ----------
        screen: pygame.Surface
            pygame screen
        image: str
            the path to the image file
        """
        pygame.draw.rect(screen, self.color, self.rect)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.rect.w, self.rect.h))
        screen.blit(self.image, self.rect)
