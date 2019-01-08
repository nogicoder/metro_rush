import pyglet
import process_data

width = 900
height = 900
window = pyglet.window.Window(width, height)

class Dot:
	def __init__(self, name, x, y):
		self.img = pyglet.image.load('white_dot.png')
		self.image_positioning(self.img)
		self.sprite = pyglet.sprite.Sprite(self.img, x=x, y=y)
		self.sprite.scale = 0.005

	def draw(self):
		self.sprite.draw()

	def image_positioning(self, img):
	    img.anchor_x = img.width // 2
	    img.anchor_y = img.height // 2

def draw_point(x, y):
	pyglet.graphics.draw(1, pyglet.gl.GL_POINTS, ('v2i', (x, y)), ('c3B', (255,255,255)))
	# pyglet.gl.glLineWidth(500)


def connect_dot(start_x, start_y, end_x, end_y, color):
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                         ("v2f", (start_x, start_y, end_x, end_y)),
						 ("c3B", color))
    # pyglet.gl.glLineWidth(200)

def draw_line(line, color):
	print(line)
	sprites = []
	for i, info in enumerate(line.info):
		try:
			print(info)
			sprite = Dot(info[1], info[2], info[3])
			sprite.draw()
			connect_dot(line.info[i][2], line.info[i][3], line.info[i+1][2], line.info[i+1][3], color)

		except IndexError:
			pass



color_dict = {"red": (255,0,0, 255,0,0),
			  "yellow": (255,255,0,255,255,0),
			  "blue": (0,0,255,0,0,255),
			  "magenta": (255,0,255,255,0,255),
			  "pink": (255,192,203,255,192,203),
			  "violet": (238,130,238,238,130,238),
			  "Airport": (34,139,34,34,139,34)
			  }


@window.event
def on_draw():
	lines = process_data.process_data("delhi_with_coordinates")
	for line in lines:
		for key in color_dict.keys():
			if line.name == key:
				draw_line(line, color_dict[key])


if __name__ == "__main__":
    pyglet.app.run()
