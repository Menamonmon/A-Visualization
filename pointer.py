from grid import *


class Pointer:

	def __init__(self, grid):
		self.grid = grid

	def test_traverse(self):
		for q in range(self.grid.size):
			even = q % 2 == 0
			for cell in self.grid[q]:
				if not even :
					cell.right_wall.hide()
				else:
					cell.left_wall.hide()
			if not even:
				self.grid[q][-1].lower_wall.hide()
			else:
				self.grid[q][0].lower_wall.hide() 

def main():
	pygame.init()
	DISPLAY = pygame.display.set_mode((600, 600))
	pygame.display.set_caption('Grid Test')

	grid = Grid(DISPLAY, 15)

	pointer = Pointer(grid)

	checking = True

	def check_cells(cell_list):
		while checking:
			for row in cell_list:
				for cell in row:
					if cell.is_clicked():
						for wall in cell.walls:
							wall.hide()
					if cell.is_clicked(2):
						for wall in cell.walls:
							wall.show()

	clicking_thread = Thread(target=lambda x=None: check_cells(grid.cell_list))
	clicking_thread.start()

	def update_display():
		DISPLAY.fill((255, 255, 255))
		grid.draw()
		pygame.display.update()

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					pointer.test_traverse()

		update_display()
	checking = False
	pygame.quit()

if __name__ == '__main__':
	main()