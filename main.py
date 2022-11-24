#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import FastAPI
from pathlib import Path
from typing import List,NewType,Union
from base.ville import Ville,Department,strip_accents
from base.crawler import Crawler
from utils.yaml_manager import YamlManger
from utils.custom_log import customLogging
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


log = customLogging(Path(__file__).stem)
VilleInfo = NewType('VilleInfo', dict['loyerMoyen': float,
                                      'globalNote': float,
                                      'name':str,
                                      'codePostal':str,
                                      'population':int])
            
source  = YamlManger("source.yaml").read_as_json()
loyer_data_url = source['LOYER_DATASET']['URL']
loyer_used_cols =source['LOYER_DATASET']['USED_COLS']
loyer_rename_cols = source['LOYER_DATASET']['RENAME_COLS']

@app.get(f"/")
def read_root()->str:
    return "Homepage"

@app.post("/search_loyer")
async def search_loyer(departement_number:Union[int, str],surface:int,loyer_maxime:int)-> List[VilleInfo]:
    """
    Return a list of cities corresponding the search condition 

    :params
        departement_number: code of department
        surface: surface souhaitée pour le logement
        loyer_maxime: loyer maximum

    :returns
        a list of cities meet the condition
    """
    crawler = Crawler(*source['API'].values())
    
    try:
        departement = Department(**crawler.getDepartment(**{'code':departement_number}))
        villes_notes = crawler.getDepartementCommunesNotes(strip_accents(departement.nom).lower())
        loyer_df = pd.read_csv(loyer_data_url,encoding="utf-8",usecols=loyer_used_cols)
    except Exception as e:
        log.error(f"Extarcting data failed: {e}")
    
    departement.villes = [Ville(**e) for e in villes_notes ]

    for v in departement.villes:
        commune = crawler.getCommune(**{'nom':v.nameUpperStripAccent})
        v.inseeCode,v.codePostal,v.population = commune['code'],commune['codesPostaux'][0],commune['population']
        
    lookup_list = [v.inseeCode for v in departement.villes]

    # Get loyer info 
    loyer_df.columns = loyer_rename_cols
    loyer_df.loc[:,'loyerMoyen']=round((loyer_df['loyerApparts']+loyer_df['loyerMaisons'])/2,2)

    target_communes = loyer_df.loc[loyer_df['inseeCode'].isin(lookup_list)].to_dict('records')

    for v in departement.villes:
        for commune in target_communes:
            if v.inseeCode == commune['inseeCode']:
                v.loyerMoyen=commune['loyerMoyen']


    # Filter with the surface/max_loyer from input
    after_filter = (v for v in departement.villes if v.loyerMoyen*surface<=loyer_maxime)
    result=[{'loyerMoyen':e.loyerMoyen,'globalNote':e.globalNote,'name':e.nameCaptitalizeAccent,'codePostal':e.codePostal,'population':e.population} for e in list(after_filter) ]
    log.info(f"Searching result for department {departement_number} (m2) with max loyer{loyer_maxime}:{result}")

    # Remove useless declaration
    del departement,lookup_list,villes_notes,target_communes,after_filter,commune
    return result
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)