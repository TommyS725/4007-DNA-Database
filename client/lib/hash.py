import hashlib
from lib import utils

def hash(input_bytes:bytes)->str:
    hash_object = hashlib.sha256(input_bytes)
    hex_dig = hash_object.hexdigest()
    return hex_dig

def getDocumentHashPath(docId:str):
    hash_name = f"{docId}.hash"
    return utils.getPath("document_hash", hash_name)

def getDocumentHash(docId:str)->str:
    with open(getDocumentHashPath(docId), "r") as f:
        return f.read()

def hasDocumentHash(docId:str)->bool:
    return utils.path.isfile(getDocumentHashPath(docId))

def generate_document_hash(decrypted_document:bytes)->str:
    document_hash = hash(decrypted_document)
    return document_hash


def save_document_hash(docId:str,documentHash:str):
    with open(getDocumentHashPath(docId), "w") as f:
        f.write(documentHash)
    return 



def verify_document_hash(docId:str, decrypted_document:bytes)->bool:
    document_hash = hash(decrypted_document)
    return document_hash == getDocumentHash(docId)

def getKeyHashPath(docId:str):
    hash_name = f"{docId}_key.hash"
    return utils.getPath("key_hash", hash_name)

def getKeyHash(docId:str)->str:
    with open(getKeyHashPath(docId), "r") as f:
        return f.read()

def hasKeyHash(docId:str)->bool:
    return utils.path.isfile(getKeyHashPath(docId))

def generate_key_hash(key:bytes)->str:
    key_hash = hash(key)
    return key_hash

def save_key_hash(docId:str,key_hash:str):
    with open(getKeyHashPath(docId), "w") as f:
        f.write(key_hash)
    return

def verify_key_hash(docId:str, key:bytes)->bool:
    key_hash = hash(key)
    return key_hash == getKeyHash(docId)

    
