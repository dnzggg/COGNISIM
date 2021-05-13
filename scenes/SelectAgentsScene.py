import pygame

from components import Button, InputBox, RadioButton, Scene, Dropdown, HorizontalScroll, Chip


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

        self.player_label = self.font.render("Player Agent", True, (255, 255, 255))
        selection_list = ["Selection 1", "Selection 2", "Selection 3", "Selection 4", "Selection 5", "Selection 6",
                          "Selection 7", "Selection 8"]
        self.player_dropdown = Dropdown("Player Type", w=128, pos=(228, 16), selections=selection_list)
        self.discrimination_type_dropdown = Dropdown("Discrimination Type", w=193, pos=(433, 16), selections=selection_list)
        self.discrimination_threshold_dropdown = Dropdown("Discrimination Threshold", w=231, pos=(703, 16), selections=selection_list)
        self.gossip_type_dropdown = Dropdown("Gossip Type", w=131, pos=(16, 54), selections=selection_list)

        self.gossip_weight_label = self.font2.render("Gossip Weight (0 to 1):", True, (255, 255, 255))
        self.gossip_weight_input = InputBox((448, 54), w=101, h=27, text="0.543")
        self.trust_criteria_label = self.font2.render("Trust Criteria (0 to 1):", True, (255, 255, 255))
        self.trust_criteria_input = InputBox((183, 96), w=101, h=27, text="0.543")
        self.number_of_players_label = self.font2.render("Number of Players:", True, (255, 255, 255))
        self.number_of_players_input = InputBox((563, 96), w=101, h=27, text="1000")

        self.self_advertisement_radio_label = self.font2.render("Self Advertisement:", True, (255, 255, 255))
        self.self_advertisement_radio_yes_label = self.font2.render("Yes", True, (255, 255, 255))
        self.self_advertisement_radio_yes = RadioButton((823 + 12, 56 + 12), active=True)
        self.self_advertisement_radio_no_label = self.font2.render("No", True, (255, 255, 255))
        self.self_advertisement_radio_no = RadioButton((884 + 12, 56 + 12), active=False)

        self.add_button = Button(w=75, pos=(859, 92))

        self.agents = ["Defector 100", "Cooperator 200", "Stern 50", "Defector 100", "Cooperator 200", "Stern 50",
                       "Defector 100", "Cooperator 200", "Stern 50", "Defector 100", "Cooperator 200", "Stern 50"]
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

        self.starting_order_radio_label = self.font2.render("Starting Order:", True, (255, 255, 255))
        self.starting_order_radio_giving_label = self.font2.render("Giving", True, (255, 255, 255))
        self.starting_order_radio_giving = RadioButton((131 + 12, 261 + 12), active=True)
        self.starting_order_radio_gossip_label = self.font2.render("Gossip", True, (255, 255, 255))
        self.starting_order_radio_gossip = RadioButton((215 + 12, 261 + 12), active=False)

    def render(self, screen):
        """Renders the radio buttons for tournament selection, labels for description, input boxes to get the values,
                and the button"""
        Scene.render(self, screen)

        screen.blit(self.player_label, (16, 16))
        screen.blit(self.gossip_weight_label, (271, 58))
        self.gossip_weight_input.render(screen)
        screen.blit(self.trust_criteria_label, (19, 100))
        self.trust_criteria_input.render(screen)
        screen.blit(self.number_of_players_label, (412, 100))
        self.number_of_players_input.render(screen)

        screen.blit(self.self_advertisement_radio_label, (672, 58))
        screen.blit(self.self_advertisement_radio_yes_label, (851, 58))
        self.self_advertisement_radio_yes.render(screen)
        screen.blit(self.self_advertisement_radio_no_label, (912, 58))
        self.self_advertisement_radio_no.render(screen)

        self.add_button.render(screen, "Add")

        self.scroll.render(screen)

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

        self.player_dropdown.render(screen)
        self.discrimination_type_dropdown.render(screen)
        self.discrimination_threshold_dropdown.render(screen)
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

    def handle_events(self, events):
        """Handles all the objects events, and when the button is pressed will move to the next scene"""
        Scene.handle_events(self, events)

        for event in events:
            self.discrimination_type_dropdown.handle_events(event)
            if i := self.scroll.handle_events(event):
                self.agents.pop(i - 1)
