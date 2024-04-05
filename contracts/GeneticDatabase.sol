//SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0 <= 0.8.19;

import "./GeneticData.sol";


contract GeneticDatabase {

    address public  creater;

    //denote the joined user addr (has upload their public key)
    mapping(address=>bool) private  isJoined;

    //deote the users uploaded their data
    mapping(address=>bool) private hasData;

    mapping(address=>string) private publicKeys;

    mapping (address=>GeneticData) private dataStore;

    //event for a user joining the database
    event UserJoined(address _user, uint256 joinedAt);

    //event for a user uploading his data
    event UserUploaded(address _user, uint256 uploadedAt);

    //event for a user updating his public key
    event PublicKeyUpdated (address _user, uint256 updatedAt);

    //event for a user updating his data
    event GeneticDataUpdated (address _user, uint256 updatedAt);

    constructor(){
        creater = msg.sender;
    }

    function join(string memory _publicKey) public {
        require(isJoined[msg.sender]==false, "You have joined the database already");
        isJoined[msg.sender] = true;
        publicKeys[msg.sender] = _publicKey;
        emit UserJoined(msg.sender, block.timestamp);
    }

    function updatePublicKey(string memory _newKey) public {
        require(isJoined[msg.sender]==true, "You have not joined the database");
        publicKeys[msg.sender] = _newKey;
        emit PublicKeyUpdated(msg.sender, block.timestamp);
    }

    function uploadData(GeneticData _data) public {
        require(isJoined[msg.sender]==true, "You have to join the databse before uploading data");
        require(hasData[msg.sender]==false, "You have uploaded your data already");
        require(_data.getOwner()== msg.sender,"You have to be the owner of the data");
        dataStore[msg.sender] = _data;
        hasData[msg.sender] = true;
        emit UserUploaded(msg.sender, block.timestamp);
    }

    function updateData(GeneticData _data) public {
        require(isJoined[msg.sender]==true, "You have to join the databse before uploading data");
        require(hasData[msg.sender]==true, "You have not uploaded your data");
        require(_data.getOwner()== msg.sender,"You have to be the owner of the data");
        dataStore[msg.sender] = _data;
        emit GeneticDataUpdated(msg.sender, block.timestamp);
    }

    function checkHasJoined(address _user) public view returns(bool){
        return isJoined[_user];
    }

    function checkHasJoined() public view returns(bool){
        return isJoined[msg.sender];
    }

    function checkHasData(address _user) public view returns(bool){
        return hasData[_user];
    }

    function checkHasData() public view returns(bool){
        return hasData[msg.sender];
    }


    function getGeneticData(address _user) public  view  returns(GeneticData){
        require(hasData[_user]==true, "User has no uploaded data");
        return dataStore[_user];
    }

    function getPublicKey(address _user) public  view returns(string memory){
        require(isJoined[_user]==true, "User did not join the database");
        return publicKeys[_user];
    }

}