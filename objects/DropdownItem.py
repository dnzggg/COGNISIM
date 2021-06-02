import pygame


class DropdownItem:
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
    def __init__(self, rect, index, text="", center=True):
        """
        Parameters
        ----------
        w: int
            width of button
        h: int
            height of button
        pos: tuple[int, int]
            position of the button
        """
        self.rect = rect
        self.index = index
        self.text = text
        self.center = center
        self.font = pygame.font.Font("Images/Montserrat-Regular.ttf", 11)
        self.color = (255, 255, 255)
        self.selected = index == 0

    def render(self, screen):
        """Render the button and its text

        Parameters
        ----------
        screen: pygame.Surface
            pygame screen
        """

        text = self.font.render(self.text, True, self.color)
        shift = int((self.rect.w - text.get_size()[0]) / 2) - 1
        screen.blit(text, (self.rect.x + shift, self.rect.y))
        if self.selected:
            pygame.draw.rect(screen, (255, 255, 255), (self.rect.x + shift - 2, self.rect.y - 2, text.get_size()[0] + 4, text.get_size()[1] + 4), 1)

    def update(self, selected):
        self.selected = selected

    def handle_events(self, event):
        """Change button color onClick and onHover

        event: pygame.event.Event
            pygame event
        """
        r = pygame.Rect(self.rect.x, self.rect.y - 2, self.rect.w, 14)
        if event.type == pygame.MOUSEMOTION:
            if r.collidepoint(event.pos[0], event.pos[1]):
                self.color = (141, 182, 205)
            else:
                self.color = (255, 255, 255)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if r.collidepoint(event.pos[0], event.pos[1]):
                return True
