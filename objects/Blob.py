import pygame
from pygame import gfxdraw


class Blob:
    """Blob object to draw agents on the screen.

    Attributes
    ----------
    pos: list [int, int]
        position that it is to be drawn
    playing: bool
        stores if the agent is playing or not
    watching: bool
        stores if the agent is watching or not
    gossiping: bool
        stores if the agent is gossiping or not
    color: list(int, int, int)
        Color of the object to be displayed
    circle: pygame.Rect
        The object that stores the position and size of the blobs

    Methods
    -------
    render(screen)
        Renders the image according to rect on pygame screen.
    update(playing=False, watching=False, gossiping=False)
        Update the color of the agent
    handle_events(event, agent)
        When blob is clicked does something
    """
    def __init__(self, pos, player=False, conductor=False):
        """
        Parameters
        ----------
        pos: tuple[int, int]
            position that it is to be drawn
        playing: bool
            stores if the agent is playing or not
        watching: bool
            stores if the agent is watching or not
        gossiping: bool
            stores if the agent is gossiping or not
        """
        self.pos = pos
        self.player = player

        if conductor:
            self.color = (255, 0, 0)
        elif player:
            self.color = (0, 255, 0)

        self.circle = pygame.Rect(pos[0]-7, pos[1]-7, 14, 14)

        self.show_name = False
        self.font = pygame.font.Font("Images/Montserrat-Regular.ttf", 15)

    def render(self, screen, agent):
        """Renders the blob on the pygame screen

        Parameters
        ----------
        screen: pygame.Surface
            pygame screen
        """
        # pygame.draw.circle(screen, self.color, self.pos, 7, 0)
        if self.player:
            gfxdraw.filled_circle(screen, self.pos[0], self.pos[1], 7, self.color)
            gfxdraw.aacircle(screen, self.pos[0], self.pos[1], 7, self.color)
            gfxdraw.aacircle(screen, self.pos[0], self.pos[1], 5, (0, 0, 0))
        else:
            gfxdraw.filled_circle(screen, self.pos[0], self.pos[1], 7, self.color)
            gfxdraw.aacircle(screen, self.pos[0], self.pos[1], 7, self.color)
            gfxdraw.aacircle(screen, self.pos[0], self.pos[1], 5, (0, 0, 0))

        if self.show_name:
            text = self.font.render(agent.name, True, (255, 255, 255))
            w = text.get_size()[0]
            pygame.draw.rect(screen, (112, 112, 112), (self.pos[0] + 7, self.pos[1] - 27, w + 6, 20), border_radius=3)
            screen.blit(text, (self.pos[0] + 10, self.pos[1] - 27))

    def update(self, playing=False):
        """Update the color of the agent

        Parameters
        ----------
        playing: bool
            stores if the agent is playing or not
        watching: bool
            stores if the agent is watching or not
        gossiping: bool
            stores if the agent is gossiping or not
        """
        if self.player:
            self.color = (0, 255, 0)
            if playing:
                self.color = (255, 255, 0)
        else:
            self.color = (255, 0, 0)
            if playing:
                self.color = (255, 0, 255)

    def handle_events(self, event, agent):
        """When blob is clicked does something

        Parameters
        ----------
        agent: Agent
            Agent object to identify
        event: pygame.event.Event
            pygame event
        """
        if event.type == pygame.MOUSEMOTION:
            if self.circle.collidepoint(event.pos[0], event.pos[1]):
                self.show_name = True
            else:
                self.show_name = False
