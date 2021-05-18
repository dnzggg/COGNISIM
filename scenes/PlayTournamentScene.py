import random

import pygame

from components import Blob, Button, RadioButton, Scene, Graph, Slider, MessageBox, PositionDict


class PlayTournamentScene(Scene):
    """Scene where the user can see the simulation and interact with its components.
    
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
        Store if the tournament is over or not
    run: Tournament.start()
        Method that initializes the tournament
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
        MessageBox object to ask the user if they want to continue to the next tournament
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
    def __init__(self, tournament_manager):
        """
        Parameters
        ----------
        tournament_manager: TournamentManager
            TournamentManager that takes control of switching between tournaments
        """
        Scene.__init__(self)
        self.font = pygame.font.Font("Images/Montserrat-Regular.ttf", 15)

        self.tournament_manager = tournament_manager

        self.running = False
        self.was_running = False
        self.new_generation = False
        self.run = self.tournament_manager.tournament.start()

        self.UPDATE = pygame.USEREVENT + 1
        self.speed = 99
        pygame.time.set_timer(self.UPDATE, self.speed)

        self.blobs = dict()

        self.agents = None
        self.playing_agents = None
        self.gossiping_agents = None
        self.watching_agents = None

        if self.tournament_manager.tournament.__class__.__name__ == "DirectReciprocity":
            self.dr_rb = RadioButton(pos=(20, 62), on=True, disabled=True)
            self.ir_rb = RadioButton(pos=(180, 62), disabled=True)
        else:
            self.dr_rb = RadioButton(pos=(20, 62), disabled=True)
            self.ir_rb = RadioButton(pos=(180, 62), on=True, disabled=True)

        if self.tournament_manager.tournament.choose_opponent:
            self.false_rb = RadioButton(pos=(360, 62), disabled=True)
            self.true_rb = RadioButton(pos=(440, 62), on=True, disabled=True)
        else:
            self.false_rb = RadioButton(pos=(360, 62), on=True, disabled=True)
            self.true_rb = RadioButton(pos=(440, 62), disabled=True)

        if self.tournament_manager.tournament.selection.__class__.__name__ == "Selection2":
            self.selection1_rb = RadioButton(pos=(185, 100), disabled=True)
            self.selection2_rb = RadioButton(pos=(235, 100), on=True, disabled=True)
        else:
            self.selection1_rb = RadioButton(pos=(185, 100), on=True, disabled=True)
            self.selection2_rb = RadioButton(pos=(235, 100), disabled=True)

        self.start_stop_button = Button(pos=(520, 45), w=75, h=30)
        self.next_step_button = Button(pos=(600, 45), w=70, h=30)
        self.reset_button = Button(pos=(520, 10), w=75, h=30)
        self.speed_slider = Slider(pos=(630, 20))

        self.see_average_cooperation_button = Button(pos=(730, 80), w=210, h=110, font_size=26)
        self.see_overall_payoff_button = Button(pos=(730, 203), w=210, h=80, font_size=26)
        self.see_overall_payoff_agents_button = Button(pos=(730, 297), w=210, h=110, font_size=26)
        self.see_number_of_agents_in_generation = Button(pos=(730, 420), w=210, h=110, font_size=26)

        self.overall_payoff_by_round = []
        self.round = []
        self.average_cooperation_by_round = []
        self.overall_payoff_agents_by_round = dict()
        self.number_of_each_agent = dict()
        self.generation = []

        self.message_box = MessageBox(400, 133)

    def render(self, screen):
        """Renders the blobs, buttons, radio buttons, labels and lines"""
        Scene.render(self, screen)

        tournament_type_label = self.font.render("Tournament Type", True, (255, 255, 255))
        screen.blit(tournament_type_label, (120, 12))
        dr_label = self.font.render("Direct reciprocity", True, (155, 155, 155))
        screen.blit(dr_label, (35, 50))
        ir_label = self.font.render("Indirect reciprocity", True, (155, 155, 155))
        screen.blit(ir_label, (195, 50))
        self.dr_rb.render(screen)
        self.ir_rb.render(screen)

        pygame.draw.line(screen, (255, 255, 255), (335, 0), (335, 80))

        choose_opponent_label = self.font.render("Choose Opponent", True, (255, 255, 255))
        screen.blit(choose_opponent_label, (355, 12))
        false_label = self.font.render("False", True, (155, 155, 155))
        screen.blit(false_label, (380, 50))
        true_label = self.font.render("True", True, (155, 155, 155))
        screen.blit(true_label, (460, 50))
        self.false_rb.render(screen)
        self.true_rb.render(screen)

        pygame.draw.line(screen, (255, 255, 255), (505, 0), (505, 80))

        if self.running:
            self.start_stop_button.render(screen, "Stop")
        else:
            self.start_stop_button.render(screen, "Start")

        self.next_step_button.render(screen, "Next")
        self.reset_button.render(screen, "Reset")

        pygame.draw.line(screen, (255, 255, 255), (610, 0), (610, 37))
        pygame.draw.line(screen, (255, 255, 255), (610, 37), (710, 37))

        selection_label = self.font.render("Selection process:", True, (255, 255, 255))
        screen.blit(selection_label, (35, 88))
        selection1_label = self.font.render("1", True, (255, 255, 255))
        screen.blit(selection1_label, (205, 88))
        selection2_label = self.font.render("2", True, (255, 255, 255))
        screen.blit(selection2_label, (255, 88))
        self.selection1_rb.render(screen)
        self.selection2_rb.render(screen)

        pygame.draw.line(screen, (255, 255, 255), (0, 115), (280, 115))
        pygame.draw.line(screen, (255, 255, 255), (280, 80), (280, 115))

        self.speed_slider.render(screen)
        speed_label = self.font.render("Speed: " + str(self.speed), True, (255, 255, 255))
        screen.blit(speed_label, (770, 40))

        self.see_average_cooperation_button.render(screen, "Average cooperation per round")
        self.see_overall_payoff_button.render(screen, "Overall payoff per round")
        self.see_overall_payoff_agents_button.render(screen, "Overall payoff of agents per round")
        self.see_number_of_agents_in_generation.render(screen, "Number of agents per generation")

        pygame.draw.line(screen, (255, 255, 255), (0, 80), (710, 80))
        pygame.draw.line(screen, (255, 255, 255), (710, 37), (710, 700))

        round_label = self.font.render("Round: " + str(len(self.tournament_manager.tournament.get_round())), True,
                                       (255, 255, 255))
        screen.blit(round_label, (300, 88))

        generation_label = self.font.render(
            "Generation: " + str(len(self.tournament_manager.tournament.get_generation()) - 1), True, (255, 255, 255))
        screen.blit(generation_label, (390, 88))

        for agent in self.blobs:
            self.blobs[agent].render(screen)

        if self.new_generation:
            self.message_box.render(screen, "Do you want to continue to a new tournament?")

    def update(self):
        """Updates the blobs status, messagebox, and slider"""
        self.speed_slider.update()

        self.agents = self.tournament_manager.tournament.agents_to_play
        self.playing_agents = self.tournament_manager.tournament.get_agents_playing()
        self.watching_agents = self.tournament_manager.tournament.get_watching_agents()
        self.gossiping_agents = self.tournament_manager.tournament.get_gossiping_agents()

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
                    if self.watching_agents:
                        if agent in self.watching_agents:
                            self.blobs[agent].update(watching=True)
                            continue
                    if self.gossiping_agents:
                        if agent in self.gossiping_agents:
                            self.blobs[agent].update(gossiping=True)
                            continue
                    self.blobs[agent].update()
            else:
                positions = PositionDict()
                positions[(range(0, 540), range(80, 125))] = ""
                for agent in self.agents:
                    x = random.randrange(10, 700)
                    y = random.randrange(95, 540)
                    cont = True
                    while cont:
                        try:
                            if positions[(x, y)] == "":
                                x = random.randrange(10, 700)
                                y = random.randrange(95, 540)
                        except KeyError:
                            cont = False

                    positions[(range(x-16, x+16), range(y-16, y+16))] = ""

                    if self.playing_agents:
                        if agent in self.playing_agents:
                            self.blobs[agent] = Blob((x, y), playing=True)
                            continue
                    if self.watching_agents:
                        if agent in self.watching_agents:
                            self.blobs[agent] = Blob((x, y), watching=True)
                            continue
                    if self.gossiping_agents:
                        if agent in self.gossiping_agents:
                            self.blobs[agent] = Blob((x, y), gossiping=True)
                            continue
                    self.blobs[agent] = Blob((x, y))
                del positions

    def handle_events(self, events):
        """If the start button is pressed, starts the simulation; if the next button is pressed, gets the next round;
        if the slider is changed, changes the speed; if the reset button is pressed, goes back to the select agents
        scene; when the graph buttons are pressed, calls the plot_graph function"""
        Scene.handle_events(self, events)

        for event in events:
            self.message_box.handle_events(event)

            self.start_stop_button.handle_events(event)
            self.next_step_button.handle_events(event)
            self.reset_button.handle_events(event)

            self.see_average_cooperation_button.handle_events(event)
            self.see_overall_payoff_button.handle_events(event)
            self.see_overall_payoff_agents_button.handle_events(event)
            self.see_number_of_agents_in_generation.handle_events(event)
            self.speed_slider.handle_events(event)

            for agent in self.blobs:
                self.blobs[agent].handle_events(event, agent)

            if event.type == self.UPDATE and self.running:
                if next(self.run):
                    self.new_generation = True
                    self.was_running = self.running
                    self.running = False

            if self.reset_button.clicked(event):
                self.manager.go_to(self.manager.previous)

            if self.start_stop_button.clicked(event):
                if self.running:
                    self.running = False
                else:
                    self.running = True

            if self.next_step_button.clicked(event):
                if next(self.run):
                    self.new_generation = True
                    self.was_running = self.running
                    self.running = False

            if int(self.speed_slider.number) != self.speed:
                self.speed = int(self.speed_slider.number)
                pygame.time.set_timer(self.UPDATE, self.speed)

            if self.see_average_cooperation_button.clicked(event):
                self.average_cooperation_by_round = self.tournament_manager.tournament.get_average_cooperation_by_round()
                self.round = self.tournament_manager.tournament.get_round()

                self.plot_graph("Average-Cooperation", self.round, self.average_cooperation_by_round, "Round",
                                "Average Cooperation", "Average Cooperation per Round")

            if self.see_overall_payoff_button.clicked(event):
                self.overall_payoff_by_round = self.tournament_manager.tournament.get_overall_payoff_by_round()
                self.round = self.tournament_manager.tournament.get_round()

                self.plot_graph("Overall-Payoff", self.round, self.overall_payoff_by_round, "Round",
                                "Overall Payoff", "Overall Payoff per Round")

            if self.see_overall_payoff_agents_button.clicked(event):
                self.overall_payoff_agents_by_round = \
                    self.tournament_manager.tournament.get_overall_payoff_agents_by_rounds()
                self.round = self.tournament_manager.tournament.get_round()

                self.plot_graph("Overall-Payoff-Agent", self.round, self.overall_payoff_agents_by_round, "Round",
                                "Overall Payoff", "Overall Payoff per Round of Agents")

            if self.see_number_of_agents_in_generation.clicked(event):
                self.number_of_each_agent = self.tournament_manager.tournament.get_number_of_agents()
                self.generation = self.tournament_manager.tournament.get_generation()

                self.plot_graph("Number-Agent", self.generation, self.number_of_each_agent, "Generation",
                                "Number of Agent", "Number of agents per generation")

    def plot_graph(self, name, xs, ys, x_label, y_label, title):
        """Creates a Graph object, adds it to the list of graphs

        Parameters
        ----------
        name: str
            key for the dictionary so that if the user wants to click on the button again, it will lift the graph rather
            than create a new one
        xs: list
            the data of the x axis
        ys: list
            the data of the y axis
        x_label: str
            the title for the x axis
        y_label: str
            the title for the y axis
        title: str
            the title for the graph
        """
        if name in self.manager.graphs:
            self.manager.graphs[name].graph.lift()
        else:
            graph = Graph.Graph(self.manager.tk, xs, ys, x_label,
                                y_label, title)
            self.manager.graphs[name] = graph
