import pygame


class Chip:
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
    def __init__(self, text="", h=35, pos=(300, 420), font_size=15):
        """
        Parameters
        ----------
        h: int
            height of button
        pos: tuple[int, int]
            position of the button
        font_size: int
            font size of the text on button
        """
        self.font_size = font_size
        self.color = (56, 151, 244)
        font = pygame.font.Font("Images/Montserrat-Regular.ttf", self.font_size)
        self.text = font.render(text, True, self.color)
        w = 8 + self.text.get_size()[0] + 2 + 8 + 15 + 8
        self.rect = pygame.Rect(pos[0], pos[1], w, h)
        self.delete_im = pygame.image.load("Images/close.png")

    def render(self, screen, move):
        """Render the button and its text

        Parameters
        ----------
        screen: pygame.Surface
            pygame screen
        text: str
            text to be rendered on the button
        """
        rect = self.rect.copy()
        rect.x += move
        pygame.draw.rect(screen, self.color, rect, 2, border_radius=20)

        screen.blit(self.text, (rect.x + 8, rect.y + 8))

        screen.blit(self.delete_im, (rect.x + rect.w - 23, rect.y + 10))

    def handle_events(self, event):
        """Change button color onClick and onHover

        event: pygame.event.Event
            pygame event
        """
        try:
            event, r = event
        except TypeError:
            r = pygame.Rect(0, 0, 0, 0)
        x, y = pygame.mouse.get_pos()
        if self.rect.x + self.rect.w - 23 + r.x < x < self.rect.x + self.rect.w - 8 + r.x and \
                self.rect.y + 10 + r.y < y < self.rect.y + self.rect.h - 10 + r.y:
            self.delete_im = pygame.image.load("Images/close2.png")
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
        else:
            self.delete_im = pygame.image.load("Images/close.png")
