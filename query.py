#!/usr/bin/python -O

import xml.etree.ElementTree as et
import nltk
import sys
import operator
import re
import cPickle
import time

from helper import *
from collections import namedtuple
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from string import punctuation

def preprocess_query(var, doc_idx, metadata, cleanmetadata):
	'''
	This method is used to check for statistical queries like df, freq, tf,
	title, author, biblio, text and similar terms. It then strips off these terms
	from the search query and passes the main query to classify_query.
	Essentially the main function of the project.
	'''
	final_out = {}
	
	if 'df ' in var:
		var = var.replace('df ', '')
		final_out = classify_query(var, doc_idx)
		print "\nDocument Frequency of " + var + " : " + str(len(final_out.keys()))
	
	elif 'freq ' in var:
		var = var.replace('freq ', '')
		final_out = classify_query(var, doc_idx)
		print "\nFrequency of " + var + " : " + str(sum(final_out.values()))
	
	elif 'tf ' in var:
		var = var.replace('tf ', '')
		doc_num = re.findall(r'\d+\s', var)
		var = re.sub(r'\d+\s', "", var)
		doc_num = int(doc_num[0])
		final_out = classify_query(var, doc_idx)
		print "\nTerm Frequency of " + var + " : " + str(final_out[doc_num])
		
	elif 'title ' in var:
		var = var.replace('title ', '')
		doc_num = re.findall(r'\d+', var)
		print doc_num
		var = re.sub(r'\d+', "", var)
		print "\nDocument Title: " + metadata[doc_num[0]][0]

	elif 'author ' in var:
		var = var.replace('author ', '')
		doc_num = re.findall(r'\d+', var)
		var = re.sub(r'\d+', "", var)
		print "\nDocument Author: " + metadata[doc_num[0]][1]

	elif 'bib ' in var:
		var = var.replace('bib ', '')
		doc_num = re.findall(r'\d+', var)
		var = re.sub(r'\d+', "", var)
		print "\nDocument Biblio: " + metadata[doc_num[0]][2]
		
	elif 'doc ' in var:
		var = var.replace('doc ', '')
		doc_num = re.findall(r'\d+', var)
		var = re.sub(r'\d+', "", var)
		print "\nDocument Text: " + metadata[doc_num[0]][3]
		
	elif 'similar ' in var:
		var = var.replace('similar ', '')
		similar_words ={}
		
		for i in metadata.values():
			for k in i[3].split():
				if k.strip(punctuation):
					k = k.strip(punctuation)
				similarity = nltk.edit_distance(k, var)
				if similarity < 3:
					similar_words[k] = similarity
		print "\nWords similar to " + var + ": "
		sort_scores = sorted(similar_words.iteritems(), key=operator.itemgetter(1))
		unique_similar = set()
		for (i,j) in sort_scores:
			unique_similar.add(i)
		print unique_similar
		print len(unique_similar)
	else:
# 		print "No stat query"
# 		print "var"
		final_out = classify_query(var, doc_idx)
	
	
	if final_out != {}:
		print_format(var, final_out, index_data, metadata, cleanmetadata)
	
	return final_out


def query_search(usr_inp, qtype, index_file):
	'''
	Separate cases to hanle Type-1,2,3,4 Queries
	Type 1 - Normal Single Word
	Type 2 - Entire Phrase
	Type 3 - Negation Single Word
	Type 4 - Negation Entire Phrase
	
	This function generates a score dictionary for each individual query type
	and returns the dictionary to classify_query
	'''
	processed_query = clean_data(usr_inp)
# 	print "Processed Query is: "
# 	print processed_query
	scoring_dict = {}
	flag = False
	
	if qtype == 1:
		for i in processed_query:
			if i in index_file.keys():
				flag = True
				for k,v in index_file[i].items():
					if k in scoring_dict.keys():
						scoring_dict[k] += len(v)
					else:
						scoring_dict[k] = len(v)
	elif qtype == 2:

		temp_dict = {}
		if processed_query[0] in index_file.keys():
				temp = index_file[processed_query[0]]
				for key, value in temp.items():
					temp_dict[key] = [set(value)]
				for j in range(1, len(processed_query)):
					if processed_query[j] in index_file.keys():
						for k,v in index_file[processed_query[j]].items():
							if k in temp_dict.keys():
								temp_dict[k].append(set(v))
				#print "Type-2 Scoring Temp Dictionary: " 
				#print temp_dict
				
				for docnum, locs in temp_dict.items():
					count = 0
					if len(locs) == len(processed_query):
						for k in temp_dict[docnum][0]:
							for i in range(1, len(locs)):
# 								print docnum, k+i, temp_dict[docnum][i]
								if k+i in temp_dict[docnum][i]:
									if i == len(locs)-1:
# 										print "Match Found. Count Incremented"
										flag = True
										count += 1
								else:
									break
					if flag:		
						scoring_dict[docnum] = count*len(processed_query)
