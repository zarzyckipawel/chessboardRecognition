import random
import time
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ChessBoard:
    def __init__(self):
        n = 9
        self.name = "tst_"
        self.Squares = [[0] * n for i in range(n)]

    def SqaureToPiece(self, number):
        switcher = {
            1:  "pawn",
            2:  "knight",
            3:  "bishop",
            4:  "rook",
            5:  "queen",
            6:  "king"
        }
        return switcher.get(number,"empty")
    
    def ToFen(self):
        rows = list()
        lineSeparator = "/"        
        emptyBuffer = 0
        for x in range(8, 0 , -1):
            row = ""
            for y in range(8, 0, -1):
                character = self.Squares[x][y]                
                if character == "e":
                    emptyBuffer += 1
                else:                  
                    row += self.flushBuffer(emptyBuffer) 
                    emptyBuffer = 0 
                    row += character        
            row += self.flushBuffer(emptyBuffer)
            emptyBuffer = 0
            rows.append(row)
        return lineSeparator.join(rows)
    
    def flushBuffer(self, number):
        return "" if number == 0 else str(number)
    
    def PrintMatrix(self):
        for x in range(8, 0 , -1):
            line = ""
            for y in range(8, 0, -1):
                line += self.Squares[x][y]  
            print(line)
    
    def SetRandomPosition(self):
        for x in range(8, 0 , -1):
            for y in range(8, 0, -1):
                empty = False if random.randint(0,3) == 0 else True
                if empty:
                    self.Squares[x][y] = "e"
                else:
                    side = random.randint(0,1)
                    piece = random.randint(1, 10) 
                    pieceToss = piece if piece <= 6 else 1 # increase probability of pawns
                    pieceCharacter = self.SqaureToPiece(pieceToss)[0]
                    pieceCharacter = pieceCharacter if side == 0 else pieceCharacter.upper()
                    self.Squares[x][y] = pieceCharacter

    def ProduceImage(self):
        fen = self.ToFen()
        content = f'<iframe src="http://chessforeva.appspot.com/C0_dg.htm?fen={fen} b - - 0&width=700&height=460" width="700" height="460" frameborder="0" name="framename"></iframe>'
        f = open("demofile.html", "w")
        f.write(content)
        f.close()
        self.renderer_func()
    
    def renderer_func(self):   
        time.sleep(2)        
        self.driver.get("C:\\Users\\pzar\\Desktop\\AI days\\GenerateTrainingSet\\demofile.html")
        print(self.driver.page_source)
        screenshot = self.driver.save_screenshot(f'out/{self.name}.png')
        f = open(f'out/{self.name}.fen', "w")
        f.write(self.ToFen())
        f.close()
        

    def massProduce(self):
        DRIVER = 'D:\Program Files\Python36\Lib\site-packages\chromedriver\chromedriver.exe'
        self.driver = webdriver.Chrome(DRIVER)
        for x in range (0, 1000):
            ch.name = "tst_" + str(x)
            ch.SetRandomPosition()
            ch.ProduceImage()
        self.driver.close()
        



ch = ChessBoard()
ch.massProduce()

print(ch.ToFen())
                
                
                
                
            
        
