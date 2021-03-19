# tree structure class for piece evaluation
# Haley Granger
# Senior Project 2021

class MoveNode(object):
    def __init__(self,move,children,parent):
        self.move = move
        self.children = children
        self.parent = parent
        # value of the move calculated in the MoveValue class
        moveValue = None
        depth = 1

    def createMoveTree(self):
        moveTree = []
        for move in


