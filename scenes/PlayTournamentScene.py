import random

import pygame

from objects import Blob, Button, RadioButton, Scene, DropdownItem, Slider, MessageBox, PositionDict

from components import Tournament


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
    tournament_manager: TournamentManager
        TournamentManager that takes control of switching between tournaments
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
    gossiping_agents: list
        List of gossiping agents
    watching_agents: list
        List of watching agents
    dr_rb: RadioButton
        Direct reciprocity radio button
    ir_rb: RadioButton
        Indirect reciprocity radio button
    true_rb: RadioButton
        Radio button for showing that agents having an option to chose if they want to play is true
    false_rb: RadioButton
        Radio button for showing that agents having an option to chose if they want to play is false
    start_stop_button: Button
        Button object to handle if the simulation is running or not
    next_step_button: Button
        Button object to get the next step if the simulation is not running
    reset_button: Button
        Button object to reset the game (return to the previous page)
    speed_slider: Slider
        Slider object to handle the simulation speed
    see_average_cooperation_button: Button
        Button to see statistics
    see_overall_payoff_button: Button
        Button to see statistics
    see_overall_payoff_agents_button: Button
        Button to see statistics
    see_number_of_agents_in_generation: Button
        Button to see statistics
    overall_payoff_by_round: list
        list of payoff amount every round (for displaying the graph)
    round: list
        list of round numbers (for displaying the graph)
    average_cooperation_by_round: list
        list of average cooperation every round (for displaying the graph)
    overall_payoff_agents_by_round: dict
        dictionary that stores distinct agent types payoff amount every round  (for displaying the graph)
    number_of_each_agent: dict
        dictionary that stores how many each distinct agent type has per round (for displaying the graph)
    message_box: MessageBox
        MessageBox object to ask the user if they want to continue to the next components
    selection1_rb: RadioButton
        First selection process radio button
    selection2_rb: RadioButton
        Second selection process radio button

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
        """
        Parameters
        ----------
        tournament_manager: TournamentManager
            TournamentManager that takes control of switching between tournaments
        """
        Scene.__init__(self)
        self.font = pygame.font.Font("Images/Montserrat-Regular.ttf", 21)
        self.font2 = pygame.font.Font("Images/Montserrat-Regular.ttf", 15)

        self.tournament = Tournament()
        self.run = self.tournament.start()
        self.agents = self.tournament.get_agents()
        self.conductors = self.tournament.get_conductors()
        self.blobs = dict()
        self.playing_agents = None

        self.running = False
        self.new_generation = False
        self.generation = self.tournament.generation
        self.total_generations = self.tournament.total_generations
        self.total_rounds = self.tournament.total_rounds
        self.total_giving_encounters = self.tournament.total_giving_encounters
        self.total_gossip_encounters = self.tournament.total_gossip_encounters

        self.UPDATE = pygame.USEREVENT + 1
        self.speed = 99
        pygame.time.set_timer(self.UPDATE, self.speed)

        self.tab = 0
        self.home_tab = DropdownItem(pygame.Rect(18, 8, 47, 19), 0, "Home", underline=0, font=15, center=False)
        self.info_tab = DropdownItem(pygame.Rect(89, 8, 29, 19), 1, "Info", underline=0, font=15, center=False)

        self.reset_button = Button(w=90, pos=(16, 39), center=True)
        self.start_stop_button = Button(w=80, pos=(130, 39), center=True)
        self.next_button = Button(w=80, pos=(234, 39), center=True)

        self.speed_label = self.font.render("Speed", True, (255, 255, 255))
        self.speed_outside_im = pygame.image.load("Images/speedometer_outside.png")
        self.speed_outside_im = pygame.transform.smoothscale(self.speed_outside_im, (30, 30))
        self.speed_inside_im = pygame.image.load("Images/speedometer_inside.png")
        self.speed_inside_im = pygame.transform.smoothscale(self.speed_inside_im, (15, 15))
        self.speed_slider = Slider((465, 57), 240, fro=5, to=100)

        self.message_box = MessageBox(400, 133)

    def render(self, screen):
        """Renders the blobs, buttons, radio buttons, labels and lines"""
        Scene.render(self, screen)

        self.home_tab.render(screen)
        self.info_tab.render(screen)

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
            generation_label = self.font2.render(
                f"{self.tournament.generation} Generation / {self.total_generations} Generations",
                True, (255, 255, 255))
            screen.blit(generation_label, (16, 35))
            round_label = self.font2.render(f"{self.tournament.round % self.total_rounds} Round / {self.total_rounds} Rounds",
                                            True, (255, 255, 255))
            screen.blit(round_label, (407, 35))
            giving_encounter_label = self.font2.render(
                f"{self.tournament.giving_encounters % self.total_giving_encounters} Giving Encounter / {self.total_giving_encounters} Rounds",
                True, (255, 255, 255))
            screen.blit(giving_encounter_label, (664, 35))
            gossip_encounter_label = self.font2.render(
                f"{self.tournament.gossip_encounters % self.total_gossip_encounters} Gossip Encounter / {self.total_gossip_encounters} Rounds",
                True, (255, 255, 255))
            screen.blit(gossip_encounter_label, (200, 58))
            encounter_type_label = self.font2.render(f"Encounter type: {self.tournament.encounter_type}",
                                                     True, (255, 255, 255))
            screen.blit(encounter_type_label, (544, 58))

        pygame.draw.line(screen, (247, 95, 23), (0, 85), (950, 85), 2)
        # pygame.draw.line(screen, (251, 164, 98), (0, 174), (284, 174), 3)
        # pygame.draw.line(screen, (251, 164, 98), (283, 0), (283, 175), 3)
        # pygame.draw.line(screen, (251, 164, 98), (283, 105), (950, 105), 3)
        # pygame.draw.line(screen, (251, 164, 98), (575, 0), (575, 105), 3)

        pos1 = pos2 = None
        if self.tournament.receiver_agent and self.tournament.giver_agent:
            pos1 = self.blobs[self.tournament.receiver_agent].pos
            pos2 = self.blobs[self.tournament.giver_agent].pos
        if self.tournament.gossiping_agents:
            pos1 = self.blobs[self.tournament.gossiping_agents[0]].pos
            pos2 = self.blobs[self.tournament.gossiping_agents[1]].pos

        render_after = []
        for agent in self.blobs:
            if self.blobs[agent].show_name:
                render_after.append(agent)
            if agent in [self.tournament.giver_agent, self.tournament.receiver_agent]:
                render_after.append(agent)
            if agent in self.tournament.gossiping_agents:
                render_after.append(agent)
            self.blobs[agent].render(screen, agent)

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
            pygame.draw.aaline(screen, color, (pos1[0]-2, pos1[1]), (pos2[0]-2, pos2[1]), blend=100)
            pygame.draw.aaline(screen, color, (pos1[0]-1, pos1[1]), (pos2[0]-1, pos2[1]), blend=100)
            pygame.draw.aaline(screen, color, pos1, pos2, blend=100)
            pygame.draw.aaline(screen, color, (pos1[0], pos1[1]-1), (pos2[0], pos2[1]-1), blend=100)
            pygame.draw.aaline(screen, color, (pos1[0], pos1[1]-2), (pos2[0], pos2[1]-2), blend=100)

        for ra in render_after:
            self.blobs[ra].render(screen, ra)

        if self.new_generation:
            self.message_box.render(screen, "Do you want to continue to a new tournament?")

    def update(self):
        """Updates the blobs status, messagebox, and slider"""
        self.agents = self.tournament.get_agents()
        self.conductors = self.tournament.get_conductors()

        if self.new_generation:
            if self.message_box.ask_again:
                self.message_box.show = True
            else:
                self.running = self.was_running
                self.new_generation = False
                self.message_box.show = False
                self.message_box.answer = ""
                self.blobs = dict()
            if self.message_box.answer == "yes":
                self.running = self.was_running
                self.new_generation = False
                self.message_box.show = False
                self.message_box.answer = ""
                self.blobs = dict()
            elif self.message_box.answer == "":
                pass
            else:
                pygame.quit()
                exit(0)
        else:
            if self.blobs:
                for agent in self.agents:
                    if agent == self.tournament.giver_agent:
                        self.blobs[agent].update(giver=True)
                        continue
                    if agent == self.tournament.receiver_agent:
                        self.blobs[agent].update(receiver=True)
                        continue
                    if agent in self.tournament.gossiping_agents:
                        self.blobs[agent].update(gossiping=True)
                        continue
                    self.blobs[agent].update()
            else:
                positions = PositionDict()
                # positions[(range(0, 295), range(80, 185))] = ""
                x = 474
                y = 317
                positions[(range(x - 16, x + 16), range(y - 16, y + 16))] = ""
                self.blobs[self.conductors[0]] = Blob((x, y), conductor=True)
                for agent in self.agents:
                    x = random.randrange(10, 940)
                    y = random.randrange(95, 540)
                    cont = True
                    while cont:
                        try:
                            if positions[(x, y)] == "":
                                x = random.randrange(10, 940)
                                y = random.randrange(95, 540)
                        except KeyError:
                            cont = False

                    positions[(range(x - 16, x + 16), range(y - 16, y + 16))] = ""
                    self.blobs[agent] = Blob((x, y), player=True)
                del positions

        self.speed_slider.update()
        if int(self.speed_slider.number) != self.speed:
            self.speed = int(self.speed_slider.number)
            pygame.time.set_timer(self.UPDATE, self.speed)

        self.home_tab.update(self.tab == self.home_tab.index)
        self.info_tab.update(self.tab == self.info_tab.index)

    def handle_events(self, events):
        """If the start button is pressed, starts the simulation; if the next button is pressed, gets the next round;
        if the slider is changed, changes the speed; if the reset button is pressed, goes back to the select agents
        scene; when the graph buttons are pressed, calls the plot_graph function"""
        Scene.handle_events(self, events)

        for event in events:
            if not self.message_box.handle_events(event):
                self.speed_slider.handle_events(event)

                for agent in self.blobs:
                    self.blobs[agent].handle_events(event, agent)

                if self.reset_button.handle_events(event):
                    self.manager.go_to(self.manager.previous)

                if self.start_stop_button.handle_events(event):
                    self.running = not self.running

                if event.type == self.UPDATE and self.running:
                    if next(self.run):
                        self.new_generation = True
                        self.was_running = self.running
                        self.running = False

                if self.next_button.handle_events(event):
                    if next(self.run):
                        self.new_generation = True
                        self.was_running = self.running
                        self.running = False

                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_mods() and pygame.KMOD_ALT:
                        if event.key == pygame.K_h:
                            self.tab = self.home_tab.index
                        if event.key == pygame.K_i:
                            self.tab = self.info_tab.index
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
