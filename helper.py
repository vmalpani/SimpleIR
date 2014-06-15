#!/usr/bin/python -O

import xml.etree.ElementTree as et
import nltk
import sys
import operator
import re

from collections import namedtuple
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from string import punctuation

def clean_data(rawdata):
	'''
	This is where preprocessing occurs. On rigorous testing, LancasterStemmer 
	was found to produces better results. Alternatively, one can also use PorterStemmer. 
	The entire preprocessing including eliminating stop words, stripping punctuation, 
	stemming and lower casing is done in a single line of code. 
	'''
	# stop words
	english_stops = set(stopwords.words('english'))
    
	# define stemmer
	portst = nltk.PorterStemmer()
	lancast = LancasterStemmer()
	
	# stemmmer auto converts words to lower case
	normal_text = [(lancast.stem(word.strip(punctuation))) for word in rawdata.split() if (word.strip(punctuation) and word not in english_stops)]
	return normal_text

def merge_dict(dicts):
	'''
	Used to combine multiple dictionaries. While merging, if the key value of different
	dictionaries match we add all the values. We can't sum the value of common keys using 
	the default update() function. We merge the individual dictionaries of each query term 
	to generate the final scoring_dict
	'''
	super_dict = {}
	for k in set(k for d in dicts for k in d):
		super_dict[k] = sum((d[k] for d in dicts if k in d))
	return super_dict
	
def print_format(query, final_dict, doc_idx, orig_data, clean_doc_text):
	'''
	Printing the output in the following specification:
	
	############################################################
	DocNum. 	Title
			author
	"Text snippets of first 1-2 matches"
	############################################################
	
	Once we have the final scores sorted in decreasing order, we call this function
	to print the top 15 documents in the above specified format.
	'''
	sort_scores = sorted(final_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
	processed_query = [word.strip(punctuation) for word in query.split() if (word.strip(punctuation))]
	count = 0
	
	print "\n\n############################################################"
	print "\n\t\t\tTOP 15 HITS\n"
	print "############################################################\n"
# 	print orig_data
	for (i,j) in sort_scores:
		count += 1
		# add
		orig_text = orig_data['\n'+str(i)+'\n'][3]
		try:		
			if count < 16 and orig_data:
				print "\n\n\n" + str(i) + ".\t" + orig_data[str(i)][0].upper()
				print "\t" + orig_data[str(i)][1] + "\n"
				for k in processed_query:
					out = ''
					if k in orig_text:
# 						print "query in doc\n\n"
						start = orig_text.index(k)
						if start > 30:
							out = '...' + ''.join(orig_text[start - 30:start + 30]) + '...'
						elif start > 20:
							out = '...' + ''.join(orig_text[start - 20:start + 20]) + '...'
						elif start > 15:
							out = '...' + ''.join(orig_text[start - 15:start + 15]) + '...'
						elif start > 10:
							out = '...' + ''.join(orig_text[start - 10:start + 10]) + '...'
						else:
							out = '...' + ''.join(orig_text[start:start + 10]) + '...'

						print (out.replace('\n', ' ')),
					if out == '':
						print ('...' + orig_text[0:50] + '...'),
						
		# Handling exception in case the author field is blank
		except:
			print "\t" + "anonymous" + "\n"
# 			print orig_data[str(i)][3] + "\n"
			for k in processed_query:
				out = ''
				if k in orig_text:
# 						print "query in doc\n\n"
					start = orig_text.index(k)
					if start > 30:
						out = '...' + ''.join(orig_text[start - 30:start + 30]) + '...'
					elif start > 20:
						out = '...' + ''.join(orig_text[start - 20:start + 20]) + '...'
					elif start > 15:
						out = '...' + ''.join(orig_text[start - 15:start + 15]) + '...'
					elif start > 10:
						out = '...' + ''.join(orig_text[start - 10:start + 10]) + '...'
					else:
						out = '...' + ''.join(orig_text[start:start + 10]) + '...'

					print (out.replace('\n', ' ')),
					
				if out == '':
					print ('...' + orig_text[0:50] + '...'),