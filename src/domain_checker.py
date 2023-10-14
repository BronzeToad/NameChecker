import time
from typing import Dict, List, Optional

import requests

from cfg.config_helper import ConfigHelper


# =============================================================================================== #


class DomainChecker:
    def __init__(
        self,
        host_names: List[str],
        config_helper: ConfigHelper,
        max_retries: Optional[int] = None,
        endings: Optional[List[str]] = None,
    ) -> None:
        self.host_names = host_names
        self.cfg = config_helper
        self.max_retries = max_retries
        self.endings = endings
        self.__post_init__()

    def __post_init__(self) -> None:
        """Post initialization to set class properties."""
        self.max_retries = self.get_max_retries()
        self.endings = self.endings or ["com"]
        self.domains = self.get_domains()
        self.api_headers = self.get_api_headers()

    def get_max_retries(self) -> int:
        """Get the maximum number of retries allowed."""
        if self.max_retries is None or self.max_retries <= 0:
            return self.cfg.godaddy_max_retries
        else:
            return self.max_retries

    def get_api_headers(self) -> Dict[str, str]:
        """Generate the API headers required for the GoDaddy API request."""
        api_key = self.cfg.godaddy_api_key
        api_secret = self.cfg.godaddy_api_secret

        return {
            "Authorization": f"sso-key {api_key}:{api_secret}",
            "Accept": "application/json",
        }

    def get_domains(self) -> List[str]:
        """Generate the list of domains to check."""
        domains = []
        for hostname in self.host_names:
            for ending in self.endings or []:
                domains.append(f"{hostname}.{ending}")
        return domains

    def check_domain(self, domain: str) -> bool:
        """Check the availability of a single domain."""
        endpoint = f"{self.cfg.godaddy_api_url}?domain={domain}"

        for _ in range(self.max_retries or 0):
            response = requests.get(endpoint, headers=self.api_headers)

            if response.status_code == 200:
                data = response.json()
                return data["available"]

            if "TOO_MANY_REQUESTS" in response.text:
                print("ERROR: TOO_MANY_REQUESTS -> pausing for 30 seconds...")
                time.sleep(30)
            else:
                print(f"ERROR: {response.status_code} -> {response.text}")
                return False

        print(f"ERROR: Failed to fetch data after {self.max_retries} retries.")
        return False

    def check(self) -> List[Dict[str, bool]]:
        """Check the availability of all domains and return the results."""
        results = []

        for domain in self.domains:
            is_available = self.check_domain(domain)
            host_name, domain_ending = domain.rsplit(".", 1)
            results.append({"name": host_name, domain: is_available})

        return results
