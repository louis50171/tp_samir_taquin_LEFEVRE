from random import randint
from class_Tile import Tile


class Puzzle:
    def __init__(self, size, n_tiles, verbose):
        self.size = size  # taille du puzzle
        self.n_tiles = n_tiles  # nombre de bloc du puzzle
        Tile.compter = 0
        self.tiles = [] # Objet block
        self.puzzle = [None] * self.size ** 2  # taille de la grille
        self.verbose = verbose
        self.memory = []  # utile pour le traçage

    def create_tiles(self):
        """Créer une configuration resolvable pour les blocs()
        """
        for k in range(self.n_tiles):
            # positon de départ aléatoire
            row, column = randint(0, self.size - 1), randint(0, self.size - 1)
            while self[row, column] is not None: # tant que cette position aléatoire est occupé
                row, column = randint(0, self.size - 1), randint(0, self.size - 1)
            # ajouté le bloc à la grille
            self.tiles.append(Tile((row, column), (Tile.compter // self.size, Tile.compter % self.size), self))
            self[row, column] = self.tiles[-1]

        # Si le puzzle n'est pas solvable le refaire
        if not self.solvable():
            self.puzzle = [None] * self.size ** 2
            self.tiles = []
            Tile.compter = 0
            self.create_tiles()

    def solve(self):
        """Résoudre la grille"""
        # Traitement de l'ordre de priorité pour les blocs
        if self.size == 3:
            pre_order = [2, 1, 0, 3, 6, 7, 4, 5]
            order = []
            t_name = [t.name-1 for t in self.tiles]
            for k in pre_order:
                if k in t_name:
                    order.append(k)

        elif self.size == 5:
            pre_order = [4, 3, 2, 1, 0, 5, 10, 15, 20, 21, 16, 11, 6, 7, 8, 9, 14, 13, 12, 17, 22, 23, 18, 19]
            order = []
            t_name = [t.name - 1 for t in self.tiles]
            for k in pre_order:
                if k in t_name:
                    order.append(k)

        c = None
        self.check_superlock()  # Vérifier si la ligne et compléter et bloquer tout les blocs dessus
        self.unlock_all()  # déverrouiller tout les blocs

        for j in order:
            tile = self.tiles[j]
            if tile.goal == tile.position:
                tile.locked = True  # Si le bloc atteint le but --> fin
                c = tile.position
            else:
                if self.verbose: print("Solution pour", tile.name)
                step = 0
                # solution pour le bloc
                while not tile.solve(c) and step<200:
                    step += 1
                    pass
                break

    def is_solve(self):
        """"vérifier si la grille est résolu"""
        for t in self.tiles:
            if t.position != t.goal:
                return False
        return True

    def check_superlock(self):
        """recherche de bloc bloqué"""
        is_row_complete = True
        line = 0
        is_col_complete = True
        col = 0

        while is_row_complete and line<self.size -1 and is_col_complete and col<self.size-1:
            is_row_complete = True
            for k in range(self.size):
                if self[line, k] is None:
                    is_row_complete = False
                elif self[line, k].position != self[line, k].goal:
                    is_row_complete = False
            if is_row_complete:
                if self.verbose: print("LA LIGNE EST BLOQUE")
                for k in range(self.size):
                    if self.verbose: print(self[line, k].name, " superlocked")
                    self[line, k].superlocked = True
            line += 1

            is_col_complete = True
            for k in range(self.size):
                if self[k, col] is None:
                    is_col_complete = False
                elif self[k, col].position != self[k, col].goal:
                    is_col_complete = False
            if is_col_complete:
                if self.verbose: print("LA COLONNE EST BLOQUE")
                for k in range(self.size):
                    if self.verbose : print(self[k, col].name, " superlocked")
                    self[k, col].superlocked = True
            col += 1

    def get_void(self):
        """retourné la première case vide"""
        for k in range(self.size):
            for j in range(self.size):
                if self[k, j] is None:
                    return (k, j)

    def unlock_all(self):
        """déverouiller tout les blocs sauf ceux sur une ligne résolue"""
        if self.verbose: print("UNLOCK")
        for t in self.tiles:
            if not t.superlocked:
                t.locked = False
            else:
                t.locked = True

    def __getitem__(self, item):
        return self.puzzle[item[0] * self.size + item[1]]

    def __setitem__(self, key, value):
        self.puzzle[key[0] * self.size + key[1]] = value

    def __repr__(self):
        s = ""
        for k in range(0, self.size ** 2, self.size):
            s += str(self.puzzle[k:k + self.size]) + "\n"
        return s

    def solvable(self):
        """Vérifier si on peut résoudre le puzzle"""
        count = 0

        for i in range(len(self.puzzle) -1):
            for j in range(i + 1, len(self.puzzle)):
                if self.puzzle[j] and self.puzzle[i] and self.puzzle[i].name > self.puzzle[j].name:
                    count += 1

        return count % 2 == 0