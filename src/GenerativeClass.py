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

import openai
from FetchData import local_fetch_json_nopoints
import json

class GenerativeTool:
	def __init__(self, app_config, path_prompts, path_focusAreas, path_priorities, path_sdgs):
		self.app_config = app_config
		openai.api_key = self.app_config.openai_key
		self.token_limit = self.app_config.openai_nmb_tokens
		self.path_prompts = path_prompts
		self.path_focusAreas = path_focusAreas
		self.path_priorities = path_priorities
		self.path_sdgs = path_sdgs

	def generative_classifier(self, path, summary, title):
		with open(self.path_prompts, 'r') as file:
			prompts = json.load(file)
		
		criteria = local_fetch_json_nopoints(path)["criterium"]
		criteria_descriptions = " ".join([c["goal"] + ": " + c["description"] for c in criteria])
		system_prompt = prompts['classification'][0]['system_prompt']
		user_prompt_propotype = prompts['classification'][0]['user_prompt']  # Assuming this is the correct key name

        # Constructing the final user prompt with the title, summary, and criteria descriptions
		user_prompt = user_prompt_propotype + "\nCRITERIA: '''" + criteria_descriptions + "'''\n" + "TEXT TO CLASSIFY: '''" + summary + "'''"
		if(self.app_config.debug == True):
			print("\nDEBUG in generative_classifier():\n", user_prompt)
		classification = self.call_classification_query(system_prompt, user_prompt)
		return(classification)

	def call_classification_query(self, system_prompt, user_prompt):
		response = openai.ChatCompletion.create(
			model=self.app_config.openai_model,
			messages=[
				{"role": "system", "content": system_prompt},
				{"role": "user", "content": user_prompt}
			]
		)
		summary = response.choices[0].message['content']
		return summary
