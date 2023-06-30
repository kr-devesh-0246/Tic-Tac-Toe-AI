import sys
import pygame
import numpy as np
import random
import copy 

from constants import *

#PYGAME
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BG_COLOR)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS,COLS))
        self.empty_sqrs = self.squares # list of squares empty
        self.marked_sqrs = 0 

    def final_state(self): #row,col,player
        '''
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''

        # vertical line
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]  # for a win condition it returns 1
            
        # horizontal line
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][0] == self.squares[col][0] != 0:
                return self.squares[row][0]
            
        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]
        # asc diagonal
        if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] != 0:
            return self.squares[1][1]
        

        # no in yet
        return 0
        


    def mark_sqr(self,row,col,player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self,row,col):
        return self.squares[row][col] == 0
    
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row,col):
                    empty_sqrs.append((row,col))
        return empty_sqrs 
    
    def is_full(self):
        return self.marked_sqrs == 9
    
    def is_empty(self):
        return self.marked_sqrs == 0

class AI:
    def __init__(self,level = 1, player = 2):
        self.level = level
        self.player = player

    def rnd(self,board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0,len(empty_sqrs))

        return empty_sqrs[idx] #(row,col)
    
    def minimax(self,board,maximizing):
        
        # terminal cases is first checked
        case = board.final_state() # a number between 0 and 2 depending on who wins/draw happens

        # player 1 wins
        if case == 1:
            return 1, None #They basically return 2 things: move and -1/+1/0
        
        # player 2 wins
        if case == 2:
            return -1, None #  We are AI and False, it is minimizing. So we must return -1
        
        # draw
        elif board.is_full():
            return 0, None
        
        if maximizing:
            pass
        
        elif not maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

        for (row,col) in empty_sqrs:
            temp_board = copy.deepcopy(board)
            temp_board.mark_sqr(row,col,1)
            eval = self.minimax(temp_board, False)[0]
            if eval > max_eval: # for the first move it will be true 
                max_eval = eval
                best_move = (row, col)
        return max_eval, best_move

    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random' # this is not that imp
            move = self.rnd(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board,False) # False for maximizing 
        print(f'AI has chosen to mark the square in pos {move} with an eval of {eval}')

        return move # row, col
class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 #1-cross #2-circle
        self.game_mode = 'ai' # pvp or ai
        self.running = True
        self.show_lines()

    def show_lines(self):

        screen.fill(BG_COLOR)
        # vertical lines
        pygame.draw.line(screen,LINE_COLOR,(SQSIZE,0),(SQSIZE,HEIGHT),LINE_WIDTH) # line 1
        pygame.draw.line(screen,LINE_COLOR,(WIDTH-SQSIZE,0),(WIDTH-SQSIZE,HEIGHT),LINE_WIDTH) # line 1

        # horizontal lines
        pygame.draw.line(screen,LINE_COLOR,(0,SQSIZE),(WIDTH,SQSIZE),LINE_WIDTH) # line 1
        pygame.draw.line(screen,LINE_COLOR,(0,HEIGHT-SQSIZE),(WIDTH,HEIGHT-SQSIZE),LINE_WIDTH) # line 1
        
    def next_turn(self):
        self.player = self.player % 2 + 1 # it will give alternate 1 and 2

    def draw_fig(self,row,col):
        if(self.player == 1):
            # draw cross
            # we need to use a ascending and a descending line

            # asc line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET) # it is difficult to just sit and code this. Hit and try, paper
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR,start_desc,end_desc,CROSS_WIDTH)

            # asc line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE +SQSIZE - OFFSET) # it is difficult to just sit and code this. Hit and try, paper
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR,start_desc,end_desc,CROSS_WIDTH)

        elif(self.player == 2):
            # draw circle
            center = (col*SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen,CIRC_COLOR,center,RADIUS,CIRC_WIDTH)



def main():
    # object creation
    game = Game()
    board = game.board
    ai = game.ai

    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                
                if(board.empty_sqr(row,col)):
                    board.mark_sqr(row,col,game.player)
                    game.draw_fig(row,col)
                    game.next_turn()
                    # print(board.squares) #prints this on console. Remember

        if game.game_mode == 'ai' and game.player == ai.player:
            # update the screen
            pygame.display.update()
            # ai methods
            row, col = ai.eval(board)

            board.mark_sqr(row,col,ai.player)
            game.draw_fig(row,col)
            game.next_turn()




        pygame.display.update()

main()                