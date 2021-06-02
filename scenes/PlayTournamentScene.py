import random

import pygame

from objects import Blob, Button, RadioButton, Scene, Graph, Slider, MessageBox, PositionDict

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
        self.total_generations = 100
        self.round = self.tournament.round
        self.total_rounds = 1000
        self.giving_encounter = 150
        self.total_giving_encounters = 1000
        self.gossip_encounter = 150
        self.total_gossip_encounters = 1000
        self.encounter_type = "Giving"

        self.UPDATE = pygame.USEREVENT + 1
        self.speed = 99
        pygame.time.set_timer(self.UPDATE, self.speed)

        self.reset_button = Button(w=90, pos=(386, 11), center=True)
        self.prev_button = Button(w=80, pos=(297, 62), center=True)
        self.start_stop_button = Button(w=80, pos=(391, 62), center=True)
        self.next_button = Button(w=80, pos=(484, 62), center=True)

        self.speed_label = self.font.render("Speed", True, (255, 255, 255))
        self.speed_outside_im = pygame.image.load("Images/speedometer_outside.png")
        self.speed_outside_im = pygame.transform.smoothscale(self.speed_outside_im, (30, 30))
        self.speed_inside_im = pygame.image.load("Images/speedometer_inside.png")
        self.speed_inside_im = pygame.transform.smoothscale(self.speed_inside_im, (15, 15))
        self.speed_slider = Slider((642, 64), 240, fro=5, to=100)

        self.message_box = MessageBox(400, 133)

    def render(self, screen):
        """Renders the blobs, buttons, radio buttons, labels and lines"""
        Scene.render(self, screen)

        generation_label = self.font2.render(f"{self.tournament.generation} Generation / {self.total_generations} Generations",
                                             True, (255, 255, 255))
        screen.blit(generation_label, (8, 8))
        round_label = self.font2.render(f"{self.tournament.round} Round / {self.total_rounds} Rounds",
                                        True, (255, 255, 255))
        screen.blit(round_label, (8, 43))
        giving_encounter_label = self.font2.render(
            f"{self.giving_encounter} Giving Encounter / {self.total_giving_encounters} Rounds",
            True, (255, 255, 255))
        screen.blit(giving_encounter_label, (8, 78))
        gossip_encounter_label = self.font2.render(
            f"{self.gossip_encounter} Gossip Encounter / {self.total_gossip_encounters} Rounds",
            True, (255, 255, 255))
        screen.blit(gossip_encounter_label, (8, 113))
        encounter_type_label = self.font2.render(f"Encounter type: {self.total_generations}",
                                                 True, (255, 255, 255))
        screen.blit(encounter_type_label, (8, 148))

        self.reset_button.render(screen, "Reset")
        self.prev_button.render(screen, "Prev")
        if not self.running:
            self.start_stop_button.render(screen, "Start")
        else:
            self.start_stop_button.render(screen, "Stop")
        self.next_button.render(screen, "Next")

        screen.blit(self.speed_label, (589, 8))
        screen.blit(self.speed_outside_im, (589, 49))
        speed_inside_im = rot_center(self.speed_inside_im, -(abs(self.speed) * 2.7 - 135))
        screen.blit(speed_inside_im, (596, 56))
        self.speed_slider.render(screen)
        speed_label = self.font.render(str(self.speed), True, (255, 255, 255))
        screen.blit(speed_label, (906, 51))

        pygame.draw.line(screen, (251, 164, 98), (0, 174), (284, 174), 3)
        pygame.draw.line(screen, (251, 164, 98), (283, 0), (283, 175), 3)
        pygame.draw.line(screen, (251, 164, 98), (283, 105), (950, 105), 3)
        pygame.draw.line(screen, (251, 164, 98), (575, 0), (575, 105), 3)
        pygame.draw.line(screen, (251, 164, 98), (734, 106), (734, 550), 3)

        for agent in self.blobs:
            self.blobs[agent].render(screen)

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
                    if self.playing_agents:
                        if agent in self.playing_agents:
                            self.blobs[agent].update(playing=True)
                            continue
                    self.blobs[agent].update()
            else:
                positions = PositionDict()
                positions[(range(0, 295), range(80, 185))] = ""
                for agent in (self.conductors + self.agents):
                    x = random.randrange(10, 725)
                    y = random.randrange(115, 540)
                    cont = True
                    while cont:
                        try:
                            if positions[(x, y)] == "":
                                x = random.randrange(10, 725)
                                y = random.randrange(115, 540)
                        except KeyError:
                            cont = False

                    positions[(range(x - 15, x + 15), range(y - 15, y + 15))] = ""
                    if agent.conductor:
                        self.blobs[agent] = Blob((x, y), conductor=True)
                    else:
                        self.blobs[agent] = Blob((x, y), player=True)
                del positions

        self.speed_slider.update()
        if int(self.speed_slider.number) != self.speed:
            self.speed = int(self.speed_slider.number)
            pygame.time.set_timer(self.UPDATE, self.speed)

    def handle_events(self, events):
        """If the start button is pressed, starts the simulation; if the next button is pressed, gets the next round;
        if the slider is changed, changes the speed; if the reset button is pressed, goes back to the select agents
        scene; when the graph buttons are pressed, calls the plot_graph function"""
        Scene.handle_events(self, events)

        for event in events:
            self.speed_slider.handle_events(event)
            self.message_box.handle_events(event)
            if self.reset_button.handle_events(event):
                self.manager.go_to(self.manager.previous)

            if self.prev_button.handle_events(event):
                print("prev")

            if self.start_stop_button.handle_events(event):
                self.tournament.start()
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