# 						print "Count: " + str(count)
		#print "Type-2 Scoring Final Dictionary: " 
		#print scoring_dict
					
	elif qtype == 3:
		scoring_dict = {i: 1 for i in range(1,1401)}
		for j in processed_query:
			if j in index_file.keys():
				flag = True
				for k in index_file[j].keys():
					if k in scoring_dict.keys():
						#scoring_dict[k] = 0
						scoring_dict.pop(k, None)
		print len(scoring_dict)
	
	elif qtype == 4:
		temp_dict = {}
		if processed_query[0] in index_file.keys():
				temp = index_file[processed_query[0]]
				for key, value in temp.items():
					temp_dict[key] = [set(value)]
				for j in range(1, len(processed_query)):
					if processed_query[j] in index_file.keys():
						for k,v in index_file[processed_query[j]].items():
							if k in temp_dict.keys():
								temp_dict[k].append(set(v))
				#print "Type-2 Scoring Temp Dictionary: " 
				#print temp_dict
				
				for docnum, locs in temp_dict.items():
					count = 0
					if len(locs) == len(processed_query):
						for k in temp_dict[docnum][0]:
							for i in range(1, len(locs)):
# 								print docnum, k+i, temp_dict[docnum][i]
								if k+i in temp_dict[docnum][i]:
									if i == len(locs)-1:
# 										print "Match Found. Count Incremented"
										flag = True
										count += 1
								else:
									break
					if flag:		
						scoring_dict[docnum] = count*len(processed_query)
# 						print "Count: " + str(count)
		for i in range(1,1401):
			if i in scoring_dict.keys():
				scoring_dict.pop(i, None)
			else:
				scoring_dict[i] = len(processed_query)

		#print "Type-4 Scoring Final Dictionary: " 
		#print scoring_dict
										
	if flag == False:
				print "\nYour search - " + usr_inp + " did not match any documents."
				print "\nSuggestions:"
				print "Make sure all words are spelled correctly."
				print "Try different keywords."
				print "Try more general keywords."
				print "Try removing quotes.\n"	
	
	return scoring_dict 

def classify_query(var, doc_index):
	'''
	Classifies each query into the following types:
	Type 1 - Normal Word
	Type 2 - Phrase
	Type 3 - Negation Word
	Type 4 - Negation Phrase
	
	Each of the term in user input is classified and sent to query_search which returns
	a list of score dictionaries for each term. Finally, we merge all dictionaries using 
	the helper function merge_dict to generate a final score dictionary.
	'''
	out = []
	
	if '!"' in var:
		for i in re.findall(r'\!\"(.+?)\"', var):
# 			print "Not Quotes Removed"
			out.append(query_search(i, 4, doc_index))
			print "Query Type : 4"
# 			print i
		  	print "\n"
		var = re.sub(r'\!\"(.+?)\"', "", var)

	if '"' in var:
# 		print "Quotes Removed"
		for i in re.findall(r'\"(.+?)\"', var):
			out.append(query_search(i, 2, doc_index))
			print "Query Type : 2"
# 			print i
		  	print "\n"
		var = re.sub(r'\"(.+?)\"', "", var)

	if var != '':
# 		print "Normal Words removed"
		inp = var.split()
		for i in inp:
			if '!' in i:
				out.append(query_search(i, 3, doc_index))
				print "Query Type : 3"
# 				print i
			  	print "\n"
			else:
				out.append(query_search(i, 1, doc_index))
				print "Query Type : 1"
# 				print i
			  	print "\n"
# 	print "Dictionaries of terms:"
# 	print out
#   	print "\n"
	
 	final_scores = merge_dict(out)
	sort_scores = sorted(final_scores.iteritems(), key=operator.itemgetter(1), reverse=True)
 	
#  	print "Final Scores: "
#   	print final_scores
#   	print "\n"
#   	
#  	print "Sorted Scores: " 
# 	print sort_scores
#   	print "\n"

 	print "\nTotal Number of Documents: " + str(len(final_scores.keys()))
	print "\nTotal Number of Occurences: " + str(sum(final_scores.values()))
		
	return final_scores


################################################################################

##############				Query Search Begins Here			################

################################################################################

flag_query = True

# Loop till the user quits
while flag_query==True:
	temp = raw_input("\nEnter Query or Type Quit: ")
	if temp == 'Quit':
		flag_query = False
	elif temp == 'quit':
		flag_query = False
	else:
		searchq = temp
		start_time = time.time()

		# Load data from disk
		index_data = cPickle.load(open('doc_index.p', 'rb'))
		meta_data = cPickle.load(open('doc_metadata.p', 'rb'))
		clean_meta_data = cPickle.load(open('doc_clean_text.p', 'rb'))
		out = preprocess_query(searchq, index_data, meta_data, clean_meta_data)

		print "\n"
		print "\nAbout " + str(len(out.keys())) + " results (" + str(time.time() - start_time) + " seconds)"