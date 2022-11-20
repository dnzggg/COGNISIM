import pygame
from pygame import gfxdraw


class Timeline:
    def __init__(self, pos=(45, 515), width=855, chunks=20, round_num=0, rounds=1452):
        self.pos = pos
        self.width = int(width/chunks)
        self.chunks = chunks
        self.round_num = round_num
        self.rounds = rounds
        self.rect = pygame.Rect(pos[0] + 5, pos[1], width - 25, 15)
        self.hover_pos = None
        self.hover_chunk = None
        self.hover_round = None
        self.font = pygame.font.Font("Images/Montserrat-Regular.ttf", 11)

    def render(self, screen):
        w = self.width
        rect = pygame.Rect(*self.pos, w * self.chunks, 15)
        pygame.draw.rect(screen, (172, 172, 172), rect, border_radius=15)

        rect = pygame.Rect(*self.pos, self.width * self.round_num / self.rounds, 15)
        pygame.draw.rect(screen, (247, 95, 23), rect, border_top_left_radius=15, border_bottom_left_radius=15)

        w = self.width
        x, y = self.pos
        rect = pygame.Rect(x, y, w, 15)
        if self.hover_chunk == 1:
            pygame.draw.rect(screen, (133, 133, 133), rect, 1, border_top_left_radius=15, border_bottom_left_radius=15)
        for chunk in range(self.chunks - 2):
            x += w
            rect = pygame.Rect(x, y, w, 15)
            if self.hover_chunk == chunk + 2:
                pygame.draw.rect(screen, (133, 133, 133), rect, 1)
        if self.hover_chunk == self.chunks:
            x += w
            rect = pygame.Rect(x, y, w, 15)
            pygame.draw.rect(screen, (133, 133, 133), rect, 1, border_top_right_radius=15, border_bottom_right_radius=15)

        if self.hover_pos:
            text = self.font.render(f"Generation {self.hover_chunk}  Round {self.hover_round}", True, (255, 255, 255))
            screen.blit(text, (self.pos[0] + 5, self.pos[1] - 19))
            pygame.draw.rect(screen, (247, 95, 23), (self.hover_pos, y, 4, 15), border_radius=2)
            pygame.draw.rect(screen, (133, 133, 133), (self.hover_pos, y, 4, 15), 1, border_radius=2)

    def update(self, round_num):
        self.round_num = round_num

    def handle_events(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos[0], event.pos[1]):
                self.hover_pos = event.pos[0]
                self.hover_chunk = int((event.pos[0] - self.pos[0] - 5) / (self.width * self.chunks - 10) * self.chunks) + 1
                self.hover_round = int(self.chunks * self.rounds * (event.pos[0] - self.pos[0] - 5) / (self.width * self.chunks - 10))
            else:
                self.hover_pos = None
                self.hover_chunk = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos[0], event.pos[1]):
                if event.button == 1:
                    return int(self.chunks * self.rounds * (event.pos[0] - self.pos[0] - 5) / (
                                self.width * self.chunks - 10)), int(
                        (event.pos[0] - self.pos[0] - 5) / (self.width * self.chunks - 10) * self.chunks) + 1

