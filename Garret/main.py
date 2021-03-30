from Board import Board
from RandomAI import RandomAI
import random

test = "WAKNRPRQKKKPLNLAKIRIRIRIKIKILILIL32iLiLiLiKiKiRiRiRaKnLpLqKkKpRnRaK"
b = Board(test)
a = RandomAI(b, 1)
c = RandomAI(b, 0)

while b.state == 2:
    b.show_board()
    x = int(input("0 for exit\n1 for move\n2 for attack\n3 for end turn: "))
    if x == 0:
        break
    else:
        if x == 1:
            y = input("piece to: ")
            b.move([int(y[0]), int(y[1])], [int(y[2]), int(y[3])])
        elif x == 2:
            y = input("piece to: ")
            print(b.attack([int(y[0]), int(y[1])], [int(y[2]), int(y[3])]))
        elif x == 3:
            # c.ai_move()
            b.end_turn()
            a.ai_move()
        elif x == 4:
            print(b.get_board())
b.show_board()
print(b.state)
