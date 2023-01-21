import re

import pygame

from objects import Scene, VerticalScroll, File, TextButton


class SelectExecutionScene(Scene):
    def __init__(self, file_type):
        Scene.__init__(self)

        self.experiments = []
        self.vertical_scroll = VerticalScroll(items=self.experiments, w=840, h=401)
        self.back_button = TextButton(pos=(16, 16), w=69, h=25, font_size=21)
        self.file_type = file_type
        self.add_rect = pygame.Rect(51, 461, 787, 63)
        self.font = pygame.font.Font("Images/Montserrat-Regular.ttf", 70)
        self.color = (112, 112, 112)

    def render(self, screen):
        Scene.render(self, screen)

        self.vertical_scroll.render(screen)
        self.back_button.render(screen, "Back")

        pygame.draw.rect(screen, self.color, self.add_rect, 3)
        plus = self.font.render("+", True, self.color)
        screen.blit(plus, (425, 450))

    def update(self):
        if not self.experiments:
            start = 0
            if self.file_type == "Evolutionary":
                lines = open("../domain/GOSSIP_MODEL/config_simulation.pl", "r").read().rstrip("\n").split()
            elif self.file_type == "Axelrod":
                lines = open("../domain/AXELROD_TOUR/config_simulation.pl", "r").read().rstrip("\n ").split()
            lines = ''.join(lines)

            for exp in re.findall(r"experiment\((\w+),\(", lines):
                chip = File(str(exp), pos=(0, start))
                self.experiments.append(chip)
                start += chip.rect.h + 60
            self.vertical_scroll.update(self.experiments)

    def handle_events(self, events):
        Scene.handle_events(self, events)

        for event in events:
            if self.back_button.handle_events(event):
                self.manager.go_back()
            elif i := self.vertical_scroll.handle_events(event):
                if self.file_type == "Evolutionary":
                    self.manager.go_to("SelectEvolutionaryAgentsScene", self.experiments[i - 1].text)
                elif self.file_type == "Axelrod":
                    self.manager.go_to("SelectAxelrodAgentsScene", self.experiments[i - 1].text)

            if event.type == pygame.MOUSEMOTION:
                if self.add_rect.collidepoint(event.pos[0], event.pos[1]):
                    self.color = (255, 255, 255)
                else:
                    self.color = (112, 112, 112)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.add_rect.collidepoint(event.pos[0], event.pos[1]):
                    if self.file_type == "Evolutionary":
                        self.manager.go_to("SelectEvolutionaryAgentsScene")
                    elif self.file_type == "Axelrod":
                        self.manager.go_to("SelectAxelrodAgentsScene")
