from random import shuffle


class Tile:
    compter = 0

    def __init__(self, start, end, p):
        self.start = start  # Position de départ
        self.position = start  # Position courante
        self.goal = end  # Objectif
        self.name = Tile.compter + 1
        self.p = p  # le Puzzle
        self.locked = False
        self.superlocked = False
        self.verbose = p.verbose
        Tile.compter += 1

    def solve(self, previous):
        """"ecoresolution pour le bloc"""

        if self.position == self.goal:
            # Si arrivé au goal
            if self.verbose: print(self.name, "à l'objectif.\n", self.p)
            self.locked = True
            return True
        else:
            # Sinon
            neighbour = self.get_sorted_neighbour()
            action_performed = False
            n = 0
            while not action_performed and n < len(neighbour):
                if self.p[neighbour[n]] is None:
                    action_performed = True
                    self.move(neighbour[n])
                    if self.verbose: print(self.name, " Va directement à l'objectif goal")
                    return True
                elif not self.p[neighbour[n]].locked:
                    action_performed = True

                    self.locked = True

                    # Attaque
                    if self.goal not in neighbour:
                        constraint = self.goal
                    else:
                        constraint = previous

                    if self.verbose: print(self.name, " demandé ", self.p[neighbour[n]].name, " de volé(c :", constraint)

                    if self.p[neighbour[n]].fly_you_fool(constraint):
                        self.move(neighbour[n])  # Déplacement si réussite
                        if self.verbose: print(self.name, " déplacé à la position demandé.\n", self.p)
                        return False
                    else:
                        self.locked = False
                        if self.verbose: print(self.name, " fail")
                        return False
                else:
                    n += 1

            self.p.unlock_all()
            self.locked = False
            return False

    def fly_you_fool(self, constraint=None):
        # La case est attaqué et veut s'enfuire.

        # 1. On récupère les voisins
        neighbour = self.get_reverse_sorted_neighbour()
        self.locked = True
        if self.verbose : print("\t ", self.name, ":", neighbour)
        if constraint == self.goal:
            constraint = None

        n = 0
        while n < len(neighbour):
            if neighbour[n] != constraint:
                if self.p[neighbour[n]] is None:
                    self.move(neighbour[n])
                    if self.verbose: print(self.name, "se déplacer vers le vide")
                    return True
                elif not self.p[neighbour[n]].locked:
                    if self.verbose: print(self.name, " attaque ", self.p[neighbour[n]].name)
                    if self.p[neighbour[n]].fly_you_fool():
                        self.move(neighbour[n])
                        if self.verbose: print(self.name, " a réussi à voler ...")
                        return True
                    else:
                        if self.verbose: print(self.name, " a rapporté une erreur")
                        return False
                else:
                    if self.verbose : print("\t", self.p[neighbour[n]].name, "est bloqué :", self.p[neighbour[n]].locked)
            n+=1

        self.p.unlock_all()
        self.fly_you_fool(constraint)
        self.locked = False
        return False

    def find_neighbour(self):
        n = []
        for move in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            new = (self.position[0] + move[0], self.position[1] + move[1])
            if 0 <= new[0] < self.p.size and 0 <= new[1] < self.p.size:
                n.append(new)
        return n

    def get_sorted_neighbour(self):
        neighbour = self.find_neighbour()
        blank = self.p.get_void()
        blank_distance = []
        goal_distance = []
        for n in neighbour:
            if self.p[n] is not None:
                blank_distance.append(self.p[n].manhattan(blank))
                goal_distance.append(self.p[n].manhattan(self.goal))
            else:
                blank_distance.append(0)
                goal_distance.append(abs(self.goal[0] - n[0]) + abs(self.goal[1] - n[1]))

        # Tri selon la proximité avec le but, puis selon la distance de la case vide
        for i in range(len(neighbour) - 1, -1, -1):
            for j in range(0, i):
                if goal_distance[j + 1] < goal_distance[j]:
                    neighbour[j + 1], neighbour[j] = neighbour[j], neighbour[j + 1]
                    blank_distance[j + 1], blank_distance[j] = blank_distance[j], blank_distance[j + 1]
                    goal_distance[j + 1], goal_distance[j] = goal_distance[j], goal_distance[j + 1]
                elif goal_distance[j + 1] == goal_distance[j]:
                    if blank_distance[j + 1] < blank_distance[j]:
                        neighbour[j + 1], neighbour[j] = neighbour[j], neighbour[j + 1]
                        blank_distance[j + 1], blank_distance[j] = blank_distance[j], blank_distance[j + 1]
                        goal_distance[j + 1], goal_distance[j] = goal_distance[j], goal_distance[j + 1]
        return neighbour

    def get_reverse_sorted_neighbour(self):

        neighbour = self.find_neighbour()
        shuffle(neighbour)
        blank = self.p.get_void()
        blank_distance = []
        goal_distance = []
        for n in neighbour:
            if self.p[n] is not None:
                blank_distance.append(self.p[n].manhattan(blank))
                goal_distance.append(self.p[n].manhattan(self.goal))
            else:
                blank_distance.append(0)
                goal_distance.append(abs(self.goal[0] - n[0]) + abs(self.goal[1] - n[1]))
        # Tri selon la proximité avec le but, puis selon la distance de la case vide
        for i in range(len(neighbour) - 1, -1, -1):
            for j in range(0, i):
                if blank_distance[j + 1] < blank_distance[j]:
                    neighbour[j + 1], neighbour[j] = neighbour[j], neighbour[j + 1]
                    blank_distance[j + 1], blank_distance[j] = blank_distance[j], blank_distance[j + 1]
                    goal_distance[j + 1], goal_distance[j] = goal_distance[j], goal_distance[j + 1]
                elif blank_distance[j + 1] == blank_distance[j]:
                    if goal_distance[j + 1] < goal_distance[j]:
                        neighbour[j + 1], neighbour[j] = neighbour[j], neighbour[j + 1]
                        blank_distance[j + 1], blank_distance[j] = blank_distance[j], blank_distance[j + 1]
                        goal_distance[j + 1], goal_distance[j] = goal_distance[j], goal_distance[j + 1]
        return neighbour

    def manhattan(self, other):
        return abs(self.position[0] - other[0]) + abs(self.position[1] - other[1])

    def move(self, pos):
        self.locked = False
        self.p[self.position] = None
        self.p.memory.append((self.position, pos))
        self.position = pos
        self.p[pos] = self

    def __repr__(self):
        return str(self.name)
