
from logs import get_transfer_logs,get_web3
from eth_abi import decode

w3 = get_web3()

current_block = w3.eth.block_number
data = get_transfer_logs(token_address="0x80B3214b38A233FFbd061273C2598B049025f397",from_block=12158522,to_block=12158522)

print(decode(["uint256"],(data[0].data)))