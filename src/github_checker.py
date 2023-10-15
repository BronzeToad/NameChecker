from typing import Dict, List

import requests

from src.utils.config_helper import ConfigHelper


# =============================================================================================== #

class GitHubChecker:

    def __init__(self, usernames: List[str], config_helper: ConfigHelper) -> None:
        self.usernames = usernames
        self.cfg = config_helper


    def check_username(self, username: str) -> bool:
        """Check the availability of a single username."""
        endpoint = f"{self.cfg.github_api_url}{username}"
        headers = {'Authorization': f"token {self.cfg.github_token}"}

        try:
            response = requests.get(url=endpoint, headers=headers)

            if response.status_code == 404:
                return True
            elif response.status_code == 200:
                return False
            else:
                print(f"ERROR: {response.status_code} -> {response.text}")
                return False

        except Exception as e:
            print(f"ERROR: {e}")
            return False


    def check(self) -> List[Dict[str, bool]]:
        """Check the availability of all usernames and return the results."""
        results = []

        for username in self.usernames:
            is_available = self.check_username(username)
            results.append({'name': username, 'GitHub': is_available})

        return results
