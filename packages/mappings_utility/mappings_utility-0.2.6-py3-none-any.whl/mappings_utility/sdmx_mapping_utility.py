from typing import Literal, Union, Dict, List
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import requests
from pathlib import Path
from copy import deepcopy
from pydantic import RootModel
import logging

from mappings_utility.sdmx_structures import NS, INVALID, ComponentMap, DataStructure, Dataflow, FixedValueMap, MapType, RepresentationMap, StructureMap, Action, Codelist

INVALID_TARGET = '!_INVALID_TARGET'

class KeyRange(RootModel):
    root: Dict[str, List[str]]
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


# Partial key mapping utility working with SDMX 3.0 structure-set and representation mapping objects
class SDMXMappingUtility():

   def __init__(self, mapping_tree: ET.ElementTree , source_file: Union[Path, None]  = None, json: Union[KeyRange, None] = None, sid_based: bool = False):
         self.source_file = source_file
         self.mapping_tree = mapping_tree
         self.json = json
         self._read_mapping()
         if source_file:
            self._read_source('csv', sid_based)
         elif json:
            self._read_source('json', sid_based)
      
   @classmethod
   def initialise_with_registry(cls, registry_url: str, source_file: Path, sid_based: bool = False):
      headers = {
         'accept': 'application/vnd.sdmx.structure+xml;version=3.0'
      }
      response = requests.get(registry_url, headers=headers)
      response.raise_for_status()
      return cls(ET.ElementTree(ET.fromstring(response.content)), source_file, sid_based=sid_based)

   @classmethod
   def initialise_with_jsonandregistry(cls, registry_url: str, json: KeyRange,  sid_based: bool = False):
      headers = {
         'accept': 'application/vnd.sdmx.structure+xml;version=3.0'
      }
      response = requests.get(registry_url, headers=headers)
      response.raise_for_status()
      return cls(ET.ElementTree(ET.fromstring(response.content)), json=json, sid_based=sid_based)

   @classmethod
   def initialise_with_file(cls, mapping_file: Path, source_file: Path, sid_based: bool = False):
      return cls(ET.parse(mapping_file), source_file, sid_based=sid_based)         
               

   def _read_mapping(self):
      logging.info('reading mapping objects...')
      try:
         root = self.mapping_tree.getroot()

         dataflow_elements = root.findall('*/str:Dataflows/str:Dataflow', namespaces=NS)
         self.dataflows = [Dataflow(e) for e in dataflow_elements]

         datastructure_elements = root.findall('*/str:DataStructures/str:DataStructure', namespaces=NS) 
         self.datastructures = [DataStructure(e) for e in datastructure_elements]

         struct_map = root.find('*/str:StructureMaps/str:StructureMap', namespaces=NS)
         self.structure_map = StructureMap(struct_map)

         component_maps = list(struct_map.findall('str:ComponentMap', namespaces=NS))
         self.component_maps = [ComponentMap(e) for e in component_maps]

         fixedvalue_maps = list(struct_map.findall('str:FixedValueMap', namespaces=NS))
         self.fixedvalue_maps = [FixedValueMap(e) for e in fixedvalue_maps]

         representations = root.findall('*/str:RepresentationMaps/str:RepresentationMap', namespaces=NS)
         self.representation_maps = [RepresentationMap(e) for e in representations]

         codelists = root.findall('*/str:Codelists/str:Codelist', namespaces=NS)
         self.code_lists = [Codelist(e) for e in codelists]

      except Exception as err:
         logging.debug(str(err))
         raise err

   def _read_source(self, stype: Literal['csv', 'json'], sid_based: bool = False):
      logging.info('reading source file...')
      try:
         if stype == 'csv':
            df = pd.read_csv(self.source_file, dtype=str, na_filter=False)
         elif stype == 'json':
            print(self.json.root)
            df = pd.DataFrame.from_dict(self.json.root, dtype=str)
         else:
            raise ValueError
      except Exception as err:
         logging.debug(str(err))
         raise err

      if sid_based:
            dsd = self.get_dsd_by_urn(self.structure_map.source)
            source_cols = dsd.dim_list()
            df[source_cols] = df.SID.str.split('.', expand=True)

      self.df_source_partial_keys = self._source_data_cosmetics(df)

   def _source_data_cosmetics(self, df):
         df.rename(columns = {cn: '_S_'+cn for cn in df.columns}, inplace = True)
         # Add missing columns
         for cm in self.component_maps:
            for source in cm.sources:
               if source not in df.columns:
                  df[source] = ''
         return df 

   def get_representation_by_urn(self, urn: str) -> Union[RepresentationMap, None]:
      for x in self.representation_maps:
         if x.urn == urn:
            return x
      return None
   
   def get_codelist_by_urn(self, urn: str) -> Union[Codelist, None]:
      for x in self.code_lists:
         if x.urn == urn:
            return x
      return None


   # the urn to lookup could be that of a Dataflow or the DSD itself 
   def get_dsd_by_urn(self, urn: str) -> DataStructure:
      for df in self.dataflows:
         if df.urn == urn:
            for ds in self.datastructures:
               if ds.urn == df.datastructure:
                  return ds

      for dsd in self.datastructures:
         if dsd.urn == urn:
            return dsd

      return None                   

   # Generate mappings partial keys
   # includeSourceColumns: if true: both keys (from source and from target) will be in the dataframe
   #          false: only keys from target dataflow will be in the dataframe
   # includeAttributesMeasures: if true: all dimensions, attributes, and measures of the target dataflow will be in the dataframe
   #          false: only dimensions from target dataflow will be in the dataframe
   # nulledFixedTargets: if true: the targets with fixed representation will not be inserted (the expected behaviour when partial keys are mapped 
   #          for attribute and referential metadata attachment), false: for full data mappings
   # writeTargetStructInfo: if true: SDMX csv 3.0 style structural and action information will be writtern into the first columns of the generated file
   # dropInvalid: if true: non-mapped and source records containing invalid members will be dropped (in cases when the mapping acts as a filter)
   # sid_based: if true read SID as co-ordinates of the source dimensions in the correct order and deliver SID according to target
   

   def generate_mappings_partial_keys(self, includeSourceColumns=False, includeAttributesMeasures=False, nulledFixedTargets=False, writeTargetStructInfo=False, dropInvalid=False, sid_based=False):
      
         df = self.df_source_partial_keys
         dsd = self.get_dsd_by_urn(self.structure_map.target)
         action = Action.Information.value
         al = ['STRUCTURE', 'STRUCTURE_ID', 'ACTION']
         if writeTargetStructInfo:
            # Only one action per input file is supported !!! 
            if '_S_ACTION' in df.columns:
               if df['_S_ACTION'].iloc[0] in Action._value2member_map_: 
                  action = df['_S_ACTION'].iloc[0]
               else:
                  logging.warning(f'action code {df["_S_ACTION"].iloc[0]} was replaced by Information (I)') 
               
            df[al] = df.apply(lambda row: [self.structure_map.target_type.lower(), self.structure_map.target_id, action], axis=1, result_type='expand')

         # ComponentMaps
         for cm in self.component_maps:
            if cm.type in [MapType.OneToOne] and cm.implicit:
               # copy identical with target component-name
               logging.info(f'copying source to target {cm.sources} -> {cm.targets}')
               dim_enum = dsd.enumerated(cm.targets[0])
               if dim_enum:
                  # Empty string added to all code-lists, as a result mapping will not spot missing source members
                  # This behaviour is needed for partial key mappings
                  # TODO ponder if partial-key mapping and full mapping should be handled separately on a larger scale
                  cl = self.get_codelist_by_urn(dim_enum)
                  if cl:
                     cl_members = cl.members.union({''})
                     df[cm.targets[0]] = df[cm.sources[0]][df[cm.sources[0]].isin(cl_members)]
                     df[cm.targets[0]] = df[cm.targets[0]].fillna(INVALID_TARGET)
                  else:
                     #codelist lookup failed TODO throw error instead?
                     df[cm.targets[0]] = df[cm.sources[0]] 
               else:
                  df[cm.targets[0]] = df[cm.sources[0]]
            else:
               # only those cases can be mapped safely where there are valid inputs in all source columns
               logging.info(f'applying representation map {cm.sources} -> {cm.targets}')
               rm = self.get_representation_by_urn(cm.representation)
               try:
                  gdf = df[cm.sources].groupby(cm.sources, group_keys=True, as_index=False)
                  for k in gdf.groups.keys():
                     df.loc[gdf.groups[k], cm.targets] =  rm.get_target_values_by_sourcelist(k) 
               except:
                  logging.info(f'error in representation map {cm.sources} -> {cm.targets};\n {cm.representation};\n {df.head(2)}')  

         # Add target missing columns mapped as fixed value
         for fvm in self.fixedvalue_maps:
            logging.info(f'adding fixed component {fvm.target}')
            if not nulledFixedTargets:
               df[fvm.target] = fvm.value
            else:
               df[fvm.target] = ''

         if sid_based:
            df['SID'] = df.apply(lambda x: '.'.join([x[c] for c in dsd.dim_list()]), axis=1)

         # Remove source columns which are in the mappings and some technical columns      
         if not includeSourceColumns:
            # Get mapped source columns 
            source_columns = []
            for cm in self.component_maps:
               source_columns += cm.sources
            # Remove technical columns if they exist
            source_columns += ['_S_STRUCTURE', '_S_STRUCTURE_ID', '_S_ACTION', '_S_SID']
            # Create a filter from the "source_columns" that exists in df
            columns_todrop = df.filter(source_columns).columns
            # Drop the all columns in this list: columns_todrop
            df.drop(columns_todrop, axis=1, inplace=True)

         # Remove columns, which are not in the dimension list of the target dataflow
         # such as attributes and measures
         dsd = self.get_dsd_by_urn(self.structure_map.target)
         if sid_based:
            columns_to_drop = [column for column in df.columns if (not column =='SID' and not column.startswith("_S_") and not column in al)]
         else: 
            columns_to_drop = [column for column in df.columns if (not dsd.isdimension(column) and not column.startswith("_S_") and not column in al)]
            
         if not includeAttributesMeasures:
            df.drop(columns_to_drop, axis=1, inplace=True)
         elif action == Action.Delete.value:
            for c in columns_to_drop:
               df[c] = ''

         if dropInvalid:
            df = df[df.ne(INVALID).all(axis=1)] 
            df = df[df.ne(INVALID_TARGET).all(axis=1)]  

         return deepcopy(df)

