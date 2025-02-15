from dotenv import load_dotenv
from src.controllers.elsapy_controller import ElsapyController
import os

def main():
    load_dotenv()
    elsevier_api_key = os.getenv("ELSEVIER_API_KEY")
    elsapy_controller = ElsapyController(elsevier_api_key)
    elsapy_query = elsapy_controller.create_query(boolean_operators="(underwater simulation) OR (subaquatic simulation)", publication_year="> 2015")
    print(elsapy_query)
    response = elsapy_controller.doc_search(query=elsapy_query, database="scopus")
    print(response)

if __name__ == "__main__":
    main()