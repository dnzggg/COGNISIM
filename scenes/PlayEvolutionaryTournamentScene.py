import pygame

from objects import Blob, Button, Scene, DropdownItem, Slider, MessageBox, PositionDict, Timeline

from components import EvolutionaryTournament


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class PlayEvolutionaryTournamentScene(Scene):
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
    back_button: Button
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

    def __init__(self, file_name):
        Scene.__init__(self)
        size = pygame.display.get_window_size()
        pygame.display.set_mode((size[0], size[1]), pygame.RESIZABLE)

        self.font = pygame.font.Font("Images/Montserrat-Regular.ttf", 21)
        self.font2 = pygame.font.Font("Images/Montserrat-Regular.ttf", 15)
        self.font3 = pygame.font.Font("Images/Montserrat-ExtraBold.ttf", 15)

        self.tournament = EvolutionaryTournament(file_name)
        self.run = self.tournament.start()
        self.agents = self.tournament.get_agents()
        self.conductors = self.tournament.get_conductors()
        self.blobs = dict()
        self.playing_agents = None

        self.running = False
        self.was_running = False
        self.new_generation = False
        self.total_generations = self.tournament.total_generations
        self.total_rounds = self.tournament.total_rounds
        self.total_giving_encounters = self.tournament.total_giving_encounters
        self.total_gossip_encounters = self.tournament.total_gossip_encounters

        self.UPDATE = pygame.USEREVENT + 1
        self.speed = 99
        pygame.time.set_timer(self.UPDATE, self.speed, True)

        self.tab = 0
        self.home_tab = DropdownItem(pygame.Rect(18, 8, 47, 19), 0, "Home", underline=0, font=15, center=False)
        self.edit_tab = DropdownItem(pygame.Rect(89, 8, 30, 19), 1, "Edit", underline=0, font=15, center=False)
        self.info_tab = DropdownItem(pygame.Rect(143, 8, 29, 19), 2, "Info", underline=0, font=15, center=False)
        self.graph_tab = DropdownItem(pygame.Rect(196, 8, 47, 19), 3, "Graph", underline=0, font=15, center=False)

        self.back_button = Button(w=80, pos=(133, 39), center=True)
        self.home_button = Button(w=93, pos=(16, 39), center=True)
        self.start_stop_button = Button(w=80, pos=(237, 39), center=True)
        self.next_button = Button(w=80, pos=(341, 39), center=True)

        self.speed_label = self.font.render("Speed", True, (255, 255, 255))
        self.speed_outside_im = pygame.image.load("Images/speedometer_outside.png")
        self.speed_outside_im = pygame.transform.smoothscale(self.speed_outside_im, (30, 30))
        self.speed_inside_im = pygame.image.load("Images/speedometer_inside.png")
        self.speed_inside_im = pygame.transform.smoothscale(self.speed_inside_im, (15, 15))
        self.speed_slider = Slider((572, 57), 240, fro=5, to=100)

        self.load_button = Button(w=208, pos=(18, 39), center=True)
        self.new_experiment_button = Button(w=279, pos=(250, 39), center=True)

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

        self.timeline = Timeline(rounds=self.total_rounds)

    def render(self, screen):
        """Renders the blobs, buttons, radio buttons, labels and lines"""
        Scene.render(self, screen)

        pos1 = pos2 = None
        if self.tournament.receiver_agent and self.tournament.giver_agent:
            pos1 = self.blobs[self.tournament.receiver_agent].get_pos()
            pos2 = self.blobs[self.tournament.giver_agent].get_pos()
        if self.tournament.gossiping_agents:
            pos1 = self.blobs[self.tournament.gossiping_agents[0]].get_pos()
            pos2 = self.blobs[self.tournament.gossiping_agents[1]].get_pos()

        render_after = []
        for agent in self.blobs:
            w, h = pygame.display.get_window_size()
            if 0 - self.blobs[agent].radius / 2 < self.blobs[agent].get_pos()[0] < w + self.blobs[agent].radius / 2:
                if 87 - self.blobs[agent].radius / 2 < self.blobs[agent].get_pos()[1] < h + self.blobs[agent].radius / 2:
                    if self.blobs[agent].show_name:
                        render_after.append(agent)
                    if agent in [self.tournament.giver_agent, self.tournament.receiver_agent]:
                        render_after.append(agent)
                    if agent in self.tournament.gossiping_agents:
                        render_after.append(agent)
                    self.blobs[agent].render(screen)

        if pos1 and pos2:
            color = (255, 255, 255)
            if self.tournament.encounter_type == "Gossip":
                if self.tournament.gossip:
                    color = (0, 0, 255)
            else:
                if self.tournament.cooperate is not None:
                    if self.tournament.cooperate:
                        color = (0, 255, 0)
                    else:
                        color = (255, 0, 0)
            pygame.draw.aaline(screen, color, (pos1[0] - 2, pos1[1]), (pos2[0] - 2, pos2[1]), blend=100)
            pygame.draw.aaline(screen, color, (pos1[0] - 1, pos1[1]), (pos2[0] - 1, pos2[1]), blend=100)
            pygame.draw.aaline(screen, color, pos1, pos2, blend=100)
            pygame.draw.aaline(screen, color, (pos1[0], pos1[1] - 1), (pos2[0], pos2[1] - 1), blend=100)
            pygame.draw.aaline(screen, color, (pos1[0], pos1[1] - 2), (pos2[0], pos2[1] - 2), blend=100)

        for ra in render_after:
            self.blobs[ra].render(screen)

        pygame.draw.rect(screen, (30, 30, 30), (0, 0, 100000, 85))

        self.home_tab.render(screen)
        self.edit_tab.render(screen)
        self.info_tab.render(screen)
        self.graph_tab.render(screen)

        if self.tab == 0:
            self.back_button.render(screen, "Back")
            self.home_button.render(screen, "Home")
            # self.prev_button.render(screen, "Prev")
            if not self.running:
                self.start_stop_button.render(screen, "Play")
            else:
                self.start_stop_button.render(screen, "Stop")
            self.next_button.render(screen, "Next")

            screen.blit(self.speed_label, (445, 42))
            screen.blit(self.speed_outside_im, (519, 42))
            speed_inside_im = rot_center(self.speed_inside_im, -(abs(self.speed) * 2.7 - 135))
            screen.blit(speed_inside_im, (526, 51))
            self.speed_slider.render(screen)
            speed_label = self.font.render(str(self.speed), True, (255, 255, 255))
            screen.blit(speed_label, (836, 44))
        elif self.tab == 1:
            self.load_button.render(screen, "Load Experiment")
            self.new_experiment_button.render(screen, "Create New Experiment")
        elif self.tab == 2:
            generation_label = self.font2.render(
                f"{self.tournament.generation} Generation / {self.total_generations} Generations",
                True, (255, 255, 255))
            screen.blit(generation_label, (16, 35))
            round_label = self.font2.render(f"{self.tournament.round} Round / {self.total_rounds} Rounds",
                                            True, (255, 255, 255))
            screen.blit(round_label, (407, 35))
            giving_encounter_label = self.font2.render(
                f"{self.tournament.giving_encounters} Giving Encounter / {self.total_giving_encounters} Rounds",
                True, (255, 255, 255))
            screen.blit(giving_encounter_label, (664, 35))
            gossip_encounter_label = self.font2.render(
                f"{self.tournament.gossip_encounters} Gossip Encounter / {self.total_gossip_encounters} Rounds",
                True, (255, 255, 255))
            screen.blit(gossip_encounter_label, (200, 58))
            encounter_type_label = self.font2.render(f"Encounter type: {self.tournament.encounter_type}",
                                                     True, (255, 255, 255))
            screen.blit(encounter_type_label, (544, 58))
        elif self.tab == 3:
            pass
            # self.show_statistics_button.render(screen, "Player 1 statistics")
            # self.show_statistics_button2.render(screen, "Player 2 statistics")
            # self.show_statistics_button3.render(screen, "Overall statistics")

        pygame.draw.line(screen, (247, 95, 23), (0, 85), (100000, 85), 2)

        if self.show_zoom:
            zoom_label = self.font3.render(f"Zoom: {self.zoom}%", True, (255, 255, 255))
            screen.blit(zoom_label, (840, 97))

        self.timeline.render(screen)

    def update(self):
        """Updates the blobs' status, and slider"""
        self.agents = self.tournament.get_agents()
        self.conductors = self.tournament.get_conductors()

        if self.new_generation:
            self.running = self.was_running
            self.new_generation = False
            self.blobs = dict()
        else:
            length = len(self.agents) + len(self.conductors)
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
                self.blobs[self.conductors[0]].update(shift=(self.shift_x, self.shift_y), zoom=self.zoom, width=w)
                for agent in self.agents:
                    if agent == self.tournament.giver_agent:
                        self.blobs[agent].update(giver=True, shift=(self.shift_x, self.shift_y), zoom=self.zoom,
                                                 width=w)
                        continue
                    if agent == self.tournament.receiver_agent:
                        self.blobs[agent].update(receiver=True, shift=(self.shift_x, self.shift_y), zoom=self.zoom,
                                                 width=w)
                        continue
                    if agent in self.tournament.gossiping_agents:
                        self.blobs[agent].update(gossiping=True, shift=(self.shift_x, self.shift_y), zoom=self.zoom,
                                                 width=w)
                        continue
                    self.blobs[agent].update(shift=(self.shift_x, self.shift_y), zoom=self.zoom, width=w)
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
                for agent in self.agents:
                    if x == int(size[0] / 2) - shift and y == int(size[1] / 2) - shift:
                        self.blobs[self.conductors[0]] = Blob((x, y), w, 20, self.conductors[0], conductor=True)
                        x += 1
                    self.blobs[agent] = Blob((x, y), w, 20, agent, player=True)
                    x += 1
                    if x == size[0] - shift:
                        x = -shift
                        y += 1

        self.speed_slider.update()
        if int(self.speed_slider.number) != self.speed:
            self.speed = int(self.speed_slider.number)

        self.home_tab.update(self.tab == self.home_tab.index)
        self.edit_tab.update(self.tab == self.edit_tab.index)
        self.info_tab.update(self.tab == self.info_tab.index)
        self.graph_tab.update(self.tab == self.graph_tab.index)

        self.timeline.update(self.tournament.round)

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
                self.blobs[agent].handle_events(event, manager=self.manager, round=self.tournament.time_stamp)

            if self.tab == 0:
                self.speed_slider.handle_events(event)

                if self.back_button.handle_events(event):
                    self.manager.go_back()

                if self.home_button.handle_events(event):
                    self.manager()

                if self.start_stop_button.handle_events(event):
                    self.running = not self.running

                if self.next_button.handle_events(event):
                    if next(self.run):
                        self.new_generation = True
                        self.was_running = self.running
                        self.running = False
            elif self.tab == 1:
                if self.load_button.handle_events(event):
                    self.manager.go_to("SelectFileScene", "Evolutionary")
                if self.new_experiment_button.handle_events(event):
                    self.manager.go_to("SelectEvolutionaryAgentsScene")

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
                    if event.key == pygame.K_e:
                        self.tab = self.edit_tab.index
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
            if self.edit_tab.handle_events(event):
                self.tab = self.edit_tab.index
            if self.info_tab.handle_events(event):
                self.tab = self.info_tab.index
            if self.graph_tab.handle_events(event):
                self.tab = self.graph_tab.index

            if info := self.timeline.handle_events(event):
                self.tournament.round, self.generation = info
