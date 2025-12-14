
# 
class Board:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        
        self.grid = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append("")
            self.grid.append(row)



    def display(self):
        print("\n  0   1   2   3   4   5   6")
        print("-----------------------------")
        for row in self.grid:
            print("|", end=" ")
            for cell in row:
                print(cell if cell else ".", end=" | ")
            print()
        print("-----------------------------")