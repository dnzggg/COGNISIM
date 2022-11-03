import pygame
from pygame import gfxdraw
import tkinter


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
    def __init__(self, pos, width, radius, agent, player=False, conductor=False):
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
        self.o_pos = pos
        self.radius = radius
        self.o_radius = radius
        self.inner_radius = radius - 6
        self.o_inner_radius = self.inner_radius
        self.width = width
        self.o_width = self.width
        self.circle = pygame.Rect(pos[0]*self.width, pos[1]*self.width+87, radius, radius)
        self.o_circle = pygame.Rect(pos[0]*self.width, pos[1]*self.width+87, radius, radius)

        self.player = player
        self.agent = agent

        if conductor:
            self.color = (255, 0, 0, 100)
        elif player:
            self.color = (0, 255, 0, 100)

        self.show_name = False
        self.font = pygame.font.Font("Images/Montserrat-Regular.ttf", 15)

        self.shift_x = 0
        self.shift_y = 0

    def render(self, screen):
        """Renders the blob on the pygame screen

        Parameters
        ----------
        screen: pygame.Surface
            pygame screen
        """
        r = int(self.radius / 2)

        x = self.pos[0] * self.width + self.shift_x + r
        y = self.pos[1] * self.width + self.shift_y + r + 87

        gfxdraw.filled_circle(screen, x, y, r, self.color)
        gfxdraw.aacircle(screen, x, y, r, self.color)
        gfxdraw.aacircle(screen, x, y, int(self.inner_radius / 2), (0, 0, 0))

        if self.show_name:
            text = self.font.render(self.agent.name, True, (255, 255, 255))
            w = text.get_size()[0]
            pygame.draw.rect(screen, (112, 112, 112), (x + 7, y - 27, w + 6, 20), border_radius=3)
            screen.blit(text, (x + 10, y - 27))

    def update(self, gossiping=False, giver=False, receiver=False, shift=(0, 0), zoom=100, width=25):
        """Update the color of the agent

        Parameters
        ----------
        gossiping: bool
            stores if the agent is playing or not
        giver: bool
            stores if the agent is watching or not
        receiver: bool
            stores if the agent is gossiping or not
        """
        if self.player:
            self.color = (0, 255, 0, 100)
            if gossiping:
                self.color = (0, 255, 0)
            if giver:
                self.color = (255, 255, 0)
            if receiver:
                self.color = (255, 0, 255)
        else:
            self.color = (255, 0, 0, 100)
            if gossiping:
                self.color = (255, 0, 0)

        self.radius = int(self.o_radius * zoom / 100)
        self.inner_radius = int(self.o_inner_radius * zoom / 100)
        self.shift_x, self.shift_y = shift
        self.width = width
        self.circle = pygame.Rect(self.pos[0] * self.width + shift[0], self.pos[1] * self.width + 87 + shift[1], self.radius, self.radius)

    def handle_events(self, event, tk):
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

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.circle.collidepoint(event.pos[0], event.pos[1]):
                tk.title(self.agent.name)
                text = tkinter.Text(tk)
                text.insert(tkinter.END, self.agent.name)
                text.insert(tkinter.END, "a")
                text.pack()
                tk.deiconify()

    def get_pos(self):
        x = self.circle.x + self.circle.w / 2
        y = self.circle.y + self.circle.h / 2
        return x, y
