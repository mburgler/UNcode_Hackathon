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
from FetchData import local_fetch_json_nopoints
import json

class ZeroShotTool:
	def __init__(self, app_config, path_prompts, path_focusAreas, path_priorities, path_sdgs):
		self.app_config = app_config
		self.path_prompts = path_prompts
		self.path_focusAreas = path_focusAreas
		self.path_priorities = path_priorities
		self.path_sdgs = path_sdgs

	def zero_shot_classifier(self, path, summary, title):
		headers = {"Authorization": f"Bearer {self.app_config.zeroshot_huggingfaceapi_token}"}
		#headers = {"Authorization": "Bearer TOKEN_HERE"}
	

		def query(payload):
			response = requests.post(self.app_config.zeroshot_huggingfaceapi_url, headers=headers, json=payload)
			return response.json()

		def get_top_six(results):
				return sorted(results, key=lambda x: x[1], reverse=True)[:3]
		
		intermediate_top_results = []
		round_results = []
		criteria = local_fetch_json_nopoints(path)["criterium"]
		criteria_list = []
		for criteria in criteria:
			criteria_list.append(criteria["goal"] + ": " + criteria["description"])
		if len(criteria_list) > 10:
			# Split into two rounds if more than 10 SDGs
			split_index = len(criteria_list) // 2
			first_half, second_half = criteria_list[:split_index], criteria_list[split_index:]
			rounds = [first_half, second_half]
		else:
			rounds = [criteria_list]
		# Initial classification rounds
		nmb = 0
		description = "Title: " + title + "\n" + "Description: " + summary
		for round_criteria in rounds:
			output = query({
				"inputs": description,
				"parameters": {"candidate_labels": round_criteria},
			})
			if(self.app_config.debug == True):
				print("\nDEBUG for ZeroShotTool 1:\n")
				print("### OUTPUT ZEROSHOT: ", output)
				print("### HEADER ZEROSHOT: ", headers)
			#try except
			try:
				if output is not None and 'labels' in output and 'scores' in output:
					round_results = list(zip(output['labels'], output['scores']))
					top_six = get_top_six(round_results)
					intermediate_top_results.extend(top_six)
					if self.app_config.debug:
						print("\nDEBUG for ZeroShotTool 2:\n")
						self.print_tmp_output(output, nmb)
				else:
					raise ValueError("API response is missing expected data.")
			except Exception as e:
				print("Answer from API: ", output)
				print("HuggingFace API not working... this happens sometimes with Hugging Face. Try again later.")
				exit()
			# round_results = list(zip(output['labels'], output['scores']))
			# top_six = get_top_six(round_results)
			# intermediate_top_results.extend(top_six)
			# if(self.app_config.debug == True):
			# 	self.print_tmp_output(output, nmb)
			nmb += 1

		# Sort results by score in descending order

		# Third round for top 5 SDGs if more than 5 SDGs initially

		final_results = intermediate_top_results
		if len(rounds) > 1:
			top_candidates = [result[0] for result in intermediate_top_results]
			output = query({
				"inputs": description,
				"parameters": {"candidate_labels": top_candidates},
			})
			final_results = list(zip(output['labels'], output['scores']))
		if(self.app_config.debug == True):
			print("\nDEBUG for ZeroShotTool 3, *** FINAL RESULTS ***:\n")
			print(self.prettify(final_results))
		return final_results

	def prettify(self, data):
		print("\nClassification Results:\n")
		for label, score in data:
			print(f"- {label}: {score:.2%}")
				

	def print_tmp_output(self, data, nmb):
		print(f"\nTMP Results of {nmb} round:")
		for label, score in zip(data['labels'], data['scores']):
			print(f"- {label}: {score:.2%}")
		print()

	# if __name__ == "__main__":
	# 	main()
