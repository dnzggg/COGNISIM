import pygame
from . import DropdownItem


class Dropdown:
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
    def __init__(self, text="", selections=None, w=350, h=27, pos=(300, 420), font_size=15):
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
        # if selections is None:
        #     self.selections = []
        # else:
        #     self.selections = selections

        self.text = text
        self.rect = pygame.Rect(pos[0], pos[1], w, h)
        self.color = (56, 151, 244)
        self.font_size = font_size
        self.expand_im = pygame.image.load("Images/Expand.png")
        self.un_expand_im = pygame.image.load("Images/Un-expand.png")
        self.expanded = False
        self.selected = 0
        self.selections = []
        for i, selection in enumerate(selections):
            y = self.rect.y + self.rect.h + 4 + i * (14 + 4 + 1 + 4)
            r = pygame.Rect(pos[0], y, w, h)
            self.selections.append(DropdownItem(r, i, selection))

    def render(self, screen):
        """Render the button and its text

        Parameters
        ----------
        screen: pygame.Surface
            pygame screen
        """
        if self.expanded:
            height = len(self.selections) * (4 + 14 + 4 + 1) - 1

            pygame.draw.rect(screen, (112, 112, 112), (self.rect.x, self.rect.y + self.rect.h, self.rect.w, 4))
            pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y + self.rect.h - 4, self.rect.w, 4))
            pygame.draw.rect(screen, (112, 112, 112), (self.rect.x, self.rect.y + self.rect.h, self.rect.w, height), border_radius=7)

        pygame.draw.rect(screen, self.color, self.rect, border_radius=7)

        font = pygame.font.Font("Images/Montserrat-Regular.ttf", self.font_size)
        text = font.render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.rect.x + 8, self.rect.y + 4))

        if self.expanded:
            screen.blit(self.un_expand_im, (self.rect.x + self.rect.w - 29, self.rect.y + 9))

            for i, selection in enumerate(self.selections):
                selection.render(screen)
                if i is not len(self.selections) - 1:
                    pygame.draw.line(screen, (255, 255, 255), (self.rect.x + 8, selection.rect.y + 14 + 4), (self.rect.x + self.rect.w - 8, selection.rect.y + 14 + 4))
        else:
            screen.blit(self.expand_im, (self.rect.x + self.rect.w - 29, self.rect.y + 10))

    def update(self):
        for i, selection in enumerate(self.selections):
            selection.update(i == self.selected)

    def handle_events(self, event):
        """Change button color onClick and onHover

        event: pygame.event.Event
            pygame event
        """
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos[0], event.pos[1]):
                self.expanded = True
                self.color = (53, 188, 255)
            else:
                self.color = (56, 151, 244)
        try:
            height = len(self.selections) * (4 + 14 + 4 + 1) - 1
            r = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h + height)
            if not r.collidepoint(event.pos[0], event.pos[1]):
                self.expanded = False
        except AttributeError:
            pass
        if self.expanded:
            for i, selection in enumerate(self.selections):
                if selection.handle_events(event):
                    self.selected = i
            return True
