#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from typing import List
from dataclasses import dataclass,field

@dataclass
class Crawler:
    department_url:str = ''
    commune_url:str = ''
    note_url:str=''
    headers: dict = field(default_factory=lambda:{'accept': 'application/json'})

    def getDepartment(self,**kwargs)->dict:
        departement = requests.get(self.department_url,headers=self.headers,params=kwargs).json()[0]
        return departement


    def getCommune(self,**kwargs)->dict:
        commune = requests.get(self.commune_url,headers=self.headers,params=kwargs).json()[0]
        return commune

    def getDepartementCommunesNotes(self,department_name:str)->List[dict]:

        result=[]
        html_doc = requests.get(self.note_url.format(department_name)).text
        table = BeautifulSoup(html_doc, 'html.parser').find('table')
        for row in table.tbody.find_all('tr'):
            columns = row.find_all('td')
            if(columns!= []):
                ville_name = columns[1].text.split(" (")[0]
                note = float(columns[2].text.strip())
                result.append({"nameCaptitalizeAccent":ville_name,"globalNote":note})
        del html_doc,table
        return result

