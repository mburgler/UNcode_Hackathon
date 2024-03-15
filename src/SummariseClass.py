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
import json

class SummarisationTool:
	def __init__(self, app_config, path_prompts):
		self.app_config = app_config
		openai.api_key = self.app_config.openai_key
		self.token_limit = self.app_config.openai_nmb_tokens
		self.avg_chars_per_token = 4
		self.path_prompts = path_prompts
	
	def summarise(self, text, filename=None, method=None):
		with open(self.path_prompts, 'r') as file:
			prompts = json.load(file)
		cumulative_summary = ""
		remaining_text = text
		system_prompt = prompts['summarisation'][0]['system_prompt']
		if(method == "summary_of_summaries"):
			user_prompt = prompts['summarisation'][0]['user_sum_of_sum']
		else:
			user_prompt = prompts['summarisation'][0]['user_sum_general']
		print("Summarising ...")
		while remaining_text:
			if(cumulative_summary != ""):
				user_prompt = prompts['summarisation'][0]['user_continued_chunking'] + "\nPrior Summary: " + cumulative_summary + "\nCurrent Text: "
			else:
				user_prompt += " "
			estimated_tokens_for_next_chunk = int(self.token_limit) - self.estimate_tokens(system_prompt + user_prompt)
			next_chunk_size = estimated_tokens_for_next_chunk * self.avg_chars_per_token
			chunk, remaining_text = remaining_text[:next_chunk_size], remaining_text[next_chunk_size:]
			if not chunk:
				break
			user_prompt = user_prompt + chunk
			cumulative_summary = self.call_summarization_query(system_prompt, user_prompt)
			if(self.app_config.debug == True):
				print("\nDEBUG for SummarisationTool:\n")
				print("SYSTEMPROMPT", system_prompt)
				print("USER_PROMPT", user_prompt)
				print("LEN TEXT", len(text))
				print("LEN CHUNK", len(chunk))
				print("LEN CHUNK", len(remaining_text))
				print("CUMMULATIVE SUMMARY", cumulative_summary)
		return cumulative_summary

	def call_summarization_query(self, system_prompt, user_prompt):
		response = openai.ChatCompletion.create(
			model=self.app_config.openai_model,
			messages=[
				{"role": "system", "content": system_prompt},
				{"role": "user", "content": user_prompt}
			]
		)
		summary = response.choices[0].message['content']
		return summary

	def estimate_tokens(self, text):
		return len(text) // self.avg_chars_per_token


