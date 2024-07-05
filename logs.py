

# function that get logs from web3 eth

from web3 import Web3
import json

#  import file erc20.json
with open('erc20.json') as f:
    erc20_abi = json.load(f)


class TransferLog:
    from_address: str
    to_address: str
    value: int
    block_number: int
    
    def __init__(self,from_address:str,to_address:str,value:int,block_number:int):
        self.from_address = from_address
        self.to_address = to_address
        self.value = value
        self.block_number = block_number

    def __str__(self):
        return f"Transfer from {self.from_address} to {self.to_address} value {self.value} block number {self.block_number}"

    def __repr__(self):
        return self.__str__()

w3 = Web3(Web3.HTTPProvider('https://sepolia.base.org'))

def get_web3():
    return w3

def get_transfer_logs(token_address,from_block=0,to_block="latest") -> list[TransferLog]:
    topic0 = w3.to_hex(w3.keccak(text="Transfer(address,address,uint256)"))
    # topic1 = "0x0000000000000000000000000000000000000000000000000000000000000000"
    # print(topic0,topic1)
    logs = w3.eth.get_logs({
        'fromBlock': from_block,
        'toBlock': to_block,
        'address': token_address,
        'topics': [topic0]
    })
    transfers = []
    for log in logs:
        # print(log['topics'][2])
        # print(log['topics'][2][-20:])
        transfer = TransferLog(
            from_address=w3.to_checksum_address(log['topics'][1][-20:]),
            to_address=w3.to_checksum_address(log['topics'][2][-20:]),
            value=int(w3.to_hex(log['data']), 16),
            block_number=log['blockNumber']
        )
        transfers.append(transfer)
    return transfers
