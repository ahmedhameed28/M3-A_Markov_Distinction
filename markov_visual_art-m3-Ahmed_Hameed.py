"""
A program that reads in text, computes transition probabilities based on the text, creates new text based
off those probabilites, then creates art based off the text

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

class MarkovTextArt:

    # Mapping of alphabetic characters to RGB values of colors. RGB values are retty uniformly distributed 
    # across the color spectrum
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
        Constructs a new MarkovTextArt class with a transition 
        """
        # a frequency table that tracks 1 previous character occurences based off of current character
        # dictionary where a key is the current character and a value is a dictionary of previous characters
        # and their number occurrences
        self.frequency_table = frequency_table
        
        #self.all_chars = list(self.frequency_table.keys())

        # transition probabilites matrix based off of character occurrences in frequency table 
        # MIGHT JUST POPULATE USING A FUNCTION THAT RETURNS A TRANSITION MATRIX??
        self.transition_matrix = transition_matrix
    

    def read_string(self, words):
        """
        Function that takes a string, words, and reads through each character while updating the
        frequency table.
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
                    #self.frequency_table[current_char].update({prev_char: 1})
            
            # otherwise, create a new entry in the dictionary for the character
            else:
                self.frequency_table[current_char] = {prev_char: 1}


    def read_from_file(self, filename):
        """
        Given a filename, reads the contents of that file and populates the frequency table, line by line.
            Args: filename (str) - The name of the .txt file to be processed. 
        """
        text_file = open(filename, 'r')

        # read entire file as a string and send to read_string()
        text_str = text_file.read()
        self.read_string(text_str)
        print("File size ", len(text_str), "characters")
        #for line in text_file:
        #    self.read_string(line)
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
        """
    
        # iterate over every character key in frequency table
        for key in self.frequency_table.keys():

            prev_char_dict = self.frequency_table.get(key)
            #print("Prev Char Dict:", prev_char_dict)
            total_sum = self.sum_char_occurences(prev_char_dict)
            #print("Total sum:", total_sum)
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
        #print(current_char)
        prev_chars_dict = self.frequency_table.get(current_char)
        all_chars = list(prev_chars_dict.keys())
        char_counts = list(prev_chars_dict.values())

        next_char = ''.join(rand.choices(list(all_chars), weights=char_counts, k=1))
        return next_char


    def generate_markov_text(self, num_chars, start_string):
        """
        Uses a 1-order Markov chain (a matrix of characters and transition probabilites) to generate new
        text based off the previous character occurrences. A 1-order Markov chain only looks the previous 
        state. Creates new text of size num_chars, and the new text continues after the last character 
        in start_string
        Example: "This is a test string!!!!!!!!" --> At character '!': There's a 87.5% chance of the next
                character being another '!' and a 12.5% of it being 'g'.
            Args:
                num_chars (int) - The number of characters to be generated by the function
                start_string (str) - The start of the new text, last character will be used to generate
                                        the new text. 
            Return:
                markov_text (str) - The new text generated by the 1-order Markov Chain and transition matrix
        """

        markov_text = "Start String: " + start_string + "\n"

        current_char = start_string[-1]
        for i in range(num_chars):
            next_char = (self.get_next_char(current_char))
            markov_text += next_char
            current_char = next_char
        
        return markov_text

            
    def draw_one_char(self, turtle_dude, screen_size, start_coords, current_char):
        """
        Uses the turtle object to create a visual for just one character
        """

        # current (x,y) position of turtle dude before any drawing 
        t_pos = turtle_dude.pos()
        pen_size = turtle_dude.pensize()
        initial_pen_state = turtle_dude.pen()
        #turtle_dude.setheading(0)
        
        if current_char.isalpha():
            color_RGB = self.CHARS_TO_COLORS.get(current_char)
            turtle_dude.pendown()
            turtle_dude.color(color_RGB)
            turtle_dude.circle(20)
        elif current_char == " ":
            turtle_dude.penup()
        elif current_char == ".":
            turtle_dude.dot()
            turtle_dude.end_fill()
        elif current_char == ",":
            turtle_dude.begin_fill()
        elif current_char == ("\'" or "\""):
            turtle_dude.shape("arrow")
            turtle_dude.setheading(0) # might comment this line out
            turtle_dude.stamp()
        elif current_char == "?":
            turtle_dude.shape("classic")
            turtle_dude.stamp()
        elif current_char == "!":
            turtle_dude.shape("triangle")
            turtle_dude.stamp()
        elif current_char == (":" or ";"):
            turtle_dude.shape("square")
            turtle_dude.stamp()
            pen_speed = turtle_dude.pen().get("speed")
            turtle_dude.pen(pensize=pen_size+1, speed=pen_speed+1)
        elif current_char == "-":
            turtle_dude.pen(tilt=30.0, pensize=pen_size+1, speed=4)
        elif current_char == "\n":
            # will need to fiddle around with this value so that turtle doesn't go off the screen
            turtle_dude.setpos(start_coords[0], t_pos[1] + 10)
            turtle_dude.pen(initial_pen_state)
            turtle_dude.shape("turtle")
        elif current_char.isdigit():
            num = int(current_char)
            turtle_dude.speed(num)
            turtle_dude.pen(stretchfactor=(num, num/2))

        
        turtle_dude.setheading(0)
        current_pos = turtle_dude.pos()
        # NEED TO FIX LOGIC OF COORDINATES HERE, WAS ASSUMING WRONG KIND OF COORDINATE SYSTEM
        if (-screen_size[1]/2 - current_pos[1]) < 10: #?? Unsure of this
            turtle_dude.setpos(start_coords)
        elif (screen_size[0]/2 - current_pos[0]) < 10:
            turtle_dude.setpos(start_coords[0], current_pos[1] - 10)
        else:
            turtle_dude.forward(10)
        




    def generate_markov_art(self, markov_text, screen_width, screen_height, background_color, output_name):
        """
        Reads through each character of markov_text and generates art based off of each character. 
        Art is generated using the Turtle module.
            Args:
                markov_text (str) - A string containing the text produced by the markov chain
        """
        
        andrey = turtle.Turtle()
        t_screen = andrey.getscreen()
        t_screen.screensize(screen_width, screen_height)
        t_screen.bgcolor(background_color)
        t_screen.colormode(255)
        # want turtle to start drawing at the top left of the screen, similar to how 
        # English is written from left to right
        start_coords = (-screen_width/2, screen_height/2) # NEED TO FIX THIS, what are x,y coordinates based
        # off of the screen size? Are those things even related?
        andrey.setpos(start_coords)
        andrey.speed(9)

        for char in markov_text:
            self.draw_one_char(andrey, (screen_width, screen_height), start_coords, char)

        t_canvas = andrey.getscreen().getCanvas()
        t_canvas.postscript(file=output_name+".eps", width=screen_width, height=screen_height)
        img_output = Image.open(output_name + ".eps")
        img_output.save(output_name + ".png")




        

def main():
    testing = MarkovTextArt()
    testing.read_from_file("/Users/Ahmed/Desktop/Junior Year/Spring 2021 Semester/Computational Creativity/CC Programming/M3-A_Markov_Distinction/arctic_monkeys_AM_album_song_lyrics.txt")
    
    print(testing.frequency_table)
    print()
    #testing.populate_transition_matrix()
    #print(testing.transition_matrix)
    print()
    #print(testing.get_next_char('a'))

    new_text = testing.generate_markov_text(2000, "t")
    print(new_text)
    print()
    screen_w = 2000
    screen_h = 1600
    background = 'black'
    testing.generate_markov_art(new_text, screen_w, screen_h, background, "first_output")


     
if __name__ == "__main__":
    main()