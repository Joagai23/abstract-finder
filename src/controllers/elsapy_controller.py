from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch
from ..models.elsapy_model import ScopusModel
import json

class ElsapyController:
    def __init__(self, api_key):
        self.client = ElsClient(api_key=api_key)

    def doc_search(self, query:str, database="scopus", get_all_results=False, entry_count=25) -> str:
        """
        Searches inside the Elsevier Databases given the input query.

        Args:
            query (str): Input data to send to the DDBB
            database (str): The online database to query. Must be one of:
                "scopus": Uses the Scopus search engine.
                "sciencedirect": Uses the Science Direct search engine (requires specialized API key).
                Defaults to "scopus".
            get_all_results (bool): If False (default), retrieves the default number of results specified for the API. If True, multiple API calls will be made to iteratively get all results for the search, up to a maximum of 5,000.
            entry_count (int): Defines the number of entries to look for it get_all_results == False.
                Defaults to 25.
        Returns:
            str: Json array containing Elsevier metadata entries.
        """
        # Create and execute Elsevier search
        doc_srch = ElsSearch(query=query, index=database)
        doc_srch.execute(self.client)
        print ("doc_srch has", len(doc_srch.results), "results.")
        
        # Create result array
        results = []
        # Get results from search and fill array
        for entry in doc_srch.results:
            scopus_object = self._create_scopus_object(entry)
            results.append(scopus_object.to_json())

        # Return results in JSON format
        return json.dumps(results)

    def create_query(self, boolean_operators="", affiliation="", author_name="", publication_year="", format = True) -> str:
        """
        Generates a search query compatible with Elsevier online libraries. For more documentation refer to https://dev.elsevier.com/sc_search_tips.html

        Args:
            boolean_operators (str): You can use Boolean operators (AND, OR, AND NOT) in your search. If you use more than one operator in your search, Scopus interprets your search according to the order of precedence (1. OR 2. AND 3. AND NOT). You can also use proximity operators (pre/n, w/n) with Boolean operators.
                Defaults to empty "". If empty, format is needed.
            affiliation (str): Institution or organization where research has been conducted.
                Defaults to empty "".
            author_name (str): The name of an author. This field finds variants for a single author name.
                Defaults to empty "".
            publication_year (str): Year of Publication. A numeric field indicating the year of publication.
                You can indicate the year using the following operators:
                    < Before
                    > After
                    = Equal to
                Defaults to empty "".
            format (bool): Whether the query must be formatted. If False the value of "boolean_operators" will be used as final query.
                Defaults to True.
        Returns:
            str: Elsevier query in str format.
        """
        # Initialize query to format
        query = boolean_operators
        # Format if necessary
        if format:
            # Check affiliation and if so append to query
            if affiliation != "":
                affiliation_str = " AND AFFIL(" + affiliation + ")"
                query = query + affiliation_str
            if author_name != "":
                author_str = " AND AUTHOR-NAME(" + author_name + ")"
                query = query + author_str
            if publication_year != "":
                year_str = " AND PUBYEAR " + publication_year
                query = query + year_str       
        # Return query and remove 'AND' from beggining if present
        return query[4:].lstrip() if query.startswith(" AND") else query

    def _create_scopus_object(self, query_item) -> ScopusModel:
        # Create Scopus object and fill with values from dict
        scopus_item = ScopusModel()
        # Title
        if "dc:title" in query_item:
            scopus_item.set_title(query_item["dc:title"])
        # Author
        if "dc:creator" in query_item:
            scopus_item.set_author(query_item["dc:creator"])
        # Date
        if "prism:coverDate" in query_item:
            scopus_item.set_date(query_item["prism:coverDate"])
        # Uri
        if "link" in query_item:
            for link_item in query_item["link"]:
                if "@ref" in link_item and link_item["@ref"] == "scopus" and "@href" in link_item :
                    scopus_item.set_uri(link_item["@href"])
                    break

        return scopus_item