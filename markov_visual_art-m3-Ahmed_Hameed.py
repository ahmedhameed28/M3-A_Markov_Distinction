"""
Markov Text Visual Art Generator
Author: Ahmed Hameed
Version Date: 5/15/2021

Course: Computational Creativity (CSCI 3725)
Instructor: Sarah Harmon
Assignment: Mission 3 - A Markov Distinction

Description: A program that reads in input text, populates frequency table of previous character occurrences in input 
text (only looking at 1 previous character), creates new text based off of the previous occurrence counts, and
then finally, generate unique visual output for each character in the newly produced text using a mapping of 
common characters to visual elements.

Dependencies: os, unidecode, random, turtle
"""

import os
import unidecode as ud
import random as rand
from turtle import *

WINDOW_WIDTH = 1210  # the approximate width of the coordinate plane when using turtle
WINDOW_HEIGHT = 580  # the approximate height of the coordiante plane when using turtle

# approximate length of x-axis based on the width of the drawing window
X_AXIS = WINDOW_WIDTH/2
# approximate length of y-axis based on the height of the drawing window
Y_AXIS = WINDOW_HEIGHT/2

class MarkovTextArt:

    # Mapping of alphabet characters to RGB values of colors. RGB values are uniformly distributed
    # across the color spectrum using RGB color table from:
    # https://www.rapidtables.com/web/color/RGB_Color.html
    CHARS_TO_COLORS = {
        "a": (128, 0, 0), "A": (178, 34, 34), "b": (255, 0, 0), "B": (205, 92, 92),
        "c": (233, 150, 122), "C": (255, 69, 0), "d": (255, 165, 0), "D": (218, 165, 32), "e": (189, 183, 107), "E": (255, 255, 0),
        "f": (85, 107, 47), "F": (127, 255, 0), "g": (0, 100, 0), "G": (0, 255, 0), "h": (144, 238, 144), "H": (0, 250, 154),
        "i": (46, 139, 87), "I": (32, 178, 170), "j": (0, 128, 128), "J": (0, 255, 255), "k": (0, 206, 209), "K": (175, 238, 238),
        "l": (176, 224, 230), "L": (100, 149, 237), "m": (30, 144, 255), "M": (135, 206, 250), "n": (0, 0, 128), "N": (0, 0, 255),
        "o": (138, 43, 226), "O": (106, 90, 205), "p": (147, 112, 219), "P": (153, 50, 204), "q": (128, 0, 128), "Q": (238, 130, 238),
        "r": (218, 112, 214), "R": (255, 20, 147), "s": (255, 182, 193), "S": (139, 69, 19), "t": (255, 235, 205), "T": (222, 184, 135),
        "u": (250, 250, 210), "U": (255, 228, 225), "v": (244, 164, 96), "V": (255, 245, 238), "w": (255, 222, 173), "W": (230, 230, 250),
        "x": (253, 245, 230), "X": (255, 255, 240), "y": (119, 136, 153), "Y": (105, 105, 105), "z": (248, 248, 255), "Z": (220, 220, 220)
    }


    def __init__(self, frequency_table={}, transition_matrix={}):
        """
        Constructs a new MarkovTextArt object with a frequency table and transition_matrix.
            Args:
                frequency_table (dict) - A dictionary that tracks that tracks 1 previous character occurences 
                based off of the current character. A key is the current character and a value is a
                dictionary of previous characters and their number occurrences
                transition_matrix (dict) - A transition probabilites matrix based off of character 
                occurrences in frequency table
        """
        self.frequency_table = frequency_table
        # NOTE: transition matrix is NOT currently being used by program but could be useful later on.
        self.transition_matrix = transition_matrix
        self.input_text = ''


    def read_string(self, words):
        """
        Function that takes a string 'words' and reads through each character while updating the
        frequency table (global variable).
            Args: words (str) - A string containing the text that will be processed.
            Return: None
        """

        # for every character in words that has a previous character (so starting at index 1)
        for i in range(1, len(words)):
            current_char = words[i]
            prev_char = words[i-1]

            # if character is in the frequency_table then just update the prev char occurrence
            if current_char in self.frequency_table.keys():
                prev_chars_dict = self.frequency_table.get(current_char)

                # if the previous character already exists in the dictionary then update frequency by 1
                if prev_char in prev_chars_dict.keys():
                    self.frequency_table[current_char][prev_char] = prev_chars_dict[prev_char] + 1
                # otherwise, create a new entry for the previous character
                else:
                    self.frequency_table[current_char][prev_char] = 1

            # otherwise, create a new entry in the dictionary for the character
            else:
                self.frequency_table[current_char] = {prev_char: 1}

        return words[-1]


    def read_from_file(self, filename):
        """
        Given a filename, reads the entire contents of that file at once and then calls a 
        a method that populates the frequency table.
            Args: filename (str) - The name of the .txt file to be processed. 
            Return: None
        """
        with open(filename, 'r', encoding='utf-8') as text_file:
            # read entire file as a string and stores in the input_text class variable
            self.input_text = text_file.read()
            self.read_string(self.input_text)


    def sum_char_occurences(self, char_dict):
        """
        Given a dictionary of characters and their occurrences, sums all of the occurrences and return
        the total.
            Args: char_dict (dict) - A dictionary of ASCII characters (keys) and their counts (values)
            Return: char_total (int) - The sum of all the character occurrences in char_dict
        """
        char_total = 0

        # iterating over every character count in char_dict
        for val in char_dict.values():
            char_total += val

        return char_total


    def populate_transition_matrix(self):
        """
        Populates transition probabilites matrix based off of the frequency table.
        Sums up all the previous character occurrences for a given character and turns them
        into probabilities: frequency/sum of previous character occurrences = probability. 
            Args: None.
            Return: None.
        NOTE: This function isn't actually used by the program unfortunately. I wrote it but
            ended up not needing it since random.choices() takes in a 'weights' argument.
            Could still be useful in future version of the program.
        """

        # iterate over every character key in frequency table
        for key in self.frequency_table.keys():

            prev_char_dict = self.frequency_table.get(key)
            total_sum = self.sum_char_occurences(prev_char_dict)
            self.transition_matrix[key] = {}

            # iterate over every previous character occurrence for current character key
            for prev_char, count in prev_char_dict.items():
                trans_prob = round(count/total_sum, 3)
                self.transition_matrix[key].update({prev_char: trans_prob})


    def get_next_char(self, current_char):
        """
        Given a character key, uses the frequency table of previous characters associated with that 
        character to generate the next character.
            Args: current_char (str) - The character key which will be used to access the character counts
                                        in the frequency table.
            Return: next_char (str) - The next character, generated from the transition probabilities 
                                        created by random.choices() 
        """
        prev_chars_dict = self.frequency_table.get(current_char)
        all_chars = list(prev_chars_dict.keys())
        char_counts = list(prev_chars_dict.values())

        next_char = ''.join(rand.choices(list(all_chars), weights=char_counts, k=1))
        return next_char


    def generate_markov_text(self, num_chars):
        """
        Uses a 1-order Markov chain (a matrix of characters and transition probabilites) to generate new
        text based off the previous character occurrences. A 1-order Markov chain only looks at the previous 
        state. Creates new text of size num_chars, and the new text continues after the last character 
        in start_string
        Example: "This is a test string!!!!!!!!" --> At character '!': There's a 87.5% chance of the next
                character being another '!' and a 12.5% of it being 'g'.
            Args:
                num_chars (int) - The number of characters to be generated by the function
            Return:
                markov_text (str) - The new text generated by the 1-order Markov Chain and transition matrix
        """
        # pick a random start character from the known characters in frequency table
        start_string = rand.choice(list(self.frequency_table.keys()))  
        markov_text = ""

        current_char = start_string
        for i in range(num_chars):
            next_char = self.get_next_char(current_char)
            markov_text += next_char
            current_char = next_char

        return markov_text


    def export_text(self, text, output_filename):
        """
        Given a string of text, writes the contents of text to output_filename. In this program, the text
        will be generated from a first order Markov chain.
            Args:
                text (str) - Any string of text.
                output_filename (str) - The output file path that the text will be written to.
        """
        with open(output_filename, 'w', encoding='utf-8') as output:
            output.write(text)


    def draw_one_char(self, current_char, turtle_dude, initial_pen_state, start_coords, step_x, step_y, font_size):
        """
        Helper function for generate_markov_art() that uses the turtle object to create visual output for 
        just one character.
            Args:
                current_char (str) - The current character that is being drawn
                turtle_dude (Turtle object) - The Turtle object that is drawing everything
                initial_pen_state (dict) - A dictionary containing the initial attributes of the Turtle pen
                                            before any drawing is done
                start_coords (tuple) - A tuple containing the starting coordinates (x,y) of the Turtle object
                step_x (int) - How much the x coordinate of the Turtle object changes after every character drawn
                step_y (int) - How much the y coordinate of the Turtle object changes after every new line
                font_size (int) - Determines the size of the circles being drawn for letters
            Return: None
        """
        # current state of turtle dude before any drawing
        t_pos = turtle_dude.pos()
        pen_size = turtle_dude.pensize()
        turtle_size = turtle_dude.shapesize()
        
        # set turtle facing East and put the pen down so drawing can be done
        turtle_dude.setheading(0)
        turtle_dude.pendown()

        # remove accents and diacritics from character
        # Source: https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string
        current_char = ud.unidecode(current_char)

        # if the character is a letter then draw a circle with a color unique to that letter
        if current_char.isalpha():
            color_RGB = self.CHARS_TO_COLORS.get(current_char)
            turtle_dude.color(color_RGB)
            turtle_dude.circle(font_size)
        # simulates the use of a space in writing, nothing is drawn and turtle simply
        # moves step_size distance to the right
        elif current_char == " ":
            turtle_dude.penup()
        # a period marks the end of the current sentences and the start of a new sentence so a dot is drawn
        # and the drawing pen is reset to its initial values
        elif current_char == ".":
            turtle_dude.dot(font_size-3)
            turtle_dude.pen(initial_pen_state)
        # a comma here marks a pause in the sentence and connection between the previous words in the sentence
        # so we move the turtle forward without lifting the pen
        elif current_char == ",":
            turtle_dude.forward(step_x)
        # attempting to simulate an italics effect after the quotation marks, will likely need to separate
        # apostrophe from a quotation mark in the future
        elif current_char == ("\'" or "\""):
            turtle_dude.pen(tilt=15, stretchfactor=(0.8, 0.2))
        # question mark is signified by a triangle and since question marks also serve to end a sentence
        # the drawing pen is reset to its initial values
        elif current_char == "?":
            turtle_dude.turtlesize(0.5, 0.5, 0.5)
            turtle_dude.shape("triangle")
            turtle_dude.setheading(90)
            turtle_dude.stamp()
            turtle_dude.setpos(t_pos) # moving turtle back to its position before drawing
            turtle_dude.turtlesize(*turtle_size)
            turtle_dude.pen(initial_pen_state)
        # exclamation point is signified by an arrow pointing down and exclamation points also serve to
        # end a sentence, the drawing pen is reset to its initial values
        elif current_char == "!":
            turtle_dude.turtlesize(0.5, 0.5, 0.5)
            turtle_dude.setheading(270)
            turtle_dude.shape("arrow")
            turtle_dude.stamp()
            turtle_dude.setpos(t_pos)
            turtle_dude.turtlesize(*turtle_size)
            turtle_dude.pen(initial_pen_state)
        # colon or semicolons are often used to emphasize a clause in a sentence or connect a related clause
        # to the previous clause in a sentence so a 'bold' effect is applied to the drawings
        elif current_char == (":" or ";"):
            turtle_dude.pen(pensize=pen_size+3)
        # dashes are also used to connect words, clauses, and for emphasis so a small 'bold'
        # effect is applied here as well
        elif current_char == "-":
            turtle_dude.pen(tilt=30.0, pensize=pen_size+1)
        # it's a new line so the turtle is moved down and the pen is reset
        elif current_char == "\n":
            turtle_dude.penup()
            turtle_dude.setpos(start_coords[0], t_pos[1] - step_y)
            #turtle_dude.pen(initial_pen_state)
        # a bit random but a number produces a stretching effect in the drawing based on what the digit is
        elif current_char.isdigit():
            num = int(current_char)
            turtle_dude.pen(stretchfactor=(3*num, num))

        # turtle has finished producing a visual for the current character so the pen is lifted and 
        # turtle heading is reset so that it faces East again
        turtle_dude.penup()
        turtle_dude.setheading(0) 
        # drawing of the current character is complete so turtle moves forward
        turtle_dude.forward(step_x)

        current_pos = turtle_dude.pos() 
        # if the turtle is at the bottom of the screen, reset position to top-left
        if current_pos[1] < -Y_AXIS:
            turtle_dude.setpos(start_coords)
        # if turtle is at the far right of the screen, move turtle down and to the left
        elif current_pos[0] > X_AXIS:
            turtle_dude.setpos(-X_AXIS, current_pos[1] - step_y)


    def generate_art(self, turtle_dude, markov_text, step_x=10, step_y=15, font_size=13):
        """
        Reads through each character of markov_text and generates art based off of each character.
        Each letter in the text is represented by a circle with a unique color.
        Art is generated using the Turtle module.
            Args:
                turtle_dude (Turtle object) - The Turtle object that will be used to draw the image
                markov_text (str) - A string containing the text produced by the markov chain
                step_size (int) - The amount of space between each line of drawings: affects how much the
                                 x and y coordinates of the turtle change after every character. Default = 10
                font_size (int) - The size of the circles that are drawn. Default = 13
            Return: None
        """
        # want turtle to start drawing at the top left of the screen, similar to how
        # English is written top, down, from left to right
        start_coords = (-X_AXIS, Y_AXIS)
        turtle_dude.penup()
        turtle_dude.setpos(start_coords)

        # setting the speed to 0 and hiding the turtle so that it draws more quickly
        turtle_dude.speed(0)
        turtle_dude.hideturtle()
        # pen attributes might change after drawing operations so we want to store the initial state of the pen
        initial_pen_state = turtle_dude.pen()

        # create unique visual output for every character in markov_text
        for char in markov_text:
            self.draw_one_char(char, turtle_dude, initial_pen_state,
                               start_coords, step_x, step_y, font_size)



