#! /usr/bin/env python

"""
Generates random links based on a prefix.
usage: ./rp.py -p <f3> -r 200  
"""

import urllib2
from urllib2 import Request
import re
import time
import signal
import sys
import os
import random
import string
import urlparse
import argparse
from msvcrt import putch, getch

# Detects Ctrl+C command
def signal_handler(signal, frame):
	print('[*] Ctrl+C detected! Aborting...')
	sys.exit(0)

# Creates random url
def randomstring(pref):
	return 'http://prnt.sc/' + pref + ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(4))

# Creates folder to save images
if not os.path.isdir('images-light'):
   os.makedirs('images-light')
   
def main():
	parser = argparse.ArgumentParser(description="Get random images from lightshot", prog="rp")
	parser.add_argument("-p", dest="prefix", help="Prefix to use", required=True)
	parser.add_argument("-r", dest="results", help="Max number of results", required=True, type=int)
	options = parser.parse_args()
	print "[*] Finding Images..."
	a = range(0, options.results)
	for i in a:
		signal.signal(signal.SIGINT, signal_handler)
		link = randomstring(options.prefix)
		file_name= link.split("/")[-1]
		opener = urllib2.build_opener()
		opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36')]
		response = opener.open(link)
		html = response.read()
		time.sleep( 1 )
		m = re.search(r"<meta property=\"og:image\" content=\"(.+).png\"/>", html)
		print('[*] Trying id: ' + link)
		if m:
			try:
				final_link = m.group(1) + '.png'
				opener_file = urllib2.build_opener()
				opener_file.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36')]
				response_file = opener_file.open(final_link)
				with open('images-light\\' + file_name + '.png', 'wb') as output:
					output.write(response_file.read())
				print('	Found image with id ' + file_name)
			except ValueError:
				print('	Error downloading image with id ' + file_name)		
		else:
			print('	No image with id ' + file_name)	
	print("[*] Download complete!")
main()