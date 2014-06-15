#!/usr/bin/python -O

import xml.etree.ElementTree as et
import nltk
import sys
import operator
import re
import cPickle
import time
import os

# add
import glob 
import shutil

from helper import *
from collections import namedtuple
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from string import punctuation
	
def init(xml_path):
	'''
        Parse the given xml using ElementTree
        Preprocessing xml includes:
			1. Changing text to lowercase
			2. Removing punctuation (Not hypen as it might have undesirable results)
			3. Eliminating stop words
        We use clean_data helper function in helper.py for preprocessing
    '''
	
	xmlTree = et.parse(xml_path)
	xmlRoot = xmlTree.getroot()
    
	metadata = namedtuple('metadata', 'docnum title author bib txt')
	docDB = []
	doc_dict = {}
    
	# Parse the xml file and extract relevant info using find, findall functions
	for docs in xmlRoot.findall('DOC'):
		docNum = docs.find('DOCNO').text
		title = docs.find('TITLE').text
		author = docs.find('.//AUTHOR').text
		bib = docs.find('BIBLIO').text
		txt = docs.find('TEXT').text
        
		doc_dict[docNum] = [title,author,bib,txt]
		Node = metadata(docNum, title, author, bib, txt)
		docDB.append(Node)
		
	text_list = []
    
	for i in docDB:
		# preprocessing the raw data
		text_list.append(clean_data(i[4]))
    
	# Dictionary of Dictionaries Word --> Doc Num --> [Occurrences]
	index = {}
	count_docs = 0
	count_words = 0
	for i in text_list:
		count_docs += 1
		for j in range(len(i)):
			if len(i[j]) > 2 and not i[j].isdigit():
				count_words += 1
				if i[j] in index.keys():
					if count_docs in index[i[j]].keys():
						index[i[j]][count_docs].append(j)
					else:
						index[i[j]][count_docs] = []
						index[i[j]][count_docs].append(j)
				else:
					index[i[j]] = {}
					index[i[j]][count_docs]= []
					index[i[j]][count_docs].append(j)
		if count_docs % 100 == 0:
			print "Indexing Files..."
    
	cPickle.dump(index, open('doc_index.p', 'wb'))
 	cPickle.dump(doc_dict, open('doc_metadata.p', 'wb'))
  	cPickle.dump(text_list, open('doc_clean_text.p', 'wb'))
	print "\n" + str(count_words) + " Words in " + str(count_docs) + " Files Indexed Successfully!!"
	print "\nIndex Stored: doc_index.p"


################################################################################

##############				Code Flow Begins Here				################

################################################################################

cran_path = raw_input("Enter Path Of XML(No Quotes): ")

# add
with open(cran_path, 'wb') as outfile:
	outfile.write('<cran>\n')
	for filename in glob.glob('*.xml'):
		with open(filename) as readfile:
			shutil.copyfileobj(readfile, outfile)
	outfile.write('\n</cran>')

start_time = time.time()
init(cran_path)
print "\nIndexing Time: ", time.time() - start_time, "seconds"
print "\nIndex File Size: " + str((os.stat('doc_index.p')).st_size)
print "\nMetadata File Size: " + str((os.stat('doc_metadata.p')).st_size)