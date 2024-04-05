//SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0 <= 0.8.19;



contract GeneticData {

    address private   owner;

    string private  documentId ;

    string private  documentHash;

    string private  keyHash;

    uint256 private lastUpdatedAt;

    mapping(address => string) private  encryptedKeys;
    mapping(address=>bool) private hasAccess;

    //event for contract set up
    event GeneticDataCreated(address indexed  _owner,uint256 _createdAt );

    //event for updating document
    event GeneticDocumentUpdated(address indexed _owner, uint256 _updatedAt);

    //event for giving document access to other user
    event AccessGranted(address indexed _owner,address indexed _authorizedUser, uint256 _grantedAt);

    constructor (string memory _documentId, string memory _docHash, string memory _keyHash ){
        owner = msg.sender;
        documentId = _documentId;
        documentHash = _docHash;
        keyHash = _keyHash;
        lastUpdatedAt = block.timestamp;
        emit GeneticDataCreated(owner, block.timestamp);
    }

    function getOwner() view public  returns(address){
        return owner;
    }

    //output fomat documentId, doc hash, key hash
    function getDocument() view public returns(string memory, string memory, string memory)  {
        return (documentId,documentHash,keyHash);
    }

    function getLastUpdatedTimestamp() view public  returns(uint256){
        return lastUpdatedAt;
    }


    //the key used to encrypt the new docuemnt should be the same as before
    function updateEncryptedDocumen(string memory _documentId, string memory _docHash) public {
        require(msg.sender == owner, "You have to be the owner to modify the data"  );
        documentId = _documentId;
        documentHash = _docHash;
        lastUpdatedAt = block.timestamp;
        emit GeneticDocumentUpdated(msg.sender, block.timestamp);
    }

    //encryptedKey is the document key encrypted by authorizedUser's publick key in base64
    function grantAccess(address _authorizedUser, string memory encryptedKey) public {
        require(msg.sender == owner, "You have to be the owner to grant access to other"  );
        encryptedKeys[_authorizedUser] = encryptedKey;
        hasAccess[_authorizedUser] = true;
        emit AccessGranted(msg.sender, _authorizedUser, block.timestamp);
    }

    //check whether a specific user has access to the document
    function checkHasAccess(address _toCheck) view public returns(bool){
        return hasAccess[_toCheck];
    }

    //check wheteher the msg sender has access to the document
    function checkHasAccess() view public returns(bool){
        return hasAccess[msg.sender];
    }

    //get encrypted access key in base64
    function getEncryptedKey() view  public  returns(string memory){
        require(hasAccess[msg.sender],"You do not have access to the document");
        return (encryptedKeys[msg.sender]);
    }

}