### Rush Hour - Text Version ###
### Name: Thai Doan
import string
class Cars_Board:
    def __init__(self):
        ''' Initialize the class '''
        self.width = 6
        self.length = 6
        self.board = []
        self.all_cars = []
        self.avail_range = []        
        self.def_car = "r"
        self.up_letters = string.ascii_uppercase
        self.cars_list_name = self.def_car + self.up_letters
        self.set_board()
        self.read_data()        
              
    def read_data(self):
        ''' Reading data of the cars from the file and at the same time, add the current car to the board '''
        file_read =  open("file1.txt", "r")  # Open the file
        pos = 0                              # To get the respective letter in cars_list_name 
        while (True):
            read_line = file_read.readline() # Start reading every line
            if len(read_line) == 0:          # If it finishes reading, break the loop
                break
            list_ele = read_line.strip().split(", ") # Split the line
            c_orien,c_size,c_row,c_column = list_ele # Getting the given data from the file
            c_name = self.cars_list_name[pos]        # Name for the current car
            car_setup = cars(c_orien,c_size,c_row,c_column,c_name) 
            car_setup.add_car(self.board)            # Adding car to the board
            self.all_cars.append([car_setup])        # Saving all cars data to the cars list
            pos += 1
        file_read.close()
    
    def set_board(self):
        ''' Create a list to save the current position on the board '''
        for row in range(self.width):
            column = self.width*["-"]
            self.board += [column]
        
    def display(self):
        ''' Convert a nested list to a board (text) '''
        new_str = ""
        len_b = len(self.board)
        for i in range(len_b):
            row_str = '  '.join(self.board[i])
            new_str += row_str + "\n"
        return new_str
    
    def gameover(self, cur_car, head_range):
        ''' Check if the game is over '''
        ## head_range: the maximum range that the head of car can reach
        if cur_car.name == self.def_car:          # If the current car is the default car
            gate = len(self.board[cur_car.row])   # Find the last column to win of the car's row on the board
            return head_range + 1 == gate         # If the the head of the car reach the last column
        return False      
        
    def main_game(self):
        ''' Main function to run the text version '''
        stop_loop = False  
        board_line = self.display()
        print(board_line) 
        while (not stop_loop):
            c_name, num_move = input("Name, move: ").split(", ") # Split the command from the terminal 
            num_move = int(num_move) 
            for car_data in self.all_cars:                       
                for t in car_data:
                    range_car = t.move_range(self.board)
                    self.avail_range.append(range_car)           # Update the range the car can move
                    
            for pos, car in enumerate(self.all_cars):           
                for e in car:                    
                    if e.name == c_name:                         # If the current car is the car called in command line
                        e.move_car(num_move, self.board, self.avail_range[pos])    # Move the car
                        board_line = self.display()
                        print(board_line)
                        stop_loop = self.gameover(e, self.avail_range[pos][1])     # Check if the game is over
                        self.avail_range = []                                      # Reset the available range     
                        break
    def call_func(self):
        '''  A function for calling the main_game and display '''
        self.main_game()
        self.display()          
        
class cars:
    def __init__(self, car_orien, car_size, car_row, car_column, car_name):
        ''' Initialize the current car '''
        self.orien = car_orien
        self.size = int(car_size)
        self.row = int(car_row)
        self.column = int(car_column)
        self.name = car_name
        
    def add_car(self, board):
        ''' A function to add the current car to the board based on the given position '''
        if self.orien == "h":  # Horizontal car
            # For the horizontal car, row will be consistent but column will change
            cur_row = board[self.row]
            board[self.row] = cur_row[:self.column] + [self.name]*self.size + cur_row[self.column + self.size:]
        else:                  # Vertical car
            # For the vertical car, row will change but colmn will be consistent
            for i in range(self.row, self.row + self.size):
                board[i][self.column] = self.name
                
    def move_range(self, board):
        ''' A list contains the possible range can move for every car '''
        range_from, range_to = 0, 0                 
        if self.orien == "h":
            cur_row = board[self.row]
            to_left = 1
            to_right = 1
            first_done, second_done = False, False
            head_car = self.column + self.size - 1
            while (True):
                if first_done and second_done:
                    break
                # From tail car to left
                if not first_done  and self.column - to_left >= 0 and cur_row[self.column - to_left] == "-":
                    range_from = self.column - to_left
                    to_left += 1
                else:
                    range_from = self.column - to_left + 1
                    first_done = True
                # From head car to right
                if not second_done and head_car + to_right < len(cur_row) and cur_row[head_car + to_right] == "-":
                        range_to = head_car + to_right
                        to_right += 1                        
                else:
                    range_to = head_car + to_right - 1
                    second_done = True
        elif self.orien == "v":
            head_car = self.row + self.size - 1
            # From tail car to top
            for i in range(1, self.row + 1):
                if board[self.row - i][self.column] == "-":
                    range_from = self.row - i
                else:
                    range_from = self.row - i + 1
                    break
            # From head car to bottom
            for k in range(len(board) - head_car):
                if (board[head_car + k][self.column] == "-") or (board[head_car + k][self.column] == self.name):
                    range_to = head_car + k
                else:
                    range_to = head_car + k - 1
                    break       
        return (range_from, range_to)
        
    def move_car(self, num_move, board, car_range):
        num_move = int(num_move)
        range_tail, range_head = car_range
        if self.orien == "h": #Horizontal car
            head_car = self.column + self.size - 1 
            if num_move < 0 and (self.column - abs(num_move)) >= range_tail :
                board[self.row][self.column - abs(num_move) : head_car + 1] = [self.name]*self.size + abs(num_move)*["-"]
                self.column +=  num_move #Update the new position
            elif num_move > 0 and (head_car + num_move) <= range_head:
                board[self.row][self.column : head_car + num_move + 1] = num_move*["-"] + [self.name]*self.size
                self.column +=  num_move #Update the new position       
        elif self.orien == "v": #Vertical car
            ### Vertical cars ### 
            head_car = self.row + self.size - 1 
            if num_move > 0 and head_car + num_move <= range_head :
                for i in range(self.row, head_car + num_move + 1):
                    if i < (self.row + num_move):
                        board[i][self.column] = "-"
                        continue
                    board[i][self.column] = self.name                
                self.row += num_move
            elif num_move < 0 and self.row - abs(num_move) >= range_tail:
                for i in range(self.row - abs(num_move), head_car + 1):
                    if i > (head_car - abs(num_move)):
                        board[i][self.column] = "-"
                        continue
                    board[i][self.column] = self.name                
                self.row += num_move                
             
if __name__ == '__main__' :
    rush_hour = Cars_Board()
    rush_hour.call_func()
