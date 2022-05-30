import itertools
from msilib import knownbits
import random
from xml.dom import HierarchyRequestErr


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines

    def return_board(self):
        return self.board

class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        self.set_safes = set()
        self.set_mines = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count
    
    def __ne__(self, other):
        return self.cells != other.cells

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def undetermined_cells(self):
        return self.cells

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        
        # If the count of mines is equal a elemennts of determined set, therefore all elements of set is a mine. 
        if self.count == len(self.cells):
            self.set_mines.update(self.cells)
        
        return self.set_mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        if self.count == 0:
            self.set_safes.update(self.cells)

        return self.set_safes 
        

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

            self.set_mines.add(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells: 
            self.cells.remove(cell)
            self.set_safes.add(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
        

    def update_knowledge(self):
        """
        Update knowledge internal and external while the amount of mines, safes and knowledge change.
        """
        
        while True:
            mines_len = len(self.mines)
            safes_len = len(self.safes)
            sentences_len = len(self.knowledge)

            # Update MinesWeeperAI() knowledge based on internal knowledge at each one of the sentences
            for sentence in self.knowledge:
                self.mines.update(sentence.known_mines())
                self.safes.update(sentence.known_safes())
            
            # Update the internal sentence knowledge based on MinesWeeperAI() knowledge
            for sentence in self.knowledge:
                for mine in self.mines:
                    sentence.mark_mine(mine)
                for safe in self.safes:
                    sentence.mark_safe(safe)
            
            # Generates news inferences
            for sub_sentence in self.knowledge:
                for sentence in self.knowledge:
                    
                    # Excludes the sentence itself and nulls sentences
                    if sub_sentence != sentence and sub_sentence.cells != 0 and sentence.cells != 0:
                        
                        # The news inferece need to be a subset
                        if sub_sentence.cells.issubset(sentence.cells):
                           
                            new_inference = Sentence(sentence.cells - sub_sentence.cells, sentence.count - sub_sentence.count)
                            
                            # The inference may not have been made yet
                            if new_inference not in self.knowledge:
                                self.knowledge.append(new_inference)

            # The loop only ends when the number os mines, safes and knowledge not change after the execution
            if mines_len == len(self.mines) and safes_len == len(self.safes) and sentences_len == len(self.knowledge):
                break


    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        self.moves_made.add(cell) # 1 
        self.mark_safe(cell) # 2
        
        # Set to guard all the cells around the cell
        set_sentence = set()
        
        # Loop over all around the cell
        for j in range(cell[0]-1, cell[0]+2):
            for i in range(cell[1]-1, cell[1]+2):
                
                # Ignore the cell itself
                if (j, i) == cell:
                    continue
                
                # Only add if cell is in the board (between 0 and height or width of the board)
                if 0 <= j < self.height and 0 <= i < self.width:
                    # Check if the cell not in moves_made or in safes cells
                    if (j, i) not in self.moves_made and (j, i) not in self.safes:
                        
                        # If is a mine, decrease the counter and not add in the set
                        if (j, i) not in self.mines:
                            set_sentence.add((j, i))
                        else: 
                            count -= 1
        
        cell_sentence = Sentence(set_sentence, count) 
        self.knowledge.append(cell_sentence) # 3
        self.update_knowledge() # 4 e 5

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe in self.safes: 
            if safe not in self.moves_made:
                return safe
        
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        already_tested = set()

        while True:
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            already_tested.add((i, j))

            if (i, j) not in self.moves_made and (i, j) not in self.mines:
                return (i, j)
            elif len(already_tested) == self.height * self.width:
                return None
