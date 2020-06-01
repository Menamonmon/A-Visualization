from grid import *

def retrace_path(start, end):
		path = []
		current_cell = end
		
		while current_cell != start:
			path.append(current_cell)
			current_cell = current_cell.parent

		return reversed(path)

class AStar:

	def __init__(self):
		pygame.init()
		self.DISPLAY = pygame.display.set_mode((600, 600))
		pygame.display.set_caption('Grid Test')

		self.grid = Grid(self.DISPLAY, 30)

		self.checking = True
		self._start_cell = None
		self._end_cell = None
		self.choosing_start = False
		self.choosing_end = False
		self.algo_started = False
		self.start_cell = self.grid[0][0]
		self.end_cell = self.grid[-1][-1]
		self.clicking_thread = Thread(target=self.check_cells)
		self.clicking_thread.start()
		self.current_cell = self.start_cell
		self.path = []
		self.clock = pygame.time.Clock()

	def assign_source_and_goal(self):
		for row in self.grid:
			for cell in row:
				cell.start = self.start_cell
				cell.end = self.end_cell

	@property
	def start_cell(self):
		return self._start_cell
		
	@start_cell.setter
	def start_cell(self, cell):
		if self._start_cell is not None:
			self.start_cell.role = None
		cell.role = 1
		self._start_cell = cell
	
	@property
	def end_cell(self):
		return self._end_cell
		
	@end_cell.setter
	def end_cell(self, cell):
		if self._end_cell is not None:
			self.end_cell.role = None
		cell.role = 0
		self._end_cell = cell

	def check_cells(self, cell_list=None):
		if cell_list is None:
			cell_list = self.grid.cell_list
		while self.checking and not self.algo_started:
			for row in cell_list:
				for cell in row:
					if cell.is_clicked():
						if self.choosing_start:
							self.start_cell = cell
						elif self.choosing_end:
							self.end_cell = cell
						else:
							cell.role = 3
					if cell.is_clicked(2):
						cell.role = None

	def update_display(self):
		self.DISPLAY.fill(COLORS[4])
		self.grid.draw()
		pygame.display.update()
		self.clock.tick(60)

	def a_star(self):
		if self.start_cell.role != 1 or self.end_cell.role != 0:
			return
		self.algo_started = True
		self.assign_source_and_goal()
		open_list = []
		closed_list = []
		open_list.append(self.start_cell)

		stack_length = 0

		while len(open_list) > 0:
			if stack_length > (self.grid.size ** 2): # To handle stack overflow
				break

			# choosing the cell in the open list with the lowest f cost 
			current_cell = open_list[0]
			for i in range(len(open_list)):
				if open_list[i].f_cost() < current_cell.f_cost() or (open_list[i].f_cost() == current_cell.f_cost() and open_list[i].h_cost() < current_cell.h_cost()): 
					current_cell = open_list[i]

			current_cell.color = (255, 46, 63) # current cells are red colors
			# moving the current cell form the open list to the closed one
			open_list.remove(current_cell)
			closed_list.append(current_cell)

			# break and show the path in blue if the current cell is the end (target) cell
			if current_cell == self.end_cell:
				path = retrace_path(self.start_cell, self.end_cell)
				for cell in path:
					cell.color = (46, 255, 252)
					self.update_display()
				return

			for neighbor in current_cell.neighbors: # looping over the available neighbors and the ones that are not blocks
				neighbor.color = (46, 255, 81)
				if neighbor in closed_list: # skip the adding of the neighbor if it's in the closed list
					continue
				
				cost_to_neighbor = current_cell.h_cost() + distance(neighbor.position, current_cell.position) # the cost of moving to the neighbor 
				if cost_to_neighbor < neighbor.h_cost() or neighbor not in open_list:
					neighbor.parent = current_cell
					neighbor._h = cost_to_neighbor

					if neighbor not in open_list:
						open_list.append(neighbor)

			stack_length += 1
			if stack_length % 3 == 0:
				self.update_display()

	def mainloop(self):
		running = True
		g = 0
		while running:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.checking = False
					running = False

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.checking = not checking
					elif event.key == pygame.K_s:
						self.choosing_start = True
					elif event.key == pygame.K_e:
						self.choosing_end = True
					elif event.key == pygame.K_RETURN:
						self.a_star()
						self.algo_started = False
					elif event.key == pygame.K_r:
						self.grid.reset()
						self.start_cell = self.grid[0][0]
						self.end_cell = self.grid[-1][-1]
						self.algo_started = False
						self.clicking_thread = Thread(target=self.check_cells)
						self.clicking_thread.start()
			
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_s:
						self.choosing_start = False
					elif event.key == pygame.K_e:
						self.choosing_end = False
				
			self.update_display()
		pygame.quit()


def main():
	app = AStar()
	app.mainloop()

if __name__ == "__main__":
	main()