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
from datetime import datetime

def start_up():
    print_header_from_json("../our_data/header_data.json", "header_welcome")
    check_internet_connection()
    check_file_readability("../provided_data/project-dataset.json",
                           "../provided_data/project-documents.json",
                           "../settings.ini",
                           "../our_data/prompts.json",
                           "../our_data/classification_focusAreas.json",
                           "../our_data/classification_priorities.json",
                           "../our_data/classification_sdgs.json")


def filter_projects(projects, country=None, start_date=None, end_date=None, min_budget=None):
    filtered_projects = []
    for project in projects:
        if country and project["recipient-country-details"][0]["recipient-country-code"] != country:
            continue
        if min_budget and float(project["total-budget($)"]) < min_budget:
            continue
        if start_date and datetime.strptime(project["project-start"], "%m/%d/%Y") < start_date:
            continue
        if end_date and datetime.strptime(project["project-end"], "%m/%d/%Y") > end_date:
            continue
        filtered_projects.append(project["project-id"])
    return filtered_projects

def get_user_input(prompt, type=None, allow_all=True):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == 'all' and allow_all:
            return None
        if type == 'date':
            try:
                return datetime.strptime(user_input, "%m/%d/%Y")
            except ValueError:
                print("Invalid date format. Please use MM/DD/YYYY.")
        elif type == 'float':
            try:
                return float(user_input)
            except ValueError:
                print("Invalid number. Please enter a valid number.")
        else:
            return user_input.upper()

def main():
    start_up()

    # Paths
    path_project_datasets = "provided_data/project-dataset.json"
    path_project_documents = "provided_data/project-documents.json"
    path_config_file = "../settings.ini"
    path_prompts = "../our_data/prompts.json"
    path_focusAreas = "../our_data/classification_focusAreas.json"
    path_priorities = "../our_data/classification_priorities.json"
    path_sdgs = "../our_data/classification_sdgs.json"
    projects = local_fetch_json(path_project_datasets)
    app_config = AppConfig(path_config_file)

    # Define filters in code
    # country_code = "RW"  # Example: Filter by Rwanda
    # start_date = datetime(2018, 1, 1)  # Example: Projects starting after January 1, 2019
    # end_date = datetime(2024, 6, 30)  # Example: Projects ending before June 30, 2024
    # min_budget = 100000  # Example: Projects with a budget over 100,000

    # Prompt User for Filter
    country_code = get_user_input("Enter country code (or 'all' to skip): ", allow_all=True)
    start_date = get_user_input("Enter start date (MM/DD/YYYY) or 'all' to skip: ", type='date', allow_all=True)
    end_date = get_user_input("Enter end date (MM/DD/YYYY) or 'all' to skip: ", type='date', allow_all=True)
    min_budget = get_user_input("Enter minimum budget or 'all' to skip: ", type='float', allow_all=True)



    filtered_project_ids = filter_projects(projects, country=country_code, start_date=start_date, end_date=end_date, min_budget=min_budget)
    print("\nFiltered projects. The following projects meet all criteria:")
    print(", ".join(filtered_project_ids))
    # Process each filtered project
    for project_id_str in filtered_project_ids:

        print(f"*** \nProcessing project with the id {project_id_str} ***\n")

        # Fetch project data from API or local (this is a placeholder, adjust according to your data fetching logic)
        project_api_data = api_fetch_project(project_id_str)
        project_documents = local_fetch_json(path_project_documents)

        # Extracting data for individual project from the datasets
        matched_dataset = next((project for project in projects if project.get("project-id") == project_id_str), None)
        matched_documents = [doc for doc in project_documents if doc.get("proj_id") == project_id_str]

        # Initialize and process Project
        if matched_dataset:
            project = Project(int(project_id_str), json.dumps(project_api_data), matched_dataset, matched_documents, path_prompts)
            summary = project.summarise(app_config)
            project.classifier(app_config, path_focusAreas, path_priorities, path_sdgs)
            project.create_json(app_config)

            if app_config.debug:
                print("\nDEBUG in main():\n")
                project.print_class_info()
        else:
            print(f"Project data not found for ID: {project_id_str}")

# main
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by the user with KeyboardInterruption <3.")
    finally:
        print_header_from_json("../our_data/header_data.json", "header_bye")
