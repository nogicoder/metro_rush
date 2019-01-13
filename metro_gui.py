from abc import ABC, abstractmethod
import pyglet
from pyglet.gl import *
from metro import *
from PathFinder import *
from pyglet.window import Window
from pyglet.window import key
from time import time


class ObjectSprite(ABC):
    def __init__(self, name, image, scale, x, y):
        self.name = name
        self.image = image
        self.scale = scale
        self.x = x
        self.y = y

    def draw_image(self):
        self.img = pyglet.image.load(self.image)
        self.anchor_image()
        self.sprite = pyglet.sprite.Sprite(self.img, x=self.x, y=self.y)
        self.sprite.scale = self.scale
        self.sprite.draw()

    @abstractmethod
    def draw_label(self):
        pass

    @abstractmethod
    def anchor_image(self):
        pass

    def draw(self):
        start = time()
        self.draw_image()
        self.draw_label()


class StationSprite(ObjectSprite):

    def draw_label(self):
        self.label = pyglet.text.Label(self.name, font_size=7,
                                       anchor_x='right', anchor_y='top')
        self.label.color = (0, 0, 0, 255)
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(self.x, self.y - 10, 0.0)
        glRotatef(90.0, 0.0, 0.0, 1.0)
        self.label.draw()
        glRotatef(-90.0, 0.0, 0.0, 1.0)
        glPopMatrix()

    def anchor_image(self):
        self.img.anchor_x = self.img.width // 2
        self.img.anchor_y = self.img.height // 2


class TrainSprite(ObjectSprite):

    def draw_label(self):
        self.label = pyglet.text.Label("T" + str(self.name),
                                       x=self.x, y=self.y + 45,
                                       font_size=15,
                                       anchor_x='center', anchor_y='top')
        self.label.color = (0, 0, 0, 255)
        self.label.draw()

    def anchor_image(self):
        self.img.anchor_x = self.img.width // 2
        self.img.anchor_y = self.img.height // 5


class MetroWindow(pyglet.window.Window):
    colors = {"red": (255, 0, 0, 255, 0, 0),
              "yellow": (255, 255, 0, 255, 255, 0),
              "blue": (0, 0, 255, 0, 0, 255),
              "magenta": (255, 0, 255, 255, 0, 255),
              "pink": (255, 192, 203, 255, 192, 203),
              "violet": (238, 130, 238, 238, 130, 238),
              "airport ": (34, 139, 34, 34, 139, 34)
              }

    def __init__(self, file):
        super().__init__(1680, 1000, resizable=True)
        self.background = pyglet.image.load("background.jpg")
        self.metro = Metro(file)
        self.metro.build_graph(file)
        self.path = PathFinding(self.metro)
        self.actions = self.path.get_action_list_1()
        self.lines, self.delta_x, self.delta_y = self.analyse_lines()
        self.coordinates = self.generate_coordinates()
        self.metro.turn = 0
        self.trains_dict = self.generate_trains()

    def connect_dot(self, start_x, start_y, end_x, end_y, color):
        pyglet.gl.glLineWidth(2)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                             ("v2f", (start_x, start_y, end_x, end_y)),
                             ("c3B", color),
                             ("s3B", (0, 0, 0, 0, 0, 255)))

    def draw_line(self, line, color):
        stations = list(line.stations.keys())
        for i, station in enumerate(stations):
            station_sprite = StationSprite(station.name, "white_dot.png", 0.1,
                                           self.coordinates[station.name][0],
                                           self.coordinates[station.name][1])
            station_sprite.draw()
            if i == len(stations) - 1:
                continue
            self.connect_dot(self.coordinates[stations[i].name][0],
                             self.coordinates[stations[i].name][1],
                             self.coordinates[stations[i+1].name][0],
                             self.coordinates[stations[i+1].name][1], color)

    def analyse_lines(self):
        lines = []
        max_number_of_stations = 0
        for line in self.metro.lines.values():
            if line:
                lines.append(line)
                if len(line) > max_number_of_stations:
                    max_number_of_stations = len(line)
        delta_y = self.height/(len(lines) + 1)
        delta_x = self.width/(max_number_of_stations + 1)
        return lines, delta_x, delta_y

    def generate_coordinates(self):
        coordinates = {}
        line_y = self.delta_y
        for line in self.lines:
            # print(line.stations)
            for station, index in line.stations.items():
                if station.name not in coordinates.keys():
                    x, y = index * self.delta_x, line_y
                    coordinates[station.name] = (x, y)
            line_y += self.delta_y
        return coordinates

    def initial_network(self):
        self.background.blit(0, 0, width=window.width, height=window.height)
        for line in self.lines:
            for key in self.colors.keys():
                if key in line.name.lower():
                    self.draw_line(line, self.colors[key])
        pyglet.image.get_buffer_manager().get_color_buffer().save('bg.png')

    def draw_network(self):
        self.clear()
        metro_network = pyglet.image.load("bg.png")
        metro_network.blit(0, 0, width=window.width, height=window.height)

    def draw_trains(self):
        train_sprites = []
        for train, train_coordinates in self.trains_dict.items():
            train_sprite = TrainSprite(train, "train.png", 0.2,
                                       train_coordinates[0],
                                       train_coordinates[1])
            train_sprite.draw()

    def update(self, dt):
        try:
            for action in self.actions[self.metro.turn]:
                if isinstance(action, MoveTrain):
                    self.trains_dict[action.train.id] = \
                      self.coordinates[action.station_2.name]
                elif isinstance(action, SwitchLine):
                    pass
            self.metro.turn += 1
        except IndexError:
            pass

    def generate_trains(self):
        trains_dict = {}
        start = self.metro.start
        for index, train in self.metro.trains.items():
            trains_dict[train.id] = (self.coordinates[start.name][0],
                                     self.coordinates[start.name][1])
        return trains_dict

    def on_draw(self):
        if self.metro.turn == 0:
            self.initial_network()
            self.draw_trains()
        else:
            self.draw_network()
            self.draw_trains()

    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/1)
        pyglet.app.run()


if __name__ == '__main__':
    window = MetroWindow('delhi')
    window.run()
