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

    def render(self, screen):
        """Renders the blob on the pygame screen

        Parameters
        ----------
        screen: pygame.Surface
            pygame screen
        """
        # pygame.draw.circle(screen, self.color, self.pos, 8, 0)
        gfxdraw.filled_circle(screen, self.pos[0], self.pos[1], 8, self.color)
        gfxdraw.aacircle(screen, self.pos[0], self.pos[1], 8, self.color)
        gfxdraw.aacircle(screen, self.pos[0], self.pos[1], 6, (0, 0, 0))

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.circle.collidepoint(event.pos[0], event.pos[1]):
                print(agent)
