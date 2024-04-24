# FTEC4007 Project - DNA Database with Blockchain
This project is a DNA Database system that uses Blockchain technology for secure and immutable storage of DNA data. It is implemented in Python and uses Ethereum smart contracts for the blockchain component.

## Group members: 
- Cheng Ka Lam 1155160005 
- Shum Ching Chit 1155159019 
- Yeung Ho Ching 1155143105 

## Overview
The project is divided into three main parts:

1. **Client**: This is where the DNA data is processed and sent to the server. It includes encrypting documents, revoking access,hashing, keys management, and remote connections.

1. **Server**: This is the sample storage server that receives DNA data from the client, stores the encrypted data.

1. **Contracts**: This contains the Ethereum smart contracts written in Solidity that are used to create the blockchain and handle transactions.


## Installation 
1. Clone the repository to your local machine.

2. Install the required Python packages for the client and server. Navigate to the `client` and `server` directories and run the following command:

```sh
pip install -r requirements.txt
```

3. Compile and deploy the Ethereum smart contracts in the `contracts`directory using tools like [Remix IDE](https://remix.ethereum.org/).

4. Run the server by navigating to the `server `directory and running the following command:
```sh
python app.py
```

5. Run the client by navigating to the client directory and running the following command:
```sh
pyhton client.py
```

Please note that you need to have Python and pip installed on your machine to run the project. Also, you need to have an Ethereum client like [Remix IDE](https://remix.ethereum.org/) to deploy the smart contracts.

## User Manual
Please follow the user manual in the project report submited.
