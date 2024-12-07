from copy import deepcopy
from typing import Literal, NamedTuple, Union
from dataclasses import dataclass
from enum import Enum
import re
import xml.etree.ElementTree as ET
import logging

NS = {"xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "message": "http://www.sdmx.org/resources/sdmxml/schemas/v3_0/message",
        "str": "http://www.sdmx.org/resources/sdmxml/schemas/v3_0/structure",
        "com": "http://www.sdmx.org/resources/sdmxml/schemas/v3_0/common"
        }

INVALID = '!_INVALID_'


class MapType(Enum):
   OneToOne = 0
   OneToMany = 1
   ManyToOne = 2
   ManyToMany = 3

class Action(Enum):
   Information = 'I'
   Append = 'A'
   Replace = 'R'
   Delete = 'D'
   Merge = 'M'

class SourceField(NamedTuple):
  isRegEx: bool
  value: str   


@dataclass
class Dataflow():
   urn: str
   isexternalreference: bool
   agencyID: str
   id: str
   version: str
   datastructure: str

   def __init__(self, elem: ET.Element) -> None:
      self.urn = elem.get('urn')
      if elem.get('isExternalReference') == 'false': 
         self.isexternalreference = False
      else:
         self.isexternalreference = True
      self.agencyID = elem.get('agencyID')
      self.id = elem.get('id')
      self.version = elem.get('version')
      self.datastructure = elem.find('str:Structure', namespaces=NS).text

   @property
   def fullid(self):
      return f'{self.agencyID}:{self.id}({self.version})'   
     


@dataclass
class DataStructure():
   urn: str
   isexternalreference: bool
   agencyID: str
   id: str
   version: str
   dimensions: list[dict]

   def __init__(self, elem: ET.Element) -> None:
      self.urn = elem.get('urn')
      if elem.get('isExternalReference') == 'false': 
         self.isexternalreference = False
      else:
         self.isexternalreference = True
      self.agencyID = elem.get('agencyID')
      self.id = elem.get('id')
      self.version = elem.get('version')

      self.dimensions = [] 
      for dimensions_element in elem.findall('*/str:DimensionList/str:Dimension', namespaces=NS) + elem.findall('*/str:DimensionList/str:TimeDimension', namespaces=NS):
         # TODO add localrepresentation: type [Enumeration vs Typeinfo]
         # If Enumeration, build a set of codelist member IDs, so that basic implicit mapping validation can happen
         # Later Types could also be checked against their defining regex (But for that we would need an SDMX source library in Python)
         dimension = {k: dimensions_element.get(k) for k in ['id', 'position']}
         
         cl = dimensions_element.find('str:LocalRepresentation/str:Enumeration', namespaces=NS)
         if cl is not None:
            dimension['is_enumerated'] = True
            dimension['codelist_urn'] = cl.text
         else:
            dimension['is_enumerated'] = False      
         self.dimensions.append(dimension)
      
      self.attributes = []
      for attribute_element in elem.findall('*/str:AttributeList/str:Attribute', namespaces=NS):
         attribute = {k: attribute_element.get(k) for k in ['id', 'usage']}

         cl = attribute_element.find('str:LocalRepresentation/str:Enumeration', namespaces=NS)
         if cl is not None:
            attribute['is_enumerated'] = True
            attribute['codelist_urn'] = cl.text
         else:
            attribute['is_enumerated'] = False      
         
         at = attribute_element.find('str:AttributeRelationship/str:Observation', namespaces=NS)
         if at is not None:
            attribute['attachment_level'] = "observation"
         else:
            attribute['attachment_level'] = "partialkey"

         self.attributes.append(attribute)

   def isdimension(self, dimension) -> bool:
      for d in self.dimensions:
         if d['id'] == dimension:
            return True
      return False
   
   def isattribute(self, attribute) -> bool:
      for d in self.attributes:
         if d['id'] == attribute:
            return True
      return False
   
   def enumerated(self, component) -> Union[str, None]:
      for d in self.dimensions + self.attributes:
         if d['id'] == component and d['is_enumerated']:
            return d['codelist_urn']
      return None

   def dim_list(self) -> list:
      return [d['id'] for d in self.dimensions]

   def attr_list(self, attribute_type: Literal['observation','partialkey', 'all'] = 'all') -> list:
      match attribute_type:
         case 'all':
            return [a['id'] for a in self.attributes]      
         case 'observation':
            return [a['id'] for a in self.attributes if a['attachment_level'] == 'observation']
         case 'partialkey':
            return [a['id'] for a in self.attributes if a['attachment_level'] == 'partialkey']
      return []

@dataclass
class Codelist():
   id: str
   urn: str
   members: set[str]

   def __init__(self, elem: ET.Element) -> None:
      self.urn = elem.get('urn')
      self.id = elem.get('id')
      self.members = {k.get('id') for k in elem.findall('str:Code', namespaces=NS)} 

