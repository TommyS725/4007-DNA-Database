from os import path
import os

data_path = None


def getPath(*paths):
    if not data_path:
        raise Exception("Data path not initialized")
    return path.join(data_path,*paths)

def initData(user:str):
    global data_path
    dataPath = path.join(path.dirname(path.abspath(__file__)), "..", "data",user)
    if not path.isdir(dataPath):
        os.makedirs(dataPath)
    data_path = dataPath
    dirs = ['access_key','document','document_key','encrypted_document','public_key','private_key','document_hash','key_hash']
    for dir in dirs:
        dir_path =getPath(dir)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)


def disPlayOptions(description:str, options:list[str], isMain:bool = False, showExit:bool = True):
    print(description)
    for i in range(len(options)):
        print(f"{i+1}. {options[i]}")
    if isMain and showExit:
        print("0. Exit")
    elif showExit:
        print("0. Back")
    print("Enter your choice: ", end="")
    while True:
        try:
            choice = int(input())
            break
        except ValueError:
            print("Invalid choice!")
            print("Enter your choice: ", end="")
    while choice < 0 or choice > len(options):
        print("Invalid choice!")
        print("Enter your choice: ", end="")
        choice = int(input())
    return choice


def requiredInput(description:str):
    print(description, end="")
    value = input().strip()
    while not value:
        print("Value cannot be empty!")
        print(description, end="")
        value = input().strip()
    return value


def reqiredFileInput(description:str):
    print(description, end="")
    value = input().strip()
    while not value or not path.isfile(value):
        print("Invalid file path!")
        print(description, end="")
        value = input().strip()
    return value



def requiredMultiLineInput(description:str ):
    print(description)
    print("Press Ctrl+D when you are done.")
    lines = []
    while not len(lines):
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
    return "\n".join(lines).strip()

