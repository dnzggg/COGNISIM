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
    def __init__(self, rect, index, text="", underline=None, center=True, font=11):
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
        self.font = pygame.font.Font("Images/Montserrat-Regular.ttf", font)
        self.font2 = pygame.font.Font("Images/Montserrat-Regular.ttf", font)
        self.font2.set_underline(True)
        self.color = (255, 255, 255)
        self.selected = index == 0
        self.underline = underline

    def render(self, screen):
        """Render the button and its text

        Parameters
        ----------
        screen: pygame.Surface
            pygame screen
        """

        text = self.font.render(self.text, True, self.color)
        shift = int((self.rect.w - text.get_size()[0]) / 2) - 1
        if self.underline is not None:
            text1 = self.font.render(self.text[:self.underline], True, self.color)
            text2 = self.font2.render(self.text[self.underline], True, self.color)
            text3 = self.font.render(self.text[self.underline+1:], True, self.color)
            screen.blit(text1, (self.rect.x + shift, self.rect.y))
            screen.blit(text2, (self.rect.x + shift + text1.get_size()[0], self.rect.y))
            screen.blit(text3, (self.rect.x + shift + text1.get_size()[0] + text2.get_size()[0], self.rect.y))
        else:
            screen.blit(text, (self.rect.x + shift, self.rect.y))
        if self.selected:
            pygame.draw.line(screen, self.color, (self.rect.x + shift, self.rect.y + text.get_size()[1]), (self.rect.x + shift + text.get_size()[0], self.rect.y + text.get_size()[1]))

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
