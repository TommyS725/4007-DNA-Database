from lib import utils
from typing import Union
import requests
import zipfile
import io



default_server = "http://localhost:8888"

server = default_server

def remote_init():
    global server
    answer = input(f"Please enter the data server url [{default_server}]: ")
    if len(answer) > 0:
        server = answer
    # print(f"Server address set to {server}")
    return


def upload_encrypted_document( document_id:str, encrypted_document:bytes):
    # 1. zip the encrypted document
    # 2. upload the encrypted and zipped document to the server
    document_id= str(document_id)
    print("Uploading document...")
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Write the data to the zip file with the document ID as the file name
        zipf.writestr(document_id, encrypted_document)
    zipped_data = data.getvalue()
    url = f"{server}/upload/{document_id}"
    headers = {'Content-Type': 'application/zip'}
    # Send the zipped data to the server as body of the POST request
    response = requests.post(url, data=zipped_data, headers=headers)
    success = response.status_code == 200
    if success:
        print("Document uploaded successfully!")
    else:
        print("Document upload failed!")
    return success

def download_encrypted_document(document_id:str)->Union[bytes, None]:
    # download the encrypted and zipped document from the server
    # unzip the document
    url = f"{server}/download/{document_id}"
    response = requests.get(url)
    print("Downloading document...")
    if response.status_code != 200:
        print("Document download failed!")
        return None
    zipped = response.content

    if zipped is None:
        print("Document downloaded is empty!")
        return None
    # unzip 
    try:
        with zipfile.ZipFile(io.BytesIO(zipped), 'r') as zipf:
            # Check if the zip file contains any files
            if not zipf.namelist():
                print("Zip file is empty!")
                return None
            # Assuming the document is the only file in the zip
            document_name = zipf.namelist()[0]
            document = zipf.read(document_name)
    except zipfile.BadZipFile:
        print("The downloaded data is not a valid zip file.")
        return None
    print("Document downloaded and unzipped successfully!")
    return document