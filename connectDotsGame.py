#Import turtle library
import turtle


#Class for connect objects.  Have an x location, a y location, a value (0,1,2 for representing player who owns tiles), and count for debugging
class Bubble:
    def __init__(self,x, y, value, count=0):
        self.x = x
        self.y = y
        self.value = value
        self.count = count

#Draws the board for the game onto the screen.
def drawBoard(dimensionX, dimensionY):
    xVal = -10*dimensionX
    yVal = -10*dimensionY
    offSet = 20
    locationArray = []

    #Write numbers under screen
    tempVal = xVal
    for x in range(dimensionX):
        turtle.up()
        turtle.goto(tempVal, yVal-offSet)
        turtle.down()
        turtle.write(x)
        turtle.up()
        tempVal += offSet

    #Loop for y axis
    for i in range(dimensionY):
        turtle.up()
        turtle.goto(xVal,yVal)
        locationArray.append([])
        #Loop for x axis
        for j in range(dimensionX):
            turtle.down()
            turtle.circle(3)
            turtle.up()
            turtle.forward(offSet)
            locationArray[i].append(Bubble(xVal, yVal, 0, "x:"+str(j+1)+" = y:"+str(i)))
            xVal += offSet
        xVal = -10 * dimensionX
        yVal += offSet
    locationArray.reverse()
    return locationArray

#Displays board in the terminal for debugging purposes.
def displayBoard(playVar):
    board = []
    for i in playVar:
        temp = []
        for j in i:
            temp.append(j.value)
            #temp.append([j.value,j.x,j.y])
        board.append(temp)
    for i in board:
        print(i)


#Fills the spaces on the board with a turtle circle based on the board, space, and player.
def checkSpace(board, space, player):
    elemNum = len(board)-1
    while True:
        if elemNum < 0:
            break
        if board[elemNum][space].value == 0 and player == 1:
            board[elemNum][space].value = 1
            xVal = board[elemNum][space].x
            yVal = board[elemNum][space].y
            turtle.up()
            turtle.color("black", "red")
            turtle.goto(xVal, yVal)
            turtle.down()
            turtle.begin_fill()
            turtle.circle(3)
            turtle.end_fill()
            turtle.up()
            break
        elif board[elemNum][space].value == 0 and player == 2:
            board[elemNum][space].value = 2
            xVal = board[elemNum][space].x
            yVal = board[elemNum][space].y
            turtle.up()
            turtle.color("black", "blue")
            turtle.goto(xVal, yVal)
            turtle.down()
            turtle.begin_fill()
            turtle.circle(3)
            turtle.end_fill()
            turtle.up()
            break
        else:
            elemNum -= 1

