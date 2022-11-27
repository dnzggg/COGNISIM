import pygame

from objects import Scene


class SelectScene(Scene):
    def __init__(self):
        Scene.__init__(self)

        self.font = pygame.font.Font("Images/Montserrat-ExtraBold.ttf", 50)
        self.one = False
        self.two = False
        self.three = False
        self.four = False
        self.rect1 = pygame.Rect(0, 0, 475, 275)
        self.rect2 = pygame.Rect(475, 0, 475, 275)
        self.rect3 = pygame.Rect(0, 275, 475, 275)
        self.rect4 = pygame.Rect(475, 275, 475, 275)

    def render(self, screen):
        Scene.render(self, screen)

        load = self.font.render("Load", True, (255, 255, 255))
        screen.blit(load, (172, 46))
        evolutionary = self.font.render("Evolutionary", True, (255, 255, 255))
        screen.blit(evolutionary, (69, 107))
        experiment = self.font.render("Experiment", True, (255, 255, 255))
        screen.blit(experiment, (83, 168))

        pygame.draw.line(screen, (247, 95, 23), (475, 0), (475, 550), 5)

        create = self.font.render("Create New", True, (255, 255, 255))
        screen.blit(create, (557, 46))
        screen.blit(evolutionary, (543, 107))
        screen.blit(experiment, (557, 168))

        pygame.draw.line(screen, (247, 95, 23), (0, 275), (990, 275), 5)

        screen.blit(load, (172, 307))
        axelrod = self.font.render("Axelrod", True, (255, 255, 255))
        screen.blit(axelrod, (134, 368))
        screen.blit(experiment, (83, 429))

        screen.blit(create, (557, 307))
        screen.blit(axelrod, (609, 368))
        screen.blit(experiment, (557, 429))

        if self.one:
            shadow = pygame.Surface((475, 275), pygame.SRCALPHA)
            shadow.fill((255, 255, 255, 30))
            screen.blit(shadow, (0, 0))
        if self.two:
            shadow = pygame.Surface((475, 275), pygame.SRCALPHA)
            shadow.fill((255, 255, 255, 30))
            screen.blit(shadow, (475, 0))
        if self.three:
            shadow = pygame.Surface((475, 275), pygame.SRCALPHA)
            shadow.fill((255, 255, 255, 30))
            screen.blit(shadow, (0, 275))
        if self.four:
            shadow = pygame.Surface((475, 275), pygame.SRCALPHA)
            shadow.fill((255, 255, 255, 30))
            screen.blit(shadow, (475, 275))

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
                if self.rect3.collidepoint(event.pos[0], event.pos[1]):
                    self.three = True
                else:
                    self.three = False
                if self.rect4.collidepoint(event.pos[0], event.pos[1]):
                    self.four = True
                else:
                    self.four = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.one:
                    self.manager.go_to("SelectFileScene", "Evolutionary")
                if self.two:
                    self.manager.go_to("SelectAgentsScene")
                if self.three:
                    self.manager.go_to("SelectFileScene", "Axelrod")
                if self.four:
                    self.manager.go_to("SelectAgentsScene")
