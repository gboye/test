# -*- coding: utf8 -*-

#########################IMPORTS############################################
import codecs, optparse
import re, random
import sys,os,time
import string

#########################VARIABLES##########################################
version=os.path.basename(__file__)
time_stamp='%s' % time.strftime("%y%m%d-%H%M")
debug=0
debug_now=0
print_no=False
print_coffee=True
print_commands=True
print_phrases=True
print_glose=0
print_lexique=False
print_cloze=False
print_racines=False
no_form="***"
genre=[u'M',u'F',u'A', u'I']
classe=[u'H',u'NH']
nombre=[u'SG',u'DU',u'PL',u'NSG']
nombre_sdp=[u'SG',u'DU',u'PL']
nombre_sp=[u'SG',u'NSG']
cas=[u'',u'ERG',u'ABS']
# no_grapho=['dormir', 'lit']
# no_phono=['gros', 'coussin']
no_grapho=['petit','Nabil',"sur"]
no_phono=["grand","autruche",'dans']
phono_no=u"XXXXX"
grapho_no=u"XXXXX"

lexemes=[]
graphies={}
lexique={}
base={}
categorie_v={}
temps_v={}
radical_n={}
radical_v={}
noms=[]
cloze_noms=[]
tableau_noms=[]
verbes=[]
cloze_verbes=[]
tableau_verbes=[]
determinants=[]
tableau_determinants=[]
prepositions=[]
tableau_prepositions=[]
adjectifs=[]
tableau_adjectifs=[]
francais=[]
kalaba=[]

#########################CONSTANTS##########################################
head = [
"\\begin{tabular}[t]{|l|l|l|}",
"\\addlinespace[-1.0em]\\hline",
"Mot & Roman & Glose  \\\\",
"\\hline\\strutgh{14pt}%"
]
head_n = [
"\\begin{tabular}[t]{|l|c|c|c|}",
"\\addlinespace[-1.0em]\\hline",
"Nom & Genre & C\\indice{1}C\\indice{2}C\\indice{3} & V\\indice{L}  \\\\",
"\\hline\\strutgh{14pt}%"
]
head_v = [
"\\begin{tabular}[t]{|l|c|c|}",
"\\addlinespace[-1.0em]\\hline",
"Verbe & Type & C\\indice{1}C\\indice{2}C\\indice{3} \\\\",
"\\hline\\strutgh{14pt}%"
]

tail = [
"\\hline"
"\\end{tabular}\\\\"
]
consonnes=u"ptkbdgmnNfsSvzZrljw"
voyelles=u"iueoa"
gabarits=['SG','DU','PL','PRS','PST']
derives={'A':'V','D':'C'}
nom_classe={'A':'', 'B':'i', 'C':'a', 'D':'u'}
nom_apo={'':'i', 'i':'a', 'a':'u', 'u':'u', 'e':'o', 'o':'o'}
nom_mut={
'p':u'p',
't':u'p',
'k':u't',
'b':u'p',
'd':u'b',
'g':u'd',
'm':u'm',
'n':u'm',
'N':u'n',
'f':u'f',
's':u'f',
'S':u's',
'v':u'f',
'z':u'v',
'Z':u'z',
'r':u'w',
'l':u'r',
'j':u'w',
'w':u'w',
}
nom_nombre={'SG':'1a4A2V3e','DU':'1A8V2i6C','PL':'4U2A9u3D'}
#nom_fonct={'OBL':'ko','NOM':'re','ACC':'bo','DAT':'li'}
nom_cas={'OBL':'ko','ERG':'re','ABS':'bo','DAT':'li'}
verbe_classe={'VT':'e', 'VI':'i', 'VD':'a'}
verbe_genre={'A':'i', 'B':'a', 'C':'o', 'D':'e'}
verbe_nombre={'SG':'p','DU':'s','PL':'d'}
verbe_temps={'PRS':'A1C2a5V3u', 'PST':'C4A1o2D3V'}
verbe_forme={2:'INF',3:'PRS',4:'PRS',5:'PST',6:'PST'}
det_nb={'SG':'o', 'DU':'a', 'PL':'i'}
# det_fonct={'OBL':'g','NOM':'m','ACC':'k','DAT':'t'}
det_cas={'OBL':'g','ERG':'m','ABS':'k','DAT':'t'}
adjectif_genre={'A':'v', 'B':'f', 'C':'d', 'D':'k'}
adjectif_nb={'SG':'i', 'DU':'a', 'PL':'o'}
adj_types_nombre={'1':{'SG':'i', 'DU':'a', 'PL':'o'},'2':{'SG':'o', 'DU':'a', 'PL':'i'}}
adj_types_genre={'1':{'A':'v', 'B':'f', 'C':'d', 'D':'k'},'2':{'A':'m', 'B':'v', 'C':'t', 'D':'g'}}
# syntagmes={
# 	'Phrase':['AJOUT','SUJ','COMP','IND','OBJ','V'],
# 	'GN':['N','GP', 'GADJ', 'DET'],
# 	'GP':['GN','PREP'],
# 	'GADJ':['GP','ADV','ADJ'],
# 	}
syntagmes={
	'Phrase':['AJOUT','SUJ','COMP','IND','OBJ','V'],
	'GN':['N','GP','GADJ','DET'],
	'GP':['GN','PREP'],
	'GADJ':['GP','ADV','ADJ'],
	}

