from unittest.mock import patch

import pytest

from src.domain_checker import DomainChecker

class MockResponse:
    def __init__(self, json_data, status_code, text):
        self.json_data = json_data
        self.status_code = status_code
        self.text = text

    def json(self):
        return self.json_data

def test_domain_checker_init_host_names(domain_checker, env_type):
    assert domain_checker.host_names == ['TestName']

def test_domain_checker_init_env_type(domain_checker, env_type):
    assert domain_checker.env_type == env_type

def test_domain_checker_init_endings(domain_checker, env_type):
    assert domain_checker.endings == ['com']

def test_set_max_retries(domain_checker):
    domain_checker._set_max_retries(5)
    assert domain_checker.cfg.godaddy_max_retries == 5

def test_get_api_headers_authorization(domain_checker):
    headers = domain_checker.get_api_headers()
    assert "Authorization" in headers
    assert "sso-key" in headers["Authorization"]

def test_get_api_headers_accept(domain_checker):
    headers = domain_checker.get_api_headers()
    assert "Accept" in headers
    assert headers["Accept"] == "application/json"

@pytest.mark.parametrize('host_names, endings', [
    ('TestName', 'com'),
    ('TestName', ['com']),
    ('TestName', ['com', 'net']),
    (['TestName'], 'com'),
    (['TestName'], ['com']),
    (['TestName'], ['com', 'net']),
    (['TestName', 'FakeHost'], 'com'),
    (['TestName', 'FakeHost'], ['com']),
    (['TestName', 'FakeHost'], ['com', 'net'])
])
def test_get_domains_(env_type, host_names, endings):
    domain_checker = DomainChecker(
        host_names=host_names,
        env_type=env_type,
        endings=endings,
        test_mode=True
    )
    domains = []
    for hostname in host_names:
        for ending in endings or []:
            domains.append(f"{hostname}.{ending}")
    assert sorted(domain_checker.get_domains()) == sorted(domains)

@patch('requests.get', return_value=MockResponse({"available": True}, 200, ""))
def test_check_domain_success(mock_get, domain_checker):
    assert domain_checker.check_domain('TestName.com') is True
    mock_get.assert_called_once()

@patch('requests.get', return_value=MockResponse({}, 429, "TOO_MANY_REQUESTS"))
def test_check_domain_too_many_requests(mock_get, domain_checker):
    assert domain_checker.check_domain('TestName.com') is False
    assert mock_get.call_count == 3

@patch('requests.get', return_value=MockResponse({"available": True}, 200, ""))
def test_check_domains():
    pass