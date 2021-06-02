import pygame


class InputBox:
    """InputBox object for getting the user input.

    Attributes
    ----------
    w: int
        width of box
    rect: pygame.Rect
        Object that stores the position and size of the box
    active_color: tuple[int, int, int]
        The color of the box when it is selected
    inactive_color: tuple[int, int, int]
        The color of the box when it is not selected
    color: tuple[int, int, int]
        The current color of the box
    text: str
        Text inside the box
    active: bool
        Stores if the box is active or not
    font: pygame.font.Font
        Font of the text that is going to be rendered
    label: pygame.Surface
        Encoded text to be rendered on the screen

    Methods
    -------
    render(screen)
        Renders the box and its text inside
    update()
        Updates the size of the box
    get_text()
        Returns the text inside of the box
    handle_events(event)
        If it is clicked activates the box, and if it is active and a key is pressed updates the text inside
    """
    def __init__(self, pos=(100, 100), w=140, h=40, text="", fro=None, to=None, decimal=False, negative=False, file=False):
        """
        Parameters
        ----------
        pos: tuple [int, int]
            position that it is to be drawn
        w: int
            width of box
        h: int
            height of box
        text: str
            initial text
        """
        self.w = w
        self.rect = pygame.Rect(pos[0], pos[1], w, h)
        self.active_color = (28, 134, 238)
        self.inactive_color = (141, 182, 205)
        self.color = self.inactive_color
        self.text = text
        self.active = False
        self.font = pygame.font.Font("Images/Montserrat-Regular.ttf", 15)
        self.label = self.font.render(self.text, True, (255, 255, 255))
        if fro is not None and to is not None:
            self.range = {"start": fro, "stop": to}
        else:
            self.range = None
        self.decimal = decimal
        self.negative = negative
        self.file = file
        self.key_repeat = 250
        pygame.key.set_repeat(int(self.key_repeat))
        self.history = [self.text]
        self.BACK_TO_NORMAL = pygame.USEREVENT + 1

    def render(self, screen):
        """Renders the box and its text inside

        Parameters
        ----------
        screen: pygame.Surface
            pygame screen
        """
        screen.blit(self.label, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def update(self):
        """Updates the size of the box"""
        width = max(self.w, self.label.get_width() + 10)
        self.rect.w = width

    def get_text(self):
        """Returns the text inside of the box

        Returns
        -------
        str
            text inside of the box
        """
        if len(self.text) == 0:
            self.color = (255, 0, 0)
            pygame.time.set_timer(self.BACK_TO_NORMAL, 600)
            return False

        return self.text

    def handle_events(self, event):
        """If it is clicked activates the box, and if it is active and a key is pressed updates the text inside

        Parameters
        ----------
        event: pygame.event.Event
            pygame event
        """
        self.history = self.history[-1000:]
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos[0], event.pos[1]):
                self.active = True
            else:
                self.active = False
            self.color = self.active_color if self.active else self.inactive_color

        if event.type == pygame.KEYDOWN:
            if self.active:
                if pygame.key.get_mods() and pygame.KMOD_CTRL and event.key == pygame.K_z:
                    try:
                        if self.text != (temp := self.history.pop(-1)):
                            self.text = temp
                        else:
                            self.text = self.history.pop(-1)
                        if len(self.history) < 1:
                            self.history = [self.text]
                    except IndexError:
                        self.history.append(self.text)

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.history.append(self.text)

                elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6,
                                   pygame.K_7, pygame.K_8, pygame.K_9]:
                    self.text += event.unicode
                    if self.range:
                        if not (self.range["start"] <= float(self.text) <= self.range["stop"]):
                            self.text = self.text[:-1]
                            self.color = (255, 0, 0)
                            pygame.time.set_timer(self.BACK_TO_NORMAL, 600)
                    else:
                        self.history.append(self.text)

                elif self.decimal and event.key in [pygame.K_PERIOD]:
                    self.text += event.unicode
                    try:
                        float(self.text)
                        self.history.append(self.text)
                    except ValueError:
                        self.text = self.text[:-1]
                        self.color = (255, 0, 0)
                        pygame.time.set_timer(self.BACK_TO_NORMAL, 600)

                elif self.negative and event.key in [pygame.K_MINUS]:
                    self.text += event.unicode
                    try:
                        float(self.text)
                        self.history.append(self.text)
                    except ValueError:
                        if len(self.text) > 1:
                            self.text = self.text[:-1]
                            self.color = (255, 0, 0)
                            pygame.time.set_timer(self.BACK_TO_NORMAL, 600)
                        else:
                            self.history.append(self.text)

                elif not(pygame.key.get_mods() and pygame.KMOD_CTRL):
                    if self.file and event.key not in [pygame.K_SLASH, pygame.K_BACKSLASH, pygame.K_QUESTION,
                                                         pygame.K_PERCENT, pygame.K_ASTERISK, pygame.K_COLON,
                                                         pygame.K_EQUALS, pygame.K_QUOTE, pygame.K_LESS,
                                                         pygame.K_GREATER, pygame.K_COMMA, pygame.K_SEMICOLON,
                                                         pygame.K_SPACE, pygame.K_TAB]:
                        self.text += event.unicode
                        self.history.append(self.text)

                if not self.file and (not self.negative and event.key in [pygame.K_MINUS] or not self.decimal and event.key in [pygame.K_PERIOD]):
                    self.color = (255, 0, 0)
                    pygame.time.set_timer(self.BACK_TO_NORMAL, 600)

                self.label = self.font.render(self.text, True, (255, 255, 255))

            pygame.key.set_repeat(int(self.key_repeat))
            self.key_repeat /= 1.5
            if self.key_repeat < 50:
                self.key_repeat = 50

        if event.type == self.BACK_TO_NORMAL:
            self.color = self.active_color if self.active else self.inactive_color

        if event.type == pygame.KEYUP:
            self.key_repeat = 250
            pygame.key.set_repeat(int(self.key_repeat))
