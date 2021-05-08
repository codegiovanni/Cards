import pygame as pg
import numpy as np
import random

clock = pg.time.Clock()
FPS = 60

WIDTH = 1920
HEIGHT = 1080

x_gap = 8
y_gap = 16

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

pg.init()

pg.font.init()
my_font = pg.font.SysFont('arial', 16)

txt0 = 'King_W70.txt'
txt1 = 'Queen_W70.txt'
txt2 = 'Jack_W70.txt'
txt3 = '10_heart_W70.txt'
txt4 = '9_heart_W70.txt'
txt5 = '8_heart_W70.txt'
txt6 = '7_heart_W70.txt'
txt7 = '6_heart_W70.txt'
txt8 = '5_heart_W70.txt'
txt9 = '4_heart_W70.txt'
txt10 = '3_heart_W70.txt'
txt11 = '2_heart_W70.txt'
txt12 = 'Ace_heart_W70.txt'

deck = [txt0, txt1, txt2, txt3, txt4, txt5, txt6, txt7, txt8, txt9, txt10, txt11, txt12]


def cards():
    txt = random.choice(deck)
    return txt


txt = cards()

MAP_HEIGHT = sum(1 for line in open(txt))
MAP_WIDTH = sum(1 for char in open(txt).readline()) - 1
# print(f"W =", MAP_WIDTH,'\n'"H =", MAP_HEIGHT)


def asciiTxt(txt):
    with open(txt, 'r') as file:
        data = [file.read().replace('\n', '')]

    ascii_chars = []
    for line in data:
        for char in line:
            ascii_chars.append(char)

    inverted_ascii_chars = ascii_chars[::-1]

    return inverted_ascii_chars


class Projection:
    def __init__(self, width, height, chars):
        self.chars = chars
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((width, height))
        self.background = BLACK
        pg.display.set_caption('ASCII 3D CARD')
        self.surfaces = {}

    def addSurface(self, name, surface):
        self.surfaces[name] = surface

    def display(self):
        self.screen.fill(self.background)

        for surface in self.surfaces.values():
            i = 0
            for node in surface.nodes:
                self.text = self.chars[i]
                self.text_surface = my_font.render(self.text, False, (WHITE if self.text == '.' else RED))
                self.screen.blit(self.text_surface, (WIDTH // 2 - MAP_WIDTH // 2 * x_gap + node[0],
                                                     HEIGHT // 2 + MAP_HEIGHT // 2 * y_gap + node[1] - y_gap))
                i += 1

    def rotate_x(self, theta):
        for surface in self.surfaces.values():
            center = surface.findCentre()
            c = np.cos(theta)
            s = np.sin(theta)

            matrix = np.array([[1, 0, 0, 0],
                               [0, c, -s, 0],
                               [0, s, c, 0],
                               [0, 0, 0, 1]])

            surface.rotate(center, matrix)

    def rotate_y(self, theta):
        for surface in self.surfaces.values():
            center = surface.findCentre()
            c = np.cos(theta)
            s = np.sin(theta)

            matrix = np.array([[c, 0, s, 0],
                               [0, 1, 0, 0],
                               [-s, 0, c, 0],
                               [0, 0, 0, 1]])

            surface.rotate(center, matrix)

    def rotate_z(self, theta):
        for surface in self.surfaces.values():
            center = surface.findCentre()
            c = np.cos(theta)
            s = np.sin(theta)

            matrix = np.array([[c, -s, 0, 0],
                               [s, c, 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]])

            surface.rotate(center, matrix)


class Object:
    def __init__(self):
        self.nodes = np.zeros((0, 4))

    def addNodes(self, node_array):
        ones_column = np.ones((len(node_array), 1))
        ones_added = np.hstack((node_array, ones_column))
        self.nodes = np.vstack((self.nodes, ones_added))

    def findCentre(self):
        mean = self.nodes.mean(axis=0)
        return mean

    def rotate(self, center, matrix):
        for i, node in enumerate(self.nodes):
            self.nodes[i] = center + np.matmul(matrix, node - center)


def main():
    spinx, spiny, spinz = 0, 0, 0

    clock.tick(FPS)

    while True:

        txt = cards()
        card_ascii = asciiTxt(txt)

        xyz = []

        for i in range(MAP_HEIGHT):
            y = - (y_gap * i)
            for j in range(MAP_WIDTH):
                x = x_gap * j
                z = 0
                xyz.append((x, y, z))

        step = 0

        running = True
        while running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()

            pv = Projection(WIDTH, HEIGHT, card_ascii)

            card = Object()
            card_nodes = [i for i in xyz]
            card.addNodes(np.array(card_nodes))
            pv.addSurface('card', card)
            pv.rotate_x(spinx)
            pv.rotate_y(spiny)
            pv.rotate_z(spinz)
            pv.display()

            pg.display.update()
            spinx += 0.06
            spiny += 0.04
            spinz += 0.02

            step += 1
            if step == 200:
                running = False


main()
