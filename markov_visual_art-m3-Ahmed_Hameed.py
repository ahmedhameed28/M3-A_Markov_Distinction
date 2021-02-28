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

class MarkovTextArt:

    def __init__(self, frequency_table={{}}, transition_matrix={}):
        """
        Constructs a new MarkovTextArt class with a transition 
        """
        # a frequency table that tracks 1 previous character occurences based off of current character
        # dictionary where a key is the current character and a value is a dictionary of previous characters
        # and their number occurrences
        self.frequency_table = frequency_table

        # transition probabilites matrix based off of character occurrences in frequency table 
        # MIGHT JUST POPULATE USING A FUNCTION THAT RETURNS A TRANSITION MATRIX??
        self.transition_matrix = transition_matrix
    
    def read_string(self, words):
        """
            Function that takes a string, words, and reads through each character while updating the
            frequency table.
        """
        for i in range(1, len(words)):
            current_char = words[i]
            prev_char = words[i-1]
            # NEED TO LOOK UP WHAT METHODS CAN BE CALLED ON A PYTHON DICT
            prev_char_freq = frequency_table.get(current_char).get(prev_char)
            frequency_table.get(current_char) = {prev_char: prev_char_freq+1}

