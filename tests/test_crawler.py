import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import requests
from base.crawler import Crawler
from utils.yaml_manager import YamlManger

from faker import Faker

"""Write test cases here, for demo I just write some tests for crawler ..."""


faker = Faker()
source  = YamlManger("source.yaml").read_as_json()

def test_dataSourceDepartment():
    department_url = source['API']['DEPARTEMENT']
    response=requests.get(department_url)
    assert response.status_code ==200

def test_dataSourceCommune():
    commune_url = source['API']['COMMUNE']
    response=requests.get(commune_url)
    assert response.status_code ==200

def test_crawer_create():
    department_url,commune_url,note_url=faker.hostname(),faker.hostname(),faker.hostname()
    c = Crawler(department_url,commune_url,note_url)
    assert isinstance(c,Crawler)
    assert ( c.department_url== department_url and c.commune_url== commune_url and c.note_url== note_url)
    assert c.headers == {'accept': 'application/json'}


def test_crawer_getDepartmentDataByCode():

    c = Crawler(*source['API'].values())
    expected_data = {
        "nom": "Val-de-Marne",
        "code": "94",
        "codeRegion": "11"
        }
    assert c.getDepartment(**{'code':94}) == expected_data

""" To continue """