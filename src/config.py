import os

# A class for holding the whole configuration of the project
class Config:
    # _instance = None

    # def __new__(cls):
    #     if cls._instance is None:
    #         cls._instance = super(Config, cls).__new__(cls)
    #         project_path = os.path.join(os.getcwd(), "web-scrapper")
    #         cls._instance.project_path = project_path
    #         # os.chdir(cls._instance.project_path)
    #         cls._instance.input_file_path = os.path.join(project_path, "input", "companies.txt")
    #         cls._instance.output_file_path = os.path.join(project_path, "output", "dog_cat_food_companies.csv")
    #     return cls._instance
    def __init__(self):
        project_path = os.path.join(os.getcwd(), "web-scrapper")
        self.project_path = project_path
        self.input_file_path = os.path.join(project_path, "input", "companies.txt")
        self.output_file_path = os.path.join(project_path, "output", "dog_cat_food_companies.csv")

    # @property
    # def project_path(self):
    #     return self.project_path
    
    # @project_path.setter
    # def project_path(self, path):
    #     self._project_path = path
    #     # Update related paths when the project path changes
    #     self._input_file_path = os.path.join(self._project_path, "input", "companies.txt")
    #     self._output_file_path = os.path.join(self._project_path, "output", "dog_cat_food_companies.csv")
    
    # @property
    # def input_file_path(self):
    #     return self.input_file_path
    
    # @input_file_path.setter
    # def input_file_path(self, path):
    #     self._input_file_path = path
    
    # @property
    # def output_file_path(self):
    #     return self.output_file_path
    
    # @output_file_path.setter
    # def output_file_path(self, path):
    #     self._output_file_path = path
