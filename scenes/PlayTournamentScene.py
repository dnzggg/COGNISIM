import random

import pygame

from objects import Blob, Button, Scene, DropdownItem, Slider, MessageBox, PositionDict, Timeline

from components import Tournament
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class PlayTournamentScene(Scene):
    """Scene where the user can see the simulation and interact with its objects.
    
    Attributes
    ----------
    font: pygame.font.Font
        Font that is to be used in this scene
    running: bool
        Store if the simulation is running or not
    was_running: bool
        Store if the simulation was running or not
    new_generation: bool
        Store if the components is over or not
    run: Tournament.start()
        Method that initializes the components
    UPDATE: pygame.USEREVENT
        Event that will call the next step in the simulation
    speed: int
        speed of the simulation
    blobs: dict
        Dictionary of blobs to represent agents
    agents: list
        List of agents
    playing_agents: list
        List of playing agents
    reset_button: Button
        Button object to reset the game (return to the previous page)
    speed_slider: Slider
        Slider object to handle the simulation speed

    Methods
    -------
    render(screen)
        Renders the blobs, buttons, radio buttons, sliders, labels, and lines
    update()
        Updates the blobs status, messagebox, and slider
    handle_events()
        If the start button is pressed, starts the simulation; if the next button is pressed, gets the next round;
        if the slider is changed, changes the speed; if the reset button is pressed, goes back to the select agents
        scene; when the graph buttons are pressed, calls the plot_graph function
    plot_graph(name, xs, ys, x_label, y_label, title)
        Creates a Graph object, adds it to the list of graphs
    """
    def __init__(self):
        Scene.__init__(self)
        size = pygame.display.get_window_size()
        pygame.display.set_mode((size[0], size[1]), pygame.RESIZABLE)

        self.font = pygame.font.Font("Images/Montserrat-Regular.ttf", 21)
        self.font2 = pygame.font.Font("Images/Montserrat-Regular.ttf", 15)
        self.font3 = pygame.font.Font("Images/Montserrat-ExtraBold.ttf", 15)

        self.tournament = Tournament()
        self.run = self.tournament.run()
        self.agents = self.tournament.get_agents()
        self.conductor = self.tournament.get_conductor()
        self.blobs = dict()
        self.playing_agents = None

        self.running = False
        self.was_running = False
        self.new_generation = False
        self.total_rounds = self.tournament.total_rounds

        self.UPDATE = pygame.USEREVENT + 1
        self.speed = 99
        pygame.time.set_timer(self.UPDATE, self.speed, True)

        self.tab = 0
        self.home_tab = DropdownItem(pygame.Rect(18, 8, 47, 19), 0, "Home", underline=0, font=15, center=False)
        self.info_tab = DropdownItem(pygame.Rect(89, 8, 29, 19), 1, "Info", underline=0, font=15, center=False)
        self.graph_tab = DropdownItem(pygame.Rect(142, 8, 29, 19), 2, "Graph", underline=0, font=15, center=False)

        self.reset_button = Button(w=90, pos=(16, 39), center=True)
        self.start_stop_button = Button(w=80, pos=(130, 39), center=True)
        self.next_button = Button(w=80, pos=(234, 39), center=True)
        self.show_statistics_button = Button(w=275, pos=(16, 39), center=True)

        self.speed_label = self.font.render("Speed", True, (255, 255, 255))
        self.speed_outside_im = pygame.image.load("Images/speedometer_outside.png")
        self.speed_outside_im = pygame.transform.smoothscale(self.speed_outside_im, (30, 30))
        self.speed_inside_im = pygame.image.load("Images/speedometer_inside.png")
        self.speed_inside_im = pygame.transform.smoothscale(self.speed_inside_im, (15, 15))
        self.speed_slider = Slider((465, 57), 240, fro=5, to=100)

        self.shift = False
        self.check_shift = True
        self.max_shift = None
        self.min_shift_x = None
        self.min_shift_y = None
        self.shift_x = 0
        self.shift_y = 0
        self.border = 0

        self.zoom = 100
        self.show_zoom = False
        self.BACK_TO_NORMAL = pygame.USEREVENT + 2
        self.min_zoom = 25
        self.max_zoom = 400

        self.simulation_size_w_padding = None
        self.simulation_size_wo_padding = None

        # self.timeline = Timeline(rounds=self.tournament.total_time_stamp)

    def render(self, screen):
        """Renders the blobs, buttons, radio buttons, labels and lines"""
        Scene.render(self, screen)

        pos1 = pos2 = None
        if self.tournament.player1 and self.tournament.player2:
            pos1 = self.blobs[self.tournament.player1.index].get_pos()
            pos2 = self.blobs[self.tournament.player2.index].get_pos()

        render_after = []
        for agent in self.blobs:
            w, h = pygame.display.get_window_size()
            if 0 - self.blobs[agent].radius / 2 < self.blobs[agent].get_pos()[0] < w + self.blobs[agent].radius / 2:
                if 87 - self.blobs[agent].radius / 2 < self.blobs[agent].get_pos()[1] < h + self.blobs[agent].radius / 2:
                    if self.blobs[agent].show_name:
                        render_after.append(agent)
                    if self.tournament.player1:
                        if agent == self.tournament.player1.index:
                            render_after.append(agent)
                    if self.tournament.player2:
                        if agent == self.tournament.player2.index:
                            render_after.append(agent)
                    self.blobs[agent].render(screen)

        if pos1 and pos2:
            color = (255, 255, 255)
            if self.tournament.cooperate is not None:
                if self.tournament.cooperate:
                    color = (0, 255, 0)
                else:
                    color = (255, 0, 0)

            if self.tournament.player1.index == self.tournament.player2.index:
                pygame.gfxdraw.aacircle(screen, int(pos1[0]), int(pos1[1] + self.blobs[agent].radius / 1.5), int(self.blobs[agent].radius / 1.5) - 1, color)
                pygame.draw.circle(screen, color, (int(pos1[0]), int(pos1[1] + self.blobs[agent].radius / 1.5)), int(self.blobs[agent].radius / 1.5), 1)
                pygame.gfxdraw.aacircle(screen, int(pos1[0]), int(pos1[1] + self.blobs[agent].radius / 1.5), int(self.blobs[agent].radius / 1.5), color)

            pygame.draw.aaline(screen, color, (pos1[0] - 2, pos1[1]), (pos2[0] - 2, pos2[1]), blend=100)
            pygame.draw.aaline(screen, color, (pos1[0] - 1, pos1[1]), (pos2[0] - 1, pos2[1]), blend=100)
            pygame.draw.aaline(screen, color, pos1, pos2, blend=100)
            pygame.draw.aaline(screen, color, (pos1[0], pos1[1] - 1), (pos2[0], pos2[1] - 1), blend=100)
            pygame.draw.aaline(screen, color, (pos1[0], pos1[1] - 2), (pos2[0], pos2[1] - 2), blend=100)

        for ra in render_after:
            self.blobs[ra].render(screen)

        pygame.draw.rect(screen, (30, 30, 30), (0, 0, 100000, 85))

        self.home_tab.render(screen)
        self.info_tab.render(screen)
        self.graph_tab.render(screen)

        if self.tab == 0:
            self.reset_button.render(screen, "Reset")
            # self.prev_button.render(screen, "Prev")
            if not self.running:
                self.start_stop_button.render(screen, "Start")
            else:
                self.start_stop_button.render(screen, "Stop")
            self.next_button.render(screen, "Next")

            screen.blit(self.speed_label, (338, 42))
            screen.blit(self.speed_outside_im, (412, 42))
            speed_inside_im = rot_center(self.speed_inside_im, -(abs(self.speed) * 2.7 - 135))
            screen.blit(speed_inside_im, (419, 51))
            self.speed_slider.render(screen)
            speed_label = self.font.render(str(self.speed), True, (255, 255, 255))
            screen.blit(speed_label, (729, 44))
        elif self.tab == 1:
            round_label = self.font2.render(f"{self.tournament.round} Round / {self.total_rounds} Rounds",
                                            True, (255, 255, 255))
            screen.blit(round_label, (407, 35))
            cooperation_label = self.font2.render(
                f"{self.tournament.total_cooperation} Cooperated / {self.tournament.round} Rounds", True,
                (255, 255, 255))
            screen.blit(cooperation_label, (544, 58))
        elif self.tab == 2:
            self.show_statistics_button.render(screen, "Some statistics to show")

        pygame.draw.line(screen, (247, 95, 23), (0, 85), (100000, 85), 2)

        if self.show_zoom:
            zoom_label = self.font3.render(f"Zoom: {self.zoom}%", True, (255, 255, 255))
            screen.blit(zoom_label, (840, 97))

        # self.timeline.render(screen)

    def update(self):
        """Updates the blobs' status, and slider"""
        self.agents = self.tournament.get_agents()
        self.conductor = self.tournament.get_conductor()

        if self.new_generation:
            self.running = self.was_running
            self.new_generation = False
            self.blobs = dict()
        else:
            length = len(self.agents) + 1
            size = (38, 18)
            shift = 0
            while length > size[0] * size[1]:
                size = size[0] + 2, size[1] + 2
                shift += 1

            w = int(25 * self.zoom / 100)
            self.border = shift * w
            self.max_shift = (shift + 2) * w
            self.simulation_size_w_padding = (size[0] + 2) * w, (size[1] + 2) * w
            self.simulation_size_wo_padding = size[0] * w, size[1] * w
            self.min_shift_x = -self.simulation_size_w_padding[0] + 950 + shift * w
            self.min_shift_y = -self.simulation_size_w_padding[1] + 465 + shift * w

            if self.blobs:
                self.blobs[self.conductor].update(shift=(self.shift_x, self.shift_y), zoom=self.zoom, width=w)
                for agent in self.agents:
                    if agent == self.tournament.player1:
                        self.blobs[agent.index].update(receiver=True, shift=(self.shift_x, self.shift_y), zoom=self.zoom, width=w)
                        continue
                    if agent == self.tournament.player2:
                        self.blobs[agent.index].update(receiver=True, shift=(self.shift_x, self.shift_y), zoom=self.zoom, width=w)
                        continue
                    self.blobs[agent.index].update(shift=(self.shift_x, self.shift_y), zoom=self.zoom, width=w)
            else:
                zoom = self.zoom
                self.zoom = 100
                w = int(25 * self.zoom / 100)
                self.border = shift * w
                self.max_shift = (shift + 2) * w
                self.simulation_size_w_padding = (size[0] + 2) * w, (size[1] + 2) * w
                self.simulation_size_wo_padding = size[0] * w, size[1] * w
                self.min_shift_x = -self.simulation_size_w_padding[0] + 950 + shift * w
                self.min_shift_y = -self.simulation_size_w_padding[1] + 465 + shift * w
                self.min_zoom = int(465 / self.simulation_size_w_padding[1] * 100)
                self.zoom = zoom

                x = y = -shift
                self.blobs[self.conductor] = Blob((x, y), w, 20, self.conductor, conductor=True)
                x += 1
                for agent in self.agents:
                    self.blobs[agent.index] = Blob((x, y), w, 20, agent, player=True)
                    x += 1
                    if x == size[0] - shift:
                        x = -shift
                        y += 1

        self.speed_slider.update()
        if int(self.speed_slider.number) != self.speed:
            self.speed = int(self.speed_slider.number)

        self.home_tab.update(self.tab == self.home_tab.index)
        self.info_tab.update(self.tab == self.info_tab.index)
        self.graph_tab.update(self.tab == self.graph_tab.index)

        # self.timeline.update(self.tournament.time_stamp)

    def on_close(self, event):
        """Closes the window"""
        print(event)
        plt.ioff()
        plt.close(self.f1)

    def handle_events(self, events):
        """If the start button is pressed, starts the simulation; if the next button is pressed, gets the next round;
        if the slider is changed, changes the speed; if the reset button is pressed, goes back to the select agents
        scene; when the graph buttons are pressed, calls the plot_graph function"""
        Scene.handle_events(self, events)
        for event in events:
            if event.type == self.UPDATE:
                pygame.time.set_timer(self.UPDATE, self.speed, True)
                if self.running:
                    if next(self.run):
                        self.new_generation = True
                        self.was_running = self.running
                        self.running = False

            for agent in self.blobs:
                self.blobs[agent].handle_events(event)

            if self.tab == 0:
                self.speed_slider.handle_events(event)

                if self.reset_button.handle_events(event):
                    self.manager.go_to(self.manager.previous)

                if self.start_stop_button.handle_events(event):
                    self.running = not self.running

                if self.next_button.handle_events(event):
                    if next(self.run):
                        self.new_generation = True
                        self.was_running = self.running
                        self.running = False
            elif self.tab == 2:
                if self.show_statistics_button.handle_events(event):
                    print(self.tournament.get_agents_data())
                    plt.ion()
                    self.f1 = plt.figure(1)
                    self.f2 = plt.figure(2)
                    af1 = self.f1.add_subplot(111)
                    af2 = self.f2.add_subplot(111)
                    # self.f1.canvas.mpl_connect('close_event', self.on_close)
                    p1, = af1.plot(self.tournament.round, self.total_rounds)
                    p2, = af2.plot(self.tournament.round, self.total_rounds)
                    plt.show()
                    plt.pause(0.001)


            if self.check_shift:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 2:
                        self.shift = True

                if event.type == pygame.MOUSEBUTTONUP:
                    self.shift = False

                if event.type == pygame.MOUSEMOTION:
                    if self.shift:
                        self.shift_x += event.rel[0]
                        self.shift_y += event.rel[1]

                if self.shift_x < self.min_shift_x:
                    self.shift_x = self.min_shift_x
                if self.shift_x > self.max_shift:
                    self.shift_x = self.max_shift

                if self.shift_y < self.min_shift_y:
                    self.shift_y = self.min_shift_y
                if self.shift_y > self.max_shift:
                    self.shift_y = self.max_shift

            if event.type == pygame.MOUSEWHEEL:
                self.check_shift = True
                zoom = self.zoom
                if event.y != 0:
                    if self.zoom <= 200:
                        self.zoom += 25 * event.y
                    else:
                        self.zoom += 100 * event.y

                if self.zoom > self.max_zoom:
                    self.zoom = self.max_zoom
                elif self.zoom <= self.min_zoom:
                    self.zoom = self.min_zoom
                    zoom = self.zoom
                    shift_x = int((950 - self.simulation_size_w_padding[0]) / 2) + self.max_shift
                    shift_y = int((465 - self.simulation_size_w_padding[1]) / 2) + self.max_shift
                    self.min_shift_x = shift_x - 1
                    self.max_shift = shift_x + 1
                    self.shift_x = shift_x
                    self.shift_y = shift_y
                    self.check_shift = False
                if zoom != self.zoom:
                    mouse_pos = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - 87
                    new_pos = mouse_pos[0] * self.zoom / 100, mouse_pos[1] * self.zoom / 100
                    self.shift_x = int(mouse_pos[0] - new_pos[0])
                    self.shift_y = int(mouse_pos[1] - new_pos[1])

                self.show_zoom = True
                pygame.time.set_timer(self.BACK_TO_NORMAL, 600, True)

            if event.type == self.BACK_TO_NORMAL:
                self.show_zoom = False

            if event.type == pygame.KEYDOWN:
                if pygame.key.get_mods() and pygame.KMOD_ALT:
                    if event.key == pygame.K_h:
                        self.tab = self.home_tab.index
                    if event.key == pygame.K_i:
                        self.tab = self.info_tab.index
                    if event.key == pygame.K_g:
                        self.tab = self.graph_tab.index
                if event.key == pygame.K_SPACE:
                    self.running = not self.running
                if event.key == pygame.K_RIGHT:
                    if next(self.run):
                        self.new_generation = True
                        self.was_running = self.running
                        self.running = False

            if self.home_tab.handle_events(event):
                self.tab = self.home_tab.index
            if self.info_tab.handle_events(event):
                self.tab = self.info_tab.index
            if self.graph_tab.handle_events(event):
                self.tab = self.graph_tab.index

            # if info := self.timeline.handle_events(event):
            #     self.tournament.time_stamp, self.tournament.generation = info
            #     self.run = self.tournament.run(*info)
            #     self.new_generation = True
            #     next(self.run)
            #     self.was_running = self.running
            #     self.running = False
