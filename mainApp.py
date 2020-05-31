from pointer import *

class AStar:

    def __init__(self):
        pygame.init()
        self.DISPLAY = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Grid Test')

        self.grid = Grid(DISPLAY, 15)

        self.checking = True

        self.choosing_start = False
        self.choosing_end = False

        self.start_cell = self.grid[0][0]
        self.end_cell = self.grid[-1][-1]
        self.clicking_thread = Thread(target=self.check_cells)
        self.clicking_thread.start()

    @property
    def start_cell(self):
        return self._start_cell
        
    @start_cell.setter
    def start_cell(self, cell):
        if self._start_cell is not None:
            self.start_cell.role = None
        cell.role = 1
        self.start_cell = cell
    
    @property
    def end_cell(self):
        return self._end_cell
        
    @end_cell.setter
    def end_cell(self, cell):
        if self._end_cell is not None:
            self.end_cell.role = None
        cell.role = 1
        self.end_cell = cell

    def check_cells(self, cell_list=self.grid.cell_list):
        while self.checking:
            for row in cell_list:
                for cell in row:
                    if cell.is_clicked():
                        self.choose_start(cell)
                        self.choose_end(cell)

    def choose_start(self, cell):
        if self.choosing_start:
            self.start_cell = cell
            # self.choosing_start = False

    def choose_end(self, cell):
        if self.choosing_end:
            self.end_cell = cell
            # self.choosing_end = False

    def update_display(self):
        self.DISPLAY.fill((255, 255, 255))
        self.grid.draw()
        pygame.display.update()

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
                
                    

                
            self.update_display()
        pygame.quit()


# def main():
#     ls = Stack([1, 2, 3])
#     ls.push(4)
#     print(ls)

#     # print(ls)
#     # app = AStar()
#     # app.mainloop()

# if __name__ == "__main__":
#     main()