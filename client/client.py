
from lib import utils
from lib import actions
from lib import remote


def main():
    print( "Welcome to the DNA Database Client, please login to continue." )
    user = actions.login()
    utils.initData(user)
    actions.checkKeys(user)
    remote.remote_init()
    main_actions = [
        "Show document list",
        "Check document info",
        "Encrypt and upload a document",
        "Add an encrypted document",
        "Decrypt a document",
        "Give access to another user",
        "Revoke access from another user",
        "Show your public key",
        "Add other user's public key",
    ]
    while True:
        action = utils.disPlayOptions(f"Choose an action as {user}", main_actions, True)
        if(action == 0):
            print("Goodbye!")
            break
        switcher = {
            1: actions.showDocumentList,
            2: actions.checkDocumentInfo,
            3: actions.encrypt_and_upload_document,
            4: actions.add_encrypted_document,
            5: actions.decrypt_document,
            6: actions.give_access,
            7: actions.revoke_access,
            8: actions.show_own_public_key,
            9: actions.add_public_key,
        }
        switcher[action](user)
    return
    
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")