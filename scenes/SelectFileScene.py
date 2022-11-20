import glob

from objects import Scene, VerticalScroll, File, TextButton


class SelectFileScene(Scene):
    def __init__(self):
        Scene.__init__(self)

        self.files = []
        self.vertical_scroll = VerticalScroll(items=self.files)
        self.back_button = TextButton(pos=(16, 16), w=69, h=25, font_size=21)

    def render(self, screen):
        Scene.render(self, screen)

        self.vertical_scroll.render(screen)
        self.back_button.render(screen, "Back")

    def update(self):
        if not self.files:
            start = 0
            for file in glob.glob("*.pl"):
                chip = File(str(file), pos=(0, start))
                self.files.append(chip)
                start += chip.rect.h + 60
            for file in glob.glob("*.pl"):
                chip = File(str(file), pos=(0, start))
                self.files.append(chip)
                start += chip.rect.h + 60
            for file in glob.glob("*.pl"):
                chip = File(str(file), pos=(0, start))
                self.files.append(chip)
                start += chip.rect.h + 60
            self.vertical_scroll.update(self.files)

    def handle_events(self, events):
        Scene.handle_events(self, events)

        for event in events:
            if self.back_button.handle_events(event):
                self.manager.go_back()
            elif i := self.vertical_scroll.handle_events(event):
                self.manager.go_to("PlayAxelrodTournamentScene", self.files[i - 1].text)
