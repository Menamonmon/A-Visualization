from wall import *
from cost_functions import *


def is_valid_position(position, maximum, minimum=0):
	return (minimum <= position[0] and minimum <= position[1]) and (maximum >= position[0] and maximum >= position[1])

class Cell:

	def __init__(self, display, position, color=(59, 171, 173), side=None, grid_size=None):
		self.display = display
		self.grid_size = 10 if grid_size is None else grid_size
		display_size = min(self.display.get_size())
		self.side = display_size/self.grid_size if side is None else side
		self.position = position
		self.color = color 
		self.original_color = self.color
		self.upper_wall = Wall(self.display, self.PxlPosition, width=self.unit, height=self.side, parent=self)
		self.lower_wall = Wall(self.display, (self.PxlPosition[0], self.PxlPosition[1] + (self.unit * 7)), width=self.unit, height=self.side, parent=self)
		self.right_wall = Wall(self.display, (self.PxlPosition[0] + (self.unit * 7), self.PxlPosition[1]), width=self.unit, height=self.side, horizontal=0, parent=self)
		self.left_wall = Wall(self.display, self.PxlPosition, width=self.unit, height=self.side, horizontal=0, parent=self)
		self.neighbors = [None, None, None, None]
		self.available = True
		self.role = None
		self.end = None
		self.start = None

	def connect_with_neighbors(self, cell_list):
		for direction in DIRECTIONS:
			x, y = apply_transform(self.position, direction)
			if is_valid_position((x, y), self.grid_size - 1):
				other_cell = cell_list[y][x]
				self.add_neighbor(other_cell)

	@property
	def walls(self):
		return (self.upper_wall, self.left_wall, self.lower_wall, self.right_wall)
	
	@property 
	def x(self):
		return int(self.PxlPosition[0] + self.unit)

	@property 
	def y(self):
		return int(self.PxlPosition[1] + self.unit)

	@property
	def unit(self):
		return self.side/8

	@property
	def PxlPosition(self):
		return ((self.position[0] * self.side), (self.position[1] * self.side))

	@property
	def size(self):
		return (self.unit * 6, self.unit * 6)

	def draw(self):
		if self.role is not None:
			c = COLORS[self.role]
		else:
			c = self.color
		pygame.draw.rect(self.display, c, ((self.x, self.y), self.size))
		for wall in self.walls:
			wall.draw()

	def add_neighbor(self, neighbor):
		direction = determine_direction(self.position, neighbor.position)
		if direction == 0:
			merge_walls(neighbor.lower_wall, self.upper_wall)
		elif direction == 1:
			merge_walls(neighbor.right_wall, self.left_wall)
		elif direction == 2:
			merge_walls(neighbor.upper_wall, self.lower_wall)
		elif direction == 3:
			merge_walls(neighbor.left_wall, self.right_wall)
		else:
			raise Exception(f"The Cell at the position {neighbor.position} can not be a neighbor of the Cell at {self.position}")

		self.neighbors[direction] = neighbor

	def is_touched(self):
		mpos = pygame.mouse.get_pos()
		start = self.PxlPosition
		end = (self.PxlPosition[0] + self.side, self.PxlPosition[1] + self.side)
		return (start[0] <= mpos[0] and mpos[0] <= end[0]) and (start[1] <= mpos[1] and mpos[1] <= end[1]) 

	def is_clicked(self, button=0):
		return int(self.is_touched() and pygame.mouse.get_pressed()[button])

	def use(self):
		self.available = False
		self.color = (255, 255, 0)

	def unuse(self):
		self.available = False
		self.color = self.original_color

	def use_as_pointer(self):
		self.color = (255, 0, 0)

	def f_cost(self):
		return f(self.position, self.start, self.end)

	def g_cost(self):
		return g(self.position, self.start)

	def h_cost(self):
		return g(self.position, self.end)
	
	@property 
	def best_neighbor(self):
		costs_list = [(neighbor, neighbor.f_cost(), neighbor.g_cost(), neighbor.h_cost()) for neighbor in self.neighbors if neighbor is not None] 
		costs_list = sorted(costs_list, key=lambda x: x[1])
		b = costs_list[0]
		repeats = [cost[1] for cost in costs_list].count(b[1])
		if repeats ==  1:
			return b[0]
		else:
			costs_list = sorted(costs_list, key=lambda x: x[3])


def main():
	pygame.init()
	DISPLAY = pygame.display.set_mode((600, 600))
	pygame.display.set_caption('Cell Test')

	cell = Cell(DISPLAY, (3, 3))
	cell2 = Cell(DISPLAY, (3, 4))
	cell.add_neighbor(cell2)

	def update_display():
		global hidden
		DISPLAY.fill((255, 255, 255))

		if cell.is_clicked():
			cell.lower_wall.hide()
		if cell2.is_clicked():
			cell2.upper_wall.hide()

		if cell.is_clicked(2):
			cell.lower_wall.show()
		if cell2.is_clicked(2):
			cell2.upper_wall.show()

		cell.draw()
		cell2.draw()
		pygame.display.update()

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		update_display()
		
	pygame.quit()

if __name__ == '__main__':
	main()