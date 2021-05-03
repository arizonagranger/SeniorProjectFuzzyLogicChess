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
    smallText = p.font.SysFont("Calibri", 14)

    TextSurf, TextRect = text_objects("Rules", largeText)
    TextRect.center = (int(WIDTH / 2), int(HEIGHT / 2 + 30))


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
    TextRect.center = (int(WIDTH / 2), 150)
    SCREEN.blit(TextSurf, TextRect)

    TextSurf, TextRect = text_objects("Garret Depew", nameText)
    TextRect.center = (int(WIDTH / 2), 170)
    SCREEN.blit(TextSurf, TextRect)

    TextSurf, TextRect = text_objects("Alexandar Eubanks", nameText)
    TextRect.center = (int(WIDTH / 2), 200)
    SCREEN.blit(TextSurf, TextRect)

    TextSurf, TextRect = text_objects("Jacob Walton", nameText)
    TextRect.center = (int(WIDTH / 2), 250)
    SCREEN.blit(TextSurf, TextRect)

    TextSurf, TextRect = text_objects("Kiah Jefferies", nameText)
    TextRect.center = (int(WIDTH / 2), 270)
    SCREEN.blit(TextSurf, TextRect)