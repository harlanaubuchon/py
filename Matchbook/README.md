Matchbook compares two CSV files containing names and codes in order to provide 
a flexible way to return matches between the two files.  It was originally designed 
to compare unvalidated lists from Customs authorities which contain Names and Codes. 
The resulting files contain matching rows from the select and compare CSV files with 
a score value.

The matchbook_utility can be run to see how the Class objects can be utilized.

Requirements:
Python3
You will also need to download and install FuzzyWuzzy to use these modules.
Download or clone from here:
https://github.com/seatgeek/fuzzywuzzy
Run setup.py


The following is a brief description of the files in matchbook.

matchbook_reader: reads in CSV data expected in a 2 column format (Name, Code)

matchbook_data: provides alternative ways to use the data from CSV files.

matchbook: Uses fuzzywuzzy to match between to matchbook_reader objects and 
returns two CSV files with results.