#Logic to check if there are four in a row in any given direction
def checkWin(space, board):
    count = 0
    #Initially the win variable is set to False.
    win = False
    while True:
        #Counts downwards until it hits the tile that was last placed in that row.
        if board[count][space].value == 0:
            count += 1
        #Perform checks
        else:
            #Check Horizontal-------------------------------------------------------------
            winCount = 1
            left = -1
            right = 1
            while True:
                if left == 0 and right == 0:
                    break
                if left != 0:
                    if space+left < 0:
                        left = 0
                    elif board[count][space+left].value == board[count][space].value:
                        left -= 1
                        winCount += 1
                    else:
                        left = 0
                if right != 0:
                    if space+right >= len(board[count])-1:
                        right = 0
                    elif board[count][space+right].value == board[count][space].value:
                        winCount += 1
                        right += 1
                    else:
                        right = 0
            if winCount == 4:
                win = True
                return win
            #--------------------------------------------------------------------------------
            #Check Vertical------------------------------------------------------------------
            winCount = 1
            top = -1
            bottom = 1
            while True:
                #Checks to see if any operations can be continued.
                if top == 0 and bottom == 0:
                    break
                #Handles viewing above the given element
                if top != 0:
                    if count+top < 0:
                        top = 0
                    elif board[count+top][space].value == board[count][space].value:
                        winCount += 1
                        top-=1
                    else:
                        top = 0
                #Handle viewing below the given element
                if bottom != 0:
                    if count+bottom >= len(board[count])-1:#Not equal
                        bottom = 0
                    elif board[count+bottom][space].value == board[count][space].value:
                        winCount += 1
                        bottom += 1
                    else:
                        bottom = 0
            if winCount >= 4:
                win = True
                return win
            #--------------------------------------------------------------------------------
            #Checks diagonal-----------------------------------------------------------------
            winCount = 1
            #Array variables are indicative of x and y axis values to add.
            upRight = [1, -1]
            upLeft = [-1, -1]
            downRight = [1, 1]
            downLeft = [-1, 1]
            #Default value on which to fall back to
            tempVal = [0, 0]
            while True:
                #If all elements are checked then break from loop
                if upRight == tempVal and upLeft == tempVal and downRight == tempVal and downLeft == tempVal:
                    break
                #Checks up right
                if upRight != tempVal:
                    if upRight[0]+space > len(board[count])-1 or upRight[0]+count < 0:
                        upRight = tempVal[:]
                    elif board[count+upRight[1]][space+upRight[0]].value == board[count][space].value:
                        winCount += 1
                        upRight[0] += 1
                        upRight[1] -= 1
                    else:
                        upRight = tempVal[:]
                #Checks up left
                if upLeft != tempVal:
                    if upLeft[0]+space < 0 or upLeft[0]+count < 0:
                        upLeft = tempVal[:]
                    elif board[count + upLeft[1]][space + upLeft[0]].value == board[count][space].value:
                        winCount += 1
                        upLeft[0] -= 1
                        upLeft[1] -= 1
                    else:
                        upLeft = tempVal[:]
                #Checks down right
                if downRight != tempVal:
                    if downRight[0]+space > len(board[count])-1 or downRight[0]+count > len(board)-1:
                        downRight = tempVal[:]
                    elif board[count + downRight[1]][space + downRight[0]].value == board[count][space].value:
                        winCount += 1
                        downRight[0] += 1
                        downRight[1] += 1
                    else:
                        downRight = tempVal[:]
                #Checks down left
                if downLeft != tempVal:
                    if downLeft[0]+space < 0 or downLeft[1]+count > len(board)-1:
                        downLeft = tempVal[:]
                    elif board[count+downLeft[1]][space+downLeft[0]].value == board[count][space].value:
                        winCount += 1
                        downLeft[0] -= 1
                        downLeft[1] += 1
                    else:
                        downLeft = tempVal[:]
            if winCount >= 4:
                win = True
                return win
            #--------------------------------------------------------------------------------
            #Returns win which is false if no other options.
            return win




def main():
    #Draw the gameboard and hide turtle
    turtle.speed(0)
    turtle.hideturtle()
    #Variable for the board(An array of bubble objects
    playVar = drawBoard(7,6)
    #Variable to indicate players turn
    playerTurn = 1

    #Print instructions
    print("Welcome to match 4!  The legally safe knockoff of another game...")
    print("The rules are simple.  As the player is prompted merely give a number 0-6.")
    print("When a player gets four in a row(Horizontally, Vertically, or Diagonal) that player wins and the game exits.")





    #Main loop for gameplay
    while True:
        #Player one turn
        if playerTurn == 1:
            spaceVal = (input("Player 1(Red) Enter Row Num:"))
            if spaceVal.isdigit():
                spaceVal = int(spaceVal)
                if spaceVal > len(playVar[0]) or playVar[0][spaceVal].value != 0:
                    print("Enter Again")
                else:
                    checkSpace(playVar, spaceVal, 1)
                    if checkWin(spaceVal, playVar):
                        print("Congratulations player 1.")
                        break
                    playerTurn = 2
            else:
                print("Enter Again")

        #Player two turn
        elif playerTurn == 2:
            spaceVal = (input("Player 2(Blue) Enter Row Num:"))
            if spaceVal.isdigit():
                spaceVal = int(spaceVal)
                if spaceVal > len(playVar[0])or playVar[0][spaceVal].value != 0:
                    print("Enter Again")
                else:
                    checkSpace(playVar, spaceVal, 2)
                    if checkWin(spaceVal,playVar):
                        print("Congratulations player 2.")
                        break
                    playerTurn = 1
            else:
                print("Enter Again")
    turtle.done()

main()