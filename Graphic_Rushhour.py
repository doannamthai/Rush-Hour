### Rush Hour - Graphic Version ###
### Name: Thai Doan
import pygame
import time
import Text_Rushhour
from pygame.locals import *
# Import pgu (GUI for python)
import sys
sys.path.insert(0, '..\pgu-0.18\pgu-0.18')
from pgu import html

class main_game:
    def __init__(self):
        self.cars_board = A4T_Rushhour.Cars_Board()
        self.board_len = self.cars_board.length
        self.cars_data = self.cars_board.all_cars
        self.board_data = self.cars_board.board
        
        self.cor_range = []  # Coordinate range
        self.avail_range = [] # Pixel range
                
        self.cars_pos = [] # Position of cars
        self.old_cars_pos = [] # Position of cars
        
        self.animated_frame_count = 0
        self.t0 = time.clock()
                
        self.board_size = 600
        self.area_len = self.board_size // self.board_len
        self.margin = int(self.area_len*0.2)
        self.box_len = self.area_len - self.margin
        
        self.step_move = 0
        
        self.board_size = self.board_size + self.margin
        self.board_size_len = self.board_size + 3*self.area_len
        
        pygame.init()
        self.colors = {"grey": (204,204,204), 
                           "white":  (255,255,255), 
                               "lightgrey": (242, 242, 242),
                               "black": (79,79,79),
                               "blue": (0, 154, 211)}         
        
        self.my_clock = pygame.time.Clock()        
        self.my_font = pygame.font.SysFont("Courier", 16) 
        
        # Font for title
        
        self.title_font = pygame.font.Font("LucidaGrande.ttf", 60)
        self.title_font.set_bold(True)
        self.title_font.set_italic(True)
        font_size = self.title_font.size("Rush Hour")
        self.font_cor = (self.board_size_len - font_size[0] - self.margin, font_size[1])
        
        # Font in game
        self.time_counter = pygame.font.Font("LucidaGrande.ttf", 18)
        self.txt_time_counter = self.time_counter.render("Time: ", True, self.colors["white"])
        
        
        self.main_board = pygame.display.set_mode((self.board_size_len, self.board_size)) 
       

        self.bg_intro = pygame.image.load("background_intro.png")
         
        # Car attributes #
        self.red_car = pygame.image.load("red_car.png")
        self.list_car_img = {"sm_cars": ["red_car.png", "purple_car.png", "grey_car.png", "green_car.png", "blue_car.png", "yellow_car.png"], 
                             "lg_cars": ["green_truck.png"]
                             }
        self.sm_car_index = 0
        self.lg_car_index = 0
        
        pygame.display.set_caption('Rush Hour')
        #self.intro()
        self.run_game()
            
    def draw_board(self):
        ''' Drawing the board for moving car and the statistic showing step and time '''
        # Draw squares 
        for row in range(self.board_len):
            for column in range(self.board_len):
                # Drawing the small square
                pygame.draw.rect(self.main_board, self.colors["grey"], 
                                 [(self.margin + self.box_len) * column + self.margin, 
                                  (self.margin + self.box_len) * row + self.margin, self.box_len, self.box_len])
        # Draw statistic
        pygame.draw.rect(self.main_board, self.colors["blue"], (self.board_size + self.margin, 0, self.board_size_len - self.board_size - self.margin, self.board_size))
        html.write(self.main_board, self.time_counter, pygame.Rect(self.board_size + self.margin,0,self.board_size_len - self.board_size - self.margin,self.board_size),"""
        <div style='width:"""+str(self.board_size_len - self.board_size - self.margin)+""""; height:"""+ str(self.board_size) +"""; background: #00aeef; border: 1px; border-color: #888888;'></div>
        """)        
        
        self.main_board.blit(self.txt_time_counter, [self.board_size + 2*self.margin, self.margin])        
        
                
    def check_size(self, cur_car):
        if cur_car.size == 2:
            car_img = pygame.image.load(self.list_car_img["sm_cars"][self.sm_car_index])
        elif cur_car.size == 3:
            car_img = pygame.image.load(self.list_car_img["lg_cars"][self.lg_car_index])
        if cur_car.orien == "v":
            car_img = pygame.transform.rotate(car_img, -90)
        elif cur_car.orien == "h":
            self.sm_car_index += 1            
        return car_img
    def draw_cars(self, cur_car, car_col, car_row, dif_x = 0, dif_y = 0):
        pos_left = (self.margin + self.box_len) * car_col + self.margin
        pos_top = (self.margin + self.box_len) * car_row + self.margin
        car_length = self.box_len * cur_car.size + (cur_car.size - 1) * self.margin 
        if self.sm_car_index == 5:
            self.sm_car_index = 0
        car_img = self.check_size(cur_car)                
        if cur_car.orien == "h":
            # self.main_board.blit(car_img, (pos_left + dif_x, pos_top - 10.5))
            pygame.draw.rect(self.main_board, pygame.Color("#b50000"), [pos_left + dif_x, pos_top, car_length, self.box_len]) 
            self.cars_pos.append([pos_left + dif_x, pos_top, pos_left + car_length, pos_top])
        elif cur_car.orien == "v": # Vertical cars                                                  
            # self.main_board.blit(car_img, (pos_left - 8, pos_top + dif_y))        
            pygame.draw.rect(self.main_board, pygame.Color("#004c6d"), [pos_left, pos_top + dif_y, self.box_len, car_length]) 
            self.cars_pos.append([pos_left, pos_top + dif_y, pos_left, pos_top + car_length])
                        
    def click_pos(self, cur_car, pos_list, c_pos):
        ''' Position of the click of the user on any cars'''
        x_tail, y_tail, x_head, y_head = self.cars_pos[pos_list]
        cur_x, cur_y = c_pos                
        if cur_car.orien == "h":
            y_border = y_tail + self.box_len
            return x_tail <= cur_x <= x_head and y_tail <= cur_y <= y_border
        else:
            x_border = x_tail + self.box_len 
            return x_tail <= cur_x <= x_border and y_tail <= cur_y <= y_head 
        
    def car_range(self):
        self.avail_range = []
        self.cor_range = []
        for car in self.cars_data:
            for t in car: 
                range_of_car = t.move_range(self.board_data) 
                dif_pos = ( self.margin + self.box_len ) * (t.size - 1)
                tail_range = ( self.margin + self.box_len ) * range_of_car[0] + self.margin
                head_range = ( self.margin + self.box_len ) * range_of_car[1] + self.margin
                tail_head  = head_range  - dif_pos
                self.cor_range.append(range_of_car)                
                self.avail_range.append([tail_range, tail_head])
                
    def check_move(self, cur_car, dif_x, dif_y, rel_x, rel_y, move_range):
        tail, head = move_range
        pos_x = (self.margin + self.box_len) * cur_car.column + self.margin
        pos_y = (self.margin + self.box_len) * cur_car.row + self.margin        
        if cur_car.orien == "h":
            if tail <= pos_x + dif_x <= head:
                pass
            else:
                if rel_x < 0:
                    dif_x = tail - pos_x
                elif rel_x > 0:
                    dif_x = head - pos_x   
        else:
            if tail <= pos_y + dif_y <= head:
                pass
            else:
                if rel_y < 0:
                    dif_y = tail - pos_y
                elif rel_y > 0:
                    dif_y = head - pos_y
        return dif_x, dif_y
    
    def animation(self, cur_car, pos_list):
        rel = 4
        speed_x, speed_y = 0, 0
        new_row, new_col = cur_car.row, cur_car.column
        pos_new_x = (self.margin + self.box_len) * new_col + self.margin
        pos_new_y = (self.margin + self.box_len) * new_row + self.margin
        x_tail, y_tail, x_head, y_head = self.old_cars_pos[pos_list]
        if cur_car.orien == "h": # Horizontal car
            speed_x = (pos_new_x - x_tail)/rel
        else:
            speed_y = (pos_new_y - y_tail)/rel
        return speed_x, speed_y
                
    def update_move(self, car_name, dif_x, dif_y):
        for pos, car in enumerate(self.cars_data):
            for t in car: 
                if t.name == car_name:
                    old_col, old_row = t.column, t.row                   
                    if t.orien == "h":       
                        num_move = round( dif_x / self.area_len )
                    elif t.orien == "v":
                        num_move = round( dif_y / self.area_len ) 
                    t.move_car(num_move, self.board_data, self.cor_range[pos])
                    return (t.name, pos, old_col, old_row)
    def intro(self):
        while (True):
            control = pygame.event.poll() 
            if control.type == pygame.QUIT: 
                break
            
            
            self.bg_intro = pygame.transform.scale(self.bg_intro, (self.board_size_len, self.board_size))
            self.main_board.blit(self.bg_intro, (0,0))   
            
            the_title = self.title_font.render("Rush Hour", True, self.colors["white"])
            
            self.main_board.blit(the_title, self.font_cor)           
            pygame.display.flip()
            self.my_clock.tick(60)
            
    def run_game(self):
        is_press, is_move = False, False
        rel_x, rel_y, dif_x, dif_y = 0, 0, 0, 0        
        car_name, car_animated = None, None
        while (True):
            control = pygame.event.poll() 
            self.animated_frame_count += 1                      
            if control.type == pygame.QUIT: 
                break
            elif car_animated == None and control.type == pygame.MOUSEBUTTONDOWN:
                cur_pos = control.dict["pos"]
                for pos_list, car in enumerate(self.cars_data):
                    for t in car:
                        if self.click_pos(t, pos_list, cur_pos):
                            is_press = True
                            car_name = t.name
            elif is_press and control.type == pygame.MOUSEBUTTONUP:
                is_press, is_move = False, False
                car_animated, position, old_column, old_row = self.update_move(car_name, dif_x, dif_y)
                car_name = None

            elif is_press and control.type == pygame.MOUSEMOTION:
                is_move = True
                mouse_move = control.dict["rel"]
                rel_x, rel_y = mouse_move                 
                dif_x += rel_x
                dif_y += rel_y
                
            self.main_board.fill(self.colors["lightgrey"]) # Set the color of the screen 
            self.car_range()  
            self.cars_pos = []                          
            self.draw_board()
        
            for pos, car in enumerate(self.cars_data):
                for t in car:        
                    pos_x = (self.margin + self.box_len) * t.column + self.margin
                    pos_y = (self.margin + self.box_len) * t.row + self.margin  
                    if is_move and t.name == car_name:
                        if self.cars_board.gameover(t, self.cor_range[pos][1]):
                            return
                            #the_text = self.my_font.render("You win", True, (0,0,0))
                            #self.main_board.blit(the_text, (10, 10))                          
    
                        dif_x, dif_y = self.check_move(t, dif_x, dif_y, rel_x, rel_y, self.avail_range[pos])                    
                        self.draw_cars(t, t.column, t.row, dif_x, dif_y)                      
                    else:
                        if t.name == car_animated: 
                            if round(self.old_cars_pos[pos][0]) == pos_x and round(self.old_cars_pos[pos][1]) == pos_y:
                                car_animated = None
                                dif_x, dif_y, rel_x, rel_y = 0, 0, 0, 0
                                self.draw_cars(t, t.column, t.row, dif_x, dif_y)
                            else:
                                rel_x, rel_y = self.animation(t, pos)
                                dif_x += rel_x
                                dif_y += rel_y
                                self.draw_cars(t, old_column, old_row, dif_x, dif_y)                                                                                
                        else:
                            self.draw_cars(t, t.column, t.row, dif_x = 0, dif_y = 0)
                            
            self.old_cars_pos[:] = self.cars_pos[:]   
            
            pygame.display.flip()
            self.my_clock.tick(60)
            
        pygame.quit()     

if __name__ == '__main__' :
    rush_hour = main_game()
