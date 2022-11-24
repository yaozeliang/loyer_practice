#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass,field
from typing import Union,AnyStr,List
import unicodedata

"""
Ville class
"""
StrOrNone = Union[AnyStr, None]
IntOrNone = Union[int, None]


@dataclass
class Ville:
    nameCaptitalizeAccent:str=''
    inseeCode:str=''
    nameUpperAccent:str = field(init=False)
    nameUpperStripAccent:str = field(init=False)
    nameLowerAccent:str = field(init=False)
    nameLowerStripAccent:str = field(init=False)
    codePostal:StrOrNone=None
    population:IntOrNone=None
    globalNote:float=0.0
    loyerMoyen:float=0.0

    
    def __post_init__(self)->None:
        self.nameUpperAccent = self.nameCaptitalizeAccent.upper()
        self.nameUpperStripAccent = strip_accents(self.nameCaptitalizeAccent).upper().replace("-"," ")
        self.nameLowerAccent = self.nameCaptitalizeAccent.lower()
        self.nameLowerStripAccent = strip_accents(self.nameCaptitalizeAccent).lower()

        
    def __doc__(self)->str:
        return "This is the City class, fields are from data source: https://api.gouv.fr/documentation/api-geo"


@dataclass
class Department:
    nom:str=''
    code:str=''
    codeRegion:str=''
    villes:list=field(init=False)


def strip_accents(text:str)->str:
    """
    Strip accents from input String.

    :param text: The input string.
    :returns: The processed String.
    """
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)