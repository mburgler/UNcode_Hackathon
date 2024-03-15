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

import json
from FetchData import *
from PdfExtractor import *
from SummariseClass import SummarisationTool
from ZeroShotClass import ZeroShotTool
from GenerativeClass import GenerativeTool

class Project:
	def __init__(self, project_id, project_api_data, matched_dataset, matched_documents, path_prompts):
		project_data = json.loads(project_api_data)
	
		# Setting data from the open API
		if(project_id):
			self.id = project_id
		else:
			exit()
		if(project_data):
			self.api_actual_end_date = self._catch_empty(project_data.get("actualEndDate"))
			self.api_actual_start_date = self._catch_empty(project_data.get("actualStartDate"))
			self.api_description = self._catch_empty(project_data.get("description", "")).strip()
			self.api_display_year = self._catch_empty(project_data.get("displayYear"))
			self.api_donors = self._catch_empty(project_data.get("donors"))
			self.api_end_date = self._catch_empty(project_data.get("endDate"))
			self.api_external_id = self._catch_empty(project_data.get("externalId"))
			self.api_financials = self._catch_empty(project_data.get("financials"))
			self.api_funds = self._catch_empty(project_data.get("funds"))
			self.api_grants = self._catch_empty(project_data.get("grants"))
			self.api_is_multi_country = self._catch_empty(project_data.get("isMultiCountry"))
			self.api_is_operationally_closed = self._catch_empty(project_data.get("isOperationallyClosed"))
			self.api_kpis = self._catch_empty(project_data.get("kpis"))
			self.api_location = self._catch_empty(project_data.get("location"))
			country_data = project_data.get("location")
			if country_data:
				self.api_long = self._catch_empty(country_data.get("long"))
				self.api_lat = self._catch_empty(country_data.get("lat"))
				self.api_iso2 = self._catch_empty(country_data.get("iso2"))
			self.api_long_title = self._catch_empty(project_data.get("longTitle"))
			self.api_media = self._catch_empty(project_data.get("media"))
			self.api_ongoing_in = self._catch_empty(project_data.get("ongoingIn"))
			self.api_outcomes = self._catch_empty(project_data.get("outcomes"))
			self.api_project_manager = self._catch_empty(project_data.get("projectManager"))
			self.api_quality_rating = self._catch_empty(project_data.get("qualityRating"))
			self.api_risks = self._catch_empty(project_data.get("risks"))
			self.api_search_tag = self._catch_empty(project_data.get("searchTag"))
			self.api_start_date = self._catch_empty(project_data.get("startDate"))
			self.api_status = self._catch_empty(project_data.get("status"))
			self.api_thematic = self._catch_empty(project_data.get("thematic"))
			self.api_title = self._catch_empty(project_data.get("title"))
			#Checking for missing KPIs
			self.api_KPI_missing = not all([self.api_title, self.api_description, self.api_actual_start_date])
			self.api_Failsafe = False
		else:
			self.api_Failsafe = True

		# Setting Data from Project-Dataset
		if(matched_dataset):
			self.pData_project_title = self._catch_empty(matched_dataset.get("project-title"))
			self.pData_sector = self._catch_empty(matched_dataset.get("sector"))
			self.pData_project_start = self._catch_empty(matched_dataset.get("project-start"))
			self.pData_project_end = self._catch_empty(matched_dataset.get("project-end"))
			self.pData_project_category = self._catch_empty(matched_dataset.get("project-category"))
			self.pData_project_subcategory = self._catch_empty(matched_dataset.get("project-subcategory"))
			self.pData_total_budget = self._catch_empty(matched_dataset.get("total-budget($)"))
			self.pData_total_expenditure = self._catch_empty(matched_dataset.get("total-expenditure($)"))
			self.pData_recipient_country_details = self._catch_empty(matched_dataset.get("recipient-country-details", []))
			self.pData_donor_details = self._catch_empty(matched_dataset.get("donor-details", []))
			self.pData_Failsafe = False
		else:
			self.pData_Failsafe = True
		
		# Setting Data from Project_document
		if(matched_documents):
			self.pDoc_list = []
			for document in matched_documents:
				extracted_text = self._catch_empty(pdf_extractor(self._catch_empty(document.get('url')), self.id))
				document_failsafe = not bool(extracted_text)
				pDoc_list = {
					'pDoc_file_name': self._catch_empty(document.get('FileName')),
					'pDoc_data_id': self._catch_empty(document.get('DataID')),
					'pDoc_modify_date': self._catch_empty(document.get('ModifyDate')),
					'pDoc_url': self._catch_empty(document.get('url')),
					'pDoc_text': extracted_text,
					'pDoc_Failsafe': document_failsafe
				}
				self.pDoc_list.append(pDoc_list)
			self.pDoc_Failsafe = False
		else:
			self.pDoc_Failsafe = True

		self.aggregated_summary = ""
		self.summary = ""
		self.path_prompts = path_prompts
		self.path_focusAreas=""
		self.path_priorities=""
		self.path_sdgs=""

		self.zeroshot_focus_area_results=""
		self.zeroshot_priority_results=""
		self.zeroshot_sdg_results=""
		self.generative_focus_area_results=""
		self.generative_priority_results=""
		self.generative_sdg_results=""

	def summarise(self, app_config):
		summarisation_tool = SummarisationTool(app_config, self.path_prompts)
		individual_summaries = []

		if(self.pDoc_Failsafe == True):
			print("Could not generate summary, no readable project documents ...")
			if(app_config.use_open_api_data == True and self.api_Failsafe == False):
				print("Resorting to Open API Data as alternative as specified in settings ... ")
				print("Open API Data successfully retrieved and used for classification ... ")
				self.aggregated_summary = self.api_long_title + "\n" + self.api_description			
			elif(app_config.use_open_api_data == True and self.api_Failsafe == True):
				print("Resorting to Open API Data as alternative as specified in settings ... ")
				print("Open API Data could not be retrieved ... ")
			else:
				print("Open API Data not specified as alternative in settings ... ")
				self.aggregated_summary =""
			print()
			return (self.aggregated_summary)
		functioning_documents = [doc for doc in self.pDoc_list if not doc['pDoc_Failsafe']]
		if len(functioning_documents) == 1:
			method = "one_doc"
		elif len(functioning_documents) > 1:
			method = "multi_doc"
		else:
			method = None

		for document in functioning_documents:
			text_to_summarize = document['pDoc_text']
			summary = summarisation_tool.summarise(text_to_summarize, document['pDoc_file_name'], method=method)
			document['pDoc_summary'] = summary
			if (len(functioning_documents) > 1):
				formatted_summary = f"\n{document['pDoc_file_name']}:{summary}"
				individual_summaries.append(formatted_summary)
			else:
				individual_summaries.append(summary)
		if len(individual_summaries) > 1: # multiple summaries, concatenate and summarize again
			concatenated_summaries = "\n".join(individual_summaries)
			self.aggregated_summary = summarisation_tool.summarise(concatenated_summaries, method="summary_of_summaries")
		elif len(individual_summaries) == 1:
			self.aggregated_summary = individual_summaries[0]
		else:
			self.aggregated_summary = ""
		if(app_config.debug == True):
			print("\nDEBUG in summarise():\n")
			print("ALL SUMMARIES: ",individual_summaries)
		return (self.aggregated_summary)
	
	def	classifier(self, app_config, path_focusAreas, path_priorities, path_sdgs):
		if(self.aggregated_summary == ""):
			print("Can not classify, no data ...")
			return
		if(app_config.use_zero_shot == False and app_config.use_generative_ai == False):
			print("Can not classify, both, zero shot and generative AI, deactivated in settings ...")
			return
		self.path_focusAreas = path_focusAreas
		self.path_priorities = path_priorities
		self.path_sdgs = path_sdgs

		if(self.pData_Failsafe == False and self.pData_project_title):
			title = self.pData_project_title
		elif(self.api_Failsafe == False and self.api_title):
			title = self.api_title
		else:
			title = "N/A"
		if(app_config.use_zero_shot == True):
			zeroshot_tool = ZeroShotTool(app_config, self.path_prompts, self.path_focusAreas, self.path_priorities, self.path_sdgs)
			if app_config.criteria_sdgs:
				print("Classifying SDGs with ZeroShot ...")
				self.zeroshot_sdg_results = zeroshot_tool.zero_shot_classifier(self.path_sdgs, self.aggregated_summary, title)
				if(app_config.debug == True):
					print("\nDEBUG for zeroshot_sdg_results:\n")
					print(self.zeroshot_sdg_results)
			if app_config.criteria_focus_areas:
				print("Classifying Focus Areas with ZeroShot ...")
				self.zeroshot_focus_area_results = zeroshot_tool.zero_shot_classifier(self.path_focusAreas, self.aggregated_summary, title)
				if(app_config.debug == True):
					print("\nDEBUG for zeroshot_focus_area_results:\n")
					print(self.zeroshot_focus_area_results)
			if app_config.criteria_priorities:
				print("Classifying Priorities with ZeroShot ...")
				self.zeroshot_priority_results = zeroshot_tool.zero_shot_classifier(self.path_priorities, self.aggregated_summary, title)
				if(app_config.debug == True):
					print("\nDEBUG for zeroshot_priority_results:\n")
					print(self.zeroshot_priority_results)
		if(app_config.use_generative_ai == True):
			generative_tool = GenerativeTool(app_config, self.path_prompts, self.path_focusAreas, self.path_priorities, self.path_sdgs)
			if app_config.criteria_sdgs:
				print("Classifying SDGs and generating justification note with GenerativeAI ...")
				self.generative_sdg_results = generative_tool.generative_classifier(self.path_sdgs, self.aggregated_summary, title)
				if(app_config.debug == True):
					print("\nDEBUG for generative_sdg_results:\n")
					print(self.generative_sdg_results)
			if app_config.criteria_focus_areas:
				print("Classifying Focus Areas and generating justification note with GenerativeAI ...")
				self.generative_focus_area_results = generative_tool.generative_classifier(self.path_focusAreas, self.aggregated_summary, title)
				if(app_config.debug == True):
					print("\nDEBUG for generative_focus_area_results:\n")
					print(self.generative_focus_area_results)
			if app_config.criteria_priorities:
				print("Classifying Priorities and generating justification note with GenerativeAI ...")
				self.generative_priority_results = generative_tool.generative_classifier(self.path_priorities, self.aggregated_summary, title)
				if(app_config.debug == True):
					print("\nDEBUG for generative_priority_results:\n")
					print(self.generative_priority_results)

	def create_json(self, app_config):
		if(self.aggregated_summary == ""):
			return
		data_structure = {
			"project-id": self.id,
			"project_description": self.aggregated_summary,  # Assuming 'self.aggregated_summary' contains the description
			# Update the dataset
			"project_start": self.pData_project_start if self.pData_project_start else None,
			"project_end": self.pData_project_end if self.pData_project_end else None,
			"project_title": self.pData_project_title if self.pData_project_title else None,
			"sector": self.pData_sector if self.pData_sector else None,
			"project_start": self.pData_project_start if self.pData_project_start else None,
			"project_end": self.pData_project_end if self.pData_project_end else None,
			"project_category": self.pData_project_category if self.pData_project_category else None,
			"project_subcategory": self.pData_project_subcategory if self.pData_project_subcategory else None,
			"total_budget": self.pData_total_budget if self.pData_total_budget else None,
			"total_expenditure": self.pData_total_expenditure if self.pData_total_expenditure else None,
			"recipient_country_details": self.pData_recipient_country_details if self.pData_recipient_country_details else None,
			"donor_details": self.pData_donor_details if self.pData_donor_details else None,
			"classification_results": {
				"ZeroShot": {
					"UsedModel" : app_config.zeroshot_huggingfaceapi_url,
					"SDGs": self.zeroshot_sdg_results if app_config.criteria_sdgs else None,
					"Focus_Areas": self.zeroshot_focus_area_results if app_config.criteria_focus_areas else None,
					"Priorities": self.zeroshot_priority_results if app_config.criteria_priorities else None
				},
				"GenerativeAI": {
					"UsedModel" : app_config.openai_model,
					"SDGs": self.generative_sdg_results if app_config.criteria_sdgs else None,
					"Focus_Areas": self.generative_focus_area_results if app_config.criteria_focus_areas else None,
					"Priorities": self.generative_priority_results if app_config.criteria_priorities else None
				}
			}
		}

		json_data = json.dumps(data_structure, indent=4)
		filename = f'results_{self.id}.json'
		with open(filename, 'w') as file:
			file.write(json_data)
		print()
		print("*** Created .json file called ", filename, " ***")


	# Print basic project info
	def print_class_info(self):
		print("*** OVERVIEW ***\n#api ------------------------------------")
		if(self.api_Failsafe == True):
			print("NO API INFO")
		else:
			print(f"Project ID: {self.id}")
			print(f"Title: {self.api_title}")
			print(f"Country: {self.api_iso2}")
			print(f"Description: {self.api_description}")
			print(f"Start Date: {self.api_actual_start_date} - End Date: {self.api_actual_end_date}")
			print(f"KPI missing: {self.api_KPI_missing}")
			print(f"Failsafe: {self.api_Failsafe}")
		print("#PData ------------------------------------")
		if(self.pData_Failsafe == True):
			print("NO DATASET INFO")
		else:
			print(f"Project ID: {self.pData_project_title}")
		print("#pDoc ------------------------------------")
		if(self.pDoc_Failsafe == True):
			print("NO DOCUMENT INFO")
		else:
			print("Document URLs:")
			for document in self.pDoc_list:
				print("*** URL ***")
				print(document['pDoc_url'])
				print(document['pDoc_Failsafe'])
		print("------------------------------------")
		if(self.aggregated_summary):
			print("SUMMARY: ", self.aggregated_summary)
    
	# Private method to handle empty values
	def _catch_empty(self, value):
		return value if value else ""
