#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
An incomplete sample script.

This is not a complete bot; rather, it is a template from which simple
bots can be made. You can rename it to mybot.py, then edit it in
whatever way you want.

Use global -simulate option for test purposes. No changes to live wiki
will be done.

The following parameters are supported:

&params;

-always		   The bot won't ask for confirmation when putting a page

-text:			Use this text to be added; otherwise 'Test' is used

-replace:		 Dont add text but replace it

-top			  Place additional text on top of the page

-summary:		 Set the action summary message for the edit.
"""
#
# (C) Pywikibot team, 2006-2017
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals

import pywikibot
from pywikibot import pagegenerators
from pywikibot.bot import OptionHandler
from pywikibot import config, i18n

import os
import codecs
import string

from pywikibot.bot import (
	SingleSiteBot, ExistingPageBot, NoRedirectPageBot, AutomaticTWSummaryBot)
from pywikibot.tools import issue_deprecation_warning

# This is required for the text that is shown when you run this script
# with the parameter -help.
docuReplacements = {
	'&params;': pagegenerators.parameterHelp
}

class Singleton(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if (cls, args[0]) not in cls._instances:
			cls._instances[(cls, args[0])] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[(cls, args[0])]

class Entité(metaclass=Singleton):
	def __init__(self, nom, coordonnées):
		self._nom = nom
		self.coordonnées = coordonnées

	def nom(self):
		pass
	
	def gen(self, bot):
		pass
				
class Domaine(Entité):
	def __init__(self, nom, coordonnées = None):
		super(Domaine, self).__init__(nom, coordonnées)
		
		self.villes = {}
	
	def nom(self, suffixe = ''):
		if suffixe:
			suffixe = ' (' + suffixe + ')'
		
		if self._nom in self.villes:
			return self._nom + suffixe
		
		return self._nom
	
	def ajoutVille(self, ville):
		if ville._nom not in self.villes:
			self.villes[ville._nom] = ville
	
	def lettres(self):
		lettres = {}
		for ville in self.villes.keys():
			lettre = ville[0]
			
			if lettre not in lettres:
				lettres[lettre] = None
		
		return lettres
	
	def menu(self, lettres, préfixe = ''):
		if préfixe:
			préfixe += '/'
		
		menu = '<ul class="navigation alphabet">'
		for lettre in string.ascii_uppercase:
			if lettre in lettres:
				menu += '<li>[[' + préfixe + self._nom + '/' + lettre + '|' + lettre + ']]</li>'
			else:
				menu += '<li>' + lettre + '</li>'
		menu += '</ul>\n\n'
		
		return menu
	
	def gen(self, bot, préfixe = '', redirect = True):
		print()
		print(self.nom())
		
		lettres = self.lettres()
		menu = self.menu(lettres, préfixe if redirect else '')
		
		intro = menu
		
		if préfixe:
			modèle = préfixe
		else:
			modèle = self._nom
		
		intro += '{{' + modèle + '|' + self._nom
		if hasattr(self, 'région') and self.région:
			intro += '|région=' + self.région._nom
		if self.coordonnées:
			intro += '|coordonnées=' + ','.join(self.coordonnées)
		
		if préfixe and redirect:
			titre_page = préfixe + '/' + self._nom
		else:
			titre_page = self._nom
			
		page = pywikibot.Page(bot.site, titre_page)
		if not page.exists() or bot.getOption('force'):
			page.text = intro + '}}'
			
			if bot.getOption('vv'):
				print(page.text)
			page.save(summary='Création page ' + page.title())
		
		for lettre in lettres.keys():
			page_lettre = pywikibot.Page(bot.site, page.title() + '/' + lettre)
			
			if not page_lettre.exists() or bot.getOption('force'):
				texte = intro
				texte += '|catégories=false'
				texte += '}}'
				
				page_lettre.text = texte
				
				if bot.getOption('vv'):
					print(page_lettre.text)
				page_lettre.save(summary='Création sous-page ' + lettre + ' de ' + page.title())
		
		if redirect and page.title() != self.nom():
			if hasattr(self, 'région') or (self.provinces and not len(self.provinces)):
				redirection = pywikibot.Page(bot.site, self.nom())
				if not redirection.exists() or bot.getOption('force'):
					redirection.set_redirect_target(page.title(), create=True, force = True)
					
					if bot.getOption('vv'):
						print(redirection.text)
		
		catégorie = pywikibot.Category(bot.site, self.nom())
		if not catégorie.exists() or bot.getOption('force'):
			if préfixe:
				texte = '[[Catégorie:' + préfixe + ']] '
			else:
				texte = '[[Catégorie:' + self._nom + ']] '
			
			if hasattr(self, 'région') and self.région:
				texte += '[[Catégorie:' + self.région.nom() + ']]'
			catégorie.text = texte
			
			if bot.getOption('vv'):
				print(catégorie.text)
			catégorie.save(summary='Création catégorie ' + self.nom())


class Pays(Domaine):
	def __init__(self, pays, coordonnées = None):
		super(Pays, self).__init__(pays, coordonnées)
	
		self.provinces = {}
		self.régions = {}

	def ajoutProvince(self, province):
		if province not in self.provinces:
			self.provinces[province._nom] = None
	
	def ajoutRégion(self, région):
		if région not in self.régions:
			self.régions[région._nom] = None
		
	def gen(self, bot):
		if not bot.getOption('countryonly'):
			if bot.getOption('cityonly') or bot.getOption('provinceonly') or bot.getOption('regiononly'):
				return
		
		super(Pays, self).gen(bot, préfixe = 'Pays', redirect = False)
	
class Région(Domaine):
	def __init__(self, région, pays = None, coordonnées = None):
		super(Région, self).__init__(région, coordonnées)
		
		if pays:
			self.pays = Pays(pays)
			self.pays.ajoutRégion(région)
		
		self.provinces = {}
	
	def ajoutProvince(self, province):
		if province not in self.provinces:
			self.provinces[province._nom] = None
			
	def nom(self):
		return super(Région, self).nom('région')
	
	def gen(self, bot, préfixe = 'Région'):
		if not bot.getOption('regiononly'):
			if bot.getOption('cityonly') or bot.getOption('provinceonly') or bot.getOption('countryonly'):
				return
		
		super(Région, self).gen(bot, préfixe, not bot.getOption('noredirect'))

class Province(Domaine):
	def __init__(self, province, région, pays = None, coordonnées = None):
		super(Province, self).__init__(province, coordonnées)
		
		self.région = Région(région)
		self.région.ajoutProvince(self)
		
		if pays:
			self.pays = Pays(pays)
			self.pays.ajoutProvince(province)
			
	def nom(self):
		return super(Province, self).nom('province')
	
	def gen(self, bot, préfixe = 'Province'):
		if not bot.getOption('provinceonly'):
			if bot.getOption('cityonly') or bot.getOption('regiononly') or bot.getOption('countryonly'):
				return
		
		super(Province, self).gen(bot, préfixe, not bot.getOption('noredirect'))

class Ville(Entité):
	def __init__(self, ville, codepostal, province, région, pays = None, coordonnées = None):
		super(Ville, self).__init__(ville, coordonnées)
		
		self.codepostal = codepostal
		
		if province:
			self.province = Province(province, région)
			self.province.ajoutVille(self)
		else:
			self.province = None
		
		if région:
			self.région = Région(région)
			self.région.ajoutVille(self)
		else:
			self.région = None
			
		if région == 'Wallonie':
			self.langues = [ 'fr' ]
		elif région in [ 'Vlaanderen', 'Flandre' ]:
			self.langues = [ 'nl' ]
		else:
			self.langues = [ 'fr', 'nl' ]
			
		if pays:
			self.pays = Pays(pays)
			self.pays.ajoutVille(self)
		
	def nom(self):
		if self.province:
			return self.province.nom() + '/' + self._nom
		if self.région:
			return self.région.nom() + '/' + self._nom
		
		return self._nom
	
	def gen(self, bot):
		if not bot.getOption('cityonly'):
			if bot.getOption('provinceonly') or bot.getOption('regiononly') or bot.getOption('countryonly'):
				return
		
		print()
		print(self.nom())
		
		page = pywikibot.Page(bot.site, self.nom())
		if not page.exists() or bot.getOption('force'):
			texte = '{{Commune|' + self._nom
			if self.province:
				texte += '|province=' + self.province._nom
			if self.région:
				texte += '|région=' + self.région._nom
			texte += '|codepostal=' + self.codepostal
			texte += '|coordonnées=' + ','.join(self.coordonnées)
			texte += '|langue=' + ','.join(self.langues)
			texte += '}}'
			
			page.text = texte
			
			if bot.getOption('vv'):
				print(page.text)
			page.save(summary='Création commune ' + self.nom())		
		
		if not bot.getOption('noredirect'):
			redirection = pywikibot.Page(bot.site, self._nom)
			if not redirection.exists() or bot.getOption('force'):
				redirection.set_redirect_target(self.nom(), create = True, force = True)
				
				if bot.getOption('vv'):
					print(redirection.text)
		
		catégorie = pywikibot.Category(bot.site, self._nom)
		if not catégorie.exists() or bot.getOption('force'):
			texte = '[[Catégorie:Commune]] '
			
			if self.province:
				texte += '[[Catégorie:' + self.province.nom() + ']]'
			elif self.région:
				texte += '[[Catégorie:' + self.région.nom() + ']]'
				
			catégorie.text = texte
			
			if bot.getOption('vv'):
				print(catégorie.text)
			catégorie.save(summary='Création catégorie commune ' + self._nom)

class VillesBot(
	# Refer pywikobot.bot for generic bot classes
	SingleSiteBot,  # A bot only working on one site
	AutomaticTWSummaryBot,  # Automatically defines summary; needs summary_key
):

	"""
	An incomplete sample bot.

	@ivar summary_key: Edit summary message key. The message that should be used
		is placed on /i18n subdirectory. The file containing these messages
		should have the same name as the caller script (i.e. basic.py in this
		case). Use summary_key to set a default edit summary message.
	@type summary_key: str
	"""

	summary_key = 'This script generates a list of (Belgian) cities from an input file.'

	def __init__(self, generator, **kwargs):
		"""
		Constructor.

		@param generator: the page generator that determines on which pages
			to work
		@type generator: generator
		"""
		# Add your own options to the bot and set their defaults
		self.availableOptions.update({
			'force': False,
			'vv': False,
			'cityonly' : False,
			'provinceonly' : False,
			'regiononly' : False,
			'countryonly' : False,
			'country' : False,
			'noredirect' : False
		})

		# call constructor of the super class
		super(VillesBot, self).__init__(site=True, **kwargs)

		self.entités = {}
		
		pays = self.getOption('country')
		if pays:
			self.entités[pays] = Pays(pays)
		
		for codepostal, ville, province, région, lat, lon in generator:
			if ville:
				self.entités[ville] = Ville(ville, codepostal, province, région, pays)
				self.entités[ville].coordonnées = (lat, lon)
			elif province:
				self.entités[province] = Province(province, région, pays)
				self.entités[province].coordonnées = (lat, lon)
			elif région:
				self.entités[région] = Région(région, pays)
				self.entités[région].coordonnées = (lat, lon)
			
		# assign the generator to the bot
		self.generator = self.entités.values()
		
	def init_page(self, page):
		pass

	def treat(self, entité):
		"""Process page tuple, set page to current page and treat it."""
		entité.gen(self)
	

class PageFromFileReader(OptionHandler):
	"""Generator class, responsible for reading the file."""
	availableOptions = {}

	def __init__(self, filename, **kwargs):
		"""Constructor.

		Check if self.file name exists. If not, ask for a new filename.
		User can quit.

		"""
		super(PageFromFileReader, self).__init__(**kwargs)
		self.filename = filename

	def __iter__(self):
		"""Read file and yield a tuple of page title and content."""
		pywikibot.output('\n\nReading \'%s\'...' % self.filename)
		try:
			with codecs.open(self.filename, 'r', encoding=config.textfile_encoding) as f:
				for line in f:
					if line:
						yield [ x.strip() for x in line.split(',') ]
		except IOError as err:
			pywikibot.output(str(err))
			raise IOError

def main(*args):
	"""
	Process command line arguments and invoke bot.

	If args is an empty list, sys.argv is used.

	@param args: command line arguments
	@type args: list of unicode
	"""
	filename = "cities.csv"
	options = {}
	r_options = {}

	for arg in pywikibot.handle_args(args):
		arg, sep, value = arg.partition(':')
		option = arg.partition('-')[2]
		# reader options
		if option == 'file':
			filename = value
		elif option == 'force':
			options[option] = True
		elif option == 'noredirect':
			options['redirect'] = False
		elif option in ('vv', 'verbose'):
			options['vv'] = True
		elif option in ('cityonly', 'provinceonly', 'regiononly', 'countryonly'):
			options[option] = True
		elif option == 'country':
			options[option] = value
		elif option == 'noredirect':
			options[option] = True
		else:
			pywikibot.output(u"Disregarding unknown argument %s." % arg)

	failed_filename = False
	while not os.path.isfile(filename):
		pywikibot.output('\nFile \'%s\' does not exist. ' % filename)
		_input = pywikibot.input(
			'Please enter the file name [q to quit]:')
		if _input == 'q':
			failed_filename = True
			break
		else:
			filename = _input

	# The preloading option is responsible for downloading multiple
	# pages from the wiki simultaneously.
	if not failed_filename:
		gen = PageFromFileReader(filename, **r_options)
	if gen:
		bot = VillesBot(gen, **options)
		bot.run()  # guess what it does
		
		return True
	else:
		pywikibot.bot.suggest_help(missing_generator=True)
		return False


if __name__ == '__main__':
	main()
