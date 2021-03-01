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

class MarkovTextArt:

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

            
    def generate_markov_art(self, markov_text):
        """
        Reads through each character of markov_text and generates art based off of 
        """       

        

def main():
    testing = MarkovTextArt()
    testing.read_from_file("/Users/Ahmed/Desktop/Junior Year/Spring 2021 Semester/Computational Creativity/CC Programming/M3-A_Markov_Distinction/arctic_monkeys_AM_album_song_lyrics.txt")
    
    print(testing.frequency_table)
    print()
    #testing.populate_transition_matrix()
    #print(testing.transition_matrix)
    print()
    #print(testing.get_next_char('a'))

    print(testing.generate_markov_text(2000, "t"))

     
if __name__ == "__main__":
    main()