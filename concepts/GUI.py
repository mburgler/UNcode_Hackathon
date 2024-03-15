# import tkinter as tk
# from tkinter import ttk
# from AppConfigClass import AppConfig

# # class SimpleGUI:
# #     def __init__(self, master):
# #         self.master = master
# #         master.title("UNCode Classification")

# #         self.label = ttk.Label(master, text="Enter Project ID or Select Filters:")
# #         self.label.pack()

# #         self.entry = ttk.Entry(master)
# #         self.entry.pack()

# #         self.greet_button = ttk.Button(master, text="Classify", command=self.classify)
# #         self.greet_button.pack()

# #         self.close_button = ttk.Button(master, text="Close", command=master.quit)
# #         self.close_button.pack()

# #     def classify(self):
# #         project_id = self.entry.get()
# #         print(f"Classifying project with ID: {project_id}")
# #         # Placeholder for classification logic
# #         # You would replace this print statement with your actual classification logic

# # def main(app_config):
# #     if app_config.use_gui:
# #         root = tk.Tk()
# #         gui = SimpleGUI(root)
# #         root.mainloop()
# #     else:
# #         # Console-based interface logic here
# #         print("Running in console mode.")
# #         # Your console-based application logic goes here

# # if __name__ == "__main__":
# #     config_file_path = '../settings.ini' # Update this to the path of your .ini file
# #     app_config = AppConfig(config_file_path)
# #     main(app_config)

# import tkinter as tk
# from tkinter import ttk
# from AppConfigClass import AppConfig

# import json

# def parse_json_for_filters(json_file_path):
#     with open(json_file_path, 'r') as file:
#         data = json.load(file)

#     countries = set()
#     sectors = set()
#     for project in data:
#         for country_detail in project["recipient-country-details"]:
#             countries.add(country_detail["recipient-country"])
#         sectors.add(project["sector"])

#     # Remove 'nan' entries if present
#     countries.discard('nan')
#     sectors.discard('nan')
    
#     return list(countries), list(sectors)

# # Assuming your JSON data is in 'projects.json'
# countries, sectors = parse_json_for_filters('../provided_data/project-dataset.json')


# class SimpleGUI:
#     def __init__(self, master, countries, sectors):
#         self.master = master
#         master.title("UNCode Classification")

#         ttk.Label(master, text="Enter Project ID:").pack()
#         self.entry = ttk.Entry(master)
#         self.entry.pack()

#         ttk.Label(master, text="Or Select Filters:").pack()

#         self.country_combobox = ttk.Combobox(master, values=countries, state="readonly")
#         self.country_combobox.bind('<Button-1>', lambda event: self.country_combobox.focus())
#         self.country_combobox.set("Select Country")
#         self.country_combobox.pack()

#         self.sector_combobox = ttk.Combobox(master, values=sectors, state="readonly")
#         self.sector_combobox.bind('<Button-1>', lambda event: self.sector_combobox.focus())
#         self.sector_combobox.set("Select Sector")
#         self.sector_combobox.pack()

#         ttk.Button(master, text="Classify", command=self.classify).pack()
#         ttk.Button(master, text="Close", command=master.quit).pack()

#     def classify(self):
#         project_id = self.entry.get()
#         selected_country = self.country_combobox.get()
#         selected_sector = self.sector_combobox.get()
#         print(f"Classifying project with ID: {project_id}, Country: {selected_country}, Sector: {selected_sector}")
#         # Add your classification logic here

# def main(app_config):
#     if app_config.use_gui:
#         root = tk.Tk()
#         countries, sectors = parse_json_for_filters('../provided_data/project-dataset.json')  # Make sure to use the correct path to your JSON file
#         gui = SimpleGUI(root, countries, sectors)
#         root.mainloop()
#     else:
#         print("Running in console mode.")
#         # Console logic here

# if __name__ == "__main__":
#     config_file_path = '../settings.ini'
#     app_config = AppConfig(config_file_path)
#     main(app_config)
