import pygame
from pygame import gfxdraw

class HorizontalScroll:
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
    def __init__(self, items=None, pos=(300, 420), w=919, h=35):
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
        self.rect = pygame.Rect(pos[0], pos[1], w, h + 13)
        self.move = 0
        self.min = 0

        self.draw_bar = False
        self.bar_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.h - 6, 0, 6)
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
            item.render(scroll, self.move)
        screen.blit(scroll, (self.rect.x, self.rect.y))
        if self.draw_bar:
            pygame.draw.line(screen, self.bar_color, (self.bar_rect.x, self.bar_rect.y), (self.bar_rect.x + self.bar_rect.w, self.bar_rect.y), 5)
            gfxdraw.filled_circle(screen, self.bar_rect.x, self.bar_rect.y, 2, self.bar_color)
            gfxdraw.aacircle(screen, self.bar_rect.x, self.bar_rect.y, 2, self.bar_color)
            gfxdraw.filled_circle(screen, self.bar_rect.x + self.bar_rect.w, self.bar_rect.y, 2, self.bar_color)
            gfxdraw.aacircle(screen, self.bar_rect.x + self.bar_rect.w, self.bar_rect.y, 2, self.bar_color)

    def update(self, items):
        self.items = items
        try:
            if (size := self.items[-1].rect.x + self.items[-1].rect.w) > self.rect.w:
                self.draw_bar = True
                self.bar_rect.w = self.rect.w * (self.rect.w/size)
                self.move_of_bar = (size - self.rect.w) / (self.rect.w - self.bar_rect.w)
            else:
                self.draw_bar = False

            if self.bar_rect.x <= self.rect.x:
                self.bar_rect.x = self.rect.x
            elif self.rect.x + self.rect.w <= self.bar_rect.x + self.bar_rect.w:
                self.bar_rect.x = self.rect.x + self.rect.w - self.bar_rect.w
            if self.move + self.items[0].rect.x >= 0:
                self.move = 0
            elif self.move + self.items[-1].rect.x + self.items[-1].rect.w <= self.rect.w:
                self.move = self.rect.w - (self.items[-1].rect.x + self.items[-1].rect.w)
        except IndexError:
            pass

    def handle_events(self, event):
        """Change button color onClick and onHover

        event: pygame.event.Event
            pygame event
        """
        r = self.rect.copy()
        r.x += self.move
        for i, item in enumerate(self.items):
            if item.handle_events((event, r)):
                return i + 1
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos[0], event.pos[1]):
            if event.button == 4 and self.move + self.items[0].rect.x < 0:
                self.move += 30
                self.bar_rect.x -= 30 / self.move_of_bar
            if event.button == 5 and self.move + self.items[-1].rect.x + self.items[-1].rect.w > self.rect.w:
                self.move -= 30
                self.bar_rect.x += 30 / self.move_of_bar

        if event.type == pygame.MOUSEMOTION:
            if self.bar_rect.collidepoint(event.pos[0], event.pos[1] + 1):
                self.bar_color = (84, 84, 84)
            else:
                self.bar_color = (59, 59, 59)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.bar_rect.collidepoint(event.pos[0], event.pos[1] + 1):
                self.bar_clicked = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.bar_clicked = False

        dx, dy = pygame.mouse.get_rel()
        if self.bar_clicked:
            if self.rect.x <= self.bar_rect.x and self.rect.x + self.rect.w >= self.bar_rect.x + self.bar_rect.w:
                self.bar_rect.x = self.bar_rect.x + dx
            if self.move + self.items[0].rect.x <= 0 and self.move + self.items[-1].rect.x + self.items[-1].rect.w >= self.rect.w:
                self.move -= dx * self.move_of_bar
