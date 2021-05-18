import pygame

from components import Background, Button, Scene, Dropdown, Chip, HorizontalScroll
from .SelectAgentsScene import SelectAgentsScene


class StartScene(Scene):
    """Start scene that welcomes the user.

    Attributes
    ----------
    font: pygame.font.Font
        Font that is to be used in this scene
    button: Button
        Button object for the user to go to the next scene
    background: Background
        Background object to display another background

    Methods
    -------
    render(screen)
        Renders background, the button and the title
    update()
        Just to pass the superclass notimplemented error
    handle_events(events)
        When a key is pressed or the button is pressed will move to the next scene
    """
    def __init__(self):
        Scene.__init__(self)
        self.font = pygame.font.Font("Images/Montserrat-ExtraBold.ttf", 38)

        self.button = Button(font_size=21, w=349, center=True)
        self.background = Background("Images/background.jpg", (0, 0))

    def render(self, screen):
        """Renders background, the button and the title"""
        self.background.render(screen)

        self.button.render(screen, "Press any key or click to start")

        title = self.font.render("Cooperative Agents in Multi-agent Systems", True, (124, 124, 124))
        shadow = pygame.Surface(title.get_size(), pygame.SRCALPHA)
        shadow.fill((124, 124, 124, 100))
        title.blit(shadow, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(title, (34, 125))

        title = self.font.render("Cooperative Agents in Multi-agent Systems", True, (226, 215, 215))
        screen.blit(title, (31, 122))


    def update(self):
        """Just to pass the superclass notimplemented error"""
        pass

    def handle_events(self, events):
        """When a key is pressed or the button is pressed will move to the next scene"""
        Scene.handle_events(self, events)

        for event in events:
            self.button.handle_events(event)
            if event.type == pygame.KEYDOWN:
                self.manager.go_to(SelectAgentsScene())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.button.clicked(event):
                        self.manager.go_to(SelectAgentsScene())
