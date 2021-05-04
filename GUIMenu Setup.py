# This is just to setup the menu to be added in to the main GUI files later
# Note, in the main function, make sure to add mainMenu() under the def main():

import pygame as p

from Garret.GUI import Button
from Garret.GUI import HEIGHT
from Garret.GUI import SCREEN
from Garret.GUI import WIDTH
from Garret.GUI import load_images
from Garret.GUI import start_game
from Garret.GUI import text_objects
from Garret.Board import Board


def main():
    mainMenu()

# Menu function: what we're gonna use to navigate the games, rules, and credits
def mainMenu():
    load_images()
    menu = True

    while menu:
        for event in p.event.get():
            p.quit()
            quit()

        SCREEN.fill(p.Color("white"))

        # Images needed to be loaded in for the main menu
        # Im1 = p.image.load
        # position the images on the screen
        # screen.blit(i1

        # Text for the main menu
        largeText = p.font.SysFont("Calibri", 30)
        TextSurf, TextRect = text_objects("Medieval Fuzzy Logic Chess 4C", largeText)
        TextRect.center = (int(WIDTH /2), int(HEIGHT /2+30))
        SCREEN.blit(TextSurf, TextRect)

        # Buttons to use
        Button("Play", int(WIDTH/2 -250), 450, 100, 50, p.Color(180, 180, 180), p.Color(100, 100, 100), start_game())
        Button("Credits", int(WIDTH/2 -50), 450, 100, 50, p.Color(180, 180, 180), p.Color(100, 100, 100), creditScreen())
        Button("Rules", int(WIDTH/2 +150), 450, 100, 50, p.Color(180, 180, 180), p.Color(100, 100, 100), ruleScreen())

        # clock.tick(MAX_FPS)
        p.display.flip()


# Displays what the rules engine is setup to do in text
def ruleScreen():
    rules = True

    while rules:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                quit()

    SCREEN.fill(p.Color("white"))
    largeText = p.font.SysFont("Calibri", 30)
    meduiumText = p.font.SysFont("Calibri", 15)
    smallText = p.font.SysFont("Calibri", 12)

    TextSurf, TextRect = text_objects("Rules", largeText)
    TextRect.center = (int(WIDTH / 2), int(HEIGHT / 2 + 30))

    TextSurf, TextRect = text_objects("The armies of chess pieces for command are divided into three corp:",
                                      meduiumText)
    TextRect.center = (int(WIDTH / 2), 100)

    TextSurf, TextRect = text_objects("The King and Bishops are corp commanders, each with one command "
                                      "authority that can be used in each turn.", smallText)
    TextRect.center = (int(WIDTH / 2), 115)

    TextSurf, TextRect = text_objects("Up to three actions may be taken in each turn, one by each corp. "
                                      "Corp command actions ARE NOT required in any turn, so zero to "
                                      "three actions may be taken in a turn.", smallText)
    TextRect.center = (int(WIDTH / 2), 130)

    TextSurf, TextRect = text_objects("Command authority may not be transferred from one commander to another.",
                                      smallText)
    TextRect.center = (int(WIDTH / 2), 150)

    TextSurf, TextRect = text_objects("The left side Bishop commands the three left pawns and the left-side Knight.",
                                      smallText)
    TextRect.center = (int(WIDTH / 2), 170)

    TextSurf, TextRect = text_objects("The right side Bishop commands the three right pawns and the right-side Knight.",
                                      smallText)
    TextRect.center = (int(WIDTH / 2), 190)

    TextSurf, TextRect = text_objects("The King commands the Queen, the two rooks (archers), and the "
                                      "remaining two center pawns", smallText)
    TextRect.center = (int(WIDTH / 2), 210)

    TextSurf, TextRect = text_objects("The King may delegate any of its pieces to be commanded by either "
                                      "Bishop, at any time.", smallText)
    TextRect.center = (int(WIDTH / 2), 230)

    TextSurf, TextRect = text_objects("Each commander (King and Bishops) may command one action (move or capture) "
                                      "per turn,only for their commanded pieces.", smallText)
    TextRect.center = (int(WIDTH / 2), 250)

    TextSurf, TextRect = text_objects("When a Bishop is captured, "
                                      "his commanded pieces revert to the command of the King, but his command "
                                      "authority is lost (the army may make one fewer action per turn, "
                                      "a serious disadvantage)", smallText)
    TextRect.center = (int(WIDTH / 2), 270)

    TextSurf, TextRect = text_objects("The game ends when the King is captured "
                                      "(the Bishops do not fight on without the King, but surrender)", smallText)
    TextRect.center = (int(WIDTH / 2), 290)

    p.display.flip()


# Displays everyone involved and if we want to we can add our pictures
def creditScreen():
    credit = True

    while credit:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                quit()


    SCREEN.fill(p.Color("white"))
    largeText = p.font.SysFont("Calibri", 30)
    nameText = p.font.SysFont("Calibri", 14)

    TextSurf, TextRect = text_objects("Credits", largeText)
    TextRect.center = (int(WIDTH / 2), int(HEIGHT / 2 + 30))

    TextSurf, TextRect = text_objects("Haley Granger", nameText)
    TextRect.center = (int(WIDTH / 2), 100)
    SCREEN.blit(TextSurf, TextRect)

    TextSurf, TextRect = text_objects("Garret Depew", nameText)
    TextRect.center = (int(WIDTH / 2), 130)
    SCREEN.blit(TextSurf, TextRect)

    TextSurf, TextRect = text_objects("Alexandar Eubanks", nameText)
    TextRect.center = (int(WIDTH / 2), 170)
    SCREEN.blit(TextSurf, TextRect)

    TextSurf, TextRect = text_objects("Jacob Walton", nameText)
    TextRect.center = (int(WIDTH / 2), 210)
    SCREEN.blit(TextSurf, TextRect)

    TextSurf, TextRect = text_objects("Kiah Jefferies", nameText)
    TextRect.center = (int(WIDTH / 2), 240)
    SCREEN.blit(TextSurf, TextRect)