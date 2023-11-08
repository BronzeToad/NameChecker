import time
from typing import Dict, List, Optional

import requests

from src.utils.config_helper import ConfigHelper, EnvType


# =============================================================================================== #


class DomainChecker:
    def __init__(
        self,
        host_names: List[str],
        env_type: EnvType,
        endings: Optional[List[str]] = None,
        max_retries: Optional[int] = None,
        test_mode: Optional[bool] = False
    ) -> None:
        self.host_names = host_names
        self.env_type = env_type
        self.endings = endings or ["com"]
        self.cfg = ConfigHelper(self.env_type, test_mode)
        self._set_max_retries(max_retries)
        self.domains = self.get_domains()
        self.api_headers = self.get_api_headers()

    def _set_max_retries(self, max_retries: int) -> int:
        """Get the maximum number of retries allowed."""
        if max_retries is not None:
            self.cfg.godaddy_max_retries = max_retries

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

        for _ in range(self.cfg.godaddy_max_retries or 0):
            response = requests.get(endpoint, headers=self.api_headers)

            if response.status_code == 200:
                data = response.json()
                return data["available"]

            if response.status_code == 429:
                print("ERROR: TOO_MANY_REQUESTS -> pausing for 30 seconds...")
                if not self.cfg.test_mode:
                    time.sleep(30)
            else:
                print(f"ERROR: {response.status_code} -> {response.text}")
                return False

        print(f"ERROR: Failed to fetch data after {self.cfg.godaddy_max_retries} retries.")
        return False

    def check(self) -> List[Dict[str, bool]]:
        """Check the availability of all domains and return the results."""
        results = []

        for domain in self.domains:
            is_available = self.check_domain(domain)
            host_name, domain_ending = domain.rsplit(".", 1)
            results.append({"name": host_name, domain: is_available})

        return results
