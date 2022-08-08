"""
Class module
"""
from datetime import datetime, timedelta
import os
import logging
import requests
import pandas as pd


class KillTick:
    """General use class"""
    BASE_URL = "https://www.tickspot.com/99327/api/v2/"

    def make_request(self, method, url, params=None, data=None):
        """request gen"""
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
        return pd.DataFrame.from_dict(response_body)

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
