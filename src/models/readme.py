
class Readme:
    
    def __init__(self, project_name, type, language, language_version, environments_versions, data_security,  depcheck=None):
        self.project_name = project_name
        self.type = type
        self.language = language
        self.language_version = language_version
        self.environments_versions = environments_versions
        self.data_security = data_security
        self.depcheck = depcheck
    
