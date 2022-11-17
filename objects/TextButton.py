import pygame

from objects import Button


class TextButton(Button):
    """Button object for pygame GUI

    Attributes
    ----------
    rect: pygame.Rect
        asd
    color: tuple(int, int, int)
        asd
    font_size: int
        font size of the text on button

    Methods
    -------
    render(screen, text)
        Render the button and its text
    """
    def __init__(self, w=350, h=35, pos=(300, 420), font_size=21, center=False):
        """
        Parameters
        ----------
        w: int
            width of button
        h: int
            height of button
        pos: tuple[int, int]
            position of the button
        font_size: int
            font size of the text on button
        """
        Button.__init__(self, w, h, pos, font_size, center)

    def render(self, screen, text):
        """Render the button and its text

        Parameters
        ----------
        screen: pygame.Surface
            pygame screen
        text: str
            text to be rendered on the button
        """
        back = pygame.image.load("Images/back.png")
        back2 = pygame.image.load("Images/back2.png")
        screen.blit(back, (self.rect.x, self.rect.y + 3))
        font = pygame.font.Font("Images/Montserrat-Regular.ttf", self.font_size)
        font.set_underline(True)
        text1 = font.render(str(text), True, (255, 255, 255))
        screen.blit(text1, (self.rect.x + 18, self.rect.y))

    def clicked(self, event):
        """Returns if the button has been clicked.

        Parameters
        ----------
        event: pygame.event.Event
            pygame event

        Returns
        -------
        bool
            True if button is clicked
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos[0], event.pos[1]):
                return True

    def handle_events(self, event):
        """Change button color onClick and onHover

        event: pygame.event.Event
            pygame event
        """
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos[0], event.pos[1]):
                self.color = (53, 188, 255)
            else:
                self.color = (56, 151, 244)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos[0], event.pos[1]):
                if event.button == 1:
                    return True
