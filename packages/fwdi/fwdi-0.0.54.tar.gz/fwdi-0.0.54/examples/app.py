import os
import sys
from pathlib import Path
sys.path.insert(0,str(Path(sys.path[0]).parent))

import pathlib
from datetime import datetime
from pydantic import BaseModel

from fwdi.Infrastructure.Rest.rest_client import RestClientFWDI, RestClientConfig

class RawDatasetViewModel(BaseModel):
    create_at:datetime = datetime.now()
    project_name:str
    filename:str
    data_type:str
    dataset:bytes

class RawUploaderDataset():

    def init(self, username:str, password:str):
        self.__username:str = username
        self.__password:str = password
        self.__rest_client:RestClientFWDI = None

        config = RestClientConfig()
        config.server = "localhost"
        config.port = 5003
        config.username = self.__username
        config.password = self.__password
        self.__rest_client = RestClientFWDI(config)
        if not self.__rest_client.IsAuth:
            is_login = self.__rest_client.login()
            if not is_login:
                raise Exception("Error login !")

    
    def upload_document(self, dataset_model:RawDatasetViewModel):
        try:
            if dataset_model is not None:

                response = self.__rest_client.post('/api/v1.0/dataset/raw', dataset_model)

                return response
            else:
                return None
        
        except Exception as ex:
            print(f"{ex}")

def load_raw_dataset(project_name:str, full_path:str)->RawDatasetViewModel:
    file_ext = pathlib.Path(full_path).suffix
    with open(full_path, 'rb') as file:
        raw_data = file.read()

    raw_file = os.path.basename(full_path)
    dataset = RawDatasetViewModel(project_name=project_name, filename=raw_file, data_type=file_ext, dataset=raw_data)
    return dataset

def sample_raw_upload(project_name:str, full_path:str):

    dataset_model:RawDatasetViewModel = load_raw_dataset(project_name, full_path)
    
    raw_uploader = RawUploaderDataset()
    raw_uploader.init("admin", "admin")
    result = raw_uploader.upload_document(dataset_model)

    print(result)

if __name__ == "__main__":
    sample_raw_upload('dit_sklad', 'examples/import/SourceData.pkl')