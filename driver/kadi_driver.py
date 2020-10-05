from kadi_apy.lib.core import KadiAPI
from kadi_apy.lib.records import Record
from kadi_apy.lib.collections import Collection
import json
import time
import pandas
import os

class kadi():
    def __init__(self,conf):
        KadiAPI.token = conf['PAT']
        KadiAPI.host = conf['host']

    def addRecord(self,ident,title,filed,meta,visibility='private'):
        #create a record
        #visibility must be 'public' or 'private'
        #meta must be serialized dict
        record = Record(identifier=ident,title=title,visibility=visibility,create=True)
        record.upload_string_to_file(string=filed,file_name='{}_{}.json'.format(ident,time.time_ns()))
        record.add_metadata(json.loads(meta),True)

    def addCollection(self,ident,title,visibility='private'):
        #create collection
        collection = Collection(identifier=ident,title=title,visibility=visibility,create=True)

    def addRecordToCollection(self,identCollection,identRecord):
        record = Record(identifier=identRecord)
        record.add_collection_link(Collection(identifier=identCollection).id)

    def linkRecordToGroup(self,identGroup,identRecord):
        record = Record(identifier=identRecord)
        record.add_group_role(identGroup,"editor")

    def linkCollectionToGroup(self,identGroup,identCollection):
        collection = Collection(identifier=identCollection)
        collection.add_group_role(identGroup,"editor")

    def recordExists(self,ident):
        #determine whether a record with the given identifier exists
        try:
            record = Record(identifier=ident)
        except:
            return False
        return True

    def addFileToRecord(self,identRecord,filed):
        #if file is a filepath, upload from that path, if file is a json, upload directly
        record = Record(identifier=identRecord)
        try: 
            json.loads(filed)
            record.upload_string_to_file(string=filed,file_name='{}_{}.json'.format(identRecord,time.time_ns()))
        except:
            record.upload_file(file_path=filed)

    def downloadFilesFromRecord(self,ident,filepath):
        #download all files from record
        record = Record(identifier=ident)
        response = record.get_filelist(per_page=100).json()
        for i in range(response['_pagination']['total_pages']):
            page = response = record.get_filelist(page=i,per_page=100).json()
            for item in page['items']:
                record.download_file(item['id'],os.path.join(filepath,item['name']))

    def downloadFilesFromCollection(self,ident,filepath):
        #download all files from all records in collection
        collection = Collection(identifier=ident)
        response = collection.get_records(per_page=100).json()
        for i in range(response['_pagination']['total_pages']):
            page = collection.get_records(page=i,per_page=100).json()
            for item in page['items']:
                self.downloadFilesFromRecord(item['identifier'],filepath)
