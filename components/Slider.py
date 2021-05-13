import pygame
from pygame import gfxdraw


class Slider:
    """Slider object to change the speed of the simulation

    Attributes
    ----------
    to: int
        the max range the user will get on the slider
    fro: int
        the min range the user will get on the slider
    number: int
        the calculated number which is the number being displayed
    pressed: bool
        stores if the handle of the slider is pressed
    line_b_color: tuple[int, int, int]
        color of the line where its not selected yet
    line_a_color: tuple[int, int]
        color of the line where it is selected
    ellipse_color: tuple[int, int, int]
        color of the handle
    size: int
        the length of the slider
    start_pos: tuple[int, int]
        The starting point of the slider
    start_a: tuple[int, int]
        The starting point of the selected line
    end_pos: tuple[int, int]
        The ending point of the slider
    end_b: tuple[int, int]
        The ending point of the unselected line
    x: tuple[int, int]
        The x coordinate of the handle
    y: tuple[int, int]
        The y coordinate of the handle
    ellipse_pos: tuple[int, int]
        The position of the handle
    end_a: tuple[int, int]
        The ending point of the selected line

    Methods
    -------
    render(screen)
        Renders the selected and unselected lines and the handle
    update()
        Updates the value, given range and handle position to the slider object
    handle_events(event)
        If it is clicked changes color, if it is clicked and dragged will change the handles position
    """

    def __init__(self, pos=(100, 100), size=300, line_color=(120, 120, 120), ellipse_color=(66, 134, 244), fro=5,
                 to=100):
        """
        Parameters
        ----------
        pos: tuple [int, int]
            position that it is to be drawn
        size: int
            the length of the slider
        line_color: tuple[int, int, int]
            color of the line where its not selected yet
        ellipse_color: tuple[int, int, int]
            color of the handle and also the line where it is selected
        fro: int
            the min range the user will get on the slider
        to: int
            the max range the user will get on the slider
        """
        self.number = to
        self.to = to
        self.fro = fro
        self.pressed = False
        self.line_b_color = line_color
        self.ellipse_color = self.line_a_color = ellipse_color
        self.size = size
        self.start_pos = self.start_a = pos
        self.end_pos = self.end_b = (pos[0] + size, pos[1])
        self.x = pos[0] + size
        self.y = pos[1]
        self.ellipse_pos = (self.x, self.y)
        self.end_a = self.start_b = (self.x, self.y)
        self.hover = False

    def render(self, screen):
        """Renders the selected and unselected lines and the handle

        Parameters
        ----------
        screen: pygame.Surface
            pygame screen
        """
        pygame.draw.line(screen, self.line_a_color, self.start_a, self.end_a, 2)
        pygame.draw.line(screen, self.line_b_color, self.start_b, self.end_b, 2)
        if self.pressed:
            shadow = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(shadow, (66, 134, 244, 50), (25, 25), 25)
            screen.blit(shadow, (self.ellipse_pos[0] - 25, self.ellipse_pos[1] - 25))
        elif self.hover:
            shadow = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(shadow, (66, 134, 244, 50), (20, 20), 20)
            screen.blit(shadow, (self.ellipse_pos[0] - 20, self.ellipse_pos[1] - 20))
        gfxdraw.filled_circle(screen, self.ellipse_pos[0], self.ellipse_pos[1], 10, self.ellipse_color)
        gfxdraw.aacircle(screen, self.ellipse_pos[0], self.ellipse_pos[1], 10, self.ellipse_color)

    def update(self):
        """Updates the value, given range and handle position to the slider object"""
        self.number = (self.x - self.start_pos[0]) / (self.size / (self.to - self.fro)) + self.fro

    def handle_events(self, event):
        """If it is clicked changes color, if it is clicked and dragged will change the handles position

        Parameters
        ----------
        event: pygame.event.Event
            pygame event
        """
        x = self.ellipse_pos[0]
        y = self.ellipse_pos[1]
        mouse = pygame.mouse.get_pos()
        if x - 5 < mouse[0] < x + 5 and y - 5 < mouse[1] < y + 5:
            self.hover = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.pressed = True
        else:
            self.hover = False
        if event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False
        if self.pressed:
            if self.start_pos[0] - 1 < mouse[0] < self.end_pos[0] + 1:
                self.x = mouse[0]
                self.end_a = (self.x, self.y)
                self.ellipse_pos = (self.x, self.y)
                self.start_b = (self.x, self.y)
        else:
            self.ellipse_color = (66, 134, 244)
