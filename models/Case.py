# models/Case.py
class Case:
    def __init__(self, case_id, investigator, base_path):
        self.case_id = case_id
        self.investigator = investigator
        self.base_path = base_path
        # TODO: load metadata or create new

    def get_folder(self, name):
        # TODO: return full path to named folder
        pass
