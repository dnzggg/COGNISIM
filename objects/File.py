import pygame


class File:
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
    def __init__(self, text="", h=35, pos=(300, 420), font_size=40):
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
        self.color = (255, 255, 255)
        self.font = pygame.font.Font("Images/Montserrat-ExtraBold.ttf", self.font_size)
        self.text = text
        text = self.font.render(self.text, True, self.color)
        w = text.get_size()[0]
        self.rect = pygame.Rect(pos[0], pos[1], w, h)


    def render(self, screen, movex, movey):
        """Render the button and its text

        Parameters
        ----------
        screen: pygame.Surface
            pygame screen
        text: str
            text to be rendered on the button
        """
        rect = self.rect.copy()
        rect.x += movex
        rect.y += movey

        text = self.font.render(self.text, True, self.color)
        screen.blit(text, (rect.x, rect.y))

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
        if self.rect.x + r.x < x < self.rect.x + self.rect.w + r.x and \
                self.rect.y + r.y < y < self.rect.y + self.rect.h + r.y:
            self.color = (56, 151, 244)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
        else:
            self.color = (255, 255, 255)
