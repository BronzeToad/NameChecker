import time
from typing import Dict, List, Optional, Union

import requests

import src.utilities as Utils
from src.enum_factory import EnvType
from src.name_checker import NameChecker
from src.utilities import ConfigType


# =========================================================================== #

class DomainChecker(NameChecker):

    def __init__(
        self,
        env_type: EnvType,
        names: Optional[List[str]] = None,
        batch_size: Optional[int] = None,
        max_retries: Optional[int] = None,
        limit: Optional[int] = None,
        domain_endings: Optional[List[str]] = None
    ):
        super().__init__(env_type, names, batch_size, max_retries, limit)
        self.domain_endings = domain_endings
        self.__post_init__()


    def __post_init__(self):
        self.api_url = self.get_api_url()
        self.api_key = self.get_api_key()
        self.api_secret = self.get_api_secret()
        self.api_headers = self.get_api_headers()
        self.domain_endings = self.domain_endings or ['com']
        self.domains = self.get_domains()
        self.batches = Utils.create_batches(self.domains, self.batch_size)


    def get_api_url(self) -> str:
        return Utils.get_config_val(
            section='GoDaddy',
            key=self.env_type.name + '_API_URL'
        )


    def get_api_key(self) -> str:
        return Utils.get_config_val(
            section=self.env_type.value,
            key='GODADDY_API_KEY',
            config_type=ConfigType.SECRETS
        )


    def get_api_secret(self) -> str:
        return Utils.get_config_val(
            section=self.env_type.value,
            key='GODADDY_API_SECRET',
            config_type=ConfigType.SECRETS
        )


    def get_api_headers(self) -> Dict[str, str]:
        return {
            'Authorization': f"sso-key {self.api_key}:{self.api_secret}",
            'Accept': 'application/json'
        }


    def get_domains(self):
        domains = []
        for name in self.names:
            for ending in self.domain_endings:
                domains.append(f"{name}.{ending}")
        return domains


    def check_domain(self, domain: str) -> bool:
        endpoint = f"{self.api_url}?domain={domain}"

        for _ in range(self.max_retries):
            response = requests.get(endpoint, headers=self.api_headers)

            if response.status_code == 200:
                data = response.json()
                return data['available']

            if 'TOO_MANY_REQUESTS' in response.text:
                print("ERROR: TOO_MANY_REQUESTS -> pausing for 30 seconds...")
                time.sleep(30)
            else:
                print(f"ERROR: {response.status_code} -> {response.text}")
                return False

        print(f"ERROR: Failed to fetch data after {self.max_retries} retries.")
        return False


    def check_batch(self,
                    batch: List[str]) -> List[Dict[str, Union[str, bool]]]:
        json_results = []
        calc_results = []

        for domain in batch:
            is_available = self.check_domain(domain)
            host_name, domain_ending = domain.rsplit('.', 1)
            json_results.append({'name': host_name, domain: is_available})
            calc_results.append({'name': host_name, 'domain': is_available})

        return json_results, calc_results


    def check(self) -> None:
        total_available = 0
        total_processed = 0

        for i, batch in enumerate(self.batches):
            print(f"\nProcessing batch {i + 1} of {len(self.batches)}...")
            print(f"Batch items: {batch}")
            json_results, calc_results = self.check_batch(batch)

            batch_available = 0
            for item in calc_results:
                if item['domain'] is True:
                    batch_available += 1

            total_available += batch_available
            total_processed += len(batch)

            self.save_results(json_results)

            batch_percent = 100 * batch_available // len(batch)
            total_percent = 100.0 * total_available / total_processed

            print(f"Batch: {batch_available} of "
                  f"{len(batch)} available ({batch_percent}%).")
            print(f"Total: {total_available} of "
                  f"{total_processed} available ({total_percent:.1f}%).")


# =========================================================================== #

if __name__ == '__main__':
    from icecream import ic

    checker = GoDaddy(env_type=EnvType.PRD)

    ic(checker.env_type)
    ic(checker.names)
    ic(checker.batch_size)
    ic(checker.max_retries)
    ic(checker.api_url)
    ic(checker.api_key)
    ic(checker.api_secret)
