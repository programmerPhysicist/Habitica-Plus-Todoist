# integration test for oneWaySync.py
import pytest
import os
import sys
# TODO: move PATH change to conftest.py file
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.join(dir_path, "../../source")
src_path = os.path.abspath(dir_path)
sys.path.insert(0, src_path)
from oneWaySync import sync_todoist_to_habitica
import requests

# TODO: unit tests
'''
def test_configFileMissing():
    with pytest.raises(SystemExit):
        sync_todoist_to_habitica()

def test_badConfigFile():
    sync_todoist_to_habitica()
'''

@pytest.fixture()
def config_file(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("config")
    cfgForTest = os.path.join(tmp, "auth.cfg")
    cfg = open(cfgForTest, 'w')
    L = ["[Habitica]\n", "url = https://habitica.com\n",
         "login = cd18fc9f-b649-4384-932a-f3bda6fe8102\n",
         "password = 18f22441-2c87-6d8e-fb2a-3fa670837b5a\n",
         "\n", "[Todoist]\n", 
         "api-token = d1347120363c2b310653f610d382729bd51e13c6\n", "\n"]
    cfg.writelines(L)
    cfg.close()
    os.chdir(tmp)

# custom class to be the mock return value
# will override the requests.Response returned from requests.get
class MockResponse:
    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def json():
        list1 = []
        task = {'text': '', 'priority': '', 'attribute': '', 'type': ''}
        list1.append(task)
        return {"data": list1}

def test_fulltest(config_file, monkeypatch):
    # Any arguments may be passed and mock_get() will always return our
    # mocked object, which only has the .json() method.
    def mock_get(*args, **kwargs):
        return MockResponse()

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    # using get_all_habtasks() which contains requests.get(), uses the monkeypatch
    sync_todoist_to_habitica()