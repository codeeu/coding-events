# -*- coding: utf-8 -*-
# This diploma generator read a list of names to
# fill a LaTeX template with a point for the name.
# Optinally, it can compile the LaTeX files and join them.
# If LaTeX errors are present, then press Enter.

print "Pyploma: Diploma generator for LaTeX and pdf.\n"

import sys
# Invoke terminal
from commands import *
import commands
def run_command(cmd):
	getstatusoutput(cmd)

if len(sys.argv) != 4:
	print "Usage: python pyploma.py \"Name To be Printed\" Event_ID\"Year"
else:
	name = str(sys.argv[1])
	filename = str(sys.argv[2])
	year = str(sys.argv[3])

	salida = open(filename + ".tex","w") # create a LaTeX file for each person in the list

	text = open("certi.tex") # open the LaTeX document
	text = text.read() # read it
	text_list = list(text) # transform it into a list

	y_name = text.find("%pointname") #search the point for name inclusion
	z_name = len("%pointname")+2
	text_list[y_name+z_name:y_name+z_name] = name # insert the name
	x_name = text.find("%pointyear") #search the point for year inclusion
	n_name = len("%pointyear")+4
	text_list[x_name+n_name:x_name+n_name] = year # insert the year

	text_final = "".join(text_list) # from list to string

	salida.write(text_final) # save changes in the created file
	salida.close() # closes the file

	run_command(str("pdflatex -interaction=nonstopmode " + filename + ".tex")) # compile LaTeX a pdf (optional)
	print name #control

	run_command(str("pdftk output*.pdf cat output todos_diplomas.pdf")) # create pdf with all the created diplomas (optional)

	print "\nAnd we are done! :-)" #control
