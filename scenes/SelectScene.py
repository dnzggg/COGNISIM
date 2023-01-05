import pygame

from objects import Scene


class SelectScene(Scene):
    def __init__(self):
        Scene.__init__(self)

        self.font = pygame.font.Font("Images/Montserrat-ExtraBold.ttf", 40)
        self.one = False
        self.two = False
        self.three = False
        self.four = False
        self.five = False
        self.six = False
        self.rect1 = pygame.Rect(0, 0, 317, 275)
        self.rect2 = pygame.Rect(317, 0, 317, 275)
        self.rect3 = pygame.Rect(633, 0, 317, 275)

        self.rect4 = pygame.Rect(0, 275, 317, 275)
        self.rect5 = pygame.Rect(317, 275, 317, 275)
        self.rect6 = pygame.Rect(633, 275, 317, 275)

    def render(self, screen):
        Scene.render(self, screen)

        load = self.font.render("Load", True, (255, 255, 255))
        screen.blit(load, (105, 52))
        evolutionary = self.font.render("Evolutionary", True, (255, 255, 255))
        screen.blit(evolutionary, (23, 113))
        experiment = self.font.render("Experiment", True, (255, 255, 255))
        screen.blit(experiment, (34, 174))

        pygame.draw.line(screen, (247, 95, 23), (317, 0), (317, 550), 5)

        create = self.font.render("Create New", True, (255, 255, 255))
        screen.blit(create, (351, 52))
        screen.blit(evolutionary, (340, 113))
        screen.blit(experiment, (351, 174))

        pygame.draw.line(screen, (247, 95, 23), (0, 275), (990, 275), 5)

        screen.blit(load, (105, 327))
        axelrod = self.font.render("Axelrod", True, (255, 255, 255))
        screen.blit(axelrod, (74, 388))
        screen.blit(experiment, (34, 449))

        screen.blit(create, (352, 327))
        screen.blit(axelrod, (393, 388))
        screen.blit(experiment, (352, 449))

        pygame.draw.line(screen, (247, 95, 23), (633, 0), (633, 550), 5)

        initiate = self.font.render("Initiate", True, (255, 255, 255))
        screen.blit(initiate, (716, 52))
        screen.blit(evolutionary, (657, 113))
        screen.blit(experiment, (668, 174))

        screen.blit(initiate, (716, 327))
        screen.blit(axelrod, (709, 388))
        screen.blit(experiment, (668, 449))


        if self.one:
            shadow = pygame.Surface((self.rect1.w, self.rect1.h), pygame.SRCALPHA)
            shadow.fill((255, 255, 255, 30))
            screen.blit(shadow, (self.rect1.x, self.rect1.y))
        if self.two:
            shadow = pygame.Surface((self.rect2.w, self.rect2.h), pygame.SRCALPHA)
            shadow.fill((255, 255, 255, 30))
            screen.blit(shadow, (self.rect2.x, self.rect2.y))
        if self.three:
            shadow = pygame.Surface((self.rect3.w, self.rect3.h), pygame.SRCALPHA)
            shadow.fill((255, 255, 255, 30))
            screen.blit(shadow, (self.rect3.x, self.rect3.y))
        if self.four:
            shadow = pygame.Surface((self.rect4.w, self.rect4.h), pygame.SRCALPHA)
            shadow.fill((255, 255, 255, 30))
            screen.blit(shadow, (self.rect4.x, self.rect4.y))
        if self.five:
            shadow = pygame.Surface((self.rect5.w, self.rect5.h), pygame.SRCALPHA)
            shadow.fill((255, 255, 255, 30))
            screen.blit(shadow, (self.rect5.x, self.rect5.y))
        if self.six:
            shadow = pygame.Surface((self.rect6.w, self.rect6.h), pygame.SRCALPHA)
            shadow.fill((255, 255, 255, 30))
            screen.blit(shadow, (self.rect6.x, self.rect6.y))

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
                if self.rect5.collidepoint(event.pos[0], event.pos[1]):
                    self.five = True
                else:
                    self.five = False
                if self.rect6.collidepoint(event.pos[0], event.pos[1]):
                    self.six = True
                else:
                    self.six = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.one:
                    self.manager.go_to("SelectFileScene", "Evolutionary")
                if self.two:
                    self.manager.go_to("SelectEvolutionaryAgentsScene")
                if self.three:
                    self.manager.go_to("SelectExecutionScene", "Evolutionary")
                if self.four:
                    self.manager.go_to("SelectFileScene", "Axelrod")
                if self.five:
                    self.manager.go_to("SelectAxelrodAgentsScene")
                if self.six:
                    self.manager.go_to("SelectExecutionScene", "Axelrod")
