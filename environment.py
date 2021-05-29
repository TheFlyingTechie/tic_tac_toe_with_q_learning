# Environment class to train our AIs in.
# It contains all information the bots
# will need to play a game

class Environment:
    def __init__(self, length: int) -> None:
        self.length = length  # Length of the board
        self.x = 1.0  # The 'x' symbol. It has a value to make it easier to calculate states and the winner
        self.o = -1.0  # The 'o' symbol
        self.winner = None
        self.ended = False
        # This variable holds the information for the number of possible states.
        self.states = 3**(self.length**2)
        # There are 3 possible states for each square; x, o, or empty.
        # The board has a size of length x length. That means the number of possible states are,
        # in the case of a 3 x 3 board, 19 683 states.
        self.board = self.init_board()  # Call the init_board which returns a fresh board

    def init_board(self) -> list:
        '''
        The function to create a new board. I have chosen to have it return a board instead
        of adding it directly to the self.board variable because I want it to be more
        flexable, and I can create new boards for the AI to test on easily

        All this function does is make an array of size length x length, and then fill it with zeros.
        Returns a 2D array
        '''
        board = []
        for row in range(self.length):
            board.append([])
            for _ in range(self.length):
                board[row].append(0.0)

        return board

    def reset(self) -> None:
        '''
        Completely reset the board and game. This is for reuseablity purposes

        It overwrites the self.board variable with a fresh board
        '''
        self.board = self.init_board()
        self.winner = None
        self.ended = False

    def is_empty(self, position: tuple) -> bool:
        '''
        Returns true if the position on the board is empty, else false
        '''
        x, y = position[:2]
        return self.board[x][y] == 0.0

    def get_reward(self, symbol: int) -> int:
        '''
        Returns the award of the current state
        '''
        if not self.game_over():
            return -1
        if self.ended and self.winner == symbol:
            return 5
        elif self.ended and self.winner == None:
            return 2
        else:
            return -5

    def get_state(self, custom_board: any = None) -> int:
        '''
        This function gets the current state of the global board, or a custom one
        '''
        if not custom_board:
            k = 0
            h = 0
            for x in range(self.length):
                for y in range(self.length):
                    v = 0
                    if self.board[x][y] != 0:
                        if self.board[x][y] == self.x:
                            v = 1
                        else:
                            v = 2
                    h += (3**k)*v
                    k += 1
        else:
            k = 0
            h = 0
            for x in range(len(custom_board)):
                for y in range(len(x)):
                    v = 0
                    if custom_board[x][y] != 0:
                        if custom_board[x][y] == self.x:
                            v = 1
                        else:
                            v = 2
                    h += (3**k)*v
                    k += 1
        return h

    def game_over(self) -> bool:
        '''
        Checks the entire board to see if the game is over by checking the sums of the rows.
        This is where the values for symbols comes in handy
        '''
        if self.ended:
            return True

        rotated_board = self.rotate()  # Create a new board that is rotated 90º clockwise

        for player in (self.x, self.o):  # This is to prevent repeat repetition
            for row in self.board:  # Loop over each row in the board
                # And check if the sum of the row is equal to the current player
                if sum(row) == player*self.length:
                    self.winner = player
                    self.ended = True
                    return True

            for row in rotated_board:  # Doing the same for the rotated board
                if sum(row) == player*self.length:
                    self.winner = player
                    self.ended = True
                    return True

            for board in (self.board, rotated_board):  # Checking the diagonals
                diagonal = []
                for i in range(self.length):
                    diagonal.append(board[i][i])
                if sum(diagonal) == player*self.length:
                    self.winner = player
                    self.ended = True
                    return True

        count = 0  # Since there are no rows of length self.length, check if the entire board is filled
        for row in self.board:
            for item in row:
                if item != 0:
                    count += 1
        if count == self.length**2:
            self.winner = None
            self.ended = True
            return True

        return False

    def rotate(self) -> list:
        '''
        This function is to rotate the board.

        Returns a list of the rotated board
        '''
        rotated = list(zip(*self.board[::-1]))
        # Converting all tuples back into a list. zip function return tuples, but we can't
        for row_index in range(len(rotated)):
            rotated[row_index] = list(rotated[row_index])  # work with that
        return rotated

    def print_board(self) -> None:
        '''
        This function print the board. This is pretty much only for human benefit
        '''
        values = self.convert_float_to_symbol(self.board)
        # First, all values have to be converted to something humans can easily
        # understand. All of this code is dynamic, so that way we can print a board of any size
        for length in range(self.length):
            print('\t' + '     |'*int(self.length-1))
            print('\t', end='')
            for width in range(self.length):
                if width != self.length-1:
                    print('  {}  |'.format(str(values[length][width])), end='')
                else:
                    print('  {}'.format(str(values[length][width])))
            if length == self.length-1:
                print('\t' + '     |'*int(self.length-1))
            else:
                print('\t' + '_____|'*int(self.length-1)+'_____')

    def convert_float_to_symbol(self, board: list) -> list:
        '''
        This function loops over the board and turns all floats into a symbol

        Returns a human reabable board
        '''
        corrected_board = []
        for x in range(self.length):
            corrected_board.append([])
            for _ in range(self.length):
                corrected_board[x].append(' ')
        for row_index, row in enumerate(board):
            for value_index, value in enumerate(row):
                if value == -1.0:
                    corrected_board[row_index][value_index] = 'o'
                elif value == 1.0:
                    corrected_board[row_index][value_index] = 'x'
        return corrected_board