def main():
    """
    main() function used to create a MarkovTextArt object, read and process the text from an input .txt file
    to create first order Markov chain, and lastly, generate visuals based on the text produced by the Markov chain.
    """

    # set parameters of the visual art here!
    step_x = 16 # distance between each circle drawn
    step_y = 28 # distance between each row of circles
    font_size = 10 # the radius of the circles drawn
    pen_size = 1 # the thickness of the lines in the drawing
    # number of characters that will be generated using 1-order Markov chain and then drawn using 
    num_chars = 1200  
    background_color = 'black' # color of drawing screen, black looks best considering the range of colors

    # SET INPUT FILENAME HERE! Format: text_input/[filename.txt]. 
    # NOTE: If using VS Code and you have the folder opened then find the desired input file in the "EXPLORER" window,
    # right click on it, and select "Copy Relative Path" then paste into input_file below.
    # Make sure to change all '\' to '/'
    input_file = "text_input/random_text_ABC.txt"
    visual_name = input_file.strip('.txt').lstrip("text_input/") # getting rid of the '.txt' and 'text_input/'
    # filename of the generated 1-order Markov Chain text
    new_markov_text_output_file = "text_output/markov_" + visual_name + ".txt"

    # preparing the turtle for drawing
    andrey = Turtle() # name is based off of Andrey Andreyevich Markov, the original developer of Markov chains
    andrey.pensize(pen_size)
    t_screen = Screen()
    t_screen.bgcolor(background_color)
    t_screen.colormode(255) # allows turtle to accept RGB color values from 0-255
    
    # NOTE: IF YOU WANT TO SEE THE TURTLE DRAW: increase the value of the argument in tracer()
    t_screen.tracer(0) # 0 turns off screen updates so that the drawing occurs more quickly

    print ("\nCurrent visual:", visual_name)
    print()

    current_artist = MarkovTextArt()
    current_artist.read_from_file(input_file)
    new_text = current_artist.generate_markov_text(num_chars)
    # saving Markov chain generated text to a .txt file in 'text_output'
    current_artist.export_text(new_text, new_markov_text_output_file)  
    # generating the actual drawing 
    current_artist.generate_art(andrey, new_text, step_x, step_y, font_size)
    
    t_screen.update()  # updates the screen after the turtle is done drawing
    t_screen.mainloop() # keeps the screen open
    # NOTE: All .png files in output were gathered by taking a screenshot of this screen 


if __name__ == "__main__":
    main()
