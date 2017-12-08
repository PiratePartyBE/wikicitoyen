#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import re
import sys

import copy
import json
import random

import grammar

from itertools import product
from unidecode import unidecode

class Tag:
	def __init__(self, terms, value, children = None, intersect = None, disjoin = None, union = None, erase = True, replace = True):
		self.value = value
		self.type = 'other'
		
		if isinstance(terms, str):
			terms = [ terms ]
		self.terms = [ Word(term) if isinstance(term, str) else term for term in terms ]
		
		self.children = set() if not children else children
		self.intersect = set() if not intersect else intersect
		self.union = set() if not union else union
		self.disjoin = set() if not disjoin else disjoin
		
		self.erase = bool(erase)
		self.replace = bool(replace)
		
		self.values = set()
		
	def parse(self, text):
		self.matches = []
		self.values = set()
		
		for term in self.terms:
			#size = 0
			for match, value in term.findall(text):
				if self.replace:
					#start, end = map(lambda x: x - size, match.span())
					#replace = '' if self.erase else str(value)
					#text = text[:start] + replace + text[end:]
					#print('s:', start, 'e:', end, 'w:', size, match.group(), replace, text)
					#size += len(match.group()) - len(replace)
					text = re.compile(r'\b' + re.escape(match.group()) + r'\b').sub(('' if self.erase else str(value)), text)
				
				self.matches.append(match)
				self.values.add(self.value if self.value else value)
		
		return self.values, text
	
	def highlight(self, text):
		for match in self.matches:
			match = match.group()
			text = re.compile(r'\b' + match + r'\b').sub('\033[91m' + match + '\033[00m', text)
		
		return text
	
	def __repr__(self):
		name = self.__class__.__name__
		value = self.value if self.value else ','.join(map(str, self.values))
		
		if value:
			name += ':' + value
			
		return name
	
	def find(self, attributes, tags):
		for value in attributes:
			if isinstance(value, tuple):
				attr, value = value
			else: attr = 'value'
			
			for tag in tags:
				if tag is not self and hasattr(tag, attr) and getattr(tag, attr) == value:
					yield tag
	
	def require(self, tags):
		self.requiredtags = set(self.find(self.intersect, tags))
		
		return not self.intersect or self.requiredtags
	
	def merge(self, tags):
		self.mergedtags = set(self.find(self.union, tags))
	
	def unify(self, tags):
		self.childtags = set(self.find(self.children, tags))
	
	def exclude(self, tags):
		self.excludedtags = set(self.find(self.disjoin, tags))
		
		return self.disjoin and self.excludedtags
		
	def isroot(self, tags):
		for tag in tags:
			if self in tag.childtags:
				return False
			
		return True
	
	def isparent(self, tag):
		return tag in self.childtags
	
	def __contains__(self, tag):
		if not isinstance(tag, Tag):
			raise TypeError('Tag can only contains other tags')
		
		for child in self.childtags:
			if tag is child or tag in child:
				return True
			
		return False
		
	def dump(self):
		#if not self.childtags:
			#return [ { 'type' : self.type, 'value' : value } for value in self.values ]
		
		properties = { 'type' : self.type, 'value' : self.values }
		
		for child in self.childtags:
			for dump in child.dump():
				del dump['type']

				for key, value in dump.items():
					if isinstance(value, dict) and len(value) == 1:
						dump[key] = next(iter(value.values()))

				if len(dump) == 1:
					dump = next(iter(dump.values()))
				
				if child.type not in properties:
					properties[child.type] = [ dump ]
				else:
					properties[child.type].append(dump)
		
		singlevalues = {}
		multivalues = {}
		for key, value in properties.items():
			if not isinstance(value, (list, set)):
				singlevalues[key] = value
			else:
				multivalues[key] = value
				
		keys, values = zip(*multivalues.items())
		
		results = []
		for value in product(*values):
			d = dict(zip(keys, value))
			d.update(singlevalues)
			
			results.append(d)
			
		return results

class TagFactory:
	tags = { 'other' : Tag }
	
	def genClass(d):
		if 'type' in d:
			return None
		
		tag_children, tag_union, tag_intersect, tag_disjoin = (d[option] if option in d else None for option in ('children', 'union', 'intersect', 'disjoin'))
		
		tag_type = d['value']
		tag_parent = TagFactory.tags[d['parent']] if 'parent' in d and d['parent'] in TagFactory.tags else Tag
		tag_class = (tag_type.title() if tag_type != 'other' else '') + 'Tag'
		
		def __init__(self, terms, value = None, children = None, intersect = None, disjoin = None, union = None, erase = True, replace = True):
			super(TagFactory.tags[tag_type], self).__init__(terms, value, children, intersect, disjoin, union, erase, replace)
			
			self.type = tag_type
			
			if tag_children:
				self.children.update(tag_children)
			
			if tag_union:
				self.union.update(tag_union)
				
			if tag_intersect:
				self.intersect.update(tag_intersect)
				
			if tag_disjoin:
				self.disjoin.update(tag_disjoin)
		
			return None
			
		TagFactory.tags[tag_type] = type(tag_class, (tag_parent,), { '__init__' : __init__ })
		
		return TagFactory.tags[tag_type]
	
	def genTag(d):
		if 'type' not in d or d['type'] not in TagFactory.tags:
			return None
		
		SomeTag = TagFactory.tags[d['type']]
		
		options = { option : d[option] if option in d else None for option in ('value', 'children', 'intersect', 'disjoin', 'union') }

		return SomeTag(
			d['terms'], 
			value = options['value'], 
			children = options['children'], 
			intersect = options['intersect'], 
			disjoin = options['disjoin'],
			union = options['union'],
			erase = d['erase'] if 'erase' in d else True,
			replace = d['replace'] if 'replace' in d else True
		)
		



