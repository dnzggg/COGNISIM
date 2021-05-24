import pygame


class Button:
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
        self.rect = pygame.Rect(pos[0], pos[1], w, h)
        self.color = (56, 151, 244)
        self.font_size = font_size
        self.center = center

    def render(self, screen, text):
        """Render the button and its text

        Parameters
        ----------
        screen: pygame.Surface
            pygame screen
        text: str
            text to be rendered on the button
        """
        # For transparent
        # surface = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        # surface.set_alpha(128)
        # rect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
        # pygame.draw.rect(surface, self.color, rect)
        # screen.blit(surface, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, self.color, self.rect, border_radius=3)

        font = pygame.font.Font("Images/Montserrat-Regular.ttf", self.font_size)
        if self.rect.w - 8 > font.size(str(text))[0]:
            text1 = font.render(str(text), True, (255, 255, 255))
            if self.center:
                shift = int((self.rect.w - text1.get_size()[0]) / 2) - 1
                screen.blit(text1, (self.rect.x + shift, self.rect.y + 5))
            else:
                screen.blit(text1, (self.rect.x + 14, self.rect.y + 5))
        else:
            text += " "
            t = ""
            line = 0
            for string in text.split(" "):
                temp = t
                t += string + " "
                if self.rect.w - 8 < font.size(str(t))[0] and string != "":
                    text1 = font.render(str(temp), True, (255, 255, 255))
                    if self.center:
                        screen.blit(text1, (self.rect.x + 10, self.rect.y + 4 + (line * 25)))
                    else:
                        screen.blit(text1, (self.rect.x + 10, self.rect.y + 4 + (line * 25)))
                    t = string + " "
                    line += 1
                else:
                    text1 = font.render(str(t), True, (255, 255, 255))
                    if self.center:
                        screen.blit(text1, (self.rect.x + 10, self.rect.y + 4 + (line * 25)))
                    else:
                        screen.blit(text1, (self.rect.x + 10, self.rect.y + 4 + (line * 25)))

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
