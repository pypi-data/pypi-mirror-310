import requests
from rdflib import Graph, URIRef, Literal
import yaml
import os
import json
from urllib.parse import urlparse, urljoin
from pathlib import Path
from typing import Union

"""

"""


def triples_count():
    # query to count all triples
    query = """
    SELECT (COUNT(*) as ?triplesCount)
    WHERE { ?s ?p ?o }
    """


class kb_toolbox:  #fixme change to KbToolBox
    def __init__(self, service=None):
        """
        if service is none, the default one is used, other wise the specified one of exists
        the service is the name of the service in omikb.yml
        :param service:
        """

        service = service or "kb"

        with open(os.path.expanduser('~/omikb.yml'), 'r') as file:
            config = yaml.safe_load(file)

        self.query_iri = config["services"][service]["end_point"]["query"]
        self.update_iri = config["services"][service]["end_point"]["update"]
        self.data_iri = config["services"][service]["end_point"]["data"]
        self.ping_iri = config["services"][service]["end_point"]["ping"]
        self.stats_iri = config["services"][service]["end_point"]["stats"]

        self.hub_iri = config["jupyter"]["hub"]
        self.hub_token = config["jupyter"]["token"]

        print(f"token= {self.hub_token}")

        self.username = config["jupyter"]["username"]
        print(f"hub user name is {self.username}")
        self.hub_api_header = {
            'Authorization': f'token {self.hub_token}',
        }

        response = requests.get(f"{self.hub_iri}/hub/api/users/{self.username}", headers=self.hub_api_header)
        if response.status_code != 200:
            raise ConnectionError(
                f"Error connecting to Jupyter Hub/fetching user data Failed with: {response.status_code} - \
                      \nSorry, you are not able to use OMI - Contact Admin")

        user_data = response.json()
        auth_state = user_data.get('auth_state', {})
        access_token = auth_state.get('access_token', {})
        print(f"Hello {self.username}: Your access token is obtained: (Showing last 10 digits only) "
              f"{access_token[-10:]}")
        self.access_token = access_token = user_data['auth_state']['access_token']
        self.userinfo = user_data['auth_state']['oauth_user']

        self.omi_get_headers = {
            'Accept': "application/json",
            'Authorization': f'Bearer {access_token}'
        }
        # self.data_headers = self.omi_get_headers
        # self.data_headers['Content-Type'] = 'text/turtle'
        self.data_headers = {
            'Accept': "application/json",
            'Content-Type': 'text/turtle',
            'Authorization': f'Bearer {access_token}'
        }
        self.update_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/sparql-update',
            'Authorization': f"Bearer {access_token}"
        }
        self.ping_headers = self.omi_get_headers
        self.ping_headers["Content-Type"] = "application/x-www-form-urlencoded"

        print("Initialised Knowledge Base and OMI access from the jupyter interface for the user:")
        print(print(json.dumps(self.userinfo, indent=2)))

    def query(self, query):
        # note proper encoding, seems like response does not encode. 
        params = {'query': query}
        response = requests.post(self.query_iri, params=params, headers=self.omi_get_headers, timeout=50)
        return response

    def search_keyword(self, keyword):
        query = f"""
                SELECT ?s ?p ?o
                WHERE {{
                  ?s ?p ?o .
                  FILTER (regex(str(?s), "{keyword}", "i") ||
                          regex(str(?p), "{keyword}", "i") ||
                          regex(str(?o), "{keyword}", "i"))
                }}
                """
        # params = {'query': query}
        # response = requests.post(self.query_iri, params=params, headers=self.omi_get_headers, timeout=50)
        response = self.query(query)
        return response

    def ping(self):
        try:

            response = requests.post(self.ping_iri, headers=self.ping_headers, timeout=50)
            if response.status_code == 200:
                return "The OpenModel Knowledge Base is Alive!"
            else:
                return f"Unexpected status code: {response.status_code}"
        except requests.RequestException as e:
            return f"server down: {e}"

    # check if the server is online
    @property
    def is_online(self):
        try:

            response = requests.post(self.ping_iri, headers=self.ping_headers, timeout=50)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.RequestException as e:
            return f"Server down, exception obtained: {e}"

    def stats(self):
        response = requests.post(self.stats_iri, headers=self.ping_headers, timeout=50)
        return response.json()

    def update(self, query):
        response = requests.post(self.update_iri, data=query, headers=self.update_headers)
        if response.status_code == 200:
            print("SPARQL update executed successfully.")
        else:
            print(f"--Error: {response.status_code} - {response.text}")

    def import_ontology(self, source: Union[str, Path]) -> requests.Response:
        # should add graph name (default user;s named graph) 

        if not source:
            raise ValueError("Error - You must specify either a URL of an ontology or a file path as source!.")
        g = Graph()
        g.parse(source, format="turtle")
        ttl_data = g.serialize(format='turtle').encode('utf-8')
        # graph_url = f"{fuseki_url}/data?graph={graph_name}"

        response = requests.post(self.data_iri, data=ttl_data, headers=self.data_headers)
        if response.status_code in [200, 201, 204]:
            graph_name = "default"
            print(f"Successfully added {len(g)} triplets to the dataspace {graph_name} in the knowledge base.")
        else:
            print(f"failed to import ontology: {response.status_code}, {response.text}")

        return response

    def curl(self):
        curl_command = f"curl -X GET '{self.stats_iri}' " + \
                       " ".join([f"-H '{key}: {value}'" for key, value in self.omi_get_headers.items()])

        print(curl_command)