contractions={
	'au':['à', 'le'],
	'aux':['à','les'],
	'du':['de','le'],
	'des':['de','les']
}

syllabes={
	'da':u'd', 
	'de':u'D', 
	'di':u'f',
	'do':u'g', 
	'du':u'x',
	'ja':u'j', 
	'je':u'J', 
	'jo':u'b', 
	'ju':u'L',
	'ka':u'k', 
	'ke':u'K', 
	'ki':u'c',
	'ko':u'h', 
	'ku':u'v',
	'ma':u'm', 
	'me':u'M', 
	'mi':u'y',
	'mo':u'A', 
	'mu':u'B',
	'na':u'n', 
	'ne':u'N', 
	'ni':u'C',
	'no':u'E', 
	'nu':u'F',
	'pa':u'p', 
	'pe':u'P', 
	'pi':u'G',
	'po':u'H', 
	'pu':u'I',
	'qa':u'q', 
	'qe':u'Q', 
	'qi':u'X',
	'qo':u'8', 
	'ra':u'r', 
	're':u'R', 
	'ri':u'O',
	'ro':u'U', 
	'ru':u'V',
	'sa':u's', 
	'se':u'S', 
	'si':u'Y',
	'so':u'1', 
	'su':u'2',
	'ta':u't', 
	'te':u'T', 
	'ti':u'3',
	'to':u'4', 
	'tu':u'5',
	'wa':u'w', 
	'we':u'W', 
	'wi':u'6',
	'wo':u'7', 
	'za':u'z', 
	'ze':u'Z', 
	'zo':u'9', 
}

