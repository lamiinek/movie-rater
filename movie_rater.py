"""

Aut: Lamine Ka
Tit: Movie rater
Desc: This program will scan movies in a folder and check their rotten tomato percentage

"""

#import selenium
from bs4 import BeautifulSoup as bs
import requests as r
import os, csv
#add some color to the display
from termcolor import colored as color
from colorama import Fore, Back, Style, init

def rate():
	BASE_URL = "http://www.rottentomatoes.com/m/"
	MOVIES_DIR = "path_to_folder_containing_movies"
	movies = os.listdir(MOVIES_DIR)

	rank_file = open(str(MOVIES_DIR)+"\_Rottent Tomatoes.txt", "a")
	csv_file = open(MOVIES_DIR+"\_Movies details.csv", "w", newline="")
	csv_w = csv.writer(csv_file, delimiter=",")
	t = [["Movies", "Rotten Tomatoes", "Cast", "Critics"]] # the title (optional)
	csv_w.writerows(t)
	
	# table like display
	print("\n"+"-"*72)
	print(Fore.RED+" ROTTEN TOMATOES %"+Fore.WHITE+" |		 	MOVIES 				 				")
	print(""-"*72")
	print("		   |")

	for m in movies:
		m = m.replace(" ", "_").replace("'", "") # replace spaces w/ _ and ' w/ nothing
		# this allow me to get only the name, not the extension
		name = m.split(".")

		req = r.get(BASE_URL+str(name[0]))
		cont = req.content
		html = bs(cont, "html.parser")
		elem = html.find("span", attrs={"itemprop": "ratingValue"})
		critic = html.find("p", attrs={"class": "critic_consensus"})
		cast = html.find("div", attrs={"class": "media-body"})

		# Make a nice command line display of the results
		colors = ['green','yellow','red']
		
		try:
			#write in a csv file
			d = [[str(name[0]), str(elem.get_text()), str(cast.get_text()), str(critic.get_text())]]
			csv_w.writerows(d)
			
			
			# color the result in green, yellow or red according to its % and display it table like

			if int(elem.get_text())> 70:
				print(" "+color(str(elem.get_text()), colors[0])+"%		   |			"+str(name[0]))
				#print(str(critic.get_text())+"\n"+"-"*72)
			elif int(elem.get_text()) < 70 and int(elem.get_text()) > 40:
				print(" "+color(str(elem.get_text()), colors[1])+"%		   |			"+str(name[0]))
				#print(str(critic.get_text())+"\n"+"-"*72)
			elif int(elem.get_text()) < 40:
				print(Style.BRIGHT+" "+color(str(elem.get_text()), colors[2])+"%		   |			"+str(name[0]))
				#print(str(critic.get_text())+"\n"+"-"*72)
			
			

			rank_file.write(str(name[0])+" ["+str(elem.get_text())+"]\n")
			

		except:
			print(" "+color(':(', 'grey', attrs=['bold'])+"		   |			"+str(name[0]))
			err = str(name[0])+" [not rated :/]"
			rank_file.write(err+"\n")

	rank_file.close()

rate()
