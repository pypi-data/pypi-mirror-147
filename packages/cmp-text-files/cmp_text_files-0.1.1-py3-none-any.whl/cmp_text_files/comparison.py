import difflib

class Comparison:
    """A simple attempt to model a comparison of text files"""

    def __init__(self) -> None:
        """Initialize comparison attributes"""
        pass


    def compare(self):
        """Compare given text files"""

        # Ask the user to enter the names of files to compare
        file_name_1 = input("Enter the first file name with its path: ")
        file_name_2 = input("Enter the second file name with its path: ")

        # Open file for reading in text mode (default mode)
        file_1 = open(file_name_1)
        file_2 = open(file_name_2)
  
        file_1_text = file_1.readlines()
        file_2_text = file_2.readlines()
  
        # Find and print the diff:
        for line in difflib.unified_diff(
                file_1_text, file_2_text, fromfile=file_name_1, 
                tofile=file_name_2, lineterm=''):
            print(line)
