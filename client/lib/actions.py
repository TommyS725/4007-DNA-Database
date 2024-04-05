from lib import utils
from lib import keys
from lib import documents
from lib import remote
from lib import hash
import uuid


def login()->str:
    print("Enter your address: ", end="")
    address = input().strip()
    while not address:
        print("Address cannot be empty!")
        print("Enter your address: ", end="")
        address = input().strip()
    print("Login successful!")
    return address
    
    
def checkKeys(address:str):
    unexistKey = []
    hasPublicKey = keys.hasPublicKey(address)
    hasPrivateKey = keys.hasPrivateKey(address)
    if not hasPublicKey:
        unexistKey.append("public key")
    if not hasPrivateKey:
        unexistKey.append("private key")
    if len(unexistKey) > 0:
        print(f"Your account is missing {' and '.join(unexistKey)}")
        print('Do you want to generate them?')
        if(hasPrivateKey or hasPublicKey):
            print(f"IMPORTANT: If you generate a new key pair, the old key pair will be lost.")
        choice = utils.disPlayOptions("Choose an option", ["Yes", "No"], showExit=False)
        if choice == 1:
            print("Generating keys...")
            keys.generate_asymmetric_key_pair(address)
            print("Keys generated successfully!")
        else:
            print("Please return when you are ready.")
            exit(0)
            
            
def showDocumentList(user:str):
    documentList = documents.getDocumentList()
    if len(documentList) == 0:
        print("No documents found!")
        return
    print("Documents:")
    for docId in documentList:
        print(docId)
    return

def checkDocumentInfo(user:str):
    docId = utils.requiredInput("Enter the document ID: ")
    hasDocument = documents.hasDocument(docId)
    if not hasDocument:
        print("Document not found!")
        return
    hasDocumentHash = hash.hasDocumentHash(docId)
    if not hasDocumentHash:
        print("Document hash not found!")
        return
    hasKeyHash = hash.hasKeyHash(docId)
    if not hasKeyHash:
        print("Document key hash not found!")
        return
    documentHash = hash.getDocumentHash(docId)
    keyHash = hash.getKeyHash(docId)
    print("Document ID:")
    print(docId)
    print("Document Hash:")
    print(documentHash)
    print("Key Hash:")
    print(keyHash)
                 
def encrypt_and_upload_document(user:str):
    file = utils.reqiredFileInput("Enter the path to your DNA data: ")
    docId = uuid.uuid4()
    key = keys.generate_symmetric_key(docId)
    with open(file, "rb") as f:
        data = f.read()
        encrypted_data = keys.encrypt_document(data, key)
        keyHash = hash.generate_key_hash(key)
        documentHash = hash.generate_document_hash(data)
        uploaded = remote.upload_encrypted_document(docId, encrypted_data)
        if not uploaded:
            return
        documents.saveDocument(docId,data)
        documents.saveEncryptedDocument(docId, encrypted_data)
        keys.saveDocumentKey(docId, key)
        hash.save_key_hash(docId, keyHash)
        hash.save_document_hash(docId, documentHash)
    print("Document encrypted and uploaded successfully!")
    print("Document ID:")
    print(docId)
    print("Document Hash:")
    print(documentHash)
    print("Key Hash:")
    print(keyHash)
    return

def add_encrypted_document(user:str):
    docId = utils.requiredInput("Enter the document ID: ")
    data = remote.download_encrypted_document(docId)
    if data is None:
        print("Document not found!")
        return
    document_hash = utils.requiredInput("Enter the document hash: ")
    key_hash = utils.requiredInput("Enter the key hash: ")
    hash.save_document_hash(docId, document_hash)
    hash.save_key_hash(docId, key_hash)
    documents.saveEncryptedDocument(docId, data)
    print("Encrypted document added successfully!")
    return


def decrypt_document(user:str):
    docId = utils.requiredInput("Enter the document ID: ")
    hasEncryptedDocument = documents.hasEncryptedDocument(docId)
    if(not hasEncryptedDocument):
        print("Document not found!")
        return
    hasDocumentKey = keys.hasDocumentKey(docId)
    if(not hasDocumentKey):
        print("Document key not found!")
        return
    hasDocumentHash = hash.hasDocumentHash(docId)
    if(not hasDocumentHash):
        print("Document hash not found!")
        return
    with open(documents.getEncryptedDocumentPath(docId), "rb") as f:
        encrypted_data = f.read()
        key = keys.getDocumentKey(docId)
        decrypted_data = keys.decrypt_document(encrypted_data, key)
        verified = hash.verify_document_hash(docId, decrypted_data)
        if not verified:
            print("Document hash verification failed!")
            return
        documents.saveDocument(docId, decrypted_data)
    print("Document decrypted successfully!")
    return

def give_access(user:str):
    docId = utils.requiredInput("Enter the document ID: ")
    if not keys.hasDocumentKey(docId):
        print("Document key not found!")
        return
    target_address = utils.requiredInput("Enter the user's address: ")
    if not keys.hasPublicKey(target_address):
        print("User's public key not found!")
        return
    encrypted_key = keys.encrypt_document_key_with_public_key(docId, target_address)
    keys.saveAccessKey(docId,target_address,encrypted_key)
    print("Access key generated successfully!")
    print(f"Document ID: {docId}")
    print(f"User address: {target_address}")
    print("Accesss key in base64:")
    print(keys.accessKeyToBase64(encrypted_key))
    return


def revoke_access(user:str):
    hasOwnPrivateKey   =  keys.hasPrivateKey(user)
    if not hasOwnPrivateKey:
        print("Your private key not found!")
        return
    docId = utils.requiredInput("Enter the document ID: ")
    if not hash.hasKeyHash(docId):
        print("Document key hash not found!")
        return
    access_key_base64 = utils.requiredInput("Enter the access key in base64: ")
    access_key = keys.accessKeyFromBase64(access_key_base64)
    document_key = keys.decrypt_access_key_with_private_key(user, access_key)
    verified = hash.verify_key_hash(docId, document_key)
    if not verified:
        print("Document key hash verification failed!")
        return
    keys.saveAccessKey(docId, user, access_key)
    keys.saveDocumentKey(docId, document_key)
    print("Access revoked successfully!")
    pass

def show_own_public_key(user:str):
    if not keys.hasPublicKey(user):
        print("Public key not found!")
        print("Please restart the program and generate a new key pair.")
        return
    public_key = keys.getPublicKey(user)
    key_str = keys.public_key_as_string(public_key)
    print("Public key:")
    print(key_str)
    pass

def add_public_key(user:str):
    target_address = utils.requiredInput("Enter the user's address: ")
    if keys.hasPublicKey(target_address):
        print("User's public key already exists.")
        choice = utils.disPlayOptions("Do you want to replace it?", ["Yes", "No"],showExit=False)
        if choice == 1:
            print("Replacing public key...")
        else:
            return
    public_key = keys.read_public_key_from_input()
    keys.savePublicKey(target_address, public_key)
    print("Public key added successfully!")
    pass