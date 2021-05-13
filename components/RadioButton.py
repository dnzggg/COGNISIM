import pygame
from pygame import gfxdraw


class RadioButton:
    """RadioButton object for pygame GUI.

    Attributes
    ----------
    color: tuple[int, int, int]
        The border of the button
    active: bool
        Stores if the button has been active or not
    active_color: tuple[int, int, int]
        The color of the button when its active
    pos: tuple[int, int]
        Position of the button
    pressed: bool
        Stores if the button has been clicked or not
    hover: bool
        Stores if the object is onHover or not
    disabled: bool
        Stores if the button is disabled or not
    go_back: bool
        Stores if the button can be pressed again to go back or not

    Methods
    -------
    render(screen)
        Renders the button
    activate()
        Activate the button (so select the choice)
    deactivate()
        Deactivate the button (so deselect the choice)
    handle_events(event, other_buttons)
        If button is pressed activates itself, and deactivates the other buttons in its group
    """

    def __init__(self, pos=(200, 200), color=(56, 151, 244), active=False, disabled=False,
                 go_back=False):
        """
        Parameters
        ----------
        pos: tuple[int, int]
            Position of the button
        color: tuple[int, int, int]
            The border of the button
        active: bool
            Stores if the button has been active or not
        disabled: bool
            Stores if the button is disabled or not
        go_back: bool
            Stores if the button can be pressed again to go back or not
        """
        self.color = color
        self.active = active
        self.pos = pos
        self.pressed = False
        self.hover = False
        self.disabled = disabled
        self.go_back = go_back

    def render(self, screen):
        """Renders the button

        screen: pygame.Surface
            pygame screen
        """
        if self.hover:
            shadow = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(shadow, (56, 151, 244, 20), (20, 20), 20)
            screen.blit(shadow, (self.pos[0] - 20, self.pos[1] - 20))
        if self.disabled:
            self.color = (38, 63, 88) if self.active else (59, 59, 59)
        else:
            self.color = (112, 112, 112) if not self.active else (56, 151, 244)

        gfxdraw.filled_circle(screen, self.pos[0], self.pos[1], 12, self.color)
        gfxdraw.filled_circle(screen, self.pos[0], self.pos[1], 9, (30, 30, 30))
        gfxdraw.aacircle(screen, self.pos[0], self.pos[1], 9, (30, 30, 30))
        gfxdraw.aacircle(screen, self.pos[0], self.pos[1], 12, self.color)
        if self.active:
            gfxdraw.filled_circle(screen, self.pos[0], self.pos[1], 5, self.color)
            gfxdraw.aacircle(screen, self.pos[0], self.pos[1], 5, self.color)

    def activate(self):
        """Activate the button (so select the choice)"""
        self.active = True

    def deactivate(self):
        """Deactivate the button (so deselect the choice)"""
        self.active = False

    def handle_events(self, event, other_buttons):
        """If button is pressed activates itself, and deactivates the other buttons in its group

        Parameters
        ----------
        event: pygame.event.Event
            pygame event
        other_buttons: list[RadioButton]
            radio buttons that it is linked with so they can get deactivated
        """
        x = self.pos[0] - 12
        y = self.pos[1] - 12
        height = width = 24
        mouse = pygame.mouse.get_pos()
        if x < mouse[0] < x + width and y < mouse[1] < y + height:
            self.hover = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.go_back:
                    self.activate()
                    self.pressed = True
                    for button in other_buttons:
                        button.deactivate()
                else:
                    self.active = not self.active
                    self.pressed = not self.pressed
        else:
            self.pressed = False
            self.hover = False
