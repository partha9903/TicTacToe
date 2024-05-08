import pygame
import sys 


Width, Height = 600, 600
pygame.init()
screen = pygame.display.set_mode((Width, Height))

screen.fill((255,255,255))
grid = pygame.image.load("TTT.jpeg")
grid = pygame.transform.scale(grid,(Width, Height))
screen.blit(grid,(0,0))

Circle = pygame.image.load("O.png")
Circle = pygame.transform.scale(Circle,(Width/3, Height/3))

Cross = pygame.image.load("X.png")
Cross = pygame.transform.scale(Cross,(Width/3, Height/3))

pygame.display.flip()

class Board:
    def __init__(self):
        self._board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
    
    def draw(self, surf):
        for i in range(3):
            for j in range(3):
                if self._board[i][j] == (+1):
                    surf.blit(Cross, (i * (Width / 3), j * (Height / 3)))
                elif self._board[i][j] == (-1):
                    surf.blit(Circle, (i * (Width / 3), j * (Height / 3)))
            print(self._board[i][::-1])
        print()

    def get_value(self, x, y):
        return self._board[x][y]
    
    def set_value(self, x, y, value):
        if self._board[x][y] == 0 and value in [1,-1]:
            self._board[x][y] = value
            return True
        else : return False

    def undo_move(self, x, y) :
        self._board[x][y] = 0

    def minimax(self,depth,isMaximizing):
        result = self.check()
        if result is not None:
            return result
        if isMaximizing :
            BestScore = -1000
            for i in range(3):
                for j in range(3):
                    if self.set_value(i,j,+1) :
                        score = self.minimax(depth+1,False)
                        self.undo_move(i,j)
                        BestScore = max(score,BestScore)
            return BestScore
        else :
            BestScore = 1000
            for i in range(3):
                for j in range(3):
                    if self.set_value(i,j,-1) :
                        score = self.minimax(depth+1,True)
                        self.undo_move(i,j)
                        BestScore = min(score,BestScore)
            return BestScore
        
    def check(self): # returns player (-1 or 1) or draw (0) or None (havnt reached last stage)
        for x in range (3):
            col = set([i[x] for i in self._board])      #col check
            if (len(col) == 1) and 0 not in col:  
                return col.pop()
            
            row = set(self._board[x])                   #row check
            if (len(row) == 1) and 0 not in row:  
                return row.pop()
        
        M_dia = set([self._board[i][i] for i in range(3)])      #main diagonal check
        if (len(M_dia) == 1) and 0 not in M_dia:
            return M_dia.pop()
        
        S_dia = set([self._board[i][2-i] for i in range(3)])    #sun diagonal check
        if (len(S_dia) == 1) and 0 not in S_dia:
            return S_dia.pop()
        
        #check for draw
        if not any( el == 0 for el in set(self._board[0]+self._board[1]+self._board[2])) :
            return 0
    
        return None  

class Game:
    def __init__(self):
        self.brd = Board()
        #self.Winner = None
        self.Player = 1
    
    def get_clicked_index(self, mouse_pos):
        m_x, m_y = mouse_pos
        x = int(m_x / (Width / 3))
        y = int(m_y / (Height / 3))
        return (x, y)
    
    def PlayerTurn(self,x,y): 
        if self.brd.get_value(x, y) == 0:
            self.brd.set_value(x, y, self.Player)
            self.brd.draw(screen)
            self.Player = (-1)*self.Player   # Toggle player between -1 and 1
        return
    
    def play(self):
        running = True
        while running:
            if self.Player == 1 :
                pygame.event.wait()
                if (pygame.mouse.get_pressed()[0]):
                    x, y = self.get_clicked_index(pygame.mouse.get_pos())
                    self.PlayerTurn(x,y)
            else :
                BestScore = 1000
                BestMove = None 
                
                for i in range(3):
                    for j in range(3):
                        if self.brd.set_value(i,j,self.Player) :
                            score = self.brd.minimax(0,True)
                            self.brd.undo_move(i,j) 
                            if score < BestScore :
                                BestScore = score
                                BestMove = (i,j)
                if BestMove is not None :
                    x, y = BestMove
                    self.PlayerTurn(x,y)
                                
            pygame.display.flip()
                
            res = self.brd.check()
            if res != (None):
                running = False
            
            pygame.event.wait()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("U can't close if u didn't finish the game.")
                    if input("Really wanna quit?(Y/N) :") == 'y' or 'Y' :\
                        running = False
             
        match res :
            case 0:
                print("draw")
            case (1):
                print("X Won")
            case (-1):
                print("O Won")
            case _ :
                pass
    

if __name__ == "__main__" :
    #while True:
        newGame = Game()
        newGame.play()
        #newGame.reset()
        print("Yeyeeeee")
        pygame.display.flip()
          #need a prompt when who's turn 

        