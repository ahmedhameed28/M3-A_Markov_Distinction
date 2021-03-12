"""
A program that reads in text, computes transition probabilities based off the input text, creates new text based
off those probabilites using a Markov chain, then creates visual art based off the newly produced text.

Outline:
    * Read in text and process the text:
        * Function that reads in a text file, line by line and parsing the text and updating the
            frequency table as it encounters characters (could implement this function so that it reads
            the text backwards from end to beginning since Markov chains rely on what occurred BEFORE hand)
        * Function that takes in a string and updates frequency table (to be used in conjugtion with above)
        
        * Function that takes in user input from the terminal and fills up the frequency table??
            **** Functionality that allows users to directly interact with creative system via terminal
              rather than text files ****
        
    
    * Populate transition probabilities matrix based on the frequency table
        * Function that sums up all the previous character occurrences for a given character and turns them
            into probabilities: frequency/total_sum = probability. Transition matrix will also be a dict
    
    * Create new text using transition probabilites matrix
        * Function that generates 1 new character based off of transition matrix
        * Function that takes in a int for the length of the new text and generates new text of that length
            based on the transition matrix (works in conjuction with function above)
    
    THIS PART WILL LIKELY BE THE MOST DIFFICULT!
    * Read through new text and create unique visual output for each character 
        * Requirements: Visual output must somehow be unique to the text that it is produced from.
                        Example: visual output generated from Arctic Monkeys EP must be different from
                                visual output generated from a Shakespeare play or an instruction manual
        * Need a mapping of ASCII characters to visual elements, from text to art
            Possible Ideas: 
                - Map ASCII characters and their positions to RGB values on the color spectrum
                    (uniform distribution?) 
                - Every space changes color or changes the line or shape being drawn or Turtle position
                - Every period changes color or shape or line or drawing angle or Turtle position
                - Every comma, apostrophe, underscore, etc. does something
                - Assign unique features to punctuation.
                --> Punctuation is what makes the text unique? Spacing? What is it that makes language "unique"?
        * Function that encodes all of the visual rules discussed above and reads through the text and
            creates the art using Turtle! Save the art onto a .png file. Profit!

    * Try different types of text input and see what gets produced by the system.
"""

import numpy as np
import random as rand
import turtle
from PIL import Image

WINDOW_WIDTH = 1260 # the approximate width of the coordinate plane when using turtle
WINDOW_HEIGHT = 660 # the approximate height of the coordiante plane when using turtle

X_AXIS = WINDOW_WIDTH/2 # approximate length of x-axis based on the width of the drawing window
Y_AXIS = WINDOW_HEIGHT/2 # approximate length of y-axis based on the height of the drawing window

