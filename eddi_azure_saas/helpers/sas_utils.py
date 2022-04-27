
import numpy as np
import pandas as pd

from azure.storage.blob import BlobServiceClient
import requests
import os


def get_readonly_sas_link(filename, container_sas_link, directory_name='eddi_files'):
    """
    Returns a link to the data without dropping the file or any other change.
    """
    # container information
    blob_service_client = BlobServiceClient(account_url=container_sas_link.split('?')[0], credential=container_sas_link.split('?')[1])
    blob = blob_service_client.get_container_client(directory_name)

    # train-datasource is a sas link that is returned, for EDDI
    data_source = container_sas_link.split('?')[0] + '/' + directory_name + '/' + \
        os.path.basename(filename) + '?' + container_sas_link.split('?')[1]

    return data_source

def get_data_link(filepath, container_sas_link, directory_name='eddi_files'):
    """
    Get the link to the data.  Use this to replace the previous file with "filepath". 
    """
    # container information
    blob_service_client = BlobServiceClient(account_url=container_sas_link.split('?')[0], credential=container_sas_link.split('?')[1])
    blob = blob_service_client.get_container_client(directory_name)

    # train-datasource sas link
    data_source = container_sas_link.split('?')[0] + '/' + directory_name + '/' + \
        os.path.basename(filepath) + '?' + container_sas_link.split('?')[1]

    # del previous one
    requests.delete(data_source)

    # upload new one
    with open(filepath, "rb") as data:
        blob.upload_blob(data=data, name=os.path.basename(filepath), overwrite=True)

    return data_source

def get_placeholder_link(filepath, container_sas_link, directory_name='eddi_files', delete_prev=True):
    """
    Get the link to the data.
    """
    # datasource sas link
    data_source = container_sas_link.split('?')[0] + '/' + directory_name + '/' + \
        os.path.basename(filepath) + '?' + container_sas_link.split('?')[1]

    if delete_prev:
        # del previous one
        requests.delete(data_source)
    return data_source