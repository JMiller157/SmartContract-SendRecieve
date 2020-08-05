from web3 import Web3, HTTPProvider
from solc import compile_source
from web3.contract import ConciseContract


#IP and port number of the node.
#In this case the code and the node are both on the pi
w3 = Web3(HTTPProvider('http://127.0.0.1:8042'))

#ABI of the contract
abi= '''[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"constant":false,"inputs":[{"internalType":"string","name":"_sensorData","type":"string"}],"name":"setSensorData","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getSensorData","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]'''

#Address of the contract
address = Web3.toChecksumAddress("0x85a89b1BdfF236F54056551967d5C450177004bF")

#Varible to make calling the contract easier
StoreSensorData = w3.eth.contract(address, abi = abi, ContractFactoryClass = ConciseContract)

#account of the node on the raspi use geth attach and call eth.coinbase
raspi = Web3.toChecksumAddress("0xc6eb9b055483e6a2b5ad82d7da9ac87bf3e544f6")


# submitSensorData calls the function of the same name from the smart contract
def submitSensorData(data):
    StoreSensorData.setSensorData((data), transact = {'from':raspi})

#Gets the data from the file created by the sensor code
datafile = open('temperatureData', 'r')

#Type casts the data file as a string
datastring = str(datafile.read())

#Submits the data to the SmartContract
submitSensorData(datastring)
