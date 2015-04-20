#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, os.path as op, re
import fileinput as fi
from glob import glob

all_files = [f for files in sys.argv[1:] for f in glob(files)]
f = fi.FileInput(all_files, openhook=fi.hook_encoded("iso-8859-1"))

try:
	for line in f:
		if f.isfirstline():
			datos = []
			print(op.basename(f.filename()) + '...')
			
			try:
				newfile.close()
			except NameError:
				pass
			
			nd = op.join(op.dirname(f.filename()), 'thm')
			try:
				if not op.isdir(nd):
					os.mkdir(nd)
				newfile = op.join(nd, re.findall('^(.+)\.[^\.]+$', op.basename(f.filename()))[0] + '.thm')
				newfile = open(newfile, 'w', encoding='utf8')
			except OSError as e:
				print('Error creating file (' + e.errno + '): ' + e.strerror)
				f.nextfile()
				continue
		
			datos.append(re.findall(r'^[^:]+:\s*(.+)$', line.strip())[0])
			print('Current list: ' + datos[0])
			print('''ListName\t{}
ListNickName\t
ListDescription\t'''.format(datos[0]), file=newfile)
		else:
			# Ignore empty lines...
			if not len(line.strip()):
				continue
				
			# And "members" line...
			nc = re.findall('^([^:]+):\s*$', line)
			if len(nc):
				continue

			contacto = re.compile(r'^([^\t]+)\t(.+)\s*$')
			nuevo_contacto = contacto.findall(line.strip())
			if len(nuevo_contacto):
				print('  {}\n    {}\n'.format(nuevo_contacto[0][0], nuevo_contacto[0][1]))
				datos.append(nuevo_contacto[0])
				print('{} <{}>'.format(nuevo_contacto[0][0], nuevo_contacto[0][1]), file=newfile)
	newfile.close()
	
except FileNotFoundError as e:
	print('ERR: ' + f.filename() + '...')
