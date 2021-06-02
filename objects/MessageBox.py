import pygame
from . import RadioButton


class MessageBox:
    """Message box that asks the user for input

    Attributes
    ----------
    size: tuple [int, int]
        Size of the pygame display
    rect: pygame.Rect
        Object that stores the position and size of the box
    answer: str
        The answer of the user
    font_size: int
        Font size of the text on box
    font: pygame.font.Font
        Font of the text that is going to be rendered
    show: bool
        Stores if the message box is shown or not
    highlight_yes: bool
        Stores if yes button is highlighted
    highlight_no: bool
        Stores if yes button is highlighted
    ask_again_rb: RadioButton
        Radio button to ask the user if they don't want to see the message box again.
    ask_again: bool
        Store if the user don't want to see the message box or not

    Methods
    -------
    render(screen, question)
        Renders the box, the question, and buttons for the user to pick the answer
    handle_events(event)
        If the yes or no button pressed updates the answer and also when onHover the button color changes
    """
    def __init__(self, w, h):
        """
        Parameters
        ----------
        w: int
            width of the box
        h: int
            height of the box
        """
        self.size = pygame.display.get_surface().get_size()
        self.rect = pygame.Rect(self.size[0]/2 - w/2, self.size[1]/2 - h/2, w, h)
        self.answer = ""
        self.font_size = 20
        self.font = pygame.font.Font("Images/Montserrat-Regular.ttf", self.font_size)
        self.show = False
        self.highlight_yes = False
        self.highlight_no = False
        self.ask_again_rb = RadioButton(pos=(self.rect.x + 180, self.rect.y + self.rect.h - 25), self_deactivate=True)
        self.ask_again = True

    def render(self, screen, question):
        """Renders the box, the question, and buttons for the user to pick the answer

        Parameters
        ----------
        screen: pygame.Surface
            pygame screen
        question: str
            Question to be displayed on the screen
        """
        shadow = pygame.Surface(self.size, pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 100))
        pygame.draw.rect(shadow, (0, 0, 0, 110), (self.rect.x - 16, self.rect.y - 16, self.rect.w + 32, self.rect.h + 32), border_radius=3)
        pygame.draw.rect(shadow, (0, 0, 0, 120), (self.rect.x - 8, self.rect.y - 8, self.rect.w + 16, self.rect.h + 16), border_radius=3)
        pygame.draw.rect(shadow, (0, 0, 0, 140), (self.rect.x - 4, self.rect.y - 4, self.rect.w + 8, self.rect.h + 8), border_radius=3)
        screen.blit(shadow, (0, 0))

        pygame.draw.rect(screen, (66, 66, 66), self.rect, border_radius=3)

        if self.rect.w - 8 > self.font.size(str(question))[0]:
            text1 = self.font.render(str(question), True, (255, 255, 255))
            screen.blit(text1, (self.rect.x + 10, self.rect.y + 5))
        else:
            question += " "
            t = ""
            line = 0
            for string in question.split(" "):
                temp = t
                t += string + " "
                if self.rect.w - 8 < self.font.size(str(t))[0] and string != "":
                    text1 = self.font.render(str(temp), True, (255, 255, 255))
                    screen.blit(text1, (self.rect.x + 10, self.rect.y + 5 + (line * (self.font_size + 10))))
                    t = string + " "
                    line += 1
                else:
                    text1 = self.font.render(str(t), True, (255, 255, 255))
                    screen.blit(text1, (self.rect.x + 10, self.rect.y + 5 + (line * (self.font_size + 10))))

        if self.highlight_yes:
            surface = pygame.Surface((45, 30), pygame.SRCALPHA)
            pygame.draw.rect(surface, (136, 188, 230, 50), surface.get_rect(), border_radius=2)
            screen.blit(surface, (self.rect.x + self.rect.w - 105, self.rect.y + self.rect.h - 40))

        if self.highlight_no:
            surface = pygame.Surface((40, 30), pygame.SRCALPHA)
            pygame.draw.rect(surface, (136, 188, 230, 50), surface.get_rect(), border_radius=2)
            screen.blit(surface, (self.rect.x + self.rect.w - 55, self.rect.y + self.rect.h - 40))

        yes = self.font.render("Yes", True, (136, 188, 230))
        screen.blit(yes, (self.rect.x + self.rect.w - 100, self.rect.y + self.rect.h - 40))

        no = self.font.render("No", True, (136, 188, 230))
        screen.blit(no, (self.rect.x + self.rect.w - 50, self.rect.y + self.rect.h - 40))

        ask_again = self.font.render("Don't ask again", True, (200, 200, 200))
        screen.blit(ask_again, (self.rect.x + 10, self.rect.y + self.rect.h - 40))
        self.ask_again_rb.render(screen)

    def handle_events(self, event):
        """If the yes or no button pressed updates the answer and also when onHover the button color changes

        Parameters
        ----------
        event: pygame.event.Event
            pygame event
        """
        self.ask_again_rb.handle_events(event)
        if self.show:
            x, y = pygame.mouse.get_pos()
            if self.rect.x + self.rect.w - 105 < x < self.rect.x + self.rect.w - 60 and \
                    self.rect.y + self.rect.h - 40 < y < self.rect.y + self.rect.h - 10:
                self.highlight_yes = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.answer = "yes"
                    if self.ask_again_rb.on:
                        self.ask_again = False
            else:
                self.highlight_yes = False

            if self.rect.x + self.rect.w - 55 < x < self.rect.x + self.rect.w - 15 and \
                    self.rect.y + self.rect.h - 40 < y < self.rect.y + self.rect.h - 10:
                self.highlight_no = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.answer = "no"
            else:
                self.highlight_no = False


