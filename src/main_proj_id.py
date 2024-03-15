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

from FetchData import *
from ProjectClass import Project
from AppConfigClass import AppConfig
from Prerequisites import check_internet_connection, check_file_readability, print_header_from_json
import json

def start_up():
	print_header_from_json("../our_data/header_data.json", "header_welcome")
	check_internet_connection()
	check_file_readability("../provided_data/project-dataset.json", \
						"../provided_data/project-documents.json", \
						"../settings.ini", \
						"../our_data/prompts.json", \
						"../our_data/classification_focusAreas.json", \
						"../our_data/classification_priorities.json", \
						"../our_data/classification_sdgs.json")


def main():
	start_up()

	path_project_datasets="provided_data/project-dataset.json"
	path_project_documents="provided_data/project-documents.json"
	path_config_file="../settings.ini"
	path_prompts="../our_data/prompts.json"
	path_focusAreas="../our_data/classification_focusAreas.json"
	path_priorities="../our_data/classification_priorities.json"
	path_sdgs="../our_data/classification_sdgs.json"

	

	#loading config
	app_config = AppConfig(path_config_file)

	#get project id
	#project_id_str = "170162" #"120383" #"200322"
	project_id_str = input("Please enter a project ID: ")
	if(project_id_str == "exit"):
		exit()
	while not project_id_str.isdigit():
		print("Invalid project ID. Please enter a vaild number.")
		project_id_str = input("Enter project ID: ")
		if(project_id_str == "exit"):
			exit()
	print()
	project_id = int(project_id_str)

	#get project data
	project_api_data = api_fetch_project(project_id_str)
	project_datasets = local_fetch_json(path_project_datasets)
	project_documents = local_fetch_json(path_project_documents)

	#extracting data for individual project
	matched_dataset = next((project for project in project_datasets if project.get("project-id") == project_id_str), None)
	matched_documents = [doc for doc in project_documents if doc.get("proj_id") == project_id_str]

	project = Project(project_id, json.dumps(project_api_data), matched_dataset, matched_documents, path_prompts)
	summary = project.summarise(app_config)
	project.classifier(app_config, path_focusAreas, path_priorities, path_sdgs)
	project.create_json(app_config)

	#test printing
	if(app_config.debug == True):
		print("\nDEBUG in main():\n")
		project.print_class_info()

# main
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("\nProgram interrupted by the user with KeyboardInterruption <3.")
	finally:
		print_header_from_json("../our_data/header_data.json", "header_bye")

