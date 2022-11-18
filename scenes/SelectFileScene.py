import glob

from objects import Scene, VerticalScroll, File, TextButton


class SelectFileScene(Scene):
    def __init__(self):
        Scene.__init__(self)

        self.files = []
        self.horizontal_scroll = VerticalScroll(items=self.files)
        self.back_button = TextButton(pos=(16, 16), w=69, h=25, font_size=21)

    def render(self, screen):
        Scene.render(self, screen)

        self.horizontal_scroll.render(screen)
        self.back_button.render(screen, "Back")

    def update(self):
        if not self.files:
            start = 0
            for file in glob.glob("*.pl"):
                chip = File(str(file), pos=(0, start))
                self.files.append(chip)
                start += chip.rect.h + 60
            self.horizontal_scroll.update(self.files)

    def handle_events(self, events):
        Scene.handle_events(self, events)

        for event in events:
            if i := self.horizontal_scroll.handle_events(event):
                print(self.files[i - 1].text)
                self.manager.go_to("PlayTournamentScene", self.files[i - 1].text)
            if self.back_button.handle_events(event):
                self.manager.go_back()
