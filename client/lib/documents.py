from lib import utils
from os import path
import os

def getDocumentPath(docId:str):
    doc_name = f"{docId}.txt"
    return utils.getPath("document", doc_name)

def hasDocument(docId:str):
    return path.isfile(getDocumentPath(docId))


def saveDocument(docId:str, data:bytes):
    with open(getDocumentPath(docId), "wb") as f:
        f.write(data)
    return

def getEncryptedDocumentPath(docId:str):
    doc_name = f"{docId}.enc"
    return utils.getPath("encrypted_document", doc_name)

def saveEncryptedDocument(docId:str, data:bytes):
    with open(getEncryptedDocumentPath(docId), "wb") as f:
        f.write(data)
    return

def hasEncryptedDocument(docId:str):
    return path.isfile(getEncryptedDocumentPath(docId))


def getDocumentList():
    documentList = []
    for file in os.listdir(utils.getPath("document")):
        if file.endswith(".txt"):
            docId = file.split(".")[0]
            documentList.append(docId)
    return documentList