class MarkovTextArt:
    """

    """
    # Mapping of alphabetic characters to RGB values of colors. RGB values are uniformly distributed 
    # across the color spectrum using RGB color table from: 
    # https://www.rapidtables.com/web/color/RGB_Color.html#:~:text=RGB%20color%20space%20or%20RGB,*256%3D16777216%20possible%20colors.

    CHARS_TO_COLORS = {
    "a":(128,0,0), "A":(178,34,34), "b":(255,0,0), "B":(205,92,92), 
    "c":(233,150,122), "C":(255,69,0), "d":(255,165,0), "D":(218,165,32), "e":(189,183,107), "E":(255,255,0), 
    "f":(85,107,47), "F":(127,255,0),"g":(0,100,0), "G":(0,255,0), "h":(144,238,144), "H":(0,250,154), 
    "i":(46,139,87), "I":(32,178,170), "j":(0,128,128), "J":(0,255,255), "k":(0,206,209), "K":(175,238,238), 
    "l":(176,224,230), "L":(100,149,237), "m":(30,144,255), "M":(135,206,250), "n":(0,0,128), "N":(0,0,255), 
    "o":(138,43,226), "O":(106,90,205), "p":(147,112,219), "P":(153,50,204), "q":(128,0,128), "Q":(238,130,238), 
    "r":(218,112,214), "R":(255,20,147), "s":(255,182,193), "S":(139,69,19), "t":(255,235,205),"T":(222,184,135), 
    "u":(250,250,210),"U":(255,228,225), "v":(244,164,96), "V":(255,245,238), "w":(255,222,173), "W":(230,230,250), 
    "x":(253,245,230), "X":(255,255,240),"y":(119,136,153), "Y":(105,105,105), "z":(248,248,255), "Z":(220,220,220)
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
    

    def read_string(self, words):
        """
        Function that takes a string, words, and reads through each character while updating the
        frequency table.
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
        Given a filename, reads the contents of that file and populates the frequency table, line by line.
            Args: filename (str) - The name of the .txt file to be processed. 
            Return: None
        """
        text_file = open(filename, 'r')

        # read entire file as a string and send to read_string()
        text_str = text_file.read()
        self.read_string(text_str)
        
        text_file.close()


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


    def generate_markov_text(self, num_chars, start_string):
        """
        Uses a 1-order Markov chain (a matrix of characters and transition probabilites) to generate new
        text based off the previous character occurrences. A 1-order Markov chain only looks at the previous 
        state. Creates new text of size num_chars, and the new text continues after the last character 
        in start_string
        Example: "This is a test string!!!!!!!!" --> At character '!': There's a 87.5% chance of the next
                character being another '!' and a 12.5% of it being 'g'.
            Args:
                num_chars (int) - The number of characters to be generated by the function
                start_string (str) - The start of the new text, last character will be used to generate the new text. 
            Return:
                markov_text (str) - The new text generated by the 1-order Markov Chain and transition matrix
        """

        markov_text = ""

        current_char = start_string[-1]
        for i in range(num_chars):
            next_char = (self.get_next_char(current_char))
            markov_text += next_char
            current_char = next_char
        
        return markov_text

            
    def draw_one_char(self, current_char, turtle_dude, initial_pen_state, start_coords, step_size, font_size):
        """
        Helper function for generate_markov_art() that uses the turtle object to create visual output for 
        just one character.
            Args:
                current_char (str) - The current character that is being drawn
                turtle_dude (Turtle object) - The Turtle object that is drawing everything
                initial_pen_state (dict) - A dictionary containing the initial attributes of the Turtle pen
                                            before any drawing is done
                start_coords (tuple) - A tuple containing the starting coordinates (x,y) of the Turtle object
                step_size (int) - How much the x and y coordinates of the Turtle object change after every
                                    drawing.
                font_size (int) - Determines the size of the circles being drawn for letters
            Return: None
        """

        # current (x,y) position of turtle dude before any drawing 
        t_pos = turtle_dude.pos()
        pen_size = turtle_dude.pensize()
        turtle_size = turtle_dude.shapesize()
        turtle_dude.setheading(0)
        turtle_dude.pendown()
        
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
            turtle_dude.dot(font_size)
            turtle_dude.pen(initial_pen_state)
        # a comma here marks a pause in the sentence and connection between the previous words in the sentence
        # so we move the turtle forward without lifting the pen
        elif current_char == ",":
            turtle_dude.forward(step_size)
        # attempting to simulate an italics effect after the quotation marks, will likely need to separate
        # apostrophe from a quotation mark in the future
        elif current_char == ("\'" or "\""):
            turtle_dude.pen(tilt=15, stretchfactor=(0.8,0.1))
        # question mark is signified by a triangle and since question marks also serve to end a sentence
        # the drawing pen is reset to its initial values
        elif current_char == "?":
            turtle_dude.turtlesize(0.5,0.5,0.5)
            turtle_dude.setheading(90)
            turtle_dude.shape("triangle")
            turtle_dude.stamp()
            turtle_dude.turtlesize(*turtle_size)
            turtle_dude.pen(initial_pen_state)            
        # exclamation point is signified by an arrow pointing down and since question marks also serve to
        # end a sentence, the drawing pen pen is reset to its initial values
        elif current_char == "!":
            turtle_dude.turtlesize(0.5,0.5,0.5)
            turtle_dude.setheading(270)
            turtle_dude.shape("arrow")
            turtle_dude.stamp()
            turtle_dude.setpos(t_pos)
            turtle_dude.turtlesize(*turtle_size)
            turtle_dude.pen(initial_pen_state)
        # colon or semicolons are often used to emphasize a clause in a sentence or connect a related clause
        # to the previous clause in a sentence so a 'bold' effect is applied to the drawings
        elif current_char == (":" or ";"):
            turtle_dude.pen(pensize=pen_size+5)
        # dashes are also used to connect words, clauses, and for emphasis so a small 'bold' 
        # effect is applied here as well
        elif current_char == "-":
            turtle_dude.pen(tilt=30.0, pensize=pen_size+2)
        # it's a new line so the turtle is moved down and the pen is reset
        elif current_char == "\n":
            turtle_dude.penup()
            turtle_dude.setpos(start_coords[0], t_pos[1] - step_size)
            turtle_dude.pen(initial_pen_state)
        # a bit random but a number produces a stretching effect in the drawing based on what the digit is
        elif current_char.isdigit():
            num = int(current_char)
            turtle_dude.pen(stretchfactor=(3*num, num))

        # turtle has finished producing a visual for the current character so the pen is lifted
        turtle_dude.penup()

        turtle_dude.setheading(0) # resetting the turtle so that it faces East
        current_pos = turtle_dude.pos()

        # if the turtle is at the bottom of the screen, reset position to top-left
        if (current_pos[1] + step_size) < (-Y_AXIS):
            turtle_dude.setpos(start_coords)

        # if turtle is at the far right of the screen, move turtle down and to the left
        elif (current_pos[0] + step_size) > X_AXIS:
            turtle_dude.setpos(-X_AXIS, current_pos[1] - step_size)
            
        turtle_dude.forward(step_size+5)
        

    # self defined function to print coordinate 
    def buttonclick(something, x,y):  
        print("You clicked at this coordinate({0},{1})".format(x,y)) 


    def generate_markov_art(self, turtle_dude, markov_text, output_name, background_color="black", step_size=10, font_size=13):
        """
        Reads through each character of markov_text and generates art based off of each character.
        Each letter in the text is represented by a circle with a unique color.
        Art is generated using the Turtle module.
            Args:
                turtle_dude (Turtle object) - The Turtle object that will be used to draw the image
                markov_text (str) - A string containing the text produced by the markov chain
                background_color (str) - A string indicating the background color of the turtle drawing 
                                        such as 'white' or 'black'. Default = 'black' since that looks better
                                        considering the range of colors. 
                output_name (str) - The name of the output file that the drawing will be saved to
                step_size (int) - The amount of space between each line of drawings: affects how much the
                                 x and y coordinates of the turtle change after every character. Default = 10
                font_size (int) - The size of the circles that are drawn. Default = 13
            Return: None
        """

        t_screen = turtle_dude.getscreen()
        #t_screen.screensize(screen_width, screen_height)
        t_screen.bgcolor(background_color)
        t_screen.colormode(255) # allows turtle to accept RGB color values from 0-255
        t_screen.tracer(0) # turns off screen updates so that the drawing occurs more quickly

        # want turtle to start drawing at the top left of the screen, similar to how 
        # English is written top, down, from left to right
        start_coords = (-X_AXIS, Y_AXIS) 

        #print(start_coords)
        turtle_dude.penup()
        turtle_dude.setpos(start_coords)
        turtle_dude.speed(0)
        turtle_dude.hideturtle()
        initial_pen_state = turtle_dude.pen()

        for char in markov_text:
            self.draw_one_char(char, turtle_dude, initial_pen_state, start_coords, step_size, font_size)
        
        t_screen.update() # updates the screen after the turtle is done drawing

        # keep the screen open 
        t_screen.mainloop()

        #t_canvas = t_screen.getcanvas()
        #t_canvas.postscript(file=output_name+'.eps', width=1000, height=1000)
        #img_output = Image.open(output_name + '.eps')
        #img_output.save(output_name + '.jpg')

'''
        #onscreen function to send coordinate 
        turtle.home()
        turtle.onscreenclick(self.buttonclick,1)  
        t_screen.listen()  # listen to incoming connections 
        turtle.speed(10) # set the speed 
        turtle.done()    # hold the screen 
'''   

def main():
    """
    main() function used to create a MarkovTextArt object, read and process the text from an input .txt file
    to create first order Markov chain, and lastly, generate visuals based on the text produced by the Markov chain.
    """
    testing = MarkovTextArt()
    testing.read_from_file("arctic_monkeys_AM_album_song_lyrics.txt")

    print()
    num_chars = 2000
    start_string = "t"
    new_text = testing.generate_markov_text(num_chars, start_string)
    print(new_text)
    print()

    andrey = turtle.Turtle()
    step_size = 10
    font_size = 22
    output_filename = "/Users/Ahmed/Desktop/Junior Year/Spring 2021 Semester/Computational Creativity/CC Programming/M3-A_Markov_Distinction/first_output"
    testing.generate_markov_art(andrey, new_text, output_filename, step_size=step_size, font_size=font_size)

     
if __name__ == "__main__":
    main()