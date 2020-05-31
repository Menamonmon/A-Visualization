from cell import *

class Grid:

	def __init__(self, display, size=20):
		self.display = display
		self.size = size
		self.min_width = min(self.display.get_size())
		self.cell_side = self.min_width/self.size
		self.cell_list = [ [ Cell(self.display, (x, y), grid_size=self.size) for x in range(self.size) ] for y in range(self.size) ]
		# self.cell_list = [ [ Cell(self.display, (c, r), grid_size=self.size) for c in range(self.size) ] for r in range(self.size) ]
		self.connect_cells()

	def __iter__(self):
		for row in self.cell_list:
			yield row

	def __getitem__(self, index):
		return self.cell_list[index]

	def connect_cells(self):
		for row in self.cell_list:
			for cell in row:
				cell.connect_with_neighbors(self.cell_list)

	def draw(self):
		for r in self.cell_list:
			for cell in r:
				cell.draw()

# def main():
pygame.init()
DISPLAY = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Grid Test')

grid = Grid(DISPLAY, 15)

checking = True

choosing_start = False
choosing_end = False

start_cell = None
end_cell = None

def check_cells(cell_list):
	global choosing_end, choosing_start, start_cell, end_cell
	while checking:
		for row in cell_list:
			for cell in row:
				if cell.is_clicked():
					if choosing_start:
						if start_cell != None:
							start_cell.role = None
						start_cell = cell
						cell.role = 1
						start_cell = cell
						# print(f"Cell at {cell.position} is the start")
						choosing_start = False
					
					elif choosing_end:
						if end_cell != None:
							end_cell.role = None
						# print(f"Cell at {cell.position} is the end")
						cell.role = 0
						choosing_end = False
						end_cell = cell
					# for wall in cell.walls:
					# 	wall.hide()
				# if cell.is_clicked(2):
					# for wall in cell.walls:
					# 	wall.show()

clicking_thread = Thread(target=lambda x=None: check_cells(grid.cell_list))
clicking_thread.start()

def update_display():
	DISPLAY.fill((255, 255, 255))
	grid.draw()
	pygame.display.update()

running = True
while running:
# 	choosing_start = False
# 	choosing_end = False

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				checking = not checking
			elif event.key == pygame.K_s:
				choosing_start = True
			elif event.key == pygame.K_e:
				choosing_end = True
				
		
	update_display()
checking = False
pygame.quit()

# if __name__ == '__main__':
# 	main()