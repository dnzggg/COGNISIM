import glob, os

from objects import Scene, VerticalScroll, File, TextButton


class SelectFileScene(Scene):
    def __init__(self, file_type):
        Scene.__init__(self)

        self.files = []
        self.vertical_scroll = VerticalScroll(items=self.files)
        self.back_button = TextButton(pos=(16, 16), w=69, h=25, font_size=21)
        self.file_type = file_type

    def render(self, screen):
        Scene.render(self, screen)

        self.vertical_scroll.render(screen)
        self.back_button.render(screen, "Back")

    def update(self):
        if not self.files:
            start = 0
            os.chdir(self.file_type)
            files = glob.glob("*.pl")
            os.chdir("..")
            for file in files:
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
                if self.file_type == "Evolutionary":
                    self.manager.go_to("PlayEvolutionaryTournamentScene", self.file_type + "/" + self.files[i - 1].text)
                elif self.file_type == "Axelrod":
                    self.manager.go_to("PlayAxelrodTournamentScene", self.file_type + "/" + self.files[i - 1].text)
