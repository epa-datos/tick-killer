"""
Tickspot API client class module
"""
import os
import logging
import requests
import pandas as pd


class KillTick:
    """API Requests client"""
    BASE_URL = "https://www.tickspot.com/99327/api/v2/"

    def make_request(self, method, url, params=None, data=None):
        """request gen"""
        if method == "GET":
            all_entries = []
            new_results = True
            page = 1

            while new_results:
                if params is None:
                    params = {'page': page}
                else:
                    params.update({'page': page})

                response = requests.request(
                    method,
                    f"{self.BASE_URL}/{url}",
                    params=params,
                    json=data,
                    headers={'Authorization': f"Token token={os.getenv('TICKSPOT_API_KEY')}",
                             'User-Agent': "MyCoolApp (jcorona@epa.digital)"}
                )
                response_body = {}
                try:
                    response_body = response.json()
                    new_results = len(response_body) > 0
                    page += 1
                    all_entries.extend(response_body)
                except ValueError:
                    logging.warning("Unexpected Response '%s' from '%s'",
                                    response.content, response.url)
            return pd.DataFrame.from_dict(all_entries)
        else:
            response = requests.request(
                method,
                f"{self.BASE_URL}/{url}",
                params=params,
                json=data,
                headers={'Authorization': f"Token token={os.getenv('TICKSPOT_API_KEY')}",
                         'User-Agent': "MyCoolApp (jcorona@epa.digital)"}
            )
            response_body = {}
            try:
                response_body = response.json()
            except ValueError:
                logging.warning("Unexpected Response '%s' from '%s'",
                                response.content, response.url)
            return response_body

    def get_clients(self):
        """Get tick clients"""
        return self.make_request("GET", "clients.json")

    def get_projects(self):
        """Get tick projects"""
        return self.make_request("GET", "projects.json")

    def get_tasks(self):
        """Get tick tasks"""
        return self.make_request("GET", "tasks.json")

    def get_entries(self, start_date, end_date):
        """Get all entries between 2 dates"""
        payload = {'start_date': start_date,
                   'end_date': end_date}
        return self.make_request(method="GET", url="entries.json", params=payload)

    def create_entry(self, data):
        """Post a tickspot entry"""
        return self.make_request("POST", "entries.json", data=data)

    def update_entry(self, entry_id, data):
        """Update given entry"""
        return self.make_request("PUT", f"entries/{entry_id}.json", data=data)
