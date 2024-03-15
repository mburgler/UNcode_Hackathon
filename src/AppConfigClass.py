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

import configparser
import os

class AppConfigError(Exception):
    """Custom exception for AppConfig errors."""
    pass

class AppConfig:
    def __init__(self, path_config_file):
        self.config = configparser.ConfigParser()
        self.config.read(path_config_file)

        try:
            # SETTINGS
            self.use_gui = self.get_config_boolean('SETTINGS', 'UseGUI')
            self.debug = self.get_config_boolean('SETTINGS', 'DebugMode')
            
            # CLASSIFICATION METHOD
            self.use_openai_generative_ai = self.get_config_boolean('CLASSIFICATION METHOD', 'UseOpenAI_GenerativeAI')
            self.use_zero_shot = self.get_config_boolean('CLASSIFICATION METHOD', 'UseZeroShotApproach')
            self.use_generative_ai = self.get_config_boolean('CLASSIFICATION METHOD', 'UseGenerativeAI')
            self.use_open_api_data = self.get_config_boolean('CLASSIFICATION METHOD', 'UseOpenAPIDataIfNoDataProvided')
            self.criteria = self.get_config_value('CLASSIFICATION METHOD', 'ClassifyBy').lower()
            self.criteria_sdgs = False
            self.criteria_focus_areas = False
            self.criteria_priorities = False
            if self.criteria == "sdgs" or self.criteria == "all":
                self.criteria_sdgs = True
            if self.criteria == "focus areas" or self.criteria == "all":
                self.criteria_focus_areas = True
            if self.criteria == "priorities" or self.criteria == "all":
                self.criteria_priorities = True
            
            # API KEYS
            self.openai_model = self.get_config_value('LLM DETAILS', 'OpenAI_Model')
            self.openai_nmb_tokens = self.get_config_value('LLM DETAILS', 'OpenAI_NmbOfTokens')
            self.openai_key = self.get_config_value('LLM DETAILS', 'OpenAI_Key')
            self.zeroshot_huggingfaceapi_url = self.get_config_value('LLM DETAILS', 'ZeroShot_HuggingfaceAPI_URL')
            self.zeroshot_huggingfaceapi_token = self.get_config_value('LLM DETAILS', 'ZeroShot_HuggingfaceAPI_Token')
        except AppConfigError as e:
            print(f"Configuration Error: {e}")
            exit()

    def get_config_boolean(self, section, option):
        try:
            return self.config.getboolean(section, option)
        except ValueError:
            raise AppConfigError(f"The value for '{option}' in section '{section}' is not a boolean.")
        except (configparser.NoOptionError, configparser.NoSectionError) as e:
            raise AppConfigError(f"Missing or incorrect configuration: {e}")

    def get_config_value(self, section, option):
        try:
            value = self.config.get(section, option)
        except (configparser.NoOptionError, configparser.NoSectionError) as e:
            raise AppConfigError(f"Missing or incorrect configuration: {e}")
        if not value.strip():
            raise AppConfigError(f"The value for '{option}' in section '{section}' cannot be empty.")
        return value

    def print_config(self):
        # Your existing print_config method
        pass
