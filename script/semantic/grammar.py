from parsers import *

rules = [
	{ "value" : "digit" },
	{
		"type" : "digit",
		"erase" : False,
		"terms" : [
			Number(r"(?:ndeg|numeros?) *(\d|I)\b"),
			Number(r"\b(\d|I) ?(?:er|eme|e)\b"),
			Number(r"(" + r'|'.join(Number.ordinals) + r")")
		]
	},
	{
		"type" : "digit",
		"replace" : False,
		"terms" : [
			Number(r"\b(\d)[-/]\d{4}"),
			Number(r"\d{4}/(\d)\b"),
		]
	},
		
	{ "value" : "document" },
	{ 
		"type" : "document", 
		"value" : "Procès verbal", 
		"terms" : [ Word("Procès verbal"), Word("Procès verbaux"), Word("Procès-verbal"), Word("Procès-verbaux"), Acronym("PV") ],
		"children" : { ("type", "date") },
		"disjoin" : { "Procès verbal" }
	},
	{
		"type" : "document",
		"value" : "Procès verbal",
		"terms" : [ Word("Vérification") ],
		"intersect" : { "Procès verbal" }
	},
	{
		"type" : "document",
		"value" : "Contrat-Programme",
		"terms" : [ Word("Contrat-Programme"), Word("Contrat Programme") ],
		"children" : { ("type", "year") }
	},
	{
		"type" : "document",
		"value" : "Programme CLE",
		"terms" : [ Intersect(Word("Programme"), Acronym("CLE")), Word("Coordination Locale pour l'Enfance"), Word("Programme de Coordination de l'Enfance") ],
		"children" : { ("type", "year") }
	},
	{
		"type" : "document",
		"value" : "Plan d'alignement",
		"terms" : [ Word("Plans? d'alignements?") ]
	},
	{
		"type" : "document",
		"value" : "PCDR",
		"terms" : [ Acronym("PCDR"), Word("Programme Communal de Développement Rural") ]
	},
	{
		"type" : "document",
		"value" : "Permis d'urbanisme",
		"terms" : [ Word("Permis d'urbanisme"), Word("Permis d'urbanisation") ],
		"children" : { ("type", "number"), ("type", "year") }
	},
	{
		"type" : "document",
		"value" : "ROI",
		"terms" : [ Acronym("ROI"), Word("Règlement d'ordre intérieur"), Word("Règlements d'ordre intérieur") ],
		"children" : { ("type", "article") }
	},
	{
		"type" : "document",
		"value" : "Coût-Vérité",
		"terms" : [ Word("Coût-Vérité"), Word("Coût Vérité") ]
	},
	{
		"type" : "document",
		"value" : "Plan stratégique",
		"terms" : [ Word("Plan stratégique"), Word("Plans stratégiques") ]
	},
	{
		"type" : "document",
		"value" : "PCS",
		"terms" : [ Word("Plan de cohésion sociale"), Word("Plans de cohésion sociale"), Word("Plan de cohésion social"), Acronym("PCS") ],
		"children" : { ("type", "year"), "Rapport" }
	},
	{
		"type" : "document",
		"value" : "UREBA",
		"terms" : [ Acronym("UREBA"), Word("Rénovation énergétique des bâtiments") ],
		"children" : { ("type", "percent") }
	},
	{
		"type" : "document",
		"value" : "Plan de mobilité",
		"terms" : [ Word("Plan communal de mobilité"), Word("Plans communaux de mobilité"), Word("Plans? de mobilité") ]
	},
	
	{ "value" : "market" },
	{
		"type" : "market",
		"value" : "Cahier des charges",
		"terms" : [ 
			Word("Cahier des charges"),
			Word("Cahiers des charges"),
			Word("Cahier de charges"),
			Word("Cahiers des charges"),
			Word("Cahier spécial des charges"),
			Word("Cahiers spéciaux des charges"),
			Word("Cahier spécial de charges"),
			Word("Cahiers spéciaux de charges"),
		]
	},
	{
		"type" : "market",
		"value" : "Mode de Marché",
		"terms" : [ Word("Mode de marché"), Word("Modes de marché"), Word("Mode de passation"), Word("Modes de passation") ],
		"children" : { "Cahier des charges" }
	},
	{
		"type" : "market",
		"value" : "Marché de fournitures",
		"terms" : [ 
			Word("Marchés? de fournitures?"), 
			Word("Marchés? publics? de fournitures?"),
		],
		"children" : { "Cahier des charges", "Mode de Marché" }
	},
	{
		"type" : "market",
		"value" : "Marché de services",
		"terms" : [
			 Word("Marchés? publics? de services?"), 
			 Word("Marchés? de services?")
		],
		"children" : { "Cahier des charges", "Mode de Marché" }
	},
	{
		"type" : "market",
		"value" : "Marché Public",
		"terms" : [ Word("Marché public"), Word("Marchés publics") ],
		"children" : { "Cahier des charges", "Mode de Marché", "Marché de fournitures", "Marché de services" }
	},
	{
		"type" : "market",
		"value" : "Marché de travaux",
		"terms" : [ Word("Marché de travaux"), Word("Marchés de travaux") ],
		"children" : { "Cahier des charges", "Mode de Marché" }
	},

	{ "value" : "law" },
	{
		"type" : "law",
		"value" : "Arrêté Royal", 
		"terms" : [ Word("Arrêté Royal"), Word("Arrêtés Royaux") ],
		"children" : { ("type", "date") }
	},
	{
		"type" : "law",
		"value" : "Arrêté Ministériel", 
		"terms" : [ Word("Arrêté Ministériel"), Word("Arrêtés Ministériels") ],
		"children" : { ("type", "date") }
	},
	{ 
		"type" : "law",
		"value" : "Arrêté wallon",
		"terms" : [ Word("Arrêté du Gouvernement wallon"), Word("Arrêtés du Gouvernement wallon") ],
		"children" : { ("type", "date"), ("type", "article") }
	},
	{
		"type" : "law",
		"value" : "Décret",
		"terms" : [ Word("Décrêt") ],
		"children" : { ("type", "date"), ("type", "article") }
	},
	{
		"type" : "law",
		"value" : "Ordonnance",
		"terms" : [ Word("Ordonnances? de Police") ]
	},
	{
		"type" : "law",
		"value" : "Amende",
		"terms" : [ 
			Word("Amendes? administratives?"), 
			Word("Sanctions? administrativess? communales?"), 
			Word("Sanctions? administrativess?")
		],
		"children" : { "Stationnement" }
	},
	{
		"type" : "law",
		"value" : "Loi",
		"terms" : [ Word("Loi"), Word("Lois") ],
		"children" : { ("type", "date"), ("type", "article") }
	},
	{
		"type" : "law",
		"value" : "Règlement de vente",
		"terms" : [ Word("Règlement de vente"), Word("Règlements de vente") ],
	},
	{
		"type" : "law", 
		"value" : "RCCR",
		"terms" : [ 
			Word("Règlement complémentaire de roulage"), 
			Word("Règlements complémentaires de roulage"), 
			Word("Règlement communal complémentaire"),
			Word("Règlements communaux complémentaires"),
			Word("Règlement général de police"),
			Word("Règlements généraux de police"),
			Word("Circulation routière"),
			Word("Règlement complémentaire"),
			Word("Règlements complémentaires"),
			Acronym("RCCR")
		],
		"children" : { "Parking", "Stationnement" }
	},
	{
		"type" : "law",
		"value" : "Règlement d'urbanisme",
		"terms" : [ Word("Règlement d'urbanisme") ],
	},
	{
		"type" : "law",
		"value" : "Règlement communal",
		"terms" : [ Word("Règlement communal"), Word("Règlements communaux") ]
	},
	{
		"type" : "law",
		"value" : "Redevance",
		"terms" : [ Intersect(Word("Règlement"), Word("Redevance")) ]
	},
	{
		"type" : "law",
		"value" : "Recours",
		"terms" : [ Word("Recours") ]
	},
	{
		"type" : "law",
		"value" : "CoDT",
		"terms" : [ Acronym("CoDT"), Word("Code du Développement Territorial") ]
	},
	{
		"type" : "law",
		"value" : "CDLD",
		"terms" : [ 
			Acronym("CDLD"), 
			Word("Code de la Démocratie Locale et de la Décentralisation"), 
			Word("Code wallon de la Démocratie Locale et de la Décentralisation"),
			Word("Code de la Démocratie Locale") 
		],
		"children" : { ("type", "cdld") }
	},
	{
		"type" : "law",
		"value" : "CWATUP",
		"terms" : [ 
			Acronym("CWATUP")
		],
		"children" : { ("type", "article") }
	},
	{
		"type" : "law",
		"value" : "CWADEL",
		"terms" : [ 
			Acronym("CWADEL")
		],
		"children" : { ("type", "cdld") }
	},
	{
		"type" : "law",
		"value" : "RGCR",
		"terms" : [ 
			Acronym("RGCR")
		],
		"children" : { ("type", "article") }
	},
	{
		"type" : "law",
		"value" : "RGCC",
		"terms" : [ 
			Acronym("RGCC")
		],
		"children" : { ("type", "article") }
	},
	
	{ "value" : "cdld" },
	{
		"type" : "cdld",
		"terms" : [ 
			Number(r"\bart(?:\.|icles?) (\d{4}-\d{1,2})\b"),
			Number(r"\b(?:art(?:\.|icles?) )?(L ?\d{4}-\d{1,2})\b")
		]
	},
	{ "value" : "article" },
	{
		"type" : "article",
		"terms" : [ 
			FormatTerm(r"\bart(?:\.|icles?) (\d+\.[\.\da-z]+)\b", '%1'),
			Number(r"\bart(?:\.|icles?) (\d+)\b")
		]
	},
	
	
	{ "value" : "finance" },
	{
		"type" : "finance",
		"value" : "Trésorerie",
		"terms" : [ 
			Word("Trésorerie"), 
			Word("Caisses?"), 
			Word("Encaisse"),
			Intersect(Word("États?"), Word("Recettes?"), Word("Dépenses?"))
		],
		"children" : { "Procès verbal", ("type", "year"), ("type", "date") },
		"disjoin" : { "Comptes" }
	},
	{
		"type" : "finance",
		"value" : "Modification budgétaire",
		"terms" : [ Word("Modifications? budgétaires?") ],
		"children" : { ("type", "digit"), ("type", "year"), ("type", "date") }
	},
	{
		"type" : "finance",
		"value" : "Budget",
		"terms" : [ Word("Budgets"), Word("Budget") ],
		"children" : { ("type", "year"), ("type", "date"), "Modification budgétaire" }
	},
	{
		"type" : "finance",
		"value" : "Modification budgétaire",
		"terms" : [ Word("Révisions?"), Word("Modifications?") ],
		"children" : { ("type", "digit"), ("type", "year"), ("type", "date") },
		"intersect" : { "Budget" }
	},
	{
		"type" : "other",
		"terms" : [ Word("Compte tenu"), Word("Prises? en compte") ],
		"intersect" : { "" }
	},
	{
		"type" : "other",
		"value" : "Contrôleur aux Comptes",
		"terms" : [ Word("Contrôleurs? aux Comptes"), Word("Commissaires? aux Comptes") ],
		"intersect" : { "" }
	},
	{
		"type" : "finance",
		"value" : "Comptes",
		"terms" : [ Word("Comptes"), Word("Compte") ],
		"children" : { ("type", "year"), ("type", "date"), ("type", "money"), ("type", "tva") }
	},
	{
		"type" : "finance",
		"value" : "Subside",
		"terms" : [ Word("Subsides?"), Word("Subsidiés?"), Word("Subventions?"), Word("Subventionnement") ],
		"children" : { "UREBA", ("type", "money"), ("type", "tva"), "Dépense" }
	},
	{
		"type" : "finance",
		"value" : "Dotation",
		"terms" : [ Word("Dotations?") ],
		"children" : { ("type", "year") }
	},
	{
		"type" : "finance",
		"value" : "Dépense",
		"terms" : [ Word("Dépenses?") ],
		"children" : { ("type", "money"), ("type", "tva") },
		"disjoin" : { "Comptes", "Budget", "Modification budgétaire" }
	},
	{
		"type" : "finance",
		"value" : "Cotisation",
		"terms" : [ Word("Cotisations?") ],
		"children" : { ("type", "money"), ("type", "tva"), ("type", "year") }
	},
	{
		"type" : "finance",
		"value" : "Prêt CRAC",
		"terms" : [ Word("Prêt") ],
		"intersect" : { 'CRAC' }
	},
	{
		"type" : "finance",
		"replace":False,
		"value" : "Rapport",
		"terms" : [ Intersect(Word("Rapport"), Word("Financier")) ],
		"children" : { ("type", "year") }
	},
	{
		"type" : "document",
		"value" : "Rapport",
		"terms" : [ Word("Rapports? d'activités?"), Word("Rapports? de gestions?") ],
		"children" : { ("type", "year") }
	},
	{
		"type" : "document",
		"value" : "Rapport",
		"terms" : [ Word("Rapports? annuels?") ],
		"children" : { ("type", "year") },
		"disjoin" : { "Rapport" }
	},
	
	{ "value" : "route" },
	{
		"type" : "route",
		"value" : "RER",
		"terms" : [ Acronym("RER"), Word("Réseau Express Régional") ]
	},
	{
		"type" : "route",
		"value" : "Proxibus",
		"terms" : [ Word("Proxibus") ]
	},
	{
		"type" : "route",
		"value" : "Stationnement",
		"terms" : [ Word("Stationnements?"), Word("Emplacements?"), Word("Zones? Bleues?") ],
		"children" : { "PMR", "Voiture partagée" },
		"disjoin" : { "Cimetière" }
	},
	{
		"type" : "route",
		"value" : "Parking",
		"terms" : [ Word("Parkings?") ],
		"children" : { "PMR", "Voiture partagée", "Stationnement" }
	},
	{
		"type" : "route",
		"value" : "Voiture partagée",
		"terms" : [ Word("Voitures? partagées?"), Word("car ?- ?sharing") ]
	},
	{
		"type" : "route",
		"value" : "Voirie",
		"terms" : [ Word("Voiries?") ]
	},
	
	{ "value" : "person" },
	{
		"type" : "person",
		"value" : "PMR",
		"terms" : [ 
			Acronym("PMR"), 
			Word("Personnes? à Mobilité Réduite"), 
			Word("Personnes? handicapées?"),
			Word("Handicapé"),
			Word("Handicapés"),
			Word("Mobilité réduite"),
			Word("Personnes? atteintes? d'un handicap")
		]
	},
	{
		"type" : "person",
		"value" : "Primo-arrivant",
		"terms" : [ Word("Primo-arrivants?") ]
	},
	{
		"value" : "entity",
		"children" : { ("type", "finance"), ("type", "document"), ("type", "market"), "Parking" }
	},
	
	{
		"type" : "entity",
		"value" : "SPW",
		"terms" : [ Word("Service Public de Wallonie"), Acronym("SPW") ]
	},
	{
		"type" : "entity",
		"value" : "Conseil d'État",
		"terms" : [ Word("Conseil d'État") ],
		"children" : { "Recours" }
	},
	
	{
		"value" : "asbl",
		"union" : { 'ASBL' },
		"children" : { "Subside", "Dotation", "Cotisation", ("type", "document"), ("type", "market"), "Parking" }
	},
	{
		"type" : "asbl",
		"value" : "ASBL",
		"terms" : [ Acronym("ASBL", ignorecase=True), Word("Association Sans But Lucratif") ]
	},
	{
		"type" : "régie",
		"value" : "Maison des Sports",
		"replace" : False,
		"terms" : [ 
			Word("Maisons? des Sports")
		]
	},
	{
		"type" : "asbl",
		"value" : "Maison des Sports",
		"terms" : [ 
			Word("Maisons? des Sports")
		],
		"intersect" : { "ASBL" },
		"union" : { "Maison des Sports" },
		"children" : { "Location", "Logement" }
	},
	{
		"type" : "asbl",
		"value" : "Maison des Sports",
		"terms" : [ 
			Word("Centres? sportifs?"), 
			Word("Complexes? sportifs?"), 
			Word("Halls? des sports"), 
			Word("Chalets? des Sports"),
			Word("Omnisports?")
		],
		"children" : { "Location", "Logement" }
	},
	
	{
		"type" : "asbl",
		"value" : "TV Com",
		"terms" : [ 
			Word("TV Com")
		]
	},
	{
		"type" : "asbl",
		"value" : "Immeubles en Fête",
		"terms" : [ 
			Word("Immeubles? en Fête")
		]
	},
	
	{
		"type" : "entity",
		"value" : "Commission Européenne",
		"terms" : [ Word("Commission Européenne") ]
	},
	
	{
		"value" : "commission",
		"children": { "Rapport" }
	},
	{
		"type" : "council",
		"value" : "CCATM",
		"terms" : [ 
			Acronym("CCATM"), 
			Word("Aménagement du Territoire et de Mobilité"),
			Word("Aménagement du Territoire et de la Mobilité"),
			Intersect(Word("Aménagement du Territoire"), Word("Mobilité"))
		],
		"intersect" : { "Conseil Consultatif", "Commission" },
		"union" : { "Conseil Consultatif", "Commission" }
	},
	{
		"type" : "commission",
		"value" : "Inondations",
		"terms" : [ Word("Inondations?") ],
		"intersect" : { "Commission" },
		"union" : { "Commission" }
	},
	{
		"type" : "commission",
		"replace" : False,
		"value" : "Économie",
		"terms" : [ Word("Économie") ],
		"intersect" : { "Commission" },
		"union" : { "Commission" }
	},
	{
		"type" : "commission",
		"replace" : False,
		"value" : "Mobilité",
		"terms" : [ Word("Mobilité") ],
		"intersect" : { "Commission" },
		"union" : { "Commission" }
	},
	{
		"type" : "commission",
		"value" : "COPALOC",
		"terms" : [ Intersect(Word("Paritaire Locale"), Word("Enseignement")), Word("Paritaire Locale"), Acronym("COPALOC") ],
		"intersect" : { "Commission" },
		"union" : { "Commission" }
	},
	{
		"type" : "commission",
		"replace" : False,
		"value" : "Enseignement",
		"terms" : [ Word("Enseignement") ],
		"intersect" : { "Commission" },
		"union" : { "Commission" }
	},
	{
		"type" : "commission",
		"value" : "Tiers-Monde",
		"terms" : [ Word("Tiers-Monde") ],
		"intersect" : { "Commission" },
		"union" : { "Commission" }
	},
	{
		"type" : "commission",
		"value" : "Travaux",
		"replace" : False,
		"terms" : [ Word("Travaux") ],
		"intersect" : { "Commission" },
		"union" : { "Commission", "Travaux" }
	},
	{
		"type" : "commission",
		"replace" : False,
		"value" : "Finance",
		"terms" : [ Word("Finances?") ],
		"intersect" : { "Commission" },
		"union" : { "Commission", "Finance" }
	},
	{
		"type" : "commission",
		"value" : "CLDR",
		"terms" : [ Word("Locale de Développement Rural"), Acronym("CLDR") ],
		"intersect" : { "Commission" },
		"union" : { "Commission" }
	},
	{
		"type" : "commission",
		"value" : "CRU",
		"terms" : [ Word("Rénovation Urbaine"), Acronym("CRU") ],
		"intersect" : { "Commission" },
		"union" : { "Commission" }
	},
	{
		"type" : "commission",
		"replace" : False,
		"value" : "Environnement",
		"terms" : [ Word("Environnement") ],
		"intersect" : { "Commission" },
		"union" : { "Commission", "Environnement" }
	},
	{
		"type" : "council",
		"replace" : False,
		"value" : "Jeunesse et Sports",
		"terms" : [ Intersect(Word("Jeunesse"), Word("Sports")) ],
		"intersect" : { "Conseil Consultatif" },
		"union" : { "Conseil Consultatif" }
	},
	{
		"type" : "commission",
		"value" : "Jeunesse et Sports",
		"terms" : [ Intersect(Word("Jeunesse"), Word("Sports")) ],
		"intersect" : { "Commission" },
		"union" : { "Commission" }
	},
	{
		"type" : "commission",
		"value" : "CCA",
		"terms" : [ Word("Accueil"), Acronym("CCA") ],
		"intersect" : { "Commission" },
		"union" : { "Commission" }
	},
	{
		"type" : "commission",
		"value" : "CLE",
		"terms" : [ Word("Locale pour l'Énergie"), Acronym("CLE") ],
		"intersect" : { "Commission" },
		"union" : { "Commission" }
	},
	
	{ 
		"parent" : "entity",
		"value" : "council" 
	},
	{
		"type" : "council",
		"value" : "Conseil Consultatif",
		"terms" : [ Word("Conseils? Consultatifs?"), Word("Commissions? Consultatives?"), Word("Comités? Consultatifs?") ],
		"children" : { "PMR" }
	},
	{
		"type" : "commission",
		"value" : "Commission",
		"terms" : [ Word("Commissions?") ]
	},
	{
		"type" : "council",
		"value" : "Affaires sociales et Assuétudes",
		"terms" : [ Word("Affaires sociales et Assuétudes") ],
		"union" : { "Conseil Consultatif" }
	},
	{
		"type" : "council",
		"value" : "Cinéma",
		"terms" : [ Word("7 Arts?") ],
		"union" : { "Conseil Consultatif" },
		"intersect" : { "Conseil Consultatif" }
	},
	{
		"type" : "council",
		"replace" : False,
		"value" : "Culture",
		"terms" : [ Word("Culture") ],
		"union" : { "Conseil Consultatif" },
		"intersect" : { "Conseil Consultatif" }
	},
	{
		"type" : "commission",
		"value" : "Culture",
		"terms" : [ Word("Culture") ],
		"union" : { "Commission" },
		"intersect" : { "Commission" }
	},
	{
		"type" : "council",
		"value" : "Jeunesse",
		"terms" : [ Word("Jeunesses?") ],
		"union" : { "Conseil Consultatif" },
		"intersect" : { "Conseil Consultatif" }
	},
	{
		"type" : "council",
		"value" : "Numérique",
		"terms" : [ Word("Numérique") ],
		"union" : { "Conseil Consultatif" },
		"intersect" : { "Conseil Consultatif" }
	},
	{
		"type" : "council",
		"value" : "Sports",
		"terms" : [ Word("Sports") ],
		"union" : { "Conseil Consultatif" },
		"intersect" : { "Conseil Consultatif" }
	},
	{
		"type" : "council",
		"value" : "Économie",
		"terms" : [ Word("Économie") ],
		"union" : { "Conseil Consultatif" },
		"intersect" : { "Conseil Consultatif" }
	},
	{
		"type" : "council",
		"value" : "Emploi",
		"terms" : [ Word("Emploi") ],
		"union" : { "Conseil Consultatif" },
		"intersect" : { "Conseil Consultatif" }
	},
	{
		"type" : "council",
		"value" : "Mobilité",
		"terms" : [ Word("Mobilité") ],
		"union" : { "Conseil Consultatif" },
		"intersect" : { "Conseil Consultatif" }
	},
	{
		"type" : "council",
		"value" : "CCCA",
		"terms" : [ Word("Ainés"), Acronym("CCCA") ],
		"union" : { "Conseil Consultatif" },
		"intersect" : { "Conseil Consultatif" }
	},
	
	{
		"parent" : "entity",
		"value" : "intercommunale",
		"children" : { 'Assemblée Générale' }
	},
	{
		"type" : "intercommunale",
		"value" : "CRIBW",
		"terms" : [ 
			Acronym("CRIBW"), 
			Word("Centre Régional d'Intégration du Brabant Wallon"),
			Word("Centre d'Intégration Sociale du Brabant Wallon")
		],
		"children" : { "Primo-arrivant" }
	},
	{
		"type" : "intercommunale",
		"value" : "SPGE",
		"terms" : [ 
			Acronym("SPGE"), 
			Word("Société Publique de Gestion de l'Eau")
		]
	},
	{
		"type" : "intercommunale",
		"value" : "Conseil 27+1",
		"terms" : [ Word("Conseil 27 ?\+ ?1") ]
	},
	{
		"type" : "intercommunale",
		"value" : "Inter-Régies",
		"terms" : [ Word("Inter ?- ?Régies?") ]
	},
	{
		"type" : "entity",
		"value" : "CPAS",
		"terms" : [ 
			Acronym("CPAS"), 
			Word("Centre Public d'Action Sociale"),
			Word("Centre Public d'Aide Sociale") 
		]
	},
	{
		"type" : "intercommunale",
		"value" : "IBW",
		"terms" : [ Acronym("IBW"), Word("Intercommunale du Brabant Wallon") ]
	},
	{
		"type" : "intercommunale",
		"value" : "IMIO",
		"terms" : [ 
			Acronym("IMIO"), 
			Word("Intercommunale de Mutualisation en Matière Informatique et Organisationnelle"), 
			Word("Intercommunale de Mutualisation en Matière d'Informatique et Organisationnelle") 
		],
		"union" : { "SCRL" }
	},

	{
		"parent" : "entity",
		"value" : "régie",
		"union" : { "Régie" }
	},
	{
		"type" : "régie",
		"replace" : False,
		"value" : "Régie",
		"terms" : [ Word("Régies? Communales? Autonomes?"), Word("Régies? Autonomes?"), Acronym("RCA") ]
	},
	{
		"type" : "régie",
		"value" : "OTP",
		"terms" : [ Acronym("OTP"), Word("Office du Tourisme et du Patrimoine") ]
	},
	{
		"type" : "régie",
		"value" : "RDI",
		"terms" : [ Acronym("RDI"), Word("Régie des Infrastructures") ],
		"children" : { ("type", "building") }
	},
	{
		"type" : "régie",
		"value" : "Régie Foncière Provinciale",
		"terms" : [ Word("Régie Foncière Provinciale autonome") ],
		"children" : { ("type", "building") }
	},
	{
		"type" : "régie",
		"value" : "Régie de l'Électricité",
		"terms" : [ Word("Régie de l'Électricité") ]
	},
	{
		"type" : "régie",
		"value" : "RFI",
		"terms" : [ Acronym("RFI"), Word("Régie Foncière et Immobilière"), Word("Régie foncière") ],
		"union" : { "Régie" },
		"children" : { ("type", "building") }
	},
	{
		"type" : "asbl",
		"value" : "Régie des Quartiers",
		"terms" : [ Word("Régies? des Quartiers"), Word("Régies? d[ue] Quartier") ],
		"union" : { "Régie" }
	},
	{
		"type" : "intercommunale",
		"value" : "SARSI",
		"terms" : [ Acronym("SARSI") ]
	},
	{
		"type" : "intercommunale",
		"value" : "SEDIFIN",
		"terms" : [ Acronym("SEDIFIN", ignorecase = True) ],
		"union" : { "SCRL" }
	},
	{
		"type" : "intercommunale",
		"value" : "PUBLIFIN",
		"terms" : [ Acronym("Publifin Scirl", ignorecase = True), Acronym("PUBLIFIN", ignorecase = True) ]
	},
	{
		"type" : "entity",
		"value" : "TEC",
		"terms" : [ Acronym("TEC"), Word("Société de Transports en Commun"), Word("Société des Transports en Commun") ],
		"children" : { "Proxibus" }
	},
	{
		"type" : "entity",
		"value" : "SNCB",
		"terms" : [ Acronym("SNCB", ignorecase=True) ]
	},
	{
		"type" : "intercommunale",
		"value" : "Vivaqua",
		"terms" : [ Word("Vivaqua"), Word("HydroBru") ],
		"union" : { "SPRL" }
	},
	{
		"type" : "entity",
		"value" : "Piscine",
		"terms" : [ Word("Piscines?") ]
	},
	{
		"type" : "entity",
		"value" : "Hôpital",
		"terms" : [ Word("Hôpital"), Word("Hôpitaux"), Word("Centres? Hospitaliers?") ],
		"children" : { "CHIREC" }
	},
	{
		"type" : "asbl",
		"value" : "CHIREC",
		"terms" : [ Word("Chirec") ]
	},
	{
		"type" : "entity",
		"value" : "CAMBIO",
		"terms" : [ Acronym("CAMBIO", ignorecase=True) ]
	},
	{
		"type" : "entity",
		"value" : "UCL",
		"terms" : [ Acronym("UCL") ]
	},
	{
		"type" : "entity",
		"value" : "Bpost",
		"terms" : [ Word("Bpost") ]
	},
	{
		"type" : "intercommunale",
		"value" : "ORES",
		"terms" : [ Acronym("ORES", ignorecase = True), Word("Opérateur des Réseaux Gaz et Électricité") ]
	},
	{
		"type" : "intercommunale",
		"value" : "ISBW", 
		"terms" : [ Acronym("ISBW"), Word("Intercommunale Sociale du Brabant Wallon") ]
	},
	{
		"type" : "intercommunale",
		"value" : "IECBW", 
		"terms" : [ Acronym("IECBW"), Word("Intercommunale des Eaux du Centre du Brabant Wallon") ]
	},
	
	{
		"type" : "asbl",
		"value" : "CCBW",
		"terms" : [ Acronym("CCBW"), Word("Centre Culturel du Brabant Wallon") ],
		"children" : { "Assemblée Générale" }
	},
	{
		"type" : "asbl",
		"value" : "Association des Habitants",
		"terms" : [ Acronym("AH"), Word("Association des Habitants") ]
	},
	{
		"type" : "asbl",
		"value" : "UVCW",
		"terms" : [ Acronym("UVCW"), Word("Union des Villes et des Communes de Wallonie"), Word("Union des Villes et Communes de Wallonie") ]
	},
	
	{
		"parent" : "entity",
		"value" : "scrl",
		"children" : { "Assemblée Générale" },
		"union" : { "SCRL" }
	},
	{
		"type" : "scrl",
		"value" : "SCRL",
		"terms" : [ Acronym("SCRL", ignorecase=True) ]
	},
	{
		"type" : "asbl",
		"value" : "Maison du Tourisme Roman Païs",
		"terms" : [ 
			Word("Maison d[ue] Tourisme d[ue] Roman Païs"), 
			Word("Maison d[ue] Tourisme Roman Païs")
		]
	},
	{
		"type" : "scrl",
		"value" : "Notre Maison",
		"terms" : [ Word("Notre Maison") ],
		"children" : { "Logement" },
		"union" : { "Régie des Quartiers" }
	},
	{
		"type" : "scrl",
		"value" : "Roman Païs",
		"terms" : [ Word("Habitations Sociales du Roman Païs"), Word("Habitations Sociales Roman Païs"), Word("Habitations Sociales"), Word("Roman Païs") ]
	},
	{
		"type" : "entity",
		"value" : "Église",
		"terms" : [ 
			Word("Fabriques? d'Église"), 
			Word("Églises?"), 
			Word("Conseils? de fabriques?"), 
			Word("Bâtiments? d[ue] Culte")
		]
	},
	{
		"type" : "scrl",
		"value" : "Académie Intercommunale de Musique",
		"terms" : [ Word("Académie Intercommunale de Musique") ]
	},
	{
		"type" : "entity",
		"value" : "Académie de Musique",
		"terms" : [ Word("Académie de Musique"), Word("Académies de Musique") ]
	},
	{ 
		"type" : "entity", 
		"value" : "École des Arts",
		"terms" : [ Word("École des Arts") ]
	},
	{ 
		"type" : "entity",
		"value" : "Centre Culturel",
		"terms" : [ Word("Centre Culturel"), Word("Centres Culturels"), Word("Espace Culturel"), Word("Espaces Culturels") ],
		"union" : { "ASBL" },
		"children": { "Stationnement", "Location" }
	},
	{
		"type" : "entity",
		"value" : "Maison du Tourisme",
		"terms" : [ Word("Maison du Tourisme"), Word("Maison de Tourisme"), Word("Office du Tourisme"), Word("Office de Tourisme") ]
	},
	{
		"type" : "entity",
		"value" : "École",
		"terms" : [ 
			Word("Écoles?"), 
			Word("Instituteurs?"), 
			Word("Institutrices?"),
			Word("Enseignement communal"), 
			Word("Enseignement fondamental"),
			Word("Institeurs?"),
			Word("Institutrices?"),
			Word("Maîtresses?"),
			Word("Enseignante?s?")
		],
		"children" : { "Location" }
	},
	{
		"type" : "entity",
		"value" : "École",
		"terms" : [
			Word("Maîtres?")
		],
		"disjoin" : { "Église" }
	},
	{
		"type" : "entity",
		"value" : "Plaine de jeux",
		"terms" : [ Word("Plaines? de jeux") ]
	},
	{
		"type" : "entity",
		"value" : "Bibliothèque",
		"terms" : [ Word("Bibliothèque"), Word("Bibliothèques") ]
	},
	{
		"type" : "entity",
		"value" : "Cimetière",
		"terms" : [ Word("Cimetière"), Word("Cimetières") ],
	},
	{
		"type" : "entity",
		"value" : "Zone de Police",
		"terms" : [ Word("Zone de Police"), Word("Zones de Police"), Acronym("ZP") ],
		"children" : { ("type", "number") }
	},
	{
		"type" : "entity",
		"value" : "Zone de Secours",
		"terms" : [ Word("Zone de Secours"), Word("Zones de Secours") ]
	},
	{
		"type" : "scrl",
		"value" : "Bataille de Waterloo 1815",
		"terms" : [ Word("Bataille de Waterloo 1815") ],
		"union" : { "SCRL" }
	},
	{
		"type" : "entity",
		"value" : "ZIT",
		"terms" : [ Acronym("ZIT"), Word("Zone d'immersion temporaire"), Word("Zones d'immersion temporaire") ]
	},
	{
		"type" : "entity",
		"value" : "CRAC",
		"terms" : [ Acronym("CRAC"), Word("Centre Régional d'Aide aux Communes") ]
	},
	
	{
		"value" : "event",
		"children" : { ("type", "date") }
	},
	{
		"type" : "event",
		"value" : "Assemblée Générale",
		"terms" : [ Word("Assemblée Générale"), Word("Assemblées Générales"), Acronym("AG") ],
		"children" : { "Procès verbal" }
	},
	{
		"type" : "event",
		"value" : "Séance précédente",
		"terms" : [ 
			Word("Séance précédente"), 
			Word("Séances précédentes"), 
			Word("Séance antérieure"),
			Word("Séances antérieures"),
			Word('Dernière séance'),
			Word("Dernières séances")
		], 
		"children" :  { 'Procès verbal' }
	},
	{
		"type" : "event",
		"value" : "Marché de Noël",
		"terms" : [ Word("Marché de Noël"), Word("Marché communal de Noël") ],
		"children" : { ("type", "year") }
	},
	
	{ "value" : "service" },
	{ 
		"type" : "service", 
		"value" : "Bâtiments", 
		"replace" : False,
		"terms" : [ Word("Services? des Bâtiments"), Word("Services? Bâtiments") ],
		"union" : { "Service" }
	},
	{ 
		"type" : "service", 
		"value" : "Finance", 
		"terms" : [ Word("Finances communales"), Word("Finances?") ],
		"union" : { "Service" }
	},
	{ 
		"type" : "service", 
		"value" : "Travaux", 
		"terms" : [ Word("Travaux publics"), Word("Travaux") ],
		"union" : { "Service" }
	},
	{ 
		"type" : "service", 
		"value" : "Festivités", 
		"terms" : [ Word("Festivités?"), Word("Cérémonies?"), Word("Fêtes?") ],
		"intersect" : { "Service" },
		"union" : { "Service" }
	},
	{
		"type" : "service",
		"value" : "Service",
		"terms" : [ Word("Service"), Word("Services") ],
		"intersect" : { ("type", "service") },
	},
	{ 
		"type" : "service", 
		"value" : "Urbanisme", 
		"terms" : [ Word("Urbanisme") ],
		"intersect" : { "Service", "Marché de services" },
		"union" : { "Service" }
	},
	{ 
		"type" : "service", 
		"value" : "Aménagement du territoire", 
		"terms" : [ Word("Aménagement du Territoire") ],
		"union" : { "Service" }
	},
	{ 
		"type" : "service", 
		"value" : "Secrétariat", 
		"terms" : [ Word("Secrétariat général"), Word("Secrétariat") ],
		"union" : { "Service" }
	},
	{ 
		"type" : "service", 
		"value" : "Cartographie", 
		"terms" : [ Word("Cartographie") ],
		"intersect" : { "Service", "Marché de services" },
		"union" : { "Service" }
	},
	{ 
		"type" : "service", 
		"value" : "Nettoyage", 
		"terms" : [ Word("Nettoyage") ],
		"intersect" : { "Service", "Marché de services" },
		"union" : { "Service" }
	},
	{ 
		"type" : "service", 
		"value" : "Environnement", 
		"terms" : [ Word("Environnement") ],
		"intersect" : { "Service" },
		"union" : { "Service" }
	},
	
	{ 
		"type" : "entity", 
		"value" : "Stade", 
		"terms" : [ Word("Stades?") ],
		"union" : { "ASBL" },
		"children": { "Stationnement" }
	},
	{ 
		"type" : "entity", 
		"value" : "Espace vert", 
		"terms" : [ Word("Espaces? Verts?") ]
	},
	
	{
		"value" : "decision"
	},
	{
		"type": "decision",
		"value": "Approbation",
		"terms" : [ Word("Approbation"), Word("Approuver") ]
	},
	{
		"type": "decision",
		"value": "Réformation",
		"terms" : [ Word("Réformations?") ],
		"union" : { "Approbation" }
	},
	{
		"type": "decision",
		"value": "Connaissance",
		"terms" : [ Word("Prendre connaissance"), Word("Prises de connaissance") ]
	},
	{
		"type": "decision",
		"value": "Accord",
		"terms" : [ 
			Word("Accords? de principe"), 
			Word("Accords? transactionnels?"), 
			Intersect(Word("Marquer?"), Word("Accords?")), 
			Word("Accords? sur"),
			Word("Accords? de"),
			Word("Accords? pour"),
			Word("Pour accords?"),
			#Intersect(Word("Pour"), Word("Accords?"))
		]
	},
	{
		"type": "decision",
		"value": "Décharge",
		"terms" : [ Word("Décharges?") ],
		"disjoin" : { "Pollution" }
	},
	
	{
		"type" : "other",
		"value" : "Logiciel",
		"terms" : [ Word("Logiciels?") ]
	},
	{
		"type" : "other",
		"value" : "Pollution",
		"terms" : [ Word("Pollutions?"), Word("Immondices?") ]
	},
	
	{
		"value" : "building"
	},
	{
		"type" : "building",
		"value" : "Logement",
		"terms" : [ Word("Logements? Publics?"), Word("Appartements?") ],
		"children" : { "Location", "Parking" }
	},
	{
		"type" : "building",
		"value" : "Bâtiment",
		"terms" : [ 
			Word("Bâtiment communal"), 
			Word("Bâtiments communaux"), 
			Word("Biens? sis"), 
			Word("Biens? immeubles? sis"),
			Word("Immeubles? sis"),
			Word("Immeubles?"),
			Word("Préfabriqués?"),
			Word("Chalets?"),
			Intersect(Word("Bâtiments?"), Word("situés?"))
		],
		"children" : { ("type", "route"), "Location" }
	},
	{
		"type" : "building",
		"value" : "Bâtiment",
		"terms" : [ Word("Bâtiments?") ],
		"disjoin" : { "Bâtiments" },
		"children" : { ("type", "route") },
		"intersect" : { ("type", "market"), ("type", "finance") }
	},
	{
		"type" : "building",
		"value" : "Logement",
		"terms" : [ Intersect(Word("Logements?"), Word("Patrimoine")), Word("Nouveaux? logements?") ],
		"children" : { "Location", "Parking" },
		"union" : { "Bâtiment" }
	},
	{
		"type" : "building",
		"value" : "Logement",
		"terms" : [ Word("Logements?") ],
		"children" : { "Location", "Parking" },
		"intersect" : { 
			("type", "market"), 
			("type", "subside"), 
			("type", "scrl"), 
			("type", "régie"), 
			("type", "route"), 
			("type", "building"), 
			"Travaux"
		},
		"union" : { "Bâtiment" }
	},
	{
		"type" : "building",
		"value" : "Location",
		"terms" : [ 
			Word("Bail"), 
			Word("Contrats? de locations?"), 
			Word("Contrats? de base de locations?"), 
			Intersect(Word("Locations?"), Word("Salles?")),
			Intersect(Word("Locations?"), Word("Local")),
			Intersect(Word("Locations?"), Word("Locaux"))
		]
	},
	{
		"type" : "building",
		"value" : "Location",
		"terms" : [ Word("Locations?") ],
		"intersect": { "Logement", "Bâtiment", ("type", "régie"), "Maison des Sports" },
		"disjoin" : { "Logiciel", "Matériel" }
	},
	
	{ "value" : "date" },
	{
		"type" : "date",
		"terms" : [ 
			Date(r"(\d{2})([^\d])(\d{2})\2(\d{4}|\d{2})", "%4-%3-%1"), 
			Date(r"(\d{1,2}) (?:et|au) (\d{1,2}) ?(" + r"|".join(Date.months) + r") (\d{4}|\d{2})", "%4-%3-%1,%4-%3-%2"),
			Date(r"(\d{1,2}) ?(" + r"|".join(Date.months) + r") (?:et|au) (\d{1,2}) ?(" + r"|".join(Date.months) + r") (\d{4}|\d{2})", "%5-%2-%1,%5-%4-%3"),
			Date(r"(\d{1,2}) ?(" + r"|".join(Date.months) + r") (\d{4}|\d{2})", "%3-%2-%1"),
			Trimester(r"(\d) et (\d) trimestres (\d{4}|\d{2})", "%1-%3,%2-%3"),
			Trimester(r"(\d) ?trimestre (\d{4}|\d{2})", "%1-%2"),
			Semester(r"(\d) semestre (\d{4}|\d{2})", "%1-%2")
		]
	},
		
	{ "value" : "number" },
	{ 
		"type" : "number",
		"terms" : [
			Number(r"(?:ndeg|numeros?) *(\d{2,}[a-z]*)\b"),
			Number(r"\b(\d{2,}) ?(?:er|eme|e)\b")
		]
	},
	
	{ "value" : "money" },
	{ "value" : "htva" },
	{ "value" : "tva" },
	{
		"type" : "htva",
		"terms" : [
			Number(r"([\d\.,]+) ?(?:euro?s?)? hors T\.?V\.?A\b"),
			Number(r"([\d\.,]+) ?(?:euro?s?)? H\.?T\.?V\.?A\b")
		]
	},
	{
		"type" : "tva",
		"terms" : [
			Number(r"([\d\.,]+) ?(?:euro?s?)? T\.?V\.?A\.?C\b"),
			Number(r"([\d\.,]+) ?(?:euro?s?)? T\.?V\.?A\b")
		],
		"children" : [ ("type", "htva"), ("type", "money"), ("type", "percent") ]
	},
	{
		"type" : "money",
		"terms" : [
			Number(r"([\d\.,]+) ?(?:euro?s?)\b")
		]
	},
		
	{ "value" : "percent" },
	{
		"type" : "percent",
		"terms" : [ Number(r'(\d{1,2}(?:,\d+)?) ?\%') ]
	},
	
	{ "value" : "year" },
	{
		"type" : "year",
		"terms" : [ 
			Range(r"\b(\d{4}) ?[-/a] ?(?:(?:" + r'|'.join(Date.months) + r") )?(\d{4})\b"),
			Year(r"(?<=[^\d\(])(\d{4})(?=[^\d\)]|$)"), 
		]
	},
	
	{ 
		"type" : "number",
		"terms" : [
			Number(r"\d{4}/(\d{2,})\b")
		]
	}
]
