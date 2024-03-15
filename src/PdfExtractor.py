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

import fitz  # PyMuPDF
import os
def pdf_extractor(url, project_id):
	def download_pdf(url, filename):
		import requests
		response = requests.get(url)
		with open(filename, 'wb') as f:
			f.write(response.content)

	def extract_text_from_pdf(filename):
		text = ""
		with fitz.open(filename) as doc:
			for page in doc:
				text += page.get_text()
		return text

	try:
		filename = "tmpFile_" + str(project_id)
		#url.split("/")[-1].replace(" ", "_")

		download_pdf(url, filename)
		text = extract_text_from_pdf(filename)

		# Optional
		os.remove(filename)


		return(text)
	except Exception as e:
		return ""

#Testing
#print(pdf_extractor("https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", 0))