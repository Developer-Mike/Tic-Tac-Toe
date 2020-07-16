import tkinter as tk
from numpy import transpose

size = {'x':3, 'y':3}

def CreateMatrix(size):
    matrix = []
    for y in range(size['y']):
        matrix.append([])
        for x in range(size['x']):
            matrix[y].append(None)
    return matrix

def RemoveMatrix(matrix):
    tmpList = []
    for element in matrix:
        if type(element) == list:
            for innerElement in element:
                tmpList.append(innerElement)
        else:
            tmpList.append(element)
    return tmpList
	
root = tk.Tk()
root.title('Tic Tac Toe')

noneSprite = tk.PhotoImage(file='None.png')
xSprite = tk.PhotoImage(file='X.png')
oSprite = tk.PhotoImage(file='O.png')

turnX = True

def Create2DTicTacToe():
    global fields
    field2D = CreateMatrix(size)
    for y in range(size['y']):
        for x in range(size['x']):
            if fields[x][y]["image"] == str(xSprite):
                field2D[x][y] = 'X'
            elif fields[x][y]["image"] == str(oSprite):
                field2D[x][y] = 'O'
            else:
                field2D[x][y] = None
    return field2D

def CheckForWin(board):
    #Check row and column (rotate)
    for newBoard in [board, transpose(board)]:
        #Check rows
        for row in newBoard:
            if len(set(row)) == 1 and row[0] != None:
                return row[0]
    
    #Check 
    #0 - -
    #- 0 -
    #- - 0
    if len(set([board[0][0], board[1][1], board[2][2]])) == 1 and board[0][0] != None:
        return board[0][0]
    
    #Check 
    #- - 0
    #- 0 -
    #0 - -
    if len(set([board[0][2], board[1][1], board[2][0]])) == 1 and board[0][2] != None:
        return board[0][2]

def UpdateCursor():
    global fields
    for button in RemoveMatrix(fields):
        if turnX:
            button['cursor'] = 'X_cursor'
        else:
            button['cursor'] = 'circle'

def DisableButtons(disable=True):
    global fields
    for button in RemoveMatrix(fields):
        if disable:
            button["state"] = tk.DISABLED
        else:
            button["state"] = tk.ACTIVE

def ResetFields():
    global fields, turnX, winner
    
    try:
        global popup
        popup.destroy()
    except:
        pass
    
    DisableButtons(False)
    for button in RemoveMatrix(fields):
        button['image'] = noneSprite
    
    turnX = True
    UpdateCursor()
    
    winner = None

def Place(X, Y):
    global turnX, fields
    if turnX:
        fields[X][Y]["image"]  = xSprite
        turnX = False
    else:
        fields[X][Y]["image"] = oSprite
        turnX = True
    fields[X][Y]["state"] = tk.DISABLED
    UpdateCursor()
    
    field2D = Create2DTicTacToe()
    global winner
    winner = CheckForWin(field2D)
    if winner != None:
        DisableButtons()
        WinnerScreen()
    else:
        if not None in set(RemoveMatrix(field2D)):
            winner = '\r\r\rDraw'
            DisableButtons()
            WinnerScreen()
        
def WinnerScreen():
    global winner, popup
    
    popup = tk.Toplevel(root)
    popup.title("Game Finished")
    
    def Quit():
        popup.destroy()
        root.destroy()
    
    tk.Label(popup, text='The Winner Is: '+winner).grid(row=0, column=0, columnspan=2)
    tk.Button(popup, text='Replay', relief='groove', command=lambda:ResetFields()).grid(row=1, column=0)
    tk.Button(popup, text='Quit', relief='groove', command=lambda:Quit()).grid(row=1, column=1)
    
    popup.protocol("WM_DELETE_WINDOW", Quit)

fields = CreateMatrix(size)
for y in range(size['y']):
    for x in range(size['x']):
        fields[x][y] = tk.Button(root, 
              width=100, height=100, 
              image=noneSprite, cursor='X_cursor',
              relief='groove', 
              command=lambda x=x, y=y: Place(x, y))
        fields[x][y].grid(row=x, column=y)

root.mainloop()