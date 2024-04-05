from os import path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

import base64
from lib import utils


def publicKeyPath(id:str):
    key_name = f"{id}_rsa.pem"
    return utils.getPath("public_key", key_name)

def privateKeyPath(id:str):
    key_name = f"{id}_rsa.pem"
    return utils.getPath("private_key", key_name)

def hasPublicKey(id:str):
    return path.isfile(publicKeyPath(id))

def hasPrivateKey(id:str):
    return path.isfile(privateKeyPath(id))

def getPublicKey(id:str):
    with open(publicKeyPath(id), "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
        )
    return public_key

def getPrivateKey(id:str):
    with open(privateKeyPath(id), "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )
    return private_key

def savePublicKey(id:str, key:str):
    with open(publicKeyPath(id), "wb") as key_file:
        key_file.write(key.encode())

def documentKeyPath(docId:str):
    key_name = f"{docId}_key.key"
    return utils.getPath("document_key", key_name)

def hasDocumentKey(docId:str):
    return path.isfile(documentKeyPath(docId))

def getDocumentKey(docId:str):
    with open(documentKeyPath(docId), "rb") as key_file:
        key = key_file.read()
    return key

def generate_asymmetric_key_pair(id:str):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

 
    # Save the private key to a file
    with open(privateKeyPath(id), "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Save the public key to a file
    with open(publicKeyPath(id), "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))
        
def saveDocumentKey(docId:str, key:bytes):
    with open(documentKeyPath(docId), "wb") as key_file:
        key_file.write(key)
    return
        
def generate_symmetric_key(docId:str):
    key = Fernet.generate_key()
    return key


def encrypt_document(document:bytes, key:bytes):
    cipher = Fernet(key)
    encrypted_document = cipher.encrypt(document)
    return encrypted_document
 
 
def decrypt_document(encrypted_document:bytes, key:bytes)->bytes:
    cipher = Fernet(key)
    document = cipher.decrypt(encrypted_document)
    return document


def getAccessKeyPath(docId:str, address:str):
    key_name = f"{docId}_{address}_access.key"
    return utils.getPath("access_key", key_name)

def hasAccessKey(docId:str, address:str):
    return path.isfile(getAccessKeyPath(docId, address))

def getAccessKey(docId:str, address:str):
    with open(getAccessKeyPath(docId, address), "rb") as key_file:
        key = key_file.read()
    return key

def saveAccessKey(docId:str, address:str, key:bytes):
    with open(getAccessKeyPath(docId, address), "wb") as key_file:
        key_file.write(key)
    return

def accessKeyFromBase64(base64_key:str):
    return base64.b64decode(base64_key)

def accessKeyToBase64(key:bytes):
    return base64.b64encode(key).decode()

def encrypt_document_key_with_public_key(docId:str, address:str):
    document_key = getDocumentKey(docId)
    public_key = getPublicKey(address)
    encrypted_key = public_key.encrypt(
        document_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_key


def decrypt_access_key_with_private_key (address:str, access_key:bytes):
    private_key = getPrivateKey(address)
    document_key = private_key.decrypt(
        access_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return document_key


def format_public_key_from_singleline_input(singleline_key:str,line_length: int = 64):
    
    key_body = singleline_key.replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", "").strip()
    key_body = key_body.replace(" ", "")
    # Break the key into lines of the specified length
    key_lines = [key_body[i:i+line_length] for i in range(0, len(key_body), line_length)]
    
    # Reassemble the key
    formatted_key = "-----BEGIN PUBLIC KEY-----\n" + "\n".join(key_lines) + "\n-----END PUBLIC KEY-----"
    
    return formatted_key


def read_public_key_from_input():
    while True:
        print("Enter the public key: ")
        print("Press Ctrl+D when you are done.")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
                pass
        if len(lines) == 1:
            key =format_public_key_from_singleline_input(lines[0])
        else:
            key = "\n".join(lines).strip()
        if not key.startswith("-----BEGIN PUBLIC KEY-----") or not key.endswith("-----END PUBLIC KEY-----"):
            print("Invalid public key format. The key should start with '-----BEGIN PUBLIC KEY-----' and end with '-----END PUBLIC KEY-----'.")
            continue
        return key
    
    
def public_key_as_string(public_key:RSAPublicKey):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem.decode('utf-8')
