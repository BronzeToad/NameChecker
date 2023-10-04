from typing import Dict, List, Optional, Union

import requests

import src.utilities as Utils
from src.utilities import ConfigType
from src.enum_factory import EnvType
from src.parent_checker import ParentChecker

# =========================================================================== #

class GitHubChecker(ParentChecker):

    def __init__(
        self,
        env_type: EnvType,
        names: Optional[List[str]] = None,
        batch_size: Optional[int] = None,
        max_retries: Optional[int] = None,
        limit: Optional[int] = None
    ):
        super().__init__(env_type, names, batch_size, max_retries, limit)
        self.__post_init__()


    def __post_init__(self):
        self.api_url = Utils.get_config_val('GitHub', 'BASE_API_URL')
        self.api_token = self.get_api_token()
        self.api_headers = self.get_api_headers()
        self.batches = Utils.create_batches(self.names, self.batch_size)


    def get_api_token(self):
        return Utils.get_config_val(
            section=self.env_type.value,
            key='GITHUB_TOKEN',
            config_type=ConfigType.SECRETS
        )


    def get_api_headers(self) -> Dict[str, str]:
        return {'Authorization': f"token {self.api_token}"}


    def check_username(self, username: str) -> bool:
        url = f"{self.api_url}{username}"

        try:
            response = requests.get(url=url, headers=self.api_headers)

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


    def check_batch(self,
                    batch: List[str]) -> List[Dict[str, Union[str, bool]]]:
        results = []

        for username in batch:
            is_available = self.check_username(username)
            results.append({'name': username, 'GitHub': is_available})

        return results


    def check(self) -> None:
        total_available = 0
        total_processed = 0

        for i, batch in enumerate(self.batches):
            print(f"\nProcessing batch {i + 1} of {len(self.batches)}...")
            print(f"Batch items: {batch}")
            results = self.check_batch(batch)

            batch_available = 0
            for item in results:
                if item['GitHub'] is True:
                    batch_available += 1

            total_available += batch_available
            total_processed += len(batch)

            self.save_results(results)

            batch_percent = 100 * batch_available // len(batch)
            total_percent = 100.0 * total_available / total_processed

            print(f"Batch: {batch_available} of "
                  f"{len(batch)} available ({batch_percent}%).")
            print(f"Total: {total_available} of "
                  f"{total_processed} available ({total_percent:.1f}%).")


# =========================================================================== #

if __name__ == '__main__':
    pass