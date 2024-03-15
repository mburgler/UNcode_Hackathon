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

import requests
import json
import os

# takes an endpoint and gives a json
def api_fetch_general(url, endpoint):
	full_url = url + "/" + endpoint
	response = requests.get(full_url)
	data = response.json()
	return data

# takes a projects external ID and gives a json
def api_fetch_project(project_id):
	url = "https://open.unido.org/api"
	full_url = url + "/projects/" + project_id
	response = requests.get(full_url)
	data = response.json()
	return data

# fetches a list of all projects 
def	api_fetch_all():
	url = "https://open.unido.org/api"
	endpoint = "projects"
	return (api_fetch_general(url, endpoint))

# open and read a local JSON file
def local_fetch_json(file_name):
    file_path = os.path.join(os.path.dirname(__file__), '..', file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def local_fetch_json_nopoints(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

#testing
def	test_print_project_fetch():
	project_id = "200017"
	result = api_fetch_project(project_id)
	print(result)

# grep description
# result = api_fetch_project("200017")['description']
# print(result)