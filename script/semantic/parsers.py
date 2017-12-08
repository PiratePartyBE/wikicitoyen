
import re

from datetime import datetime
from unidecode import unidecode

class Term:
	def __init__(self, regex):
		self.regex = regex
		self.values = {}
	
	def __repr__(self):
		return self.__class__.__name__ + ':' + self.regex.pattern.strip(r'\b')
	
	def findall(self, text):
		for m in self.regex.finditer(text):
			if not m:
				continue
			
			for value in self._parse(m):
				self.values[m.group()] = value
				
				yield (m, value)
	
	def _parse(self, m):
		yield m.group()
	
class FormatTerm(Term):
	def __init__(self, regex, fmt, ignorecase = True):
		if isinstance(regex, str):
			regex = re.compile(regex, re.I if ignorecase else 0)
		
		super(FormatTerm, self).__init__(regex)
		
		self.fmt = fmt
		
	def _parse(self, m):
		for value in self.fmt.split(','):
			value = value.split('-')
			
			for i, x in enumerate(value):
				j = int(x[1:])
				
				value[i] = m.group(j)
		
			value = self._process(value)
				
			if value:
				for x in self._join(value):
					yield x
				
	def _process(self, value):
		return value
	
	def _join(self, value):
		return value
	
class Intersect:
	def __init__(self, *terms):
		self.terms = [ term for term in terms if isinstance(term, Term) ]
		self.values = {}
		
	def findall(self, text):
		values = [ list(term.findall(text)) for term in self.terms ]
		
		if not all(values):
			return
		
		for value in values:
			for m, v in value:
				self.values[m.group()] = v
				yield (m, v)
	
class Word(Term):
	def __init__(self, regex):
		super(Word, self).__init__(re.compile(r'\b' + unidecode(regex) + r'\b', re.I))
	
class Acronym(Term):
	def __init__(self, regex, ignorecase = False):
		regex = unidecode(r'\.?'.join(regex))
		flag = re.I if ignorecase else 0
		
		super(Acronym, self).__init__(re.compile(r'\b' + regex + r'\b', flag))

class Date(FormatTerm):
	months = {
		'janvier' : 1,
		'fevrier' : 2,
		'mars' : 3,
		'avril' : 4,
		'mai' : 5,
		'juin' : 6,
		'juillet' : 7,
		'aout' : 8,
		'septembre' : 9,
		'octobre' : 10,
		'novembre' : 11,
		'decembre' : 12
	}
	
	def __init__(self, regex, fmt, ignorecase = True):
		super(Date, self).__init__(re.compile(r'\b' + regex + r'\b', re.I if ignorecase else 0), fmt)
		
	def _process(self, value):
		year, month, day = map(lambda x: int(x) if x.isdigit() else x, value)
		
		if isinstance(month, str):
			month = Date.months[month.lower()]
		
		if year < 100:
			year += 1900 if year > 50 else 2000
			
		try:
			date = datetime(year, month, day)
		except:
			return None
		
		return date
	
	def _join(self, value):
		yield format(value, '%Y-%m-%d')

class Trimester(Date):
	def __init__(self, regex, fmt, ignorecase = True):
		super(Trimester, self).__init__(regex, fmt, ignorecase)
		
		self.duration = 3
		
	def _process(self, value):
		n, year = map(lambda x: int(x) if x.isdigit() else x, value)

		if n > (12 // self.duration):
			return None
		
		month = (n * self.duration) - self.duration + 1
		day = 1

		try:
			date = datetime(year, month, day)
		except:
			return None
		
		return date
	
class Semester(Trimester):
	def __init__(self, regex, fmt, ignorecase = True):
		super(Semester, self).__init__(regex, fmt, ignorecase)
		
		self.duration = 6

class Quadrimester(Trimester):
	def __init__(self, regex, fmt, ignorecase = True):
		super(Quadrimester, self).__init__(regex, fmt, ignorecase)
		
		self.duration = 4
		
class Number(FormatTerm):
	ordinals = {
		'premier' : 1,
		'premiere' : 1,
		'deuxieme' : 2,
		'troisieme' : 3,
		'quatrieme' : 4,
		'cinquieme' : 5,
		'sixieme' : 6
	}
	
	romans = {
		'i' : 1,
		'ii' : 2,
		'iii' : 3,
		'iv' : 4,
		'v' : 5,
		'vi' : 6
	}
	
	def __init__(self, regex, fmt = '%1', ignorecase = True):
		super(Number, self).__init__(re.compile(regex, re.I if ignorecase else 0), fmt)
		
	def _process(self, value):
		for x in value:
			x = x.replace('.', '').replace(',', '.')
			
			if x.isdigit():
				yield int(x)
			elif x.replace('.', '').isdigit():
				yield(float(x))
			elif x.lower() in Number.ordinals:
				yield Number.ordinals[x.lower()]
			elif x.lower() in Number.romans:
				yield Number.romans[x.lower()]
			else:
				yield x

class Year(Number):
	def __init__(self, regex, fmt = '%1', ignorecase = True):
		super(Year, self).__init__(regex, fmt, ignorecase)
	
	def _process(self, value):
		for x in value:
			if not x.isdigit():
				continue
			
			x = int(x)
			
			if x < 1800:
				continue
			
			yield x

class Range(Year):
	def __init__(self, regex, fmt = '%1-%2', ignorecase = True):
		super(Range, self).__init__(regex, fmt, ignorecase)
	
	def _process(self, value):
		start, end = super(Year, self)._process(value)
		
		if start >= end:
			return None
		
		if end - start > 6:
			return None
		
		for x in range(start, end+1):
			yield x
