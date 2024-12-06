import pygame
import pygame_shaders


class Window():
    def __init__(self) -> None:
        pygame.init()
        self.size = self.w, self.h = (840, 720)

        # init surfaces
        self.screen = pygame.display.set_mode(self.size, pygame.OPENGL | pygame.DOUBLEBUF)
        self.display = pygame.Surface(self.size, pygame.SRCALPHA)

        # init shaders
        self.screen_shader = pygame_shaders.DefaultScreenShader(self.screen)
        
        self.clock = pygame.time.Clock()

        self.mouse = {
            "press": [False, False, False],
            "release": [False, False, False],
            "pos": (0, 0),
        }

    def events(self):
        self.mouse["press"] = [False, False, False]
        self.mouse["release"] = [False, False, False]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse["press"][0] = True
                if event.button == 2:
                    self.mouse["press"][1] = True
                if event.button == 3:
                    self.mouse["press"][2] = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse["release"][0] = True
                if event.button == 2:
                    self.mouse["release"][1] = True
                if event.button == 3:
                    self.mouse["release"][2] = True
        self.mouse["pos"] = pygame.mouse.get_pos()
        


    def run(self):
        self.screen_shader.render()
        pygame.display.flip()
        self.clock.tick(120)
        
if __name__ == '__main__':
    app = Window()
    while True:
        app.events()
        app.run()