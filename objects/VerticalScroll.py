import pygame
from pygame import gfxdraw


class VerticalScroll:
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
    def __init__(self, items=None, pos=(30, 49), w=840, h=486):
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
        if items is None:
            items = []
        self.items = items
        self.rect = pygame.Rect(pos[0], pos[1], w + 13, h)
        self.move = 0
        self.min = 0

        self.draw_bar = False
        self.bar_rect = pygame.Rect(self.rect.x + self.rect.w - 6, self.rect.y, 6, 0)
        self.move_of_bar = 0
        self.bar_color = (59, 59, 59)
        self.bar_clicked = False

    def render(self, screen):
        """Render the button and its text

        Parameters
        ----------
        screen: pygame.Surface
            pygame screen
        """
        scroll = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        for item in self.items:
            item.render(scroll, 0, self.move)
        screen.blit(scroll, (self.rect.x, self.rect.y))
        if self.draw_bar:
            pygame.draw.line(screen, self.bar_color, (self.bar_rect.x, self.bar_rect.y), (self.bar_rect.x, self.bar_rect.y + self.bar_rect.h), 5)
            gfxdraw.filled_circle(screen, self.bar_rect.x, self.bar_rect.y, 2, self.bar_color)
            gfxdraw.aacircle(screen, self.bar_rect.x, self.bar_rect.y, 2, self.bar_color)
            gfxdraw.filled_circle(screen, self.bar_rect.x, self.bar_rect.y + self.bar_rect.h, 2, self.bar_color)
            gfxdraw.aacircle(screen, self.bar_rect.x, self.bar_rect.y + self.bar_rect.h, 2, self.bar_color)

    def update(self, items):
        self.items = items
        try:
            if (size := self.items[-1].rect.y + self.items[-1].rect.h) > self.rect.h:
                self.draw_bar = True
                self.bar_rect.h = self.rect.h * (self.rect.h/size)
                self.move_of_bar = (size - self.rect.h) / (self.rect.h - self.bar_rect.h)
            else:
                self.draw_bar = False

            if self.bar_rect.y <= self.rect.y:
                self.bar_rect.y = self.rect.y
            elif self.rect.y + self.rect.h <= self.bar_rect.y + self.bar_rect.h:
                self.bar_rect.y = self.rect.y + self.rect.h - self.bar_rect.h
            if self.move + self.items[0].rect.y >= 0:
                self.move = 0
            elif self.move + self.items[-1].rect.y + self.items[-1].rect.h <= self.rect.h:
                self.move = self.rect.h - (self.items[-1].rect.y + self.items[-1].rect.h)
        except IndexError:
            pass

    def handle_events(self, event):
        """Change button color onClick and onHover

        event: pygame.event.Event
            pygame event
        """
        r = self.rect.copy()
        r.y += self.move
        for i, item in enumerate(self.items):
            if item.handle_events((event, r)):
                return i + 1
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos[0], event.pos[1]):
            if event.button == 4 and self.move + self.items[0].rect.y < 0:
                self.move += 30
                self.bar_rect.y -= 30 / self.move_of_bar
            if event.button == 5 and self.move + self.items[-1].rect.y + self.items[-1].rect.h > self.rect.h:
                self.move -= 30
                self.bar_rect.y += 30 / self.move_of_bar

        if event.type == pygame.MOUSEMOTION:
            if self.bar_rect.collidepoint(event.pos[0] + 1, event.pos[1]):
                self.bar_color = (84, 84, 84)
            else:
                self.bar_color = (59, 59, 59)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.bar_rect.collidepoint(event.pos[0] + 1, event.pos[1]):
                self.bar_clicked = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.bar_clicked = False

        dx, dy = pygame.mouse.get_rel()
        if self.bar_clicked:
            if self.rect.y <= self.bar_rect.y and self.rect.y + self.rect.h >= self.bar_rect.y + self.bar_rect.h:
                self.bar_rect.y = self.bar_rect.y + dy
            if self.move + self.items[0].rect.y <= 0 and self.move + self.items[-1].rect.y + self.items[-1].rect.h >= self.rect.h:
                self.move -= dy * self.move_of_bar