@dataclass
class StructureMap():
   source: str 
   target: str
   target_type: str = ''
   target_id: str = '' 
   
   def __init__(self, elem: ET.Element) -> None:
      self.source = elem.find('str:Source', namespaces=NS).text
      self.target = elem.find('str:Target', namespaces=NS).text
      p = re.compile(r'.*datastructure\.(.+)=(.+:.+\([0-9]+\.[0-9]+\))')
      m = p.match(self.target)      
      if m:
         self.target_type, self.target_id = m.groups()
     

@dataclass
class ComponentMap():
   sources: list[str]
   targets: list[str]
   type: MapType
   implicit: bool
   representation: str = ''
  
   def __init__(self, elem: ET.Element) -> None:
      sl = list(elem.findall('str:Source', namespaces=NS))
      self.sources = ['_S_'+e.text for e in sl]

      tl = list(elem.findall('str:Target', namespaces=NS))
      self.targets = [e.text for e in tl]

      rm = elem.findall('str:RepresentationMap', namespaces=NS)
      if rm:
            self.representation = rm[0].text
            self.implicit = False
      else:
            self.implicit = True

      if len(sl)==1:
            if len(tl)==1:
               self.type = MapType.OneToOne
            else:
               self.type = MapType.OneToMany
      else:
         if len(tl)==1:
            self.type = MapType.ManyToOne
         else:
            self.type = MapType.ManyToMany


@dataclass
class FixedValueMap():
   value: str
   target: str
  
   def __init__(self, elem: ET.Element) -> None:
      self.target = elem.find('str:Target', namespaces=NS).text
      self.value = elem.find('str:Value', namespaces=NS).text


@dataclass
class RepresentationMap():
   urn: str
   isexternalreference: bool
   mappings: list
   target_component_count: int

   def __init__(self, elem: ET.Element) -> None:
      self.urn = elem.get('urn')

      if elem.get('isExternalReference') == 'false': 
         self.isexternalreference = False
      else:
         self.isexternalreference = True

      self.target_component_count = len(elem.findall('str:TargetCodelist', namespaces=NS)) + len(elem.findall('str:TargetDataType', namespaces=NS))

      self.mappings = [] 
      for rm in elem.findall('str:RepresentationMapping', namespaces=NS):
         rmd = {'sourcevalues': [], 'targetvalues': []}
         for sv in rm.findall('str:SourceValue', namespaces=NS):
            if 'isRegEx' in sv.attrib.keys():
               rmd['sourcevalues'].append(SourceField(value=sv.text, isRegEx=bool(sv.attrib['isRegEx'])))
            else:   
               rmd['sourcevalues'].append(SourceField(value=sv.text, isRegEx=False))   
               
         for tv in rm.findall('str:TargetValue', namespaces=NS):
            rmd['targetvalues'].append(tv.text)
         
         padding = self.target_component_count - len(rmd['targetvalues'])
         # TODO - revise padding strategy, code is error prone for cases when multiple optional attributes are presented and they are not in last position in the target mapping
         # in any case such attributes should preferably be mapped separately
         for _ in range(padding):
            rmd['targetvalues'].append(None)
         self.mappings.append(deepcopy(rmd))

   # @deprecated   
   # def _replace_matches(self, matching_groups: tuple, target_list: list[str]) -> list[str]:
   #    #print("replacement checks:", matching_groups, target_list)
   #    sp = re.compile(r'(\\[1-9])')
   #    for idx, val in enumerate(target_list):
   #       if val:
   #          sm = sp.match(val)
   #          if sm: 
   #             for x in sm.groups():
   #                print(val, sm.groups(), matching_groups)
   #                # index correction to allow end-user to use 1 based indexing for matching groups
   #                target_list[idx] = val.replace(x, matching_groups[int(x[1])-1], 1) 
   #    return target_list

   def get_target_values_by_sourcelist(self, sourcelst: Union[tuple[str], str]) -> Union[list[str], None]:
         if isinstance(sourcelst, str):
            sourcelst = (sourcelst,)
         
         for m in self.mappings:
            
            pairs = zip(m['sourcevalues'], sourcelst)      
            matched = True
            target = m['targetvalues']
            
            # assumption: only one of the fields in source has RegEx with substitution 
            for pair in pairs:
               if pair[0].isRegEx:
                  p = re.compile(pair[0].value)
                  matches = p.match(pair[1])
                  if matches:
                     #target = self._replace_matches(matches.groups(), deepcopy(target))
                     target = [re.sub(pair[0].value,'' if t is None else t, pair[1], 1,re.MULTILINE) for t in target]                
                  else: 
                     matched = False
               else:
                  if pair[0].value != pair[1]:
                     matched = False
            
            if matched:
               logging.debug(f"produced target: {target} for pair {m['sourcevalues']}, {sourcelst}")
               return target
         
         if any([s!='' for s in sourcelst]):
            return [INVALID] * len(self.mappings[0]['targetvalues'])
         else:
            return [''] * len(self.mappings[0]['targetvalues'])   