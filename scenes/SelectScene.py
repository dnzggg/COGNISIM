import pygame

from objects import Scene


class SelectScene(Scene):
    def __init__(self):
        Scene.__init__(self)

        self.font = pygame.font.Font("Images/Montserrat-ExtraBold.ttf", 50)
        self.one = False
        self.two = False
        self.rect1 = pygame.Rect(0, 0, 475, 550)
        self.rect2 = pygame.Rect(475, 0, 475, 550)

    def render(self, screen):
        Scene.render(self, screen)

        load = self.font.render("Load", True, (255, 255, 255))
        screen.blit(load, (173, 185))
        experiment = self.font.render("Experiment", True, (255, 255, 255))
        screen.blit(experiment, (84, 306))

        pygame.draw.line(screen, (247, 95, 23), (475, 0), (475, 550), 5)

        create = self.font.render("Create", True, (255, 255, 255))
        screen.blit(create, (627, 124))
        new = self.font.render("New", True, (255, 255, 255))
        screen.blit(new, (655, 245))
        experiment2 = self.font.render("Experiment", True, (255, 255, 255))
        screen.blit(experiment2, (560, 366))

        if self.one:
            shadow = pygame.Surface((475, 550), pygame.SRCALPHA)
            shadow.fill((255, 255, 255, 30))
            screen.blit(shadow, (0, 0))
        if self.two:
            shadow = pygame.Surface((475, 550), pygame.SRCALPHA)
            shadow.fill((255, 255, 255, 30))
            screen.blit(shadow, (475, 0))

    def update(self):
        pass

    def handle_events(self, events):
        Scene.handle_events(self, events)

        for event in events:
            if event.type == pygame.MOUSEMOTION:
                if self.rect1.collidepoint(event.pos[0], event.pos[1]):
                    self.one = True
                else:
                    self.one = False
                if self.rect2.collidepoint(event.pos[0], event.pos[1]):
                    self.two = True
                else:
                    self.two = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.one:
                    self.manager.go_to("SelectFileScene")
                if self.two:
                    self.manager.go_to("SelectAgentsScene")
