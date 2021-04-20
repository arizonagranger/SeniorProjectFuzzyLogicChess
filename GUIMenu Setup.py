# This is just to setup the menu to be added in to the main GUI files later
# Note, in the main function, make sure to add mainMenu() under the def main():

import pygame as p

#Menu function: what we're gonna use to navigate the games, rules, and credits
def mainMenu():
    loadImages()
    menu = True

    while menu:
        for event in p.event.get():
            p.quit()
            quit()

        screen.fill(p.Color("white"))

        #Images needed to be loaded in for the main menu
        # Im1 = p.image.load
        #position the images on the screen
        #screen.blit(i1

        #Text for the main menu
        largeText = p.font.SysFont("Calibri")
        TextSurf, TextRect = text_obj("4D Chess AI", largeText)
        TextRect.center = (int(WIDTH /2), int(HEIGHT /2+30))
        screen.blit(TextSurf, TextRect)

        #Buttons to use
        button("Play", new_game) #Needs positioning and color of the button
        button("Credits", ) #Positioning, color, we also need a credit screen
        button("Rules", ) #Positioning, color, rules screen

        clock.tick(MAX_FPS)
        p.display.flip()


#Displays what the rules engine is setup to do in text
def ruleScreen():
    rules = True

    while rules:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                quit()

    screen.fill(p.Color("white"))
    largeText = p.font.SysFont("Calibri")

    TextSurf, TextRect = text_obj("Rules", largeText)
    TextRect.center = () #positioning


    p.display.flip()


#Displays everyone involved and if we want to we can add our pictures
def creditScreen():
    credit = True

    while credit:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                quit()


    screen.fill(p.Color("white"))
