import os
import re

from pyswip import Prolog

import pygame
from pygame import gfxdraw

from objects import Button, InputBox, RadioButton, Scene, Dropdown, HorizontalScroll, Chip, DropdownItem, TextButton


class SelectAxelrodAgentsScene(Scene):
    """Select agents scene where the user can select the amount of agents and number of rounds.

    Attributes
    ----------
    font: pygame.font.Font
        Font that is to be used in this scene
    tournament_manager: TournamentManager
        TournamentManager that takes control of switching between tournaments.
    dr_rb: RadioButton
        Direct reciprocity radio button
    ir_rb: RadioButton
        Indirect reciprocity radio button
    true_rb: RadioButton
        Radio button for asking that agents having an option to chose if they want to play is true
    false_rb: RadioButton
        Radio button for asking that agents having an option to chose if they want to play is false
    input_boxes: list [InputBox]
        list of input boxes where the user enters the amount of agents they want
    input_label: list [pygame.Surface]
        list of labels for the input boxes
    round_input_box: InputBox
        input box to ask the user the number of rounds they want
    start_button: Button
        The button that will take the user to the playing screen
    user_input: list
        list that will store the values the user has chosen
    selection: int
        Stores the selection process the user chose
    selection1_rb: RadioButton
        First selection process radio button
    selection2_rb: RadioButton
        Second selection process radio button

    Methods
    -------
    render(screen)
        Renders the radio buttons for components selection, labels for description, input boxes to get the values, and
        the button
    update()
        Update input box text, and radio buttons
    get_user_input()
        Gets user input from input boxes
    handle_events(events)
        Handles all the objects events, and when the button is pressed will move to the next scene
    """
    def __init__(self, exp_name=None):
        Scene.__init__(self)
        self.font = pygame.font.Font("Images/Montserrat-Regular.ttf", 21)
        self.font2 = pygame.font.Font("Images/Montserrat-Regular.ttf", 15)
        self.font3 = pygame.font.Font("Images/Montserrat-Regular.ttf", 28)

        self.back_button = TextButton(pos=(16, 16), w=69, h=25, font_size=21)
        self.execute_button = Button(w=111, pos=(823, 499), font_size=21)

        self.player_label = self.font.render("Player Agent", True, (255, 255, 255))
        self.strategy_type_list = ["All C", "All D", "Tit For Tat", "Spiteful", "Soft Majo", "Hard Majo", "Per DDC",
                                   "Per CCD", "Per CD", "Mistrust", "Pavlov", "Tf2t", "Hard Tft", "Slow Tft", "Gradual",
                                   "Prober", "Mem2"]
        self.strategy_type_dropdown = Dropdown("Strategy Type", w=193, pos=(314, 16), selections=self.strategy_type_list)

        self.number_of_players_label = self.font2.render("Number of Players:", True, (255, 255, 255))
        self.number_of_players_input = InputBox((705, 16), w=101, h=27, text="1000")

        self.add_button = Button(w=75, pos=(859, 12), center=True)

        self.added = []
        self.agents = []
        self.agents2 = []
        self.chips = []
        self.scroll = HorizontalScroll(items=self.chips, pos=(16, 67))

        self.p_label = self.font2.render("Value of P:", True, (255, 255, 255))
        self.p_input = InputBox((102, 171), w=101, h=27, text="1")
        self.r_label = self.font2.render("Value of R:", True, (255, 255, 255))
        self.r_input = InputBox((320, 171), w=101, h=27, text="3")
        self.s_label = self.font2.render("Value of S:", True, (255, 255, 255))
        self.s_input = InputBox((102, 238), w=101, h=27, text="0")
        self.t_label = self.font2.render("Value of T:", True, (255, 255, 255))
        self.t_input = InputBox((320, 238), w=101, h=27, text="5")
        self.p = 1
        self.r = 3
        self.s = 0
        self.t = 5

        self.number_of_rounds_label = self.font2.render("Total Number of Rounds:", True, (255, 255, 255))
        self.number_of_rounds_input = InputBox((211, 370), w=101, h=27, text="1000")

        self.start_time_label = self.font2.render("Start Time:", True, (255, 255, 255))
        self.start_time_input = InputBox((105, 304), w=101, h=27, text="10")

        self.events_file_name_label = self.font2.render("Events File Name:", True, (255, 255, 255))
        self.events_file_name_input = InputBox((162, 437), w=236, h=27, text="example.event", file=True)
        self.results_file_name_label = self.font2.render("Results File Name:", True, (255, 255, 255))
        self.results_file_name_input = InputBox((162, 503), w=236, h=27, text="example.res", file=True)

        self.player1_label = self.font.render("Player 1", True, (255, 255, 255))
        self.player2_label = self.font.render("Player 2", True, (255, 255, 255))
        self.defection_label = self.font.render("Defection", True, (255, 255, 255))
        self.cooperation_label = self.font.render("Cooperation", True, (255, 255, 255))

        self.inputs = [self.number_of_players_input, self.number_of_rounds_input, self.start_time_input,
                       self.events_file_name_input, self.results_file_name_input, self.p_input, self.r_input,
                       self.s_input, self.t_input]
        self.illegal_input = None

        self.start_button = Button(w=80, pos=(854, 499), center=True)

        self.exp_name = exp_name

    def render(self, screen):
        """Renders the radio buttons for components selection, labels for description, input boxes to get the values,
                and the button"""
        Scene.render(self, screen)

        self.back_button.render(screen, "Back")

        screen.blit(self.player_label, (131, 16))
        screen.blit(self.number_of_players_label, (554, 20))
        self.number_of_players_input.render(screen)

        self.add_button.render(screen, "Add")

        self.scroll.render(screen)

        pygame.draw.line(screen, (247, 95, 23), (16, 131), (934, 131), 5)
        gfxdraw.filled_circle(screen, 16, 131, 2, (247, 95, 23))
        gfxdraw.aacircle(screen, 16, 131, 2, (247, 95, 23))
        gfxdraw.filled_circle(screen, 934, 131, 2, (247, 95, 23))
        gfxdraw.aacircle(screen, 934, 131, 2, (247, 95, 23))

        screen.blit(self.p_label, (16, 175))
        self.p_input.render(screen)
        screen.blit(self.r_label, (234, 175))
        self.r_input.render(screen)
        screen.blit(self.s_label, (16, 242))
        self.s_input.render(screen)
        screen.blit(self.t_label, (234, 242))
        self.t_input.render(screen)

        screen.blit(self.number_of_rounds_label, (16, 374))
        self.number_of_rounds_input.render(screen)

        screen.blit(self.events_file_name_label, (16, 441))
        self.events_file_name_input.render(screen)
        screen.blit(self.results_file_name_label, (16, 507))
        self.results_file_name_input.render(screen)
        screen.blit(self.start_time_label, (16, 308))
        self.start_time_input.render(screen)

        pygame.draw.rect(screen, (247, 95, 23), (454, 165, 160, 100), 5)
        pygame.draw.rect(screen, (247, 95, 23), (614, 165, 160, 100), 5)
        pygame.draw.rect(screen, (247, 95, 23), (774, 165, 160, 100), 5)
        pygame.draw.rect(screen, (247, 95, 23), (454, 265, 160, 100), 5)
        pygame.draw.rect(screen, (247, 95, 23), (614, 265, 160, 100), 5)
        pygame.draw.rect(screen, (247, 95, 23), (774, 265, 160, 100), 5)
        pygame.draw.rect(screen, (247, 95, 23), (454, 365, 160, 100), 5)
        pygame.draw.rect(screen, (247, 95, 23), (614, 365, 160, 100), 5)
        pygame.draw.rect(screen, (247, 95, 23), (774, 365, 160, 100), 5)
        pygame.draw.aaline(screen, (247, 95, 23), (457, 168), (457+157, 168+97))
        pygame.draw.aaline(screen, (247, 95, 23), (457, 167), (457+157, 167+97))
        pygame.draw.aaline(screen, (247, 95, 23), (457, 166), (457+157, 166+97))
        pygame.draw.aaline(screen, (247, 95, 23), (457, 165), (457+157, 165+97))
        pygame.draw.aaline(screen, (247, 95, 23), (457, 164), (457+157, 164+97))

        screen.blit(self.player1_label, (521, 173))
        screen.blit(self.player2_label, (466, 224))
        screen.blit(self.defection_label, (480, 302))
        screen.blit(self.cooperation_label, (466, 402))
        screen.blit(self.defection_label, (640, 208))
        screen.blit(self.cooperation_label, (786, 208))
        cell1 = self.font3.render("(", True, (255, 255, 255))
        screen.blit(cell1, (622, 298))
        cell1 = self.font3.render("P:" + str(self.p), True, (56, 151, 244))
        screen.blit(cell1, (630, 298))
        cell1 = self.font3.render(",", True, (255, 255, 255))
        screen.blit(cell1, (688, 298))
        cell1 = self.font3.render("P:" + str(self.p), True, (56, 151, 244))
        screen.blit(cell1, (696, 298))
        cell1 = self.font3.render(")", True, (255, 255, 255))
        screen.blit(cell1, (756, 298))
        cell2 = self.font3.render("(", True, (255, 255, 255))
        screen.blit(cell2, (781, 298))
        cell2 = self.font3.render("T:" + str(self.t), True, (0, 255, 186))
        screen.blit(cell2, (789, 298))
        cell2 = self.font3.render(",", True, (255, 255, 255))
        screen.blit(cell2, (847, 298))
        cell2 = self.font3.render("S:" + str(self.s), True, (181, 52, 255))
        screen.blit(cell2, (855, 298))
        cell2 = self.font3.render(")", True, (255, 255, 255))
        screen.blit(cell2, (915, 298))
        cell3 = self.font3.render("(", True, (255, 255, 255))
        screen.blit(cell3, (622, 398))
        cell3 = self.font3.render("S:" + str(self.s), True, (255, 0, 0))
        screen.blit(cell3, (630, 398))
        cell3 = self.font3.render(",", True, (255, 255, 255))
        screen.blit(cell3, (688, 398))
        cell3 = self.font3.render("T:" + str(self.t), True, (0, 255, 186))
        screen.blit(cell3, (696, 398))
        cell3 = self.font3.render(")", True, (255, 255, 255))
        screen.blit(cell3, (756, 398))
        cell4 = self.font3.render("(", True, (255, 255, 255))
        screen.blit(cell4, (781, 398))
        cell4 = self.font3.render("R:" + str(self.r), True, (244, 56, 56))
        screen.blit(cell4, (789, 398))
        cell4 = self.font3.render(",", True, (255, 255, 255))
        screen.blit(cell4, (847, 398))
        cell4 = self.font3.render("R:" + str(self.r), True, (244, 56, 56))
        screen.blit(cell4, (855, 398))
        cell4 = self.font3.render(")", True, (255, 255, 255))
        screen.blit(cell4, (915, 398))

        self.start_button.render(screen, "Save")

        self.strategy_type_dropdown.render(screen)

        if self.exp_name:
            (w, h) = pygame.display.get_window_size()
            transparent_surface = pygame.Surface((w, h), pygame.SRCALPHA)
            transparent_surface.fill((255, 255, 255, 100))
            screen.blit(transparent_surface, (0, 0))

            self.execute_button.render(screen, "Execute")

        self.back_button.render(screen, "Back")

    def update(self):
        """Update input box text, and radio buttons"""
        if self.agents != self.agents2:
            self.agents2 = self.agents.copy()
            self.chips = []
            start = 0
            for i, item in enumerate(self.agents):
                chip = Chip(item, pos=(start, 0))
                self.chips.append(chip)
                start += chip.rect.w + 16
        self.scroll.update(self.chips)
        self.strategy_type_dropdown.update()

        self.illegal_input = None
        for i in self.inputs:
            if i.active and i.text == "":
                self.illegal_input = i

    def handle_events(self, events):
        """Handles all the objects events, and when the button is pressed will move to the next scene"""
        Scene.handle_events(self, events)

        for event in events:
            if self.back_button.handle_events(event):
                self.manager.go_back()

            if not self.exp_name:
                active = False
                active = active or self.strategy_type_dropdown.handle_events(event)

                if not active:
                    self.number_of_players_input.handle_events(event, self.illegal_input)
                    self.number_of_rounds_input.handle_events(event, self.illegal_input)
                    self.events_file_name_input.handle_events(event, self.illegal_input)
                    self.results_file_name_input.handle_events(event, self.illegal_input)
                    self.start_time_input.handle_events(event, self.illegal_input)
                    if self.s_input.handle_events(event, self.illegal_input):
                        self.s = self.s_input.text
                    if self.t_input.handle_events(event, self.illegal_input):
                        self.t = self.t_input.text
                    if self.r_input.handle_events(event, self.illegal_input):
                        self.r = self.r_input.text
                    if self.p_input.handle_events(event, self.illegal_input):
                        self.p = self.p_input.text

                    if self.add_button.handle_events(event) and not self.illegal_input:
                        strategy_type = self.strategy_type_list[self.strategy_type_dropdown.selected]
                        number_of_players = self.number_of_players_input.get_text()

                        self.agents.append(strategy_type + " " + str(number_of_players))
                        self.added.append({"n": number_of_players, "name": strategy_type})

                    if self.start_button.handle_events(event) and not self.illegal_input:
                        with open("AEC2.0/domain/AXELROD_TOUR/config_simulation.pl", "r") as file:
                            lines = file.readlines()
                            text = ''.join([i.strip("\t\n ") for i in lines])

                            exp_found = False
                            experiment_name = 0
                            while not exp_found:
                                experiment_name +=1
                                if not re.findall(f"experiment\(exp({experiment_name}),\(", text):
                                    exp_found = True
                            experiment_name = f"exp{experiment_name}"

                            lines.insert(65, f"experiment({experiment_name},(\n")
                            lines.insert(66, "set(r(" + self.r + ")),\n")
                            lines.insert(67, "set(s(" + self.s + ")),\n")
                            lines.insert(68, "set(t(" + self.t + ")),\n")
                            lines.insert(69, "set(p(" + self.p + ")),\n")
                            lines.insert(70, "set(starttime(" + self.start_time_input.get_text() + ")),\n")
                            items = ','.join(
                                [f"players({len(self.added)})", f"rounds(0,{self.number_of_rounds_input.get_text()})"])
                            lines.insert(71, "make(1,conductor([" + items + "])),\n")
                            i = 72
                            for item in self.added:
                                lines.insert(i, "make(" + item["n"] + ",player(" + item["name"] + ")),\n")
                                i += 1
                            lines.insert(i, "output(resultsin('" + self.results_file_name_input.get_text() + "')),\n")
                            lines.insert(i + 1, "output(eventsin('" + self.events_file_name_input.get_text() + "')))).\n")

                            fw = open("AEC2.0/domain/AXELROD_TOUR/config_simulation.pl", "w")
                            fw.writelines(lines)
                        self.manager.go_to("SelectExecutionScene", "Axelrod")

                    if i := self.scroll.handle_events(event):
                        self.agents.pop(i - 1)
                        self.added.pop(i - 1)
            else:
                if self.execute_button.handle_events(event):
                    prolog = Prolog()
                    prolog.consult("/Users/denizgorur/PycharmProjects/COGNISIM/AEC2.0/src/loader_AlexrodTournament.pl")
                    os.chdir("Axelrod")
                    for _ in prolog.query(f"run({self.exp_name})."):
                        pass
                    os.chdir("..")