def taches(chaine):
	result=[]
	choix=random.sample(["a","b","c","d","e","f","g","h"],len(chaine)//2+len(chaine)%2)
	for n in range(0, len(chaine), 2):
		result.append("\\cache%s{%s}" % (choix[n//2],chaine[n:n+2]))
	return "".join(result)


def parse_grapho(graphie):
	chunks=re.findall(ur"([djkmnpqrstwz][aeiou]?)|[aeiou]|[.…,;!?:—–()\[\]\/# ""«»<>]", graphie)
	result=[]
	for chunk in chunks:
		if chunk in syllabes.keys():
			result.append(syllabes[chunk])
		else:
			result.append(chunk)
	return "".join(result)

def blanc(chaine):
	result="\\blanc{"+chaine+"}"
	return result

def apophone(voyelle):
	result=nom_apo[voyelle]
	return result

def mutation(consonne):
	result=nom_mut[consonne]
	return result


def fait_racine(simple):
	if debug: print "simple : ", simple
	c=1
	result={'1':'','2':'','3':'','V':''}
	for lettre in simple:
		if debug: print "lettre : ",lettre
		if lettre in consonnes:
			result[str(c)]=lettre
			c=c+1
		elif lettre in voyelles:
			if result['V']=='':
				result['V']=lettre
		else:
			if debug: print "erreur sur racine", simple
	return result

def affixe(debut, fin):
	return debut+fin

def gabarit(forme,racine):					#met la racine dans le gabarit forme
	if debug: print "gabarit : ", forme, racine
	result=""
	for signe in forme:
		if signe in "123":				#place les consonnes en 1, 2, 3
			result=result+racine[signe]
		elif signe in "456":
			result=result+mutation(racine[str(int(signe)-3)])
		elif signe in "789":
			result=result+mutation(mutation(racine[str(int(signe)-6)]))
		elif signe in "VC":				#place la voyelle radicale V et la voyelle de classe C
			result=result+racine[signe]
		elif signe in "AD":
			result=result+apophone(racine[derives[signe]])	#place les apophones de V et C (resp. A et D)
		elif signe in "U":
			result=result+apophone(apophone(racine['V']))	#place le bi-apophone de V
		else:
			result=result+signe
		if debug: print signe, result
	if debug: print result
	return result

def n_nombre(nombre, nom, classe):
	radical=nom
	if debug: print "radical : ",radical
	racine=fait_racine(radical)
	racine["C"]=nom_classe[classe]
	if debug: print "racine : ", radical, racine
	forme=nom_nombre[nombre]
	if debug: print "n_nombre :", nombre, forme
	if nombre in gabarits :
		if debug: print "forme gabaritique : ", forme, racine
		result=gabarit(forme, racine)
	else:
		result=affixe(nom_nombre[nombre], radical)
	return result
	
def n_cas(cas, nom, classe):
	if cas!='Ø':
		result=nom_cas[cas]+nom
	else:
		result=nom
	return result

def paradigme_nom(nom):
	genre=nom[0]
	racine=nom[1]
	lemme=nom[2]
	if not lemme.istitle():
		lemme=lemme.lower()
	if debug: print lemme, racine, genre
	extrait=fait_racine(racine)
	radical_n[lemme]= ("%s%s%s" % (extrait['1'],extrait['2'],extrait['3']), extrait['V'], genre)
	for nombre in nombres:
		if debug: print nombre
		if debug: print nombre, racine, genre
		phono_n=n_nombre(nombre, racine, genre)
		if nombre in gabarits:
			gloss_n=lemme+str(blanc("."+genre.capitalize()+"x"+nombre.upper()))
			gloss_n_cloze=lemme+";."+genre.capitalize()+";x"+nombre.upper()
		else:
			gloss_n=lemme+str(blanc("."+genre.capitalize()+"."+nombre.upper()))
			gloss_n_cloze=lemme+";."+genre.capitalize()+";."+nombre.upper()
		for case in cases:
			if debug: print case
			phono=n_cas(case, phono_n, classe)
			grapho=phono
			grapho=parse_grapho(grapho.translate(translit))
			if case!='Ø':
				gloss=str(blanc(case.upper()+"-"))+gloss_n
				gloss_cloze=case.upper()+"-;"+gloss_n_cloze
				ref=lemme.translate(deaccent)+genre.capitalize()+nombre.capitalize()+case.capitalize()
			else:
				gloss=gloss_n
				gloss_cloze=gloss_n_cloze
				ref=lemme.translate(deaccent)+genre.capitalize()+nombre.capitalize()
			if nom[2] in no_grapho and print_no:
				grapho_no=taches(grapho)
				noms.append("\\newcommand{\\"+ref+"}{\\strutgb{0pt}\\grapho{"+grapho_no+"}}")
				grapho=grapho_no
			else:
				noms.append("\\newcommand{\\"+ref+"}{\\strutgb{0pt}\\grapho{"+grapho+"}}")
			if nom[2] in no_phono and print_no:
				phono_no=taches(phono)
				noms.append("\\newcommand{\\"+ref+"P}{\\textipa{"+phono_no+"}}")
				phono=phono_no
			else:
				noms.append("\\newcommand{\\"+ref+"P}{\\textipa{"+phono+"}}")
				cloze_noms.append((phono,gloss_cloze))
			graphies["\\"+ref]=grapho
			noms.append("\\newcommand{\\"+ref+"G}{"+gloss+"}")
			if print_glose:
				tableau_noms.append("\\"+ref+" & \\"+ref+"P & \\"+ref+"G \\\\")
			else:
				tableau_noms.append("\\"+ref+" & \\"+ref+"P & \\\\")

def v_temps(tense, verbe, type, genre):
	radical=verbe
	if debug: print "radical : ",radical
	racine=fait_racine(radical)
	racine["V"]=verbe_classe[type]
	racine["C"]=verbe_genre[genre]
	if debug: print "racine : ", radical,type,genre, racine
	forme=verbe_temps[tense]
	if debug: print "v_temps :", tense, forme
	if tense in gabarits :
		if debug: print "forme gabaritique : ", forme, racine
		result=gabarit(forme, racine)
	else:
		result=affixe(verbe_temps[tense], radical)
	return result
	
def v_nombre(nombre, verbe):
	if debug: print nombre, verbe
	result=verbe_nombre[nombre]+verbe
	return result

def paradigme_verbe(verbe):
	type=verbe[0]
	racine=verbe[1]
	lemme=verbe[2]
	if debug: print lemme, racine, type
	extrait=fait_racine(racine)
	radical_v[lemme]= ("%s%s%s" % (extrait['1'],extrait['2'],extrait['3']), type)
	for tense in temps:
		if debug: print tense
		for genre in genres:
			if debug: print genre
			phono_t=v_temps(tense,racine,type,genre)
			if tense in gabarits:
				gloss_t=lemme.lower()+str(blanc("."+type.upper()+"x"+tense.upper()+"x"+genre.upper()))
				gloss_t_cloze=lemme.lower()+";."+type.upper()+";x"+tense.upper()+";x"+genre.upper()
			else:
				gloss_t=lemme.lower()+str(blanc("."+type.upper()+"-"+tense.upper()+"-"+genre.upper()))
				gloss_t_cloze=lemme.lower()+";."+type.upper()+";-"+tense.upper()+";-"+genre.upper()
			for nombre in nombres:
				if debug: print nombre
				phono=v_nombre(nombre,phono_t)
				grapho=phono
				gloss=str(blanc(nombre+"-"))+gloss_t
				gloss_cloze=nombre+"-;"+gloss_t_cloze
				ref=lemme.translate(deaccent)+type.capitalize()+tense.capitalize()+genre.capitalize()+nombre.capitalize()
				grapho=parse_grapho(grapho.translate(translit))
				if verbe[2] in no_grapho and print_no:
					grapho_no=taches(grapho)
					verbes.append("\\newcommand{\\"+ref+"}{\\strutgb{0pt}\\grapho{"+grapho_no+"}}")
					grapho=grapho_no
				else:
					verbes.append("\\newcommand{\\"+ref+"}{\\strutgb{0pt}\\grapho{"+grapho+"}}")
				if verbe[2] in no_phono and print_no:
					phono_no=taches(phono)
					verbes.append("\\newcommand{\\"+ref+"P}{\\textipa{"+phono_no+"}}")
					phono=phono_no
				else:
					verbes.append("\\newcommand{\\"+ref+"P}{\\textipa{"+phono+"}}")
					cloze_verbes.append((phono,gloss_cloze))
				graphies["\\"+ref]=grapho
				
				verbes.append("\\newcommand{\\"+ref+"G}{"+gloss+"}")
				if print_glose:
					tableau_verbes.append("\\"+ref+" & \\"+ref+"P & \\"+ref+"G \\\\")
				else:
					tableau_verbes.append("\\"+ref+" & \\"+ref+"P & \\\\")

def adj_nombre(nombre, adjectif,type=0):
	if debug: print nombre, adjectif
	if type==0:
		result=adjectif+adjectif_nb[nombre]
	elif type in adj_types_nombre.keys():
		result=adjectif+adj_types_nombre[type][nombre]
	return result

def adj_genre(genre, adjectif,type=0):
	if debug: print genre, adjectif
	if type==0:
		result=adjectif+adjectif_genre[genre]
	elif type in adj_types_genre.keys():
		result=adjectif+adj_types_genre[type][genre]
	return result

def paradigme_adj(lexeme):
	cat_adj=lexeme[0].split('.')
	if len(cat_adj)==2:
		classe_flex=cat_adj[1]
		adj_flex=".A"+str(classe_flex)
	else:
		classe_flex=0
		adj_flex=""
	radical=lexeme[1]
	lemme=lexeme[2]
	if debug: print lemme, radical
	for nombre in nombres:
		if debug: print genre
		phono_n=adj_nombre(nombre,radical,classe_flex)
		for genre in genres:
			phono=adj_genre(genre,phono_n,classe_flex)
			gloss=lemme.lower()+str(blanc(adj_flex+"-"+nombre.upper()+"-"+genre.upper()))
			ref=lemme.lower()+nombre.capitalize()+genre.capitalize()
			grapho=phono
			grapho=parse_grapho(grapho.translate(translit))
			if lexeme[2] in no_grapho and print_no:
				grapho_no=taches(grapho)
				adjectifs.append("\\newcommand{\\"+ref+"}{\\strutgb{0pt}\\grapho{"+grapho_no+"}}")
#				grapho=grapho_no
			else:
				adjectifs.append("\\newcommand{\\"+ref+"}{\\strutgb{0pt}\\grapho{"+grapho+"}}")
			if lexeme[2] in no_phono and print_no:
				phono_no=taches(phono)
				adjectifs.append("\\newcommand{\\"+ref+"P}{\\textipa{"+phono_no+"}}")
#				phono=phono_no
			else:
				adjectifs.append("\\newcommand{\\"+ref+"P}{\\textipa{"+phono+"}}")
			graphies["\\"+ref]=grapho
			adjectifs.append("\\newcommand{\\"+ref+"G}{"+gloss+"}")
			if print_glose:
				tableau_adjectifs.append("\\"+ref+" & \\"+ref+"P & \\"+ref+"G \\\\")
			else:
				tableau_adjectifs.append("\\"+ref+" & \\"+ref+"P & \\\\")
			
			

def paradigme_det(lexeme):
	radical=lexeme[1]
	lemme=lexeme[2]
	if debug: print lemme, radical
	for nombre in nombres:
		if debug: print nombre
		phono_n=radical+det_nb[nombre]
		for case in cases:
			if case!='Ø':
				phono=phono_n+det_cas[case]
				gloss=lemme.upper()+str(blanc("-"+nombre.upper()+"-"+case.upper()))
				ref=lemme.lower()+nombre.capitalize()+case.capitalize()
			else:
				phono=phono_n
				gloss=lemme.upper()+str(blanc("-"+nombre.upper()))
				ref=lemme.lower()+nombre.capitalize()
			grapho=phono
			if lexeme[2] in no_grapho and print_no: grapho=taches(grapho)
			if lexeme[2] in no_phono and print_no: phono=taches(phono)
			determinants.append("\\newcommand{\\"+ref+"}{\\strutgb{0pt}\\grapho{"+parse_grapho(grapho.translate(translit))+"}}")
			graphies["\\"+ref]=grapho
			determinants.append("\\newcommand{\\"+ref+"P}{\\textipa{"+phono+"}}")
			determinants.append("\\newcommand{\\"+ref+"G}{"+gloss+"}")
			if print_glose:
				tableau_determinants.append("\\"+ref+" & \\"+ref+"P & \\"+ref+"G \\\\")
			else:
				tableau_determinants.append("\\"+ref+" & \\"+ref+"P & \\\\")

def paradigme_prep(lexeme):
	phono=lexeme[1]
	lemme=lexeme[2].translate(deaccent)
	gloss=lemme.upper()
	grapho=phono
	grapho=parse_grapho(grapho.translate(translit))
	ref=lemme.upper()
	if lexeme[2] in no_grapho and print_no: grapho=taches(grapho)
	if lexeme[2] in no_phono and print_no: phono=taches(phono)
	prepositions.append("\\newcommand{\\"+ref+"}{\\strutgb{0pt}\\grapho{"+grapho+"}}")
	graphies["\\"+ref]=grapho
	prepositions.append("\\newcommand{\\"+ref+"P}{\\textipa{"+phono+"}}")
	prepositions.append("\\newcommand{\\"+ref+"G}{"+gloss+"}")
	if print_glose:
		tableau_prepositions.append("\\"+ref+" & \\"+ref+"P & \\"+ref+"G \\\\")
	else:
		tableau_prepositions.append("\\"+ref+" & \\"+ref+"P & \\\\")


def faire_tableau(tableau,tab=(head,tail,"")):
	if len(tableau)==0: return
	comment=tab[2]
	for element in tab[0]:
		print comment+element
	for element in tableau:
		print comment+element
	for element in tab[1]:
		print comment+element

def print_tableaux(cols,tableau,texte="",debut=0,tab=(head,tail,"")):
	print tab[2]+"\\begin{multicols}{"+str(cols)+"}"
	if texte!="":
		table=filtrer_tableau(tableau,texte)
	else:
		table=tableau
	chunk=(len(table)-debut*cols)/cols+1
	faire_tableaux(table,debut,cols,tab)
	print tab[2]+"\\end{multicols}"
	


#def faire_tableaux(tableau,taille=16,debut=16,nombre=0):
#	for i in range(nombre):
#		faire_tableau(tableau[debut*i:debut*(i+1)])
#	longueur=len(tableau)-nombre*debut
#	chunks=longueur/taille
##	print longueur, taille, chunks
#	for i in range(chunks+1):
##		print i
#		faire_tableau(tableau[nombre*debut+taille*i:nombre*debut+taille*(i+1)])

def faire_tableaux(tableau,debut=16,nombre=1,tab=(head,tail,"")):
	reste=[]
	if debug: print nombre,debut,tableau
	if debut!=0:
		for i in range(nombre):
			faire_tableau(tableau[debut*i:debut*(i+1)],tab)
		table=tableau[debut*nombre:]
	else:
		table=tableau
	longueur=len(table)
	chunk=longueur/nombre+1
	if debug: print "CHUNKING : ",longueur, nombre, chunk, table
	if chunk<48:
		chunks=chunk
	else:
		chunks=48
		reste=table[48*nombre:]
	if debug: print "RESTE : ", chunk, reste
#	print longueur, taille, chunks
	for i in range(nombre):
#		print i
		faire_tableau(table[chunks*i:chunks*(i+1)],tab)
	if reste:
		faire_tableaux(reste,0,nombre,tab)

def filtrer_tableau(tableau,filtre):
	result=[]
	for line in tableau:
		elements=line.split(" ")
		if elements[0] in filtre: result.append(line)
	return result

def faire_gn(depart,cas):
	global erg_genre, erg_nombre, abs_genre, abs_nombre
	if debug: print "groupe depart :", depart
	groupe_nom=[]
	groupe_nom.append(depart[0])
	if debug: print depart[0]
	for mot in depart[1:]:
		if debug: print mot
		groupe_nom.extend(etendre_contraction([mot]))
	if debug: print "groupe nom :", groupe_nom
	mots=[]
	det=[]
	adj=[]
	nom=[]
	gp=[]
	tete=""
	nombre=""
	reste=0
	for mot in groupe_nom:
		if reste==0:
			if mot=="deux":
				nombre="DU"
				if det==[]: det.append(base["des"])
			else:
				if debug:
					print mot,
					print base[mot],
					print lexique[base[mot]]
				categorie=lexique[base[mot]]
				if categorie in genres:
					tete=categorie
					if debug: print "tête :", tete
					tampon=tete.split('.')
					classe=tampon[0]
					try:
						type=tampon[1]
					except IndexError:
						type=''
					if mot[len(mot)-1]=='s':
						if nombre=="": nombre="PL"
					else:
						if nombre=="": nombre="SG"
					nom.append(base[mot])
					cellule=classe.capitalize()+nombre.capitalize()+cas.capitalize()
					if cas=="ERG":
						erg_genre=classe
						erg_nombre=nombre
					elif cas=="ABS":
						abs_genre=classe
						abs_nombre=nombre
				elif categorie in ["DEF","DEM","IND"]:
					det.append(categorie)
				elif categorie.startswith("ADJ"):
					adj.append(base[mot])
				elif categorie=="PREP":			#Si on trouve une PREP, elle et le reste forment un GP
					gp.append(mot)
					reste=1
		else:							#On a trouvé une PREP, toute la suite va dans DP
			gp.append(mot)
	if debug: print "accord :", tete
	if reste==1: gp=faire_gp(gp)
	if debug: print "GP dans le GN : ", gp
	if debug: print "GN sans det ? ", det
	if not det: det.append("IND")
	for mot in det:
#		glose=faire_glose(mot,classe,type,nombre)
		ref="\\"+mot.lower()+nombre.capitalize()+cas.capitalize()
		mots.append(ref)
		texte.append(ref)
	for mot in gp: mots.append(mot)
	for mot in adj:
#		glose=faire_glose(mot,classe,type,nombre)
		ref="\\"+mot.lower()+nombre.capitalize()+classe.capitalize()
		mots.append(ref)
		texte.append(ref)
	for mot in nom:
#		glose=faire_glose(mot,classe,type,nombre)
		if mot.istitle():
			ref="\\"+mot+cellule
		else:
			ref="\\"+mot.lower()+cellule
		mots.append(ref)
		texte.append(ref)
	return mots

def faire_gp(groupe_prep):
	mots=[]
	groupe_prep=etendre_contraction(groupe_prep)
	if debug: print "faire_gp", groupe_prep
	if groupe_prep[0]!=u"à" :
		if debug: print "PREP!=à"
		ref="\\"+groupe_prep[0].upper()
		mots.append(ref)
		texte.append(ref)
		if debug:
			print "groupe prep :", groupe_prep
			print ref
		if len(groupe_prep)>1:
			groupe_nom=groupe_prep[1:]
			mots.insert(0,faire_gn(groupe_nom,"OBL"))
		return mots
	else:
		groupe_nom=groupe_prep[1:]
		if debug: print "faire_gn", groupe_nom, faire_gn(groupe_nom,"DAT")
		mots.append(faire_gn(groupe_nom,"DAT"))
		return mots

def etendre_contraction(liste):
	result=[]
	if liste[0] in contractions.keys():
		if debug: print "EXT : ", liste, contractions[liste[0]],liste[1:] 
		result.extend(contractions[liste[0]])
		result.extend(liste[1:])
	else:
		result=liste
	#for element in liste:
	#	if element in contractions.keys(): result.extend(contractions[element])
	#	else: result.append(element)
	return result

def printflat(liste,suffixe="",prefixe=""):
	if debug: print "printflat", liste
	if not isinstance(liste, basestring):
		for element in liste:
			print prefixe,
			printflat(element,suffixe)
	else: print prefixe,liste+suffixe,


#######################
#
#	INITIALISATION DES VARIABLES
#
#######################

genres=nom_classe.keys()
types=verbe_classe.keys()
nombres=nom_nombre.keys()
cases=nom_cas.keys()
temps=verbe_temps.keys()


################
#
# LECTURE DU FICHIER DE LEXEMES
#
#		LES LIGNES QUI COMMENCENT PAR # SONT IGNOREES
#
################
print "%% version : "+version
print "%% traitement : "+time_stamp

parser=optparse.OptionParser()
parser.add_option("-o", "--out", dest="outfile", action="store_true", help="write to FILE")
parser.add_option("-c", "--cloze", dest="print_cloze", action="store_true", help="write a CLOZE FILE")
parser.add_option("-l", "--lexicon", dest="print_lexique", action="store_true", help="append a lexicon")
parser.add_option("-r", "--roots", dest="print_racines", action="store_true", help="append a root list")


(options, args) = parser.parse_args()


try:
    lexeme_file = codecs.open(args[0],"r","utf-8")
except IOError:
    print 'I could not open the lexeme file', args[0]
    sys.exit()

try:
    phrase_file = codecs.open(args[1],"r","utf-8")
except IOError:
    print 'I could not open the sentence file', args[1]
    sys.exit()

#translit=string.maketrans(u'iueoaftgzZvjkSpN',u'tgazpHTGZJVkXyxI')
phonlit =  u"ptkbdgmnNfsSvzZrljw"
graphlit = u"ptkpdkmnnqssqzzrrjw"
translit = dict((ord(a), b) for a, b in zip(phonlit, graphlit))


#deaccent=string.maketrans(u'àâçéèêîùô',u'aaceeeiuo')
accented =  u"àâçéèêîùô"
unaccented = u"aaceeeiuo"
deaccent = dict((ord(a), b) for a, b in zip(accented, unaccented))

tipa = u"SZN"
ipa = u"ʃʒŋ"
toipa = dict((ord(a), b) for a, b in zip(tipa, ipa))

lexemes=[]
graphies={}
noms=[]
tableau_noms=[]
verbes=[]
tableau_verbes=[]
determinants=[]
tableau_determinants=[]
prepositions=[]
tableau_prepositions=[]
adjectifs=[]
tableau_adjectifs=[]
francais=[]
kalaba=[]

for line in lexeme_file:
	tampon=(line.strip()).split(',')
	if not tampon[0].startswith("#"):
		lexemes.append(tampon)
lexeme_file.close()


for lexeme in lexemes:
	lemme=lexeme[2].translate(deaccent)
	categorie=lexeme[0]
	lexique[lemme]=categorie
	for forme in lexeme[2:]:
		base[forme]=lemme
		if debug: print "base :", forme, lexeme[2]
		if categorie in types:
			categorie_v[forme]=categorie
			temps_v[forme]=verbe_forme[lexeme.index(forme)]
			if debug: print forme, lemme, lexeme.index(forme), temps_v[forme]
	if lexeme[0] in genres:
		paradigme_nom(lexeme)
	elif lexeme[0] in types:
		paradigme_verbe(lexeme)
	elif lexeme[0].startswith("ADJ"):
		paradigme_adj(lexeme)
	elif lexeme[0] in ["DEF","IND","DEM"]:
		paradigme_det(lexeme)
	elif lexeme[0]=="PREP":
		paradigme_prep(lexeme)
	else: print "erreur de catégorie : ",lexeme[0]

if print_commands:
	comment=""
else:
	comment="%"	
for nom in noms:
	print comment+nom
print
print
print
for adjectif in adjectifs:
	print comment+adjectif
print
print
print
for verbe in verbes:
	print comment+verbe
print
print
print
for determinant in determinants:
	print comment+determinant
print
print
print
for preposition in prepositions:
	print comment+preposition
print
print
#################################################
#################################################
#################################################
##
##
##	FAIRE LE TRI DES FORMES UTILISEES DANS LES PHRASES
##	AFFICHER DANS LES TABLEAUX SEULEMENT CES FORMES
##
##
#################################################
################################################
#
#
#	FAIRE LA LISTE DES PHRASES AVEC LES 4 LIGNES
#		GRAPHO, PHONO, GLOSE, TRAD
#
#
################################################
texte=[]
graphies={}
abs_genre=""
abs_nombre=""

if debug:
	for forme in base.keys():
		print forme, base[forme]
if print_phrases:
	comment=""
else:
	comment="%"
print comment+"\\begin{exe}"
for line in phrase_file:
	phrase=[0 for i in range(len(syntagmes['Phrase']))]
	#
	# Insertion du replace("'"," ") pour la gestion des articles élidés en français
	#
	tampon=(line.strip().rstrip('.')).replace("'"," ").split("\t")
	if not tampon[0].startswith("#"):
		verbe=tampon[1].split(" ")
		if debug: print "verbe :", verbe
		if categorie_v[verbe[0]] == "VI":
			suj_cas="ABS"
		else:
			suj_cas="ERG"
			obj_cas="ABS"
		suj_genre="A"
		suj_nombre="SG"
		obj_genre="A"
		obj_nombre="SG"
		sujet=tampon[0].strip().split(" ")
		phrase[syntagmes['Phrase'].index('SUJ')]=faire_gn(sujet,suj_cas)
		if debug: print "sujet :",phrase[1]
# 		verbe=tampon[1].split(" ")
# 		if debug: print "verbe :", verbe
		if len(tampon)>=3:
			objet=tampon[2].split(" ")
			if debug: print "objet : ",objet
			if objet!=['']: phrase[syntagmes['Phrase'].index('OBJ')]=faire_gn(objet,obj_cas)
		if len(tampon)>=4:
			indirect=tampon[3].split(" ")
			if debug: print "indirect : ",indirect
			if indirect!=['']: phrase[syntagmes['Phrase'].index('IND')]=faire_gp(indirect)
		#if len(tampon)>=4:
		#	indirect=tampon[3].split(" ")
		#	if indirect!=['']: phrase[2]=faire_gp(indirect)
		if len(tampon)>=5:
			ajout=tampon[4].split(" ")
			phrase[syntagmes['Phrase'].index('AJOUT')]=faire_gp(ajout)
#		glose=faire_glose(base[verbe[0]],suj_genre,suj_num)
#		if debug: print verbe[0],categorie_v[verbe[0]], temps_v[verbe[0]], suj_genre, suj_nombre
#		glose="\\"+base[verbe[0]]+categorie_v[verbe[0]].capitalize()+temps_v[verbe[0]].capitalize()+suj_genre.capitalize()+suj_nombre.capitalize()
#  		if categorie_v[verbe[0]] == "VI":
#  			glose="\\"+base[verbe[0]]+categorie_v[verbe[0]].capitalize()+temps_v[verbe[0]].capitalize()+suj_genre.capitalize()+suj_nombre.capitalize()
#  		else:
 		glose="\\"+base[verbe[0]]+categorie_v[verbe[0]].capitalize()+temps_v[verbe[0]].capitalize()+abs_genre.capitalize()+abs_nombre.capitalize()
 		phrase[syntagmes['Phrase'].index('V')]=glose
		texte.append(glose)
		if print_glose:
			print comment+"\\ex\\glll"
		else:
			print comment+"\\ex\\gll"
		print comment,
		for mot in phrase:
			if mot!=0:
				printflat(mot,"{}")
		print "\\\\"
		print comment,
		for mot in phrase:
			if mot!=0:
				printflat(mot,"P{}")
		print "\\\\"
		if print_glose:
			print comment,
			for mot in phrase:
				if mot!=0:
					printflat(mot,"G{}")
			print "\\\\"
		traduction=(line.strip().rstrip('.')).split()
		start=1
		sys.stdout.write(comment)
		for element in traduction:			# convertir les S majuscules à la finale des mots en minuscules
			if element!="":
				if start:
					start=0
					element=element.capitalize()
				else:
					sys.stdout.write(' ')
				caracteres=list(element)
				if caracteres[len(caracteres)-1]=='S':
					caracteres[len(caracteres)-1]='s'
				sys.stdout.write("".join(caracteres))
		sys.stdout.write('.\r')
		if print_coffee and random.randint(1,6)==1:
			stain=random.choice(["A","B"])
			alpha=random.random()/1.5
			angle=random.randint(0,360)
			xoff=random.randint(-200,0)
			sys.stdout.write('\\\\\\cofe%sm{%.3f}{1}{%d}{%d}{0}' % (stain,alpha,angle,xoff))
print comment+"\\end{exe}"
	
phrase_file.close()
#################################################
if options.print_racines or print_racines:
	tableau_racines_n=[]
	tableau_racines_v=[]
	print
	print
	print
	print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%RACINES%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	print
	print
	print
	print "%										NOMS"
	print
	for element in sorted(radical_n.keys()):
		tableau_racines_n.append("%s & %s & \\textipa{%s} & \\textipa{%s} \\\\" % (element, radical_n[element][2], radical_n[element][0], radical_n[element][1]))
	print_tableaux(2,tableau_racines_n,"",0,(head_n,tail,"%"))	
	print
	print
	print
	print "%										VERBES"	
	print
	for element in sorted(radical_v.keys()):
		tableau_racines_v.append("%s & %s & \\textipa{%s} \\\\" % (element, radical_v[element][1], radical_v[element][0]))
	print_tableaux(2,tableau_racines_v,"",0,(head_v,tail,"%"))	


if options.print_lexique or print_lexique:
	tab=(head,tail,"")
else:
	tab=(head,tail,"%")
print tab[2]+"\\begin{itemize}"
print tab[2]+"\\item NOMS\\\\[-3ex]"
print_tableaux(2,tableau_noms,texte,21,tab)
print tab[2]+"\\item ADJECTIFS\\\\[-3ex]"
print_tableaux(3,tableau_adjectifs,texte,4,tab)
print tab[2]+"\\item VERBES\\\\[-3ex]"
print_tableaux(2,tableau_verbes,texte,35,tab)
print tab[2]+"\\item DETERMINANTS\\\\[-3ex]"
print_tableaux(3,tableau_determinants,texte,12,tab)
print tab[2]+"\\item PREPOSITIONS\\\\[-3ex]"
print_tableaux(3,tableau_prepositions,texte,0,tab)
print tab[2]+"\\end{itemize}"


if options.print_cloze or print_cloze:
	print
	print
	print
	print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%CLOZE%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	print
	print
	print
	print "%										NOMS"	
	for element in cloze_noms:
		print "% ", element[0].translate(toipa)+";"+element[1]
	print
	print
	print
	print "%										VERBES"	
	for element in cloze_verbes:
		print "% ", element[0].translate(toipa)+";"+element[1]		