# **************************************************************************** #
#                                                                              #
#    888     888 8888b   888                       888                         #
#    888     888 88888b  888                       888                         #
#    888     888 888Y88b 888  .d8888b .d88b.   .d88888  .d88b.                 #
#    888     888 888 Y88b888 d88P"   d88""88b d88" 888 d8P  Y8b                #
#    Y88b. .d88P 888   Y8888 Y88b.   Y88..88P Y88b 888 Y8PPPP                  #
#     "Y88888P"  888    Y888  "Y8888P "Y88P"   "Y88888  "Ybbbb.                #
#                                                                              #
#   By: UNexpectedOutput                                                       #
#       Franziska Adler, Clemens Bene, Matteo Buergler and Benjamin Michel     #
#   Contribution Dates: 2024/03/13 - 2024/03/14                                #
#                                                                              #
# **************************************************************************** #

import os
import requests
import sys
import json

def check_internet_connection():
	url='https://1.1.1.1'
	timeout=5
	try:
		response = requests.get(url, timeout=timeout)
		response.raise_for_status()
		print("Internet connection successfully established ...")
		return
	except (requests.ConnectionError, requests.Timeout, requests.HTTPError):
		print("No internet connection available. Exiting the program.")
	sys.exit(1)

def check_file_readability(*file_paths):
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"File does not exist: {file_path}")
            sys.exit(1)
        try:
            with open(file_path, 'r') as file:
                pass
        except IOError:
            print(f"File is not readable: {file_path}")
            sys.exit(1)
    print("All Files successfully retrieved ...\n")

def print_header_from_json(file_path, name):
	if not os.path.exists(file_path):
		print(f"File does not exist: {file_path}")
		sys.exit(1)
	try:
		with open(file_path, 'r') as file:
			pass
	except IOError:
		print(f"File is not readable: {file_path}")
		sys.exit(1)
	with open(file_path, 'r') as file:
		data = json.load(file)
		header = data[name]
		for line in header.split('\n'):
			print(line)
