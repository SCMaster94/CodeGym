import tkinter as tk
from tkinter import ttk
import ChessMan as cm
class GUI():
    stadium_w = stadium_h = 640
    dim = 8
    chess_box_size = stadium_w/dim
    images = {}
    color1 = 'white'
    color2 = 'brown'
    high_light = 'yellow'
    kill_color = 'red'
    colors = [color1, color2, high_light, kill_color]
    chess_mans = {}
    chess_list = ['Rook', 'Knight' , 'Bishop', 'Queen' , 'King' , 'Bishop', 'Knight', 'Rook', 'Pawn']
    pawn_up_list = [['Rook', 'Knight'] , ['Bishop', 'Queen']]
    pawn_up_map = []
    chess_map = []
    chess_man_selected = None
    pick_available = None
    player_turn = 'white'
    dest_pos = None
    history = []
    pawn_upto = None
    def __init__(self, root):
        self.message = ""
        self.chess_arrange()
        self.root = root
        self.pawn_up_option = tk.Canvas(root, width=self.chess_box_size*2, height=self.chess_box_size*2)
        self.stadium = tk.Canvas(root, width=self.stadium_w, height=self.stadium_h )
        self.draw_pawn_up_area()
        self.print_board()
        self.print_chess_man() 
        self.pawn_up_option.pack(padx=5, pady=5, side='left')
        self.stadium.pack(padx=5, pady=5, side='right')
        self.stadium.bind("<Button-1>", self.pickup_square)
    
    def new_game(self):
        chess_map = []
        self.print_board()
        self.print_chess_man()
        self.player_turn = 'white'
        

    def pickup_square(self, event):
        selected_column = int(event.x//self.chess_box_size)
        selected_row = int(7 - event.y//self.chess_box_size)
        if selected_column<0 or selected_row<0 or selected_column>7 or selected_row>7:
            return
        else:
            pos = (selected_row, selected_column)           
        if self.chess_man_selected:
            self.move(self.chess_man_selected, pos)
            self.chess_man_selected = None
            self.pick_available = None
            self.print_board()
            self.print_chess_man()
        self.focus(pos)
        self.print_board()

    def move(self, p1, p2):
        begin_pos = p1
        dest_pos = p2
        chess_man = self.chess_map[p1[0]][p1[1]]

        if dest_pos in self.pick_available:
            chess_man_captured = self.chess_map[p2[0]][p2[1]]
            chess_man.fisrt_move = False 
            self.chess_map[p2[0]][p2[1]] = chess_man            
            self.chess_map[p1[0]][p1[1]] = cm.create_piece('-', None)
            self.chess_man_selected = self.chess_map[p2[0]][p2[1]]
            if chess_man_captured.name != '-':
                if chess_man_captured.name.split()[1] == 'King':
                    print('%s win' %self.player_turn)
                    self.player_turn = 'None'
                # if chess_man.name.split()[1] != 'Pawn':
                #     print("da vao day")
                #     self.end_turn()


            if chess_man.name.split()[1] == 'Pawn':
                level = abs(p2[0]-chess_man.startpos)
                if level == 6:
                    self.player_turn = None
                    self.dest_pos = p2
                    print(self.dest_pos)
                    self.pawn_up(chess_man.color)
                else:
                    self.end_turn()
            else:
                self.end_turn()                  
    def pawn_up_comlete(self):
        self.chess_map[self.dest_pos[0]][self.dest_pos[1]] = cm.create_piece(self.pawn_upto.split()[1], self.pawn_upto.split()[0])
        self.chess_map[self.dest_pos[0]][self.dest_pos[1]].place(self) 
        self.player_turn = self.pawn_upto.split()[0]     
        self.end_turn()

    def end_turn(self):
        self.chess_man_selected = None
        self.pick_available = None
        self.print_board()
        self.print_chess_man()
        self.pawn_upto = None
        self.dest_pos = None 
        if self.player_turn == 'white':
            self.player_turn = 'black'
        else:
            self.player_turn = 'white'
                
    def focus(self, pos):
        try:
            chess_man = self.chess_map[pos[0]][pos[1]]
        except:
            chess_man = None
        if chess_man is not None and (chess_man.color == self.player_turn):
            self.chess_man_selected = (pos)
            self.pick_available = self.chess_map[pos[0]][pos[1]].moves_available(pos)
            
    def print_board(self):
        for row in range(self.dim):
            for col in range(self.dim):
                color = self.colors[(row+col)%2]                  
                x1 = col * self.chess_box_size
                y1 = (7 - row) * self.chess_box_size
                x2 = x1 + self.chess_box_size
                y2 = y1 + self.chess_box_size
                if (self.pick_available is not None and (row, col) in self.pick_available):
                    self.stadium.create_rectangle(x1, y1, x2, y2, fill=self.high_light, tags="land")
                else:
                    self.stadium.create_rectangle(x1, y1, x2, y2, fill=color, tags="land")
        self.stadium.tag_raise("chess")
    
    def print_chess_man(self):
        self.stadium.delete("chess")
        for i in range(self.dim):
            for j in range(self.dim):
                if self.chess_map[i][j].name == '-':
                    pass
                else:
                    file_name = "images/%s.png" % (self.chess_map[i][j].name)
                    chess_man_name = self.chess_map[i][j].name + str(i) + str(j)
                    self.stadium.create_image(0, 0, image = self.images[file_name], tags=(chess_man_name, "chess"))
                    xchess = (j * self.chess_box_size) + int(self.chess_box_size/2)
                    ychess = ((7 - i) * self.chess_box_size) + int(self.chess_box_size/2)
                    self.stadium.coords(chess_man_name, xchess, ychess)
                    
                        
    def chess_arrange(self):
        for i in range(self.dim):
            chess_line = []
            if i == 0:
                line_type = self.chess_list
                n=1
                color = "white"
            elif i == 1:
                line_type = ["Pawn"]
                n=8
                color = "white"
            elif i == 6:
                line_type = ["Pawn"]
                n=8
                color = "black"
            elif i == 7:
                line_type = self.chess_list
                n=1
                color = "black"
            else:
                line_type = ['-']
                n = 8
                color = None
            for i in range(n):
                for chess_type in line_type:
                    chess_man = cm.create_piece(chess_type, color)
                    chess_man.place(self)
                    chess_line.append(chess_man)
            self.chess_map.append(chess_line)

        for i in ['white', 'black']:
            for j in self.chess_list:
                chess_man_name = i + " " + j
                file_name = "images/%s.png" % (chess_man_name)
                if file_name not in self.images:
                    self.images[file_name] = tk.PhotoImage(file=file_name)
                    
    def draw_pawn_up_area(self): 
        for row in range(2):
            for col in range(2):
                color = self.colors[(row+col)%2]
                x1 = col * self.chess_box_size
                y1 = (1 - row) * self.chess_box_size
                x2 = x1 + self.chess_box_size
                y2 = y1 + self.chess_box_size
                self.pawn_up_option.create_rectangle(x1, y1, x2, y2, tags="chess", fill=color)
                self.pawn_up_option.tag_raise("chess")
#                 self.pawn_up_option.delete("chess")
    def pawn_up(self, color):
        pawn_up_map = []
        for row in range(2):
            line = []
            for col in range(2): 
                chess_type = self.pawn_up_list[row][col]
                chess_man_name = color + ' ' + chess_type
                file_name = "images/%s.png" % (chess_man_name)
                line.append(chess_man_name)      
                self.pawn_up_option.create_image(0, 0, image = self.images[file_name], tags=(chess_man_name, "chess"))
                xchess = (col * self.chess_box_size) + int(self.chess_box_size/2)
                ychess = ((1 - row) * self.chess_box_size) + int(self.chess_box_size/2)
                self.pawn_up_option.coords(chess_man_name, xchess, ychess)
            pawn_up_map.append(line)
            self.pawn_up_map = pawn_up_map
            self.pawn_up_option.bind("<Button-1>", self.choose)
    
    def choose(self, event):
        selected_column = int(event.x//self.chess_box_size)
        selected_row = int(1 - event.y//self.chess_box_size)
        if selected_column<0 or selected_row<0 or selected_column>1 or selected_row>1:
            return
        else:
            pos = (selected_row, selected_column)
            self.pawn_upto = self.pawn_up_map[pos[0]][pos[1]]
            print(self.pawn_upto)
            self.pawn_up_comlete()
                    
###########################################################################
###########################################################################
###########################################################################
###########################################################################
    def all_moves_available(self, color):
        pass
        
    def game_check(self, color):
        pass

    def checkmate(self, color):
        pass
            
    def king_in_check(self, color):
        pass

def main():
    root = tk.Tk()
    root.title("Chess")   
    gui = GUI(root)
    gui.print_board()
    root.mainloop()

if __name__ == "__main__":
    main()

            