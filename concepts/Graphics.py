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

import matplotlib.pyplot as plt
import numpy as np
import json
import os
import textwrap

def	graphics_zeroshot_only(data_structure):

	# Extracting ZeroShot SDG results
	zero_shot_sdgs = data_structure["classification_results"]["ZeroShot"]["SDGs"]

	# Preparing data for plotting
	labels = [sdg[0].split(":")[0] for sdg in zero_shot_sdgs]  # SDG numbers
	scores = [sdg[1] for sdg in zero_shot_sdgs]  # Corresponding scores

	# Creating the bar chart
	fig, ax = plt.subplots()
	y_pos = np.arange(len(labels))
	ax.barh(y_pos, scores, align='center')
	ax.set_yticks(y_pos)
	ax.set_yticklabels(labels)
	ax.invert_yaxis()  # Invert the Y-axis so the highest value is on top
	ax.set_xlabel('Scores')
	ax.set_title('ZeroShot SDG Classification Results')

	plt.show()

def local_fetch_json(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def graphics_combined(data_structure):

	# Extracting data for plotting
	zero_shot_sdgs = data_structure["classification_results"]["ZeroShot"]["SDGs"]
	labels = [sdg[0].split(":")[0] for sdg in zero_shot_sdgs]  # Extracting SDG numbers/names
	scores = [sdg[1] for sdg in zero_shot_sdgs]  # Extracting corresponding scores

	# GenerativeAI text output
	generative_ai_output = data_structure["classification_results"]["GenerativeAI"]["SDGs"]
	# Wrapping text for better display
	wrapped_text = textwrap.fill(generative_ai_output, width=70)

	# Creating the plot
	fig, ax = plt.subplots(figsize=(12, 6))
	y_pos = np.arange(len(labels))

	# Bar chart for ZeroShot results
	ax.barh(y_pos, scores, color='skyblue')
	ax.set_yticks(y_pos)
	ax.set_yticklabels(labels)
	ax.invert_yaxis()  # Highest values at the top
	ax.set_xlabel('Scores')
	ax.set_title('ZeroShot SDG Classification Results')

	# Text box for GenerativeAI output
	# Calculate the box height dynamically based on the number of lines in wrapped text
	box_height = max(len(wrapped_text.split('\n')) / len(labels), 1)
	text_box_props = dict(boxstyle='round', facecolor='lightgrey', alpha=0.5)
	ax.text(1.05, 0.5, wrapped_text, transform=ax.transAxes, fontsize=10, verticalalignment='center', bbox=text_box_props, wrap=True)

	plt.tight_layout()
	plt.show()



data = local_fetch_json("results_170162.json")
graphics_combined(data)
