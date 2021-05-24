import pygame
from pygame import gfxdraw

from components import Button, InputBox, RadioButton, Scene, Dropdown, HorizontalScroll, Chip, DropdownItem
from .PlayTournamentScene import PlayTournamentScene


class SelectAgentsScene(Scene):
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
        Renders the radio buttons for tournament selection, labels for description, input boxes to get the values, and
        the button
    update()
        Update input box text, and radio buttons
    get_user_input()
        Gets user input from input boxes
    handle_events(events)
        Handles all the objects events, and when the button is pressed will move to the next scene
    """
    def __init__(self):
        Scene.__init__(self)
        self.font = pygame.font.Font("Images/Montserrat-Regular.ttf", 21)
        self.font2 = pygame.font.Font("Images/Montserrat-Regular.ttf", 15)

        self.item = DropdownItem((100, 100), 1, "12345678")

        self.player_label = self.font.render("Player Agent", True, (255, 255, 255))
        self.gossip_type_list = ["Fair", "Selection 2", "Selection 3", "Selection 4", "Selection 5", "Selection 6"]
        self.gossip_type_dropdown = Dropdown("Gossip Type", w=131, pos=(177, 16), selections=self.gossip_type_list)
        self.discrimination_type_list = ["Cooperator", "Stern", "Defector", "Selection 4", "Selection 5", "Selection 6"]
        self.discrimination_type_dropdown = Dropdown("Discrimination Type", w=193, pos=(334, 16), selections=self.discrimination_type_list)

        self.discrimination_threshold_label = self.font2.render("Discrimination Threshold (-5 to 5.5):", True, (255, 255, 255))
        self.discrimination_threshold_input = InputBox((833, 16), w=101, h=27, text="0.543")
        self.gossip_weight_label = self.font2.render("Gossip Weight (0 to 1):", True, (255, 255, 255))
        self.gossip_weight_input = InputBox((196, 55), w=101, h=27, text="0.543")
        self.trust_criteria_label = self.font2.render("Trust Criteria (0 to 1):", True, (255, 255, 255))
        self.trust_criteria_input = InputBox((521, 55), w=101, h=27, text="0.543")
        self.number_of_players_label = self.font2.render("Number of Players:", True, (255, 255, 255))
        self.number_of_players_input = InputBox((833, 55), w=101, h=27, text="1000")

        self.self_advertisement = True
        self.self_advertisement_radio_label = self.font2.render("Self Advertisement:", True, (255, 255, 255))
        self.self_advertisement_radio_yes_label = self.font2.render("Yes", True, (255, 255, 255))
        self.self_advertisement_radio_yes = RadioButton((170 + 12, 100 + 12), on=True)
        self.self_advertisement_radio_no_label = self.font2.render("No", True, (255, 255, 255))
        self.self_advertisement_radio_no = RadioButton((231 + 12, 100 + 12), on=False)
        self.self_advertisement_radio_no.bind(self.self_advertisement_radio_yes, self.change_self_advertisement)

        self.add_button = Button(w=75, pos=(859, 92), center=True)

        self.added = []
        self.agents = []
        self.agents2 = []
        self.chips = []
        self.scroll = HorizontalScroll(items=self.chips, pos=(16, 139))

        self.conductor_label = self.font.render("Conductor Agent", True, (255, 255, 255))
        self.number_of_conductors_label = self.font2.render("Number of Conductors:", True, (255, 255, 255))
        self.number_of_conductors_input = InputBox((460, 221), w=101, h=27, text="1000")
        self.number_of_rounds_label = self.font2.render("Total Number of Rounds:", True, (255, 255, 255))
        self.number_of_rounds_input = InputBox((833, 221), w=101, h=27, text="1000")
        self.giving_encounters_label = self.font2.render("Total Giving Encounters:", True, (255, 255, 255))
        self.giving_encounters_input = InputBox((513, 260), w=101, h=27, text="1000")
        self.gossip_encounters_label = self.font2.render("Total Giving Encounters:", True, (255, 255, 255))
        self.gossip_encounters_input = InputBox((833, 260), w=101, h=27, text="1000")

        self.starting_order = True
        self.starting_order_radio_label = self.font2.render("Starting Order:", True, (255, 255, 255))
        self.starting_order_radio_giving_label = self.font2.render("Giving", True, (255, 255, 255))
        self.starting_order_radio_giving = RadioButton((131 + 12, 261 + 12), on=True)
        self.starting_order_radio_gossip_label = self.font2.render("Gossip", True, (255, 255, 255))
        self.starting_order_radio_gossip = RadioButton((215 + 12, 261 + 12), on=False)
        self.starting_order_radio_gossip.bind(self.starting_order_radio_giving, self.change_starting_order)

        self.events_file_name_label = self.font2.render("Events File Name:", True, (255, 255, 255))
        self.events_file_name_input = InputBox((162, 326), w=236, h=27, text="example.event")
        self.results_file_name_label = self.font2.render("Results File Name:", True, (255, 255, 255))
        self.results_file_name_input = InputBox((162, 365), w=236, h=27, text="example.res")
        self.benefit_cooperation_label = self.font2.render("Benefit of Cooperation:", True, (255, 255, 255))
        self.benefit_cooperation_input = InputBox((607, 326), w=101, h=27, text="10")
        self.cost_cooperation_label = self.font2.render("Cost of Cooperation:", True, (255, 255, 255))
        self.cost_cooperation_input = InputBox((585, 365), w=101, h=27, text="10")
        self.start_time_label = self.font2.render("Start Time:", True, (255, 255, 255))
        self.start_time_input = InputBox((833, 365), w=101, h=27, text="10")

        self.evolution_type_list = ["Cultural", "Genetic", "Selection 3", "Selection 4", "Selection 5", "Selection 6"]
        self.evolution_type_dropdown = Dropdown("Evolution Type", w=157, pos=(777, 326), selections=self.evolution_type_list)

        self.generation_range_label = self.font.render("Generation Range", True, (255, 255, 255))
        self.min_generation_range_label = self.font2.render("Minimum Generation Range:", True, (255, 255, 255))
        self.min_generation_range_input = InputBox((246, 468), w=101, h=27, text="-5")
        self.max_generation_range_label = self.font2.render("Maximum Generation Range:", True, (255, 255, 255))
        self.max_generation_range_input = InputBox((246, 507), w=101, h=27, text="5")

        self.image_score_range_label = self.font.render("Image Score Range", True, (255, 255, 255))
        self.min_image_score_range_label = self.font2.render("Minimum Image Score:", True, (255, 255, 255))
        self.min_image_score_range_input = InputBox((680, 468), w=101, h=27, text="-5")
        self.max_image_score_range_label = self.font2.render("Maximum Image Score:", True, (255, 255, 255))
        self.max_image_score_range_input = InputBox((680, 507), w=101, h=27, text="5")

        self.start_button = Button(w=80, pos=(854, 499), center=True)

    def change_starting_order(self):
        self.starting_order = not self.starting_order

    def change_self_advertisement(self):
        self.self_advertisement = not self.self_advertisement

    def render(self, screen):
        """Renders the radio buttons for tournament selection, labels for description, input boxes to get the values,
                and the button"""
        Scene.render(self, screen)

        screen.blit(self.player_label, (16, 16))
        screen.blit(self.discrimination_threshold_label, (553, 20))
        self.discrimination_threshold_input.render(screen)
        screen.blit(self.gossip_weight_label, (19, 59))
        self.gossip_weight_input.render(screen)
        screen.blit(self.trust_criteria_label, (357, 59))
        self.trust_criteria_input.render(screen)
        screen.blit(self.number_of_players_label, (682, 59))
        self.number_of_players_input.render(screen)

        screen.blit(self.self_advertisement_radio_label, (19, 102))
        screen.blit(self.self_advertisement_radio_yes_label, (198, 102))
        self.self_advertisement_radio_yes.render(screen)
        screen.blit(self.self_advertisement_radio_no_label, (259, 102))
        self.self_advertisement_radio_no.render(screen)

        self.add_button.render(screen, "Add")

        self.scroll.render(screen)

        pygame.draw.line(screen, (251, 164, 98), (16, 201), (934, 201), 5)
        gfxdraw.filled_circle(screen, 16, 201, 2, (251, 164, 98))
        gfxdraw.aacircle(screen, 16, 201, 2, (251, 164, 98))
        gfxdraw.filled_circle(screen, 934, 201, 2, (251, 164, 98))
        gfxdraw.aacircle(screen, 934, 201, 2, (251, 164, 98))

        screen.blit(self.conductor_label, (16, 222))
        screen.blit(self.number_of_conductors_label, (275, 225))
        self.number_of_conductors_input.render(screen)
        screen.blit(self.number_of_rounds_label, (638, 225))
        self.number_of_rounds_input.render(screen)
        screen.blit(self.giving_encounters_label, (322, 264))
        self.giving_encounters_input.render(screen)
        screen.blit(self.gossip_encounters_label, (642, 264))
        self.gossip_encounters_input.render(screen)

        screen.blit(self.starting_order_radio_label, (16, 263))
        self.starting_order_radio_giving.render(screen)
        screen.blit(self.starting_order_radio_giving_label, (159, 263))
        self.starting_order_radio_gossip.render(screen)
        screen.blit(self.starting_order_radio_gossip_label, (243, 263))

        pygame.draw.line(screen, (251, 164, 98), (16, 306), (934, 306), 5)
        gfxdraw.filled_circle(screen, 16, 306, 2, (251, 164, 98))
        gfxdraw.aacircle(screen, 16, 306, 2, (251, 164, 98))
        gfxdraw.filled_circle(screen, 934, 306, 2, (251, 164, 98))
        gfxdraw.aacircle(screen, 934, 306, 2, (251, 164, 98))

        screen.blit(self.events_file_name_label, (16, 330))
        self.events_file_name_input.render(screen)
        screen.blit(self.results_file_name_label, (16, 369))
        self.results_file_name_input.render(screen)
        screen.blit(self.benefit_cooperation_label, (425, 330))
        self.benefit_cooperation_input.render(screen)
        screen.blit(self.cost_cooperation_label, (425, 369))
        self.cost_cooperation_input.render(screen)
        screen.blit(self.start_time_label, (744, 369))
        self.start_time_input.render(screen)

        pygame.draw.line(screen, (251, 164, 98), (16, 411), (934, 411), 5)
        gfxdraw.filled_circle(screen, 16, 411, 2, (251, 164, 98))
        gfxdraw.aacircle(screen, 16, 411, 2, (251, 164, 98))
        gfxdraw.filled_circle(screen, 934, 411, 2, (251, 164, 98))
        gfxdraw.aacircle(screen, 934, 411, 2, (251, 164, 98))

        screen.blit(self.generation_range_label, (16, 431))
        screen.blit(self.min_generation_range_label, (16, 472))
        self.min_generation_range_input.render(screen)
        screen.blit(self.max_generation_range_label, (16, 511))
        self.max_generation_range_input.render(screen)

        pygame.draw.line(screen, (251, 164, 98), (421, 412), (421, 534), 5)
        gfxdraw.filled_circle(screen, 421, 534, 2, (251, 164, 98))
        gfxdraw.aacircle(screen, 421, 534, 2, (251, 164, 98))

        screen.blit(self.image_score_range_label, (493, 431))
        screen.blit(self.min_image_score_range_label, (493, 472))
        self.min_image_score_range_input.render(screen)
        screen.blit(self.max_image_score_range_label, (493, 511))
        self.max_image_score_range_input.render(screen)

        self.start_button.render(screen, "Save")

        self.discrimination_type_dropdown.render(screen)
        self.evolution_type_dropdown.render(screen)
        self.gossip_type_dropdown.render(screen)

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
        self.gossip_type_dropdown.update()
        self.discrimination_type_dropdown.update()
        self.evolution_type_dropdown.update()

    def handle_events(self, events):
        """Handles all the objects events, and when the button is pressed will move to the next scene"""
        Scene.handle_events(self, events)

        for event in events:
            active = False
            active = active or self.discrimination_type_dropdown.handle_events(event)
            active = active or self.evolution_type_dropdown.handle_events(event)
            active = active or self.gossip_type_dropdown.handle_events(event)

            if not active:
                self.discrimination_threshold_input.handle_events(event)
                self.gossip_weight_input.handle_events(event)
                self.trust_criteria_input.handle_events(event)
                self.number_of_players_input.handle_events(event)
                self.number_of_conductors_input.handle_events(event)
                self.number_of_rounds_input.handle_events(event)
                self.giving_encounters_input.handle_events(event)
                self.gossip_encounters_input.handle_events(event)
                self.events_file_name_input.handle_events(event)
                self.results_file_name_input.handle_events(event)
                self.benefit_cooperation_input.handle_events(event)
                self.cost_cooperation_input.handle_events(event)
                self.start_time_input.handle_events(event)
                self.min_image_score_range_input.handle_events(event)
                self.min_generation_range_input.handle_events(event)
                self.max_image_score_range_input.handle_events(event)
                self.max_generation_range_input.handle_events(event)

                if self.add_button.handle_events(event):
                    discrimination_type = self.discrimination_type_list[self.discrimination_type_dropdown.selected]
                    discrimination_threshold = self.discrimination_threshold_input.get_text()
                    gossip_type = self.gossip_type_list[self.gossip_type_dropdown.selected]
                    gossip_weight = self.gossip_weight_input.get_text()
                    trust_criteria = self.trust_criteria_input.get_text()
                    self_advertisement = "yes" if self.self_advertisement else "no"
                    number_of_players = self.number_of_players_input.get_text()

                    self.agents.append(discrimination_type + " " + str(number_of_players))
                    self.added.append(
                        {"d_ty": discrimination_type, "d_th": discrimination_threshold, "g_t": gossip_type,
                         "g_w": gossip_weight, "t_c": trust_criteria, "s_a": self_advertisement,
                         "n": number_of_players})
                if self.start_button.handle_events(event):
                    for item in self.added:
                        items = list(item.values())
                        items = ','.join(items)
                        print("make(" + item["n"] + ",player(" + items + ")),")
                    giving = "on" if self.starting_order else "off"
                    gossip = "off" if self.starting_order else "on"
                    items = ','.join(
                        [self.number_of_conductors_input.get_text(), "1", self.number_of_rounds_input.get_text(), "1",
                         self.giving_encounters_input.get_text(), self.gossip_encounters_input.get_text(), giving,
                         gossip, "active"])
                    print("make(1,conductor(0," + items + ")),")
                    print("set(imagescorerange(" + self.min_image_score_range_input.get_text() + "," + self.max_image_score_range_input.get_text() + ")),")
                    print("set(cooperationcost(" + self.cost_cooperation_input.get_text() + ")),")
                    print("set(cooperationbenefit(" + self.benefit_cooperation_input.get_text() + ")),")
                    print("set(generationinfo(" + self.min_generation_range_input.get_text() + "," + self.max_generation_range_input.get_text() + ")),")
                    print("set(starttime(" + self.start_time_input.get_text() + ")),")
                    print("set(evolutiontype(" + self.evolution_type_list[self.evolution_type_dropdown.selected] + ")),")
                    print("output(resultsin('" + self.results_file_name_input.get_text() + "')),")
                    print("output(eventsin('" + self.events_file_name_input.get_text() + "'))")


                self.self_advertisement_radio_no.handle_events(event)
                self.self_advertisement_radio_yes.handle_events(event)
                self.starting_order_radio_gossip.handle_events(event)
                self.starting_order_radio_giving.handle_events(event)
                if i := self.scroll.handle_events(event):
                    self.agents.pop(i - 1)
                    self.added.pop(i - 1)
