from web3 import Web3, HTTPProvider
from solc import compile_source
from web3.contract import ConciseContract

data = 0

w3 = Web3(HTTPProvider('http://127.0.0.1:8042'))

abi= '''[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"constant":false,"inputs":[{"internalType":"string","name":"_sensorData","type":"string"}],"name":"setSensorData","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getSensorData","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]'''

address = Web3.toChecksumAddress("0x85a89b1BdfF236F54056551967d5C450177004bF")

StoreSensorData = w3.eth.contract(address, abi = abi, ContractFactoryClass = ConciseContract)

host = Web3.toChecksumAddress("0x927a0d148f11d6fa6d1bcdaa7e3a6c862ccccdbd")

def readSensorData():
    return StoreSensorData.getSensorData(call = {'from':host})

data = readSensorData()

print(data)
