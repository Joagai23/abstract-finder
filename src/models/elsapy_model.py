import json

class ScopusModel:
    def __init__(self):
        self.uri = ""
        self.title = ""
        self.author = ""
        self.date = ""
        self.origin = "Scopus"

    def set_uri(self, uri):
        self.uri = uri

    def set_title(self, title):
        self.title = title

    def set_author(self, author):
        self.author = author
    
    def set_date(self, date):
        self.date = date

    def to_json(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)