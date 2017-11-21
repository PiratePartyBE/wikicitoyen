#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import codecs
import sys
import json
from unidecode import unidecode
import re

r_article = re.compile(r' ((de (l|i)|d)\'|(de (l|i)a|de|du|des|aux) )', re.I)
r_street = re.compile(r'(impasse|rue|pre|avenue|cite|clos|chemin|chaussee|boulevard|dreve|square|route|vallee|allee) ', re.I)
r_streets = re.compile(r'(rue)s (.+?)( et|,) ')
r_hyphen = re.compile(r'\s*[\-\']\s*')
r_propernoun = re.compile(r'^[A-Z][a-z]{3,}$')

r_word = re.compile(r'[\w\-\']+', re.I)
r_particule = re.compile(r'^(de|la)$', re.I)

def abbreviate(sentence, lookup, train = False):
	if sentence.isupper():
		# if the sentence is capitalized, we only capitalize the first letter of each word
		sentence = sentence.title() 
	
	sentence = unidecode(sentence) # remove accentued chars
	
	# two modes : either we fill the lookup dictionary
	if train:
		words = sentence.split()
		
		# skip the first word, as it is in general the street's type
		# skip particule word ('de', 'la')
		nouns = [ (i, word) for i, word in enumerate(words[1:], 1) if not r_particule.search(word) ]
		
		# build a list indicating if a word is a proper noun or not 
		# (i.e. uppercase letter followed by lowercase letters)
		propers = [ (i, bool(r_propernoun.search(word))) for i, word in nouns ]
		
		# keep couple of proper nouns, to abbreviate the first one
		nouns = [ (i, words[i]) for p, (i, is_proper) in enumerate(propers) \
			if is_proper and p+1 < len(propers) and propers[p+1][1] ]
		
		# if we have results :)
		if len(nouns) > 0:
			i, noun = nouns[-1] # shorten the last result
			
			words[i] = noun[0] + '.'
			
			# add the couple to the dictionary
			lookup.add((noun.lower(), words[i+1].lower()))
		
		return ' '.join(words)
	
	# or we use the dictionary to check if a couple of words is there
	words = r_word.findall(sentence) # split to avoid noise (parenthesis, dots, commas, etc.)
	
	for i, word in enumerate(words):
		# if the current couple of words is in the dictionary
		if i+1 < len(words) and (word.lower(), words[i+1].lower()) in lookup:
			# we shorten the first
			sentence = sentence.replace(word, word[0] + '.')

	return sentence

def normalize(sentence):
	m = r_streets.search(sentence)
	while m:
		# when there is several streets, they can be grouped
		# we thus need to ungroup them
		sentence = sentence.replace(m.group(), m.group(1) + ' ' + m.group(2) + ' ' \
				+ (m.group(1) + 's ' if m.group(3).strip() == ',' else ''))
		m = r_streets.search(sentence)
	
	# replace street's type by a generic type ('rue'), to avoid wrong categorization of the street
	sentence = r_street.sub('rue ', sentence)
	
	# remove articles
	sentence = r_article.sub(' ', sentence)
	# remove hypens and quotation marks
	sentence = r_hyphen.sub(' ', sentence)
	
	# other replacements
	sentence = sentence.replace('Ier', '1er').replace('Lt', 'Lieutenant')
	
	return sentence.replace(' ', '').lower()


				
def read_streets(filename, city):
	streets = {}
	abbrs = set()
	
	with codecs.open(filename, 'r') as ifs:
		for line in ifs:
			line = line.split(';')
			
			street = line[3].strip()
			c = line[8].strip()
			
			if c != city:
				continue
			
			key = normalize( abbreviate(street, abbrs, train = True) )
			streets[key] = street
			
	return streets, abbrs


def parse(streets, abbrs, files, quiet = False):
	res_streets = set()
	
	for filename in files:
		with open(filename, 'r') as ifs:
			for line in ifs:
				line = line.strip()
				line = normalize( abbreviate(line, abbrs) )
				l = line
				
				results = []
				# collect the streets that are in the line
				for street in streets:
					if street in line:
						results.append(street)
					
				# filter streets shorter than some longer street, and beginning with the same words
				for street in results:
					if all([ street == other or street not in other for other in results ]):
						res_streets.add(street)
						
						line = line.replace(street, '\033[91m' + street + '\033[0m')
				
				if l != line and not quiet:
					print(line)
	
	return res_streets

if __name__ == '__main__':
	if len(sys.argv) < 4:
		print('Usage: address.py streets.csv <city> file1 [file2 ...]')
		exit(1)
	
	streets, abbrs = read_streets(sys.argv[1], sys.argv[2])
	
	parse(streets, abbrs, sys.argv[3:])