class SemanticParser:
	def __init__(self):
		for rule in grammar.rules:
			if 'type' not in rule:
				TagFactory.genClass(rule)
		
		self.grammar = [ TagFactory.genTag(rule) for rule in grammar.rules if 'type' in rule ]

	def parse(self, text, verbose = True):
		text = unidecode(text).strip()
		
		if not text:
			return [], text
		
		diff = text
		tags = set()
		for tag in self.grammar:
			values, text = tag.parse(text)
			if not values:
				continue
			
			tags.add(tag)
			
			#if verbose:
			diff = tag.highlight(diff)
		
		if not tags:
			return [], diff
		#for tag in tags:
			#if not tag.require(tags):
				#print("not tag.require", tag, tag.matches, diff)
		tags = set(tag for tag in tags if tag.require(tags))
		#for tag in tags:
			#if any(map(lambda t: tag in t.requiredtags, tags)):
				#print("any", tag, tag.matches, diff)
		
		#tags = set(tag for tag in tags if not any(map(lambda t: tag in t.requiredtags, tags)))
		
		for tag in tags:
			tag.merge(tags)
		
		tags = set(tag for tag in tags if not any(map(lambda t: tag in t.mergedtags, tags)))
		
		tags = set(tag for tag in tags if not tag.exclude(tags))
		
		for tag in tags:
			tag.unify(tags)
		
		
		roots = self.prune(tags)
		
		res = [ dump for tag in roots for dump in tag.dump() ]
		
		if verbose:
			print(res, diff)
		
		return res, diff
	
	def find(self, tag, tags):
		if not tags:
			return False
		
		for t in tags:
			if tag is t or self.find(tag, t.childtags):
				return True
		
		return False
	
	def prune(self, tags):
		tags = [ tag for tag in tags if not any(map(lambda t: self.find(tag, t.childtags), tags)) ]
		
		for tag in tags:
			tag.childtags = self.prune(tag.childtags)
		
		return tags
			
	#def prune(self, toprune, tags = None, parent = True):
		#if not tags:
			#tags = toprune
		
		##print('toprune', toprune, 'tags', tags)
		##for tag in toprune:
			##for t in tags:
				##print(tag, t, parent and t.isparent(tag), tag is t, tag in t)
		#return set(tag for tag in toprune if not any(map(lambda t: not (parent and t.isparent(tag)) and tag is not t and tag in t, tags)))

def walk(data, key = None):
	if isinstance(data, dict):
		for k, value in data.items():
			for item in walk(value, key if key and key not in k else None):
				yield item
	elif isinstance(data, list):
		for value in data:
			for item in walk(value, key):
				yield item
	elif isinstance(data, str):
		if not key:
			yield data

if __name__ == '__main__':
	parser = SemanticParser()
	
	args = sys.argv[1:]
	
	test = False
	for i, arg in enumerate(args):
		if arg == '-t':
			test = True
			del args[i]
	
	if test:
		results = []
		for arg in args:
			always = False
			with open(arg, 'r') as ifs:
				for line, tags in json.load(ifs):
					diff = False
					parsed, highlight = parser.parse(line, verbose = False)
					for tag in parsed:
						if tag not in tags:
							diff = True
					for tag in tags:
						if tag not in parsed:
							diff = True
							
					if diff:
						print(sorted((tag for tag in tags if tag not in parsed), key=str))
						print(sorted((tag for tag in parsed if tag not in tags), key=str))
						print(highlight)
						if not always:
							ans = input("Accepter ou rejeter (o) ? ")
							if ans == 'a':
								always = True
								ans = True
							else:
								ans = not ans or ans.lower() in 'yo' 
								
						results.append([ line, parsed if ans else tags ])
						print("Acceptée" if ans else "Rejetée")
						print()
					else:
						results.append([ line, tags ])
		
		with open("output.json", 'w') as ofs:
			json.dump(results, ofs, indent=4, ensure_ascii=False)
			
		exit()
	
	results = []
	for arg in sys.argv[1:]:
		print(arg)
		with open(arg, 'r') as ifs:
			for line in walk(json.load(ifs)):
				tag = parser.parse(line)
				
				results.append([ line, tag ])

	if not results:
		exit()
		
	with open('test.json', 'w') as ofs:
		json.dump(results, ofs, indent=4, ensure_ascii=False)
