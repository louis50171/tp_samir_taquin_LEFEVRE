try:
    import pygame

    is_pygame = True
except ImportError:
    is_pygame = False


class Square:
    """Management graphic des blocks"""

    def __init__(self, pos, name, screen):
        self.x = (pos[1] + 1) * 2 + pos[1] * 100  # Position X du bloc
        self.y = (pos[0] + 1) * 2 + pos[0] * 100  # Position Y du bloc

        self.target_x = self.x  # position cible X du bloc
        self.target_y = self.y  # position cible Y du bloc

        self.r = pygame.Rect(self.x, self.y, 100, 100)  # faire un rectangle graphic
        self.screen = screen  # écran Pygame
        self.font = pygame.font.Font(pygame.font.get_default_font(), 80)  # la police
        self.name = name  # Tile index

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.r)  # Draw rectangle
        # Calculer la position du texte sur le bloc
        if self.name > 9:
            text_x = self.x
        else:
            text_x = self.x + 25
        text_y = self.y + 10
        # desiner le texte sur le bloc
        self.screen.blit(self.font.render(str(self.name), True, (0, 0, 0)), (text_x, text_y))

    def move(self, pos):
        """"Déplacer le bloc à un autre endroit"""
        self.x = (pos[1] + 1) * 2 + pos[1] * 100
        self.y = (pos[0] + 1) * 2 + pos[0] * 100
        self.r.x = self.x
        self.r.y = self.y

    def reach(self, pos):
        """"Fixer une nouvelle position cible pour le bloc"""
        self.target_x = (pos[1] + 1) * 2 + pos[1] * 100
        self.target_y = (pos[0] + 1) * 2 + pos[0] * 100

    def pursue(self):
        """"Déplacer le bloc de manière à ce qu'il atteigne sa position cible"""
        if self.x < self.target_x:
            self.x += 1
        elif self.x > self.target_x:
            self.x -= 1

        if self.y < self.target_y:
            self.y += 1
        elif self.y > self.target_y:
            self.y -= 1

        self.r.x = self.x
        self.r.y = self.y

        if self.x == self.target_x and self.y == self.target_y:
            return False  # Retourne False si position atteinte
        else:
            return True  #sinon True


class Grid:
    """" Objet grille pour la manipulation graphique des blocs"""

    def __init__(self, size, screen, p):
        self.size = size  # Size of the grid
        self.screen = screen  # Pygame screen
        self.p = p  # Puzzle
        self.grid = [None] * (size ** 2)  # Tiles container

        self.step = 0
        self.sliding = False

        for tile in p.tiles:  # Tiles initial positioning:
            self[tile.start] = Square(tile.start, tile.name, self.screen)

    def move(self):
        """Déplacer un block selon la mémoire du puzzle"""

        start = self.p.memory[self.step][0]  # Start position
        end = self.p.memory[self.step][1]  # End position

        if self.step == 0 and not self.sliding:
            self[start].reach(end)  # Move the first tile
            self.sliding = True

        if self.sliding:  # Pursue the sliding of a tile
            self.sliding = self[start].pursue()
            if not self.sliding:
                self.step += 1
                self[end] = self[start]
                self[start] = None
        else:  # Move the next tile
            self.sliding = True
            self[start].reach(end)

    def __getitem__(self, item):
        return self.grid[self.size * item[0] + item[1]]

    def __setitem__(self, key, value):
        self.grid[self.size * key[0] + key[1]] = value

    def draw(self):
        for g in self.grid:
            if g:
                g.draw()


def pygame_gui(p):
    """" GUI demonstration de la résolution du puzzle p"""

    # GUI setup
    size = [p.size * 100 + (p.size + 1) * 2, p.size * 100 + (p.size + 1) * 2]
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    pygame.display.update()

    g = Grid(p.size, screen, p)  # Objet grille pour manipuler un objet graphique

    running = True

    while running:
        clock.tick(600)  # Ticker to control fps
        screen.fill((0, 0, 0))  # la remplir avec du noir
        g.draw()  # Redessiner la grille
        pygame.display.update()

        if g.step < len(p.memory):
            g.move()  # déplacer le prochain block

        # procédure d'arrête
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False


def console_plot(p):
    grid = ["_"] * p.size ** 2
    for tile in p.tiles:
        pos = tile.start
        grid[pos[0] * p.size + pos[1]] = str(tile.name)

    for k in range(len(p.memory)):
        console_print_grid(grid, p.size)
        s = p.size * p.memory[k][0][0] + p.memory[k][0][1]
        e = p.size * p.memory[k][1][0] + p.memory[k][1][1]
        grid[s], grid[e] = grid[e], grid[s]

    console_print_grid(grid, p.size)


def console_print_grid(grid, size):
    print("_" * 10)
    for j in range(0, len(grid), size):
        line = ""
        for t in range(size):
            line += str(grid[j + t])
            line += " "
        print(line)


def launch_gui(p):
    global is_pygame
    if is_pygame:
        pygame_gui(p)
    else:
        console_plot(p)
