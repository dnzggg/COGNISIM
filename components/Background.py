import pygame


class Background:
    """Background object for pygame GUI

    Attributes
    ----------
    image: pygame.Surface
        Encoded image that is going to be displayed on the screen
    rect: pygame.Rect
        Object that stores the position and size of the image

    Methods
    -------
    render(screen)
        Renders the image according to rect on pygame screen.
    """

    def __init__(self, image_file, pos):
        """Creates the object

        Parameters
        ----------
        image_file: str
            the path to the image file
        pos: tuple [int, int]
            position that it is to be drawn
        """
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos

    def render(self, screen):
        """Renders the image according to rect on pygame screen.

        Parameters
        ----------
        screen: pygame.Surface
            pygame screen
        """
        width = pygame.display.Info().current_w
        height = pygame.display.Info().current_h
        self.image = pygame.transform.scale(self.image, (width, height))
        screen.blit(self.image, self.rect)
