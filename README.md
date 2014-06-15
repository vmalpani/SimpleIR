			-----------------------------
			   SEARCH ENGINE TECHNOLOGY
			-----------------------------
1. Vaibhav Malpani			vom2102

===================================================================
CODE ARCHITECTURE :
===================================================================
STAGE 1:
The code executes by first taking user input of an xml file. 
This file is then parsed in the init() function and we store the
original data as a list of namedtuples. Also, we create a dictionary
mapping document number to its text.

While indexing we preprocess the data using clean_data helper function.
Once the preprocessing is completed, a dictionary of dictionaries is 
used to represent indexing (Term --> DocNum --> [Locs]). Finally
we use cPickle to save - original metadata, processed document index
and dictionary mapping of document text.

We use the built in packages like os, time to display important statistics
of the stored data.

STAGE 2:
In the second stage we prompt the user to enter a query or type in quit.
Once the query is entered, the preprocess_query function is called to look
for statistical queries (df, tf, similar, etc..). 

The preprocess_query function then calls classify_query to identify the category of each of the entered terms. Once the categories are decided, the classify_query function in turn calls the search_query function to lookup the indexing structure and generate an output dictionary of each of the terms. We have 4 separate cases in the search_query method to handle each category (Word, Phrase,Negative Word, Negative Phrase).

We then merge all the dictionaries into a final_dict using the merge_dict 
helper function and sort it in decreasing order of ranks.
Last, but not the least, we call the print_format helper function
to display the output in the desired format.

===================================================================
TO EXECUTE :
===================================================================
1. python -t preprocessDB.py
2. python -t query.py
	
STEP 1: 
To execute, type in the 1st line of code. Enter appropriate path 
of 'crane.xml' when prompted. This would build up the document index.

STEP 2:
Once the document index is ready, enter the 2nd line of code. 
Type in the desired query and the top 15 hits would be displayed.

STEP 3:
The code automatically prompts you to enter another query once the
earlier one is evaluated. To quit, type 'Quit' or 'quit'


===================================================================
DELIVERABLES :
===================================================================
1. preprocessDB.py
2. query.py
3. helper.py